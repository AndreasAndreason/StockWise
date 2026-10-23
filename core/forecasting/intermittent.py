import numpy as np
import pandas as pd


def croston_forecast(demand: np.ndarray, alpha: float = 0.1) -> float:
    """
    Forecast intermittent demand using Croston's method.

    Parameters
    ----------
    demand : numpy.ndarray
        Historical demand observations.
    alpha : float, default=0.1
        Smoothing parameter for demand size and demand interval.

    Returns
    -------
    float
        Forecasted demand per period.
    """
    demand = np.asarray(demand, dtype=float)
    positive = demand[demand > 0]

    if len(positive) == 0:
        return 0.0
    if len(positive) == 1:
        return float(positive[0])

    demand_estimate = positive[0]
    interval_estimate = len(demand) / len(positive)
    last_positive = -1

    for t, value in enumerate(demand):
        if value > 0:
            if last_positive >= 0:
                interval = t - last_positive
                interval_estimate += alpha * (interval - interval_estimate)
            demand_estimate += alpha * (value - demand_estimate)
            last_positive = t

    return float(demand_estimate / interval_estimate)


def sba_forecast(demand: np.ndarray, alpha: float = 0.1) -> float:
    """
    Forecast intermittent demand using the SBA method.

    Parameters
    ----------
    demand : numpy.ndarray
        Historical demand observations.
    alpha : float, default=0.1
        Smoothing parameter for demand size and demand interval.

    Returns
    -------
    float
        Forecasted demand per period.
    """
    return float((1 - alpha / 2) * croston_forecast(demand, alpha))


def create_intermittent_forecast(df: pd.DataFrame, method: str = "croston", alpha: float = 0.1) -> pd.DataFrame:
    """
    Create an intermittent-demand forecast for each product.

    Parameters
    ----------
    df : pandas.DataFrame
        Historical product-level daily demand data.
    method : {"croston", "sba"}, default="croston"
        Forecasting method.
    alpha : float, default=0.1
        Smoothing parameter.

    Returns
    -------
    pandas.DataFrame
        Product-level forecasts.
    """
    forecast_func = croston_forecast if method == "croston" else sba_forecast
    forecasts = []

    for stock_code, group in df.groupby("StockCode"):
        demand = group.sort_values("Date")["Demand"].to_numpy()
        forecasts.append({"StockCode": stock_code, "Forecast": forecast_func(demand, alpha)})

    return pd.DataFrame(forecasts)


def evaluate_intermittent_forecast(df: pd.DataFrame, cutoff: str = "2011-09-26", method: str = "croston", alpha: float = 0.1) -> pd.DataFrame:
    """
    Evaluate an intermittent-demand method using a time-based holdout.

    Parameters
    ----------
    df : pandas.DataFrame
        Continuous daily product-level demand data.
    cutoff : str, default="2011-09-26"
        First date of the test period.
    method : {"croston", "sba"}, default="croston"
        Forecasting method.
    alpha : float, default=0.1
        Smoothing parameter.

    Returns
    -------
    pandas.DataFrame
        Product-level actual and forecast demand for the test period.
    """
    forecast_func = croston_forecast if method == "croston" else sba_forecast
    train = df[df["Date"] < cutoff]
    test = df[df["Date"] >= cutoff]
    forecasts = []

    for stock_code, group in train.groupby("StockCode"):
        demand = group.sort_values("Date")["Demand"].to_numpy()
        forecast = forecast_func(demand, alpha)
        product_test = test[test["StockCode"] == stock_code].copy()

        if not product_test.empty:
            product_test["Forecast"] = forecast
            forecasts.append(product_test[["Date", "StockCode", "Demand", "Forecast"]])

    return pd.concat(forecasts, ignore_index=True)