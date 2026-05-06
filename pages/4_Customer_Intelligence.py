import streamlit as st
import plotly.express as px

from ui_utils import setup_page, premium_hero, metric_card, insight_card, section_title, style_plotly
from data_utils import load_data


setup_page("Customer Intelligence", icon="👥")

customers, loans, transactions = load_data()

premium_hero(
    "👥 Customer Intelligence",
    """
    Customer analytics for segmentation, churn risk, product engagement,
    branch performance, deposits, income, and relationship value.
    """,
    badge="Customer Analytics & Churn Intelligence"
)

# -----------------------------
# KPIs
# -----------------------------
section_title("📌 Customer KPIs")

high_churn = customers[customers["churn_risk"] >= 70]
medium_churn = customers[(customers["churn_risk"] >= 40) & (customers["churn_risk"] < 70)]
premium_customers = customers[customers["segment"] == "Private Banking"]

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Customers", f"{len(customers):,}", "Total customer base")

with c2:
    metric_card("High Churn Risk", f"{len(high_churn):,}", "Risk ≥ 70")

with c3:
    metric_card("Avg Products", f"{customers['num_products'].mean():.1f}", "Product engagement")

with c4:
    metric_card("Private Banking", f"{len(premium_customers):,}", "High-value segment")

c5, c6, c7, c8 = st.columns(4)

with c5:
    metric_card("Total Deposits", f"£{customers['account_balance'].clip(lower=0).sum():,.0f}", "Positive balances")

with c6:
    metric_card("Avg Income", f"£{customers['annual_income'].mean():,.0f}", "Customer income")

with c7:
    metric_card("Avg Credit Score", f"{customers['credit_score'].mean():.0f}", "Credit quality")

with c8:
    metric_card("Avg Churn Risk", f"{customers['churn_risk'].mean():.1f}", "Retention risk")

# -----------------------------
# INSIGHTS
# -----------------------------
section_title("🧠 Customer Intelligence Insights")

if len(high_churn) > 100:
    insight_card(
        f"⚠️ {len(high_churn):,} customers have high churn risk. Retention campaigns should prioritize these accounts.",
        level="critical"
    )
else:
    insight_card("✅ High churn exposure appears manageable.", level="good")

if customers["num_products"].mean() < 3:
    insight_card(
        "⚠️ Average product holding is low. Cross-sell opportunities may exist.",
        level="risk"
    )
else:
    insight_card("✅ Product engagement appears healthy.", level="good")

if customers["account_balance"].median() < 1000:
    insight_card(
        "⚠️ Median customer balance is low. Segment-level profitability should be reviewed.",
        level="risk"
    )
else:
    insight_card("✅ Customer balance profile appears stable.", level="good")

# -----------------------------
# SEGMENT ANALYSIS
# -----------------------------
section_title("🏦 Customer Segment Analysis")

segment_summary = (
    customers.groupby("segment")
    .agg(
        customers=("customer_id", "count"),
        deposits=("account_balance", "sum"),
        avg_income=("annual_income", "mean"),
        avg_credit_score=("credit_score", "mean"),
        avg_products=("num_products", "mean"),
        avg_churn_risk=("churn_risk", "mean"),
    )
    .reset_index()
)

s1, s2 = st.columns(2)

with s1:
    fig_segment = px.pie(
        segment_summary,
        names="segment",
        values="customers",
        title="Customer Segment Distribution",
        hole=0.45
    )
    st.plotly_chart(style_plotly(fig_segment), use_container_width=True)

with s2:
    fig_deposits = px.bar(
        segment_summary.sort_values("deposits", ascending=False),
        x="segment",
        y="deposits",
        title="Deposits by Segment"
    )
    st.plotly_chart(style_plotly(fig_deposits), use_container_width=True)

st.dataframe(segment_summary, use_container_width=True)

# -----------------------------
# CHURN RISK
# -----------------------------
section_title("⚠️ Churn Risk Analysis")

customers["churn_level"] = customers["churn_risk"].apply(
    lambda x: "High" if x >= 70 else "Medium" if x >= 40 else "Low"
)

churn_counts = customers["churn_level"].value_counts().reset_index()
churn_counts.columns = ["Churn Level", "Count"]

