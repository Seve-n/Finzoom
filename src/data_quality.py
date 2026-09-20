"""Data quality checks for the historical financials.

Each check returns a list of human-readable anomaly strings (an empty list
means no issue was found). Kept separate from calculations.py because this
is a validation concern, not a KPI concern.
"""

import pandas as pd


def check_missing_values(df: pd.DataFrame) -> list[str]:
    issues = []
    for column, count in df.isna().sum().items():
        if count > 0:
            issues.append(f"{count} missing value(s) in column '{column}'.")
    return issues


def check_negative_revenue(df: pd.DataFrame) -> list[str]:
    negative_years = df.loc[df["Revenue"] < 0, "Year"].tolist()
    return [f"Negative revenue in year {year}." for year in negative_years]


def check_ebitda_exceeds_revenue(df: pd.DataFrame) -> list[str]:
    bad_years = df.loc[df["EBITDA"] > df["Revenue"], "Year"].tolist()
    return [f"EBITDA exceeds Revenue in year {year}." for year in bad_years]


def check_missing_years(df: pd.DataFrame) -> list[str]:
    years = sorted(df["Year"].tolist())
    expected = list(range(years[0], years[-1] + 1))
    missing = [year for year in expected if year not in years]
    return [f"Missing year {year} in historical data." for year in missing]


def check_wacc_vs_terminal_growth(wacc: float, terminal_growth: float) -> list[str]:
    if wacc <= terminal_growth:
        return [
            f"WACC ({wacc:.1%}) must be greater than Terminal Growth ({terminal_growth:.1%})."
        ]
    return []


def run_all_checks(
    df: pd.DataFrame, wacc: float | None = None, terminal_growth: float | None = None
) -> list[str]:
    issues = []
    issues += check_missing_values(df)
    issues += check_negative_revenue(df)
    issues += check_ebitda_exceeds_revenue(df)
    issues += check_missing_years(df)
    if wacc is not None and terminal_growth is not None:
        issues += check_wacc_vs_terminal_growth(wacc, terminal_growth)
    return issues
