import time
import pandas as pd
import streamlit as st

from ui_utils import setup_page, premium_hero, metric_card, insight_card, section_title
from data_utils import (
    load_data,
    calculate_executive_kpis,
    calculate_credit_kpis,
    calculate_fraud_kpis,
    calculate_aml_kpis,
    calculate_customer_kpis,
)
from ai_insights import generate_executive_insights


setup_page("AI Executive Copilot", icon="🧠")

customers, loans, transactions = load_data()

kpis = calculate_executive_kpis(customers, loans, transactions)
credit_kpis = calculate_credit_kpis(loans)
fraud_kpis = calculate_fraud_kpis(transactions)
aml_kpis = calculate_aml_kpis(transactions)
customer_kpis = calculate_customer_kpis(customers)


def stream_text(text, speed=0.01):
    for word in str(text).split(" "):
        yield word + " "
        time.sleep(speed)


premium_hero(
    "🧠 AI Executive Copilot",
    "Board-level banking AI assistant for credit risk, fraud, AML, customer churn, forecasting, and executive decision support.",
    badge="Executive Banking AI Assistant"
)


if "exec_copilot_history" not in st.session_state:
    st.session_state.exec_copilot_history = []

if "exec_prompt" not in st.session_state:
    st.session_state.exec_prompt = None


section_title("📌 Executive AI Snapshot")

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Deposits", f"£{kpis['total_deposits']:,.0f}", "Customer balances")

with c2:
    metric_card("Loan Book", f"£{kpis['total_loan_book']:,.0f}", "Credit exposure")

with c3:
    metric_card("Fraud Alerts", f"{kpis['fraud_cases']:,}", "Suspicious activity")

with c4:
    metric_card("AML Alerts", f"{kpis['aml_cases']:,}", "Compliance workload")

c5, c6, c7, c8 = st.columns(4)

with c5:
    metric_card("Default Rate", f"{kpis['default_rate']:.2f}%", "Portfolio risk")

with c6:
    metric_card("High-Risk Loans", f"{credit_kpis['high_risk_loans']:,}", "Credit review")

with c7:
    metric_card("High-Risk Fraud", f"{fraud_kpis['high_risk_transactions']:,}", "Fraud queue")

with c8:
    metric_card("High Churn", f"{customer_kpis['high_churn_customers']:,}", "Retention queue")


section_title("🧠 Auto Executive Insights")

for insight in generate_executive_insights(
    kpis,
    credit_kpis,
    fraud_kpis,
    aml_kpis,
    customer_kpis,
):
    level = "risk" if "⚠️" in insight or "📌" in insight else "good"
    insight_card(insight, level=level)


