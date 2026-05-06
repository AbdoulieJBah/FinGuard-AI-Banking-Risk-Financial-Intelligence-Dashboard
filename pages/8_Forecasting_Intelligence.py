import streamlit as st
import pandas as pd
import plotly.express as px

from ui_utils import setup_page, premium_hero, metric_card, insight_card, section_title, style_plotly
from data_utils import load_data
from global_copilot import render_global_copilot
from auth import require_login


setup_page("Forecasting Intelligence", icon="📈")

customers, loans, transactions = load_data()

premium_hero(
    "📈 Forecasting Intelligence",
    "Predictive banking analytics for transaction volume, transaction value, fraud alerts, AML alerts, customer churn pressure, and credit risk exposure.",
    badge="Banking Forecasting & Predictive Intelligence"
)

# -----------------------------
# SAFE DATE SETUP
# -----------------------------
transactions = transactions.copy()

if "date" not in transactions.columns:
    transactions["date"] = pd.date_range(
        end=pd.Timestamp.today(),
        periods=len(transactions),
        freq="h"
    )

transactions["date"] = pd.to_datetime(transactions["date"], errors="coerce")
transactions["date_only"] = transactions["date"].dt.date

daily = (
    transactions.dropna(subset=["date_only"])
    .groupby("date_only")
    .agg(
        transactions=("transaction_id", "count"),
        transaction_value=("amount", "sum"),
        fraud_alerts=("fraud_flag", "sum"),
        aml_alerts=("aml_flag", "sum"),
    )
    .reset_index()
)

daily["date_only"] = pd.to_datetime(daily["date_only"])
daily = daily.sort_values("date_only")

# -----------------------------
# SIMPLE FORECAST FUNCTION
# -----------------------------
def forecast_series(data, target_col, periods=14):
    df = data[["date_only", target_col]].copy()
    df = df.rename(columns={"date_only": "date", target_col: "value"})
    df = df.sort_values("date")

    df["rolling_7"] = df["value"].rolling(7, min_periods=1).mean()

    last_date = df["date"].max()
    last_value = df["rolling_7"].iloc[-1]

    recent_trend = 0
    if len(df) >= 14:
        recent_trend = (
            df["rolling_7"].iloc[-1] - df["rolling_7"].iloc[-7]
        ) / 7

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=periods,
        freq="D"
    )

    forecast_values = [
        max(0, last_value + recent_trend * i)
        for i in range(1, periods + 1)
    ]

    forecast_df = pd.DataFrame({
        "date": future_dates,
        "value": forecast_values,
        "type": "Forecast"
    })

    historical_df = df[["date", "value"]].copy()
    historical_df["type"] = "Historical"

    return pd.concat([historical_df, forecast_df], ignore_index=True)


# -----------------------------
# FORECAST DATA
# -----------------------------
tx_forecast = forecast_series(daily, "transactions")
value_forecast = forecast_series(daily, "transaction_value")
fraud_forecast = forecast_series(daily, "fraud_alerts")
aml_forecast = forecast_series(daily, "aml_alerts")

next_14_tx = tx_forecast[tx_forecast["type"] == "Forecast"]["value"].sum()
next_14_value = value_forecast[value_forecast["type"] == "Forecast"]["value"].sum()
next_14_fraud = fraud_forecast[fraud_forecast["type"] == "Forecast"]["value"].sum()
next_14_aml = aml_forecast[aml_forecast["type"] == "Forecast"]["value"].sum()

