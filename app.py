import streamlit as st
import pandas as pd
import plotly.express as px

import joblib

@st.cache_resource
def load_prediction_model():
    return joblib.load("purchase_prediction_model.pkl")

prediction_model = load_prediction_model()

# Load dataset
df = pd.read_csv("customer_journey.csv")

# Page setup
st.set_page_config(
    page_title="Customer Journey & Conversion Insights",
    layout="wide"
)

st.title("Customer Journey & Conversion Insights")
st.write("Analyze customer behavior, funnel performance, and conversion patterns.")

# Core KPIs
total_customers = len(df)

product_viewers = df["viewed_product"].sum()
checkout_starters = df["started_checkout"].sum()
purchasers = df["completed_purchase"].sum()

product_view_rate = round(product_viewers / total_customers * 100, 2)
checkout_rate = round(checkout_starters / product_viewers * 100, 2)
purchase_rate = round(purchasers / checkout_starters * 100, 2)

total_revenue = df["revenue"].sum()
average_order_value = total_revenue / purchasers

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Product View Rate", f"{product_view_rate}%")
col3.metric("Purchase Conversion", f"{purchase_rate}%")
col4.metric("Total Revenue", f"{total_revenue:,.0f}")

# Funnel Analysis
st.subheader("Customer Funnel")

stages = [
    "Customers",
    "Product Viewed",
    "Checkout Started",
    "Purchase Completed"
]

funnel_data = pd.DataFrame({
    "Stage": stages,
    "Customers": [
        total_customers,
        product_viewers,
        checkout_starters,
        purchasers
    ]
})

fig = px.bar(
    funnel_data,
    x="Stage",
    y="Customers",
    category_orders={"Stage": stages},
    text="Customers"
)

fig.update_layout(
    xaxis_title="Customer Journey Stage",
    yaxis_title="Number of Customers"
)

st.plotly_chart(fig, use_container_width=True)

# Conversion by Acquisition Channel
st.subheader("Conversion by Acquisition Channel")

channel_conversion = (
    df.groupby("acquisition_channel")["completed_purchase"]
    .mean()
    .mul(100)
    .round(2)
    .reset_index()
)

fig_channel = px.bar(
    channel_conversion,
    x="acquisition_channel",
    y="completed_purchase",
    text="completed_purchase",
    labels={
        "acquisition_channel": "Acquisition Channel",
        "completed_purchase": "Conversion Rate (%)"
    }
)

st.plotly_chart(fig_channel, use_container_width=True)

channel_performance = (
    df.groupby("acquisition_channel")
    .agg(
        total_customers=("customer_id", "nunique"),
        total_purchases=("completed_purchase", "sum"),
        conversion_rate=("completed_purchase", "mean")
    )
    .reset_index()
)

channel_performance["conversion_rate"] = (
    channel_performance["conversion_rate"] * 100
).round(2)

st.subheader("Channel Performance")
st.dataframe(channel_performance)


st.subheader("Revenue by Acquisition Channel")

