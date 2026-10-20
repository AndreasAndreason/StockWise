import pandas as pd

df = pd.read_excel("data/raw/Online Retail.xlsx")

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nDate range:")
print(df["InvoiceDate"].min())
print(df["InvoiceDate"].max())

print("\nUnique products:", df["StockCode"].nunique())
print("Unique invoices:", df["InvoiceNo"].nunique())

print("\nNegative quantities:", (df["Quantity"] < 0).sum())
print("Zero quantities:", (df["Quantity"] == 0).sum())

print("\nCancellation invoices:", df["InvoiceNo"].astype(str).str.startswith("C").sum())