import streamlit as st
import plotly.graph_objects as go


# -----------------------------
# GLOBAL PAGE SETUP
# -----------------------------
def setup_page(title, icon="🏦"):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    inject_global_css()


# -----------------------------
# GLOBAL CSS
# -----------------------------
def inject_global_css():

    st.markdown("""
    <style>

    section[data-testid="stSidebarNav"] {
        display: none;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, #14213d 0%, #0b1220 40%, #050816 100%);
        color: #f3f4f6;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #0a0f1f 0%, #111827 100%);
        border-right: 1px solid rgba(255,215,0,0.18);
    }

    [data-testid="stSidebar"] * {
        color: #f3f4f6;
    }

    .hero-card {
        padding: 42px;
        border-radius: 28px;

        background:
            linear-gradient(
                135deg,
                rgba(15,23,42,0.96),
                rgba(17,24,39,0.92)
            );

        border: 1px solid rgba(255,215,0,0.22);

        box-shadow:
            0 18px 55px rgba(0,0,0,0.45),
            0 0 35px rgba(255,215,0,0.05);

        margin-bottom: 28px;
    }

    .hero-badge {
        display: inline-block;

        padding: 7px 16px;

        border-radius: 999px;

        background: rgba(255,215,0,0.12);

        color: #facc15;

        font-weight: 800;

        font-size: 0.78rem;

        margin-bottom: 18px;

        border: 1px solid rgba(255,215,0,0.25);
    }

    .hero-title {
        font-size: 3rem;

        font-weight: 950;

        color: #ffffff;

        letter-spacing: -0.04em;
    }

    .hero-title span {
        color: #facc15;
    }

    .hero-subtitle {
        margin-top: 16px;

        color: #d1d5db;

        font-size: 1.08rem;

        line-height: 1.8;

        max-width: 1000px;
    }

    .metric-card {
        padding: 24px;

        border-radius: 20px;

        background:
            rgba(15,23,42,0.86);

        border: 1px solid rgba(255,215,0,0.15);

        box-shadow:
            0 12px 30px rgba(0,0,0,0.28);

        margin-bottom: 14px;
    }

    .metric-label {
        color: #9ca3af;

        font-size: 0.88rem;

        font-weight: 700;
    }

    .metric-value {
        color: #ffffff;

        font-size: 2rem;

        font-weight: 900;

        margin-top: 8px;
    }

    .metric-delta {
        color: #facc15;

        margin-top: 8px;

        font-size: 0.85rem;
    }

    .glass-card {
        padding: 24px;

        border-radius: 22px;

        background:
            rgba(15,23,42,0.82);

        border: 1px solid rgba(255,255,255,0.06);

        box-shadow:
            0 14px 34px rgba(0,0,0,0.28);

        margin-bottom: 18px;
    }

    .section-title {
        color: #ffffff;

        font-size: 1.45rem;

        font-weight: 900;

        margin-top: 10px;

        margin-bottom: 18px;
    }

    .risk-card {
        border-left: 5px solid #ef4444;
    }

    .warning-card {
        border-left: 5px solid #f59e0b;
    }

    .good-card {
        border-left: 5px solid #22c55e;
    }

    div[data-testid="stMetric"] {
        background: rgba(15,23,42,0.85);

        border: 1px solid rgba(255,215,0,0.14);

        padding: 18px;

        border-radius: 16px;

        box-shadow:
            0 10px 28px rgba(0,0,0,0.24);
    }

    .stButton > button {

        border-radius: 14px;

        border: 1px solid rgba(255,215,0,0.32);

        background:
            linear-gradient(
                135deg,
                #b45309,
                #f59e0b
            );

        color: white;

        font-weight: 800;

        transition: 0.3s ease;
    }

    .stButton > button:hover {

        border-color: #fde047;

        box-shadow:
            0 0 22px rgba(250,204,21,0.28);

        transform: translateY(-1px);
    }

    .stDataFrame {
        border-radius: 18px;
        overflow: hidden;
    }

    h1, h2, h3 {
        color: #ffffff !important;
    }

    </style>
    """, unsafe_allow_html=True)


# -----------------------------
# HERO
# -----------------------------
def premium_hero(title, subtitle, badge="AI Banking Intelligence"):

    st.markdown(f"""
    <div class="hero-card">

        <div class="hero-badge">
            {badge}
        </div>

        <div class="hero-title">
            {title}
        </div>

        <div class="hero-subtitle">
            {subtitle}
        </div>

    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# METRIC CARD
# -----------------------------
def metric_card(label, value, delta=""):

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            {label}
        </div>

        <div class="metric-value">
            {value}
        </div>

        <div class="metric-delta">
            {delta}
        </div>

    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# SECTION TITLE
# -----------------------------
def section_title(title):

    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


# -----------------------------
# INSIGHT CARD
# -----------------------------
def insight_card(text, level="good"):

    css = "good-card"

    if level == "risk":
        css = "warning-card"

    if level == "critical":
        css = "risk-card"

    st.markdown(f"""
    <div class="glass-card {css}">
        {text}
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# PLOTLY THEME
# -----------------------------
def style_plotly(fig):

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.55)",

        font=dict(
            color="#e5e7eb"
        ),

        title_font=dict(
            size=20
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    return fig
