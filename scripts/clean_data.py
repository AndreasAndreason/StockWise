import pandas as pd
from pathlib import Path


RAW_FILE = Path("data/raw/Online Retail.xlsx")
OUTPUT_FILE = Path("data/processed/daily_sales.csv")


def load_data():
    print("Loading raw dataset...")
    return pd.read_excel(RAW_FILE)


def classify_transactions(df):
    df = df.copy()

    invoice = df["InvoiceNo"].astype(str).str.strip()

    df["TransactionType"] = "OTHER"

    # Positive quantities represent observed sales/demand.
    df.loc[df["Quantity"] > 0, "TransactionType"] = "SALE"

    # Cancellation invoices are explicitly marked with C.
    df.loc[invoice.str.startswith("C"), "TransactionType"] = "CANCELLATION"

    # Remaining negative transactions are operational/inventory
    # adjustments such as damages, write-offs, checks, etc.
    df.loc[(df["Quantity"] < 0) & ~invoice.str.startswith("C"), "TransactionType"] = "INVENTORY_ADJUSTMENT"

    return df


def create_daily_sales(df):
    sales = df[df["TransactionType"] == "SALE"].copy()

    sales["Date"] = sales["InvoiceDate"].dt.date

    daily_sales = (sales.groupby(["Date", "StockCode"], as_index=False).agg(Demand=("Quantity", "sum")))

    return daily_sales


def main():
    df = load_data()

    print(f"Original rows: {len(df):,}")

    df = classify_transactions(df)

    print("\nTransaction types:")
    print(df["TransactionType"].value_counts().to_string())

    daily_sales = create_daily_sales(df)

    OUTPUT_FILE.parent.mkdir(parents=True,exist_ok=True)

    daily_sales.to_csv(OUTPUT_FILE, index=False)

    print(f"\nDaily sales rows: {len(daily_sales):,}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()