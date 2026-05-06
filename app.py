import streamlit as st

from ui_utils import (
    setup_page,
    premium_hero,
    metric_card,
    insight_card,
    section_title,
    glass_card,
)


setup_page("FinGuard AI", icon="🏦")


# -----------------------------
# HERO
# -----------------------------
premium_hero(
    "🏦 FinGuard <span>AI</span>",
    "Premium banking risk and financial intelligence platform for credit risk, fraud detection, AML monitoring, customer intelligence, executive analytics, and AI-powered banking decision support.",
    badge="AI Banking Risk Intelligence Platform"
)


# -----------------------------
# PLATFORM OVERVIEW
# -----------------------------
section_title("🚀 Platform Overview")

glass_card(
    """
<b>FinGuard AI</b> is an end-to-end finance and banking analytics platform designed
to help banks understand risk, monitor financial performance, detect suspicious activity,
and support smarter decision-making.
<br><br>
It combines <b>Business Intelligence</b>, <b>Machine Learning</b>,
<b>Fraud Detection</b>, <b>Credit Risk Scoring</b>, <b>AML Compliance</b>,
and an <b>AI Banking Copilot</b> in one executive-level dashboard.
"""
)


# -----------------------------
# CORE MODULES
# -----------------------------
section_title("🏛️ Core Banking Modules")

c1, c2, c3 = st.columns(3)

with c1:
    metric_card("Executive Dashboard", "BI Layer", "Revenue, loans, deposits, customers")

with c2:
    metric_card("Credit Risk", "ML Scoring", "Loan default prediction")

with c3:
    metric_card("Fraud Detection", "Risk Engine", "Suspicious transaction monitoring")

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

# NEW ROW
c7, c8, c9 = st.columns(3)

with c7:
    metric_card(
        "Executive Action Center",
        "Risk Actions",
        "Critical banking decisions"
    )

with c8:
    metric_card(
        "Fraud Watchlist",
        "Real-Time Monitoring",
        "Suspicious transaction queue"
    )

with c9:
    metric_card(
        "Executive Reporting",
        "Board Intelligence",
        "Exportable banking insights"
    )
# FORECASTING ROW
c10, c11, c12 = st.columns(3)

with c10:
    metric_card(
        "Forecasting Intelligence",
        "Predictive Analytics",
        "Fraud, AML, transaction and portfolio forecasts"
    )

with c11:
    metric_card(
        "Portfolio Pressure",
        "Risk Forecast",
        "Credit and churn exposure outlook"
    )

with c12:
    metric_card(
        "AI Executive Copilot",
        "Board AI Assistant",
        "Executive reasoning and risk recommendations"
    )

# -----------------------------
# VALUE PROPOSITION
# -----------------------------
section_title("💡 Why This Project Matters")

m1, m2 = st.columns(2)

with m1:
    insight_card(
        """
<b>For Banking Roles:</b><br><br>
Shows strong understanding of:
<ul>
    <li>Credit risk</li>
    <li>Fraud detection</li>
    <li>AML compliance</li>
    <li>Financial KPIs</li>
    <li>Executive intelligence dashboards</li>
</ul>
""",
        level="good"
    )

with m2:
    insight_card(
        """
<b>For AI/Data Roles:</b><br><br>
Demonstrates:
<ul>
    <li>Data engineering</li>
    <li>Machine learning workflows</li>
    <li>Analytics storytelling</li>
    <li>Interactive dashboards</li>
    <li>Real-world AI business applications</li>
</ul>
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
# PROJECT IMPACT
# -----------------------------
section_title("🎯 Portfolio Impact")

p1, p2, p3 = st.columns(3)

with p1:
    insight_card(
        "<b>Banking relevance:</b><br>Shows ability to work with credit, fraud, AML, customers, and financial risk analytics.",
        level="good"
    )

with p2:
    insight_card(
        "<b>AI relevance:</b><br>Demonstrates ML scoring, risk engines, customer intelligence, and AI decision support.",
        level="good"
    )

with p3:
    insight_card(
        "<b>Business relevance:</b><br>Turns raw banking data into executive insights, alerts, and recommended actions.",
        level="good"
    )


# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")

st.markdown(
    """
### 🏦 FinGuard AI  
Built by **Abdoulie J Bah**  
AI Engineer • Data Scientist • Financial Intelligence Developer
"""
)
