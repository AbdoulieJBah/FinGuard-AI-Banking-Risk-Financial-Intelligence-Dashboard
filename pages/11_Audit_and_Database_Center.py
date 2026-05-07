import streamlit as st

from auth import require_login
from global_copilot import render_global_copilot
from auth import require_role
from ui_utils import setup_page, premium_hero, metric_card, insight_card, section_title
from database import (
    init_db,
    load_prediction_logs,
    load_executive_actions,
    load_audit_logs,
    update_action_status,
)


setup_page("Audit & Database Center", icon="🗄️")
require_role(["Admin"])
init_db()

premium_hero(
    "🗄️ Audit & Database Center",
    "Persistent banking intelligence storage for AI prediction logs, executive actions, audit trails, and operational monitoring.",
    badge="Database + Audit Intelligence"
)


# -----------------------------
# LOAD DATA
# -----------------------------
prediction_logs = load_prediction_logs(limit=200)
executive_actions = load_executive_actions(limit=300)
audit_logs = load_audit_logs(limit=200)


# -----------------------------
# KPIs
# -----------------------------
section_title("📌 Database KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Prediction Logs", f"{len(prediction_logs):,}", "AI inference history")

with c2:
    metric_card("Executive Actions", f"{len(executive_actions):,}", "Saved risk actions")

with c3:
    open_actions = (
        (executive_actions["status"] == "Open").sum()
        if not executive_actions.empty and "status" in executive_actions.columns
        else 0
    )
    metric_card("Open Actions", f"{open_actions:,}", "Pending review")

with c4:
    metric_card("Audit Logs", f"{len(audit_logs):,}", "System events")


# -----------------------------
# DATABASE STATUS
# -----------------------------
section_title("🧠 Database Intelligence")

if prediction_logs.empty and executive_actions.empty and audit_logs.empty:
    insight_card(
        "⚠️ Database is initialized but no records are saved yet. Use Real-Time AI Predictions and Executive Action Center to generate persistent records.",
        level="risk"
    )
else:
    insight_card(
        "✅ Database is active and storing FinGuard AI operational records.",
        level="good"
    )


# -----------------------------
# PREDICTION LOGS
# -----------------------------
section_title("⚡ AI Prediction Logs")

if prediction_logs.empty:
    insight_card("No prediction logs saved yet.", level="risk")
else:
    st.dataframe(prediction_logs, use_container_width=True)


# -----------------------------
# EXECUTIVE ACTIONS
# -----------------------------
section_title("🎯 Executive Actions Database")

if executive_actions.empty:
    insight_card("No executive actions saved yet.", level="risk")
else:
    st.dataframe(executive_actions, use_container_width=True)

    section_title("🔄 Update Action Status")

    selected_action_id = st.selectbox(
        "Select Action ID",
        executive_actions["id"].tolist()
    )

    selected_action = executive_actions[
        executive_actions["id"] == selected_action_id
    ].iloc[0]

    a1, a2, a3 = st.columns(3)

    with a1:
        metric_card("Risk Type", selected_action["risk_type"], "Action category")

    with a2:
        metric_card("Priority", f"{selected_action['priority']:.1f}", "Risk score")

    with a3:
        metric_card("Status", selected_action["status"], "Current state")

    new_status = st.selectbox(
        "New Status",
        ["Open", "In Progress", "Resolved"],
        index=["Open", "In Progress", "Resolved"].index(selected_action["status"])
        if selected_action["status"] in ["Open", "In Progress", "Resolved"]
        else 0
    )

    if st.button("Update Status", use_container_width=True):
        update_action_status(selected_action_id, new_status)
        st.success("✅ Action status updated.")
        st.rerun()


# -----------------------------
# AUDIT LOGS
# -----------------------------
section_title("🧾 Audit Logs")

if audit_logs.empty:
    insight_card("No audit logs saved yet.", level="risk")
else:
    st.dataframe(audit_logs, use_container_width=True)


# -----------------------------
# EXPORTS
# -----------------------------
section_title("⬇️ Export Database Records")

e1, e2, e3 = st.columns(3)

with e1:
    st.download_button(
        "Download Prediction Logs",
        prediction_logs.to_csv(index=False),
        "finguard_prediction_logs.csv",
        "text/csv",
        use_container_width=True
    )

with e2:
    st.download_button(
        "Download Executive Actions",
        executive_actions.to_csv(index=False),
        "finguard_executive_actions.csv",
        "text/csv",
        use_container_width=True
    )

with e3:
    st.download_button(
        "Download Audit Logs",
        audit_logs.to_csv(index=False),
        "finguard_audit_logs.csv",
        "text/csv",
        use_container_width=True
    )
render_global_copilot(
    page_name="Audit And Database Center",
    page_context="This page shows executive banking KPIs, credit risk, fraud alerts, AML exposure, customers, deposits, and portfolio performance."
)
