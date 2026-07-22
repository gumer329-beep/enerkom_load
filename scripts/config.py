"""CONFIGURACION DE LA APLICACION DE CARGA A BASE DE DATOS
Este archivo contiene la configuración de la aplicación, incluyendo rutas de archivos, reglas de validación y mapeos de columnas. Se utiliza para personalizar el comportamiento del pipeline ETL.
"""

INPUT_PATH_ENERKOM = "data/enerkom"
INPUT_PATH_ULTRAGAS = "data/ultragas"
INPUT_PATH_AMEX = "data/amex"
INPUT_PATH_GASNGO = "data/gasngo"
INPUT_PATH_GASOMATIC = "data/gasomatic"
INPUT_PATH_GASOPASS = "data/gasopass"
INPUT_PATH_EFECTICARD = "data/efecticard"
OUTPUT_PATH = "output"
# # ====== REGLAS ======
# scripts/config.py

TABLES_CONFIG = {
    "Tesoreria_TpvAmex": {
        "not_null_cols": [
            "FechaEnvio",
            "NumeroFacturaDeCargos",
            "IdAfiliacion",
            "NumeroDePago",
            "NumeroEstablecimiento",
            "SucursalQueEnvia",
            "ConteoDeTransacciones",
            "FechaPago",
            "NombreSucursal",
            "Descripcion",
            "FechaTransaccion",
            "NumeroDeMensualidades",
        ],
        "date_strict_cols": ["FechaEnvio", "FechaPago", "FechaTransaccion"],
        "exclude_cols": ["Id", "CrtdDateTime"],
        "decimal_cols": [
            "CargosTotales",
            "Creditos",
            "MontoDeEnvio",
            "TotalDelEnvio",
            "MontoDelDescuento",
            "CuotasEIncentivos",
            "MontoDePago",
            "IVA",
        ],
        "duplicate_cols": [
            "FechaEnvio",
            "NumeroFacturaDeCargos",
            "NumeroDePago",
            "TotalDelEnvio",
        ],
        "validations": {"TotalDelEnvio": "sum"},
        "mapping_enabled": False,
        "mapping_configs": [
            {
                "columna_csv": "Sucursal",
                "tabla_catalogo": "Tesoreria_Referencia",
                "columna_relacion_catalogo": "Referencia",
                "columna_id_catalogo": "Id",
                "alias_destino": "Id_Referencia",
                # "where_clause": "IdFormaPago =  AND IdSubFormaPago = ",  # ← Ajusta aquí
                "enabled": False,
            }
        ],
        # "csv_filename": "TPVAMEX_*.csv"
    },
    "Cxc_Enerkom": {
        "not_null_cols": [
            "Sucursal",
            "NoEstacion",
            "TARJETA",
            "FECHA",
            "TIPO",
            "TRANSACCION",
            "PRODUCTO",
            "PRECIO_UNITARIO",
            "LITROS",
            "TOTAL",
        ],
        "date_strict_cols": ["Fecha"],
        "exclude_cols": [
            "Id",
            "CrtdDateTime",
        ],
        "decimal_cols": ["Litros", "Subtotal", "Iva", "Total"],
        "duplicate_cols": ["Fecha", "Transaccion", "Sucursal", "Total"],
        "validations": {"Total": "sum"},
        "mapping_enabled": True,
        "mapping_configs": [
            {
                "columna_csv": "Sucursal",
                "tabla_catalogo": "Tesoreria_Referencia",
                "columna_relacion_catalogo": "Referencia",  # conlumna con el que hace el merge
                "columna_id_catalogo": "Id",
                "alias_destino": "IdReferencia",
                "where_clause": "IdFormaPago = 5 AND IdSubFormaPago = 6",  # ← Distinto
                "enabled": True,
            }
        ],
        # "csv_filename": "ENERKOM_*.csv"
    },
    "Cxc_Ultragas": {
        "not_null_cols": [
            "Sucursal",
            "NoTran",
            "Fecha",
            "NoCliente",
            "NoVehiculo",
            "Producto",
            "NoLitros",
            "Importe",
        ],
        "date_strict_cols": ["Fecha"],
        "exclude_cols": [
            "Id",
            "CrtdDateTime",
        ],
        "decimal_cols": [
            "NoLitros",
            "Importe",
        ],
        "duplicate_cols": ["Sucursal", "Fecha", "NoTran", "Importe"],
        "validations": {"Importe": "sum"},
        "mapping_enabled": True,
        "mapping_configs": [
            {
                "columna_csv": "Sucursal",
                "tabla_catalogo": "Tesoreria_Referencia",
                "columna_relacion_catalogo": "Referencia",  # conlumna con el que hace el merge
                "columna_id_catalogo": "Id",
                "alias_destino": "IdReferencia",
                "where_clause": "IdFormaPago = 5 AND IdSubFormaPago = 4",  # ← Distinto
                "enabled": True,
            }
        ],
        # "csv_filename": "ULTRASGAS_*.csv"
    },
    "Cxc_Gasngo": {
        "not_null_cols": [
            "FechaFact",
            "TotalFact",
            "FechaTransaccion",
            "NoEstacion",
            "Importe",
        ],
        "date_strict_cols": ["FechaFact", "FechaTransaccion"],
        "exclude_cols": [
            "Id",
            "CrtdDateTime",
        ],
        "decimal_cols": ["PrecioUnitario", "CantidadLitro", "Importe"],
        "duplicate_cols": [
            "FolioOperacion",
            "FolioFact",
            "FechaFact",
            "FechaTransaccion",
            "NoTarjeta",
        ],
        "validations": {"Importe": "sum"},
        "mapping_enabled": True,
        "mapping_configs": [
            {
                "columna_csv": "NoEstacion",
                "tabla_catalogo": "Tesoreria_Referencia",
                "columna_relacion_catalogo": "Referencia",  # conlumna con el que hace el merge
                "columna_id_catalogo": "Id",
                "alias_destino": "IdReferencia",
                "where_clause": "IdFormaPago = 5 AND IdSubFormaPago = 24",  # ← Distinto
                "enabled": True,
            }
        ],
        # "csv_filename": "ULTRASGAS_*.csv"
    },
    "Cxc_Gasopass": {
        "not_null_cols": [
    "NoTransaccion",
    "Fecha",
    "RazonSocial",
    "Sucursal",
    "Ciudad",
    "Estado",
    "Placa",
    "Producto",
    "Litros",
    "Precio",
    "Importe",
    "NoTarjeta",
    "Parcelamento",
    "MetodoPago",
    "OrigenTran",
    "Estatus",
        ],
        "date_strict_cols": ["Fecha"],
        "exclude_cols": [
            "Id",
            "CrtdDateTime",
        ],
        "decimal_cols": ["Litros", "Precio", "Importe"],
        "duplicate_cols": ["NoTransaccion", "Fecha de Registro", "Importe"],
        "validations": {"Importe": "sum"},
        "mapping_enabled": True,
        "mapping_configs": [
            {
                "columna_csv": "Sucursal",
                "tabla_catalogo": "Tesoreria_Referencia",
                "columna_relacion_catalogo": "Referencia",  # conlumna con el que hace el merge
                "columna_id_catalogo": "Id",
                "alias_destino": "IdReferencia",
                "where_clause": "IdFormaPago = 5 AND IdSubFormaPago = 2",  # ← Distinto
                "enabled": True,
            }
        ],
        # "csv_filename": "gasomatic_*.csv"
    },
    "Cxc_Gasomatic": {
        "not_null_cols": [
            "Excluido",
            "Importe",
            "Fechahoraestacion",
            "FechaReal",
            "Codigo",
        ],
        "date_strict_cols": ["FechaReal", "Fechahoraestacion"],
        "exclude_cols": [
            "Id",
            "CrtdDateTime",
        ],
        "decimal_cols": ["Cantidad", "Precio", "Importe"],
        "duplicate_cols": ["FechaReal", "Fechahoraestacion", "Cantidad", "Importe"],
        "validations": {"Importe": "sum"},
        "mapping_enabled": True,
        "mapping_configs": [
            {
                "columna_csv": "Comercio",
                "tabla_catalogo": "Tesoreria_Referencia",
                "columna_relacion_catalogo": "Referencia",  # conlumna con el que hace el merge
                "columna_id_catalogo": "Id",
                "alias_destino": "IdReferencia",
                "where_clause": "IdFormaPago = 5 AND IdSubFormaPago = 7",  # ← Distinto
                "enabled": True,
            }
        ],
        # "csv_filename": "gasomatic_*.csv"
    },
    "Cxc_Efecticard": {
        "not_null_cols": [
            "Fecha",
            "FechaConsumo",
            "ClaveEstacion",
            "TotalConsumo",
            "Serie",
        ],
        "date_strict_cols": ["Fecha", "FechaConsumo"],
        "exclude_cols": [
            "Id",
            "CrtdDateTime",
        ],
        "decimal_cols": ["Total6", "Cantidad9", "ValorUnitario10", "TotalConsumo"],
        "duplicate_cols": ["Folio","Fecha", "NumeroDeCuenta", "Total6", "FechaConsumo","FolioDeOperacion","TotalConsumo","UUID"],
        "validations": {"TotalConsumo": "sum"},
        "mapping_enabled": True,
        "mapping_configs": [
            {
                "columna_csv": "NumeroDeCuenta",
                "tabla_catalogo": "Tesoreria_Referencia",
                "columna_relacion_catalogo": "Referencia",  # conlumna con el que hace el merge
                "columna_id_catalogo": "Id",
                "alias_destino": "IdReferencia",
                "where_clause": "IdFormaPago = 5 AND IdSubFormaPago = 3",  # ← Distinto
                "enabled": True,
            }
        ],
        # "csv_filename": "gasomatic_*.csv"
    }
    # Puedes agregar más tablas con sus propios filtros

}


def get_table_config(table_name):
    """Retorna la configuración de una tabla"""
    return TABLES_CONFIG.get(table_name)
