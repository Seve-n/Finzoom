"""3-year forecast engine.

The user only adjusts Revenue Growth and EBITDA Margin per year (as
specified). Every other ratio (D&A, Capex, Working Capital, effective tax
rate) is held at its historical average as a percentage of revenue, so the
forecast stays grounded in the company's own historical data instead of
requiring the user to guess unrelated assumptions.
"""

import pandas as pd


def historical_ratios(historical: pd.DataFrame) -> dict:
    """Average historical ratios used as fixed assumptions in the forecast."""
    return {
        "da_pct_revenue": (historical["D_A"] / historical["Revenue"]).mean(),
        "capex_pct_revenue": (historical["Capex"] / historical["Revenue"]).mean(),
        "wc_pct_revenue": (historical["Working_Capital_Change"] / historical["Revenue"]).mean(),
        "effective_tax_rate": (historical["Taxes"] / historical["EBIT"]).mean(),
    }


def build_forecast(
    historical: pd.DataFrame,
    forecast_years: list[int],
    revenue_growth_assumptions: list[float],
    ebitda_margin_assumptions: list[float],
) -> pd.DataFrame:
    """Project Revenue, EBITDA, EBIT, Taxes, Net Income, D&A, Capex, Working
    Capital and Free Cash Flow for each forecast year.
    """
    if not (
        len(forecast_years)
        == len(revenue_growth_assumptions)
        == len(ebitda_margin_assumptions)
    ):
        raise ValueError(
            "forecast_years, revenue_growth_assumptions and "
            "ebitda_margin_assumptions must have the same length."
        )

    ratios = historical_ratios(historical)
    revenue = historical.sort_values("Year")["Revenue"].iloc[-1]

    rows = []
    for year, growth, margin in zip(
        forecast_years, revenue_growth_assumptions, ebitda_margin_assumptions
    ):
        revenue = revenue * (1 + growth)
        ebitda = revenue * margin
        d_a = revenue * ratios["da_pct_revenue"]
        ebit = ebitda - d_a
        taxes = ebit * ratios["effective_tax_rate"]
        net_income = ebit - taxes
        capex = revenue * ratios["capex_pct_revenue"]
        wc_change = revenue * ratios["wc_pct_revenue"]
        fcf = ebit * (1 - ratios["effective_tax_rate"]) + d_a - capex - wc_change

        rows.append(
            {
                "Year": year,
                "Revenue": revenue,
                "Revenue_Growth": growth,
                "EBITDA": ebitda,
                "EBITDA_Margin": margin,
                "D_A": d_a,
                "EBIT": ebit,
                "Taxes": taxes,
                "Net_Income": net_income,
                "Capex": capex,
                "Working_Capital_Change": wc_change,
                "Free_Cash_Flow": fcf,
            }
        )

    return pd.DataFrame(rows)
