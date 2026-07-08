from pathlib import Path
from scripts.config import INPUT_PATH_AMEX
import pandas as pd


def leer_excel(INPUT_PATH):
    """Lee archivos Excel de la carpeta de entrada y devuelve una lista de DataFrames."""
    input_folder = Path(INPUT_PATH)
    excel_files = list(input_folder.glob("*.xlsx"))
    if not excel_files:
        print(f"No se encontraron archivos Excel en la carpeta: {input_folder.absolute()}")
    else:
         #dataframes = []
         for file in excel_files:
            print(f"Procesando len({len(excel_files)}): {file.name}")
            df = pd.read_excel(file)
            #dataframes.append(df)
    #print(df.head(5))  
    return df


def leer_csv_amex(INPUT_PATH):
    """Lee archivos CSV de la carpeta de entrada y devuelve una lista de DataFrames."""
    input_folder = Path(INPUT_PATH)
    csv_files = list(input_folder.glob("*.csv"))
    if not csv_files:
        print(f"No se encontraron archivos CSV en la carpeta: {input_folder.absolute()}")
        return
    else:
        df = []
        for file in csv_files:
            print(f"Procesando len({len(csv_files)}): {file.name}")
            if(INPUT_PATH==INPUT_PATH_AMEX):
                df.append(pd.read_csv(file, skiprows=9, dtype=str, keep_default_na=False))
            else:
                df.append(pd.read_csv(file))

    #print(df.head(5))  
    return pd.concat(df)