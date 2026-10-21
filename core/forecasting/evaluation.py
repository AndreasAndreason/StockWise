import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def evaluate_forecast(actual: pd.Series, predicted: pd.Series) -> dict[str, float]:
    """
    Evaluate forecast accuracy using MAE and RMSE.

    Parameters
    ----------
    actual : pd.Series
        Actual observed demand values.

    predicted : pd.Series
        Forecasted demand values.

    Returns
    -------
    dict
        Dictionary containing MAE and RMSE.
    """

    mae = mean_absolute_error(actual, predicted)

    rmse = mean_squared_error(actual, predicted) ** 0.5

    return {"MAE": mae, "RMSE": rmse}