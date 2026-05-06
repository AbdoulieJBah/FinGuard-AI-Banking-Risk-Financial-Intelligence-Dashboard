import os
import joblib
import pandas as pd
import streamlit as st

from ui_utils import setup_page, premium_hero, metric_card, insight_card, section_title
from credit_model import predict_default_probability
from fraud_model import score_single_transaction
from ai_insights import explain_credit_prediction, explain_fraud_transaction


setup_page("Real-Time AI Predictions", icon="⚡")

premium_hero(
    "⚡ Real-Time AI Predictions",
    "Live banking AI inference for credit default risk, fraud anomaly scoring, and explainable financial decision support.",
    badge="Production AI Inference Layer"
)


MODEL_DIR = "models"
CREDIT_MODEL_PATH = os.path.join(MODEL_DIR, "credit_risk_model.pkl")
FRAUD_MODEL_PATH = os.path.join(MODEL_DIR, "fraud_anomaly_model.pkl")


@st.cache_resource
def load_credit_model():
    if not os.path.exists(CREDIT_MODEL_PATH):
        return None

    artifact = joblib.load(CREDIT_MODEL_PATH)
    return artifact


@st.cache_resource
def load_fraud_model():
    if not os.path.exists(FRAUD_MODEL_PATH):
        return None

    artifact = joblib.load(FRAUD_MODEL_PATH)
    return artifact


credit_artifact = load_credit_model()
fraud_artifact = load_fraud_model()

credit_model = credit_artifact["model"] if credit_artifact else None
credit_metrics = credit_artifact["metrics"] if credit_artifact else {}

fraud_model = fraud_artifact["model"] if fraud_artifact else None
fraud_metrics = fraud_artifact["metrics"] if fraud_artifact else {}


# -----------------------------
# MODEL STATUS
# -----------------------------
section_title("🧠 Model Status")

m1, m2, m3, m4 = st.columns(4)

with m1:
    metric_card(
        "Credit Model",
        credit_metrics.get("model_type", "Missing"),
        "Default prediction"
    )

with m2:
    metric_card(
        "Credit F1",
        credit_metrics.get("f1_score", "N/A"),
        "Model quality"
    )

with m3:
    metric_card(
        "Fraud Model",
        fraud_metrics.get("model_type", "Missing"),
        "Anomaly detection"
    )

with m4:
    metric_card(
        "Anomaly Rate",
        f"{fraud_metrics.get('anomaly_rate', 0)}%",
        "Fraud engine"
    )

if credit_model is None:
    insight_card(
        "⚠️ Credit model not found. Run `python train_models.py` locally and commit the generated model files.",
        level="risk"
    )

if fraud_model is None:
    insight_card(
        "⚠️ Fraud model not found. Run `python train_models.py` locally and commit the generated model files.",
        level="risk"
    )


# -----------------------------
# CREDIT RISK LIVE PREDICTION
# -----------------------------
section_title("🏦 Live Credit Risk Prediction")

with st.form("credit_prediction_form"):

    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input("Age", min_value=18, max_value=90, value=38)
        annual_income = st.number_input("Annual Income (£)", min_value=0.0, value=52000.0)
        account_balance = st.number_input("Account Balance (£)", value=8500.0)
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=650)

    with c2:
        years_with_bank = st.number_input("Years With Bank", min_value=0, max_value=40, value=5)
        num_products = st.number_input("Number of Products", min_value=1, max_value=10, value=3)
        loan_amount = st.number_input("Loan Amount (£)", min_value=0.0, value=45000.0)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, value=7.5)

    with c3:
        loan_term_months = st.number_input("Loan Term Months", min_value=1, max_value=120, value=60)
        monthly_payment = st.number_input("Monthly Payment (£)", min_value=0.0, value=750.0)
        employment_status = st.selectbox(
            "Employment Status",
            ["Employed", "Self-employed", "Unemployed", "Retired"]
        )

        debt_to_income = (
            (monthly_payment * 12) / annual_income
            if annual_income else 0
        )

        st.metric("Debt-to-Income", f"{debt_to_income:.2f}")

    run_credit = st.form_submit_button("Predict Credit Risk", use_container_width=True)


