from scripts.processors.process_input import leer_carpeta, pd

def clean_enerkom_data():
    """Realiza la limpieza de los datos de Enerkom."""
    df = leer_carpeta().copy()
    col = df["Columna2"]
    # Aquí puedes agregar las operaciones de limpieza específicas que necesites
    #extrae el contenido dentro parentesis
    content_p = col.astype(str).str.extract(r'\[([^\]]+)\]',expand=False).astype("string").str.strip()
    # separa nombre y código (código = dígitos al final)
    parts = content_p.str.extract(r'^(?P<sucursal_nombre>.*?)(?P<sucursal_codigo>\d+)?$')
    parts = parts.astype('string').apply(lambda s: s.str.strip())
    #df['sucursal_full'] = content_p
    df['sucursal_nombre'] = parts['sucursal_nombre'].replace({'': pd.NA})
    df['sucursal_codigo'] = parts['sucursal_codigo'].replace({'': pd.NA})
    df['sucursal_numero'] = pd.to_numeric(df['sucursal_codigo'], errors='coerce').astype('Int64')
    return df                                              
    