channel_revenue = (
    df.groupby("acquisition_channel")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_revenue = px.bar(
    channel_revenue,
    x="acquisition_channel",
    y="revenue",
    text="revenue",
    category_orders={
        "acquisition_channel": channel_revenue["acquisition_channel"].tolist()
    }
)

st.plotly_chart(fig_revenue, use_container_width=True)

st.subheader("Average Order Value by Channel")

channel_aov = (
    df.groupby("acquisition_channel")
    .agg(
        total_revenue=("revenue", "sum"),
        total_purchases=("completed_purchase", "sum")
    )
)

channel_aov["AOV"] = (
    channel_aov["total_revenue"] /
    channel_aov["total_purchases"]
).round(2)

st.dataframe(channel_aov)

st.subheader("Revenue per Customer by Channel")

channel_rpc = (
    df.groupby("acquisition_channel")
    .agg(
        total_revenue=("revenue", "sum"),
        total_customers=("customer_id", "nunique")
    )
)

channel_rpc["revenue_per_customer"] = (
    channel_rpc["total_revenue"] /
    channel_rpc["total_customers"]
).round(2)

st.dataframe(channel_rpc)

st.subheader("New vs Returning Customers")

customer_conversion = (
    df.groupby("customer_type")["completed_purchase"]
    .mean()
    .mul(100)
    .round(2)
)

st.dataframe(customer_conversion)

st.bar_chart(customer_conversion)

st.subheader("Conversion by Device Type")

device_conversion = (
    df.groupby("device_type")["completed_purchase"]
    .mean()
    .mul(100)
    .round(2)
)

st.bar_chart(device_conversion)

st.header("Customer Purchase Prediction")

channel = st.selectbox(
    "Acquisition Channel",
    ["Organic", "Paid Search", "Social Media", "Email", "Referral"]
)

device = st.selectbox(
    "Device Type",
    ["Mobile", "Desktop", "Tablet"]
)

region = st.selectbox(
    "Region",
    ["North", "South", "East", "West"]
)

customer_type = st.selectbox(
    "Customer Type",
    ["New", "Returning"]
)

viewed = st.checkbox("Viewed Product")
checkout = st.checkbox("Started Checkout")

if st.button("Predict Purchase"):
    input_data = pd.DataFrame([{
        "acquisition_channel": channel,
        "device_type": device,
        "region": region,
        "customer_type": customer_type,
        "viewed_product": int(viewed),
        "started_checkout": int(checkout)
    }])

    probability = prediction_model.predict_proba(input_data)[0][1]

    st.metric(
        "Estimated Purchase Probability",
        f"{probability:.1%}"
    )

st.header("AI-Powered Business Insights")

channel_insights = (
    df.groupby("acquisition_channel")
    .agg(
        customers=("customer_id", "count"),
        purchases=("completed_purchase", "sum")
    )
)

channel_insights["conversion_rate"] = (
    channel_insights["purchases"]
    / channel_insights["customers"] * 100
)

best_channel = channel_insights["conversion_rate"].idxmax()

st.success(
    f"Top converting channel: {best_channel}"
)

worst_channel = channel_insights["conversion_rate"].idxmin()

best_rate = channel_insights.loc[best_channel, "conversion_rate"]
worst_rate = channel_insights.loc[worst_channel, "conversion_rate"]

st.info(
    f"Opportunity: {worst_channel} has the lowest conversion "
    f"rate ({worst_rate:.2f}%). Investigate customer drop-offs "
    f"and compare its journey with {best_channel} "
    f"({best_rate:.2f}%)."
)
st.subheader("Customer Journey Drop-off Insights")

viewed_count = df["viewed_product"].sum()
checkout_count = df["started_checkout"].sum()
purchase_count = df["completed_purchase"].sum()

view_to_checkout = (
    (viewed_count - checkout_count) / viewed_count * 100
    if viewed_count else 0
)

checkout_to_purchase = (
    (checkout_count - purchase_count) / checkout_count * 100
    if checkout_count else 0
)

st.write(f"Product View → Checkout Drop-off: {view_to_checkout:.2f}%")
st.write(f"Checkout → Purchase Drop-off: {checkout_to_purchase:.2f}%")

if checkout_to_purchase > view_to_checkout:
    st.warning(
        "Recommendation: Investigate checkout friction, "
        "payment failures, and unexpected fees."
    )
else:
    st.warning(
        "Recommendation: Investigate product-page engagement "
        "and barriers to starting checkout."
    )
st.subheader("Customer Segment Insights")

segment_insights = (
    df.groupby("customer_type")
    .agg(
        customers=("customer_id", "count"),
        purchases=("completed_purchase", "sum")
    )
)

segment_insights["conversion_rate"] = (
    segment_insights["purchases"]
    / segment_insights["customers"] * 100
)

new_rate = segment_insights.loc["New", "conversion_rate"]
returning_rate = segment_insights.loc["Returning", "conversion_rate"]

st.write(f"New Customer Conversion: {new_rate:.2f}%")
st.write(f"Returning Customer Conversion: {returning_rate:.2f}%")

if returning_rate > new_rate:
    st.info(
        "Recommendation: Investigate onboarding and first-purchase "
        "friction for new customers."
    )
else:
    st.info(
        "Recommendation: Investigate repeat-purchase barriers "
        "and customer retention opportunities."
    )
st.subheader("Revenue Insights")

revenue_by_channel = df.groupby("acquisition_channel")["revenue"].sum()

top_revenue_channel = revenue_by_channel.idxmax()
top_revenue = revenue_by_channel.max()

st.success(
    f"Highest revenue channel: {top_revenue_channel} "
    f"with revenue of {top_revenue:,.2f}"
)

if top_revenue_channel != best_channel:
    st.info(
        f"{top_revenue_channel} generates the most revenue, "
        f"while {best_channel} has the highest conversion rate. "
        "Compare customer value and acquisition costs before "
        "deciding where to increase marketing investment."
    )
else:
    st.info(
        f"{top_revenue_channel} leads in both revenue and conversion. "
        "Investigate whether this performance can scale profitably."
    )

