import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------
# Load data (local project path)
# -------------------------------
base_path = Path.home() / "Desktop" / "SQL project"

inventory = pd.read_csv(base_path / "inventory.csv")
sales = pd.read_csv(base_path / "sales.csv")
suppliers = pd.read_csv(base_path / "suppliers.csv")

print("Data loaded successfully...\n")

# -------------------------------
# Merge datasets
# -------------------------------
data = sales.merge(inventory, on="product_id")

# -------------------------------
# 1. Product demand analysis
# -------------------------------
product_demand = (
    data.groupby("product_name")["quantity_sold"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop performing products:")
print(product_demand)

# -------------------------------
# 2. Stock health classification
# -------------------------------
def classify_stock(row):
    if row["stock_quantity"] <= row["reorder_level"]:
        return "CRITICAL"
    elif row["stock_quantity"] <= row["reorder_level"] * 2:
        return "LOW"
    else:
        return "OK"

inventory["stock_status"] = inventory.apply(classify_stock, axis=1)

print("\nInventory status overview:")
print(inventory[["product_name", "stock_status"]])

# -------------------------------
# 3. Stockout risk analysis
# -------------------------------
avg_sales = (
    data.groupby("product_id")["quantity_sold"]
    .mean()
    .reset_index()
    .rename(columns={"quantity_sold": "avg_daily_sales"})
)

stock_analysis = inventory.merge(avg_sales, on="product_id", how="left")

stock_analysis["days_until_stockout"] = (
    stock_analysis["stock_quantity"] / stock_analysis["avg_daily_sales"]
)

print("\nStockout risk analysis:")
print(stock_analysis[["product_name", "days_until_stockout"]])

# -------------------------------
# 4. Category performance
# -------------------------------
category_sales = (
    data.groupby("category")["quantity_sold"]
    .sum()
)

print("\nCategory performance:")
print(category_sales)

# -------------------------------
# 5. Visualization
# -------------------------------
product_demand.head(5).plot(kind="bar")
plt.title("Top 5 Products by Demand")
plt.xlabel("Product")
plt.ylabel("Units Sold")
plt.tight_layout()
plt.show()
