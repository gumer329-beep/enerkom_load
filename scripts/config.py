""" CONFIGURACION DE LA APLICACION DE CARGA A BASE DE DATOS
Este archivo contiene la configuración de la aplicación, incluyendo rutas de archivos, reglas de validación y mapeos de columnas. Se utiliza para personalizar el comportamiento del pipeline ETL.
"""



INPUT_PATH_ENERKOM = "data/enerkom"
INPUT_PATH_AMEX = "data/amex"
OUTPUT_PATH = "output"
# # ====== REGLAS ======
# scripts/config.py

TABLES_CONFIG = {
    "TVP_Amex": {
        "not_null_cols": [
            "FechaEnvio", "NumeroFacturaDeCargos", "IdAfiliacion",
            "NumeroDePago", "NumeroEstablecimiento", "SucursalQueEnvia",
            "ConteoDeTransacciones", "FechaPago", "NombreSucursal",
            "Descripcion", "FechaTransaccion", "NumeroDeMensualidades"
        ],
        "date_strict_cols": ["FechaEnvio", "FechaPago", "FechaTransaccion"],
        "exclude_cols":["Id", "creado_en", "actualizado_en"],
        "decimal_cols": ["CargosTotales", "Creditos", "MontoDeEnvio", "TotalDelEnvio",
                         "MontoDelDescuento", "CuotasEIncentivos", "MontoDePago", "IVA"],
        "duplicate_cols": ["NumeroFacturaDeCargos", "NumeroDePago"],
        "validations": {"TotalDelEnvio": "sum"},
        "mapping_enabled": False,
        "mapping_configs": [{
            "columna_csv": "Sucursal",
            "tabla_catalogo": "Tesoreria_referencia",
            "columna_relacion_catalogo": "Referencia",
            "columna_id_catalogo": "Id",
            "alias_destino": "Id_Referencia",
            #"where_clause": "IdFormaPago =  AND IdSubFormaPago = ",  # ← Ajusta aquí
            "enabled": False
        }],
        #"csv_filename": "TPVAMEX_*.csv"
    },
    "CXC_Enerkom": {
        "not_null_cols": [
            "Sucursal", "NoEstacion", "TARJETA", "FECHA", "TIPO",
            "TRANSACCION", "PRODUCTO", "PRECIO_UNITARIO", "LITROS", "TOTAL"
        ],
        "date_strict_cols": ["FECHA"],
        "exclude_cols":["Id", "creado_en", "actualizado_en"],
        "decimal_cols": ["PRECIO_UNITARIO", "LITROS", "SUBTOTAL", "TOTAL", "IVA"],
        "duplicate_cols": ["Sucursal", "FECHA", "TRANSACCION", "PRODUCTO"],
        "validations": {"TOTAL": "sum"},
        "mapping_enabled": True,
        "mapping_configs": [{
            "columna_csv": "Sucursal",
            "tabla_catalogo": "Tesoreria_referencia",
            "columna_relacion_catalogo": "Referencia",
            "columna_id_catalogo": "Id",
            "alias_destino": "Id_Referencia",
            "where_clause": "IdFormaPago = 5 AND IdSubFormaPago = 6",  # ← Distinto
            "enabled": True
        }],
        #"csv_filename": "ENERKOM_*.csv"
    },
    # Puedes agregar más tablas con sus propios filtros
}



def get_table_config(table_name):
    """Retorna la configuración de una tabla"""
    return TABLES_CONFIG.get(table_name)