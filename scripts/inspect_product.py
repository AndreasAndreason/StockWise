import pandas as pd

RAW_FILE = "data/raw/Online Retail.xlsx"

df = pd.read_excel(RAW_FILE)

product = "23843"

print(f"Investigating product: {product}")

product_data = df[df["StockCode"].astype(str).str.strip() == product].copy()

print("\n--- Product Information ---")

print(product_data[
        [
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "UnitPrice",
            "Country",
        ]
    ].to_string(index=False)
)

print("\n--- Summary ---")

print(f"Number of transaction rows: {len(product_data):,}")
print(f"Total quantity: {product_data['Quantity'].sum():,}")
print(f"Positive quantity: {product_data.loc[product_data['Quantity'] > 0, 'Quantity'].sum():,}")
print(f"Negative quantity: {product_data.loc[product_data['Quantity'] < 0, 'Quantity'].sum():,}")
