"""Tests to guarantee no data leakage across forecasting splits."""
from datetime import date, timedelta

import numpy as np
import pandas as pd

from rasadtwin.forecast.features import create_horizon_features


def test_create_horizon_features_strict_lag():
    """Verify that horizon features do NOT contain information from the future.
    If predicting for date D with horizon H, the most recent data MUST be from D - H.
    """
    # Create fake daily demand for 1 item
    n_days = 100
    start = date(2021, 1, 1)
    df = pd.DataFrame({
        "date": [start + timedelta(days=i) for i in range(n_days)],
        "node_id": ["N1"] * n_days,
        "item": ["RATIONS"] * n_days,
        "demand_units": np.arange(n_days, dtype=float),
    })

    horizon = 7
    feat_df = create_horizon_features(df, horizon=horizon)

    # Check a specific row. E.g. date index 20 (demand=20)
    # The 'lag_7' for this date should be the demand from index 20-7=13
    row = feat_df[feat_df["demand_units"] == 20.0].iloc[0]
    assert row["lag_7"] == 13.0, "Leakage: lag_7 does not match true t-7 value"

    # The rolling mean at this date is computed on data ending at index 13.
    # Rolling mean 7 of [7,8,9,10,11,12,13] is 10.0
    assert row["rolling_mean_7_at_7"] == 10.0, "Leakage: rolling features access future data"
