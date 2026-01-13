import os
import pandas as pd
import joblib
from pathlib import Path


def save_dataframe_as_csv(
    df: pd.DataFrame,
    folder_path: str,
    filename: str = "result.csv"
):
    """
    Save a DataFrame as a CSV file, replacing it if it already exists.
    """

    os.makedirs(folder_path, exist_ok=True)

    full_path = os.path.join(folder_path, filename)

    if os.path.exists(full_path):
        os.remove(full_path)
        print(f"Old file deleted: {full_path}")

    df.to_csv(full_path, index=False)
    print(f"New file saved: {full_path}")




def download_model(model, results_dir: Path, filename: str = "model.pkl"):
    """
    Save a trained model to disk using joblib.
    """
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    model_path = results_dir / filename
    joblib.dump(model, model_path)

    print(f"✅ Model saved to {model_path}")


# Load the model to test if it works
def load_model(path, model_name):
    model = joblib.load(path / model_name)
    print("Model loaded successfully")
    return model
    