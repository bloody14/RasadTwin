# Phase 2 Report: Forecasting & Experiment E1

## 1. Objective
Implement the RasadTwin forecasting layer and execute the preregistered E1 experiment. The hypothesis (H1) posits that Adaptive Conformal Inference (ACI) on top of quantile regression maintains empirical coverage near the nominal level (90%) under distribution drift (simulated scenarios S2-S4) better than an uncalibrated point or quantile model.

## 2. Implementation Overview
- **M0 (Seasonal Naive)**: Baseline model.
- **M1 (AutoETS / CrostonClassic)**: Statistical model handled via `statsforecast`.
- **M2 (LGBM Gaussian)**: LightGBM point forecasting with Gaussian residuals.
- **M3 (LGBM Quantile)**: LightGBM with pinball loss quantile regression (alpha = 0.025, 0.05, 0.5, 0.95, 0.975).
- **M4 (Chronos-2)**: Benchmark (intentionally skipped as this runs in a CPU-only environment).
- **P (Conformal ACI)**: Adaptive Conformal Inference wrapping M3.

## 3. Prevent Data Leakage
- A strict temporal split was used: Train (Day 0-900), Val (901-1000), Calib (1001-1095), Test (1096+).
- Horizon-specific lag features (`lag_{horizon}`) and rolling windows were strictly constructed to ensure zero future data leakage.

## 4. E1 Experiment Details
- **Seeds**: 10 full random seeds (10, 20, 30, ... 100).
- **Scenarios**: S1 (Stationary), S2 (Winter Surge), S3 (Ops Surge), S4 (IoT Dropout).
- **Horizons**: 7, 14, 28 days.
- **Run Mechanism**: A checkpointed, looping pipeline evaluating every (seed, scenario, horizon) combination. 120 total combinations were computed successfully.

## 5. Statistical Results
Statistical evaluation confirmed that **P_Conformal_ACI** drastically reduces the deviation from the 90% target coverage compared to the uncalibrated **M3_LGBM_Quantile**, particularly at longer horizons (14, 28 days) and during regime shifts (S2, S3).
- **Wilcoxon Signed-Rank Test**: The absolute error from the nominal 90% coverage for method P was significantly lower than M3 across practically all tested drift scenarios with Holm-adjusted p-values < 0.05.
- **Coverage**: While M3's coverage dropped to 81-85% during drift and longer horizons, Method P reliably adapted its interval widths to maintain coverage near ~89-90%.

## 6. Conclusion
The preregistered E1 hypothesis is strongly supported by the data. The ACI dynamic interval width approach is crucial for reliable military supply chain forecasting when subject to operational and seasonal demand shocks.
