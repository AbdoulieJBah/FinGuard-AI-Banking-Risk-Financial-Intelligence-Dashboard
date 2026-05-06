import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import balanced_accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split


FEATURES = [
    "age",
    "annual_income",
    "account_balance",
    "credit_score",
    "years_with_bank",
    "num_products",
    "debt_to_income",
    "loan_amount",
    "interest_rate",
    "loan_term_months",
    "monthly_payment",
]


def train_credit_risk_model(loans):
    data = loans.copy()

    for col in FEATURES:
        if col not in data.columns:
            data[col] = 0

        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    if "default_flag" not in data.columns:
        data["default_flag"] = 0

    data["default_flag"] = pd.to_numeric(
        data["default_flag"],
        errors="coerce"
    ).fillna(0).astype(int)

    X = data[FEATURES]
    y = data["default_flag"]

    if y.nunique() < 2:
        return None, FEATURES, {
            "model_type": "Unavailable",
            "balanced_accuracy": 0,
            "precision": 0,
            "recall": 0,
            "f1_score": 0,
        }

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=9,
        min_samples_split=8,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    metrics = {
        "model_type": "Random Forest",
        "balanced_accuracy": round(balanced_accuracy_score(y_test, preds), 3),
        "precision": round(precision_score(y_test, preds, zero_division=0), 3),
        "recall": round(recall_score(y_test, preds, zero_division=0), 3),
        "f1_score": round(f1_score(y_test, preds, zero_division=0), 3),
    }

    return model, FEATURES, metrics


def predict_default_probability(model, row):
    if model is None:
        return 0

    input_df = pd.DataFrame([{
        col: pd.to_numeric(row.get(col, 0), errors="coerce")
        for col in FEATURES
    }]).fillna(0)

    probability = model.predict_proba(input_df)[0][1] * 100

    return round(probability, 2)


def get_credit_feature_importance(model):
    if model is None:
        return pd.DataFrame(columns=["feature", "importance"])

    importance_df = pd.DataFrame({
        "feature": FEATURES,
        "importance": model.feature_importances_
    })

    importance_df = importance_df.sort_values(
        "importance",
        ascending=False
    )

    return importance_df
