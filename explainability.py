import pandas as pd


def credit_reason_codes(row):
    reasons = []

    credit_score = float(row.get("credit_score", 0))
    debt_to_income = float(row.get("debt_to_income", 0))
    account_balance = float(row.get("account_balance", 0))
    annual_income = float(row.get("annual_income", 0))
    loan_amount = float(row.get("loan_amount", 0))
    employment_status = str(row.get("employment_status", ""))

    if credit_score < 580:
        reasons.append({
            "factor": "Credit Score",
            "impact": "High Negative",
            "reason": "Credit score is below preferred lending threshold."
        })

    if debt_to_income > 0.45:
        reasons.append({
            "factor": "Debt-to-Income",
            "impact": "High Negative",
            "reason": "Borrower has elevated affordability pressure."
        })

    if account_balance < 500:
        reasons.append({
            "factor": "Account Balance",
            "impact": "Medium Negative",
            "reason": "Low balance may indicate weak liquidity buffer."
        })

    if annual_income > 0 and loan_amount > annual_income:
        reasons.append({
            "factor": "Loan Amount",
            "impact": "Medium Negative",
            "reason": "Loan amount is high relative to annual income."
        })

    if employment_status == "Unemployed":
        reasons.append({
            "factor": "Employment Status",
            "impact": "High Negative",
            "reason": "Unemployment increases repayment uncertainty."
        })

    if not reasons:
        reasons.append({
            "factor": "Portfolio Profile",
            "impact": "Low",
            "reason": "No major negative credit driver detected."
        })

    return pd.DataFrame(reasons)


def fraud_reason_codes(row):
    reasons = []

    amount = float(row.get("amount", 0))
    country = str(row.get("country", "UK"))
    hour = int(row.get("hour", 12))
    transaction_type = str(row.get("transaction_type", ""))

    if amount > 7500:
        reasons.append({
            "factor": "Transaction Amount",
            "impact": "High Negative",
            "reason": "Transaction is high value compared with standard monitoring threshold."
        })

    if country != "UK":
        reasons.append({
            "factor": "Country",
            "impact": "Medium Negative",
            "reason": "Transaction is cross-border and may require additional monitoring."
        })

    if 0 <= hour <= 5:
        reasons.append({
            "factor": "Transaction Time",
            "impact": "Medium Negative",
            "reason": "Transaction occurred during night-time risk window."
        })

    if transaction_type == "International Transfer":
        reasons.append({
            "factor": "Transaction Type",
            "impact": "High Negative",
            "reason": "International transfers carry elevated fraud and AML monitoring risk."
        })

    if not reasons:
        reasons.append({
            "factor": "Transaction Pattern",
            "impact": "Low",
            "reason": "No major fraud driver detected."
        })

    return pd.DataFrame(reasons)


def aml_reason_codes(row):
    reasons = []

    amount = float(row.get("amount", 0))
    country = str(row.get("country", "UK"))
    transaction_type = str(row.get("transaction_type", ""))

    if amount > 10000:
        reasons.append({
            "factor": "High-Value Transaction",
            "impact": "High Negative",
            "reason": "Transaction exceeds high-value compliance monitoring threshold."
        })

    if country != "UK":
        reasons.append({
            "factor": "Cross-Border Activity",
            "impact": "Medium Negative",
            "reason": "Cross-border transaction may require enhanced monitoring."
        })

    if country in ["Nigeria", "Gambia", "UAE"]:
        reasons.append({
            "factor": "EDD Country Exposure",
            "impact": "High Negative",
            "reason": "Country exposure may trigger enhanced due diligence review."
        })

    if transaction_type == "Cash Deposit":
        reasons.append({
            "factor": "Cash Deposit",
            "impact": "Medium Negative",
            "reason": "Cash deposit activity can require source-of-funds review."
        })

    if transaction_type == "International Transfer":
        reasons.append({
            "factor": "International Transfer",
            "impact": "Medium Negative",
            "reason": "International transfer requires compliance pattern monitoring."
        })

    if not reasons:
        reasons.append({
            "factor": "AML Pattern",
            "impact": "Low",
            "reason": "No major AML reason code detected."
        })

    return pd.DataFrame(reasons)
