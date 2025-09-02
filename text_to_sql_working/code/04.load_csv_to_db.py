import sqlite3
import pandas as pd
import os

folder_loc = "D:\\Projects\\Forecasting\\text_to_sql_working\\data\\"


# --- Step 1: Connect to SQLite (creates a file 'mydb.db')
conn = sqlite3.connect(os.path.join(folder_loc, "damydb.dbta"))
cursor = conn.cursor()

# --- Step 2: Load CSVs into tables
# Example: two CSV files -> customers.csv, orders.csv


def load_csv_to_sqlite(csv_file, table_name):
    df = pd.read_csv(os.path.join(folder_loc, csv_file))
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {csv_file} into table '{table_name}'")


load_csv_to_sqlite("customers.csv", "customers")
load_csv_to_sqlite("campaigns.csv", "campaigns")
load_csv_to_sqlite("customer_reviews_complete.csv", "customer_reviews_complete")
load_csv_to_sqlite("interactions.csv", "interactions")
load_csv_to_sqlite("support_tickets.csv", "support_tickets")
load_csv_to_sqlite("transactions.csv", "transactions")

# "customers.csv",
# "campaigns.csv",
# "customer_reviews_complete.csv",
# "interactions.csv",
# "support_tickets.csv",
# "transactions.csv",


print("Completed")
