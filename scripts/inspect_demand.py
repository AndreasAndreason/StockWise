import pandas as pd

FILE = "data/processed/daily_sales.csv"

df = pd.read_csv(FILE, parse_dates=["Date"])

print("Demand investigation...")

# --------------------------------------------------
# 1. Highest product-day demand
# --------------------------------------------------

print("\n--- Highest Product-Day Demand ---")

top_product_days = (df.sort_values("Demand", ascending=False).head(20))

print(top_product_days.to_string(index=False))

# --------------------------------------------------
# 2. Highest-demand days
# --------------------------------------------------

daily_demand = (df.groupby("Date")["Demand"].sum().sort_values(ascending=False))

print("\n--- Highest-Demand Days ---")
print(daily_demand.head(20))

# --------------------------------------------------
# 3. Demand for the highest-demand product
# --------------------------------------------------

top_product = df.loc[df["Demand"].idxmax(),"StockCode"]

print(f"\n--- Product {top_product} ---")

product_history = (df[df["StockCode"] == top_product].sort_values("Date"))

print(product_history.to_string(index=False))

# --------------------------------------------------
# 4. Final dates in dataset
# --------------------------------------------------

print("\n--- Final 10 Dates ---")

final_dates = (df.groupby("Date")["Demand"].sum().tail(10))

print(final_dates)

# --------------------------------------------------
# 5. Number of products sold each day
# --------------------------------------------------

daily_products = (df.groupby("Date")["StockCode"].nunique())

print("\n--- Products Sold Per Day ---")
print(daily_products.describe())

print("\nDays with highest number of products:")
print(daily_products.sort_values(ascending=False).head(10))

# --------------------------------------------------
# 6. Monthly demand
# --------------------------------------------------

monthly_demand = (df.set_index("Date").resample("ME")["Demand"].sum())

print("\n--- Monthly Demand ---")
print(monthly_demand)