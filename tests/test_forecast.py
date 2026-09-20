"""Unit tests for src/forecast.py (Arrange-Act-Assert pattern)."""

import pandas as pd
import pytest

from src.forecast import build_forecast, historical_ratios


@pytest.fixture
def sample_historical():
    return pd.DataFrame(
        {
            "Year": [2023, 2024],
            "Revenue": [10_000_000, 12_000_000],
            "D_A": [400_000, 420_000],
            "EBIT": [2_000_000, 2_400_000],
            "Taxes": [500_000, 600_000],
            "Capex": [500_000, 480_000],
            "Working_Capital_Change": [200_000, 240_000],
        }
    )


def test_historical_ratios_are_averages_of_revenue_ratios(sample_historical):
    # Act
    ratios = historical_ratios(sample_historical)

    # Assert
    expected_effective_tax_rate = ((500_000 / 2_000_000) + (600_000 / 2_400_000)) / 2
    assert ratios["effective_tax_rate"] == pytest.approx(expected_effective_tax_rate)


def test_build_forecast_applies_compounding_revenue_growth(sample_historical):
    # Act
    forecast = build_forecast(
        sample_historical,
        forecast_years=[2025, 2026],
        revenue_growth_assumptions=[0.10, 0.10],
        ebitda_margin_assumptions=[0.20, 0.20],
    )

    # Assert
    assert forecast["Revenue"].iloc[0] == pytest.approx(12_000_000 * 1.10)
    assert forecast["Revenue"].iloc[1] == pytest.approx(12_000_000 * 1.10 * 1.10)


def test_build_forecast_ebitda_matches_margin_assumption(sample_historical):
    # Act
    forecast = build_forecast(
        sample_historical,
        forecast_years=[2025],
        revenue_growth_assumptions=[0.10],
        ebitda_margin_assumptions=[0.20],
    )

    # Assert
    assert forecast["EBITDA"].iloc[0] == pytest.approx(forecast["Revenue"].iloc[0] * 0.20)


def test_build_forecast_raises_on_mismatched_assumption_lengths(sample_historical):
    # Act / Assert
    with pytest.raises(ValueError):
        build_forecast(
            sample_historical,
            forecast_years=[2025, 2026],
            revenue_growth_assumptions=[0.10],
            ebitda_margin_assumptions=[0.20, 0.20],
        )
