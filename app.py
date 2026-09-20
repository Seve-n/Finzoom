"""FinZoom - Home / Executive Financial Dashboard.

Entry point of the Streamlit app. Shows the latest-year KPIs, four
historical evolution charts, auto-generated descriptive insights, and a
data quality panel.
"""

import plotly.graph_objects as go
import streamlit as st

from src.calculations import compute_all_kpis, revenue_cagr
from src.data_loader import load_financials
from src.data_quality import run_all_checks

st.set_page_config(page_title="FinZoom", layout="wide")

st.title("FinZoom — Financial Analysis & Valuation Dashboard")
st.caption(
    "Fictional portfolio project analyzing a synthetic B2B SaaS company, "
    "\"NovaTech Solutions\". Not affiliated with KPMG or any real company."
)

historical = load_financials("data/financials.csv")
enriched = compute_all_kpis(historical)
latest = enriched.iloc[-1]
previous = enriched.iloc[-2]

st.header(f"Financial Snapshot — FY{int(latest['Year'])}")

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Revenue", f"€{latest['Revenue']/1e6:.1f}M", f"{latest['Revenue_Growth']:+.1%}")
col2.metric("Revenue Growth", f"{latest['Revenue_Growth']:.1%}")
col3.metric("EBITDA", f"€{latest['EBITDA']/1e6:.1f}M")
col4.metric(
    "EBITDA Margin",
    f"{latest['EBITDA_Margin']:.1%}",
    f"{(latest['EBITDA_Margin'] - previous['EBITDA_Margin']) * 100:+.1f} pts",
)
col5.metric("Net Income", f"€{latest['Net_Income']/1e6:.1f}M")
col6.metric("Free Cash Flow", f"€{latest['Free_Cash_Flow']/1e6:.1f}M")

st.divider()

st.subheader("Historical Evolution (2021-2025)")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_revenue = go.Figure(
        go.Bar(x=enriched["Year"], y=enriched["Revenue"], marker_color="#2E5EAA")
    )
    fig_revenue.update_layout(title="Revenue Evolution", yaxis_title="EUR")
    st.plotly_chart(fig_revenue, use_container_width=True)

    fig_margin = go.Figure(
        go.Scatter(
            x=enriched["Year"],
            y=enriched["EBITDA_Margin"],
            mode="lines+markers",
            line=dict(color="#D9822B"),
        )
    )
    fig_margin.update_layout(title="EBITDA Margin Evolution", yaxis_tickformat=".0%")
    st.plotly_chart(fig_margin, use_container_width=True)

with chart_col2:
    fig_ebitda = go.Figure(
        go.Bar(x=enriched["Year"], y=enriched["EBITDA"], marker_color="#3E8E5A")
    )
    fig_ebitda.update_layout(title="EBITDA Evolution", yaxis_title="EUR")
    st.plotly_chart(fig_ebitda, use_container_width=True)

    fig_fcf = go.Figure(
        go.Scatter(
            x=enriched["Year"],
            y=enriched["Free_Cash_Flow"],
            mode="lines+markers",
            line=dict(color="#7A4FA3"),
        )
    )
    fig_fcf.update_layout(title="Free Cash Flow Evolution", yaxis_title="EUR")
    st.plotly_chart(fig_fcf, use_container_width=True)

st.divider()

st.subheader("Financial Insights")
st.caption("Descriptive observations only — no investment recommendations.")

start_revenue = enriched["Revenue"].iloc[0]
end_revenue = enriched["Revenue"].iloc[-1]
start_margin = enriched["EBITDA_Margin"].iloc[0]
end_margin = enriched["EBITDA_Margin"].iloc[-1]
cagr = revenue_cagr(historical)

st.markdown(
    f"""
- Revenue increased by **{(end_revenue / start_revenue - 1):.0%}** between
  {int(enriched['Year'].iloc[0])} and {int(enriched['Year'].iloc[-1])}
  (CAGR of **{cagr:.1%}**).
- EBITDA margin increased from **{start_margin:.1%}** to **{end_margin:.1%}**
  over the same period.
- Free cash flow represented **{latest['FCF_Margin']:.1%}** of revenue in
  {int(latest['Year'])}, compared to **{enriched['FCF_Margin'].iloc[0]:.1%}**
  in {int(enriched['Year'].iloc[0])}.
"""
)

st.divider()

with st.expander("Data Quality Checks"):
    issues = run_all_checks(historical)
    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("No data quality anomalies detected.")

st.divider()
st.caption(
    "Navigate through Financials, Forecast, Valuation, Sensitivity, Scenarios, "
    "Business Analysis and Requirements using the sidebar."
)
