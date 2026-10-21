import pandas as pd
import numpy as np
from pathlib import Path


PROCESSED_FILE = Path("data/processed/daily_sales.csv")


def load_daily_sales() -> pd.DataFrame:
    """
    Load the processed daily sales dataset.

    Reads the processed CSV file, converts the `Date` column to
    datetime format, and normalizes `StockCode` values to strings
    without surrounding whitespace.

    Returns
    -------
    pandas.DataFrame
        Processed daily sales data with normalized `Date` and
        `StockCode` columns.
    """

    df = pd.read_csv(PROCESSED_FILE)

    df["Date"] = pd.to_datetime(df["Date"])

    df["StockCode"] = df["StockCode"].astype(str).str.strip()

    return df


def add_active_date_range(df: pd.DataFrame) -> pd.DataFrame:
    """
    Determine the observed date range for each product.

    For each StockCode, identifies the first and last date on which
    the product appears in the input data.

    Parameters
    ----------
    df : pandas.DataFrame
        Daily product-level demand data containing `StockCode`
        and `Date` columns.

    Returns
    -------
    pandas.DataFrame
        One row per product containing `StockCode`, `FirstDate`,
        and `LastDate`.
    """

    return df.groupby("StockCode")["Date"].agg(FirstDate="min", LastDate="max").reset_index()


def create_daily_series(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a continuous daily demand series for each product.

    For each product, creates a daily date range from its first
    observed sale to its last observed sale. Missing product-day
    combinations within this active period are filled with zero
    demand.

    Days before a product's first observed sale and after its last
    observed sale are not added to the series.

    Parameters
    ----------
    df : pandas.DataFrame
        Daily product-level demand data containing `StockCode`,
        `Date`, and `Demand` columns.

    Returns
    -------
    pandas.DataFrame
        Continuous daily product-level demand data containing
        `Date`, `StockCode`, `Demand`, and `ActiveDays`.
    """

    activity = add_active_date_range(df)

    activity["ActiveDays"] = (activity["LastDate"] - activity["FirstDate"]).dt.days + 1

    daily = (df.groupby(["StockCode", "Date"], as_index=False)["Demand"].sum())

    active_days = activity["ActiveDays"].to_numpy()

    stock_codes = np.repeat(activity["StockCode"].to_numpy(), active_days)

    first_dates = np.repeat(activity["FirstDate"].to_numpy(), active_days)

    starts = np.repeat(np.cumsum(active_days) - active_days, active_days)

    offsets = np.arange(len(stock_codes)) - starts

    dates = first_dates + pd.to_timedelta(offsets, unit="D")

    calendar = pd.DataFrame({"StockCode": stock_codes, "Date": dates})

    result = calendar.merge(daily, on=["StockCode", "Date"], how="left")

    result["Demand"] = result["Demand"].fillna(0)

    result = result.merge(activity[["StockCode", "ActiveDays"]], on="StockCode", how="left")

    return result[["Date", "StockCode", "Demand", "ActiveDays"]]