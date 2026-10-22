import sqlite3
import pandas as pd

# Load the CSV
df = pd.read_csv("customer_journey.csv")

# Create a SQLite database
connection = sqlite3.connect("customer_insight.db")

# Load the DataFrame into SQLite
df.to_sql("customers", connection, if_exists="replace", index=False)

print("Database created successfully!")

# Close the connection
connection.close()