from scripts.config import INPUT_PATH_ENERKOM, INPUT_PATH_AMEX
from scripts.processors.process_input import leer_excel, leer_csv_amex, pd
from scripts.services.clean_and_map import parse_date
from scripts.processors.data_processor import clean_column_names, trim_values

def clean_enerkom_data():
    """Realiza la limpieza de los datos de Enerkom."""
    df = leer_excel(INPUT_PATH_ENERKOM).copy()
    col = df["Columna2"]
    # Aquí puedes agregar las operaciones de limpieza específicas que necesites
    #extrae el contenido dentro parentesis
    content_p = col.astype(str).str.extract(r'\[([^\]]+)\]',expand=False).astype("string").str.strip()
    # separa nombre y código (código = dígitos al final)
    code = content_p.str.extract(r'(\d+)', expand=False)
    name = content_p.str.replace(r'\d+', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()
    # asignar columnas: texto con ceros, y numérico nullable para cálculos
    df['Sucursal'] = content_p
    #df["Sucursal"] = name.replace({"": pd.NA})
    df["NoEstacion"] = code.replace({"": pd.NA})
    df["Subtotal"] = 0
    df['IVA'] = 0
    df["Producto"] = df["Producto         Bomba"]
    # convierte "13/06/2026 11:18:23 a. m." -> "2026-06-13 11:18:23"
    df["Fecha"] = parse_date(df["Fecha"])
    df = df[["Sucursal","NoEstacion"] + [c for c in df.columns if c not in ("Sucursal","NoEstacion", "Monto", "Precio Unit.","Litros","Subtotal","IVA")]+["Precio Unit.","Litros","Subtotal","IVA","Monto"]]
    df = df.rename(
        columns={
            "Fecha": "FECHA",
            "#Trans": "TRANSACCION",
            "# Tarjeta": "TARJETA",
            "Columna3": "TIPO",
            "Producto": "PRODUCTO",
            "Precio Unit.": "PRECIO_UNITARIO",
            "Litros": "LITROS",
            "Subtotal": "SUBTOTAL",
            "Monto": "TOTAL",
           # "Id_referencia": "Id_Referencia",

        }
    )
    df = df.drop(columns=["Columna1","Columna2", "Comision", "IVA Comision", "Total Comision", "Columna6", "Producto         Bomba", "Columna4", "Columna4","Columna5"], errors="ignore")
    df = clean_column_names(df)
    df = trim_values(df)
    print(f'cantidad de datos de dataframe: {df["Sucursal"].count()}')
    #df3 = df.merge(dfidgm, left_on="Sucursal", right_on="Referencia", how="inner")
    #df3 = df3.drop(columns=["IDGM","IdFormaPago","IdSubFormaPago","Referencia","Estatus","CrtdDateTime"])
    #print(f'cantidad de datos de dataframe que Tienen IDReferencia: {df3["Sucursal"].count()}')
    return df


def clean_amex_data():
    # LIMPIAR DATAFRAME y renombrar columnas
    df = leer_csv_amex(INPUT_PATH_AMEX).copy()
    # df = df.iloc[8:].reset_index(drop=True)
    df = df.replace(r"MXN\$", "", regex=True)
    

    # Renombrar columnas (ejemplo, ajusta según tus nombres reales)
    df = df.rename(
        columns={
            "Fecha de envío": "FechaEnvio",
            "Número de factura del monto del resumen de los cargos": "NumeroFacturaDeCargos",
            "Número de Pago": "NumeroDePago",
            "Cargos totales": "CargosTotales",
            "Créditos": "Creditos",
            "Monto del envío": "MontoDeEnvio",
            "Total del envío": "TotalDelEnvio",
            "Monto del descuento": "MontoDelDescuento",
            "Cuotas e incentivos": "CuotasEIncentivos",
            "Monto del pago": "MontoDePago",
            "Número de establecimiento receptor del pago": "IdAfiliacion",
            "Número de establecimiento que envía": "NumeroEstablecimiento",
            "Sucursal que envía": "SucursalQueEnvia",
            "Conteo de transacciones": "ConteoDeTransacciones",
            "Fecha de pago": "FechaPago",
            "Nombre de sucursal que envía": "NombreSucursal",
            "IVA": "IVA",
            "Descripción": "Descripcion",
            "Fecha de la transacción": "FechaTransaccion",
            "Número de mensualidades": "NumeroDeMensualidades",
        }
    )
    # Supongamos df ya cargado y columnas renombradas
    date_cols = ["FechaEnvio", "FechaPago", "FechaTransaccion"]

    for c in date_cols:
        if c in df.columns:
            # Verificar tipo
            print(f"{c} dtype antes:", df[c].dtype)
            # Si tiene componente horario o zona, normalizar a fecha
            # Esto deja solo la parte de fecha y la convierte a string YYYY-MM-DD
            df[c] = pd.to_datetime(df[c], errors="coerce", dayfirst=True).dt.strftime(
                "%Y-%m-%d"
            )
            df[c] = df[c].astype(str).replace("NaT", "")  # convertir NaT a cadena vacía
            print(f"{c} ejemplo:", df[c].head(1).tolist())
    print(f'cantidad de datos de dataframe: {df["FechaEnvio"].count()}')
    return df

CLEANERS = {
    "CXC_Enerkom": clean_enerkom_data(),
    "TVP_Amex": clean_amex_data(),
    #Puedes agregar más funciones de limpieza aquí
}                                              
    