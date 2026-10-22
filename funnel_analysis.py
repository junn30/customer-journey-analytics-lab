import pandas as pd

# Load the dataset
df = pd.read_csv("customer_journey.csv")

# Count customers at each funnel stage
total_customers = len(df)
product_viewers = df["viewed_product"].sum()
checkout_starters = df["started_checkout"].sum()
purchasers = df["completed_purchase"].sum()

# Display funnel
print("CUSTOMER FUNNEL")
print("-------------------------")
print(f"Customers:        {total_customers}")
print(f"Product viewed:   {product_viewers}")
print(f"Checkout started: {checkout_starters}")
print(f"Purchase:         {purchasers}")

product_view_rate = product_viewers / total_customers * 100
checkout_rate = checkout_starters / product_viewers * 100
purchase_rate = purchasers / checkout_starters * 100

print("\nFUNNEL CONVERSION RATES")
print(f"Product view rate: {product_view_rate:.2f}%")
print(f"Checkout rate: {checkout_rate:.2f}%")
print(f"Purchase rate: {purchase_rate:.2f}%")