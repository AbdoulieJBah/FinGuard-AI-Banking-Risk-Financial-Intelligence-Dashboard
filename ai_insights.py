def generate_executive_insights(kpis, credit_kpis=None, fraud_kpis=None, aml_kpis=None, customer_kpis=None):
    insights = []

    if kpis.get("default_rate", 0) > 10:
        insights.append("⚠️ Credit default exposure is elevated. Management should review high-risk borrowers and affordability pressure.")
    else:
        insights.append("✅ Credit portfolio default exposure appears controlled.")

    if kpis.get("fraud_cases", 0) > 0:
        insights.append(f"⚠️ {kpis.get('fraud_cases', 0)} fraud alerts detected. Fraud operations should review suspicious transactions.")
    else:
        insights.append("✅ No major fraud alert pressure detected.")

    if kpis.get("aml_cases", 0) > 0:
        insights.append(f"⚠️ {kpis.get('aml_cases', 0)} AML alerts detected. Compliance review may be required.")
    else:
        insights.append("✅ AML monitoring appears stable.")

    if kpis.get("avg_churn_risk", 0) > 45:
        insights.append("⚠️ Customer churn risk is increasing. Relationship managers should prioritize retention campaigns.")
    else:
        insights.append("✅ Customer churn risk is within an acceptable range.")

    if credit_kpis and credit_kpis.get("high_risk_loans", 0) > 0:
        insights.append(f"📌 Credit team should prioritize {credit_kpis.get('high_risk_loans', 0)} high-risk loan accounts.")

    if fraud_kpis and fraud_kpis.get("high_risk_transactions", 0) > 0:
        insights.append(f"📌 Fraud team should investigate {fraud_kpis.get('high_risk_transactions', 0)} high-risk transactions.")

    if aml_kpis and aml_kpis.get("cross_border_transactions", 0) > 0:
        insights.append(f"📌 Compliance should monitor {aml_kpis.get('cross_border_transactions', 0)} cross-border transactions.")

    if customer_kpis and customer_kpis.get("high_churn_customers", 0) > 0:
        insights.append(f"📌 Customer team should contact {customer_kpis.get('high_churn_customers', 0)} high-churn-risk customers.")

    return insights


def generate_risk_recommendations(actions):
    recommendations = []

    if actions is None or len(actions) == 0:
        return ["✅ No urgent executive risk actions detected. Continue monitoring portfolio performance."]

    top_risk = actions.iloc[0]

    recommendations.append(
        f"🚨 Immediate priority: {top_risk.get('risk_type', 'Risk')} for {top_risk.get('customer_name', 'Unknown Customer')}."
    )

    recommendations.append(
        f"🎯 Recommended action: {top_risk.get('recommended_action', 'Review this case with the responsible team.')}"
    )

    risk_counts = actions["risk_type"].value_counts().to_dict() if "risk_type" in actions.columns else {}

    if risk_counts:
        main_risk = max(risk_counts, key=risk_counts.get)
        recommendations.append(
            f"📊 Most frequent risk category: {main_risk} with {risk_counts[main_risk]} cases."
        )

    if "branch" in actions.columns:
        branch_counts = actions["branch"].value_counts()
        if len(branch_counts) > 0:
            recommendations.append(
                f"🏦 Branch requiring most attention: {branch_counts.index[0]} with {branch_counts.iloc[0]} risk items."
            )

    return recommendations


def explain_credit_prediction(row, probability):
    reasons = []

    if row.get("credit_score", 700) < 580:
        reasons.append("low credit score")

    if row.get("debt_to_income", 0) > 0.45:
        reasons.append("high debt-to-income ratio")

    if row.get("account_balance", 0) < 500:
        reasons.append("low account balance")

    if row.get("employment_status", "") == "Unemployed":
        reasons.append("unemployment risk")

    if row.get("loan_amount", 0) > row.get("annual_income", 1):
        reasons.append("loan amount is high relative to income")

    if not reasons:
        reasons.append("general portfolio risk factors")

    return (
        f"Predicted default probability is {probability}%. "
        f"Main contributing factors: {', '.join(reasons)}."
    )


def explain_fraud_transaction(row):
    reasons = []

    if row.get("is_high_value", False):
        reasons.append("high-value transaction")

    if row.get("is_cross_border", False):
        reasons.append("cross-border activity")

    if row.get("is_night_tx", False):
        reasons.append("night-time transaction")

    if row.get("transaction_type", "") == "International Transfer":
        reasons.append("international transfer")

    if row.get("amount", 0) > 10000:
        reasons.append("large transaction amount")

    if not reasons:
        reasons.append("pattern differs from normal activity")

    return f"Fraud risk drivers: {', '.join(reasons)}."
