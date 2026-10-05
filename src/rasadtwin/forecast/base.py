"""Forecasting base schemas and interfaces."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class ForecastRecord(BaseModel):
    date: str
    node_id: str
    item: str
    horizon: int
    model: str
    seed: int
    scenario: str
    y_true: float | None = None
    y_pred: float
    lower_90: float | None = None
    upper_90: float | None = None
    lower_95: float | None = None
    upper_95: float | None = None


class BaseForecaster(ABC):
    """Abstract base class for all forecasting models."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def fit(self, train_df: Any, val_df: Any | None = None) -> None:
        """Fit the model on training data."""
        pass

    @abstractmethod
    def calibrate(self, calib_df: Any) -> None:
        """Calibrate intervals on the calibration set."""
        pass

    @abstractmethod
    def predict(self, test_df: Any, horizon: int) -> Any:
        """Predict on the test set for a specific horizon.
        
        Returns a DataFrame with predictions and intervals.
        """
        pass
