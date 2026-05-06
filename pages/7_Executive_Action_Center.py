import streamlit as st
import pandas as pd

from ui_utils import setup_page, premium_hero, metric_card, insight_card, section_title
from data_utils import load_data


setup_page("Executive Action Center", icon="🎯")

customers, loans, transactions = load_data()

premium_hero(
    "🎯 Executive Action Center",
    "Central command page for credit risk, fraud, AML, customer churn, and management action priorities.",
    badge="Banking Risk Action Hub"
)

# Credit actions
credit_actions = loans[loans["default_probability"] >= 70].copy()
credit_actions["risk_type"] = "Credit Risk"
credit_actions["priority"] = credit_actions["default_probability"]
credit_actions["recommended_action"] = "Review affordability, credit exposure, and repayment plan."

# Fraud actions
fraud_actions = transactions[transactions["fraud_risk_score"] >= 70].copy()
fraud_actions["risk_type"] = "Fraud Risk"
fraud_actions["priority"] = fraud_actions["fraud_risk_score"]
fraud_actions["recommended_action"] = "Investigate suspicious transaction and verify customer activity."

# AML actions
aml_actions = transactions[transactions["aml_risk_score"] >= 65].copy()
aml_actions["risk_type"] = "AML Compliance"
aml_actions["priority"] = aml_actions["aml_risk_score"]
aml_actions["recommended_action"] = "Escalate for compliance review and enhanced due diligence."

# Churn actions
churn_actions = customers[customers["churn_risk"] >= 70].copy()
churn_actions["risk_type"] = "Customer Churn"
churn_actions["priority"] = churn_actions["churn_risk"]
churn_actions["recommended_action"] = "Contact customer with retention or relationship management offer."

actions = pd.concat(
    [
        credit_actions[["customer_id", "customer_name", "branch", "segment", "risk_type", "priority", "recommended_action"]],
        fraud_actions[["customer_id", "customer_name", "branch", "segment", "risk_type", "priority", "recommended_action"]],
        aml_actions[["customer_id", "customer_name", "branch", "segment", "risk_type", "priority", "recommended_action"]],
        churn_actions[["customer_id", "customer_name", "branch", "segment", "risk_type", "priority", "recommended_action"]],
    ],
    ignore_index=True
)

actions["priority_level"] = actions["priority"].apply(
    lambda x: "Critical" if x >= 80 else "High" if x >= 65 else "Medium"
)

actions = actions.sort_values("priority", ascending=False)

section_title("📌 Action KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Total Actions", f"{len(actions):,}", "Risk items")

with c2:
    metric_card("Credit Actions", f"{len(credit_actions):,}", "Loan risk")

with c3:
    metric_card("Fraud Actions", f"{len(fraud_actions):,}", "Suspicious activity")

with c4:
    metric_card("AML Actions", f"{len(aml_actions):,}", "Compliance review")

c5, c6, c7, c8 = st.columns(4)

with c5:
    metric_card("Churn Actions", f"{len(churn_actions):,}", "Retention risk")

with c6:
    metric_card("Critical Items", f"{(actions['priority_level'] == 'Critical').sum():,}", "Priority ≥ 80")

with c7:
    metric_card("Branches", f"{actions['branch'].nunique() if len(actions) else 0}", "Affected locations")

with c8:
    metric_card("Avg Priority", f"{actions['priority'].mean():.1f}" if len(actions) else "0", "Risk score")

section_title("🧠 Executive Risk Summary")

if len(actions) == 0:
    insight_card("✅ No major executive actions detected.", level="good")
else:
    worst = actions.iloc[0]
    insight_card(
        f"""
<b>Top priority:</b> {worst['risk_type']}<br>
<b>Customer:</b> {worst['customer_name']}<br>
<b>Branch:</b> {worst['branch']}<br>
<b>Priority:</b> {worst['priority']:.1f}/100<br>
<b>Action:</b> {worst['recommended_action']}
""",
        level="critical"
    )

section_title("🔎 Action Filters")

f1, f2, f3 = st.columns(3)

with f1:
    risk_filter = st.selectbox(
        "Risk Type",
        ["All"] + sorted(actions["risk_type"].unique().tolist()) if len(actions) else ["All"]
    )

with f2:
    branch_filter = st.selectbox(
        "Branch",
        ["All"] + sorted(actions["branch"].unique().tolist()) if len(actions) else ["All"]
    )

with f3:
    priority_filter = st.selectbox(
        "Priority Level",
        ["All", "Critical", "High", "Medium"]
    )

filtered = actions.copy()

if risk_filter != "All":
    filtered = filtered[filtered["risk_type"] == risk_filter]

if branch_filter != "All":
    filtered = filtered[filtered["branch"] == branch_filter]

if priority_filter != "All":
    filtered = filtered[filtered["priority_level"] == priority_filter]

section_title("📋 Executive Action Queue")

if len(filtered) == 0:
    insight_card("No matching actions found.", level="risk")
else:
    st.dataframe(filtered, use_container_width=True)

section_title("⬇️ Export Action Report")

st.download_button(
    "Download Executive Action Report",
    actions.to_csv(index=False),
    "finguard_executive_action_report.csv",
    "text/csv",
    use_container_width=True
)
