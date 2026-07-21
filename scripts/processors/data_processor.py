# scripts/processors/data_processor.py
import pandas as pd
import re

def clean_column_names(df):
    """
    Limpia nombres de columnas:
    - Elimina BOM (\ufeff)
    - Elimina espacios extras
    """
    df.columns = [c.strip().lstrip('\ufeff') for c in df.columns]
    return df

def trim_values(df):
    """
    Elimina espacios en blanco al inicio y final de cada valor
    """
    for col in df.columns:
        if df[col].dtype == 'object':  # Solo para columnas de texto
            df[col] = df[col].astype(str).str.strip()
    return df

def filter_valid_rows(df, required_cols):
    """
    Filtra filas que tienen todas las columnas obligatorias
    Retorna: (df_validos, df_invalidos)
    """
    present = [c for c in required_cols if c in df.columns]
    
    if not present:
        return df.copy(), pd.DataFrame()
    
    mask = df[present].notna().all(axis=1)
    return df[mask].copy(), df[~mask].copy()

def clean_text_column(df, col_name):
    """
    Limpia una columna de texto específica:
    - Elimina caracteres especiales
    - Normaliza espacios
    """
    if col_name in df.columns:
        df[col_name] = df[col_name].astype(str).str.strip()
        df[col_name] = df[col_name].str.replace(r'\s+', ' ', regex=True)
    return df

def rename_column_if_exists(df, old_name, new_name):
    """
    Renombra una columna si existe
    """
    if old_name in df.columns:
        df.rename(columns={old_name: new_name}, inplace=True)
    return df

def drop_empty_columns(df, threshold=0.9):
    """
    Elimina columnas que están vacías en más del {threshold}% de las filas
    """
    for col in df.columns:
        if df[col].isna().sum() / len(df) > threshold:
            df.drop(columns=[col], inplace=True)
    return df

def convert_to_numeric(df, col_name):
    """
    Convierte una columna a numérico, manejando errores
    """
    if col_name in df.columns:
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    return df

def fill_missing_with_default(df, col_name, default_value):
    """
    Rellena valores nulos con un valor por defecto
    """
    if col_name in df.columns:
        df[col_name] = df[col_name].fillna(default_value)
    return df

def drop_columns(df, cols_to_drop):
    """
    Elimina columnas especificadas si existen
    """
    for col in cols_to_drop:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
    return df

def replace_values(df, col_name, old_values, new_values, verbose=True):
    """
    Reemplaza valores en una columna
    """
    if col_name in df.columns:
      if df[col_name].dtype == 'str':  # Solo para columnas de texto
        df[col_name] = df[col_name].astype(str).str.strip()
        df[col_name] = df[col_name].str.replace(old_values, new_values)
      else:
        df[col_name] = df[col_name].replace(old_values, new_values)
    return df 