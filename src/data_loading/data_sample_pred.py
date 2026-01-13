
import numpy as np 


# Function to associate to every Time spent the time spent predict by my model 
def predict_on_sample(df_samp, model, train_features, final_features):
    df_out = df_samp.copy()

    # Initialize column
    df_out["TimeSpentPred"] = np.nan

    # Masque Magnus
    mask_magnus = df_out["PlayerName"] == "Carlsen, Magnus"

    # Features
    X_pred = df_out.loc[mask_magnus, train_features]

    # Prédiction
    df_out.loc[mask_magnus, "TimeSpentPred"] = model.predict(X_pred)

    return df_out[final_features]



