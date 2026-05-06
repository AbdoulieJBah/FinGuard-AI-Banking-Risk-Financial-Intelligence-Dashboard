import streamlit as st
import plotly.express as px

from utils import setup_page, premium_hero, metric_card, insight_card, section_title, style_plotly
from data_utils import load_data


setup_page("Compliance AML", icon="🛡️")

customers, loans, transactions = load_data()

premium_hero(
    "🛡️ Compliance & AML Monitoring",
    """
    Anti-money laundering and compliance intelligence for suspicious transactions,
    cross-border activity, high-value transfers, risky countries, cash deposits,
    and enhanced due diligence monitoring.
    """,
    badge="AML & Regulatory Risk Intelligence"
)

# -----------------------------
# KPIs
# -----------------------------
section_title("📌 Compliance KPIs")

aml_df = transactions[transactions["aml_flag"] == 1]
high_value = transactions[transactions["amount"] > 10000]
cross_border = transactions[transactions["is_cross_border"] == True]
cash_deposits = transactions[transactions["transaction_type"] == "Cash Deposit"]

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("AML Alerts", f"{len(aml_df):,}", "Flagged transactions")

with c2:
    metric_card("High-Value Tx", f"{len(high_value):,}", "Amount > £10,000")

with c3:
    metric_card("Cross-Border Tx", f"{len(cross_border):,}", "Non-domestic activity")

with c4:
    metric_card("Cash Deposits", f"{len(cash_deposits):,}", "Cash-based monitoring")

c5, c6, c7, c8 = st.columns(4)

with c5:
    metric_card("AML Exposure", f"£{aml_df['amount'].sum():,.0f}", "Flagged value")

with c6:
    metric_card("Avg AML Score", f"{transactions['aml_risk_score'].mean():.1f}", "Compliance risk")

with c7:
    metric_card("High Risk Countries", f"{transactions['country'].isin(['Nigeria', 'Gambia', 'UAE']).sum():,}", "EDD review")

with c8:
    metric_card("Total Tx Value", f"£{transactions['amount'].sum():,.0f}", "Monitored flow")

# -----------------------------
# INSIGHTS
# -----------------------------
section_title("🧠 AML Risk Intelligence")

if len(aml_df) > 0:
    insight_card(
        f"⚠️ {len(aml_df):,} AML alerts detected. Compliance team should review high-value and cross-border transactions.",
        level="critical"
    )
else:
    insight_card("✅ No AML alerts detected.", level="good")

if len(high_value) > 500:
    insight_card(
        "⚠️ High-value transaction volume is elevated. Enhanced monitoring is recommended.",
        level="risk"
    )

if len(cross_border) > len(transactions) * 0.25:
    insight_card(
        "⚠️ Cross-border transaction volume is significant. Review country exposure and customer patterns.",
        level="risk"
    )
else:
    insight_card("✅ Cross-border transaction volume appears manageable.", level="good")

# -----------------------------
# AML RISK DISTRIBUTION
# -----------------------------
section_title("📊 AML Risk Distribution")

transactions["aml_risk_level"] = transactions["aml_risk_score"].apply(
    lambda x: "High" if x >= 65 else "Medium" if x >= 40 else "Low"
)

risk_counts = transactions["aml_risk_level"].value_counts().reset_index()
risk_counts.columns = ["AML Risk Level", "Count"]

r1, r2 = st.columns(2)

with r1:
    fig_risk = px.pie(
        risk_counts,
        names="AML Risk Level",
        values="Count",
        title="AML Risk Level Distribution",
        hole=0.45
    )
    st.plotly_chart(style_plotly(fig_risk), use_container_width=True)

with r2:
    fig_score = px.histogram(
        transactions,
        x="aml_risk_score",
        color="aml_risk_level",
        nbins=40,
        title="AML Risk Score Distribution"
    )
    st.plotly_chart(style_plotly(fig_score), use_container_width=True)

# -----------------------------
# COUNTRY RISK
# -----------------------------
section_title("🌍 Country Exposure & AML Risk")

country_summary = (
    transactions.groupby("country")
    .agg(
        transactions=("transaction_id", "count"),
        value=("amount", "sum"),
        aml_alerts=("aml_flag", "sum"),
        avg_aml_score=("aml_risk_score", "mean"),
    )
    .reset_index()
)

country_summary["aml_alert_rate_%"] = (
    country_summary["aml_alerts"] / country_summary["transactions"] * 100
)

c1, c2 = st.columns(2)

