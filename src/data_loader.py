"""Load and validate FinZoom historical financial data."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "Year",
    "Revenue",
    "COGS",
    "Operating_Expenses",
    "EBITDA",
    "D_A",
    "EBIT",
    "Taxes",
    "Net_Income",
    "Capex",
    "Working_Capital_Change",
]


def load_financials(path: str | Path) -> pd.DataFrame:
    """Load historical financials from CSV, sorted by year."""
    df = pd.read_csv(path)

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return df.sort_values("Year").reset_index(drop=True)
