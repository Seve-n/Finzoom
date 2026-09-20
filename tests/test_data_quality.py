"""Unit tests for src/data_quality.py (Arrange-Act-Assert pattern)."""

import pandas as pd

from src.data_quality import (
    check_ebitda_exceeds_revenue,
    check_missing_years,
    check_negative_revenue,
    check_wacc_vs_terminal_growth,
)


def test_check_negative_revenue_flags_negative_years():
    # Arrange
    df = pd.DataFrame({"Year": [2021, 2022], "Revenue": [1_000_000, -500_000]})

    # Act
    issues = check_negative_revenue(df)

    # Assert
    assert len(issues) == 1
    assert "2022" in issues[0]


def test_check_ebitda_exceeds_revenue_flags_impossible_years():
    # Arrange
    df = pd.DataFrame(
        {"Year": [2021, 2022], "Revenue": [1_000_000, 1_000_000], "EBITDA": [200_000, 1_500_000]}
    )

    # Act
    issues = check_ebitda_exceeds_revenue(df)

    # Assert
    assert len(issues) == 1
    assert "2022" in issues[0]


def test_check_missing_years_detects_gap_in_sequence():
    # Arrange
    df = pd.DataFrame({"Year": [2021, 2023]})

    # Act
    issues = check_missing_years(df)

    # Assert
    assert len(issues) == 1
    assert "2022" in issues[0]


def test_check_wacc_vs_terminal_growth_flags_invalid_combination():
    # Act
    issues = check_wacc_vs_terminal_growth(wacc=0.02, terminal_growth=0.025)

    # Assert
    assert len(issues) == 1


def test_check_wacc_vs_terminal_growth_passes_valid_combination():
    # Act
    issues = check_wacc_vs_terminal_growth(wacc=0.09, terminal_growth=0.025)

    # Assert
    assert issues == []
