"""E1 Forecasting Experiment Runner."""
from __future__ import annotations

import argparse
import warnings
from pathlib import Path

import pandas as pd

# Suppress statsforecast and LightGBM warnings for cleaner output
warnings.filterwarnings("ignore")

from rasadtwin.forecast.chronos_benchmark import ChronosBenchmark
from rasadtwin.forecast.conformal import ConformalACI
from rasadtwin.forecast.ets import ETSForecaster
from rasadtwin.forecast.features import generate_features, load_and_merge_data
from rasadtwin.forecast.lightgbm_models import LGBMPointGaussian, LGBMQuantile
from rasadtwin.forecast.naive import SeasonalNaive
from rasadtwin.forecast.pipeline import run_pipeline
from rasadtwin.sim.generator import run_simulation


def run_e1(quick: bool = False) -> None:
    """Execute the E1 preregistered experiment."""
    scenarios = ["S1", "S2", "S3", "S4"]
    horizons = [7, 14, 28]

    if quick:
        seeds = [42, 99]
        horizons = [7]
        scenarios = ["S1", "S2"]
        n_posts = 8
        print("Running QUICK validation mode...")
    else:
        # At least 10 world seeds
        seeds = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        n_posts = 20
        print("Running FULL E1 evaluation...")

    models = [
        SeasonalNaive(),
        ETSForecaster(),
        LGBMPointGaussian(),
        LGBMQuantile(),
        ChronosBenchmark(),
        ConformalACI(lr=0.05),
    ]

    all_results = []

    out_dir = Path("results/raw/e1_forecast")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Checkpoint file logic
    ckpt_file = out_dir / ("quick_checkpoint.parquet" if quick else "full_checkpoint.parquet")
    completed_runs = set()
    if ckpt_file.exists():
        existing = pd.read_parquet(ckpt_file)
        all_results.append(existing)
        # Identify completed (seed, scenario) pairs
        for _, row in existing[["seed", "scenario"]].drop_duplicates().iterrows():
            completed_runs.add((row["seed"], row["scenario"]))
        print(f"Resuming from checkpoint with {len(completed_runs)} completed (seed, scenario) pairs.")

    for seed in seeds:
        for scenario in scenarios:
            if (seed, scenario) in completed_runs:
                continue

            print(f"Generating world: Seed={seed}, Scenario={scenario}")
            sim_out = run_simulation(
                config_path="config/world.yaml",
                seed=seed,
                n_posts=n_posts,
                scenario_name=scenario,
                output_dir=f"results/raw/sim_temp_{seed}_{scenario}",
                quick=False  # We always need full history for forecast training
            )

            print("Loading and generating features...")
            df_raw = load_and_merge_data(sim_out)
            df_feat = generate_features(df_raw)

            run_frames = []
            for h in horizons:
                print(f"  -> Forecasting Horizon: {h} days")
                try:
                    preds = run_pipeline(df_feat, models, h, seed, scenario)
                    if preds:
                        run_frames.extend(preds)
                except Exception as e:
                    print(f"  -> [ERROR] Pipeline failed for horizon {h}: {e}")

            if run_frames:
                run_df = pd.concat(run_frames, ignore_index=True)
                all_results.append(run_df)

                # Checkpoint
                full_df = pd.concat(all_results, ignore_index=True)
                full_df.to_parquet(ckpt_file)

            print(f"Completed Seed={seed}, Scenario={scenario}")

    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        final_file = out_dir / ("quick_results.parquet" if quick else "full_results.parquet")
        final_df.to_parquet(final_file)
        print(f"Execution finished. Results saved to {final_file}")
    else:
        print("No results generated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Run in quick validation mode")
    args = parser.parse_args()
    run_e1(quick=args.quick)
