import numpy as np
import pandas as pd

from data_schema import prepare_all


# -----------------------------
# SAMPLE DATA GENERATOR
# -----------------------------
def generate_sample_data(n_customers=1200, n_loans=900, n_transactions=5000):
    np.random.seed(42)

    branches = [
        "London Central",
        "Manchester",
        "Birmingham",
        "Leeds",
        "Liverpool",
        "Bristol",
        "Edinburgh",
        "Glasgow",
    ]

    segments = [
        "Retail",
        "SME",
        "Corporate",
        "Private Banking",
    ]

    countries = [
        "UK",
        "Italy",
        "Germany",
        "France",
        "Spain",
        "Nigeria",
        "Gambia",
        "UAE",
        "USA",
    ]

    channels = [
        "Mobile",
        "Web",
        "Branch",
        "ATM",
        "POS",
    ]

    transaction_types = [
        "Card Payment",
        "ATM Withdrawal",
        "Bank Transfer",
        "Online Purchase",
        "Cash Deposit",
        "International Transfer",
    ]

    # -----------------------------
    # CUSTOMERS
    # -----------------------------
    customer_ids = [f"CUST-{i:05d}" for i in range(1, n_customers + 1)]

    customers = pd.DataFrame({
        "customer_id": customer_ids,
        "customer_name": [f"Customer {i}" for i in range(1, n_customers + 1)],
        "branch": np.random.choice(branches, n_customers),
        "segment": np.random.choice(
            segments,
            n_customers,
            p=[0.58, 0.22, 0.13, 0.07]
        ),
        "age": np.random.randint(18, 75, n_customers),
        "annual_income": np.random.normal(52000, 22000, n_customers).clip(12000, 250000),
        "account_balance": np.random.normal(8500, 14000, n_customers).clip(-2000, 180000),
        "credit_score": np.random.normal(650, 85, n_customers).clip(300, 850),
        "years_with_bank": np.random.randint(1, 25, n_customers),
        "num_products": np.random.randint(1, 7, n_customers),
    })

    customers["churn_risk"] = (
        70
        - customers["num_products"] * 7
        - customers["years_with_bank"] * 1.2
        + np.where(customers["account_balance"] < 1000, 15, 0)
        + np.random.normal(0, 12, n_customers)
    ).clip(0, 100)

    customers["churn_risk_score"] = customers["churn_risk"]

    # -----------------------------
    # LOANS
    # -----------------------------
    loan_customer_ids = np.random.choice(customer_ids, n_loans)

    loan_base = customers.set_index("customer_id").loc[loan_customer_ids].reset_index()

    loans = pd.DataFrame({
        "loan_id": [f"LOAN-{i:05d}" for i in range(1, n_loans + 1)],
        "customer_id": loan_customer_ids,
        "customer_name": loan_base["customer_name"],
        "branch": loan_base["branch"],
        "segment": loan_base["segment"],
        "age": loan_base["age"],
        "annual_income": loan_base["annual_income"],
        "account_balance": loan_base["account_balance"],
        "credit_score": loan_base["credit_score"],
        "years_with_bank": loan_base["years_with_bank"],
        "num_products": loan_base["num_products"],
        "employment_status": np.random.choice(
            ["Employed", "Self-employed", "Unemployed", "Retired"],
            n_loans,
            p=[0.66, 0.18, 0.08, 0.08]
        ),
        "loan_amount": np.random.normal(45000, 28000, n_loans).clip(3000, 250000),
        "interest_rate": np.random.normal(7.5, 2.5, n_loans).clip(2.5, 18),
        "loan_term_months": np.random.choice([12, 24, 36, 48, 60, 72, 84], n_loans),
    })

    loans["monthly_payment"] = loans["loan_amount"] / loans["loan_term_months"]

    loans["debt_to_income"] = (
        (loans["monthly_payment"] * 12) / loans["annual_income"]
    ).replace([np.inf, -np.inf], 0).fillna(0).clip(0, 1.5)

    loans["default_probability"] = (
        25
        + loans["debt_to_income"] * 45
        + np.where(loans["credit_score"] < 580, 25, 0)
        + np.where(loans["employment_status"] == "Unemployed", 20, 0)
        + np.where(loans["account_balance"] < 500, 10, 0)
        + np.random.normal(0, 10, n_loans)
    ).clip(0, 100)

    loans["default_flag"] = (loans["default_probability"] >= 70).astype(int)

    # -----------------------------
    # TRANSACTIONS
    # -----------------------------
    tx_customer_ids = np.random.choice(customer_ids, n_transactions)

    tx_base = customers.set_index("customer_id").loc[tx_customer_ids].reset_index()

    transactions = pd.DataFrame({
        "transaction_id": [f"TX-{i:06d}" for i in range(1, n_transactions + 1)],
        "customer_id": tx_customer_ids,
        "customer_name": tx_base["customer_name"],
        "branch": tx_base["branch"],
        "segment": tx_base["segment"],
        "transaction_type": np.random.choice(
            transaction_types,
            n_transactions,
            p=[0.30, 0.13, 0.20, 0.18, 0.09, 0.10]
        ),
        "amount": np.random.lognormal(mean=7.0, sigma=1.1, size=n_transactions).clip(5, 75000),
        "country": np.random.choice(
            countries,
            n_transactions,
            p=[0.68, 0.06, 0.05, 0.05, 0.04, 0.035, 0.025, 0.03, 0.04]
        ),
        "channel": np.random.choice(channels, n_transactions),
        "hour": np.random.randint(0, 24, n_transactions),
    })

    transactions["transaction_amount"] = transactions["amount"]

    transactions["is_high_value"] = transactions["amount"] > 7500
    transactions["is_cross_border"] = transactions["country"] != "UK"
    transactions["is_night_tx"] = transactions["hour"].between(0, 5)

    transactions["fraud_risk_score"] = (
        10
        + transactions["is_high_value"].astype(int) * 35
        + transactions["is_cross_border"].astype(int) * 20
        + transactions["is_night_tx"].astype(int) * 18
        + np.where(transactions["transaction_type"] == "International Transfer", 22, 0)
        + np.random.normal(0, 8, n_transactions)
    ).clip(0, 100)

    transactions["fraud_flag"] = (transactions["fraud_risk_score"] >= 70).astype(int)

    transactions["aml_risk_score"] = (
        8
        + (transactions["amount"] > 10000).astype(int) * 30
        + transactions["is_cross_border"].astype(int) * 25
        + transactions["country"].isin(["Nigeria", "Gambia", "UAE"]).astype(int) * 18
        + np.where(transactions["transaction_type"] == "Cash Deposit", 15, 0)
        + np.where(transactions["transaction_type"] == "International Transfer", 12, 0)
        + np.random.normal(0, 7, n_transactions)
    ).clip(0, 100)

    transactions["aml_flag"] = (transactions["aml_risk_score"] >= 65).astype(int)

    return prepare_all(customers, loans, transactions)


# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    try:
        customers = pd.read_csv("data/customers.csv")
        loans = pd.read_csv("data/loans.csv")
        transactions = pd.read_csv("data/transactions.csv")
        return prepare_all(customers, loans, transactions)

    except Exception:
        return generate_sample_data()


# -----------------------------
# EXECUTIVE KPIS
# -----------------------------
def calculate_executive_kpis(customers, loans, transactions):
    customers, loans, transactions = prepare_all(customers, loans, transactions)

    total_customers = len(customers)
    total_deposits = customers["account_balance"].clip(lower=0).sum()
    total_loan_book = loans["loan_amount"].sum()
    total_transactions = len(transactions)

    default_rate = loans["default_flag"].mean() * 100 if len(loans) else 0
    fraud_cases = int(transactions["fraud_flag"].sum())
    aml_cases = int(transactions["aml_flag"].sum())

    avg_credit_score = customers["credit_score"].mean() if len(customers) else 0
    avg_churn_risk = customers["churn_risk"].mean() if len(customers) else 0

    return {
        "total_customers": total_customers,
        "total_deposits": total_deposits,
        "total_loan_book": total_loan_book,
        "total_transactions": total_transactions,
        "default_rate": default_rate,
        "fraud_cases": fraud_cases,
        "aml_cases": aml_cases,
        "avg_credit_score": avg_credit_score,
        "avg_churn_risk": avg_churn_risk,
    }


# -----------------------------
# PAGE-SPECIFIC SUMMARIES
# -----------------------------
def calculate_credit_kpis(loans):
    loans = loans.copy()

    high_risk = loans[loans["default_probability"] >= 70]
    medium_risk = loans[
        (loans["default_probability"] >= 40) &
        (loans["default_probability"] < 70)
    ]

    return {
        "loan_accounts": len(loans),
        "loan_book": loans["loan_amount"].sum(),
        "high_risk_loans": len(high_risk),
        "medium_risk_loans": len(medium_risk),
        "avg_default_probability": loans["default_probability"].mean(),
        "avg_credit_score": loans["credit_score"].mean(),
        "default_cases": int(loans["default_flag"].sum()),
    }


def calculate_fraud_kpis(transactions):
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
        "high_risk_value": high_risk["amount"].sum(),
        "avg_fraud_score": transactions["fraud_risk_score"].mean(),
    }


def calculate_aml_kpis(transactions):
    aml_alerts = transactions[transactions["aml_flag"] == 1]
    high_value = transactions[transactions["amount"] > 10000]
    cross_border = transactions[transactions["is_cross_border"] == True]

    return {
        "aml_alerts": len(aml_alerts),
        "aml_exposure": aml_alerts["amount"].sum(),
        "high_value_transactions": len(high_value),
        "cross_border_transactions": len(cross_border),
        "avg_aml_score": transactions["aml_risk_score"].mean(),
        "total_transaction_value": transactions["amount"].sum(),
    }


def calculate_customer_kpis(customers):
    high_churn = customers[customers["churn_risk"] >= 70]
    premium_customers = customers[customers["segment"] == "Private Banking"]

    return {
        "customers": len(customers),
        "high_churn_customers": len(high_churn),
        "premium_customers": len(premium_customers),
        "avg_products": customers["num_products"].mean(),
        "total_deposits": customers["account_balance"].clip(lower=0).sum(),
        "avg_income": customers["annual_income"].mean(),
        "avg_credit_score": customers["credit_score"].mean(),
        "avg_churn_risk": customers["churn_risk"].mean(),
    }
