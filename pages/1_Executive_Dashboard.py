import streamlit as st
import plotly.express as px
import pandas as pd

from utils import setup_page, premium_hero, metric_card, insight_card, section_title, style_plotly
from data_utils import load_data, calculate_executive_kpis


setup_page("Executive Dashboard", icon="📊")

customers, loans, transactions = load_data()
kpis = calculate_executive_kpis(customers, loans, transactions)


premium_hero(
    "📊 Executive Banking Dashboard",
    """
    Strategic overview of customer base, deposits, loan book exposure, credit risk,
    fraud signals, AML alerts, branch performance, and transaction activity.
    """,
    badge="Executive Financial Intelligence"
)


# -----------------------------
# KPIs
# -----------------------------
section_title("📌 Executive KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Customers", f"{kpis['total_customers']:,}", "Active customer base")

with c2:
    metric_card("Total Deposits", f"£{kpis['total_deposits']:,.0f}", "Positive balances")

with c3:
    metric_card("Loan Book", f"£{kpis['total_loan_book']:,.0f}", "Credit exposure")

with c4:
    metric_card("Transactions", f"{kpis['total_transactions']:,}", "Monitored activity")

c5, c6, c7, c8 = st.columns(4)

with c5:
    metric_card("Fraud Alerts", f"{kpis['fraud_cases']:,}", "Suspicious transactions")

with c6:
    metric_card("AML Alerts", f"{kpis['aml_cases']:,}", "Compliance monitoring")

with c7:
    metric_card("Default Rate", f"{kpis['default_rate']:.2f}%", "Loan portfolio risk")

with c8:
    metric_card("Avg Credit Score", f"{kpis['avg_credit_score']:.0f}", "Customer credit quality")


# -----------------------------
# EXECUTIVE INSIGHTS
# -----------------------------
section_title("🧠 Executive Risk Intelligence")

i1, i2, i3 = st.columns(3)

with i1:
    if kpis["default_rate"] > 20:
        insight_card("⚠️ Credit default risk is elevated. Review high-risk loan segments.", level="critical")
    elif kpis["default_rate"] > 10:
        insight_card("⚠️ Credit default risk requires monitoring.", level="risk")
    else:
        insight_card("✅ Credit portfolio appears stable.", level="good")

with i2:
    if kpis["fraud_cases"] > 300:
        insight_card("⚠️ Fraud alert volume is high. Fraud operations should review flagged transactions.", level="critical")
    else:
        insight_card("✅ Fraud alert volume is within manageable range.", level="good")

with i3:
    if kpis["aml_cases"] > 300:
        insight_card("⚠️ AML alert volume is high. Compliance team should review suspicious activity.", level="critical")
    else:
        insight_card("✅ AML monitoring appears stable.", level="good")


# -----------------------------
# CUSTOMER AND BRANCH PERFORMANCE
# -----------------------------
section_title("🏦 Customer & Branch Performance")

