"""Unit tests for src/calculations.py (Arrange-Act-Assert pattern)."""

import pandas as pd
import pytest

from src.calculations import (
    add_ebitda_margin,
    add_fcf_margin,
    add_free_cash_flow,
    add_net_margin,
    add_revenue_growth,
    revenue_cagr,
)


@pytest.fixture
def sample_financials():
    return pd.DataFrame(
        {
            "Year": [2021, 2022],
            "Revenue": [8_000_000, 10_400_000],
            "EBITDA": [1_200_000, 1_872_000],
            "D_A": [280_000, 364_000],
            "EBIT": [920_000, 1_508_000],
            "Taxes": [230_000, 377_000],
            "Net_Income": [690_000, 1_131_000],
            "Capex": [360_000, 447_000],
            "Working_Capital_Change": [150_000, 180_000],
        }
    )


def test_revenue_growth_is_nan_for_first_year_and_correct_for_second(sample_financials):
    # Act
    result = add_revenue_growth(sample_financials)

    # Assert
    assert pd.isna(result["Revenue_Growth"].iloc[0])
    assert result["Revenue_Growth"].iloc[1] == pytest.approx(0.30, rel=1e-2)


def test_ebitda_margin_matches_expected_ratio(sample_financials):
    # Act
    result = add_ebitda_margin(sample_financials)

    # Assert
    assert result["EBITDA_Margin"].iloc[0] == pytest.approx(0.15, rel=1e-2)
    assert result["EBITDA_Margin"].iloc[1] == pytest.approx(0.18, rel=1e-2)


def test_net_margin_matches_expected_ratio(sample_financials):
    # Act
    result = add_net_margin(sample_financials)

    # Assert
    assert result["Net_Margin"].iloc[0] == pytest.approx(690_000 / 8_000_000)


def test_free_cash_flow_uses_effective_tax_rate_derived_from_data(sample_financials):
    # Act
    result = add_free_cash_flow(sample_financials)

    # Assert
    expected_fcf_2021 = 920_000 * (1 - 230_000 / 920_000) + 280_000 - 360_000 - 150_000
    assert result["Free_Cash_Flow"].iloc[0] == pytest.approx(expected_fcf_2021)


def test_fcf_margin_matches_free_cash_flow_over_revenue(sample_financials):
    # Arrange
    with_fcf = add_free_cash_flow(sample_financials)

    # Act
    result = add_fcf_margin(with_fcf)

    # Assert
    assert result["FCF_Margin"].iloc[0] == pytest.approx(
        result["Free_Cash_Flow"].iloc[0] / result["Revenue"].iloc[0]
    )


def test_revenue_cagr_between_first_and_last_year(sample_financials):
    # Act
    cagr = revenue_cagr(sample_financials)

    # Assert
    expected = (10_400_000 / 8_000_000) ** (1 / 1) - 1
    assert cagr == pytest.approx(expected)


def test_add_revenue_growth_does_not_mutate_input(sample_financials):
    # Act
    add_revenue_growth(sample_financials)

    # Assert
    assert "Revenue_Growth" not in sample_financials.columns
