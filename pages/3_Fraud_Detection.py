import streamlit as st
import plotly.express as px
import pandas as pd

from utils import setup_page, premium_hero, metric_card, insight_card, section_title, style_plotly
from data_utils import load_data


setup_page("Fraud Detection", icon="🚨")

customers, loans, transactions = load_data()

premium_hero(
    "🚨 Fraud Detection Intelligence",
    """
    Real-time banking fraud monitoring using transaction behavior, high-value activity,
    cross-border payments, night transactions, unusual channels, and rule-based risk scoring.
    """,
    badge="Transaction Fraud Risk Engine"
)


# -----------------------------
# FRAUD KPIs
# -----------------------------
section_title("📌 Fraud Detection KPIs")

fraud_df = transactions[transactions["fraud_flag"] == 1]
high_risk_df = transactions[transactions["fraud_risk_score"] >= 70]
medium_risk_df = transactions[
    (transactions["fraud_risk_score"] >= 40) &
    (transactions["fraud_risk_score"] < 70)
]

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Transactions", f"{len(transactions):,}", "Total monitored")

with c2:
    metric_card("Fraud Alerts", f"{len(fraud_df):,}", "Flagged suspicious activity")

with c3:
    metric_card("High Risk Value", f"£{high_risk_df['amount'].sum():,.0f}", "Exposure at risk")

with c4:
    metric_card("Avg Fraud Score", f"{transactions['fraud_risk_score'].mean():.1f}", "Risk engine score")

c5, c6, c7, c8 = st.columns(4)

with c5:
    metric_card("High Risk Tx", f"{len(high_risk_df):,}", "Score ≥ 70")

with c6:
    metric_card("Medium Risk Tx", f"{len(medium_risk_df):,}", "Score 40–69")

with c7:
    metric_card("Cross-Border Tx", f"{transactions['is_cross_border'].sum():,}", "Non-domestic activity")

with c8:
    metric_card("Night Tx", f"{transactions['is_night_tx'].sum():,}", "00:00–05:00 activity")


# -----------------------------
# FRAUD INTELLIGENCE
# -----------------------------
section_title("🧠 Fraud Risk Intelligence")

if len(fraud_df) > 0:
    insight_card(
        f"⚠️ {len(fraud_df):,} suspicious transactions detected. Fraud operations should prioritize high-value and cross-border alerts.",
        level="critical"
    )
else:
    insight_card("✅ No suspicious transactions detected.", level="good")

if high_risk_df["amount"].sum() > 500000:
    insight_card(
        "⚠️ High-risk transaction exposure is significant. Review large-value alerts immediately.",
        level="critical"
    )
else:
    insight_card("✅ High-risk exposure appears manageable.", level="good")

if transactions["is_night_tx"].sum() > len(transactions) * 0.20:
    insight_card(
        "⚠️ Night-time transaction activity is unusually high.",
        level="risk"
    )
else:
    insight_card("✅ Night-time activity appears within normal range.", level="good")


# -----------------------------
# RISK DISTRIBUTION
# -----------------------------
section_title("📊 Fraud Risk Distribution")

transactions["fraud_risk_level"] = transactions["fraud_risk_score"].apply(
    lambda x: "High" if x >= 70 else "Medium" if x >= 40 else "Low"
)

risk_counts = transactions["fraud_risk_level"].value_counts().reset_index()
risk_counts.columns = ["Risk Level", "Count"]

r1, r2 = st.columns(2)

with r1:
    fig_risk = px.pie(
        risk_counts,
        names="Risk Level",
        values="Count",
        title="Fraud Risk Level Distribution",
        hole=0.45
    )
    st.plotly_chart(style_plotly(fig_risk), use_container_width=True)

with r2:
    fig_score = px.histogram(
        transactions,
        x="fraud_risk_score",
        color="fraud_risk_level",
        nbins=40,
        title="Fraud Risk Score Distribution"
    )
    st.plotly_chart(style_plotly(fig_score), use_container_width=True)


# -----------------------------
# TRANSACTION TYPE ANALYSIS
# -----------------------------
section_title("💳 Fraud by Transaction Type")

type_summary = (
    transactions.groupby("transaction_type")
    .agg(
        transactions=("transaction_id", "count"),
        total_value=("amount", "sum"),
        fraud_alerts=("fraud_flag", "sum"),
        avg_fraud_score=("fraud_risk_score", "mean"),
        high_value_tx=("is_high_value", "sum"),
        cross_border_tx=("is_cross_border", "sum"),
    )
    .reset_index()
)

type_summary["fraud_rate_%"] = (
    type_summary["fraud_alerts"] / type_summary["transactions"] * 100
)

t1, t2 = st.columns(2)

with t1:
    fig_type_alerts = px.bar(
        type_summary.sort_values("fraud_alerts", ascending=False),
        x="transaction_type",
        y="fraud_alerts",
        title="Fraud Alerts by Transaction Type"
    )
    st.plotly_chart(style_plotly(fig_type_alerts), use_container_width=True)

with t2:
    fig_type_rate = px.bar(
        type_summary.sort_values("fraud_rate_%", ascending=False),
        x="transaction_type",
        y="fraud_rate_%",
        title="Fraud Rate by Transaction Type"
    )
    st.plotly_chart(style_plotly(fig_type_rate), use_container_width=True)

st.dataframe(type_summary, use_container_width=True)


# -----------------------------
# CHANNEL AND COUNTRY ANALYSIS
# -----------------------------
section_title("🌍 Channel & Country Risk")