branch_summary = (
    customers.groupby("branch")
    .agg(
        customers=("customer_id", "count"),
        deposits=("account_balance", "sum"),
        avg_credit_score=("credit_score", "mean"),
        avg_churn_risk=("churn_risk", "mean"),
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
    fig_branch_customers = px.bar(
        branch_summary.sort_values("customers", ascending=False),
        x="branch",
        y="customers",
        title="Customers by Branch"
    )
    st.plotly_chart(style_plotly(fig_branch_customers), use_container_width=True)

st.dataframe(branch_summary, use_container_width=True)


# -----------------------------
# SEGMENT INTELLIGENCE
# -----------------------------
section_title("👥 Customer Segment Intelligence")

segment_summary = (
    customers.groupby("segment")
    .agg(
        customers=("customer_id", "count"),
        deposits=("account_balance", "sum"),
        avg_income=("annual_income", "mean"),
        avg_credit_score=("credit_score", "mean"),
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
        title="Customer Segments",
        hole=0.45
    )
    st.plotly_chart(style_plotly(fig_segment), use_container_width=True)

with s2:
    fig_segment_deposits = px.bar(
        segment_summary.sort_values("deposits", ascending=False),
        x="segment",
        y="deposits",
        title="Deposits by Customer Segment"
    )
    st.plotly_chart(style_plotly(fig_segment_deposits), use_container_width=True)

st.dataframe(segment_summary, use_container_width=True)


# -----------------------------
# LOAN PORTFOLIO
# -----------------------------
section_title("💳 Loan Portfolio Risk")

loan_branch = (
    loans.groupby("branch")
    .agg(
        loans=("loan_id", "count"),
        loan_book=("loan_amount", "sum"),
        avg_default_probability=("default_probability", "mean"),
        defaults=("default_flag", "sum"),
    )
    .reset_index()
)

loan_branch["default_rate_%"] = loan_branch["defaults"] / loan_branch["loans"] * 100

l1, l2 = st.columns(2)

with l1:
    fig_loan_book = px.bar(
        loan_branch.sort_values("loan_book", ascending=False),
        x="branch",
        y="loan_book",
        title="Loan Book by Branch"
    )
    st.plotly_chart(style_plotly(fig_loan_book), use_container_width=True)

with l2:
    fig_default = px.bar(
        loan_branch.sort_values("default_rate_%", ascending=False),
        x="branch",
        y="default_rate_%",
        title="Default Rate by Branch"
    )
    st.plotly_chart(style_plotly(fig_default), use_container_width=True)

st.dataframe(loan_branch, use_container_width=True)


# -----------------------------
# TRANSACTION RISK
# -----------------------------
section_title("🚨 Transaction Risk Overview")

risk_summary = (
    transactions.groupby("transaction_type")
    .agg(
        transactions=("transaction_id", "count"),
        total_value=("amount", "sum"),
        fraud_alerts=("fraud_flag", "sum"),
        aml_alerts=("aml_flag", "sum"),
        avg_fraud_risk=("fraud_risk_score", "mean"),
        avg_aml_risk=("aml_risk_score", "mean"),
    )
    .reset_index()
)

t1, t2 = st.columns(2)

with t1:
    fig_fraud = px.bar(
        risk_summary.sort_values("fraud_alerts", ascending=False),
        x="transaction_type",
        y="fraud_alerts",
        title="Fraud Alerts by Transaction Type"
    )
    st.plotly_chart(style_plotly(fig_fraud), use_container_width=True)

with t2:
    fig_aml = px.bar(
        risk_summary.sort_values("aml_alerts", ascending=False),
        x="transaction_type",
        y="aml_alerts",
        title="AML Alerts by Transaction Type"
    )
    st.plotly_chart(style_plotly(fig_aml), use_container_width=True)

st.dataframe(risk_summary, use_container_width=True)


# -----------------------------
# ACTIVITY TREND
# -----------------------------
section_title("📈 Transaction Activity Trend")

daily_tx = (
    transactions.copy()
    .assign(date_only=lambda x: pd.to_datetime(x["date"]).dt.date)
    .groupby("date_only")
    .agg(
        transactions=("transaction_id", "count"),
        value=("amount", "sum"),
        fraud_alerts=("fraud_flag", "sum"),
        aml_alerts=("aml_flag", "sum"),
    )
    .reset_index()
)

trend1, trend2 = st.columns(2)

with trend1:
    fig_daily_value = px.line(
        daily_tx,
        x="date_only",
        y="value",
        title="Daily Transaction Value",
        markers=True
    )
    st.plotly_chart(style_plotly(fig_daily_value), use_container_width=True)

with trend2:
    fig_daily_alerts = px.line(
        daily_tx,
        x="date_only",
        y=["fraud_alerts", "aml_alerts"],
        title="Daily Fraud & AML Alerts",
        markers=True
    )
    st.plotly_chart(style_plotly(fig_daily_alerts), use_container_width=True)


# -----------------------------
# DOWNLOAD
# -----------------------------
section_title("⬇️ Export Executive Data")

st.download_button(
    "Download Branch Summary",
    branch_summary.to_csv(index=False),
    "finguard_branch_summary.csv",
    "text/csv",
    use_container_width=True
)
