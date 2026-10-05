"""Forecasting metrics implementation."""
from __future__ import annotations

import numpy as np


def wmape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Weighted Mean Absolute Percentage Error. Zero-safe."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    sum_true = np.sum(np.abs(y_true))
    if sum_true == 0:
        return 0.0 if np.all(y_pred == 0) else np.inf
    return float(np.sum(np.abs(y_true - y_pred)) / sum_true)


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error."""
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def empirical_coverage(y_true: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
    """Proportion of true values falling within the predicted interval."""
    y_true = np.asarray(y_true)
    lower = np.asarray(lower)
    upper = np.asarray(upper)
    covered = (y_true >= lower) & (y_true <= upper)
    return float(np.mean(covered))


def interval_width(lower: np.ndarray, upper: np.ndarray) -> float:
    """Mean width of the predicted intervals."""
    return float(np.mean(np.asarray(upper) - np.asarray(lower)))


def interval_score(y_true: np.ndarray, lower: np.ndarray, upper: np.ndarray, alpha: float) -> float:
    """Winkler Interval Score. Lower is better."""
    y_true = np.asarray(y_true)
    lower = np.asarray(lower)
    upper = np.asarray(upper)
    width = upper - lower
    penalty_low = (2 / alpha) * (lower - y_true) * (y_true < lower)
    penalty_high = (2 / alpha) * (y_true - upper) * (y_true > upper)
    return float(np.mean(width + penalty_low + penalty_high))


def pinball_loss(y_true: np.ndarray, y_pred: np.ndarray, quantile: float) -> float:
    """Pinball loss for a specific quantile."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    error = y_true - y_pred
    loss = np.maximum(quantile * error, (quantile - 1) * error)
    return float(np.mean(loss))
