"""KPI calculations for FinZoom.

Every function takes a DataFrame and returns a NEW DataFrame (no mutation of
the input), following the immutability principle: original data stays
untouched so callers can compare before/after or reuse the source frame.
"""

import pandas as pd


def add_revenue_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Year-over-year revenue growth: (Rev_t - Rev_t-1) / Rev_t-1."""
    result = df.copy()
    result["Revenue_Growth"] = result["Revenue"].pct_change()
    return result


def add_ebitda_margin(df: pd.DataFrame) -> pd.DataFrame:
    """EBITDA / Revenue."""
    result = df.copy()
    result["EBITDA_Margin"] = result["EBITDA"] / result["Revenue"]
    return result


def add_net_margin(df: pd.DataFrame) -> pd.DataFrame:
    """Net Income / Revenue."""
    result = df.copy()
    result["Net_Margin"] = result["Net_Income"] / result["Revenue"]
    return result


def add_free_cash_flow(df: pd.DataFrame) -> pd.DataFrame:
    """FCF = EBIT x (1 - effective tax rate) + D&A - Capex - Working Capital Change.

    The effective tax rate is derived per year from Taxes / EBIT in the data,
    rather than a hardcoded assumption, so FCF stays consistent with the
    Net_Income already reported for that year.
    """
    result = df.copy()
    effective_tax_rate = result["Taxes"] / result["EBIT"]
    nopat = result["EBIT"] * (1 - effective_tax_rate)
    result["Free_Cash_Flow"] = (
        nopat + result["D_A"] - result["Capex"] - result["Working_Capital_Change"]
    )
    return result


def add_fcf_margin(df: pd.DataFrame) -> pd.DataFrame:
    """Free Cash Flow / Revenue. Requires Free_Cash_Flow to already exist."""
    result = df.copy()
    result["FCF_Margin"] = result["Free_Cash_Flow"] / result["Revenue"]
    return result


def compute_all_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Apply every KPI calculation and return one enriched DataFrame."""
    result = add_revenue_growth(df)
    result = add_ebitda_margin(result)
    result = add_net_margin(result)
    result = add_free_cash_flow(result)
    result = add_fcf_margin(result)
    return result


def revenue_cagr(df: pd.DataFrame) -> float:
    """Compound Annual Growth Rate of revenue between the first and last year."""
    start_revenue = df["Revenue"].iloc[0]
    end_revenue = df["Revenue"].iloc[-1]
    n_years = df["Year"].iloc[-1] - df["Year"].iloc[0]
    return (end_revenue / start_revenue) ** (1 / n_years) - 1
