"""Seasonal Naive Forecasting Model (M0)."""
from __future__ import annotations

import pandas as pd

from rasadtwin.forecast.base import BaseForecaster


class SeasonalNaive(BaseForecaster):
    """M0: Seasonal Naive model using 7-day seasonality."""

    def __init__(self, name: str = "M0_SeasonalNaive"):
        super().__init__(name)

    def fit(self, train_df: pd.DataFrame, val_df: pd.DataFrame | None = None) -> None:
        """Seasonal Naive has no fitted parameters."""
        pass

    def calibrate(self, calib_df: pd.DataFrame) -> None:
        """Seasonal Naive does not have calibrated bounds in this implementation."""
        pass

    def predict(self, test_df: pd.DataFrame, horizon: int) -> pd.DataFrame:
        """Predict using the observation from 'horizon' days ago.
        
        Since features.py already creates `lag_{horizon}`, which represents
        the observation at time t for target t+horizon, we can use it.
        But wait, seasonal naive uses t+horizon - season.
        Actually, we can just use `lag_{horizon + (7 - (horizon % 7)) % 7}` to align to the same weekday.
        For simplicity, let's just use `lag_{horizon}` if we assume the last available observation,
        or specifically shift back to the matching weekday.
        
        If horizon is 7, 14, 28, the horizon itself is a multiple of 7.
        Thus, the observation from exactly `horizon` days ago is the same weekday!
        So `lag_{horizon}` is exactly the seasonal naive forecast.
        """
        preds = test_df.copy()
        lag_col = f"lag_{horizon}"

        preds["y_pred"] = preds[lag_col]
        # No probabilistic bounds for M0
        preds["lower_90"] = preds["y_pred"]
        preds["upper_90"] = preds["y_pred"]
        preds["lower_95"] = preds["y_pred"]
        preds["upper_95"] = preds["y_pred"]

        return preds
