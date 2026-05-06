import streamlit as st

from utils import setup_page, premium_hero, metric_card, insight_card, section_title


setup_page("FinGuard AI", icon="🏦")


# -----------------------------
# HERO
# -----------------------------
premium_hero(
    "🏦 FinGuard <span>AI</span>",
    """
    Premium banking risk and financial intelligence platform for credit risk,
    fraud detection, AML monitoring, customer intelligence, executive analytics,
    and AI-powered banking decision support.
    """,
    badge="AI Banking Risk Intelligence Platform"
)


# -----------------------------
# PLATFORM OVERVIEW
# -----------------------------
section_title("🚀 Platform Overview")

st.markdown("""
<div class="glass-card">
    <b>FinGuard AI</b> is an end-to-end finance and banking analytics platform designed
    to help banks understand risk, monitor financial performance, detect suspicious activity,
    and support smarter decision-making.
    <br><br>
    It combines <b>Business Intelligence</b>, <b>Machine Learning</b>,
    <b>Fraud Detection</b>, <b>Credit Risk Scoring</b>, <b>AML Compliance</b>,
    and an <b>AI Banking Copilot</b> in one executive-level dashboard.
</div>
""", unsafe_allow_html=True)


# -----------------------------
# CORE MODULES
# -----------------------------
section_title("🏛️ Core Banking Modules")

c1, c2, c3 = st.columns(3)

with c1:
    metric_card(
        "Executive Dashboard",
        "BI Layer",
        "Revenue, loans, deposits, customers"
    )

with c2:
    metric_card(
        "Credit Risk",
        "ML Scoring",
        "Loan default prediction"
    )

with c3:
    metric_card(
        "Fraud Detection",
        "Risk Engine",
        "Suspicious transaction monitoring"
    )

c4, c5, c6 = st.columns(3)

with c4:
    metric_card(
        "Customer Intelligence",
        "Segmentation",
        "Churn and product insights"
    )

with c5:
    metric_card(
        "Compliance AML",
        "Monitoring",
        "KYC and transaction risk"
    )

with c6:
    metric_card(
        "AI Banking Copilot",
        "Decision Support",
        "Ask questions across the platform"
    )


# -----------------------------
# VALUE PROPOSITION
# -----------------------------
section_title("💡 Why This Project Matters")

v1, v2 = st.columns(2)

with v1:
    insight_card(
        """
        <b>For banking roles:</b><br>
        Shows strong understanding of credit risk, fraud analytics,
        compliance monitoring, financial KPIs, and AI-driven decision support.
        """,
        level="good"
    )

with v2:
    insight_card(
        """
        <b>For AI/Data roles:</b><br>
        Demonstrates data engineering, machine learning, risk scoring,
        dashboards, analytics storytelling, and real-world business impact.
        """,
        level="good"
    )


# -----------------------------
# ARCHITECTURE
# -----------------------------
section_title("🧠 Technical Architecture")

a1, a2, a3, a4 = st.columns(4)

with a1:
    metric_card("Frontend", "Streamlit", "Interactive banking UI")

with a2:
    metric_card("Analytics", "Pandas + Plotly", "Financial intelligence")

with a3:
    metric_card("Machine Learning", "Scikit-learn", "Risk prediction")

with a4:
    metric_card("AI Layer", "Gemini/OpenAI Ready", "Copilot support")


# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")

st.markdown("""
### 🏦 FinGuard AI  
Built by **Abdoulie J Bah**  
AI Engineer • Data Scientist • Financial Intelligence Developer
""")
