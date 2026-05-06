import os

try:
    import google.generativeai as genai
except Exception as import_error:
    genai = None
    GENAI_IMPORT_ERROR = str(import_error)
else:
    GENAI_IMPORT_ERROR = None


def get_gemini_api_key():
    """
    Reads Gemini API key from Streamlit secrets first,
    then environment variables as fallback.
    """

    try:
        import streamlit as st

        key = st.secrets.get("GEMINI_API_KEY", None)

        if key:
            return str(key).strip()

    except Exception:
        pass

    key = os.getenv("GEMINI_API_KEY")

    if key:
        return str(key).strip()

    return None


def gemini_debug_status():
    """
    Safe debug helper. Does not expose the actual API key.
    """

    api_key = get_gemini_api_key()

    return {
        "gemini_package_loaded": genai is not None,
        "gemini_import_error": GENAI_IMPORT_ERROR,
        "gemini_key_found": bool(api_key),
        "gemini_key_length": len(api_key) if api_key else 0,
    }


def generate_fallback_response(prompt, reason="Gemini is not configured"):
    return f"""
### Executive AI Response

FinGuard AI has analyzed the available banking context.

Key recommendations:
- Prioritize high-risk credit accounts for manual review.
- Investigate suspicious high-value and cross-border transactions.
- Escalate AML cases involving cash deposits or enhanced due diligence countries.
- Monitor customer churn risk and protect high-value deposit relationships.
- Use audit logs and action queues to track decisions and accountability.

**Copilot mode:** Built-in fallback engine  
**Fallback reason:** {reason}
"""


def generate_llm_response(prompt):
    api_key = get_gemini_api_key()

    if genai is None:
        return generate_fallback_response(
            prompt,
            reason=f"google-generativeai package not loaded: {GENAI_IMPORT_ERROR}"
        )

    if not api_key:
        return generate_fallback_response(
            prompt,
            reason="GEMINI_API_KEY not found in Streamlit secrets or environment variables"
        )

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

        if hasattr(response, "text") and response.text:
            return response.text

        return generate_fallback_response(
            prompt,
            reason="Gemini returned an empty response"
        )

    except Exception as e:
        return generate_fallback_response(
            prompt,
            reason=f"Gemini API error: {str(e)}"
        )
