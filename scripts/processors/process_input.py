from  pathlib import Path
from scripts.config import INPUT_PATH
import pandas as pd

def leer_carpeta():
    """Lee archivos Excel de la carpeta de entrada y devuelve una lista de DataFrames."""
    input_folder = Path(INPUT_PATH)
    excel_files = list(input_folder.glob("*.xlsx"))
    if not excel_files:
        raise FileNotFoundError(f"No se encontraron archivos Excel en la carpeta: {input_folder.absolute()}")
    else:
        #dataframes = []
        for file in excel_files:
            print(f"Procesando len({len(excel_files)}): {file.name}")
            df = pd.read_excel(file)
            #dataframes.append(df)
    print(df.head(5))        
    
    return df