import pandas as pd
import numpy as np

# Make the results reproducible
np.random.seed(42)

# Number of customers
n = 1500

# -----------------------------
# 1. Basic customer information
# -----------------------------

customer_id = np.arange(1, n + 1)

signup_date = pd.to_datetime(
    np.random.choice(
        pd.date_range("2025-01-01", "2025-06-30"),
        size=n
    )
)

acquisition_channel = np.random.choice(
    ["Organic", "Paid Search", "Social Media", "Email", "Referral"],
    size=n,
    p=[0.30, 0.25, 0.20, 0.15, 0.10]
)

device_type = np.random.choice(
    ["Mobile", "Desktop", "Tablet"],
    size=n,
    p=[0.60, 0.30, 0.10]
)

region = np.random.choice(
    ["North", "South", "East", "West"],
    size=n,
    p=[0.25, 0.25, 0.20, 0.30]
)

customer_type = np.random.choice(
    ["New", "Returning"],
    size=n,
    p=[0.70, 0.30]
)

# -----------------------------
# 2. Customer journey
# -----------------------------

# Product viewing
viewed_product = np.random.choice(
    [0, 1],
    size=n,
    p=[0.20, 0.80]
)

# Checkout is more likely if the customer viewed a product
started_checkout = np.where(
    viewed_product == 1,
    np.random.choice([0, 1], size=n, p=[0.45, 0.55]),
    0
)

# Purchase is more likely if checkout was started
completed_purchase = np.where(
    started_checkout == 1,
    np.random.choice([0, 1], size=n, p=[0.60, 0.40]),
    0
)

# -----------------------------
# 3. Revenue
# -----------------------------

# Give purchasing customers a random order value
revenue = np.where(
    completed_purchase == 1,
    np.random.randint(500, 10001, size=n),
    0
)

# -----------------------------
# 4. Returning user flag
# -----------------------------

returning_user = np.where(
    customer_type == "Returning",
    1,
    0
)

# -----------------------------
# 5. Customer support
# -----------------------------

support_contacted = np.random.choice(
    [0, 1],
    size=n,
    p=[0.75, 0.25]
)

# -----------------------------
# 6. Create DataFrame
# -----------------------------

df = pd.DataFrame({
    "customer_id": customer_id,
    "signup_date": signup_date,
    "acquisition_channel": acquisition_channel,
    "device_type": device_type,
    "region": region,
    "customer_type": customer_type,
    "viewed_product": viewed_product,
    "started_checkout": started_checkout,
    "completed_purchase": completed_purchase,
    "revenue": revenue,
    "returning_user": returning_user,
    "support_contacted": support_contacted
})

# -----------------------------
# 7. Sort by customer ID
# -----------------------------

df = df.sort_values("customer_id").reset_index(drop=True)

# -----------------------------
# 8. Save dataset
# -----------------------------

df.to_csv("customer_journey.csv", index=False)

# -----------------------------
# 9. Display basic information
# -----------------------------

print("Dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nPurchase summary:")
print(f"Total customers: {len(df)}")
print(f"Completed purchases: {df['completed_purchase'].sum()}")
print(
    f"Conversion rate: "
    f"{df['completed_purchase'].mean() * 100:.2f}%"
)

print("\nTotal revenue:")
print(f"${df['revenue'].sum():,.2f}")