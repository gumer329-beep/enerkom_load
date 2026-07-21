from scripts.processors.process_input import leer_excel, leer_csv, pd
from scripts.config import INPUT_PATH_GASOPASS
import re


def clean_gasopass_data():
    """Realiza la limpieza de los datos de Enerkom."""
  
    df = leer_excel(INPUT_PATH_GASOPASS).copy()

    # convierte "13/06/2026 11:18:23 a. m." -> "2026-06-13 11:18:23"
    # Mantener datetime
    print(f"es :{df['Fecha de Registro'].dtype}")
    iso_mask = df["Fecha de Registro"].astype(str).str.match(r"^\d{4}-\d{2}-\d{2}")
    print("ISO:", iso_mask.sum(), "No ISO:", (~iso_mask).sum())
    print(df.loc[~iso_mask, "Fecha de Registro"].head())

    df["Fecha de Registro"] = pd.to_datetime(
        df["Fecha de Registro"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    print(f"es :{df['Fecha de Registro'].dtype}")

    for v in df["Fecha de Registro"].astype(str).head(10):
        print(repr(v))

    print(df.head(5))
    print(f'cantidad de datos de dataframe: {df["N°. Transacción"].count()}')

    df = df.rename(
        columns={
            "N°. Transacción": "NoTransaccion",
            "Fecha de Registro": "Fecha",
            "Razón Social": "RazonSocial",
            "Nombre Comercial": "Sucursal",
            "Combustible": "Producto",
            "Precio por Litro": "Precio",
            "Valor Bruto": "Importe",
            "N°. Tarjeta": "NoTarjeta",
            "Cuotas": "Parcelamento",
            "Producto": "MetodoPago",
            "Transacción de Origen": "OrigenTran",
            "Situación": "Estatus",
            "N°. de Cuotas": "NParcela",
            "N°. Terminal": "NoTerminal",
            "NSU": "Nsuo",
            "NSU Red": "Nsur",
            "NIT PJ/NIT PM/OTROS": "Rfc",
            "Descuento o Recargo": "DescontoEncargo",
            "Valor de la Tasa Adm.": "TxAdm",
        }
    )
    # df["NoTerminal"] = pd.to_numeric(df["NoTerminal"], errors="coerce").astype("int64")

    print(df["NoTerminal"].dtype)
    df["Correccion"] = ""
    df["Sucursal"] = df["Sucursal"].replace(
        {
            "LOMAS DE OCUITZAPOTLAN": "ESGES 4 MARZO",
            "ESGES AV CENTRAL": "CENTRAL",
        }
    )
    print(df.head(5))
    return df
