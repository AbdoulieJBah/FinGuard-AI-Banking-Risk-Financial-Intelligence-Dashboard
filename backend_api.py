import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from credit_model import predict_default_probability
from fraud_model import score_single_transaction
from ai_insights import explain_credit_prediction, explain_fraud_transaction


app = FastAPI(
    title="FinGuard AI Backend API",
    description="Production API for banking credit risk and fraud anomaly inference.",
    version="1.0.0"
)

MODEL_DIR = "models"
CREDIT_MODEL_PATH = os.path.join(MODEL_DIR, "credit_risk_model.pkl")
FRAUD_MODEL_PATH = os.path.join(MODEL_DIR, "fraud_anomaly_model.pkl")


def load_model(path):
    if not os.path.exists(path):
        return None
    return joblib.load(path)


credit_artifact = load_model(CREDIT_MODEL_PATH)
fraud_artifact = load_model(FRAUD_MODEL_PATH)

credit_model = credit_artifact["model"] if credit_artifact else None
fraud_model = fraud_artifact["model"] if fraud_artifact else None


class CreditInput(BaseModel):
    age: int
    annual_income: float
    account_balance: float
    credit_score: int
    years_with_bank: int
    num_products: int
    debt_to_income: float
    loan_amount: float
    interest_rate: float
    loan_term_months: int
    monthly_payment: float
    employment_status: str = "Employed"


class FraudInput(BaseModel):
    amount: float
    transaction_amount: float
    hour: int
    is_high_value: int
    is_cross_border: int
    is_night_tx: int
    transaction_type: str = "Card Payment"
    country: str = "UK"
    channel: str = "Mobile"


@app.get("/")
def home():
    return {
        "message": "FinGuard AI Backend API is running",
        "endpoints": [
            "/credit-risk",
            "/fraud-risk",
            "/health"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "credit_model_loaded": credit_model is not None,
        "fraud_model_loaded": fraud_model is not None,
    }


@app.post("/credit-risk")
def credit_risk(data: CreditInput):
    row = data.dict()

    probability = predict_default_probability(
        credit_model,
        row
    )

    risk_level = (
        "High" if probability >= 70
        else "Medium" if probability >= 40
        else "Low"
    )

    explanation = explain_credit_prediction(row, probability)

    return {
        "default_probability": probability,
        "risk_level": risk_level,
        "explanation": explanation,
        "decision": (
            "Escalate for manual credit review"
            if risk_level == "High"
            else "Review affordability and pricing"
            if risk_level == "Medium"
            else "Acceptable risk range"
        )
    }


@app.post("/fraud-risk")
def fraud_risk(data: FraudInput):
    row = data.dict()

    result = score_single_transaction(
        fraud_model,
        row
    )

    explanation = explain_fraud_transaction(row)

    return {
        "anomaly_score": result["anomaly_score"],
        "anomaly_level": result["anomaly_level"],
        "anomaly_flag": result["anomaly_flag"],
        "explanation": explanation,
        "decision": (
            "Hold or block transaction for investigation"
            if result["anomaly_level"] == "High"
            else "Allow with enhanced monitoring"
            if result["anomaly_level"] == "Medium"
            else "Allow transaction"
        )
    }
