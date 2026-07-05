from pathlib import Path
from scripts.config import INPUT_PATH
import pandas as pd


<<<<<<< HEAD
def leer_carpeta():
    """Lee archivos Excel de la carpeta de entrada y devuelve una lista de DataFrames."""
    input_folder = Path(INPUT_PATH)
    excel_files = list(input_folder.glob("*.xlsx"))
    # csv_files = list(input_folder.glob("*.csv"))
    df = pd.DataFrame()
    if not excel_files:  # or not csv_files:
        print(
            f"No se encontraron archivos Excel o csv en la carpeta: {input_folder.absolute()}"
        )
=======
def leer_excel():
    """Lee archivos Excel de la carpeta de entrada y devuelve una lista de DataFrames."""
    input_folder = Path(INPUT_PATH)
    excel_files = list(input_folder.glob("*.xlsx"))
    if not excel_files:
        print(f"No se encontraron archivos Excel en la carpeta: {input_folder.absolute()}")
>>>>>>> b5acbe6 (refactorisar y etl)
    else:
        # dataframes = []
        for file in excel_files:
            print(f"Procesando len({len(excel_files)}): {file.name}")
<<<<<<< HEAD
            xls = pd.ExcelFile(file)
            ultima = xls.sheet_names[-1]
            print(f"ultima:{ultima}")
            df = pd.read_excel(file, sheet_name=ultima, engine="openpyxl")
            # dataframes.append(df)

        # for file2 in csv_files:
        #     print(f"procesando len({len(csv_files)}):{file2.name}")
        #     df2 = pd.read_csv(file2)
    # print(df.head(5))
    # print(df2.head(5))

    return df
=======
            df = pd.read_excel(file)
            #dataframes.append(df)
    #print(df.head(5))  
    return df


def leer_csv():
    """Lee archivos CSV de la carpeta de entrada y devuelve una lista de DataFrames."""
    input_folder = Path(INPUT_PATH)
    csv_files = list(input_folder.glob("*.csv"))
    if not csv_files:
        print(f"No se encontraron archivos CSV en la carpeta: {input_folder.absolute()}")
    else:
        for file in csv_files:
            print(f"Procesando len({len(csv_files)}): {file.name}")
            df = pd.read_csv(file)
    #print(df.head(5))  
    return df
>>>>>>> b5acbe6 (refactorisar y etl)
