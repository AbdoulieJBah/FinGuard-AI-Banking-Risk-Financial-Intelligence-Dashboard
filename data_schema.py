import pandas as pd


def ensure_columns(df, defaults):
    df = df.copy()

    for col, default_value in defaults.items():
        if col not in df.columns:
            df[col] = default_value

    return df


def ensure_numeric(df, cols):
    df = df.copy()

    for col in cols:
        if col not in df.columns:
            df[col] = 0

        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def ensure_datetime(df, cols):
    df = df.copy()

    for col in cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def prepare_customers(customers):
    customers = customers.copy()
    customers.columns = customers.columns.str.strip().str.lower()

    defaults = {
        "customer_id": "UNKNOWN",
        "customer_name": "Unknown Customer",
        "branch": "Unknown Branch",
        "segment": "Retail",
        "customer_segment": "Retail",
        "age": 0,
        "annual_income": 0,
        "account_balance": 0,
        "credit_score": 0,
        "years_with_bank": 0,
        "num_products": 0,
        "churn_risk": 0,
        "churn_risk_score": 0,
    }

    customers = ensure_columns(customers, defaults)

    numeric_cols = [
        "age",
        "annual_income",
        "account_balance",
        "credit_score",
        "years_with_bank",
        "num_products",
        "churn_risk",
        "churn_risk_score",
    ]

    customers = ensure_numeric(customers, numeric_cols)

    if customers["churn_risk"].sum() == 0 and customers["churn_risk_score"].sum() > 0:
        customers["churn_risk"] = customers["churn_risk_score"]

    if customers["churn_risk_score"].sum() == 0 and customers["churn_risk"].sum() > 0:
        customers["churn_risk_score"] = customers["churn_risk"]

    if "customer_segment" in customers.columns and customers["customer_segment"].nunique() > 1:
        customers["segment"] = customers["customer_segment"]

    customers["churn_level"] = customers["churn_risk"].apply(
        lambda x: "High" if x >= 70 else "Medium" if x >= 40 else "Low"
    )

    customers["customer_value_score"] = (
        customers["account_balance"].clip(lower=0) * 0.0004
        + customers["annual_income"] * 0.0002
        + customers["num_products"] * 8
        + customers["years_with_bank"] * 2
    ).clip(0, 100)

    return customers


def prepare_loans(loans):
    loans = loans.copy()
    loans.columns = loans.columns.str.strip().str.lower()

    defaults = {
        "loan_id": "UNKNOWN",
        "customer_id": "UNKNOWN",
        "customer_name": "Unknown Customer",
        "branch": "Unknown Branch",
        "segment": "Retail",
        "employment_status": "Unknown",
        "age": 0,
        "annual_income": 0,
        "account_balance": 0,
        "credit_score": 0,
        "years_with_bank": 0,
        "num_products": 0,
        "debt_to_income": 0,
        "loan_amount": 0,
        "interest_rate": 0,
        "loan_term_months": 0,
        "monthly_payment": 0,
        "default_flag": 0,
        "default_probability": 0,
    }

    loans = ensure_columns(loans, defaults)

    numeric_cols = [
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
        "default_flag",
        "default_probability",
    ]

    loans = ensure_numeric(loans, numeric_cols)

    loans["default_flag"] = loans["default_flag"].astype(int)

    loans["default_risk_level"] = loans["default_probability"].apply(
        lambda x: "High" if x >= 70 else "Medium" if x >= 40 else "Low"
    )

    return loans


def prepare_transactions(transactions):
    transactions = transactions.copy()
    transactions.columns = transactions.columns.str.strip().str.lower()

    defaults = {
        "transaction_id": "UNKNOWN",
        "customer_id": "UNKNOWN",
        "customer_name": "Unknown Customer",
        "branch": "Unknown Branch",
        "segment": "Retail",
        "transaction_type": "Unknown",
        "transaction_amount": 0,
        "amount": 0,
        "country": "UK",
        "channel": "Mobile",
        "hour": 12,
        "fraud_flag": 0,
        "fraud_risk_score": 0,
        "aml_flag": 0,
        "aml_risk_score": 0,
        "is_high_value": False,
        "is_cross_border": False,
        "is_night_tx": False,
    }

    transactions = ensure_columns(transactions, defaults)

    numeric_cols = [
        "transaction_amount",
        "amount",
        "hour",
        "fraud_flag",
        "fraud_risk_score",
        "aml_flag",
        "aml_risk_score",
    ]

    transactions = ensure_numeric(transactions, numeric_cols)

    if transactions["amount"].sum() == 0 and transactions["transaction_amount"].sum() > 0:
        transactions["amount"] = transactions["transaction_amount"]

    if transactions["transaction_amount"].sum() == 0 and transactions["amount"].sum() > 0:
        transactions["transaction_amount"] = transactions["amount"]

    transactions["fraud_flag"] = transactions["fraud_flag"].astype(int)
    transactions["aml_flag"] = transactions["aml_flag"].astype(int)

    transactions["is_high_value"] = transactions["amount"] > 7500
    transactions["is_cross_border"] = transactions["country"].astype(str).str.upper() != "UK"
    transactions["is_night_tx"] = transactions["hour"].between(0, 5)

    transactions["fraud_risk_level"] = transactions["fraud_risk_score"].apply(
        lambda x: "High" if x >= 70 else "Medium" if x >= 40 else "Low"
    )

    transactions["aml_risk_level"] = transactions["aml_risk_score"].apply(
        lambda x: "High" if x >= 65 else "Medium" if x >= 40 else "Low"
    )

    return transactions


def prepare_all(customers, loans, transactions):
    customers = prepare_customers(customers)
    loans = prepare_loans(loans)
    transactions = prepare_transactions(transactions)

    return customers, loans, transactions
