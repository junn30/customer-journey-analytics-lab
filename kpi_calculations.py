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

print("Total Revenue:", total_revenue)
print("Average Order Value:", round(average_order_value, 2))

# New vs Returning conversion

new_customers = df[df["customer_type"] == "New"]
returning_customers = df[df["customer_type"] == "Returning"]

new_conversion = (
    new_customers["completed_purchase"].mean() * 100
)

returning_conversion = (
    returning_customers["completed_purchase"].mean() * 100
)

print("New Customer Conversion:", round(new_conversion, 2))
print("Returning Customer Conversion:", round(returning_conversion, 2))

# Conversion by acquisition channel

channel_conversion = (
    df.groupby("acquisition_channel")["completed_purchase"]
      .mean() * 100
)

print("\nConversion by Channel:")
print(channel_conversion.round(2))


# Conversion by device type

device_conversion = (
    df.groupby("device_type")["completed_purchase"]
      .mean() * 100
)

print("\nConversion by Device:")
print(device_conversion.round(2))

# Revenue by region

regional_revenue = (
    df.groupby("region")["revenue"]
      .sum()
)

print("\nRevenue by Region:")
print(regional_revenue)


# Funnel counts

funnel = {
    "Customers": total_customers,
    "Product Viewed": product_viewers,
    "Checkout Started": checkout_starters,
    "Purchase Completed": purchasers
}

print("\nFunnel:")
print(funnel)