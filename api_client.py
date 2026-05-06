import requests


API_BASE_URL = "http://127.0.0.1:8000"


def check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()

        return {
            "status": "unavailable",
            "error": f"Status code: {response.status_code}"
        }

    except Exception as e:
        return {
            "status": "unavailable",
            "error": str(e)
        }


def predict_credit_risk(payload):
    try:
        response = requests.post(
            f"{API_BASE_URL}/credit-risk",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        return {
            "error": f"API error: {response.status_code}",
            "details": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def predict_fraud_risk(payload):
    try:
        response = requests.post(
            f"{API_BASE_URL}/fraud-risk",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        return {
            "error": f"API error: {response.status_code}",
            "details": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }
