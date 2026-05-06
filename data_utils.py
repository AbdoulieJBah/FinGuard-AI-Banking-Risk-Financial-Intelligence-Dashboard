import numpy as np
import pandas as pd


def generate_banking_data(n_customers=1200, n_transactions=8000, seed=42):
    np.random.seed(seed)

    customer_ids = [f"CUST-{i:05d}" for i in range(1, n_customers + 1)]

    branches = [
        "London Central", "Manchester", "Birmingham", "Leeds",
        "Bristol", "Edinburgh", "Cardiff", "Liverpool"
    ]

    segments = ["Retail", "SME", "Corporate", "Private Banking"]
    employment_statuses = ["Employed", "Self-Employed", "Unemployed", "Student", "Retired"]

    customers = pd.DataFrame({
        "customer_id": customer_ids,
        "age": np.random.randint(18, 75, n_customers),
        "branch": np.random.choice(branches, n_customers),
        "segment": np.random.choice(segments, n_customers, p=[0.62, 0.22, 0.10, 0.06]),
        "employment_status": np.random.choice(employment_statuses, n_customers, p=[0.55, 0.20, 0.08, 0.07, 0.10]),
        "annual_income": np.random.normal(52000, 22000, n_customers).clip(9000, 250000),
        "account_balance": np.random.normal(9000, 18000, n_customers).clip(-4000, 250000),
        "credit_score": np.random.normal(660, 95, n_customers).clip(300, 850),
        "years_with_bank": np.random.randint(0, 22, n_customers),
        "num_products": np.random.randint(1, 7, n_customers),
    })

    customers["debt_to_income"] = np.random.beta(2.2, 5.5, n_customers).clip(0.02, 0.95)
    customers["churn_risk"] = (
        (customers["years_with_bank"] < 2).astype(int) * 25
        + (customers["num_products"] <= 2).astype(int) * 20
        + (customers["account_balance"] < 500).astype(int) * 20
        + np.random.randint(0, 25, n_customers)
    ).clip(0, 100)

    # Loans
    loan_probability = np.random.rand(n_customers)
    loans = customers[loan_probability < 0.55].copy()

    loans["loan_id"] = [f"LOAN-{i:05d}" for i in range(1, len(loans) + 1)]
    loans["loan_amount"] = np.random.normal(42000, 28000, len(loans)).clip(3000, 250000)
    loans["interest_rate"] = np.random.normal(7.2, 2.3, len(loans)).clip(2.5, 18)
    loans["loan_term_months"] = np.random.choice([12, 24, 36, 48, 60, 72, 84], len(loans))
    loans["monthly_payment"] = (
        loans["loan_amount"] * (1 + loans["interest_rate"] / 100)
        / loans["loan_term_months"]
    )

    default_score = (
        (850 - loans["credit_score"]) * 0.10
        + loans["debt_to_income"] * 45
        + (loans["employment_status"].isin(["Unemployed", "Student"])).astype(int) * 25
        + (loans["account_balance"] < 1000).astype(int) * 15
        + np.random.normal(0, 10, len(loans))
    )

    loans["default_probability"] = default_score.clip(1, 98)
    loans["default_flag"] = (loans["default_probability"] > 58).astype(int)

    # Transactions
    tx_customer_ids = np.random.choice(customer_ids, n_transactions)

    transaction_types = [
        "Card Payment", "ATM Withdrawal", "Bank Transfer",
        "Online Purchase", "Cash Deposit", "International Transfer"
    ]

    countries = ["UK", "Italy", "Germany", "France", "Spain", "Nigeria", "Gambia", "UAE", "USA"]

    transactions = pd.DataFrame({
        "transaction_id": [f"TX-{i:07d}" for i in range(1, n_transactions + 1)],
        "customer_id": tx_customer_ids,
        "transaction_type": np.random.choice(transaction_types, n_transactions),
        "amount": np.random.lognormal(mean=4.6, sigma=1.1, size=n_transactions).clip(2, 50000),
        "country": np.random.choice(countries, n_transactions, p=[0.68, 0.06, 0.05, 0.05, 0.04, 0.03, 0.03, 0.03, 0.03]),
        "channel": np.random.choice(["Mobile", "Web", "Branch", "ATM", "POS"], n_transactions),
        "hour": np.random.randint(0, 24, n_transactions),
    })

    transactions["date"] = pd.date_range(
        end=pd.Timestamp.today(),
        periods=n_transactions,
        freq="h"
    )

    transactions = transactions.merge(
        customers[["customer_id", "branch", "segment", "credit_score"]],
        on="customer_id",
        how="left"
    )

    transactions["is_high_value"] = transactions["amount"] > 7500
    transactions["is_night_tx"] = transactions["hour"].between(0, 5)
    transactions["is_cross_border"] = transactions["country"] != "UK"

    fraud_score = (
        transactions["is_high_value"].astype(int) * 35
        + transactions["is_night_tx"].astype(int) * 18
        + transactions["is_cross_border"].astype(int) * 20
        + (transactions["transaction_type"] == "International Transfer").astype(int) * 22
        + np.random.randint(0, 25, n_transactions)
    )

    transactions["fraud_risk_score"] = fraud_score.clip(0, 100)
    transactions["fraud_flag"] = (transactions["fraud_risk_score"] >= 70).astype(int)

    # AML risk
    transactions["aml_risk_score"] = (
        (transactions["amount"] > 10000).astype(int) * 30
        + transactions["is_cross_border"].astype(int) * 25
        + (transactions["country"].isin(["Nigeria", "Gambia", "UAE"])).astype(int) * 18
        + (transactions["transaction_type"] == "Cash Deposit").astype(int) * 15
        + np.random.randint(0, 20, n_transactions)
    ).clip(0, 100)

    transactions["aml_flag"] = (transactions["aml_risk_score"] >= 65).astype(int)

    return customers, loans, transactions


def load_data():
    return generate_banking_data()


def calculate_executive_kpis(customers, loans, transactions):
    total_deposits = customers["account_balance"].clip(lower=0).sum()
    total_loan_book = loans["loan_amount"].sum()
    total_transactions = len(transactions)
    fraud_cases = int(transactions["fraud_flag"].sum())
    aml_cases = int(transactions["aml_flag"].sum())
    default_rate = loans["default_flag"].mean() * 100 if len(loans) else 0

    return {
        "total_customers": len(customers),
        "total_deposits": total_deposits,
        "total_loan_book": total_loan_book,
        "total_transactions": total_transactions,
        "fraud_cases": fraud_cases,
        "aml_cases": aml_cases,
        "default_rate": default_rate,
        "avg_credit_score": customers["credit_score"].mean(),
    }
