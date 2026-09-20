"""Downside / Base / Upside scenarios, presented side by side."""

import streamlit as st

from src.data_loader import load_financials
from src.scenarios import SCENARIOS, run_scenarios

st.set_page_config(page_title="FinScope - Scenarios", layout="wide")
st.title("Scenarios")
st.caption(
    "Three assumption sets applied to the same forecast + DCF engine. "
    "Results are presented as-is, without labelling any scenario as better."
)

historical = load_financials("data/financials.csv")
forecast_years = [2026, 2027, 2028]

input_col1, input_col2 = st.columns(2)
wacc_pct = input_col1.slider("WACC %", 3.0, 20.0, 9.0, 0.5, format="%.1f%%")
terminal_growth_pct = input_col2.slider("Terminal Growth %", 0.0, 6.0, 2.5, 0.25, format="%.2f%%")
wacc = wacc_pct / 100
terminal_growth = terminal_growth_pct / 100

if wacc <= terminal_growth:
    st.error("WACC must be strictly greater than Terminal Growth.")
    st.stop()

results = run_scenarios(historical, forecast_years, wacc, terminal_growth)

st.subheader("Scenario Assumptions")
assumption_cols = st.columns(3)
for col, (name, assumptions) in zip(assumption_cols, SCENARIOS.items()):
    col.metric(f"{name} — Revenue Growth", f"{assumptions['revenue_growth']:.0%}")
    col.metric(f"{name} — EBITDA Margin", f"{assumptions['ebitda_margin']:.0%}")

st.subheader(f"Results (final forecast year: {forecast_years[-1]})")
st.dataframe(
    results.set_index("Scenario").style.format(
        {
            "Revenue_Growth": "{:.0%}",
            "EBITDA_Margin": "{:.0%}",
            "Final_Year_Revenue": "{:,.0f}",
            "Final_Year_EBITDA": "{:,.0f}",
            "Final_Year_FCF": "{:,.0f}",
            "Enterprise_Value": "{:,.0f}",
        }
    ),
    use_container_width=True,
)
