import os
import joblib

from data_utils import load_data
from credit_model import train_credit_risk_model
from fraud_model import train_fraud_anomaly_model


MODEL_DIR = "models"


def ensure_model_dir():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)


def train_and_save_models():
    ensure_model_dir()

    customers, loans, transactions = load_data()

    credit_model, credit_features, credit_metrics = train_credit_risk_model(loans)

    if credit_model is not None:
        joblib.dump(
            {
                "model": credit_model,
                "features": credit_features,
                "metrics": credit_metrics,
            },
            os.path.join(MODEL_DIR, "credit_risk_model.pkl")
        )

    fraud_model, scored_transactions, fraud_metrics = train_fraud_anomaly_model(transactions)

    if fraud_model is not None:
        joblib.dump(
            {
                "model": fraud_model,
                "features": [
                    "amount",
                    "transaction_amount",
                    "hour",
                    "is_high_value",
                    "is_cross_border",
                    "is_night_tx",
                ],
                "metrics": fraud_metrics,
            },
            os.path.join(MODEL_DIR, "fraud_anomaly_model.pkl")
        )

    print("✅ Models trained and saved successfully")
    print("Credit metrics:", credit_metrics)
    print("Fraud metrics:", fraud_metrics)


if __name__ == "__main__":
    train_and_save_models()