ch1, ch2 = st.columns(2)

with ch1:
    fig_churn = px.pie(
        churn_counts,
        names="Churn Level",
        values="Count",
        title="Churn Risk Distribution",
        hole=0.45
    )
    st.plotly_chart(style_plotly(fig_churn), use_container_width=True)

with ch2:
    fig_churn_segment = px.box(
        customers,
        x="segment",
        y="churn_risk",
        color="segment",
        title="Churn Risk by Segment"
    )
    st.plotly_chart(style_plotly(fig_churn_segment), use_container_width=True)

# -----------------------------
# BRANCH CUSTOMER PERFORMANCE
# -----------------------------
section_title("🏛️ Branch Customer Performance")

branch_summary = (
    customers.groupby("branch")
    .agg(
        customers=("customer_id", "count"),
        deposits=("account_balance", "sum"),
        avg_income=("annual_income", "mean"),
        avg_credit_score=("credit_score", "mean"),
        avg_churn_risk=("churn_risk", "mean"),
        avg_products=("num_products", "mean"),
    )
    .reset_index()
)

b1, b2 = st.columns(2)

with b1:
    fig_branch_deposits = px.bar(
        branch_summary.sort_values("deposits", ascending=False),
        x="branch",
        y="deposits",
        title="Deposits by Branch"
    )
    st.plotly_chart(style_plotly(fig_branch_deposits), use_container_width=True)

with b2:
    fig_branch_churn = px.bar(
        branch_summary.sort_values("avg_churn_risk", ascending=False),
        x="branch",
        y="avg_churn_risk",
        title="Average Churn Risk by Branch"
    )
    st.plotly_chart(style_plotly(fig_branch_churn), use_container_width=True)

st.dataframe(branch_summary, use_container_width=True)

# -----------------------------
# PRODUCT ENGAGEMENT
# -----------------------------
section_title("💼 Product Engagement Intelligence")

p1, p2 = st.columns(2)

with p1:
    fig_products = px.histogram(
        customers,
        x="num_products",
        nbins=7,
        title="Number of Products per Customer"
    )
    st.plotly_chart(style_plotly(fig_products), use_container_width=True)

with p2:
    fig_products_churn = px.scatter(
        customers,
        x="num_products",
        y="churn_risk",
        color="segment",
        size="account_balance",
        title="Product Engagement vs Churn Risk"
    )
    st.plotly_chart(style_plotly(fig_products_churn), use_container_width=True)

# -----------------------------
# HIGH VALUE CUSTOMERS
# -----------------------------
section_title("💎 High Value Customer Watchlist")

customers["customer_value_score"] = (
    customers["account_balance"].clip(lower=0) * 0.0004
    + customers["annual_income"] * 0.0002
    + customers["num_products"] * 8
    + customers["years_with_bank"] * 2
).clip(0, 100)

high_value = customers.sort_values("customer_value_score", ascending=False).head(50)

value_cols = [
    "customer_id",
    "branch",
    "segment",
    "age",
    "annual_income",
    "account_balance",
    "credit_score",
    "years_with_bank",
    "num_products",
    "churn_risk",
    "customer_value_score",
]

st.dataframe(high_value[value_cols], use_container_width=True)

# -----------------------------
# RETENTION RECOMMENDATIONS
# -----------------------------
section_title("🎯 Retention & Growth Recommendations")

if len(high_churn) > 0:
    insight_card(
        "Prioritize high-churn customers with low product engagement for retention campaigns.",
        level="risk"
    )

if customers["num_products"].mean() < 3:
    insight_card(
        "Launch cross-sell campaigns for savings, credit cards, insurance, and investment products.",
        level="good"
    )

if not premium_customers.empty:
    insight_card(
        "Private Banking customers should receive personalized relationship management due to high value potential.",
        level="good"
    )

# -----------------------------
# DOWNLOAD
# -----------------------------
section_title("⬇️ Export Customer Intelligence Data")

st.download_button(
    "Download Customer Intelligence Report",
    customers.to_csv(index=False),
    "finguard_customer_intelligence.csv",
    "text/csv",
    use_container_width=True
)
