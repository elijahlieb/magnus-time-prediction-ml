from .pgn_parser import df_pgn_full
import os 
import pandas as pd
from pathlib import Path 


# Function to browse all the files contained in the data folder
# Function to browse all the files contained in the data folder
def df_final(start_folder):
    
    liste_data = os.listdir(start_folder)
    ID_game = 0

    i = 1
    n = len(liste_data)
    list_to_concat = []
    for file in liste_data:
        pgn = open(f'{start_folder}\{file}')
        df, ID_game = df_pgn_full(pgn, ID_game)
        list_to_concat.append(df)
        print(f"✅ Finish file [{i}/{n}]")
        i += 1

    
    return pd.concat(list_to_concat)

