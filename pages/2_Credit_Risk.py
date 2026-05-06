import streamlit as st
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, balanced_accuracy_score
from sklearn.ensemble import RandomForestClassifier

from ui_utils import setup_page, premium_hero, metric_card, insight_card, section_title, style_plotly
from data_utils import load_data
from global_copilot import render_global_copilot
from auth import require_login


setup_page("Credit Risk", icon="💳")

customers, loans, transactions = load_data()

premium_hero(
    "💳 Credit Risk Intelligence",
    """
    Machine learning powered loan default risk scoring for banking portfolios.
    Analyze borrower risk, credit quality, loan exposure, debt-to-income pressure,
    and high-risk customer segments.
    """,
    badge="ML Credit Risk Scoring"
)

# -----------------------------
# DATA PREP
# -----------------------------
model_df = loans.copy()

features = [
    "age",
    "annual_income",
    "account_balance",
    "credit_score",
    "years_with_bank",
    "num_products",
    "debt_to_income",
    "loan_amount",
    "interest_rate",
    "loan_term_months",
    "monthly_payment",
]

X = model_df[features]
y = model_df["default_flag"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=250,
    max_depth=8,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

preds = model.predict(X_test)
probs = model.predict_proba(X_test)[:, 1]

balanced_acc = balanced_accuracy_score(y_test, preds)
accuracy = accuracy_score(y_test, preds)
precision = precision_score(y_test, preds, zero_division=0)
recall = recall_score(y_test, preds, zero_division=0)
f1 = f1_score(y_test, preds, zero_division=0)

model_df["ml_default_probability"] = model.predict_proba(X)[:, 1] * 100

model_df["ml_risk_level"] = model_df["ml_default_probability"].apply(
    lambda x: "High" if x >= 70 else "Medium" if x >= 40 else "Low"
)

# -----------------------------
# KPIs
# -----------------------------
section_title("📌 Credit Risk KPIs")

high_risk_loans = model_df[model_df["ml_risk_level"] == "High"]
medium_risk_loans = model_df[model_df["ml_risk_level"] == "Medium"]
low_risk_loans = model_df[model_df["ml_risk_level"] == "Low"]

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Loan Accounts", f"{len(model_df):,}", "Active loan portfolio")

with c2:
    metric_card("Loan Book", f"£{model_df['loan_amount'].sum():,.0f}", "Total exposure")

with c3:
    metric_card("High Risk Loans", f"{len(high_risk_loans):,}", "ML risk ≥ 70%")

with c4:
    metric_card("Avg Default Probability", f"{model_df['ml_default_probability'].mean():.1f}%", "Portfolio risk")

m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    metric_card("Balanced Accuracy", f"{balanced_acc:.2f}", "Class imbalance aware")

with m2:
    metric_card("Accuracy", f"{accuracy:.2f}", "Overall correctness")

with m3:
    metric_card("Precision", f"{precision:.2f}", "Risk alert quality")

with m4:
    metric_card("Recall", f"{recall:.2f}", "Default capture")

with m5:
    metric_card("F1 Score", f"{f1:.2f}", "Balanced model score")

# -----------------------------
# RISK INSIGHTS
# -----------------------------
section_title("🧠 Credit Risk Intelligence")

if len(high_risk_loans) > 0:
    insight_card(
        f"⚠️ {len(high_risk_loans):,} loans are classified as high risk. Credit review should prioritize these accounts.",
        level="critical"
    )
else:
    insight_card("✅ No high-risk loans detected by the ML model.", level="good")

if model_df["debt_to_income"].mean() > 0.45:
    insight_card(
        "⚠️ Average debt-to-income ratio is elevated. Borrower affordability pressure may be increasing.",
        level="risk"
    )
else:
    insight_card("✅ Debt-to-income pressure appears manageable.", level="good")

if model_df["credit_score"].mean() < 620:
    insight_card(
        "⚠️ Average credit score is below preferred lending quality threshold.",
        level="risk"
    )
else:
    insight_card("✅ Average credit quality appears stable.", level="good")

# -----------------------------
# RISK DISTRIBUTION
# -----------------------------
section_title("📊 Credit Risk Distribution")

risk_counts = (
    model_df["ml_risk_level"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = ["Risk Level", "Count"]

r1, r2 = st.columns(2)

with r1:
    fig_risk = px.pie(
        risk_counts,
        names="Risk Level",
        values="Count",
        title="ML Credit Risk Distribution",
        hole=0.45
    )
    st.plotly_chart(style_plotly(fig_risk), use_container_width=True)

with r2:
    fig_prob = px.histogram(
        model_df,
        x="ml_default_probability",
        color="ml_risk_level",
        nbins=35,
        title="Default Probability Distribution"
    )
    st.plotly_chart(style_plotly(fig_prob), use_container_width=True)

# -----------------------------
# FEATURE IMPORTANCE
# -----------------------------
section_title("🧪 Model Feature Importance")

importance_df = (
    dict(zip(features, model.feature_importances_))
)

importance_df = (
    __import__("pandas")
    .DataFrame(
        {
            "feature": list(importance_df.keys()),
            "importance": list(importance_df.values())
        }
    )
    .sort_values("importance", ascending=False)
)

fig_importance = px.bar(
    importance_df,
    x="importance",
    y="feature",
    orientation="h",
    title="Credit Risk Model Feature Importance"
)

st.plotly_chart(style_plotly(fig_importance), use_container_width=True)

st.dataframe(importance_df, use_container_width=True)

# -----------------------------
# PORTFOLIO SEGMENTS
# -----------------------------
section_title("🏦 Credit Risk by Segment and Branch")

seg_risk = (
    model_df.groupby("segment")
    .agg(
        loans=("loan_id", "count"),
        exposure=("loan_amount", "sum"),
        avg_default_probability=("ml_default_probability", "mean"),
        high_risk_loans=("ml_risk_level", lambda x: (x == "High").sum()),
    )
    .reset_index()
)

branch_risk = (
    model_df.groupby("branch")
    .agg(
        loans=("loan_id", "count"),
        exposure=("loan_amount", "sum"),
        avg_default_probability=("ml_default_probability", "mean"),
        high_risk_loans=("ml_risk_level", lambda x: (x == "High").sum()),
    )
    .reset_index()
)

b1, b2 = st.columns(2)

with b1:
    fig_seg = px.bar(
        seg_risk.sort_values("avg_default_probability", ascending=False),
        x="segment",
        y="avg_default_probability",
        title="Average Default Probability by Segment"
    )
    st.plotly_chart(style_plotly(fig_seg), use_container_width=True)

with b2:
    fig_branch = px.bar(
        branch_risk.sort_values("avg_default_probability", ascending=False),
        x="branch",
        y="avg_default_probability",
        title="Average Default Probability by Branch"
    )
    st.plotly_chart(style_plotly(fig_branch), use_container_width=True)

st.dataframe(seg_risk, use_container_width=True)
st.dataframe(branch_risk, use_container_width=True)

# -----------------------------
# HIGH RISK LOAN TABLE
# -----------------------------
section_title("🚨 High Risk Loan Watchlist")

watch_cols = [
    "loan_id",
    "customer_id",
    "branch",
    "segment",
    "employment_status",
    "annual_income",
    "credit_score",
    "debt_to_income",
    "loan_amount",
    "interest_rate",
    "ml_default_probability",
    "ml_risk_level",
]

if len(high_risk_loans) > 0:
    st.dataframe(
        high_risk_loans[watch_cols].sort_values("ml_default_probability", ascending=False),
        use_container_width=True
    )
else:
    insight_card("✅ No loans currently meet the high-risk threshold.", level="good")

# -----------------------------
# SINGLE CUSTOMER SCORING
# -----------------------------
section_title("🔍 Manual Credit Risk Scoring")

with st.expander("Score a New Loan Applicant"):
    a1, a2, a3 = st.columns(3)

    with a1:
        age = st.number_input("Age", 18, 80, 35)
        annual_income = st.number_input("Annual Income", 5000, 300000, 52000)
        account_balance = st.number_input("Account Balance", -10000, 500000, 9000)
        credit_score = st.number_input("Credit Score", 300, 850, 660)

    with a2:
        years_with_bank = st.number_input("Years with Bank", 0, 40, 3)
        num_products = st.number_input("Number of Products", 1, 10, 2)
        debt_to_income = st.slider("Debt-to-Income Ratio", 0.0, 1.0, 0.35)
        loan_amount = st.number_input("Loan Amount", 1000, 500000, 40000)

    with a3:
        interest_rate = st.slider("Interest Rate", 1.0, 25.0, 7.2)
        loan_term_months = st.selectbox("Loan Term Months", [12, 24, 36, 48, 60, 72, 84])
        monthly_payment = loan_amount * (1 + interest_rate / 100) / loan_term_months

    if st.button("Score Applicant", use_container_width=True):
        input_df = __import__("pandas").DataFrame([{
            "age": age,
            "annual_income": annual_income,
            "account_balance": account_balance,
            "credit_score": credit_score,
            "years_with_bank": years_with_bank,
            "num_products": num_products,
            "debt_to_income": debt_to_income,
            "loan_amount": loan_amount,
            "interest_rate": interest_rate,
            "loan_term_months": loan_term_months,
            "monthly_payment": monthly_payment,
        }])

        probability = model.predict_proba(input_df)[0, 1] * 100
        risk_level = "High" if probability >= 70 else "Medium" if probability >= 40 else "Low"

        metric_card("Predicted Default Probability", f"{probability:.1f}%", f"{risk_level} risk")

        if risk_level == "High":
            insight_card("⚠️ Recommendation: escalate to manual credit review before approval.", level="critical")
        elif risk_level == "Medium":
            insight_card("⚠️ Recommendation: consider lower exposure, collateral, or adjusted interest rate.", level="risk")
        else:
            insight_card("✅ Recommendation: applicant appears within acceptable credit risk range.", level="good")

# -----------------------------
# DOWNLOAD
# -----------------------------
section_title("⬇️ Export Credit Risk Data")

st.download_button(
    "Download Credit Risk Scored Portfolio",
    model_df.to_csv(index=False),
    "finguard_credit_risk_scored_portfolio.csv",
    "text/csv",
    use_container_width=True
)
render_global_copilot(
    page_name="Credit Risk",
    page_context="This page shows executive banking KPIs, credit risk, fraud alerts, AML exposure, customers, deposits, and portfolio performance."
)
