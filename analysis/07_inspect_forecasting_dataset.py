from core.forecasting.dataset import load_daily_sales, create_daily_series


df = load_daily_sales()

forecasting_data = create_daily_series(df)

product_history = (forecasting_data.groupby("StockCode")["Date"].agg(FirstDate="min", LastDate="max", Days="nunique"))

print("\n--- Product History ---")

print(product_history["Days"].describe())

print("\nProducts with fewer than 28 days:")

print((product_history["Days"] < 28).sum())

print("\nProducts with fewer than 56 days:")

print((product_history["Days"] < 56).sum())

print("\n--- Forecasting Dataset ---")

print(f"Rows: {len(forecasting_data):,}")
print(f"Products: {forecasting_data['StockCode'].nunique():,}")
print(f"Date range: {forecasting_data['Date'].min().date()} to {forecasting_data['Date'].max().date()}")

print("\n--- Demand ---")

print(forecasting_data["Demand"].describe())

print("\nZero-demand rows:")
print((forecasting_data["Demand"] == 0).sum())

print("\nMissing values:")
print(forecasting_data.isna().sum())

print("\nDemand accounting:")
print(f"Positive-demand rows: {(forecasting_data['Demand'] > 0).sum():,}")
print(f"Zero-demand rows: {(forecasting_data['Demand'] == 0).sum():,}")
print(f"Total rows: {len(forecasting_data):,}")