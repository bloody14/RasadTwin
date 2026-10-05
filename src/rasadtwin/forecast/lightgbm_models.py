"""M2 and M3: LightGBM based forecasting models."""
from __future__ import annotations

import lightgbm as lgb
import numpy as np
import pandas as pd
from scipy.stats import norm

from rasadtwin.forecast.base import BaseForecaster


class LGBMPointGaussian(BaseForecaster):
    """M2: LightGBM point forecast with Gaussian residual intervals."""

    def __init__(self, name: str = "M2_LGBM_Gaussian"):
        super().__init__(name)
        self.model = lgb.LGBMRegressor(
            n_estimators=100, learning_rate=0.1, random_state=42, verbose=-1,
        )
        self.features = []
        self.std_dev = 0.0

    def fit(self, train_df: pd.DataFrame, val_df: pd.DataFrame | None = None) -> None:
        self.features = [c for c in train_df.columns if c not in [
            "date", "node_id", "item", "demand_units", "unique_id", "tempo_state", "node_type"
        ]]

        X_train = train_df[self.features]
        y_train = train_df["demand_units"]

        if val_df is not None:
            X_val = val_df[self.features]
            y_val = val_df["demand_units"]
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_val, y_val)],
                callbacks=[lgb.early_stopping(10, verbose=False)],
            )
        else:
            self.model.fit(X_train, y_train)

    def calibrate(self, calib_df: pd.DataFrame) -> None:
        X_cal = calib_df[self.features]
        y_cal = calib_df["demand_units"]
        preds = self.model.predict(X_cal)
        residuals = y_cal - preds
        self.std_dev = float(np.std(residuals))

    def predict(self, test_df: pd.DataFrame, horizon: int) -> pd.DataFrame:
        preds = test_df.copy()
        X_test = preds[self.features]
        preds["y_pred"] = np.maximum(0, self.model.predict(X_test))

        z_90 = norm.ppf(0.95)
        z_95 = norm.ppf(0.975)

        preds["lower_90"] = np.maximum(0, preds["y_pred"] - z_90 * self.std_dev)
        preds["upper_90"] = preds["y_pred"] + z_90 * self.std_dev

        preds["lower_95"] = np.maximum(0, preds["y_pred"] - z_95 * self.std_dev)
        preds["upper_95"] = preds["y_pred"] + z_95 * self.std_dev

        return preds


class LGBMQuantile(BaseForecaster):
    """M3: LightGBM quantile regression, uncalibrated."""

    def __init__(self, name: str = "M3_LGBM_Quantile"):
        super().__init__(name)
        self.model_mid = lgb.LGBMRegressor(objective="quantile", alpha=0.5, random_state=42, verbose=-1)
        self.model_low90 = lgb.LGBMRegressor(objective="quantile", alpha=0.05, random_state=42, verbose=-1)
        self.model_high90 = lgb.LGBMRegressor(objective="quantile", alpha=0.95, random_state=42, verbose=-1)
        self.model_low95 = lgb.LGBMRegressor(objective="quantile", alpha=0.025, random_state=42, verbose=-1)
        self.model_high95 = lgb.LGBMRegressor(objective="quantile", alpha=0.975, random_state=42, verbose=-1)
        self.features = []

    def fit(self, train_df: pd.DataFrame, val_df: pd.DataFrame | None = None) -> None:
        self.features = [c for c in train_df.columns if c not in [
            "date", "node_id", "item", "demand_units", "unique_id", "tempo_state", "node_type"
        ]]
        X_train = train_df[self.features]
        y_train = train_df["demand_units"]

        self.model_mid.fit(X_train, y_train)
        self.model_low90.fit(X_train, y_train)
        self.model_high90.fit(X_train, y_train)
        self.model_low95.fit(X_train, y_train)
        self.model_high95.fit(X_train, y_train)

    def calibrate(self, calib_df: pd.DataFrame) -> None:
        pass

    def predict(self, test_df: pd.DataFrame, horizon: int) -> pd.DataFrame:
        preds = test_df.copy()
        X_test = preds[self.features]

        preds["y_pred"] = np.maximum(0, self.model_mid.predict(X_test))
        preds["lower_90"] = np.maximum(0, self.model_low90.predict(X_test))
        preds["upper_90"] = np.maximum(0, self.model_high90.predict(X_test))
        preds["lower_95"] = np.maximum(0, self.model_low95.predict(X_test))
        preds["upper_95"] = np.maximum(0, self.model_high95.predict(X_test))

        # Enforce ordering
        preds["lower_90"] = np.minimum(preds["lower_90"], preds["y_pred"])
        preds["upper_90"] = np.maximum(preds["upper_90"], preds["y_pred"])

        return preds
