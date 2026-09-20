"""FinZoom - Home / Executive Financial Dashboard.

Entry point of the Streamlit app. Opens with a short "how this works"
stepper (this app doubles as a portfolio piece, so first-time clarity
matters more than usual), then the latest-year KPIs, four historical
evolution charts, auto-generated descriptive insights, and a data quality
panel.
"""

import plotly.graph_objects as go
import streamlit as st

from src.calculations import compute_all_kpis, revenue_cagr
from src.data_loader import load_financials
from src.data_quality import run_all_checks
from src.ui import CHART_PALETTE, apply_theme, how_it_works, page_header

st.set_page_config(page_title="FinZoom", page_icon="📈", layout="wide")
apply_theme()

with st.container(key="hero_badge"):
    st.markdown("Fictional portfolio project — synthetic data only")

page_header(
    "FinZoom — Financial Analysis & Valuation Dashboard",
    'Historical performance, forecast, and DCF valuation for a fictional B2B SaaS '
    'company, "NovaTech Solutions". Not affiliated with KPMG or any real company.',
)

st.divider()
st.subheader("How this dashboard works")
how_it_works()
st.divider()

historical = load_financials("data/financials.csv")
enriched = compute_all_kpis(historical)
latest = enriched.iloc[-1]
previous = enriched.iloc[-2]

st.subheader(f"Financial Snapshot — FY{int(latest['Year'])}")

with st.container(border=True):
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
    with st.container(border=True):
        fig_revenue = go.Figure(
            go.Bar(x=enriched["Year"], y=enriched["Revenue"], marker_color=CHART_PALETTE["accent"])
        )
        fig_revenue.update_layout(title="Revenue Evolution", yaxis_title="EUR", margin=dict(t=40))
        st.plotly_chart(fig_revenue, use_container_width=True)

    with st.container(border=True):
        fig_margin = go.Figure(
            go.Scatter(
                x=enriched["Year"],
                y=enriched["EBITDA_Margin"],
                mode="lines+markers",
                line=dict(color=CHART_PALETTE["accent"]),
            )
        )
        fig_margin.update_layout(title="EBITDA Margin Evolution", yaxis_tickformat=".0%", margin=dict(t=40))
        st.plotly_chart(fig_margin, use_container_width=True)

with chart_col2:
    with st.container(border=True):
        fig_ebitda = go.Figure(
            go.Bar(x=enriched["Year"], y=enriched["EBITDA"], marker_color=CHART_PALETTE["primary"])
        )
        fig_ebitda.update_layout(title="EBITDA Evolution", yaxis_title="EUR", margin=dict(t=40))
        st.plotly_chart(fig_ebitda, use_container_width=True)

    with st.container(border=True):
        fig_fcf = go.Figure(
            go.Scatter(
                x=enriched["Year"],
                y=enriched["Free_Cash_Flow"],
                mode="lines+markers",
                line=dict(color=CHART_PALETTE["primary"]),
            )
        )
        fig_fcf.update_layout(title="Free Cash Flow Evolution", yaxis_title="EUR", margin=dict(t=40))
        st.plotly_chart(fig_fcf, use_container_width=True)

st.divider()

st.subheader("Financial Insights")
st.caption("Descriptive observations only — no investment recommendations.")

start_revenue = enriched["Revenue"].iloc[0]
end_revenue = enriched["Revenue"].iloc[-1]
start_margin = enriched["EBITDA_Margin"].iloc[0]
end_margin = enriched["EBITDA_Margin"].iloc[-1]
cagr = revenue_cagr(historical)

with st.container(border=True):
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
    "Use the sidebar to go deeper: Financials for the full statements, Forecast to "
    "set your own assumptions, Valuation for the DCF, Sensitivity and Scenarios to "
    "stress-test it, and Business Analysis / Requirements for the BA deliverables."
)
