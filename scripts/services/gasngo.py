from scripts.config import INPUT_PATH_GASNGO
from scripts.processors.process_input import leer_excel, leer_csv, pd
def clean_gasngo_data():
    """Realiza la limpieza de los datos de Enerkom."""
    df = leer_excel( INPUT_PATH_GASNGO).copy()
    # # dfidgm = df2.copy()
    # df["Attribute:Fecha"] = pd.to_datetime("1899-12-30") + pd.to_timedelta(
    #     df["Attribute:Fecha"], unit="D"
    # )
    # df["Attribute:Fecha"] = df["Attribute:Fecha"].dt.round("s")
    # df[
    #     "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.9"
    # ] = pd.to_datetime("1899-12-30") + pd.to_timedelta(
    #     df[
    #         "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.9"
    #     ],
    #     unit="D",
    # )
    # df[
    #     "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.9"
    # ] = df[
    #     "Complemento.http://www.sat.gob.mx/ConsumoDeCombustibles11.ConsumoDeCombustible.9"
    # ].dt.round(
    #     "s"
    # )

    # df["sucursal_numero"] = pd.to_numeric(
    #     df["sucursal_codigo"], errors="coerce"
    # ).astype("Int64")

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
    # print(df["FolioFact"].dtype)
    print(f'cantidad de datos de dataframe: {df["SerieFact"].count()}')
    # df3 = df.merge(dfidgm, left_on="Sucursal", right_on="Referencia", how="inner")
    # df3 = df3.drop(columns=["IDGM","IdFormaPago","IdSubFormaPago","Referencia","Estatus","CrtdDateTime"])
    # print(f'cantidad de datos de dataframe que Tienen IDReferencia: {df3["Sucursal"].count()}')
    return df
