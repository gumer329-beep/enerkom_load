# scripts/etl/transform.py
from scripts.processors.data_processor import filter_valid_rows
import pandas as pd
import re
import unicodedata
import json
import sys
import os

def process_valid_rows(df, not_null_cols, verbose=True):
    """Filtra filas válidas usando data_processor"""
    
    # ✅ USAR DATA PROCESSOR
    df_validos, df_invalidos = filter_valid_rows(df, not_null_cols)
    
    if verbose:
        print(f"✅ Válidas: {len(df_validos)}, Inválidas: {len(df_invalidos)}")
    
    return df_validos, df_invalidos

def normalize_text_for_map(s):
    """Normaliza texto para mapeos"""
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = s.replace('’', "'").replace('‘', "'").replace('´', "'")
    s = re.sub(r'[^a-z0-9\s\-\']', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def clean_invisible(s):
    """Limpia caracteres invisibles"""
    if pd.isna(s):
        return ""
    s = str(s)
    s = (s.replace('\ufeff', '').replace('\u00a0', ' ')
         .replace('\u200b', '').replace('\u200e', '').replace('\u200f', ''))
    s = re.sub(r'[\x00-\x1F\x7F]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def parse_date(series):
    """Parsea fechas en múltiples formatos"""
    s = series.astype(str).str.strip().replace({'': pd.NA, 'nan': pd.NA, 'None': pd.NA})
    parsed = pd.to_datetime(s, errors='coerce', dayfirst=True)
    
    if parsed.isna().any():
        digits = s.str.replace(r'[^0-9]', '', regex=True)
        parsed2 = pd.to_datetime(digits, format='%Y%m%d', errors='coerce')
        parsed = parsed.fillna(parsed2)
    
    if parsed.isna().any():
        parsed2 = pd.to_datetime(s, errors='coerce')
        parsed = parsed.fillna(parsed2)
    
    return parsed.dt.strftime('%Y-%m-%d %H:%M:%S').where(parsed.notna(), pd.NA)

def normalize_number_str(x):
    """Convierte string a número"""
    if pd.isna(x) or str(x).strip() == '':
        return pd.NA
    s = re.sub(r'[^\d\-\+\.,\(\)]', '', str(x).strip())
    
    if re.match(r'^\(.*\)$', s):
        s = '-' + s.replace('(', '').replace(')', '')
    
    if re.match(r'^\d{1,3}(\.\d{3})+,\d+$', s):
        s = s.replace('.', '').replace(',', '.')
    elif re.match(r'^\d{1,3}(,\d{3})+\.\d+$', s):
        s = s.replace(',', '')
    elif ',' in s and '.' not in s and re.search(r',\d{1,2}$', s):
        s = s.replace(',', '.')
    else:
        s = s.replace(',', '')
    
    try:
        return float(s)
    except:
        return pd.NA

def normalize_dates(df, date_cols, strict_cols, verbose=True):
    """Normaliza columnas de fecha"""
    for col in date_cols:
        if col not in df.columns:
            continue
        
        formatted = parse_date(df[col])
        
        if col in strict_cols:
            n_bad = formatted.isna().sum()
            if n_bad > 0:
                samples = df.loc[formatted.isna(), col].unique()[:20].tolist()
                print(f"\n❌ ERROR: columna de fecha estricta '{col}' contiene {n_bad} valores no parseables.")
                for v in samples:
                    print(f"   - {v}")
                sys.exit(1)
            df[col] = formatted
            if verbose:
                print(f"✅ Columna estricta '{col}' formateada correctamente.")
        else:
            df[col] = formatted
    
    return df

def normalize_decimals(df, decimal_cols, policy_file=None, verbose=True):
    """Normaliza columnas decimales con políticas interactivas"""
    if verbose:
        print("\n======================== LIMPIEZA Y POLÍTICAS PARA DECIMALES =========================")
    
    # Cargar políticas
    col_policy = {}
    if policy_file and os.path.exists(policy_file):
        try:
            with open(policy_file) as f:
                col_policy = json.load(f)
        except:
            pass
    
    # Limpiar decimales
    for col in decimal_cols:
        if col in df.columns:
            df[f'__{col}__cleaned'] = df[col].apply(normalize_number_str)
    
    # Resumen de problemas
    problems = {col: df[f'__{col}__cleaned'].isna().sum() 
                for col in decimal_cols if col in df.columns}
    
    if verbose:
        print("Resumen problemas decimales:", problems)
        for col, n in problems.items():
            if n:
                samples = df.loc[df[f'__{col}__cleaned'].isna(), col].unique()[:5].tolist()
                print(f"⚠️ Muestra no convertibles en '{col}': {samples}")
    
    # Procesar cada columna
    show_menu = True
    for col, n_invalid in problems.items():
        if n_invalid == 0:
            df[col] = df[f'__{col}__cleaned']
            df.drop(columns=[f'__{col}__cleaned'], inplace=True)
            continue
        
        # Política
        if col in col_policy:
            action = col_policy[col]
            if verbose:
                print(f"Usando política guardada para '{col}': {action}")
        else:
            if show_menu:
                print("\nElige acción para esta columna:")
                print("  1) null   -> insertar NULL")
                print("  2) zero   -> rellenar con 0")
                print("  3) custom -> rellenar con valor personalizado")
                print("  4) abort  -> detener")
                show_menu = False
            
            samples = df.loc[df[f'__{col}__cleaned'].isna(), col].unique()[:5].tolist()
            print(f"\nColumna '{col}' tiene {n_invalid} errores. Muestra: {samples}")
            choice = input("Escribe 1/2/3/4 (enter=1): ").strip()
            
            if choice == "2":
                action = "zero"
            elif choice == "3":
                val = input("Valor: ").strip()
                action = f"custom:{val}"
            elif choice == "4":
                print("Abortando...")
                sys.exit(1)
            else:
                action = "null"
            
            if policy_file:
                save = input("¿Guardar política? (Si/No): ").strip().lower()
                if save == "si":
                    col_policy[col] = action
                    with open(policy_file, "w") as f:
                        json.dump(col_policy, f, indent=2)
        
        # Aplicar
        serie = pd.to_numeric(df[f'__{col}__cleaned'], errors='coerce')
        if action == "null":
            df[col] = serie.astype('Float64')
        elif action == "zero":
            df[col] = serie.fillna(0).astype('Float64')
        elif action.startswith("custom:"):
            try:
                df[col] = serie.fillna(float(action.split(':',1)[1])).astype('Float64')
            except:
                df[col] = serie.astype('Float64')
        else:
            df[col] = serie.astype('Float64')
        
        df.drop(columns=[f'__{col}__cleaned'], inplace=True)
    
    if verbose:
        print("✅ Decimales normalizados.")
    
    return df

def map_catalogs(df, mapping_configs, engine, verbose=True):
    """Mapea columnas contra catálogos"""
    if verbose:
        print("\n========================= BLOQUE 2: MAPEOS =========================")
    
    for cfg in mapping_configs:
        if not cfg.get('enabled', True):
            continue
        
        col_csv = cfg['columna_csv']
        table = cfg['tabla_catalogo']
        rel_col = cfg['columna_relacion_catalogo']
        id_col = cfg['columna_id_catalogo']
        alias = cfg['alias_destino']
        forma_pago = cfg["forma_pago"]
        subforma_pago = cfg["subforma_pago"]
        
        if verbose:
            print(f"\n--- Mapeo: '{col_csv}' -> {table}.{rel_col} (→ {alias})")
        
        # Leer catálogo
        catalog = pd.read_sql(f"SELECT {id_col} AS {alias}, {rel_col} FROM {table} WHERE {forma_pago} = 5 AND {subforma_pago} = 6", engine)
        catalog[rel_col] = catalog[rel_col].astype(str).apply(clean_invisible)
        catalog['__norm'] = catalog[rel_col].apply(normalize_text_for_map)
        
        # Preparar CSV
        df['__norm'] = df[col_csv].apply(normalize_text_for_map)
        
        # Merge
        df = df.merge(catalog[[alias, '__norm']], on='__norm', how='left')
        df.drop('__norm', axis=1, inplace=True)
        
        # Validar
        unmapped = df[alias].isna().sum()
        print(f"📌 Mapeados: {len(df) - unmapped}, No mapeados: {unmapped}")
        
        if unmapped > 0:
            samples = df.loc[df[alias].isna(), col_csv].unique()[:10].tolist()
            print(f"❌ Valores no mapeados: {samples}")
            sys.exit(1)
        
        if verbose:
            print(f"✅ Mapeo '{col_csv}' completado.")
    
    return df