from scripts.config import INPUT_PATH_EFECTICARD
from scripts.processors.data_processor import replace_values, rename_column_if_exists
from scripts.processors.process_input import leer_excel, pd
def clean_efecticard_data():
    """Realiza la limpieza de los datos de efecticard."""
    df = leer_excel(INPUT_PATH_EFECTICARD).copy()
    print(df.head(5))
    df.rename(columns={"SerieFact":"Serie",	"FolioFact":"Folio",	"FechaFact":"Fecha",	"CondicionesDePago":"CondicionesDePago","MetodoPago":"MetodoPago","Emisior":"Nombre",	"Receptor":"Nombre3",	"Descripcion":"Descripcion",	"TpoOperacion":"TipoOperacion", "No.Cliente":"NumeroDeCuenta",	"TotalFact":"Total6",	"NoTarjeta":"Identificador",	"FechaTransaccion":"FechaConsumo",	"NoEstacion":"ClaveEstacion",	"CantidadLitro":"Cantidad9",	"NombreCombustible":"NombreCombustible",	"FolioOperacion":"FolioDeOperacion",	"PrecioUnitario":"ValorUnitario10",	"Importe":"TotalConsumo","UUID":"UUID"}, inplace=True)
    replace_values(df, "Fecha","T"," ")
    replace_values(df, "FechaConsumo","T"," ")
    return df
    #print(df["Fecha"].head(2))
#clean_efecticard_data()