if run_credit:

    credit_row = {
        "age": age,
        "annual_income": annual_income,
        "account_balance": account_balance,
        "credit_score": credit_score,
        "years_with_bank": years_with_bank,
        "num_products": num_products,
        "debt_to_income": debt_to_income,
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "loan_term_months": loan_term_months,
        "monthly_payment": monthly_payment,
        "employment_status": employment_status,
    }

    probability = predict_default_probability(credit_model, credit_row)

    if probability >= 70:
        level = "critical"
        label = "High Risk"
    elif probability >= 40:
        level = "risk"
        label = "Medium Risk"
    else:
        level = "good"
        label = "Low Risk"

    r1, r2, r3 = st.columns(3)

    with r1:
        metric_card("Default Probability", f"{probability:.2f}%", "ML prediction")

    with r2:
        metric_card("Risk Level", label, "Credit decision")

    with r3:
        metric_card("Debt-to-Income", f"{debt_to_income:.2f}", "Affordability pressure")

    insight_card(
        explain_credit_prediction(credit_row, probability),
        level=level
    )


# -----------------------------
# FRAUD LIVE PREDICTION
# -----------------------------
section_title("🚨 Live Fraud Anomaly Scoring")

with st.form("fraud_prediction_form"):

    f1, f2, f3 = st.columns(3)

    with f1:
        amount = st.number_input("Transaction Amount (£)", min_value=0.0, value=9500.0)
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

    with f2:
        country = st.selectbox(
            "Country",
            ["UK", "Italy", "Germany", "France", "Spain", "Nigeria", "Gambia", "UAE", "USA"]
        )

        channel = st.selectbox(
            "Channel",
            ["Mobile", "Web", "Branch", "ATM", "POS"]
        )

    with f3:
        hour = st.slider("Transaction Hour", 0, 23, 2)

        is_high_value = amount > 7500
        is_cross_border = country != "UK"
        is_night_tx = hour <= 5

        st.metric("High Value", "Yes" if is_high_value else "No")
        st.metric("Cross Border", "Yes" if is_cross_border else "No")

    run_fraud = st.form_submit_button("Score Fraud Risk", use_container_width=True)


if run_fraud:

    fraud_row = {
        "amount": amount,
        "transaction_amount": amount,
        "hour": hour,
        "is_high_value": int(is_high_value),
        "is_cross_border": int(is_cross_border),
        "is_night_tx": int(is_night_tx),
        "transaction_type": transaction_type,
        "country": country,
        "channel": channel,
    }

    result = score_single_transaction(fraud_model, fraud_row)

    anomaly_score = result["anomaly_score"]
    anomaly_level = result["anomaly_level"]

    if anomaly_score >= 70:
        fraud_level = "critical"
    elif anomaly_score >= 40:
        fraud_level = "risk"
    else:
        fraud_level = "good"

    s1, s2, s3 = st.columns(3)

    with s1:
        metric_card("Anomaly Score", f"{anomaly_score:.2f}/100", "Isolation Forest")

    with s2:
        metric_card("Anomaly Level", anomaly_level, "Fraud signal")

    with s3:
        metric_card("Anomaly Flag", "Yes" if result["anomaly_flag"] else "No", "Investigation trigger")

    insight_card(
        explain_fraud_transaction(fraud_row),
        level=fraud_level
    )


# -----------------------------
# EXECUTIVE USAGE NOTES
# -----------------------------
section_title("🎯 How This Strengthens the Platform")

insight_card(
    """
<b>Production AI capability:</b><br>
This page shows that FinGuard AI can train models, save model artifacts, reload them, and perform live inference on new banking cases.
""",
    level="good"
)

insight_card(
    """
<b>Interview value:</b><br>
You can now explain the full AI lifecycle: data generation, preprocessing, model training, model persistence, deployment, inference, and explainability.
""",
    level="good"
)
