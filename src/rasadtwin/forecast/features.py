"""Feature generation for forecasting models."""
from __future__ import annotations

import pandas as pd


def load_and_merge_data(sim_dir: str) -> pd.DataFrame:
    """Load simulator Parquet outputs and merge into a single DataFrame."""
    demand = pd.read_parquet(f"{sim_dir}/demand.parquet")
    weather = pd.read_parquet(f"{sim_dir}/weather.parquet")
    nodes = pd.read_parquet(f"{sim_dir}/nodes.parquet")

    demand["date"] = pd.to_datetime(demand["date"])
    weather["date"] = pd.to_datetime(weather["date"])

    # Merge weather and nodes
    df = pd.merge(demand, weather, on=["date", "node_id"], how="left")
    df = pd.merge(df, nodes, on="node_id", how="left")

    df.sort_values(["node_id", "item", "date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def generate_features(df: pd.DataFrame, max_lag: int = 28) -> pd.DataFrame:
    """Generate lagged features to prevent temporal leakage.

    All historical demand features MUST be shifted by at least the forecast horizon
    during the pipeline generation. Here we just create basic lags and rolling stats.
    The pipeline will select the appropriate lag corresponding to the horizon.
    """
    df = df.copy()

    # Time features
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_year"] = df["date"].dt.dayofyear
    df["month"] = df["date"].dt.month
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    # Encode categorical
    if "tempo_state" in df.columns:
        tempo_map = {"normal": 0, "elevated": 1, "surge": 2}
        df["tempo_encoded"] = df["tempo_state"].map(tempo_map)

    # Note: We do NOT create lagged target features here because the required lag
    # depends on the horizon h. E.g., for horizon 7, lag 1 is illegal (it's future data).
    # Lags will be constructed dynamically per horizon in the pipeline.
    return df


def create_horizon_features(df: pd.DataFrame, horizon: int) -> pd.DataFrame:
    """Create horizon-specific lagged target features.
    
    If we are predicting y_{t+h} at time t, the most recent available observation is y_t.
    Thus, for the target at date D, the available history is at D - horizon.
    """
    df = df.copy()
    df.sort_values(["node_id", "item", "date"], inplace=True)

    # We want to predict target at 'date'. We can only use information up to 'date - horizon'.
    # Therefore, we shift the demand series grouped by node and item.
    group = df.groupby(["node_id", "item"])["demand_units"]

    df[f"lag_{horizon}"] = group.shift(horizon)
    df[f"lag_{horizon+7}"] = group.shift(horizon + 7)
    df[f"lag_{horizon+14}"] = group.shift(horizon + 14)

    # Rolling features over the available past
    df[f"rolling_mean_7_at_{horizon}"] = group.shift(horizon).rolling(7, min_periods=1).mean().reset_index(0, drop=True)
    df[f"rolling_mean_28_at_{horizon}"] = group.shift(horizon).rolling(28, min_periods=1).mean().reset_index(0, drop=True)
    df[f"rolling_std_7_at_{horizon}"] = group.shift(horizon).rolling(7, min_periods=1).std().reset_index(0, drop=True)

    # Drop rows where the base lag is NaN (can't train or predict)
    df.dropna(subset=[f"lag_{horizon}"], inplace=True)

    return df
