import pandas as pd

# Load dataset
df = pd.read_csv("customer_journey.csv")

# Core KPIs
total_customers = len(df)

product_viewers = df["viewed_product"].sum()
checkout_starters = df["started_checkout"].sum()
purchasers = df["completed_purchase"].sum()

product_view_rate = round(product_viewers / total_customers * 100, 2)
checkout_rate = round(checkout_starters / product_viewers * 100, 2)
purchase_rate = round(purchasers / checkout_starters * 100, 2)

print("Total Customers:", total_customers)
print("Product View Rate:", product_view_rate)
print("Checkout Start Rate:", checkout_rate)
print("Purchase Conversion Rate:", purchase_rate)

total_revenue = df["revenue"].sum()

average_order_value = (
    total_revenue / purchasers
)