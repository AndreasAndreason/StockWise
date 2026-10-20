import pandas as pd
from pathlib import Path


PROCESSED_FILE = Path("data/processed/daily_sales.csv")


def load_daily_sales():
    df = pd.read_csv(PROCESSED_FILE)

    df["Date"] = pd.to_datetime(df["Date"])

    df["StockCode"] = df["StockCode"].astype(str).str.strip()

    return df


def add_active_date_range(df):
    return df.groupby("StockCode")["Date"].agg(FirstDate="min", LastDate="max").reset_index()


def create_daily_series(df):
    activity = add_active_date_range(df)

    activity["ActiveDays"] = (activity["LastDate"] - activity["FirstDate"]).dt.days + 1

    series = []

    for _, product in activity.iterrows():

        product_code = product["StockCode"]
        start_date = product["FirstDate"]
        end_date = product["LastDate"]

        dates = pd.date_range(start=start_date, end=end_date, freq="D")

        product_data = df[df["StockCode"] == product_code][["Date", "Demand"]]

        product_data = (product_data.set_index("Date").reindex(dates).fillna(0).rename_axis("Date").reset_index())

        product_data["StockCode"] = product_code

        product_data["ActiveDays"] = product["ActiveDays"]

        series.append(product_data)

    result = pd.concat(series, ignore_index=True)

    return result[["Date", "StockCode", "Demand", "ActiveDays"]]


def validate_daily_series(df):
    print("--- Forecasting Dataset ---")

    print(f"Rows: {len(df):,}")
    print(f"Products: {df['StockCode'].nunique():,}")
    print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")

    print("\n--- Demand ---")

    print(df["Demand"].describe())

    print("\nZero-demand rows:")
    print((df["Demand"] == 0).sum())

    print("\nMissing values:")
    print(df.isna().sum())