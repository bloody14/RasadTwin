# RasadTwin Experiment Preregistration

## Experiment E1: Demand Forecasting under Distribution Drift

### Hypothesis
**H1:** Adaptive conformal intervals keep coverage near nominal under drift better than uncalibrated intervals.

### Scenarios
- S1: stationary
- S2: winter_surge
- S3: sudden_operational_surge
- S4: iot_dropout

### Horizons
7, 14, and 28 days.

### Models
- **M0**: Seasonal naive.
- **M1**: AutoETS + Croston/SBA for intermittent demand.
- **M2**: LightGBM point forecast + Gaussian residual intervals.
- **M3**: LightGBM quantile regression, uncalibrated.
- **M4**: Chronos-2 zero-shot benchmark on a small CPU-feasible subset only (OPTIONAL).
- **P**: LightGBM quantile regression + split conformal calibration + Adaptive Conformal Inference (ACI).

### Primary Registered Metrics
- Empirical coverage @90%
- Empirical coverage @95%
- Interval width
- Interval score
- Pinball loss
- wMAPE
- MAE

### Seed Requirement
At least 10 world seeds.

### Experimental Controls

#### Temporal Ordering
Strict chronological splitting:
`TRAIN < VALIDATION < CALIBRATION < TEST`
- **Train**: Day 0 - 900
- **Validation**: Day 901 - 1000 (used for tuning/early stopping)
- **Calibration**: Day 1001 - 1095 (used strictly for residual/conformal calibration)
- **Test**: Day 1096 - 1460 (held-out evaluation)

#### Calibration Separation
The calibration window is strictly separated from training. No model parameters are trained on the calibration window.

#### Held-out Test Protection
No tuning of hyperparameters, threshold boundaries, or ACI learning rates occurs on the test window. Test data is solely for final metric generation.

#### Aggregation Rule
Results are paired and aggregated across the 10 seeds, grouping by scenario, horizon, and model.

#### Missing-Data Handling
If a scenario runs into execution failure for a specific seed, the failure will be logged, and the seed will be skipped for that specific method/scenario. No silent replacement of seeds. S4 (iot_dropout) missing data is handled via forward filling or similar lagged imputation on the features side.

#### Intermittent-Demand Handling
Items with > 30% zero-demand days in the training set are treated as intermittent (e.g. Spares), triggering SBA/Croston logic in M1.

### Decision Rule
- **Supported**: Method P maintains median empirical coverage closer to the nominal level (90%) across drift scenarios (S2, S3) compared to M3, with statistical significance (p < 0.05).
- **Not Supported**: Method P fails to maintain coverage closer to nominal than M3, or the interval widths expand trivially (e.g. infinite width).
- **Inconclusive**: Results show no statistically significant difference between P and M3.

### Statistics Framework
- **Comparison**: Paired comparisons on matched (seed, scenario, horizon, node, item) instances.
- **Tests**: Wilcoxon signed-rank test.
- **Correction**: Holm correction for multiple comparisons.
- **Effect Size**: Median paired difference.
- **Confidence**: Bootstrap 95% Confidence Intervals.
