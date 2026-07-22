from scripts.config import INPUT_PATH_GASOMATIC
from scripts.processors.process_input import leer_excel, pd


def clean_gasomatic_data():
    """Realiza la limpieza de los datos de Enerkom."""
    df = leer_excel(INPUT_PATH_GASOMATIC).copy()
    # dfmap = df2.copy()

    # Normalizar sufijos a AM/PM

    # Convertir a datetime (si falla, asigna NaT)
    df["Fecha Real"] = (
        df["Fecha Real"]
        .astype(str)
        .str.replace("\u00a0", " ", regex=False)  # NBSP -> espacio normal
        .str.replace(r"(?i)\bp\s*\.?\s*m\s*\.?\b", "PM", regex=True)  # p. m. -> PM
        .str.replace(r"(?i)\ba\s*\.?\s*m\s*\.?\b", "AM", regex=True)  # a. m. -> AM
        .str.replace(r"\s{2,}", " ", regex=True)  # colapsa espacios dobles
        .str.strip()
    )

    # for v in df["Fechahoraestacion"].astype(str).head(10):
    # print(repr(v))

    df["Fecha Real"] = (
        df["Fecha Real"].astype(str).str.replace("AM.", "AM").str.replace("PM.", "PM")
    )

    df["Fecha Real"] = pd.to_datetime(
        df["Fecha Real"], format="%d/%m/%Y %I:%M:%S %p", dayfirst=True, errors="coerce"
    )

    df["Fechahoraestacion"] = (
        df["Fechahoraestacion"]
        .astype(str)
        .str.replace("a. m.", "AM")
        .str.replace("p. m.", "PM")
    )

    df["Fechahoraestacion"] = pd.to_datetime(
        df["Fechahoraestacion"],
        format="%d/%m/%Y %I:%M:%S %p",
        dayfirst=True,
        errors="coerce",
    )

    #print(df.head(1))
    print(f'cantidad de datos de dataframe: {df["Codigo"].count()}')
    # df3 = df.merge(dfmap, left_on="NoEs", right_on="NOSUC", how="inner")
    # df = df3.drop(
    #     columns=[
    #         "NOSUC",
    #         "Columna1",
    #         "Columna2",
    #         "Columna3",
    #         "NoEs",
    #     ]
    # )
    df = df.rename(
        columns={
            "Fecha Real": "FechaReal",
            "idoperacion": "Idoperacion",
        }
    )
    df = df[df["NSurtidor"].notna()]

    # df3 = df3[["Sucursal"] + [c for c in df3.columns if c not in ("Sucursal")]]
    # print(
    #     f'cantidad de datos de dataframe que Tienen Sucursal Mapeada: {df3["Sucursal"].count()}'
    # )
    print(df["FechaReal"].head(1))
    return df
