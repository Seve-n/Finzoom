"""Requirements table (Business Analyst deliverable)."""

import pandas as pd
import streamlit as st

from src.ui import apply_theme, page_header

st.set_page_config(page_title="FinZoom - Requirements", page_icon="📋", layout="wide")
apply_theme()
page_header("Requirements", "The functional requirements this app was built against, with acceptance criteria and status.")

requirements = pd.DataFrame(
    [
        {
            "Requirement ID": "REQ-001",
            "Requirement": "The system shall display historical revenue.",
            "Priority": "High",
            "Acceptance Criteria": "Revenue for 2021-2025 is visible on the dashboard.",
            "Status": "Done",
        },
        {
            "Requirement ID": "REQ-002",
            "Requirement": "The system shall calculate EBITDA margin.",
            "Priority": "High",
            "Acceptance Criteria": "EBITDA Margin = EBITDA / Revenue, computed for every year.",
            "Status": "Done",
        },
        {
            "Requirement ID": "REQ-003",
            "Requirement": "The user shall be able to modify forecast revenue growth.",
            "Priority": "High",
            "Acceptance Criteria": "Sliders on the Forecast page update Revenue Growth per year.",
            "Status": "Done",
        },
        {
            "Requirement ID": "REQ-004",
            "Requirement": "The system shall calculate enterprise value using a DCF.",
            "Priority": "High",
            "Acceptance Criteria": "Enterprise Value = Sum of PV(FCF) + PV(Terminal Value).",
            "Status": "Done",
        },
        {
            "Requirement ID": "REQ-005",
            "Requirement": "The system shall display sensitivity analysis.",
            "Priority": "Medium",
            "Acceptance Criteria": "A WACC x Terminal Growth heatmap is shown on the Sensitivity page.",
            "Status": "Done",
        },
        {
            "Requirement ID": "REQ-006",
            "Requirement": "The system shall flag data quality anomalies.",
            "Priority": "Medium",
            "Acceptance Criteria": "Missing values, negative revenue, EBITDA > Revenue and WACC <= g are detected.",
            "Status": "Done",
        },
        {
            "Requirement ID": "REQ-007",
            "Requirement": "The system shall export financial summaries to CSV.",
            "Priority": "Low",
            "Acceptance Criteria": "Financial Summary, Forecast and Valuation Summary can each be downloaded as CSV.",
            "Status": "Done",
        },
        {
            "Requirement ID": "REQ-008",
            "Requirement": "The system shall reject a DCF calculation when WACC <= Terminal Growth.",
            "Priority": "High",
            "Acceptance Criteria": "An explicit error is shown and no Enterprise Value is computed.",
            "Status": "Done",
        },
    ]
)

with st.container(border=True):
    st.dataframe(requirements.set_index("Requirement ID"), use_container_width=True)
