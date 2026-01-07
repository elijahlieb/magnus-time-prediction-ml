from sklearn.linear_model import LinearRegression, Ridge, Lasso
import math
from sklearn.metrics import mean_squared_error, r2_score
from .evaluation import evaluate


def lin_reg(X_train, X_test, y_test, y_train):
    # Train
    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)

    evaluate(lin_reg, X_test, y_test)

    return lin_reg


def lin_reg_lasso(X_train, X_test, y_test, y_train):
    # Train 
    lasso = Lasso(alpha=0.01)
    lasso.fit(X_train, y_train)

    evaluate(lasso, X_test, y_test)

    return lasso


def lin_reg_ridge(X_train, X_test, y_test, y_train):
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train, y_train)

    evaluate(ridge, X_test, y_test)

    return ridge