import pandas as pd

# Load the dataset
df = pd.read_csv("customer_journey.csv")

# Total customers
total_customers = len(df)

# Completed purchases
completed_purchases = df["completed_purchase"].sum()

# Conversion rate
conversion_rate = (
    completed_purchases / total_customers
) * 100

# Display results
print(f"Total customers: {total_customers}")
print(f"Completed purchases: {completed_purchases}")
print(f"Conversion rate: {conversion_rate:.2f}%")