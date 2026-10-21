import pandas as pd


def profile_demand(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a demand profile for each product.

    Calculates demand volume, demand distribution, demand frequency,
    zero-demand frequency, and demand variability for each StockCode.

    Parameters
    ----------
    df : pandas.DataFrame
        Daily product-level demand data containing at least
        `StockCode` and `Demand` columns.

    Returns
    -------
    pandas.DataFrame
        One row per product with demand statistics, including:
        active days, total demand, mean and median demand,
        standard deviation, demand percentiles, positive- and
        zero-demand days, and coefficient of variation.
    """

    profile = (
        df.assign(PositiveDemand=df["Demand"] > 0)
        .groupby("StockCode")
        .agg(
            ActiveDays=("Demand", "count"),
            TotalDemand=("Demand", "sum"),
            MeanDemand=("Demand", "mean"),
            MedianDemand=("Demand", "median"),
            StdDemand=("Demand", "std"),
            MinDemand=("Demand", "min"),
            MaxDemand=("Demand", "max"),
            P25=("Demand", lambda x: x.quantile(0.25)),
            P75=("Demand", lambda x: x.quantile(0.75)),
            P90=("Demand", lambda x: x.quantile(0.90)),
            PositiveDemandDays=("PositiveDemand", "sum"),
        )
        .reset_index()
    )

    profile["ZeroDemandDays"] = profile["ActiveDays"] - profile["PositiveDemandDays"]

    profile["ZeroDemandPct"] = profile["ZeroDemandDays"] / profile["ActiveDays"] * 100

    profile["PositiveDemandPct"] = profile["PositiveDemandDays"] / profile["ActiveDays"] * 100

    profile["CoefficientOfVariation"] = profile["StdDemand"] / profile["MeanDemand"]

    return profile
