from scripts.services.cleaning_services import clean_enerkom_data
from scripts.repositories.export_repository import export_csv
x =clean_enerkom_data()
#print(x.head(5))
export_csv(x)