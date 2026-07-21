# scripts/etl/pipeline.py
import sys
import os
import logging
import pandas as pd
from datetime import datetime
# Importar módulos ETL

#from scripts.config import   #NOT_NULL_COLS, DECIMAL_COLS, DATE_STRICT_COLS, MAPPING_ENABLED, MAPPING_CONFIGS, EXCLUDE_COLS, DUPLICATE_COLS, VALIDATIONS
from libs.db_repository import map_catalogs, get_table_columns, DB_CONFIG, get_max_id, get_db_sum, check_duplicates, insert_data, save_snapshot
from scripts.processors.data_processor import clean_column_names, trim_values, filter_valid_rows
from scripts.services.clean_and_map import normalize_dates, normalize_decimals


# ====== CONFIGURACIÓN FIJA ======
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIT_DIR = os.path.join(BASE_DIR, 'audit_insert_output')
LOGS_DIR = os.path.join(BASE_DIR, 'Logs')
POLICY_FILE = os.path.join(BASE_DIR, f"decimal_{DB_CONFIG["table"]}_policies.json")

os.makedirs(AUDIT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# ====== LOGGING ======
LOG_FILE = os.path.join(LOGS_DIR, f"import_{DB_CONFIG['table']}_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


# ====== PIPELINE ======
def run_pipeline(df, config, table_name, verbose=True):
    """Ejecuta el pipeline ETL completo"""
    
    verbose = True
    insert_success = False
    df_insert = None
    prev_max_id = None
    new_max_id = None
    # Configuración específica de la tabla
    NOT_NULL_COLS = config["not_null_cols"]
    DATE_STRICT_COLS = config["date_strict_cols"]
    DECIMAL_COLS = config["decimal_cols"]
    DUPLICATE_COLS = config["duplicate_cols"]
    VALIDATIONS = config["validations"]
    MAPPING_ENABLED = config.get("mapping_enabled", False)
    MAPPING_CONFIGS = config.get("mapping_configs", [])
    EXCLUDE_COLS = config["exclude_cols"]
    POLICY_FILE = os.path.join(BASE_DIR, f"decimal_{table_name}_policies.json")
    
    try:
        # ====== BLOQUE 0 ======
        if verbose:
            print("\n======================== BLOQUE 0: VARIABLES ========================")
            print(f"📌 Tabla destino: {table_name}")
            print(f"📌 Columnas NOT NULL: {NOT_NULL_COLS}")
            print(f"📌 Columnas decimales: {DECIMAL_COLS}")
            print(f"📌 Columnas fecha estrictas: {DATE_STRICT_COLS}")
            print(f"📌 Mapeos definidos: {[m['columna_csv'] for m in MAPPING_CONFIGS]}")
            print(f"📌 Mapeos activados: {MAPPING_ENABLED}")
            logger.info("Bloque 0 inicializado. Logging configurado en: %s", LOG_FILE)
        
        # ====== BLOQUE 1: LECTURA Y FECHAS ======
        if verbose:
            print("\n========================= BLOQUE 1: LECTURA CSV Y FECHAS =========================")
        
        # Normalizar columnas
        df = clean_column_names(df)
        df = trim_values(df)
        df.columns = [c.strip().lstrip('\ufeff') for c in df.columns]
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()
        
        if verbose:
            print("Columnas detectadas en DATAFRAME: 🗃️ ", list(df.columns))
            print("Filas totales:", len(df))
        
        # Fechas
        df = normalize_dates(df, DATE_STRICT_COLS, DATE_STRICT_COLS, verbose)
        df_validos, df_invalidos = filter_valid_rows(df, NOT_NULL_COLS)
        
        if verbose:
            print(f"✅ Válidas: {len(df_validos)}, Inválidas: {len(df_invalidos)}")
        
        # ====== BLOQUE 2: MAPEOS ======
        if MAPPING_ENABLED:
            df_validos = map_catalogs(df_validos, MAPPING_CONFIGS, verbose)
        else:
            if verbose:
                print("\n⚠️ Mapeos deshabilitados")
        
        # ====== DECIMALES ======
        df_validos = normalize_decimals(df_validos, DECIMAL_COLS, POLICY_FILE, verbose)
        
        # ====== BLOQUE 3: VALIDACIÓN DDL ======
        if verbose:
            print("\n========================= BLOQUE 3: VALIDACIÓN DDL =========================")
        
        maria_cols = get_table_columns(table_name)
        maria_cols_filtered = [c for c in maria_cols if c not in EXCLUDE_COLS]
        csv_cols = [c for c in df_validos.columns if c not in EXCLUDE_COLS]
        extras_csv = [c for c in csv_cols if c not in maria_cols_filtered]
        missing_in_csv = [c for c in maria_cols_filtered if c not in csv_cols]
        
        if verbose:
            print("📋 Validación de columnas:")
            print(f"   Columnas MariaDB: {len(maria_cols)}")
            print(f"   Columnas excluidas MariaDB: {len(EXCLUDE_COLS)}")
            print(f"   Columnas CSV detectadas: {len(csv_cols)}")
            print(f"📋 Columnas coincidentes: {len([c for c in csv_cols if c in maria_cols_filtered])}")
            if extras_csv:
                print(f"⚠️ Columnas extras en CSV: {extras_csv}")
            if missing_in_csv: 
                print(f"⚠️ Columnas faltantes en CSV: {missing_in_csv}")
            # Asegurar que IdSucursal esté presente si se mapeó
            if MAPPING_CONFIGS[0]["alias_destino"] in df_validos.columns and MAPPING_CONFIGS[0]["alias_destino"] not in maria_cols_filtered:
                print(f"⚠️ Atención: {MAPPING_CONFIGS[0]['alias_destino']} existe en CSV pero no en la tabla destino. Revisa DDL o mapeo.")
        cols_to_insert = [c for c in maria_cols_filtered if c in df_validos.columns]
        if MAPPING_CONFIGS[0]["alias_destino"]  in df_validos.columns and MAPPING_CONFIGS[0]["alias_destino"]  not in cols_to_insert:
                cols_to_insert.append("MAPPING_CONFIGS[0]['alias_destino']")
        if not cols_to_insert:
            print("❌ No hay columnas para insertar")
            sys.exit(1)

        print(f"✅ Filas válidas finales: {len(df_validos)}")
        print(f"⚠️ Filas inválidas finales: {len(df_invalidos)}")
        
        df_insert = df_validos[cols_to_insert].copy()
        
        # ====== BLOQUE 4: DEDUPLICACIÓN E INSERCIÓN ======
        if verbose:
            print("\n========================= BLOQUE 4: PREPARAR E INSERTAR =========================")
        
        prev_max_id = get_max_id(table_name)
        if prev_max_id is not None:
            print(f"🔎 MAX(Id) previo: {prev_max_id}")
        
        print(f"📊 Filas totales a evaluar: {len(df_insert)}")
        df_duplicates, df_insert_new = check_duplicates(
            df_insert, table_name, DUPLICATE_COLS
        )
        
        if len(df_duplicates) > 0:
            dup_file = save_snapshot(df_duplicates, AUDIT_DIR, 'duplicados_encontrados')
            print(f"📁 Duplicados: {dup_file}")
        
        df_insert = df_insert_new
        
        if len(df_insert) == 0:
            print("✅ No hay datos nuevos")
            sys.exit(0)
        
        # Snapshot pre-insert
        save_snapshot(df_insert, AUDIT_DIR, 'audit_pre_insert')
        print(f"📁 Snapshot pre-insert guardado")
        
        if verbose:
            print(f"\n📊 📋 Filas nuevas: {len(df_insert)}")
            print(f"📋 Columnas: {list(df_insert.columns)}")
        
        confirm = input("\n⚠️ Confirmar inserción (si/no): ").strip().lower()
        if confirm != 'si':
            print("❌ Cancelado")
            sys.exit(0)
        
        # Insertar
        count = insert_data(df_insert, table_name)
        print(f"✅ {count} filas insertadas")
        print("✅ Importación completada correctamente.")
        insert_success = True
        
        # ====== BLOQUE 5: POST-INSERT ======
        if verbose:
            print("\n========================= BLOQUE 5: POST-INSERT =========================")
        
        if insert_success:
            save_snapshot(df_insert, AUDIT_DIR, 'audit_post_insert')
            print(f"📁 Snapshot post-insert guardado")
            
            new_max_id = get_max_id(table_name)
            if new_max_id is not None:
                print(f"🔎 MAX(Id) después: {new_max_id}")
                if prev_max_id is not None:
                    inserted = int(new_max_id) - int(prev_max_id)
                    print(f"✅ Esperadas: {len(df_insert)}, Insertadas: {inserted}")
                    if inserted == len(df_insert):
                        print("🏁 Conteo OK")
                    else:
                        print("❗ Conteo DIFERENTE")
            
            # Validar sumas
            try:
                for col in VALIDATIONS.keys():
                    if col in df_insert.columns:
                        csv_sum = pd.to_numeric(df_insert[col], errors='coerce').sum()
                        db_sum = get_db_sum(col, table_name, prev_max_id, new_max_id)
                        diff = csv_sum - pd.to_numeric(db_sum, errors='coerce')
                        print(f"🔢 {col}: CSV={csv_sum:.2f} | DB={db_sum:.2f} | Diff={diff:.2f}")
                        if abs(diff) < 1e-6:
                            print(f"🏁 {col}: OK")
                        else:
                            print(f"❗ {col}: DIFERENCIA")
            except Exception as e:
                print(f"⚠️ Error en sumas: {e}")
        
        if verbose:
            print("\n========================= FIN DEL PROCESO =========================")
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.exception("Error en pipeline")
        sys.exit(1)