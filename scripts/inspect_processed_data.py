import pandas as pd

FILE = "data/processed/daily_sales.csv"

df = pd.read_csv(FILE, parse_dates=["Date"])

print("Processed data inspection...")

# 1. Basic information
print("\n--- Basic Information ---")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Columns: {list(df.columns)}")

# 2. Unique products
unique_products = df["StockCode"].nunique()
print(f"\nUnique products: {unique_products:,}")

# 3. Date range
date_min = df["Date"].min()
date_max = df["Date"].max()

print(f"Date range: {date_min.date()} to {date_max.date()}")

# 4. Product/date combinations
product_date_combinations = df.groupby(["StockCode", "Date"]).ngroups

print(f"Unique product-day combinations: {product_date_combinations:,}")

# 5. Missing values
print("\n--- Missing Values ---")

missing = df.isna().sum()

if missing.sum() == 0:
    print("No missing values.")
else:
    print(missing[missing > 0])

# 6. Duplicate product/date combinations
duplicates = df.duplicated(subset=["Date", "StockCode"]).sum()

print("\n--- Duplicates ---")
print(f"Duplicate product-day rows: {duplicates:,}")

# 7. Demand statistics
print("\n--- Demand Statistics ---")
print(df["Demand"].describe())

# 8. Daily total demand
daily_demand = df.groupby("Date")["Demand"].sum()

print("\n--- Daily Demand ---")
print(daily_demand.describe())

# 9. Products with highest total demand
product_demand = (df.groupby("StockCode")["Demand"].sum().sort_values(ascending=False))

print("\n--- Top 10 Products by Total Demand ---")
print(product_demand.head(10))

# 10. Check for invalid demand values
invalid_demand = df[df["Demand"] <= 0]

print("\n--- Demand Validation ---")

if len(invalid_demand) == 0:
    print("All demand values are greater than zero.")
else:
    print(f"Found {len(invalid_demand):,} rows with demand <= 0."    )

# 11. Check for unusual daily demand
Q1 = daily_demand.quantile(0.25)
Q3 = daily_demand.quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

unusual = daily_demand[(daily_demand < lower) | (daily_demand > upper)]

print("\n--- Unusual Daily Demand ---")
print(f"Number of unusual days: {len(unusual):,}")

if len(unusual) > 0:
    print("\nHighest unusual demand days:")
    print(unusual.sort_values(ascending=False).head(10))