country_summary = (
    transactions.groupby("country")
    .agg(
        transactions=("transaction_id", "count"),
        value=("amount", "sum"),
        fraud_alerts=("fraud_flag", "sum"),
        avg_fraud_score=("fraud_risk_score", "mean"),
    )
    .reset_index()
)

country_summary["fraud_rate_%"] = (
    country_summary["fraud_alerts"] / country_summary["transactions"] * 100
)

channel_summary = (
    transactions.groupby("channel")
    .agg(
        transactions=("transaction_id", "count"),
        value=("amount", "sum"),
        fraud_alerts=("fraud_flag", "sum"),
        avg_fraud_score=("fraud_risk_score", "mean"),
    )
    .reset_index()
)

channel_summary["fraud_rate_%"] = (
    channel_summary["fraud_alerts"] / channel_summary["transactions"] * 100
)

g1, g2 = st.columns(2)

with g1:
    fig_country = px.bar(
        country_summary.sort_values("avg_fraud_score", ascending=False),
        x="country",
        y="avg_fraud_score",
        title="Average Fraud Score by Country"
    )
    st.plotly_chart(style_plotly(fig_country), use_container_width=True)

with g2:
    fig_channel = px.bar(
        channel_summary.sort_values("avg_fraud_score", ascending=False),
        x="channel",
        y="avg_fraud_score",
        title="Average Fraud Score by Channel"
    )
    st.plotly_chart(style_plotly(fig_channel), use_container_width=True)

st.dataframe(country_summary, use_container_width=True)
st.dataframe(channel_summary, use_container_width=True)


# -----------------------------
# TIME ANALYSIS
# -----------------------------
section_title("⏱️ Time-Based Fraud Pattern")

hour_summary = (
    transactions.groupby("hour")
    .agg(
        transactions=("transaction_id", "count"),
        fraud_alerts=("fraud_flag", "sum"),
        avg_fraud_score=("fraud_risk_score", "mean"),
    )
    .reset_index()
)

h1, h2 = st.columns(2)

with h1:
    fig_hour = px.line(
        hour_summary,
        x="hour",
        y="fraud_alerts",
        title="Fraud Alerts by Hour",
        markers=True
    )
    st.plotly_chart(style_plotly(fig_hour), use_container_width=True)

with h2:
    fig_hour_score = px.line(
        hour_summary,
        x="hour",
        y="avg_fraud_score",
        title="Average Fraud Score by Hour",
        markers=True
    )
    st.plotly_chart(style_plotly(fig_hour_score), use_container_width=True)


# -----------------------------
# HIGH RISK WATCHLIST
# -----------------------------
section_title("🚨 High-Risk Transaction Watchlist")

watch_cols = [
    "transaction_id",
    "customer_id",
    "branch",
    "segment",
    "transaction_type",
    "amount",
    "country",
    "channel",
    "hour",
    "fraud_risk_score",
    "fraud_risk_level",
    "is_high_value",
    "is_cross_border",
    "is_night_tx",
]

if len(high_risk_df) > 0:
    st.dataframe(
        high_risk_df[watch_cols].sort_values("fraud_risk_score", ascending=False),
        use_container_width=True
    )
else:
    insight_card("✅ No high-risk transactions found.", level="good")


# -----------------------------
# MANUAL TRANSACTION SCORING
# -----------------------------
section_title("🔍 Manual Fraud Risk Scoring")

with st.expander("Score a New Transaction"):
    m1, m2, m3 = st.columns(3)

    with m1:
        amount = st.number_input("Transaction Amount", 1.0, 100000.0, 500.0)
        transaction_type = st.selectbox(
            "Transaction Type",
            [
                "Card Payment",
                "ATM Withdrawal",
                "Bank Transfer",
                "Online Purchase",
                "Cash Deposit",
                "International Transfer",
            ]
        )

    with m2:
        country = st.selectbox(
            "Country",
            ["UK", "Italy", "Germany", "France", "Spain", "Nigeria", "Gambia", "UAE", "USA"]
        )
        channel = st.selectbox(
            "Channel",
            ["Mobile", "Web", "Branch", "ATM", "POS"]
        )

    with m3:
        hour = st.slider("Transaction Hour", 0, 23, 14)

    if st.button("Score Transaction", use_container_width=True):
        score = 0
        reasons = []

        if amount > 7500:
            score += 35
            reasons.append("High-value transaction")

        if 0 <= hour <= 5:
            score += 18
            reasons.append("Night-time transaction")

        if country != "UK":
            score += 20
            reasons.append("Cross-border activity")

        if transaction_type == "International Transfer":
            score += 22
            reasons.append("International transfer risk")

        score = min(score + 10, 100)

        risk_level = "High" if score >= 70 else "Medium" if score >= 40 else "Low"

        metric_card("Fraud Risk Score", f"{score}/100", f"{risk_level} risk")

        if reasons:
            for reason in reasons:
                insight_card(f"⚠️ {reason}", level="risk")
        else:
            insight_card("✅ No major fraud risk indicators detected.", level="good")

        if risk_level == "High":
            insight_card("🚨 Recommendation: block or hold transaction for manual review.", level="critical")
        elif risk_level == "Medium":
            insight_card("⚠️ Recommendation: allow with enhanced monitoring or step-up authentication.", level="risk")
        else:
            insight_card("✅ Recommendation: transaction can proceed normally.", level="good")


# -----------------------------
# DOWNLOAD
# -----------------------------
section_title("⬇️ Export Fraud Detection Data")

st.download_button(
    "Download Fraud Risk Transactions",
    transactions.to_csv(index=False),
    "finguard_fraud_detection_transactions.csv",
    "text/csv",
    use_container_width=True
)
