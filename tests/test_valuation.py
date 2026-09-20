"""Unit tests for src/valuation.py (Arrange-Act-Assert pattern)."""

import pandas as pd
import pytest

from src.valuation import discount_factor, equity_value, run_dcf, terminal_value


def test_discount_factor_matches_formula():
    # Act
    result = discount_factor(wacc=0.10, t=2)

    # Assert
    assert result == pytest.approx(1 / (1.10**2))


def test_terminal_value_matches_gordon_growth_formula():
    # Act
    result = terminal_value(final_fcf=1_000_000, wacc=0.09, terminal_growth=0.025)

    # Assert
    assert result == pytest.approx(1_000_000 * 1.025 / (0.09 - 0.025))


def test_terminal_value_raises_when_wacc_not_above_terminal_growth():
    # Act / Assert
    with pytest.raises(ValueError):
        terminal_value(final_fcf=1_000_000, wacc=0.02, terminal_growth=0.025)


def test_run_dcf_raises_when_wacc_not_above_terminal_growth():
    # Arrange
    fcf = pd.Series([1_000_000, 1_100_000, 1_200_000])

    # Act / Assert
    with pytest.raises(ValueError):
        run_dcf(fcf, wacc=0.02, terminal_growth=0.025)


def test_run_dcf_enterprise_value_equals_sum_of_pv_fcf_and_pv_terminal_value():
    # Arrange
    fcf = pd.Series([1_000_000, 1_100_000, 1_200_000])

    # Act
    result = run_dcf(fcf, wacc=0.09, terminal_growth=0.025)

    # Assert
    assert result["enterprise_value"] == pytest.approx(
        sum(result["pv_fcf"]) + result["pv_terminal_value"]
    )


def test_run_dcf_discount_factors_decrease_over_time():
    # Arrange
    fcf = pd.Series([1_000_000, 1_100_000, 1_200_000])

    # Act
    result = run_dcf(fcf, wacc=0.09, terminal_growth=0.025)

    # Assert
    assert result["discount_factors"][0] > result["discount_factors"][1] > result["discount_factors"][2]


def test_equity_value_adds_cash_and_subtracts_debt():
    # Act
    result = equity_value(enterprise_value=10_000_000, cash=1_000_000, debt=2_000_000)

    # Assert
    assert result == 9_000_000
