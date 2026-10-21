import pandas as pd


def create_baseline_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a 7-day seasonal naive demand forecast for each product.

    The forecast for each product-day is based on the observed demand
    for the same product seven days earlier.

    Parameters
    ----------
    df : pandas.DataFrame
        Daily product-level demand data containing `StockCode`,
        `Date`, and `Demand` columns.

    Returns
    -------
    pandas.DataFrame
        A copy of the input data sorted by product and date, with
        a new `BaselineForecast` column containing the 7-day lagged
        demand. The first seven observations for each product have
        no baseline forecast and therefore contain NaN.
    """

    df = df.copy()

    df = df.sort_values(["StockCode", "Date"])

    df["BaselineForecast"] = (df.groupby("StockCode")["Demand"].shift(7))

    return df