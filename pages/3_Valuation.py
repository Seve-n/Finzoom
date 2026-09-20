"""Simple DCF valuation page: Enterprise Value and Equity Value, computed
step by step from a short forecast built with adjustable assumptions.
"""

import pandas as pd
import streamlit as st

from src.data_loader import load_financials
from src.forecast import build_forecast
from src.valuation import equity_value, run_dcf

st.set_page_config(page_title="FinZoom - Valuation", layout="wide")
st.title("DCF Valuation")

st.markdown(
    """
A **Discounted Cash Flow (DCF)** values a company as the sum of its future
cash flows, brought back to today's value ("discounted") because a euro
received in the future is worth less than a euro today. Beyond the
explicit forecast period, a **Terminal Value** approximates all cash flows
generated afterward, assuming they grow at a constant rate forever.
"""
)

historical = load_financials("data/financials.csv")

st.subheader("Inputs")
input_col1, input_col2, input_col3 = st.columns(3)
wacc_pct = input_col1.slider("WACC (discount rate) %", 3.0, 20.0, 9.0, 0.5, format="%.1f%%")
terminal_growth_pct = input_col2.slider("Terminal Growth %", 0.0, 6.0, 2.5, 0.25, format="%.2f%%")
wacc = wacc_pct / 100
terminal_growth = terminal_growth_pct / 100
forecast_period = input_col3.slider("Forecast Period (years)", 2, 5, 3, 1)

st.caption("Revenue Growth and EBITDA Margin below are applied flat across the forecast period.")
assumption_col1, assumption_col2 = st.columns(2)
flat_growth = assumption_col1.slider("Revenue Growth (flat) %", 0.0, 40.0, 12.0, 1.0, format="%.0f%%") / 100
flat_margin = assumption_col2.slider("EBITDA Margin (flat) %", 0.0, 45.0, 20.0, 1.0, format="%.0f%%") / 100

if wacc <= terminal_growth:
    st.error(
        f"WACC ({wacc:.1%}) must be strictly greater than Terminal Growth "
        f"({terminal_growth:.1%}). Adjust the inputs above to compute a valuation."
    )
    st.stop()

forecast_years = [2025 + i for i in range(1, forecast_period + 1)]
forecast = build_forecast(
    historical, forecast_years, [flat_growth] * forecast_period, [flat_margin] * forecast_period
)

dcf = run_dcf(forecast["Free_Cash_Flow"], wacc, terminal_growth)

st.subheader("Step-by-Step DCF")
dcf_table = pd.DataFrame(
    {
        "Year": forecast_years,
        "Free Cash Flow": dcf["fcf"],
        "Discount Factor": dcf["discount_factors"],
        "Present Value of FCF": dcf["pv_fcf"],
    }
).set_index("Year")
st.dataframe(
    dcf_table.style.format({"Free Cash Flow": "{:,.0f}", "Discount Factor": "{:.3f}", "Present Value of FCF": "{:,.0f}"}),
    use_container_width=True,
)

summary_col1, summary_col2, summary_col3 = st.columns(3)
summary_col1.metric("Terminal Value", f"€{dcf['terminal_value']/1e6:,.1f}M")
summary_col2.metric("PV of Terminal Value", f"€{dcf['pv_terminal_value']/1e6:,.1f}M")
summary_col3.metric("Enterprise Value", f"€{dcf['enterprise_value']/1e6:,.1f}M")

st.divider()
st.subheader("Enterprise Value vs Equity Value")
st.markdown(
    """
**Enterprise Value (EV)** represents the value of the company's core
operations, independent of how it is financed. **Equity Value** is what
remains for shareholders once net debt is accounted for:
`Equity Value = Enterprise Value + Cash - Debt`.
"""
)

cash_col, debt_col = st.columns(2)
cash = cash_col.number_input("Cash", min_value=0, value=1_000_000, step=100_000)
debt = debt_col.number_input("Debt", min_value=0, value=2_000_000, step=100_000)

equity = equity_value(dcf["enterprise_value"], cash, debt)

result_col1, result_col2 = st.columns(2)
result_col1.metric("Enterprise Value", f"€{dcf['enterprise_value']/1e6:,.1f}M")
result_col2.metric("Equity Value", f"€{equity/1e6:,.1f}M")

valuation_summary = pd.DataFrame(
    [
        {"Metric": "WACC", "Value": wacc},
        {"Metric": "Terminal Growth", "Value": terminal_growth},
        {"Metric": "Terminal Value", "Value": dcf["terminal_value"]},
        {"Metric": "PV of Terminal Value", "Value": dcf["pv_terminal_value"]},
        {"Metric": "Enterprise Value", "Value": dcf["enterprise_value"]},
        {"Metric": "Cash", "Value": cash},
        {"Metric": "Debt", "Value": debt},
        {"Metric": "Equity Value", "Value": equity},
    ]
)
st.download_button(
    "Export Valuation Summary (CSV)",
    data=valuation_summary.to_csv(index=False).encode("utf-8"),
    file_name="finzoom_valuation_summary.csv",
    mime="text/csv",
)
