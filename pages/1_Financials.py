"""Detailed historical financial statements + KPI table, with CSV export."""

import streamlit as st

from src.calculations import compute_all_kpis
from src.data_loader import load_financials

st.set_page_config(page_title="FinZoom - Financials", layout="wide")
st.title("Historical Financials")

historical = load_financials("data/financials.csv")
enriched = compute_all_kpis(historical)

st.subheader("Income Statement & Cash Flow Drivers (2021-2025)")
st.dataframe(
    historical.set_index("Year").style.format("{:,.0f}"),
    use_container_width=True,
)

st.subheader("KPIs")
kpi_columns = ["Year", "Revenue_Growth", "EBITDA_Margin", "Net_Margin", "Free_Cash_Flow", "FCF_Margin"]
kpi_table = enriched[kpi_columns].set_index("Year")
st.dataframe(
    kpi_table.style.format(
        {
            "Revenue_Growth": "{:.1%}",
            "EBITDA_Margin": "{:.1%}",
            "Net_Margin": "{:.1%}",
            "Free_Cash_Flow": "{:,.0f}",
            "FCF_Margin": "{:.1%}",
        }
    ),
    use_container_width=True,
)

st.download_button(
    "Export Financial Summary (CSV)",
    data=enriched.to_csv(index=False).encode("utf-8"),
    file_name="finzoom_financial_summary.csv",
    mime="text/csv",
)
