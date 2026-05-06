import random
from datetime import datetime

import pandas as pd


EVENT_TYPES = [
    "Credit Risk Spike",
    "Fraud Alert",
    "AML Alert",
    "Customer Churn Signal",
    "High-Value Transaction",
    "Cross-Border Transaction",
]


def risk_level(score):
    if score >= 80:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


def generate_stream_event(customers, loans, transactions):
    event_type = random.choice(EVENT_TYPES)

    customer = customers.sample(1).iloc[0] if customers is not None and not customers.empty else {}
    loan = loans.sample(1).iloc[0] if loans is not None and not loans.empty else {}
    tx = transactions.sample(1).iloc[0] if transactions is not None and not transactions.empty else {}

    if event_type == "Credit Risk Spike":
        score = float(loan.get("default_probability", random.randint(40, 95)))
        message = "Loan account shows elevated default probability."
        action = "Route customer to credit review queue."

    elif event_type == "Fraud Alert":
        score = float(tx.get("fraud_risk_score", random.randint(40, 95)))
        message = "Suspicious transaction pattern detected."
        action = "Hold transaction and review customer activity."

    elif event_type == "AML Alert":
        score = float(tx.get("aml_risk_score", random.randint(40, 95)))
        message = "AML monitoring rule triggered."
        action = "Escalate for compliance and KYC review."

    elif event_type == "Customer Churn Signal":
        score = float(customer.get("churn_risk", random.randint(40, 95)))
        message = "Customer relationship shows retention risk."
        action = "Assign relationship manager for retention intervention."

    elif event_type == "High-Value Transaction":
        score = min(100, float(tx.get("amount", random.randint(5000, 25000))) / 250)
        message = "High-value transaction detected."
        action = "Monitor transaction and verify customer profile."

    else:
        score = 75 if bool(tx.get("is_cross_border", True)) else random.randint(30, 70)
        message = "Cross-border transaction activity detected."
        action = "Review country risk and transaction context."

    customer_id = (
        customer.get("customer_id", None)
        or loan.get("customer_id", None)
        or tx.get("customer_id", "UNKNOWN")
    )

    customer_name = (
        customer.get("customer_name", None)
        or loan.get("customer_name", None)
        or tx.get("customer_name", "Unknown Customer")
    )

    branch = (
        customer.get("branch", None)
        or loan.get("branch", None)
        or tx.get("branch", "Unknown Branch")
    )

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "customer_id": customer_id,
        "customer_name": customer_name,
        "branch": branch,
        "risk_score": round(score, 2),
        "risk_level": risk_level(score),
        "message": message,
        "recommended_action": action,
    }


def generate_stream_batch(customers, loans, transactions, n=5):
    events = [
        generate_stream_event(customers, loans, transactions)
        for _ in range(n)
    ]

    return pd.DataFrame(events)


def summarize_stream(events_df):
    if events_df is None or events_df.empty:
        return {
            "events": 0,
            "critical": 0,
            "high": 0,
            "top_event": "None",
            "top_branch": "None",
        }

    return {
        "events": len(events_df),
        "critical": int((events_df["risk_level"] == "Critical").sum()),
        "high": int((events_df["risk_level"] == "High").sum()),
        "top_event": events_df["event_type"].value_counts().index[0],
        "top_branch": events_df["branch"].value_counts().index[0],
    }
