from core.forecasting.dataset import load_daily_sales, create_daily_series, validate_daily_series


df = load_daily_sales()

forecasting_data = create_daily_series(df)

product_history = (forecasting_data.groupby("StockCode")["Date"].agg(FirstDate="min", LastDate="max", Days="nunique"))

print("\n--- Product History ---")

print(product_history["Days"].describe())

print("\nProducts with fewer than 28 days:")

print((product_history["Days"] < 28).sum())

print("\nProducts with fewer than 56 days:")

print((product_history["Days"] < 56).sum())

validate_daily_series(forecasting_data)
