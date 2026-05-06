import streamlit as st
import pandas as pd

from utils import setup_page, premium_hero, metric_card, insight_card, section_title
from data_utils import load_data, calculate_executive_kpis


setup_page("AI Banking Copilot", icon="🤖")

customers, loans, transactions = load_data()
kpis = calculate_executive_kpis(customers, loans, transactions)

premium_hero(
    "🤖 AI Banking Copilot",
    """
    Banking decision assistant for credit risk, fraud detection, AML monitoring,
    customer intelligence, branch performance, and executive financial insights.
    """,
    badge="AI Financial Decision Assistant"
)


# -----------------------------
# SESSION STATE
# -----------------------------
if "copilot_history" not in st.session_state:
    st.session_state.copilot_history = []

if "copilot_prompt" not in st.session_state:
    st.session_state.copilot_prompt = None


# -----------------------------
# ANALYTICAL HELPERS
# -----------------------------
def get_credit_summary():
    high_risk_loans = loans[loans["default_probability"] >= 70]
    medium_risk_loans = loans[
        (loans["default_probability"] >= 40) &
        (loans["default_probability"] < 70)
    ]

    return {
        "loan_accounts": len(loans),
        "loan_book": round(loans["loan_amount"].sum(), 2),
        "average_default_probability": round(loans["default_probability"].mean(), 2),
        "high_risk_loans": len(high_risk_loans),
        "medium_risk_loans": len(medium_risk_loans),
        "average_credit_score": round(loans["credit_score"].mean(), 2),
    }


def get_fraud_summary():
    high_risk = transactions[transactions["fraud_risk_score"] >= 70]
    medium_risk = transactions[
        (transactions["fraud_risk_score"] >= 40) &
        (transactions["fraud_risk_score"] < 70)
    ]

    return {
        "transactions": len(transactions),
        "fraud_alerts": int(transactions["fraud_flag"].sum()),
        "high_risk_transactions": len(high_risk),
        "medium_risk_transactions": len(medium_risk),
        "high_risk_value": round(high_risk["amount"].sum(), 2),
        "average_fraud_score": round(transactions["fraud_risk_score"].mean(), 2),
    }


def get_aml_summary():
    aml_alerts = transactions[transactions["aml_flag"] == 1]
    high_value = transactions[transactions["amount"] > 10000]

    return {
        "aml_alerts": len(aml_alerts),
        "aml_exposure": round(aml_alerts["amount"].sum(), 2),
        "high_value_transactions": len(high_value),
        "cross_border_transactions": int(transactions["is_cross_border"].sum()),
        "average_aml_score": round(transactions["aml_risk_score"].mean(), 2),
    }


def get_customer_summary():
    high_churn = customers[customers["churn_risk"] >= 70]

    return {
        "customers": len(customers),
        "high_churn_customers": len(high_churn),
        "average_churn_risk": round(customers["churn_risk"].mean(), 2),
        "average_products": round(customers["num_products"].mean(), 2),
        "total_deposits": round(customers["account_balance"].clip(lower=0).sum(), 2),
        "average_credit_score": round(customers["credit_score"].mean(), 2),
    }


