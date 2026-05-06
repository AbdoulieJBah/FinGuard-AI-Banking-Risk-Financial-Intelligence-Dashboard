import streamlit as st
import plotly.express as px

from ui_utils import setup_page, premium_hero, metric_card, insight_card, section_title, style_plotly
from data_utils import load_data
from action_engine import generate_executive_actions, summarize_actions
from database import init_db, save_executive_action, save_audit_log, load_executive_actions
from stream_engine import generate_stream_batch, summarize_stream


setup_page("Autonomous Action Engine", icon="🎯")
init_db()

customers, loans, transactions = load_data()

actions_df = generate_executive_actions(customers, loans, transactions)
summary = summarize_actions(actions_df)

premium_hero(
    "🎯 Autonomous Action Engine",
    "Automated banking action engine for credit reviews, fraud investigations, AML escalation, and customer retention priorities.",
    badge="Autonomous Banking Action Engine"
)

section_title("📌 Action KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Generated Actions", f"{summary['total_actions']:,}", "AI action queue")

with c2:
    metric_card("Critical Actions", f"{summary['critical_actions']:,}", "Urgent escalation")

with c3:
    metric_card("High Actions", f"{summary['high_actions']:,}", "Priority review")

with c4:
    metric_card("Top Risk Type", summary["top_risk_type"], "Main pressure area")

section_title("🧠 Executive Risk Summary")

if actions_df.empty:
    insight_card("✅ No major executive actions detected.", level="good")
else:
    top = actions_df.iloc[0]

    level = "critical" if top["priority_level"] == "Critical" else "risk"

    insight_card(
        f"""
<b>Top priority:</b> {top['risk_type']}<br>
<b>Customer:</b> {top['customer_name']}<br>
<b>Branch:</b> {top['branch']}<br>
<b>Priority:</b> {top['priority']}/100<br>
<b>Action:</b> {top['recommended_action']}
""",
        level=level
    )

section_title("🔎 Action Filters")

f1, f2, f3 = st.columns(3)

with f1:
    risk_filter = st.multiselect(
        "Risk Type",
        sorted(actions_df["risk_type"].unique()) if not actions_df.empty else []
    )

with f2:
    priority_filter = st.multiselect(
        "Priority Level",
        sorted(actions_df["priority_level"].unique()) if not actions_df.empty else []
    )

with f3:
    branch_filter = st.multiselect(
        "Branch",
        sorted(actions_df["branch"].unique()) if not actions_df.empty else []
    )

filtered = actions_df.copy()

if risk_filter:
    filtered = filtered[filtered["risk_type"].isin(risk_filter)]

if priority_filter:
    filtered = filtered[filtered["priority_level"].isin(priority_filter)]

if branch_filter:
    filtered = filtered[filtered["branch"].isin(branch_filter)]

section_title("📋 Executive Action Queue")

if filtered.empty:
    insight_card("No actions match the selected filters.", level="risk")
else:
    st.dataframe(filtered, use_container_width=True)

section_title("📊 Action Intelligence Charts")

if not actions_df.empty:
    c1, c2 = st.columns(2)

    with c1:
        fig_risk = px.bar(
            actions_df.groupby("risk_type")
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False),
            x="risk_type",
            y="count",
            title="Actions by Risk Type"
        )
        st.plotly_chart(style_plotly(fig_risk), use_container_width=True)

    with c2:
        fig_priority = px.histogram(
            actions_df,
            x="priority",
            color="priority_level",
            title="Priority Score Distribution"
        )
        st.plotly_chart(style_plotly(fig_priority), use_container_width=True)

    fig_branch = px.bar(
        actions_df.groupby("branch")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(15),
        x="branch",
        y="count",
        title="Top Branches by Action Count"
    )
    st.plotly_chart(style_plotly(fig_branch), use_container_width=True)

# -----------------------------
# LIVE RISK STREAM
# -----------------------------
section_title("📡 Live Risk Stream")

stream_df = generate_stream_batch(
    customers,
    loans,
    transactions,
    n=12
)

stream_summary = summarize_stream(stream_df)

s1, s2, s3, s4 = st.columns(4)

with s1:
    metric_card(
        "Stream Events",
        f"{stream_summary['events']:,}",
        "Live monitoring queue"
    )

with s2:
    metric_card(
        "Critical Events",
        f"{stream_summary['critical']:,}",
        "Urgent escalation"
    )

with s3:
    metric_card(
        "High Events",
        f"{stream_summary['high']:,}",
        "Priority monitoring"
    )

with s4:
    metric_card(
        "Top Event",
        stream_summary["top_event"],
        "Dominant signal"
    )

if stream_df.empty:
    insight_card(
        "No live stream events generated.",
        level="risk"
    )

else:

    for _, row in stream_df.iterrows():

        level = "good"

        if row["risk_level"] == "Critical":
            level = "critical"

        elif row["risk_level"] in ["High", "Medium"]:
            level = "risk"

        insight_card(
            f"""
<b>{row['event_type']}</b><br>

<b>Customer:</b> {row['customer_name']}<br>
<b>Branch:</b> {row['branch']}<br>
<b>Risk Score:</b> {row['risk_score']}/100<br>
<b>Risk Level:</b> {row['risk_level']}<br><br>

<b>Event:</b> {row['message']}<br>
<b>Recommended Action:</b> {row['recommended_action']}
""",
            level=level
        )

st.dataframe(
    stream_df,
    use_container_width=True
)

section_title("💾 Save Actions to Database")

if actions_df.empty:
    insight_card("No actions available to save.", level="risk")
else:
    save_limit = st.slider(
        "Number of top actions to save",
        min_value=1,
        max_value=min(100, len(actions_df)),
        value=min(25, len(actions_df))
    )

    if st.button("Save Top Actions to Database", use_container_width=True):
        for _, action in actions_df.head(save_limit).iterrows():
            save_executive_action(action.to_dict())

        save_audit_log(
            event_type="Executive Actions",
            event_message=f"{save_limit} executive actions saved to database."
        )

        st.success(f"✅ {save_limit} executive actions saved to database.")

section_title("🗄️ Saved Executive Actions")

saved_actions = load_executive_actions(limit=100)

if saved_actions.empty:
    insight_card("No saved executive actions yet.", level="risk")
else:
    st.dataframe(saved_actions, use_container_width=True)

section_title("⬇️ Export Action Report")

st.download_button(
    "Download Executive Action Queue",
    actions_df.to_csv(index=False),
    "finguard_executive_action_queue.csv",
    "text/csv",
    use_container_width=True
)
