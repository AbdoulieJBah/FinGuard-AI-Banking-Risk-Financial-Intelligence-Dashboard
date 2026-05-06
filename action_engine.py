import pandas as pd


def priority_level(score):
    if score >= 80:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


def build_credit_actions(loans):
    actions = []

    if loans is None or loans.empty:
        return actions

    data = loans.copy()

    for col in ["default_probability", "loan_amount", "credit_score", "debt_to_income"]:
        if col not in data.columns:
            data[col] = 0

        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    high_risk = data[data["default_probability"] >= 70]

    for _, row in high_risk.iterrows():
        priority = min(
            100,
            row["default_probability"] * 0.65
            + min(row["loan_amount"] / 5000, 25)
            + max(0, (600 - row["credit_score"]) / 10)
        )

        actions.append({
            "customer_id": row.get("customer_id", "UNKNOWN"),
            "customer_name": row.get("customer_name", "Unknown Customer"),
            "branch": row.get("branch", "Unknown Branch"),
            "segment": row.get("segment", "Retail"),
            "risk_type": "Credit Risk",
            "priority": round(priority, 2),
            "priority_level": priority_level(priority),
            "recommended_action": "Review affordability, credit exposure, repayment capacity, and consider manual underwriting escalation.",
            "status": "Open",
        })

    return actions


def build_fraud_actions(transactions):
    actions = []

    if transactions is None or transactions.empty:
        return actions

    data = transactions.copy()

    for col in ["fraud_risk_score", "amount"]:
        if col not in data.columns:
            data[col] = 0

        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    high_risk = data[data["fraud_risk_score"] >= 70]

    for _, row in high_risk.iterrows():
        priority = min(
            100,
            row["fraud_risk_score"] * 0.75
            + min(row["amount"] / 2000, 25)
        )

        actions.append({
            "customer_id": row.get("customer_id", "UNKNOWN"),
            "customer_name": row.get("customer_name", "Unknown Customer"),
            "branch": row.get("branch", "Unknown Branch"),
            "segment": row.get("segment", "Retail"),
            "risk_type": "Fraud Alert",
            "priority": round(priority, 2),
            "priority_level": priority_level(priority),
            "recommended_action": "Place transaction in investigation queue, verify customer activity, and monitor related transactions.",
            "status": "Open",
        })

    return actions


def build_aml_actions(transactions):
    actions = []

    if transactions is None or transactions.empty:
        return actions

    data = transactions.copy()

    for col in ["aml_risk_score", "amount"]:
        if col not in data.columns:
            data[col] = 0

        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    high_risk = data[data["aml_risk_score"] >= 70]

    for _, row in high_risk.iterrows():
        priority = min(
            100,
            row["aml_risk_score"] * 0.75
            + min(row["amount"] / 3000, 25)
        )

        actions.append({
            "customer_id": row.get("customer_id", "UNKNOWN"),
            "customer_name": row.get("customer_name", "Unknown Customer"),
            "branch": row.get("branch", "Unknown Branch"),
            "segment": row.get("segment", "Retail"),
            "risk_type": "AML Investigation",
            "priority": round(priority, 2),
            "priority_level": priority_level(priority),
            "recommended_action": "Escalate for compliance review, check KYC profile, source of funds, and cross-border transaction pattern.",
            "status": "Open",
        })

    return actions


def build_customer_actions(customers):
    actions = []

    if customers is None or customers.empty:
        return actions

    data = customers.copy()

    for col in ["churn_risk", "account_balance"]:
        if col not in data.columns:
            data[col] = 0

        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    high_churn = data[data["churn_risk"] >= 70]

    for _, row in high_churn.iterrows():
        priority = min(
            100,
            row["churn_risk"] * 0.7
            + min(max(row["account_balance"], 0) / 10000, 30)
        )

        actions.append({
            "customer_id": row.get("customer_id", "UNKNOWN"),
            "customer_name": row.get("customer_name", "Unknown Customer"),
            "branch": row.get("branch", "Unknown Branch"),
            "segment": row.get("segment", "Retail"),
            "risk_type": "Customer Churn",
            "priority": round(priority, 2),
            "priority_level": priority_level(priority),
            "recommended_action": "Assign relationship manager, offer retention intervention, and review product engagement.",
            "status": "Open",
        })

    return actions


def generate_executive_actions(customers, loans, transactions):
    actions = []

    actions.extend(build_credit_actions(loans))
    actions.extend(build_fraud_actions(transactions))
    actions.extend(build_aml_actions(transactions))
    actions.extend(build_customer_actions(customers))

    actions_df = pd.DataFrame(actions)

    if actions_df.empty:
        return pd.DataFrame(
            columns=[
                "customer_id",
                "customer_name",
                "branch",
                "segment",
                "risk_type",
                "priority",
                "priority_level",
                "recommended_action",
                "status",
            ]
        )

    actions_df = actions_df.sort_values(
        ["priority", "risk_type"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return actions_df


def summarize_actions(actions_df):
    if actions_df is None or actions_df.empty:
        return {
            "total_actions": 0,
            "critical_actions": 0,
            "high_actions": 0,
            "top_risk_type": "None",
            "top_branch": "None",
        }

    return {
        "total_actions": len(actions_df),
        "critical_actions": int((actions_df["priority_level"] == "Critical").sum()),
        "high_actions": int((actions_df["priority_level"] == "High").sum()),
        "top_risk_type": actions_df["risk_type"].value_counts().index[0],
        "top_branch": actions_df["branch"].value_counts().index[0],
    }
