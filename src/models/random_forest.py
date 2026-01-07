from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np 
import matplotlib as plt
import math 
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pandas as pd 
from .evaluation import evaluate


# Random forest model 
def random_forest(X_train, y_train):
    param_grid = {
        'n_estimators': [100, 300, 500],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10],
        'max_features': ['sqrt', 'log2', None]  # ✅ no "auto"
    }

    rf = RandomForestRegressor(random_state=42)

    grid = GridSearchCV(
        rf,
        param_grid,
        cv=3,
        scoring='r2',
        n_jobs=-1,
        verbose=2,
        error_score=np.nan  # ignore invalid combos silently
    )

    grid.fit(X_train, y_train)

    return grid




# Function to select the best model and train it 
def train_best_random_forest(grid, X_train, y_train,  X_test, y_test):
    best_params = grid.best_params_
    print(best_params)

    model_rf = RandomForestRegressor(
        **best_params,
        random_state=42,
        n_jobs=-1
    )

    model_rf.fit(X_train, y_train)

    evaluate(model_rf,  X_test, y_test)

    return model_rf


