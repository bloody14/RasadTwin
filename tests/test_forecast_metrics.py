"""Tests for forecasting metrics."""
import numpy as np

from rasadtwin.forecast.metrics import (
    empirical_coverage,
    interval_score,
    interval_width,
    mae,
    pinball_loss,
    wmape,
)


def test_wmape_zero_safe():
    # Both zero
    assert wmape(np.array([0, 0]), np.array([0, 0])) == 0.0
    # True zero, pred non-zero -> inf
    assert np.isinf(wmape(np.array([0, 0]), np.array([1, 1])))
    # Normal case: sum_true=10, err=2 => 0.2
    assert np.isclose(wmape(np.array([5, 5]), np.array([6, 4])), 0.2)


def test_mae():
    assert np.isclose(mae(np.array([10, 20]), np.array([12, 18])), 2.0)


def test_empirical_coverage():
    y_true = np.array([10, 20, 30, 40])
    lower = np.array([9, 21, 29, 39])  # 20 is missed (21 > 20)
    upper = np.array([11, 25, 31, 41])
    # 3 out of 4 covered
    assert np.isclose(empirical_coverage(y_true, lower, upper), 0.75)


def test_interval_width():
    lower = np.array([10, 20])
    upper = np.array([12, 24])
    # Widths: 2, 4 -> mean 3
    assert np.isclose(interval_width(lower, upper), 3.0)


def test_interval_score():
    y_true = np.array([10])
    lower = np.array([8])
    upper = np.array([12])
    # Perfect coverage, score is just width
    assert np.isclose(interval_score(y_true, lower, upper, alpha=0.1), 4.0)

    # Penalty case: true=6, lower=8, upper=12. width=4. low err=2. penalty=2 * (2/0.1) = 40. total=44.
    y_true_out = np.array([6])
    assert np.isclose(interval_score(y_true_out, lower, upper, alpha=0.1), 44.0)


def test_pinball_loss():
    y_true = np.array([10])
    y_pred = np.array([8])
    # error = 10 - 8 = 2
    # quantile 0.9. loss = max(0.9*2, -0.1*2) = 1.8
    assert np.isclose(pinball_loss(y_true, y_pred, 0.9), 1.8)
