"""Business Analysis: problem statement, stakeholders, business questions,
and the user stories that shaped this project's requirements.
"""

import streamlit as st

from src.ui import apply_theme, page_header

st.set_page_config(page_title="Business Analysis", layout="wide")
apply_theme()
page_header("Business Analysis", "The reasoning behind this app: the problem, the people it serves, and the questions it answers.")

with st.container(border=True):
    st.subheader("Business Problem")
    st.markdown(
        "> The management team needs a simple way to understand historical "
        "performance and evaluate how business assumptions affect a simulated "
        "valuation."
    )

st.subheader("Stakeholders")
stakeholder_cols = st.columns(4)
stakeholders = [
    ("Management", "Needs a synthetic view of historical performance."),
    ("Finance Team", "Needs reliable, traceable KPIs (no hardcoded figures)."),
    ("Business Analyst", "Translates business assumptions into financial impact."),
    ("Strategy Team", "Needs to understand how sensitive the valuation is to key assumptions."),
]
for col, (name, need) in zip(stakeholder_cols, stakeholders):
    with col:
        with st.container(border=True):
            st.markdown(f"**{name}**")
            st.caption(need)

st.subheader("Business Questions")
with st.container(border=True):
    st.markdown(
        """
1. How has revenue evolved?
2. How has profitability evolved?
3. What assumptions drive the forecast?
4. How sensitive is valuation to WACC?
5. How sensitive is valuation to terminal growth?
6. How does EBITDA margin affect valuation?
"""
    )

st.subheader("User Stories")
with st.container(border=True):
    st.markdown(
        """
- As **management**, I want to see revenue and EBITDA evolution so I can understand the company's trajectory.
- As a **business analyst**, I want to adjust growth and margin assumptions so I can produce a 3-year forecast.
- As the **strategy team**, I want to visualize a WACC x Terminal Growth heatmap so I can understand valuation sensitivity.
- As a **user**, I want to export results to CSV so I can reuse them elsewhere.
"""
    )
