""" CONFIGURACION DE LA APLICACION DE CARGA A BASE DE DATOS
Este archivo contiene la configuración de la aplicación, incluyendo rutas de archivos, reglas de validación y mapeos de columnas. Se utiliza para personalizar el comportamiento del pipeline ETL.
"""


INPUT_PATH = "data"
OUTPUT_PATH = "output"
# ====== REGLAS ======
NOT_NULL_COLS = [
    "Sucursal", "NoEstacion", "TARJETA", "FECHA", "TIPO",
    "TRANSACCION", "PRODUCTO", "PRECIO_UNITARIO", "LITROS", "TOTAL"
]


DATE_STRICT_COLS = ["FECHA"]
DECIMAL_COLS = ["PRECIO_UNITARIO", "LITROS", "SUBTOTAL", "TOTAL", "IVA"]
EXCLUDE_COLS = {"Id", "creado_en", "actualizado_en"}
DUPLICATE_COLS = ['Sucursal', 'FECHA', 'TRANSACCION', 'PRODUCTO']
VALIDATIONS = {"TOTAL": "sum"}

MAPPING_CONFIGS = [{
    "columna_csv": "Sucursal",
    "tabla_catalogo": "Tesoreria_referencia",
    "columna_relacion_catalogo": "Referencia",
    "columna_id_catalogo": "Id",
    "forma_pago": "IdFormaPago",
    "subforma_pago": "IdSubFormaPago",
    "alias_destino": "Id_Referencia",
    "manual_map": {},  # ejemplo: {"BK ADO Coatzacoalcos": "BK ADO Coatzacoalcos"}
    "enabled": True
},# Puedes añadir más mapeos aquí
]
MAPPING_ENABLED = True # Cambiar a True para habilitar mapeos

FORMA_DE_PAGO = 5
SUBFORMA_DE_PAGO = 6