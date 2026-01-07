import pandas as pd

# Load raw data
customers_raw = pd.read_csv("data/customers_raw.csv")
products_raw  = pd.read_csv("data/products_raw.csv")
sales_raw     = pd.read_csv("data/sales_raw.csv")

# Log initial counts
print("Raw record counts:")
print(f"Customers: {len(customers_raw)}")
print(f"Products: {len(products_raw)}")
print(f"Sales: {len(sales_raw)}")

# Cleaning steps (example)
customers_df = customers_raw.drop_duplicates().reset_index(drop=True)
products_df  = products_raw.dropna().drop_duplicates().reset_index(drop=True)
sales_df     = sales_raw[sales_raw["quantity"] > 0].reset_index(drop=True)

# Log cleaned counts
print("\nCleaned record counts:")
print(f"Customers: {len(customers_df)} (dropped {len(customers_raw) - len(customers_df)})")
print(f"Products: {len(products_df)} (dropped {len(products_raw) - len(products_df)})")
print(f"Sales: {len(sales_df)} (dropped {len(sales_raw) - len(sales_df)})")

# Count duplicates before cleaning
customers_dupes = customers_raw.duplicated().sum()
products_dupes  = products_raw.duplicated().sum()
sales_dupes     = sales_raw.duplicated().sum()

print("Number of duplicates before cleaning:")
print(f"Customers: {customers_dupes}")
print(f"Products: {products_dupes}")
print(f"Sales: {sales_dupes}")

# Remove duplicates
customers_df = customers_raw.drop_duplicates().reset_index(drop=True)
products_df  = products_raw.drop_duplicates().reset_index(drop=True)
sales_df     = sales_raw.drop_duplicates().reset_index(drop=True)

# Verify after cleaning
print("\nNumber of records after cleaning:")
print(f"Customers: {len(customers_df)} (removed {customers_dupes})")
print(f"Products: {len(products_df)} (removed {products_dupes})")
print(f"Sales: {len(sales_df)} (removed {sales_dupes})")

# Count missing values before cleaning
print("Missing values before cleaning:")
print("Customers:\n", customers_raw.isnull().sum())
print("Products:\n", products_raw.isnull().sum())
print("Sales:\n", sales_raw.isnull().sum())

# Example cleaning (fill or drop missing values)
customers_df = customers_raw.fillna({"email": "unknown"})   # fill missing emails
products_df  = products_raw.dropna(subset=["price"])        # drop rows missing price
sales_df     = sales_raw.fillna(0)                          # fill numeric NaNs with 0

# Count missing values after cleaning
print("\nMissing values after cleaning:")
print("Customers:\n", customers_df.isnull().sum())
print("Products:\n", products_df.isnull().sum())
print("Sales:\n", sales_df.isnull().sum())

# Calculate how many were handled
customers_handled = customers_raw.isnull().sum().sum() - customers_df.isnull().sum().sum()
products_handled  = products_raw.isnull().sum().sum() - products_df.isnull().sum().sum()
sales_handled     = sales_raw.isnull().sum().sum() - sales_df.isnull().sum().sum()

print("\nNumber of missing values handled:")
print(f"Customers: {customers_handled}")
print(f"Products: {products_handled}")
print(f"Sales: {sales_handled}")

import pandas as pd
from sqlalchemy import create_engine

# Connection
engine = create_engine("mysql+mysqlconnector://root:India%4021@localhost/fleximart")

# Load cleaned DataFrames into MySQL tables
customers_df.to_sql("customers", con=engine, if_exists="append", index=False)
products_df.to_sql("products", con=engine, if_exists="append", index=False)
sales_df.to_sql("sales", con=engine, if_exists="append", index=False)

print("✅ Cleaned data loaded into MySQL successfully")

# Verify number of records loaded
customers_count = pd.read_sql("SELECT COUNT(*) FROM customers", con=engine).iloc[0,0]
products_count  = pd.read_sql("SELECT COUNT(*) FROM products", con=engine).iloc[0,0]
sales_count     = pd.read_sql("SELECT COUNT(*) FROM sales", con=engine).iloc[0,0]

print("\nNumber of records loaded successfully:")
print(f"Customers: {customers_count}")
print(f"Products: {products_count}")
print(f"Sales: {sales_count}")
