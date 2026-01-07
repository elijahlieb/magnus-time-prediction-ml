 
import random as rd 
from pathlib import Path
import sys 

PROJECT_ROOT = Path.cwd().parent
sys.path.append(str(PROJECT_ROOT))
from src.utils.io import save_dataframe_as_csv



def sampled_shuffled_data(df_all, path):
    # Keep only blitz games
    df_blitz = df_all[df_all['TimeTotal'] == 180].copy()

    # Get unique game IDs
    unique_games = df_blitz['ID_game'].unique()

    # Sample 5 random games
    list_id_sample = rd.sample(list(unique_games), 5)

    print("✅ Sampled games:", list_id_sample)

    # Dataset sample (5 games)
    df_sample = df_blitz[df_blitz['ID_game'].isin(list_id_sample)].copy()

    # Training dataset = all other games
    df = df_blitz[~df_blitz['ID_game'].isin(list_id_sample)].copy()

    # Keep only Magnus moves for training
    df = df[df['PlayerName'] == "Carlsen, Magnus"]

    # Shuffle training data
    df = df.sample(frac=1.0, random_state=42)

    save_dataframe_as_csv(df_sample, path, "data_sample_magnus.csv")
    save_dataframe_as_csv(df, path, "data_shuffled_magnus.csv")
