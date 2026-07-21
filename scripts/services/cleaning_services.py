from scripts.services.gasngo import clean_gasngo_data
from scripts.services.gasomatic import clean_gasomatic_data
from scripts.services.tpv_amex import clean_amex_data
from scripts.services.enerkom import clean_enerkom_data
from scripts.services.ultragas import clean_ultragas_data
from scripts.services.gasopass import clean_gasopass_data
from scripts.services.efecticard import clean_efecticard_data










CLEANERS = {
    "Cxc_Enerkom": clean_enerkom_data,
    "Tesoreria_TpvAmex": clean_amex_data,
    "Cxc_Ultragas": clean_ultragas_data,
    "Cxc_Gasngo": clean_gasngo_data,
    "Cxc_Gasomatic": clean_gasomatic_data,
    "Cxc_Gasopass": clean_gasopass_data,
    "Cxc_Efecticard": clean_efecticard_data,
    # Puedes agregar más funciones de limpieza aquí
}
