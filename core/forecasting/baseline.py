import pandas as pd


def create_baseline_features(df):
    df = df.copy()

    df = df.sort_values(["StockCode", "Date"])

    df["BaselineForecast"] = (df.groupby("StockCode")["Demand"].shift(7))

    return df
