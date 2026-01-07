
import math
from sklearn.metrics import mean_squared_error, r2_score


# Predict
def evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)

    # Eval
    mse = mean_squared_error(y_test, y_pred)
    rmse = math.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("MSE:", mse)
    print("RMSE: ", rmse)
    print("R²:", r2)
