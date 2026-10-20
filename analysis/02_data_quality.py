import pandas as pd

df = pd.read_excel("data/raw/Online Retail.xlsx")

invoice = df["InvoiceNo"].astype(str).str.strip()
is_cancellation = invoice.str.startswith("C")
is_negative = df["Quantity"] < 0

print("Cancellation rows:", is_cancellation.sum())
print("Negative quantity rows:", is_negative.sum())

print("\nOverlap:")
print("Both:", (is_cancellation & is_negative).sum())
print("Cancellation with non-negative quantity:",
      (is_cancellation & ~is_negative).sum())
print("Negative quantity without cancellation:",
      (~is_cancellation & is_negative).sum())

print("\nNegative quantity examples:")
print(df.loc[is_negative, ["InvoiceNo", "StockCode", "Quantity", "InvoiceDate"]].head(10).to_string(index=False))

print("\nCancellation examples:")
print(df.loc[is_cancellation, ["InvoiceNo", "StockCode", "Quantity", "InvoiceDate"]].head(10).to_string(index=False))

print("\nMissing descriptions by product:")
print(df.loc[df["Description"].isna(), "StockCode"].value_counts().head(10))


# Look at cancellation invoices and their possible original invoice numbers
cancellations = df[df["InvoiceNo"].astype(str).str.startswith("C")].copy()

cancellations["OriginalInvoiceNo"] = (cancellations["InvoiceNo"].astype(str).str.replace("^C", "", regex=True))

# Check whether the invoice without "C" exists
all_invoices = set(df["InvoiceNo"].astype(str))

cancellations["OriginalExists"] = (cancellations["OriginalInvoiceNo"].isin(all_invoices))

print("\nCancellation invoice matching:")
print(cancellations["OriginalExists"].value_counts())

print("\nExamples:")
print(cancellations[    [
            "InvoiceNo",
            "OriginalInvoiceNo",
            "StockCode",
            "Quantity",
            "OriginalExists",
        ]
    ].head(20).to_string(index=False))


positive_qty = df.loc[df["Quantity"] > 0, "Quantity"].sum()
negative_qty = df.loc[df["Quantity"] < 0, "Quantity"].sum()


print("\nQuantity summary:")
print(f"Positive quantity: {positive_qty:,}")
print(f"Negative quantity: {negative_qty:,}")
print(f"Absolute negative quantity: {abs(negative_qty):,}")

return_rate = abs(negative_qty) / positive_qty

print(f"Overall return/cancellation quantity rate: {return_rate:.2%}")

product_summary = (
    df.assign(
        PositiveQuantity=df["Quantity"].clip(lower=0),
        NegativeQuantity=df["Quantity"].clip(upper=0)
    )
    .groupby("StockCode")
    .agg(
        PositiveQuantity=("PositiveQuantity", "sum"),
        NegativeQuantity=("NegativeQuantity", "sum")
    )
)

product_summary["ReturnRate"] = (product_summary["NegativeQuantity"].abs()/ product_summary["PositiveQuantity"])

print("\nProducts with highest return rates:")
print(product_summary[product_summary["PositiveQuantity"] > 0].sort_values("ReturnRate", ascending=False).head(20).to_string())


problem_products = [
    "79323P",
    "79323B",
    "84614A",
    "84613C",
    "35610A"
]

print(df[df["StockCode"].isin(problem_products)][
        [
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate"
        ]
    ].sort_values(["StockCode", "InvoiceDate"]).to_string(index=False))


negative = df[df["Quantity"] < 0].copy()

print("\nNegative transactions by description:")
print(negative["Description"].fillna("<MISSING>").value_counts().head(30).to_string())

print("\nNegative transactions without cancellation invoice:")
print(negative[~negative["InvoiceNo"].astype(str).str.startswith("C")][
        [
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate"
        ]
    ].head(50).to_string(index=False))