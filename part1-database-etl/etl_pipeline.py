import os
import pandas as pd 
def extract_data(file_path):
    """
    Extracts data from a CSV file into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Extracted {file_path} successfully")
        return df
    except Exception as e:
        print(f"❌ Error extracting {file_path}: {e}")
        return None
customers_df = extract_data("data/customers_raw.csv")
products_df = extract_data("data/products_raw.csv")
sales_df = extract_data("data/sales_raw.csv")
if customers_df is not None:
    print(customers_df.head())
if products_df is not None:
    print(products_df.head())
if sales_df is not None:
    print(sales_df.head())
# Deduplicate
customers_df.drop_duplicates(inplace=True)

# Fill missing emails
customers_df['email'] = customers_df['email'].fillna("missing@example.com")

# Standardize phone numbers → keep last 10 digits and add +91
customers_df['phone'] = customers_df['phone'].str.replace(r'\D', '', regex=True)
customers_df['phone'] = '+91' + customers_df['phone'].str[-10:]

# Convert registration_date to proper datetime
customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'], errors='coerce')

# Normalize city names
customers_df['city'] = customers_df['city'].str.strip().str.title()
products_df['price'] = products_df['price'].fillna(products_df['price'].median())
products_df['stock_quantity'] = products_df['stock_quantity'].fillna(0)
products_df['category'] = products_df['category'].str.strip().str.lower().str.title()
products_df['product_name'] = products_df['product_name'].str.strip()
sales_df.drop_duplicates(inplace=True)
sales_df = sales_df.dropna(subset=['customer_id', 'product_id'])
sales_df['transaction_date'] = pd.to_datetime(sales_df['transaction_date'], errors='coerce')

from sqlalchemy import create_engine

# Connection string with password safely encoded
engine = create_engine("mysql+mysqlconnector://root:India%4021@localhost/fleximart")

import os

# Load cleaned DataFrames into MySQL tables
customers_df.to_sql("customers", con=engine, if_exists="replace", index=False)
products_df.to_sql("products", con=engine, if_exists="replace", index=False)
sales_df.to_sql("sales", con=engine, if_exists="replace", index=False)
print("✅ Cleaned data loaded into MySQL successfully")


