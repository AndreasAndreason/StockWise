import pandas as pd

RAW_FILE = "data/raw/Online Retail.xlsx"

df = pd.read_excel(RAW_FILE)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["StockCode"] = df["StockCode"].astype(str).str.strip()

# --------------------------------------------------
# Separate sales and cancellations
# --------------------------------------------------

sales = df[df["Quantity"] > 0].copy()
cancellations = df[df["InvoiceNo"].astype(str).str.startswith("C")].copy()

cancellations["CancelledQuantity"] = cancellations["Quantity"].abs()

print("--- Cancellation Investigation ---")
print(f"Sales rows: {len(sales):,}")
print(f"Cancellation rows: {len(cancellations):,}")

# --------------------------------------------------
# Prepare row IDs
# --------------------------------------------------

sales = sales.reset_index().rename(columns={"index": "SaleRowID"})
cancellations = cancellations.reset_index().rename(columns={"index": "CancellationRowID"})

# Sort chronologically
sales = sales.sort_values("InvoiceDate")
cancellations = cancellations.sort_values("InvoiceDate")

# --------------------------------------------------
# Find one-to-one matches
# --------------------------------------------------

used_sales = set()
matches = []

for _, cancellation in cancellations.iterrows():

    candidates = sales[
        (sales["StockCode"] == cancellation["StockCode"])
        & (sales["UnitPrice"] == cancellation["UnitPrice"])
        & (sales["Quantity"] == cancellation["CancelledQuantity"])
        & (sales["InvoiceDate"] < cancellation["InvoiceDate"])
        & (~sales["SaleRowID"].isin(used_sales))
    ]

    if candidates.empty:
        continue

    # Choose the closest previous sale
    candidates = candidates.copy()

    candidates["TimeDifference"] = (cancellation["InvoiceDate"] - candidates["InvoiceDate"])

    best = candidates.loc[candidates["TimeDifference"].idxmin()]

    used_sales.add(best["SaleRowID"])

    matches.append(
        {
            "CancellationRowID": cancellation["CancellationRowID"],
            "InvoiceNo_cancel": cancellation["InvoiceNo"],
            "InvoiceNo_sale": best["InvoiceNo"],
            "StockCode": cancellation["StockCode"],
            "Quantity_cancel": cancellation["Quantity"],
            "Quantity_sale": best["Quantity"],
            "UnitPrice": cancellation["UnitPrice"],
            "InvoiceDate_sale": best["InvoiceDate"],
            "InvoiceDate_cancel": cancellation["InvoiceDate"],
            "DaysDifference": (cancellation["InvoiceDate"] - best["InvoiceDate"]).total_seconds() / 86400,
        }
    )

matches = pd.DataFrame(matches)

# --------------------------------------------------
# Results
# --------------------------------------------------

print("\n--- Matching Results ---")

print(f"Matched cancellation rows: {len(matches):,}")
print(f"Unmatched cancellation rows: {len(cancellations) - len(matches):,}")
print(f"Cancellation rows with a matched previous sale: {len(matches):,}")

if not matches.empty:

    print("\n--- Example Matches ---")

    columns = [
        "InvoiceNo_cancel",
        "InvoiceNo_sale",
        "StockCode",
        "Quantity_cancel",
        "Quantity_sale",
        "UnitPrice",
        "InvoiceDate_sale",
        "InvoiceDate_cancel",
        "DaysDifference",
    ]

    print(matches[columns].head(20).to_string(index=False))

    print("\n--- Largest Time Differences ---")

    print(matches.sort_values("DaysDifference", ascending=False)[columns].head(20).to_string(index=False))

    print("\n--- Time Difference Statistics ---")

    print(
        matches["DaysDifference"].describe(
            percentiles=[
                0.25,
                0.50,
                0.75,
                0.90,
                0.95,
                0.99,
            ]
        )
    )

    print("\n--- Matches Within Time Windows ---")

    for days in [1, 7, 14, 30, 60, 90, 180, 365]:
        count = (matches["DaysDifference"] <= days).sum()

        print(f"Within {days:>3} days: {count:>5,} ({count / len(matches) * 100:.1f}%)")