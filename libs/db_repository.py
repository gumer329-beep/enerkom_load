# scripts/repositories/db_repository.py
from scripts.config import FORMA_DE_PAGO, SUBFORMA_DE_PAGO
from scripts.services.clean_and_map import clean_invisible, normalize_text_for_map
from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from urllib.parse import quote_plus

load_dotenv()

DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': quote_plus(os.getenv('DB_PASSWORD')),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'table': os.getenv('DB_TABLE')
}


def get_db_connection():
    conn = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:3306/{DB_CONFIG['database']}?charset=utf8mb4"
    return create_engine(conn)

def execute_query(query, params=None):
    """Ejecuta una consulta en la BD"""
    engine = get_db_connection()
    with engine.connect() as conn:
        if params:
            result = conn.execute(text(query), params)
        else:
            result = conn.execute(text(query))
        return result

def get_table_columns():
    """Obtiene columnas de una tabla"""
    query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{DB_CONFIG['database']}' AND TABLE_NAME='{DB_CONFIG['table']}'"
    result = execute_query(query)
    return [r[0] for r in result]


def map_catalogs(df, mapping_configs, verbose=True):
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
        catalog = pd.read_sql(f"SELECT {id_col} AS {alias}, {rel_col} FROM {table} WHERE {forma_pago} = {FORMA_DE_PAGO} AND {subforma_pago} = {SUBFORMA_DE_PAGO}", get_db_connection())
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
            print(
                "Detén y añade equivalencias en 'mapping_configs' -> manual_map, o corrige el catálogo."
            )
            sys.exit(1)
        
        if verbose:
            print(f"✅ Mapeo '{col_csv}' completado.")
    
    return df


def get_max_id():
    """Obtiene máximo ID"""
    query = f"SELECT MAX(Id) FROM {DB_CONFIG['database']}.{DB_CONFIG['table']}"
    result = execute_query(query)
    return result.scalar() or 0

def get_db_sum(column, prev_id, new_id):
    """Obtiene suma de columna en rango de IDs"""
    query = f"SELECT SUM(`{column}`) FROM {DB_CONFIG['database']}.{DB_CONFIG['table']} WHERE Id > :prev AND Id <= :new"
    result = execute_query(query, {'prev': prev_id or 0, 'new': new_id or 0})
    return result.scalar() or 0

def check_duplicates(df, key_cols):
    """Detecta duplicados en BD"""
    print(f"🔑🔍 Verificando duplicados en BD para columnas: {key_cols}")
    if not key_cols or len(df) == 0:
        return df, pd.DataFrame()
    
    existing = set()
    with get_db_connection().connect() as conn:
        for _, row in df.iterrows():
            conditions = []
            params = {}
            for col in key_cols:
                if col in df.columns:
                    val = row[col]
                    if pd.isna(val):
                        conditions.append(f"{col} IS NULL")
                    else:
                        conditions.append(f"{col} = :{col}")
                        params[col] = val
            
            if conditions:
                q = f"SELECT * FROM {DB_CONFIG['table']} WHERE {' AND '.join(conditions)} LIMIT 1"
                if conn.execute(text(q), params).fetchone():
                    key = tuple(row[col] if not pd.isna(row[col]) else None for col in key_cols if col in df.columns)
                    existing.add(key)
    
    is_dup = df.apply(
        lambda row: tuple(row[col] if not pd.isna(row[col]) else None for col in key_cols if col in df.columns) in existing,
        axis=1
    )
    
    print(f"📌 Duplicados detectados: {is_dup.sum()}")
    return df[is_dup].copy(), df[~is_dup].copy()

def insert_data(df):
    """Inserta datos en BD"""
    if len(df) == 0:
        return 0
    
    # Convertir NaN/NaT a None (NULL en MariaDB)
    df = df.where(pd.notna(df), None)
    
    df.to_sql(
        name=DB_CONFIG['table'],
        con=get_db_connection(),
        if_exists='append',
        index=False,
        chunksize=500
    )
    return len(df)

def save_snapshot(df, output_dir, prefix):
    """Guarda snapshot CSV"""
    if len(df) == 0:
        return None
    ts = datetime.now().strftime('%Y%m%dT%H%M%S')
    path = os.path.join(output_dir, f"{prefix}_{ts}.csv")
    df.to_csv(path, index=False, encoding='utf-8-sig')
    return path


