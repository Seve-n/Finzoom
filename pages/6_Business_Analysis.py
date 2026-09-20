"""Business Analysis: problem statement, stakeholders, business questions,
and the user stories that shaped this project's requirements.
"""

import streamlit as st

st.set_page_config(page_title="FinZoom - Business Analysis", layout="wide")
st.title("Business Analysis")

st.subheader("Business Problem")
st.markdown(
    "> The management team needs a simple way to understand historical "
    "performance and evaluate how business assumptions affect a simulated "
    "valuation."
)

st.subheader("Stakeholders")
st.markdown(
    """
- **Management** — needs a synthetic view of historical performance.
- **Finance Team** — needs reliable, traceable KPIs (no hardcoded figures).
- **Business Analyst** — translates business assumptions into financial impact.
- **Strategy Team** — needs to understand how sensitive the valuation is to key assumptions.
"""
)

st.subheader("Business Questions")
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
st.markdown(
    """
- As **management**, I want to see revenue and EBITDA evolution so I can understand the company's trajectory.
- As a **business analyst**, I want to adjust growth and margin assumptions so I can produce a 3-year forecast.
- As the **strategy team**, I want to visualize a WACC x Terminal Growth heatmap so I can understand valuation sensitivity.
- As a **user**, I want to export results to CSV so I can reuse them elsewhere.
"""
)
