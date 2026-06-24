from  pathlib import Path
from scripts.config import INPUT_PATH
import pandas as pd

def leer_carpeta():
    """Lee archivos Excel de la carpeta de entrada y devuelve una lista de DataFrames."""
    input_folder = Path(INPUT_PATH)
    excel_files = list(input_folder.glob("*.xlsx"))
    csv_files = list(input_folder.glob("*.csv"))
    if not excel_files or not csv_files:
        print(f"No se encontraron archivos Excel o csv en la carpeta: {input_folder.absolute()}")
    else:
        #dataframes = []
        for file in excel_files:
            print(f"Procesando len({len(excel_files)}): {file.name}")
            df = pd.read_excel(file)
            #dataframes.append(df)
        
        for file2 in csv_files:
            print(f"procesando len({len(csv_files)}):{file2.name}") 
            df2 = pd.read_csv(file2)
    #print(df.head(5))  
    #print(df2.head(5))      
    
    return df, df2