def answer_executive_question(question):
    q = question.lower()

    if "credit" in q or "loan" in q or "default" in q:
        return f"""
### Credit Risk Executive View

- Loan accounts: **{credit_kpis['loan_accounts']:,}**
- Loan book exposure: **£{credit_kpis['loan_book']:,.0f}**
- High-risk loans: **{credit_kpis['high_risk_loans']:,}**
- Medium-risk loans: **{credit_kpis['medium_risk_loans']:,}**
- Average default probability: **{credit_kpis['avg_default_probability']:.2f}%**
- Average credit score: **{credit_kpis['avg_credit_score']:.0f}**

**Executive action:** Prioritize high-risk loans for affordability review, exposure reduction, and repayment monitoring.
"""

    if "fraud" in q or "suspicious" in q or "transaction" in q:
        return f"""
### Fraud Risk Executive View

- Transactions monitored: **{fraud_kpis['transactions']:,}**
- Fraud alerts: **{fraud_kpis['fraud_alerts']:,}**
- High-risk transactions: **{fraud_kpis['high_risk_transactions']:,}**
- Medium-risk transactions: **{fraud_kpis['medium_risk_transactions']:,}**
- High-risk transaction value: **£{fraud_kpis['high_risk_value']:,.0f}**
- Average fraud score: **{fraud_kpis['avg_fraud_score']:.1f}/100**

**Executive action:** Review high-value, night-time, cross-border, and international transfer transactions first.
"""

    if "aml" in q or "compliance" in q or "kyc" in q or "laundering" in q:
        return f"""
### AML & Compliance Executive View

- AML alerts: **{aml_kpis['aml_alerts']:,}**
- AML exposure: **£{aml_kpis['aml_exposure']:,.0f}**
- High-value transactions: **{aml_kpis['high_value_transactions']:,}**
- Cross-border transactions: **{aml_kpis['cross_border_transactions']:,}**
- Average AML score: **{aml_kpis['avg_aml_score']:.1f}/100**

**Executive action:** Escalate high-value, cross-border, cash-deposit, and EDD-country transactions for compliance review.
"""

    if "customer" in q or "churn" in q or "deposit" in q:
        return f"""
### Customer Intelligence Executive View

- Customers: **{customer_kpis['customers']:,}**
- High-churn customers: **{customer_kpis['high_churn_customers']:,}**
- Average products per customer: **{customer_kpis['avg_products']:.1f}**
- Total deposits: **£{customer_kpis['total_deposits']:,.0f}**
- Average churn risk: **{customer_kpis['avg_churn_risk']:.1f}/100**

**Executive action:** Prioritize high-churn, high-balance customers for retention campaigns and relationship management.
"""

    return f"""
### Executive Banking Summary

- Customers: **{kpis['total_customers']:,}**
- Deposits: **£{kpis['total_deposits']:,.0f}**
- Loan book: **£{kpis['total_loan_book']:,.0f}**
- Transactions monitored: **{kpis['total_transactions']:,}**
- Fraud alerts: **{kpis['fraud_cases']:,}**
- AML alerts: **{kpis['aml_cases']:,}**
- Default rate: **{kpis['default_rate']:.2f}%**
- Average credit score: **{kpis['avg_credit_score']:.0f}**

### Management Priorities

1. Review high-risk credit accounts.
2. Investigate suspicious high-value transactions.
3. Escalate AML alerts involving cross-border or cash-deposit activity.
4. Launch retention campaigns for high-churn customers.
5. Monitor forecasted alert volume for capacity planning.
"""


section_title("⚡ Executive Quick Prompts")

questions = [
    "Give me an executive banking summary",
    "What are the biggest credit risks?",
    "Which fraud risks need attention?",
    "What should compliance prioritize?",
    "Which customers are likely to churn?",
    "What should management do today?",
]

cols = st.columns(3)

for i, q in enumerate(questions):
    if cols[i % 3].button(q, use_container_width=True):
        st.session_state.exec_prompt = q
        st.rerun()


section_title("💬 Ask the Executive Copilot")

user_input = st.chat_input(
    "Ask about credit risk, fraud, AML, customers, deposits, management priorities..."
)

if st.session_state.exec_prompt:
    user_input = st.session_state.exec_prompt
    st.session_state.exec_prompt = None

if user_input:
    st.session_state.exec_copilot_history.append(("user", user_input))
    response = answer_executive_question(user_input)
    st.session_state.exec_copilot_history.append(("assistant", response))

for role, message in st.session_state.exec_copilot_history:
    with st.chat_message(role):
        if role == "assistant":
            st.write_stream(stream_text(message))
        else:
            st.markdown(message)


section_title("🧠 Executive Copilot Memory")

if st.session_state.exec_copilot_history:
    memory_df = pd.DataFrame(
        st.session_state.exec_copilot_history,
        columns=["role", "message"]
    )
    st.dataframe(memory_df.tail(12), use_container_width=True)

    if st.button("Clear Executive Copilot Memory", use_container_width=True):
        st.session_state.exec_copilot_history = []
        st.rerun()
else:
    insight_card("No executive copilot memory yet. Ask a question to begin.", level="risk")
