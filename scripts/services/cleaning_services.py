from scripts.processors.process_input import leer_excel, pd
from scripts.services.clean_and_map import parse_date
from scripts.processors.data_processor import clean_column_names, trim_values


def clean_enerkom_data():
    """Realiza la limpieza de los datos de Enerkom."""
<<<<<<< HEAD
    df1 = leer_carpeta()
    df = df1.copy()
    # dfidgm = df2.copy()
    df["Attribute:Fecha"] = pd.to_datetime("1899-12-30") + pd.to_timedelta(
        df["Attribute:Fecha"], unit="D"
    )
    df["Attribute:Fecha"] = df["Attribute:Fecha"].dt.round("s")
    df[
        "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.9"
    ] = pd.to_datetime("1899-12-30") + pd.to_timedelta(
        df[
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.9"
        ],
        unit="D",
    )
    df[
        "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.9"
    ] = df[
        "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.9"
    ].dt.round(
        "s"
    )

    # df["sucursal_numero"] = pd.to_numeric(
    #     df["sucursal_codigo"], errors="coerce"
    # ).astype("Int64")

=======
    df = leer_excel().copy()
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
    #df['Fecha'] = pd.to_datetime(df["Fecha"], format='%d/%m/%Y %I:%M:%S %p', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    df["Fecha"] = parse_date(df["Fecha"])
    #df['sucursal_numero'] = pd.to_numeric(df['sucursal_codigo'], errors='coerce').astype('Int64')
    df = df[["Sucursal","NoEstacion"] + [c for c in df.columns if c not in ("Sucursal","NoEstacion", "Monto", "Precio Unit.","Litros","Subtotal","IVA")]+["Precio Unit.","Litros","Subtotal","IVA","Monto"]]
>>>>>>> b5acbe6 (refactorisar y etl)
    df = df.rename(
        columns={
            "Attribute:Serie": "SerieFact",
            "Attribute:Folio": "FolioFact",
            "Attribute:Fecha": "FechaFact",
            "CondicionesDepago": "CondicionesDePago",
            "Attribute:MetodoPago": "MetodoPago",
            "Emisor.Attribute:Nombre": "Emisior",
            "Receptor.Attribute:Nombre": "Receptor",
            "Conceptos.Concepto.Attribute:Descripcion": "Descripcion",
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.2": "TipoOperacion",
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.3": "NoCliente",
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.5": "TotalFact",
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.8": "NoTarjeta",
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.9": "FechaTransaccion",
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustibl.11": "NoEstacion",
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustibl.13": "CantidadLitro",
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustibl.14": "NombreCombustible",
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustibl.15": "FolioOperacion",
            "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustibl.16": "PrecioUnitario",
            "importe": "Importe",
            "Complemento.http://www.sat.gob.mx/TimbreFiscalDigital.TimbreFiscalDigital.Attr.1": "Uuid",
            # "Id_referencia": "Id_Referencia",
        }
    )
<<<<<<< HEAD
    # print(df["FolioFact"].dtype)
    print(f'cantidad de datos de dataframe: {df["SerieFact"].count()}')
    # df3 = df.merge(dfidgm, left_on="Sucursal", right_on="Referencia", how="inner")
    # df3 = df3.drop(columns=["IDGM","IdFormaPago","IdSubFormaPago","Referencia","Estatus","CrtdDateTime"])
    # print(f'cantidad de datos de dataframe que Tienen IDReferencia: {df3["Sucursal"].count()}')
    return df
=======
    df = df.drop(columns=["Columna1","Columna2", "Comision", "IVA Comision", "Total Comision", "Columna6", "Producto         Bomba", "Columna4", "Columna4","Columna5"], errors="ignore")
    df = clean_column_names(df)
    df = trim_values(df)
    print(f'cantidad de datos de dataframe: {df["Sucursal"].count()}')
    #df3 = df.merge(dfidgm, left_on="Sucursal", right_on="Referencia", how="inner")
    #df3 = df3.drop(columns=["IDGM","IdFormaPago","IdSubFormaPago","Referencia","Estatus","CrtdDateTime"])
    #print(f'cantidad de datos de dataframe que Tienen IDReferencia: {df3["Sucursal"].count()}')
    return df                                              
    
>>>>>>> b5acbe6 (refactorisar y etl)
