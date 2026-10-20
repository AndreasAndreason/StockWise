from sklearn.metrics import mean_absolute_error, mean_squared_error

from core.forecasting.dataset import load_daily_sales, create_daily_series
from core.forecasting.baseline import create_baseline_features


df = load_daily_sales()

forecasting_data = create_daily_series(df)

forecasting_data = create_baseline_features(forecasting_data)

# Only rows where the 7-day baseline exists
evaluation_data = forecasting_data.dropna(subset=["BaselineForecast"]).copy()

# Time-based split
cutoff_date = evaluation_data["Date"].quantile(0.8)

train = evaluation_data[evaluation_data["Date"] <= cutoff_date]

test = evaluation_data[evaluation_data["Date"] > cutoff_date]

mae = mean_absolute_error(test["Demand"], test["BaselineForecast"])

rmse = mean_squared_error(test["Demand"], test["BaselineForecast"]) ** 0.5

print("--- Baseline Evaluation ---")

print(f"Cutoff date: {cutoff_date.date()}")
print(f"Training rows: {len(train):,}")
print(f"Test rows: {len(test):,}")

print(f"\nMAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
