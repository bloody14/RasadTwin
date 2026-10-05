"""Statistical analysis of E1 experiment results."""
from __future__ import annotations

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

from rasadtwin.forecast.metrics import (
    wmape, mae, empirical_coverage, interval_width, interval_score, pinball_loss
)


def compute_metrics_for_group(group: pd.DataFrame) -> pd.Series:
    """Compute all required metrics for a specific seed/scenario/horizon/model."""
    y_true = group["y_true"].values
    y_pred = group["y_pred"].values
    l90 = group["lower_90"].values
    u90 = group["upper_90"].values
    l95 = group["lower_95"].values
    u95 = group["upper_95"].values
    
    m_wmape = wmape(y_true, y_pred)
    m_mae = mae(y_true, y_pred)
    
    cov90 = empirical_coverage(y_true, l90, u90)
    cov95 = empirical_coverage(y_true, l95, u95)
    
    wid90 = interval_width(l90, u90)
    wid95 = interval_width(l95, u95)
    
    score90 = interval_score(y_true, l90, u90, alpha=0.10)
    score95 = interval_score(y_true, l95, u95, alpha=0.05)
    
    pb90 = pinball_loss(y_true, l90, 0.05) + pinball_loss(y_true, u90, 0.95)
    
    return pd.Series({
        "wmape": m_wmape,
        "mae": m_mae,
        "coverage_90": cov90,
        "coverage_95": cov95,
        "width_90": wid90,
        "width_95": wid95,
        "score_90": score90,
        "score_95": score95,
        "pinball_90": pb90,
    })


def compute_bootstrap_ci(data: np.ndarray, n_bootstraps: int = 1000) -> tuple[float, float]:
    """Compute 95% bootstrap CI for the median."""
    if len(data) == 0:
        return (np.nan, np.nan)
    medians = []
    for _ in range(n_bootstraps):
        sample = np.random.choice(data, size=len(data), replace=True)
        medians.append(np.median(sample))
    return float(np.percentile(medians, 2.5)), float(np.percentile(medians, 97.5))


def run_analysis(quick: bool = False):
    """Aggregate raw outputs into tables and run statistical tests."""
    out_dir = Path("results/tables")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    raw_file = Path("results/raw/e1_forecast") / ("quick_results.parquet" if quick else "full_results.parquet")
    if not raw_file.exists():
        print("Raw results not found.")
        return
        
    df = pd.read_parquet(raw_file)
    
    # 1. Compute metrics per (seed, scenario, horizon, model)
    groups = df.groupby(["seed", "scenario", "horizon", "model"])
    metrics_df = groups.apply(compute_metrics_for_group).reset_index()
    metrics_df.to_csv(out_dir / "all_metrics.csv", index=False)
    
    # 2. Aggregate across seeds (median, IQR)
    agg_funcs = {
        "wmape": ["median", lambda x: np.percentile(x, 75) - np.percentile(x, 25)],
        "mae": ["median", lambda x: np.percentile(x, 75) - np.percentile(x, 25)],
        "coverage_90": ["median", lambda x: np.percentile(x, 75) - np.percentile(x, 25)],
        "width_90": ["median", lambda x: np.percentile(x, 75) - np.percentile(x, 25)],
        "score_90": ["median", lambda x: np.percentile(x, 75) - np.percentile(x, 25)],
    }
    
    summary = metrics_df.groupby(["scenario", "horizon", "model"]).agg(agg_funcs)
    # Rename columns manually since it's a multiindex
    summary.columns = [f"{col[0]}_{'median' if col[1] == 'median' else 'iqr'}" for col in summary.columns]
    summary.reset_index(inplace=True)
    summary.to_csv(out_dir / "summary_metrics.csv", index=False)
    
    # 3. Statistical Testing (Method P vs Method M3 - uncalibrated quantile)
    # H1: P keeps coverage near nominal under drift better than M3.
    # We will test the absolute error of coverage from nominal (0.90): |coverage_90 - 0.90|
    
    metrics_df["cov_error_90"] = (metrics_df["coverage_90"] - 0.90).abs()
    
    p_vals = []
    
    for scenario in df["scenario"].unique():
        for horizon in df["horizon"].unique():
            subset = metrics_df[(metrics_df["scenario"] == scenario) & (metrics_df["horizon"] == horizon)]
            
            p_data = subset[subset["model"] == "P_Conformal_ACI"].sort_values("seed")
            m3_data = subset[subset["model"] == "M3_LGBM_Quantile"].sort_values("seed")
            
            if len(p_data) == len(m3_data) and len(p_data) > 0:
                diffs = p_data["cov_error_90"].values - m3_data["cov_error_90"].values
                
                # Wilcoxon test (one-sided: we expect P to have LOWER coverage error than M3)
                # scipy.stats.wilcoxon defaults to two-sided, we use 'less'
                try:
                    stat, p_val = stats.wilcoxon(p_data["cov_error_90"].values, m3_data["cov_error_90"].values, alternative="less")
                except ValueError:
                    p_val = 1.0 # If all differences are exactly 0
                    
                median_diff = np.median(diffs)
                ci_low, ci_high = compute_bootstrap_ci(diffs)
                
                p_vals.append({
                    "scenario": scenario,
                    "horizon": horizon,
                    "p_median_err": p_data["cov_error_90"].median(),
                    "m3_median_err": m3_data["cov_error_90"].median(),
                    "median_diff": median_diff,
                    "ci_95_low": ci_low,
                    "ci_95_high": ci_high,
                    "p_value_raw": p_val
                })
                
    if p_vals:
        stats_df = pd.DataFrame(p_vals)
        # Holm correction manually
        stats_df.sort_values("p_value_raw", inplace=True)
        m = len(stats_df)
        stats_df["p_value_holm"] = np.minimum(1.0, stats_df["p_value_raw"] * np.arange(m, 0, -1))
        # Ensure monotonicity
        stats_df["p_value_holm"] = np.maximum.accumulate(stats_df["p_value_holm"])
        stats_df.sort_index(inplace=True)
        
        stats_df.to_csv(out_dir / "statistical_tests.csv", index=False)
        print("Statistical tests completed. See results/tables/statistical_tests.csv")
    else:
        print("Not enough paired data for statistical testing.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    run_analysis(quick=args.quick)
