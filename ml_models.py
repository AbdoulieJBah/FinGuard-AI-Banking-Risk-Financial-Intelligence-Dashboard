from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score, precision_score, recall_score, f1_score


def train_credit_model(loans):
    features = [
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

    X = loans[features]
    y = loans["default_flag"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=8,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    metrics = {
        "balanced_accuracy": balanced_accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds, zero_division=0),
        "recall": recall_score(y_test, preds, zero_division=0),
        "f1_score": f1_score(y_test, preds, zero_division=0),
    }

    return model, features, metrics
