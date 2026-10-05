"""P: Proposed Conformal Method (Quantile + Split + ACI)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from rasadtwin.forecast.lightgbm_models import LGBMQuantile


class ConformalACI(LGBMQuantile):
    """P: LightGBM Quantile regression with Split Conformal Calibration and ACI."""

    def __init__(self, name: str = "P_Conformal_ACI", lr: float = 0.05):
        super().__init__(name)
        self.lr = lr
        self.split_offset_90 = 0.0
        self.split_offset_95 = 0.0
        self.aci_alpha_90 = 0.10
        self.aci_alpha_95 = 0.05

    def calibrate(self, calib_df: pd.DataFrame) -> None:
        """Split Conformal calibration on held-out calib set."""
        if len(calib_df) == 0:
            return

        X_cal = calib_df[self.features]
        y_cal = calib_df["demand_units"].values

        # 90%
        low90 = self.model_low90.predict(X_cal)
        high90 = self.model_high90.predict(X_cal)
        scores_90 = np.maximum(low90 - y_cal, y_cal - high90)
        q_90 = np.quantile(scores_90, min(1.0, (1.0 + 1.0/len(y_cal)) * 0.90))
        self.split_offset_90 = max(0.0, q_90)

        # 95%
        low95 = self.model_low95.predict(X_cal)
        high95 = self.model_high95.predict(X_cal)
        scores_95 = np.maximum(low95 - y_cal, y_cal - high95)
        q_95 = np.quantile(scores_95, min(1.0, (1.0 + 1.0/len(y_cal)) * 0.95))
        self.split_offset_95 = max(0.0, q_95)

    def predict(self, test_df: pd.DataFrame, horizon: int) -> pd.DataFrame:
        """Predict sequentially to allow ACI updates.
        
        ACI updates the target alpha based on previous coverage.
        Since we predict for horizon h, we only know if we covered the true value
        after h days have passed. We'll group test_df by date, and sequentially 
        update the offsets.
        """
        preds = test_df.copy()
        preds.sort_values("date", inplace=True)

        dates = preds["date"].unique()

        y_preds = []
        l90, u90 = [], []
        l95, u95 = [], []

        # Track historical predictions and truth for ACI
        # In a real streaming setting, we'd only have ground truth for date - horizon.
        # So we look back 'horizon' days to compute coverage error.

        # Current ACI offsets start at split conformal
        curr_offset_90 = self.split_offset_90
        curr_offset_95 = self.split_offset_95

        date_to_coverage = {}

        for d in dates:
            # ACI update step: evaluate coverage at d - horizon
            past_d = d - pd.Timedelta(days=horizon)
            if past_d in date_to_coverage:
                past_cov_90, past_cov_95 = date_to_coverage[past_d]
                # ACI update rule: alpha_t+1 = alpha_t + lr * (error_t - alpha)
                # If coverage is lower than 90%, err > 0.1, alpha decreases, intervals widen.
                err_90 = 1.0 - past_cov_90
                self.aci_alpha_90 = self.aci_alpha_90 + self.lr * (0.10 - err_90)

                err_95 = 1.0 - past_cov_95
                self.aci_alpha_95 = self.aci_alpha_95 + self.lr * (0.05 - err_95)

                # Modulate the offset based on the ratio of target alpha to actual ACI alpha
                curr_offset_90 = self.split_offset_90 * (0.10 / max(0.01, self.aci_alpha_90))
                curr_offset_95 = self.split_offset_95 * (0.05 / max(0.01, self.aci_alpha_95))

            day_df = preds[preds["date"] == d]
            X_test = day_df[self.features]

            p_mid = np.maximum(0, self.model_mid.predict(X_test))
            p_l90 = np.maximum(0, self.model_low90.predict(X_test) - curr_offset_90)
            p_u90 = np.maximum(0, self.model_high90.predict(X_test) + curr_offset_90)
            p_l95 = np.maximum(0, self.model_low95.predict(X_test) - curr_offset_95)
            p_u95 = np.maximum(0, self.model_high95.predict(X_test) + curr_offset_95)

            y_preds.extend(p_mid)
            l90.extend(p_l90)
            u90.extend(p_u90)
            l95.extend(p_l95)
            u95.extend(p_u95)

            # Record actual coverage for this day to use it `horizon` days later
            y_true = day_df["demand_units"].values
            c90 = np.mean((y_true >= p_l90) & (y_true <= p_u90))
            c95 = np.mean((y_true >= p_l95) & (y_true <= p_u95))
            date_to_coverage[d] = (c90, c95)

        preds["y_pred"] = y_preds
        preds["lower_90"] = np.minimum(l90, preds["y_pred"])
        preds["upper_90"] = np.maximum(u90, preds["y_pred"])
        preds["lower_95"] = np.minimum(l95, preds["y_pred"])
        preds["upper_95"] = np.maximum(u95, preds["y_pred"])

        return preds
