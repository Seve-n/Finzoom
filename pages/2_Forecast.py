"""3-year forecast (2026-2028) with user-adjustable Revenue Growth and
EBITDA Margin assumptions, compared against historical performance.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.calculations import compute_all_kpis
from src.data_loader import load_financials
from src.forecast import build_forecast

st.set_page_config(page_title="FinZoom - Forecast", layout="wide")
st.title("Forecast (2026-2028)")
st.caption(
    "Revenue Growth and EBITDA Margin are the only assumptions you control. "
    "D&A, Capex, Working Capital and the effective tax rate are held at "
    "their 2021-2025 historical average as a percentage of revenue."
)

historical = load_financials("data/financials.csv")
enriched = compute_all_kpis(historical)
forecast_years = [2026, 2027, 2028]

st.subheader("Assumptions")
growth_cols = st.columns(3)
default_growth_pct = [10.0, 12.0, 14.0]
growth_assumptions = [
    growth_cols[i].slider(
        f"Revenue Growth {forecast_years[i]} %", 0.0, 40.0, default_growth_pct[i], 1.0, format="%.0f%%"
    )
    / 100
    for i in range(3)
]

margin_cols = st.columns(3)
default_margin_pct = [18.0, 20.0, 22.0]
margin_assumptions = [
    margin_cols[i].slider(
        f"EBITDA Margin {forecast_years[i]} %", 0.0, 45.0, default_margin_pct[i], 1.0, format="%.0f%%"
    )
    / 100
    for i in range(3)
]

forecast = build_forecast(historical, forecast_years, growth_assumptions, margin_assumptions)

st.subheader("Forecast Table")
st.dataframe(
    forecast.set_index("Year").style.format(
        {
            "Revenue": "{:,.0f}",
            "Revenue_Growth": "{:.1%}",
            "EBITDA": "{:,.0f}",
            "EBITDA_Margin": "{:.1%}",
            "D_A": "{:,.0f}",
            "EBIT": "{:,.0f}",
            "Taxes": "{:,.0f}",
            "Net_Income": "{:,.0f}",
            "Capex": "{:,.0f}",
            "Working_Capital_Change": "{:,.0f}",
            "Free_Cash_Flow": "{:,.0f}",
        }
    ),
    use_container_width=True,
)

st.divider()
st.subheader("Historical vs Forecast")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=historical["Year"], y=historical["Revenue"], name="Historical", marker_color="#2E5EAA"))
    fig.add_trace(go.Bar(x=forecast["Year"], y=forecast["Revenue"], name="Forecast", marker_color="#D9822B"))
    fig.update_layout(title="Historical Revenue vs Forecast Revenue", yaxis_title="EUR")
    st.plotly_chart(fig, use_container_width=True)

with chart_col2:
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(x=historical["Year"], y=enriched["EBITDA_Margin"], mode="lines+markers", name="Historical", line=dict(color="#2E5EAA"))
    )
    fig2.add_trace(
        go.Scatter(x=forecast["Year"], y=forecast["EBITDA_Margin"], mode="lines+markers", name="Forecast", line=dict(color="#D9822B"))
    )
    fig2.update_layout(title="Historical EBITDA Margin vs Forecast EBITDA Margin", yaxis_tickformat=".0%")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Assumption Gap vs Historical Average")
st.caption("Descriptive comparison only — this does not judge whether the assumption is realistic.")

historical_avg_growth = enriched["Revenue_Growth"].mean()
forecast_avg_growth = pd.Series(growth_assumptions).mean()
historical_avg_margin = enriched["EBITDA_Margin"].mean()
forecast_avg_margin = pd.Series(margin_assumptions).mean()

gap_col1, gap_col2 = st.columns(2)
gap_col1.metric("Historical Average Revenue Growth", f"{historical_avg_growth:.1%}")
gap_col1.metric(
    "Forecast Revenue Growth (average)",
    f"{forecast_avg_growth:.1%}",
    f"{(forecast_avg_growth - historical_avg_growth) * 100:+.1f} pts vs historical average",
)
gap_col2.metric("Historical Average EBITDA Margin", f"{historical_avg_margin:.1%}")
gap_col2.metric(
    "Forecast EBITDA Margin (average)",
    f"{forecast_avg_margin:.1%}",
    f"{(forecast_avg_margin - historical_avg_margin) * 100:+.1f} pts vs historical average",
)

st.download_button(
    "Export Forecast (CSV)",
    data=forecast.to_csv(index=False).encode("utf-8"),
    file_name="finzoom_forecast.csv",
    mime="text/csv",
)
