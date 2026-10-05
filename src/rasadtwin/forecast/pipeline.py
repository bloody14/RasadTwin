"""Forecasting execution pipeline."""
from __future__ import annotations

import pandas as pd

from rasadtwin.forecast.base import BaseForecaster
from rasadtwin.forecast.features import create_horizon_features


def run_pipeline(
    df: pd.DataFrame,
    models: list[BaseForecaster],
    horizon: int,
    seed: int,
    scenario: str,
) -> list[pd.DataFrame]:
    """Execute the full forecasting pipeline securely.
    
    TRAIN: Day 0 to 900
    VAL: Day 901 to 1000
    CAL: Day 1001 to 1095
    TEST: Day 1096 to max
    """
    df = df.copy()

    # 1. Generate causal lag features SPECIFIC to this horizon
    # If horizon=7, lag_7 is the most recent data point available.
    # This completely eliminates leakage.
    df = create_horizon_features(df, horizon)

    # Calculate relative days for splitting
    min_date = df["date"].min()
    df["day_idx"] = (df["date"] - min_date).dt.days

    train_df = df[df["day_idx"] <= 900]
    val_df = df[(df["day_idx"] > 900) & (df["day_idx"] <= 1000)]
    cal_df = df[(df["day_idx"] > 1000) & (df["day_idx"] <= 1095)]
    test_df = df[df["day_idx"] > 1095]

    if len(train_df) == 0 or len(test_df) == 0:
        return []

    results = []
    for model in models:
        # Fit
        model.fit(train_df, val_df)

        # Calibrate
        model.calibrate(cal_df)

        # Predict
        preds = model.predict(test_df, horizon)

        # Format output matching ForecastRecord schema
        out = preds[["date", "node_id", "item", "demand_units"]].copy()
        out.rename(columns={"demand_units": "y_true"}, inplace=True)
        out["date"] = out["date"].dt.strftime("%Y-%m-%d")
        out["horizon"] = horizon
        out["model"] = model.name
        out["seed"] = seed
        out["scenario"] = scenario

        out["y_pred"] = preds["y_pred"]
        out["lower_90"] = preds["lower_90"]
        out["upper_90"] = preds["upper_90"]
        out["lower_95"] = preds.get("lower_95", preds["lower_90"])
        out["upper_95"] = preds.get("upper_95", preds["upper_90"])

        results.append(out)

    return results
