def credit_risk_level(probability):
    if probability >= 70:
        return "High"
    if probability >= 40:
        return "Medium"
    return "Low"


def fraud_risk_score(amount, country, transaction_type, hour):
    score = 0
    reasons = []

    if amount > 7500:
        score += 35
        reasons.append("High-value transaction")

    if 0 <= hour <= 5:
        score += 18
        reasons.append("Night-time activity")

    if country != "UK":
        score += 20
        reasons.append("Cross-border transaction")

    if transaction_type == "International Transfer":
        score += 22
        reasons.append("International transfer risk")

    score = min(score + 10, 100)

    return score, reasons


def aml_risk_score(amount, country, transaction_type):
    score = 0
    reasons = []

    if amount > 10000:
        score += 30
        reasons.append("High-value transaction")

    if country != "UK":
        score += 25
        reasons.append("Cross-border transaction")

    if country in ["Nigeria", "Gambia", "UAE"]:
        score += 18
        reasons.append("Enhanced due diligence country exposure")

    if transaction_type == "Cash Deposit":
        score += 15
        reasons.append("Cash deposit monitoring trigger")

    if transaction_type == "International Transfer":
        score += 12
        reasons.append("International transfer review")

    score = min(score, 100)

    return score, reasons
