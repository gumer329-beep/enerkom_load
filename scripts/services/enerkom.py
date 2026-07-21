from scripts.config import INPUT_PATH_ENERKOM
from scripts.processors.process_input import leer_excel, pd
def clean_enerkom_data():
    """Realiza la limpieza de los datos de Enerkom."""
    df = leer_excel(INPUT_PATH_ENERKOM).copy()
    col = df["Columna2"]
    # extrae el contenido dentro parentesis
    content_p = (
        col.astype(str)
        .str.extract(r"\[([^\]]+)\]", expand=False)
        .astype("string")
        .str.strip()
    )
    # separa nombre y código (código = dígitos al final)
    code = content_p.str.extract(r"(\d+)", expand=False)
    name = (
        content_p.str.replace(r"\d+", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # asignar columnas: texto con ceros, y numérico nullable para cálculos
    df["Sucursal"] = content_p
    # df["Sucursal"] = name.replace({"": pd.NA})
    df["NoEstacion"] = code.replace({"": pd.NA})
    df["Subtotal"] = 0
    df["Iva"] = 0
    df["Producto"] = df["Producto         Bomba"]
    # convierte "13/06/2026 11:18:23 a. m." -> "2026-06-13 11:18:23"
    df["Fecha"] = pd.to_datetime(
        df["Fecha"], format="%d/%m/%Y %I:%M:%S %p", errors="raise"
    ).dt.strftime("%Y-%m-%d %H:%M:%S")
    # df["sucursal_numero"] = pd.to_numeric(
    #     df["sucursal_codigo"], errors="coerce"
    # ).astype("Int64")

    df = df[
        ["Sucursal", "NoEstacion"]
        + [
            c
            for c in df.columns
            if c
            not in (
                "Sucursal",
                "NoEstacion",
                "Monto",
                "Precio Unit.",
                "Litros",
                "Subtotal",
                "Iva",
            )
        ]
        + ["Precio Unit.", "Litros", "Subtotal", "Iva", "Monto"]
    ]
    df = df.rename(
        columns={
            "#Trans": "Transaccion",
            "# Tarjeta": "NoTarjeta",
            "Columna3": "Tipo",
            "Producto": "Producto",
            "Precio Unit.": "PrecioUnitario",
            "Monto": "Total",
            # "Id_referencia": "Id_Referencia",
        }
    )
    df = df.drop(
        columns=[
            "Columna1",
            "Columna2",
            "Comision",
            "IVA Comision",
            "Total Comision",
            "Columna6",
            "Producto         Bomba",
            "Columna4",
            "Columna4",
            "Columna5",
        ],
        errors="ignore",
    )
    print(f'cantidad de datos de dataframe: {df["Sucursal"].count()}')
    # df3 = df.merge(dfidgm, left_on="Sucursal", right_on="Referencia", how="inner")
    # df3 = df3.drop(columns=["IDGM","IdFormaPago","IdSubFormaPago","Referencia","Estatus","CrtdDateTime"])
    # print(f'cantidad de datos de dataframe que Tienen IDReferencia: {df3["Sucursal"].count()}')
    return df