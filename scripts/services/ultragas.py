from scripts.config import INPUT_PATH_ULTRAGAS
from scripts.processors.process_input import leer_excel, leer_csv, pd
def clean_ultragas_data():
    """Realiza la limpieza de los datos de Enerkom."""
    df = leer_excel(INPUT_PATH_ULTRAGAS).copy()

    dfmap = leer_csv(INPUT_PATH_ULTRAGAS).copy()

    # convierte "13/06/2026 11:18:23 a. m." -> "2026-06-13 11:18:23"
    df["Fecha"] = (
        df["Fecha"]
        .astype(str)
        .str.replace("\u00a0", " ", regex=False)  # NBSP -> espacio normal
        .str.replace(r"(?i)\bp\s*\.?\s*m\s*\.?\b", "PM", regex=True)  # p. m. -> PM
        .str.replace(r"(?i)\ba\s*\.?\s*m\s*\.?\b", "AM", regex=True)  # a. m. -> AM
        .str.replace(r"\s{2,}", " ", regex=True)  # colapsa espacios dobles
        .str.strip()
    )

    # for v in df["Fechahoraestacion"].astype(str).head(10):
    # print(repr(v))

    df["Fecha"] = (
        df["Fecha"].astype(str).str.replace("AM.", "AM").str.replace("PM.", "PM")
    )
    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors="raise")
    print(df["Fecha"].head(2))

    df["NoEs"] = pd.to_numeric(df["NoEs"], errors="coerce").astype("Int64")
    df["No Transacción"] = pd.to_numeric(df["No Transacción"], errors="coerce").astype(
        "Int64"
    )
    df["No Cliente"] = pd.to_numeric(df["No Cliente"], errors="coerce").astype("Int64")
    df["No Vehículo"] = pd.to_numeric(df["No Vehículo"], errors="coerce").astype(
        "Int64"
    )
    # print(df.head(5))
    print(f'cantidad de datos de dataframe: {df["NoEs"].count()}')
    df3 = df.merge(dfmap, left_on="NoEs", right_on="NOSUC", how="inner")
    df3 = df3.drop(
        columns=[
            "NOSUC",
            "Columna1",
            "Columna2",
            "Columna3",
            "NoEs",
        ]
    )
    df3 = df3.rename(
        columns={
            "No Transacción": "NoTran",
            "No Cliente": "NoCliente",
            "No Vehículo": "NoVehiculo",
            "Litros": "NoLitros",
            "Pesos": "Importe",
            "SUCURSALW": "Sucursal",
        }
    )
    df3 = df3[["Sucursal"] + [c for c in df3.columns if c not in ("Sucursal")]]
    print(
        f'cantidad de datos de dataframe que Tienen Sucursal Mapeada: {df3["Sucursal"].count()}'
    )
    return df3