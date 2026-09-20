"""Simple DCF valuation: discounting, terminal value, enterprise value,
equity value, and sensitivity helpers.
"""

import numpy as np
import pandas as pd

from src.forecast import build_forecast


def discount_factor(wacc: float, t: int) -> float:
    """1 / (1 + WACC)^t"""
    return 1 / (1 + wacc) ** t


def terminal_value(final_fcf: float, wacc: float, terminal_growth: float) -> float:
    """FCF x (1 + g) / (WACC - g). Raises if WACC <= terminal growth."""
    if wacc <= terminal_growth:
        raise ValueError(
            "WACC must be strictly greater than Terminal Growth to compute a Terminal Value."
        )
    return final_fcf * (1 + terminal_growth) / (wacc - terminal_growth)


def run_dcf(fcf_by_year: pd.Series, wacc: float, terminal_growth: float) -> dict:
    """Run the full DCF step by step and return every intermediate value.

    fcf_by_year must be in chronological order: year 1, year 2, ..., year n.
    """
    if wacc <= terminal_growth:
        raise ValueError("WACC must be strictly greater than Terminal Growth.")

    periods = list(range(1, len(fcf_by_year) + 1))
    discount_factors = [discount_factor(wacc, t) for t in periods]
    pv_fcf = [fcf * df for fcf, df in zip(fcf_by_year, discount_factors)]

    tv = terminal_value(fcf_by_year.iloc[-1], wacc, terminal_growth)
    pv_tv = tv * discount_factors[-1]

    enterprise_value = sum(pv_fcf) + pv_tv

    return {
        "years": periods,
        "fcf": list(fcf_by_year),
        "discount_factors": discount_factors,
        "pv_fcf": pv_fcf,
        "terminal_value": tv,
        "pv_terminal_value": pv_tv,
        "enterprise_value": enterprise_value,
    }


def equity_value(enterprise_value: float, cash: float, debt: float) -> float:
    """Enterprise Value + Cash - Debt"""
    return enterprise_value + cash - debt


def sensitivity_wacc_growth(
    fcf_by_year: pd.Series, wacc_range: list[float], growth_range: list[float]
) -> pd.DataFrame:
    """Enterprise Value for every WACC x Terminal Growth combination.
    Invalid combinations (WACC <= growth) are left as NaN.
    """
    table = pd.DataFrame(
        index=[f"{w:.1%}" for w in wacc_range],
        columns=[f"{g:.1%}" for g in growth_range],
        dtype=float,
    )
    for wacc in wacc_range:
        for growth in growth_range:
            if wacc <= growth:
                table.loc[f"{wacc:.1%}", f"{growth:.1%}"] = np.nan
            else:
                ev = run_dcf(fcf_by_year, wacc, growth)["enterprise_value"]
                table.loc[f"{wacc:.1%}", f"{growth:.1%}"] = ev
    return table


def sensitivity_growth_margin(
    historical: pd.DataFrame,
    forecast_years: list[int],
    growth_range: list[float],
    margin_range: list[float],
    wacc: float,
    terminal_growth: float,
) -> pd.DataFrame:
    """Enterprise Value for combinations of a flat Revenue Growth and EBITDA
    Margin applied across the whole forecast period.
    """
    table = pd.DataFrame(
        index=[f"{g:.0%}" for g in growth_range],
        columns=[f"{m:.0%}" for m in margin_range],
        dtype=float,
    )
    n_years = len(forecast_years)
    for growth in growth_range:
        for margin in margin_range:
            forecast = build_forecast(
                historical, forecast_years, [growth] * n_years, [margin] * n_years
            )
            ev = run_dcf(forecast["Free_Cash_Flow"], wacc, terminal_growth)["enterprise_value"]
            table.loc[f"{growth:.0%}", f"{margin:.0%}"] = ev
    return table
