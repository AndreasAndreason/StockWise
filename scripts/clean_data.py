import pandas as pd
import time
from pathlib import Path


RAW_FILE = Path("data/raw/Online Retail.xlsx")
OUTPUT_FILE = Path("data/processed/daily_sales.csv")


def load_data():
    print("Loading raw dataset...")
    start = time.perf_counter()

    df = pd.read_excel(RAW_FILE)

    print(f"Loading completed in {time.perf_counter() - start:.2f} seconds")
    return df


def classify_transactions(df):
    start = time.perf_counter()
    df = df.copy()

    invoice = df["InvoiceNo"].astype(str).str.strip()

    df["TransactionType"] = "OTHER"

    df.loc[df["Quantity"] > 0, "TransactionType"] = "SALE"

    df.loc[invoice.str.startswith("C"), "TransactionType"] = "CANCELLATION"

    df.loc[(df["Quantity"] < 0) & ~invoice.str.startswith("C"), "TransactionType"] = "INVENTORY_ADJUSTMENT"

    print(f"Classification completed in {time.perf_counter() - start:.2f} seconds")
    return df


def match_cancellations(df):
    """
    Match cancellation lines to earlier positive sales.

    Matching criteria:
    - same StockCode
    - same UnitPrice
    - same absolute quantity
    - sale occurred before cancellation
    - cancellation occurred within the configured time window
    - each sale can only be matched once

    Returns the set of sale row indices that were identified
    as reversed by a cancellation.
    """
    start = time.perf_counter()

    sales = df[df["TransactionType"] == "SALE"].copy()

    cancellations = df[df["TransactionType"] == "CANCELLATION"].copy()

    cancellations["CancelledQuantity"] = (cancellations["Quantity"].abs())

    sales = sales.sort_values("InvoiceDate")
    cancellations = cancellations.sort_values("InvoiceDate")

    used_sales = set()
    reversed_sales = set()

    matched_within_window = 0
    unmatched_cancellations = 0

    for sale_index, cancellation in cancellations.iterrows():

        candidates = sales[
            (sales["StockCode"] == cancellation["StockCode"])
            & (sales["UnitPrice"] == cancellation["UnitPrice"])
            & (sales["Quantity"] == cancellation["CancelledQuantity"])
            & (sales["InvoiceDate"] < cancellation["InvoiceDate"])
            & (~sales.index.isin(used_sales))
        ]

        if candidates.empty:
            unmatched_cancellations += 1
            continue

        candidates = candidates.copy()

        candidates["DaysDifference"] = (cancellation["InvoiceDate"] - candidates["InvoiceDate"]).dt.total_seconds() / 86400

        candidates = candidates[candidates["DaysDifference"] <= CANCELLATION_WINDOW_DAYS]

        if candidates.empty:
            continue

        best_match = candidates.loc[candidates["DaysDifference"].idxmin()]

        used_sales.add(best_match.name)
        reversed_sales.add(best_match.name)

    print(f"Cancellation matching completed in {time.perf_counter() - start:.2f} seconds")

    print(f"Unmatched cancellations: {unmatched_cancellations:,}")
    print(f"Matched sales: {len(reversed_sales):,}")

    return reversed_sales


def create_daily_sales(df):
    df = df.copy()

    # Demand consists of positive sales only.
    # Cancellations and other negative inventory movements
    # are intentionally excluded from demand forecasting.
    sales = df[df["TransactionType"] == "SALE"].copy()

    sales["Date"] = sales["InvoiceDate"].dt.date

    daily_sales = (
        sales.groupby(["Date", "StockCode"], as_index=False)
        .agg(Demand=("Quantity", "sum"))
    )

    return daily_sales


def main():
    df = load_data()

    print(f"Original rows: {len(df):,}")

    df = classify_transactions(df)

    print("\nQuantity check:")
    print(df["Quantity"].describe())

    print("\nPositive quantities:")
    print((df["Quantity"] > 0).sum())

    print("\nTransaction types:")
    print(df["TransactionType"].value_counts(dropna=False).to_string())

    daily_sales = create_daily_sales(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    daily_sales.to_csv(OUTPUT_FILE, index=False)

    print(f"\nDaily sales rows: {len(daily_sales):,}")

    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()