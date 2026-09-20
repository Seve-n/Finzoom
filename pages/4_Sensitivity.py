"""Sensitivity analysis: Enterprise Value under WACC x Terminal Growth
combinations, and under Revenue Growth x EBITDA Margin combinations.
"""

import plotly.graph_objects as go
import streamlit as st

from src.data_loader import load_financials
from src.forecast import build_forecast
from src.valuation import sensitivity_growth_margin, sensitivity_wacc_growth

st.set_page_config(page_title="FinZoom - Sensitivity", layout="wide")
st.title("Sensitivity Analysis")

historical = load_financials("data/financials.csv")
forecast_years = [2026, 2027, 2028]

st.subheader("Enterprise Value: WACC x Terminal Growth")
st.caption(
    "Free Cash Flow is fixed using the Revenue Growth and EBITDA Margin below, "
    "then Enterprise Value is recomputed for each WACC / Terminal Growth pair."
)

base_col1, base_col2 = st.columns(2)
base_growth = base_col1.slider("Revenue Growth % (flat, for this analysis)", 0.0, 40.0, 12.0, 1.0, format="%.0f%%") / 100
base_margin = base_col2.slider("EBITDA Margin % (flat, for this analysis)", 0.0, 45.0, 20.0, 1.0, format="%.0f%%") / 100

base_forecast = build_forecast(
    historical, forecast_years, [base_growth] * 3, [base_margin] * 3
)

wacc_range = [0.08, 0.09, 0.10, 0.11]
growth_range = [0.02, 0.025, 0.03]

wacc_table = sensitivity_wacc_growth(base_forecast["Free_Cash_Flow"], wacc_range, growth_range)

fig1 = go.Figure(
    data=go.Heatmap(
        z=wacc_table.values / 1e6,
        x=wacc_table.columns,
        y=wacc_table.index,
        colorscale="Blues",
        text=(wacc_table.values / 1e6).round(1),
        texttemplate="%{text}M",
        hovertemplate="WACC %{y}, Terminal Growth %{x}: €%{z:.1f}M<extra></extra>",
    )
)
fig1.update_layout(
    title="Enterprise Value (€M) — rows: WACC, columns: Terminal Growth",
    xaxis_title="Terminal Growth",
    yaxis_title="WACC",
)
st.plotly_chart(fig1, use_container_width=True)

st.divider()
st.subheader("Enterprise Value: Revenue Growth x EBITDA Margin")
st.caption("WACC and Terminal Growth are fixed below; Revenue Growth and EBITDA Margin vary.")

fixed_col1, fixed_col2 = st.columns(2)
fixed_wacc_pct = fixed_col1.slider("WACC (fixed) %", 3.0, 20.0, 9.0, 0.5, format="%.1f%%")
fixed_terminal_growth_pct = fixed_col2.slider("Terminal Growth (fixed) %", 0.0, 6.0, 2.5, 0.25, format="%.2f%%")
fixed_wacc = fixed_wacc_pct / 100
fixed_terminal_growth = fixed_terminal_growth_pct / 100

if fixed_wacc <= fixed_terminal_growth:
    st.error("WACC must be strictly greater than Terminal Growth.")
    st.stop()

growth_axis = [0.08, 0.12, 0.16, 0.20]
margin_axis = [0.16, 0.20, 0.24, 0.28]

growth_margin_table = sensitivity_growth_margin(
    historical, forecast_years, growth_axis, margin_axis, fixed_wacc, fixed_terminal_growth
)

fig2 = go.Figure(
    data=go.Heatmap(
        z=growth_margin_table.values / 1e6,
        x=growth_margin_table.columns,
        y=growth_margin_table.index,
        colorscale="Greens",
        text=(growth_margin_table.values / 1e6).round(1),
        texttemplate="%{text}M",
        hovertemplate="Revenue Growth %{y}, EBITDA Margin %{x}: €%{z:.1f}M<extra></extra>",
    )
)
fig2.update_layout(
    title="Enterprise Value (€M) — rows: Revenue Growth, columns: EBITDA Margin",
    xaxis_title="EBITDA Margin",
    yaxis_title="Revenue Growth",
)
st.plotly_chart(fig2, use_container_width=True)
