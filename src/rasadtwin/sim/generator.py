"""HimalayaSim CLI generator — orchestrates world generation.

Usage (Windows PowerShell):
    python -m rasadtwin.sim.generator `
        --config config/world.yaml `
        --seed 42 `
        --n-posts 8 `
        --scenario S1 `
        --output results/raw/sim_run

All data is synthetic and fictional.
"""
from __future__ import annotations

import argparse
from datetime import date

import numpy as np

from rasadtwin.sim.demand import generate_demand
from rasadtwin.sim.disruptions import generate_disruptions
from rasadtwin.sim.graph import generate_edges, generate_nodes
from rasadtwin.sim.inventory import generate_inventory
from rasadtwin.sim.io import write_simulation_output
from rasadtwin.sim.schemas import Scenario, SimulationMetadata
from rasadtwin.sim.weather import generate_weather
from rasadtwin.sim.world import load_world_config
from rasadtwin.utils.metadata import (
    get_config_hash,
    get_git_commit,
    get_python_version,
    get_timestamp,
)


def run_simulation(
    config_path: str,
    seed: int,
    n_posts: int,
    scenario_name: str,
    output_dir: str,
    quick: bool = False,
) -> str:
    """Run the full HimalayaSim generation pipeline.

    Args:
        config_path: Path to world.yaml.
        seed: Master random seed.
        n_posts: Number of forward posts.
        scenario_name: Scenario label (S1/S2/S3/S4).
        output_dir: Output directory path.
        quick: If True, use reduced day count for fast testing.

    Returns:
        Path to the output directory.
    """
    config = load_world_config(config_path)
    scenario = Scenario(scenario_name)

    # Determine timeline
    world_cfg = config["world"]
    if quick:
        n_days = world_cfg.get("quick_days", 90)
    else:
        n_days = world_cfg["history_days"] + world_cfg["test_days"]

    start_date = date.fromisoformat(world_cfg["start_date"])

    # Deterministic child seeds via SeedSequence
    ss = np.random.SeedSequence(seed)
    child_seeds = ss.spawn(5)
    rng_graph = np.random.default_rng(child_seeds[0])
    rng_weather = np.random.default_rng(child_seeds[1])
    rng_demand = np.random.default_rng(child_seeds[2])
    rng_disruptions = np.random.default_rng(child_seeds[3])
    rng_inventory = np.random.default_rng(child_seeds[4])

    # Generate world topology
    nodes = generate_nodes(n_posts, config["graph"], rng_graph)
    edges = generate_edges(nodes, config["modes"], rng_graph)

    # Generate weather
    weather = generate_weather(
        nodes, start_date, n_days, config["weather"], rng_weather,
    )

    # Generate demand
    scenario_cfg = config["scenarios"].get(scenario_name, {})
    demand = generate_demand(
        nodes, start_date, n_days,
        config["demand"], config["tempo"], config["items"],
        config["troops"], scenario, scenario_cfg, rng_demand,
    )

    # Generate disruptions
    disruptions = generate_disruptions(
        edges, weather, start_date, n_days,
        config["disruptions"], rng_disruptions,
    )

    # Generate inventory
    inventory = generate_inventory(
        nodes, demand, start_date, n_days,
        config["inventory"], config["items"],
        scenario, scenario_cfg, rng_inventory,
    )

    # Metadata
    metadata = SimulationMetadata(
        git_commit=get_git_commit(),
        config_hash=get_config_hash(config),
        seed=seed,
        scenario=scenario,
        n_posts=n_posts,
        timestamp=get_timestamp(),
        python_version=get_python_version(),
        config=config,
    )

    # Write output
    out = write_simulation_output(
        output_dir, nodes, edges, weather,
        demand, inventory, disruptions, metadata,
    )

    return str(out)


def main() -> None:
    """CLI entry point for HimalayaSim generator."""
    parser = argparse.ArgumentParser(
        description="HimalayaSim — synthetic logistics world generator",
    )
    parser.add_argument(
        "--config", required=True, help="Path to world.yaml",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Master random seed",
    )
    parser.add_argument(
        "--n-posts", type=int, default=8,
        help="Number of forward posts (8, 20, 50, 100)",
    )
    parser.add_argument(
        "--scenario", default="S1",
        choices=["S1", "S2", "S3", "S4"],
        help="Scenario label",
    )
    parser.add_argument(
        "--output", default="results/raw/sim_output",
        help="Output directory",
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="Use reduced timeline for fast testing",
    )

    args = parser.parse_args()

    print(f"HimalayaSim: seed={args.seed} n_posts={args.n_posts} "
          f"scenario={args.scenario} quick={args.quick}")

    out = run_simulation(
        config_path=args.config,
        seed=args.seed,
        n_posts=args.n_posts,
        scenario_name=args.scenario,
        output_dir=args.output,
        quick=args.quick,
    )

    print(f"Output written to: {out}")


if __name__ == "__main__":
    main()
