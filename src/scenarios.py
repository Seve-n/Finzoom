"""Downside / Base / Upside scenarios: the same forecast + DCF engine applied
to three pre-defined assumption sets, presented side by side. No scenario is
labelled as "better" - only the resulting numbers are shown.
"""

import pandas as pd

from src.forecast import build_forecast
from src.valuation import run_dcf

SCENARIOS = {
    "Downside": {"revenue_growth": 0.10, "ebitda_margin": 0.18},
    "Base": {"revenue_growth": 0.18, "ebitda_margin": 0.22},
    "Upside": {"revenue_growth": 0.25, "ebitda_margin": 0.26},
}


def run_scenarios(
    historical: pd.DataFrame,
    forecast_years: list[int],
    wacc: float,
    terminal_growth: float,
    scenarios: dict = SCENARIOS,
) -> pd.DataFrame:
    """Return Revenue, EBITDA, FCF (final forecast year) and Enterprise Value
    for each scenario, side by side.
    """
    n_years = len(forecast_years)
    rows = []
    for name, assumptions in scenarios.items():
        forecast = build_forecast(
            historical,
            forecast_years,
            [assumptions["revenue_growth"]] * n_years,
            [assumptions["ebitda_margin"]] * n_years,
        )
        dcf = run_dcf(forecast["Free_Cash_Flow"], wacc, terminal_growth)
        rows.append(
            {
                "Scenario": name,
                "Revenue_Growth": assumptions["revenue_growth"],
                "EBITDA_Margin": assumptions["ebitda_margin"],
                "Final_Year_Revenue": forecast["Revenue"].iloc[-1],
                "Final_Year_EBITDA": forecast["EBITDA"].iloc[-1],
                "Final_Year_FCF": forecast["Free_Cash_Flow"].iloc[-1],
                "Enterprise_Value": dcf["enterprise_value"],
            }
        )
    return pd.DataFrame(rows)