# -----------------------------
# KPIs
# -----------------------------
section_title("📌 Forecast KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("Next 14-Day Tx", f"{next_14_tx:,.0f}", "Forecast volume")

with c2:
    metric_card("Next 14-Day Value", f"£{next_14_value:,.0f}", "Forecast flow")

with c3:
    metric_card("Fraud Alerts", f"{next_14_fraud:,.0f}", "Expected cases")

with c4:
    metric_card("AML Alerts", f"{next_14_aml:,.0f}", "Expected cases")

# -----------------------------
# INSIGHTS
# -----------------------------
section_title("🧠 Forecast Intelligence")

if next_14_fraud > daily["fraud_alerts"].tail(14).sum():
    insight_card(
        "⚠️ Fraud alert forecast is above the recent historical level. Fraud operations should prepare additional review capacity.",
        level="risk"
    )
else:
    insight_card(
        "✅ Fraud forecast appears stable compared with recent history.",
        level="good"
    )

if next_14_aml > daily["aml_alerts"].tail(14).sum():
    insight_card(
        "⚠️ AML alert forecast is rising. Compliance team should monitor cross-border and high-value flows.",
        level="risk"
    )
else:
    insight_card(
        "✅ AML forecast appears stable.",
        level="good"
    )

if next_14_value > daily["transaction_value"].tail(14).sum() * 1.2:
    insight_card(
        "📈 Transaction value is forecasted to increase significantly. Monitor liquidity, fraud exposure, and transaction operations capacity.",
        level="risk"
    )
else:
    insight_card(
        "✅ Transaction value forecast is within expected range.",
        level="good"
    )

# -----------------------------
# FORECAST CHARTS
# -----------------------------
section_title("📊 Banking Forecast Charts")

f1, f2 = st.columns(2)

with f1:
    fig_tx = px.line(
        tx_forecast,
        x="date",
        y="value",
        color="type",
        title="Transaction Volume Forecast",
        markers=True
    )
    st.plotly_chart(style_plotly(fig_tx), use_container_width=True)

with f2:
    fig_value = px.line(
        value_forecast,
        x="date",
        y="value",
        color="type",
        title="Transaction Value Forecast",
        markers=True
    )
    st.plotly_chart(style_plotly(fig_value), use_container_width=True)

f3, f4 = st.columns(2)

with f3:
    fig_fraud = px.line(
        fraud_forecast,
        x="date",
        y="value",
        color="type",
        title="Fraud Alert Forecast",
        markers=True
    )
    st.plotly_chart(style_plotly(fig_fraud), use_container_width=True)

with f4:
    fig_aml = px.line(
        aml_forecast,
        x="date",
        y="value",
        color="type",
        title="AML Alert Forecast",
        markers=True
    )
    st.plotly_chart(style_plotly(fig_aml), use_container_width=True)

# -----------------------------
# CREDIT & CHURN PRESSURE
# -----------------------------
section_title("🏦 Portfolio Pressure Forecast")

high_risk_loans = loans[loans["default_probability"] >= 70]
high_churn_customers = customers[customers["churn_risk"] >= 70]

p1, p2, p3, p4 = st.columns(4)

with p1:
    metric_card("High-Risk Loans", f"{len(high_risk_loans):,}", "Credit pressure")

with p2:
    metric_card("Credit Exposure", f"£{high_risk_loans['loan_amount'].sum():,.0f}", "High-risk loan book")

with p3:
    metric_card("High-Churn Customers", f"{len(high_churn_customers):,}", "Retention pressure")

with p4:
    metric_card("Churn Deposits", f"£{high_churn_customers['account_balance'].clip(lower=0).sum():,.0f}", "At-risk deposits")

if len(high_risk_loans) > 0:
    insight_card(
        "⚠️ High-risk loan exposure should be reviewed alongside transaction and AML forecasts.",
        level="risk"
    )

if len(high_churn_customers) > 0:
    insight_card(
        "⚠️ Retention campaigns should prioritize high-churn customers with meaningful deposit balances.",
        level="risk"
    )

# -----------------------------
# EXPORT
# -----------------------------
section_title("⬇️ Export Forecast Data")

export_df = pd.concat(
    [
        tx_forecast.assign(metric="transactions"),
        value_forecast.assign(metric="transaction_value"),
        fraud_forecast.assign(metric="fraud_alerts"),
        aml_forecast.assign(metric="aml_alerts"),
    ],
    ignore_index=True
)

st.download_button(
    "Download Forecast Report",
    export_df.to_csv(index=False),
    "finguard_forecasting_report.csv",
    "text/csv",
    use_container_width=True
)
render_global_copilot(
    page_name="Forecasting Intelligence",
    page_context="This page shows executive banking KPIs, credit risk, fraud alerts, AML exposure, customers, deposits, and portfolio performance."
)
