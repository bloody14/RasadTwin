# Phase 2 Plan: Demand Forecasting and E1 Experiment

## 1. Files to Create/Change
- `docs/plans/P2_plan.md` (this file)
- `docs/PREREG.md` (Update with E1 details)
- `src/rasadtwin/forecast/`
  - `__init__.py`
  - `base.py` (Common forecasting interface)
  - `features.py` (Causal feature generation, strict temporal isolation)
  - `naive.py` (M0: Seasonal naive)
  - `ets.py` (M1: AutoETS / Croston / SBA for intermittency via `statsforecast`)
  - `lightgbm_models.py` (M2: LGBM Point + Gaussian; M3: LGBM Quantile uncalibrated)
  - `conformal.py` (P: LGBM Quantile + Split Conformal Calibration + ACI)
  - `metrics.py` (wMAPE, MAE, coverage, width, score, pinball loss)
  - `pipeline.py` (Execution pipeline tying data to models)
- `tests/`
  - `test_forecast_metrics.py`
  - `test_forecast_leakage.py`
  - `test_forecast_features.py`
- `experiments/e1_forecast/run.py`
- `reports/PHASE_2_REPORT.md`
- `reports/P2_CTO_REVIEW_PACKET.md`
- `pyproject.toml` (Add dependencies: `lightgbm`, `statsforecast`, `scipy`, `statsmodels`)

## 2. Forecasting Architecture
- Ingest Parquet data output from `rasadtwin.sim`.
- Generate features chronologically. Lags, rolling statistics, calendar, altitude, troops.
- Fit models strictly on Training data.

## 3. Temporal Splits
- Total Simulator Days: 1095 (History) + 365 (Test) = 1460 days.
- Split design:
  - **TRAIN**: Days 0 to 900
  - **VALIDATION**: Days 901 to 1000
  - **CALIBRATION**: Days 1001 to 1095 (Disjoint from Train/Val, used ONLY for residual estimation and conformal bounds).
  - **TEST**: Days 1096 to 1460 (Held-out).

## 4. Models
- **M0**: Seasonal Naive (7-day season).
- **M1**: AutoETS (statsforecast) + SBA/Croston for intermittent (using zero-demand ratio logic).
- **M2**: LightGBM Point + Gaussian residuals calculated on Calibration.
- **M3**: LightGBM Quantile (alpha=0.05, 0.95), uncalibrated.
- **M4**: Chronos-2 zero-shot benchmark (OPTIONAL, skipped if unavailable/impractical on CPU).
- **P**: LightGBM Quantile + Split Conformal Calibration + Adaptive Conformal Inference (ACI) updated sequentially through Test.

## 5. Conformal Methodology
- Split conformal: Fit bounds on Calibration set residuals.
- ACI: Adjust calibration offset dynamically on Test set based on past coverage miscalibration. 

## 6. Metrics
- Point: wMAPE (zero-safe), MAE.
- Interval: Empirical coverage (@90%), Interval width, Interval score, Pinball loss.

## 7. Experiment Design
- Predict horizons $h \in \{7, 14, 28\}$.
- Evaluate over 10 world seeds (full E1) across S1, S2, S3, S4 scenarios.
- Statistical significance: Wilcoxon signed-rank + Holm correction for paired method differences. Bootstrap 95% CIs.

## 8. Leakage Controls
- `features.py` prevents future information by using strict lagging.
- `pipeline.py` enforces index separation between train/val/calib/test. 

## 9. Quick Mode
- `--quick`: 2 seeds, shorter horizon, fast estimators to validate mechanics.

## 10. Reproducibility
- Parquet outputs preserving metadata (seed, commit, config hash).

## 11. Risks
- M1 (AutoETS) might be slow on many TS; will utilize `statsforecast` for speed.
- M4 (Chronos-2) requires heavy CPU resources; explicitly designated as optional/skipped.