with c1:
    fig_country_alerts = px.bar(
        country_summary.sort_values("aml_alerts", ascending=False),
        x="country",
        y="aml_alerts",
        title="AML Alerts by Country"
    )
    st.plotly_chart(style_plotly(fig_country_alerts), use_container_width=True)

with c2:
    fig_country_score = px.bar(
        country_summary.sort_values("avg_aml_score", ascending=False),
        x="country",
        y="avg_aml_score",
        title="Average AML Score by Country"
    )
    st.plotly_chart(style_plotly(fig_country_score), use_container_width=True)

st.dataframe(country_summary, use_container_width=True)

# -----------------------------
# TRANSACTION TYPE AML RISK
# -----------------------------
section_title("💳 AML Risk by Transaction Type")

type_summary = (
    transactions.groupby("transaction_type")
    .agg(
        transactions=("transaction_id", "count"),
        value=("amount", "sum"),
        aml_alerts=("aml_flag", "sum"),
        avg_aml_score=("aml_risk_score", "mean"),
    )
    .reset_index()
)

type_summary["aml_alert_rate_%"] = (
    type_summary["aml_alerts"] / type_summary["transactions"] * 100
)

t1, t2 = st.columns(2)

with t1:
    fig_type_alerts = px.bar(
        type_summary.sort_values("aml_alerts", ascending=False),
        x="transaction_type",
        y="aml_alerts",
        title="AML Alerts by Transaction Type"
    )
    st.plotly_chart(style_plotly(fig_type_alerts), use_container_width=True)

with t2:
    fig_type_score = px.bar(
        type_summary.sort_values("avg_aml_score", ascending=False),
        x="transaction_type",
        y="avg_aml_score",
        title="Average AML Score by Transaction Type"
    )
    st.plotly_chart(style_plotly(fig_type_score), use_container_width=True)

st.dataframe(type_summary, use_container_width=True)

# -----------------------------
# AML WATCHLIST
# -----------------------------
section_title("🚨 AML Alert Watchlist")

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
    "aml_risk_score",
    "aml_risk_level",
    "is_cross_border",
]

if len(aml_df) > 0:
    aml_display = transactions[transactions["aml_flag"] == 1].copy()
    aml_display["aml_risk_level"] = aml_display["aml_risk_score"].apply(
        lambda x: "High" if x >= 65 else "Medium" if x >= 40 else "Low"
    )

    st.dataframe(
        aml_display[watch_cols].sort_values("aml_risk_score", ascending=False),
        use_container_width=True
    )
else:
    insight_card("✅ No AML alerts currently in the watchlist.", level="good")

# -----------------------------
# MANUAL AML SCORING
# -----------------------------
section_title("🔍 Manual AML Transaction Scoring")

with st.expander("Score a New AML Transaction"):
    m1, m2, m3 = st.columns(3)

    with m1:
        amount = st.number_input("Amount", 1.0, 200000.0, 12000.0)
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
        customer_segment = st.selectbox(
            "Customer Segment",
            ["Retail", "SME", "Corporate", "Private Banking"]
        )

    if st.button("Score AML Risk", use_container_width=True):
        score = 0
        reasons = []

        if amount > 10000:
            score += 30
            reasons.append("High-value transaction")

        if country != "UK":
            score += 25
            reasons.append("Cross-border transaction")

        if country in ["Nigeria", "Gambia", "UAE"]:
            score += 18
            reasons.append("Enhanced due diligence country exposure")

        if transaction_type == "Cash Deposit":
            score += 15
            reasons.append("Cash deposit monitoring trigger")

        if transaction_type == "International Transfer":
            score += 12
            reasons.append("International transfer review")

        score = min(score, 100)
        risk_level = "High" if score >= 65 else "Medium" if score >= 40 else "Low"

        metric_card("AML Risk Score", f"{score}/100", f"{risk_level} risk")

        for reason in reasons:
            insight_card(f"⚠️ {reason}", level="risk")

        if risk_level == "High":
            insight_card("🚨 Recommendation: escalate for enhanced due diligence and compliance review.", level="critical")
        elif risk_level == "Medium":
            insight_card("⚠️ Recommendation: monitor and review customer transaction history.", level="risk")
        else:
            insight_card("✅ Recommendation: no major AML trigger detected.", level="good")

# -----------------------------
# DOWNLOAD
# -----------------------------
section_title("⬇️ Export AML Report")

st.download_button(
    "Download AML Monitoring Report",
    transactions.to_csv(index=False),
    "finguard_aml_monitoring_report.csv",
    "text/csv",
    use_container_width=True
)
