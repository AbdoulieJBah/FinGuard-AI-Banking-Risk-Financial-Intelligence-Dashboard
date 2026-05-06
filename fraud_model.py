import pandas as pd
from sklearn.ensemble import IsolationForest


FEATURES = [
    "amount",
    "transaction_amount",
    "hour",
    "is_high_value",
    "is_cross_border",
    "is_night_tx",
]


def train_fraud_anomaly_model(transactions):
    data = transactions.copy()

    for col in FEATURES:
        if col not in data.columns:
            data[col] = 0

    for col in FEATURES:
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    X = data[FEATURES]

    model = IsolationForest(
        n_estimators=300,
        contamination=0.06,
        random_state=42
    )

    model.fit(X)

    anomaly_scores = model.decision_function(X)
    anomaly_preds = model.predict(X)

    data["anomaly_flag"] = (anomaly_preds == -1).astype(int)
    data["anomaly_score"] = ((-anomaly_scores - (-anomaly_scores).min()) / ((-anomaly_scores).max() - (-anomaly_scores).min() + 1e-9) * 100).round(2)

    data["anomaly_level"] = data["anomaly_score"].apply(
        lambda x: "High" if x >= 70 else "Medium" if x >= 40 else "Low"
    )

    metrics = {
        "model_type": "Isolation Forest",
        "transactions_scored": len(data),
        "anomalies_detected": int(data["anomaly_flag"].sum()),
        "anomaly_rate": round(data["anomaly_flag"].mean() * 100, 2),
    }

    return model, data, metrics


def score_single_transaction(model, row):
    if model is None:
        return {
            "anomaly_flag": 0,
            "anomaly_score": 0,
            "anomaly_level": "Unavailable",
        }

    input_df = pd.DataFrame([{
        col: pd.to_numeric(row.get(col, 0), errors="coerce")
        for col in FEATURES
    }]).fillna(0)

    pred = model.predict(input_df)[0]
    raw_score = model.decision_function(input_df)[0]

    anomaly_score = max(0, min(100, round((-raw_score + 0.2) * 250, 2)))

    return {
        "anomaly_flag": int(pred == -1),
        "anomaly_score": anomaly_score,
        "anomaly_level": "High" if anomaly_score >= 70 else "Medium" if anomaly_score >= 40 else "Low",
    }
