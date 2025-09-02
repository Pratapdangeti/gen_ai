import sqlite3
import pandas as pd
import os

folder_loc = "D:\\Projects\\Forecasting\\text_to_sql_working\\data\\"


# --- Step 1: Connect to SQLite (creates a file 'mydb.db')
conn = sqlite3.connect(os.path.join(folder_loc, "damydb.dbta"))
cursor = conn.cursor()


query = """
SELECT c.full_name, i.channel, SUM(i.duration) AS total_duration
FROM interactions i
JOIN customers c ON i.customer_id = c.customer_id
GROUP BY c.customer_id, i.channel
ORDER BY total_duration DESC;
"""

result = pd.read_sql_query(query, conn)
print(result)
conn.close()

print("Completed")
