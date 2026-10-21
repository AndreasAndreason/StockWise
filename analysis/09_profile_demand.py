import pandas as pd

from core.forecasting.dataset import load_daily_sales, create_daily_series
from core.forecasting.profiling import profile_demand



print("Loading daily sales...")
df = load_daily_sales()

print("Creating daily product series...")
daily_series = create_daily_series(df)

print("Profiling product demand...")
profile = profile_demand(daily_series)

print("\n--- Demand Profile ---")
print(f"Products: {len(profile):,}")
print(f"Rows in forecasting dataset: {len(daily_series):,}")

print("\n--- Overall Demand ---")
print(
    profile[
        [
            "ActiveDays",
            "TotalDemand",
            "MeanDemand",
            "MedianDemand",
            "StdDemand",
            "MinDemand",
            "MaxDemand",
            "ZeroDemandPct",
            "PositiveDemandPct",
            "CoefficientOfVariation",
        ]
    ].describe()
)

print("\n--- Products With Highest Zero-Demand Percentage ---")
print(
    profile[
        [
            "StockCode",
            "ActiveDays",
            "PositiveDemandDays",
            "ZeroDemandPct",
            "MeanDemand",
            "TotalDemand",
        ]
    ]
    .sort_values("ZeroDemandPct", ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\n--- Products With Highest Coefficient of Variation ---")
print(
    profile[
        [
            "StockCode",
            "ActiveDays",
            "MeanDemand",
            "StdDemand",
            "CoefficientOfVariation",
            "MaxDemand",
        ]
    ]
    .sort_values("CoefficientOfVariation", ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\n--- Products With Highest Total Demand ---")
print(
    profile[
        [
            "StockCode",
            "ActiveDays",
            "TotalDemand",
            "MeanDemand",
            "MedianDemand",
            "MaxDemand",
        ]
    ]
    .sort_values("TotalDemand", ascending=False)
    .head(10)
    .to_string(index=False)
)