def answer_question(question):
    q = question.lower()

    credit = get_credit_summary()
    fraud = get_fraud_summary()
    aml = get_aml_summary()
    customer = get_customer_summary()

    if any(word in q for word in ["credit", "loan", "default"]):
        return f"""
### Credit Risk Insight

- Loan accounts monitored: **{credit['loan_accounts']:,}**
- Total loan book: **£{credit['loan_book']:,.0f}**
- Average default probability: **{credit['average_default_probability']:.2f}%**
- High-risk loans: **{credit['high_risk_loans']:,}**
- Medium-risk loans: **{credit['medium_risk_loans']:,}**
- Average credit score: **{credit['average_credit_score']:.0f}**

⚠️ **Recommendation:** Prioritize high-risk loans for manual credit review, affordability checks, and possible exposure reduction.
"""

    if any(word in q for word in ["fraud", "suspicious", "transaction"]):
        return f"""
### Fraud Risk Insight

- Transactions monitored: **{fraud['transactions']:,}**
- Fraud alerts: **{fraud['fraud_alerts']:,}**
- High-risk transactions: **{fraud['high_risk_transactions']:,}**
- Medium-risk transactions: **{fraud['medium_risk_transactions']:,}**
- High-risk exposure: **£{fraud['high_risk_value']:,.0f}**
- Average fraud score: **{fraud['average_fraud_score']:.1f}/100**

⚠️ **Recommendation:** Review high-value, cross-border, night-time, and international transfer transactions first.
"""

    if any(word in q for word in ["aml", "compliance", "money laundering", "kyc"]):
        return f"""
### AML & Compliance Insight

- AML alerts: **{aml['aml_alerts']:,}**
- AML exposure: **£{aml['aml_exposure']:,.0f}**
- High-value transactions: **{aml['high_value_transactions']:,}**
- Cross-border transactions: **{aml['cross_border_transactions']:,}**
- Average AML score: **{aml['average_aml_score']:.1f}/100**

⚠️ **Recommendation:** Prioritize high-value, cross-border, cash deposit, and enhanced due diligence country exposure cases.
"""

    if any(word in q for word in ["customer", "churn", "segment", "deposit"]):
        return f"""
### Customer Intelligence Insight

- Customers: **{customer['customers']:,}**
- Total deposits: **£{customer['total_deposits']:,.0f}**
- High-churn customers: **{customer['high_churn_customers']:,}**
- Average churn risk: **{customer['average_churn_risk']:.1f}/100**
- Average products per customer: **{customer['average_products']:.1f}**
- Average credit score: **{customer['average_credit_score']:.0f}**

✅ **Recommendation:** Prioritize high-value customers with high churn risk for retention and cross-sell campaigns.
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

🎯 **Top priorities:**
- Review high-risk loan accounts.
- Investigate suspicious high-value transactions.
- Escalate AML alerts with cross-border or cash deposit patterns.
- Launch retention campaigns for high-churn customers.
"""


# -----------------------------
# KPI SNAPSHOT
# -----------------------------
section_title("📌 Copilot Banking Snapshot")

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Customers", f"{kpis['total_customers']:,}", "Banking portfolio")

with c2:
    metric_card("Deposits", f"£{kpis['total_deposits']:,.0f}", "Positive balances")

with c3:
    metric_card("Loan Book", f"£{kpis['total_loan_book']:,.0f}", "Credit exposure")

with c4:
    metric_card("Fraud Alerts", f"{kpis['fraud_cases']:,}", "Suspicious activity")

c5, c6, c7, c8 = st.columns(4)

with c5:
    metric_card("AML Alerts", f"{kpis['aml_cases']:,}", "Compliance risk")

with c6:
    metric_card("Default Rate", f"{kpis['default_rate']:.2f}%", "Credit risk")

with c7:
    metric_card("Avg Credit Score", f"{kpis['avg_credit_score']:.0f}", "Credit quality")

with c8:
    metric_card("Transactions", f"{kpis['total_transactions']:,}", "Monitored activity")


# -----------------------------
# QUICK QUESTIONS
# -----------------------------
section_title("⚡ Quick Banking Questions")

questions = [
    "Give me an executive banking summary",
    "What are the biggest credit risks?",
    "Which fraud risks need attention?",
    "What AML alerts should compliance prioritize?",
    "Which customers are likely to churn?",
    "What actions should management take today?",
]

cols = st.columns(3)

for i, q in enumerate(questions):
    if cols[i % 3].button(q, use_container_width=True):
        st.session_state.copilot_prompt = q
        st.rerun()


# -----------------------------
# CHAT
# -----------------------------
section_title("💬 Ask FinGuard AI")

user_input = st.chat_input(
    "Ask about credit risk, fraud, AML, customers, deposits, transactions..."
)

if st.session_state.copilot_prompt:
    user_input = st.session_state.copilot_prompt
    st.session_state.copilot_prompt = None

if user_input:
    st.session_state.copilot_history.append(("user", user_input))

    response = answer_question(user_input)

    st.session_state.copilot_history.append(("assistant", response))


for role, message in st.session_state.copilot_history:
    with st.chat_message(role):
        st.markdown(message)


# -----------------------------
# MEMORY TABLE
# -----------------------------
section_title("🧠 Copilot Memory")

if st.session_state.copilot_history:
    memory_df = pd.DataFrame(
        st.session_state.copilot_history,
        columns=["role", "message"]
    )

    st.dataframe(memory_df.tail(10), use_container_width=True)

    if st.button("Clear Copilot Memory", use_container_width=True):
        st.session_state.copilot_history = []
        st.rerun()
else:
    insight_card("No copilot memory yet. Ask a question to begin.", level="risk")
