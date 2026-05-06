import os

try:
    import google.generativeai as genai
except Exception:
    genai = None


def get_gemini_api_key():
    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        return os.getenv("GEMINI_API_KEY")


def generate_fallback_response(prompt):
    return f"""
### Executive AI Response

FinGuard AI has analyzed the available banking context.

Key recommendations:
- Prioritize high-risk credit accounts for manual review.
- Investigate suspicious high-value and cross-border transactions.
- Escalate AML cases involving cash deposits or enhanced due diligence countries.
- Monitor customer churn risk and protect high-value deposit relationships.
- Use audit logs and action queues to track decisions and accountability.

Note: Gemini API key is not configured, so this response is generated using the built-in fallback engine.
"""


def generate_llm_response(prompt):
    api_key = get_gemini_api_key()

    if genai is None or not api_key:
        return generate_fallback_response(prompt)

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            f"""
You are FinGuard AI, an executive banking intelligence copilot.

You help banking leaders, risk analysts, compliance teams, and AI engineers interpret:
- credit risk
- fraud detection
- AML monitoring
- customer churn
- forecasting
- executive actions
- audit logs
- AI predictions

Rules:
- Be concise.
- Use executive language.
- Highlight risks clearly.
- Give practical recommended actions.
- Avoid pretending to access external systems.
- Base your answer only on the provided context.

Context and question:
{prompt}
"""
        )

        return response.text

    except Exception as e:
        return generate_fallback_response(prompt) + f"\n\nAPI fallback reason: {str(e)}"
