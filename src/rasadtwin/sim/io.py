"""Serialization utilities for HimalayaSim output.

Writes generated data to Parquet files with a JSON metadata sidecar.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rasadtwin.sim.schemas import (
    DemandRecord,
    DisruptionRecord,
    EdgeRecord,
    InventoryRecord,
    NodeRecord,
    SimulationMetadata,
    WeatherRecord,
)


def _records_to_dicts(records: list[Any]) -> list[dict[str, Any]]:
    """Convert a list of Pydantic models to a list of dicts."""
    return [r.model_dump(mode="json") for r in records]


def _write_parquet(rows: list[dict[str, Any]], path: Path) -> None:
    """Write a list of row-dicts to a Parquet file.

    Falls back to CSV if pyarrow is not available.

    Args:
        rows: List of row dictionaries.
        path: Output file path (without extension).
    """
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq

        if not rows:
            path.parent.mkdir(parents=True, exist_ok=True)
            table = pa.table({})
            pq.write_table(table, str(path.with_suffix(".parquet")))
            return

        table = pa.Table.from_pylist(rows)
        path.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(table, str(path.with_suffix(".parquet")))
    except ImportError:
        import csv

        path_csv = path.with_suffix(".csv")
        path_csv.parent.mkdir(parents=True, exist_ok=True)
        if not rows:
            path_csv.write_text("", encoding="utf-8")
            return
        fieldnames = list(rows[0].keys())
        with open(path_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


def write_simulation_output(
    output_dir: str | Path,
    nodes: list[NodeRecord],
    edges: list[EdgeRecord],
    weather: list[WeatherRecord],
    demand: list[DemandRecord],
    inventory: list[InventoryRecord],
    disruptions: list[DisruptionRecord],
    metadata: SimulationMetadata,
) -> Path:
    """Write all simulation outputs to a directory.

    Creates Parquet files for each data table and a JSON metadata sidecar.

    Args:
        output_dir: Target directory for output files.
        nodes: Generated node records.
        edges: Generated edge records.
        weather: Generated weather records.
        demand: Generated demand records.
        inventory: Generated inventory records.
        disruptions: Generated disruption records.
        metadata: Simulation reproducibility metadata.

    Returns:
        Path to the output directory.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    _write_parquet(_records_to_dicts(nodes), out / "nodes")
    _write_parquet(_records_to_dicts(edges), out / "edges")
    _write_parquet(_records_to_dicts(weather), out / "weather")
    _write_parquet(_records_to_dicts(demand), out / "demand")
    _write_parquet(_records_to_dicts(inventory), out / "inventory")
    _write_parquet(_records_to_dicts(disruptions), out / "disruptions")

    meta_path = out / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata.model_dump(mode="json"), f, indent=2)

    return out
