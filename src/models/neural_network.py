
# Neural network 
from tensorflow import keras
from tensorflow.keras import layers, callbacks
import numpy as np 
import time 
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pandas as pd 
from sklearn.model_selection import train_test_split
from .evaluation import evaluate

# Function to build the model 
def build_mlp(input_shape, layer_sizes, activation="relu", dropout=0.0, l2=0.0):
    inp = keras.Input(shape=(input_shape,))
    x = inp
    for size in layer_sizes:
        if l2 and l2 > 0:
            x = layers.Dense(size, activation=activation, kernel_regularizer=keras.regularizers.l2(l2))(x)
        else:
            x = layers.Dense(size, activation=activation)(x)
        if dropout and dropout > 0:
            x = layers.Dropout(dropout)(x)
    out = layers.Dense(1, activation='linear')(x)
    model = keras.Model(inp, out)
    model.compile(optimizer=keras.optimizers.Adam(), loss="mse", metrics=[])
    return model


# Function to randomly search the best model 
def random_search_nn(X_train, y_train, X_test=None, y_test=None,
                     n_iter=40, random_state=42, max_epochs=100, 
                     val_size=0.2, metric_to_opt="r2"):

    np.random.seed(random_state)
    
    results = []
    X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=val_size, random_state=random_state)
    input_dim = X_tr.shape[1]
    
    for it in range(n_iter):
        # --- Sample hyperparams (example sensible ranges)
        n_layers = np.random.choice([1, 2, 3])  # profondeur
        # sample neurons log-uniform between 8 and 512
        layer_sizes = [int(2 ** np.random.uniform(3, 9)) for _ in range(n_layers)]
        activation = np.random.choice(["relu", "tanh"])
        dropout = float(np.random.choice([0.0, 0.1, 0.2, 0.3]))
        l2 = float(np.random.choice([0.0, 1e-5, 1e-4, 1e-3]))
        batch_size = int(np.random.choice([32, 64, 128]))
        max_lr_epochs = int(np.random.choice([20, 50, 100]))  # just for info / scheduling
        
        # --- Build & train with early stopping
        model = build_mlp(input_dim, layer_sizes, activation=activation, dropout=dropout, l2=l2)
        es = callbacks.EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True, verbose=0)
        rl = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, verbose=0)
        
        t0 = time.time()
        history = model.fit(X_tr, y_tr,
                            validation_data=(X_val, y_val),
                            epochs=max_epochs,
                            batch_size=batch_size,
                            callbacks=[es, rl],
                            verbose=0)
        t_elapsed = time.time() - t0
        
        # --- Evaluate on validation (and optional test)
        yval_pred = model.predict(X_val).ravel()
        mse_val = mean_squared_error(y_val, yval_pred)
        rmse_val = np.sqrt(mse_val)
        mae_val = mean_absolute_error(y_val, yval_pred)
        r2_val = r2_score(y_val, yval_pred)
        
        # optional test eval
        test_metrics = {}
        if X_test is not None and y_test is not None:
            ytest_pred = model.predict(X_test).ravel()
            mse_test = mean_squared_error(y_test, ytest_pred)
            rmse_test = np.sqrt(mse_test)
            mae_test = mean_absolute_error(y_test, ytest_pred)
            r2_test = r2_score(y_test, ytest_pred)
            test_metrics.update({
                "mse_test": mse_test, "rmse_test": rmse_test, "mae_test": mae_test, "r2_test": r2_test
            })
        else:
            mse_test = rmse_test = mae_test = r2_test = np.nan
        
        results.append({
            "iter": it,
            "layer_sizes": tuple(layer_sizes),
            "n_layers": n_layers,
            "activation": activation,
            "dropout": dropout,
            "l2": l2,
            "batch_size": batch_size,
            "epochs_trained": len(history.history['loss']),
            "train_time_s": t_elapsed,
            "mse_val": mse_val,
            "rmse_val": rmse_val,
            "mae_val": mae_val,
            "r2_val": r2_val,
            **test_metrics
        })
        
        # free memory 
        keras.backend.clear_session()
    
    df_res = pd.DataFrame(results)
    # Choose best model according to metric_to_opt
    if metric_to_opt == "r2":
        best_idx = df_res['r2_val'].idxmax()
    elif metric_to_opt == "rmse":
        best_idx = df_res['rmse_val'].idxmin()
    else:
        raise ValueError("metric_to_opt must be 'r2' or 'rmse'")
    
    best_row = df_res.loc[best_idx].to_dict()
    
    # Rebuild & retrain best model longuement sur train+val si tu veux
    best_layer_sizes = list(best_row['layer_sizes'])
    best_model = build_mlp(input_dim, best_layer_sizes, activation=best_row['activation'], dropout=best_row['dropout'], l2=best_row['l2'])
    # Retrain on train+val for final model 
    X_full = np.vstack([X_tr, X_val])
    y_full = np.concatenate([y_tr, y_val])
    es_full = callbacks.EarlyStopping(monitor='val_loss', patience=12, restore_best_weights=True, verbose=1)
    # using a small validation split from full for early stopping
    history_full = best_model.fit(X_full, y_full, validation_split=0.1, epochs=300, batch_size=int(best_row['batch_size']),
                                  callbacks=[es_full, callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=6)], verbose=0)
    
    evaluate(best_model,  X_test, y_test)
    return best_model, df_res.sort_values('r2_val', ascending=False).reset_index(drop=True)


class KerasRegressorWrapper:
    def __init__(self, model):
        self.model = model

    def predict(self, X):
        return self.model.predict(X, verbose=0).ravel()