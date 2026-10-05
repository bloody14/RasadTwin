"""Tests for inventory dynamics."""
import math
from datetime import date

import numpy as np

from rasadtwin.sim.demand import generate_demand
from rasadtwin.sim.graph import generate_nodes
from rasadtwin.sim.inventory import generate_inventory
from rasadtwin.sim.schemas import Scenario
from rasadtwin.sim.world import load_world_config

CONFIG_PATH = "config/world.yaml"


def _make_inventory(seed: int = 42, n_days: int = 30):
    config = load_world_config(CONFIG_PATH)
    ss = np.random.SeedSequence(seed)
    children = ss.spawn(3)
    rng_graph = np.random.default_rng(children[0])
    rng_demand = np.random.default_rng(children[1])
    rng_inv = np.random.default_rng(children[2])

    nodes = generate_nodes(8, config["graph"], rng_graph)
    demand = generate_demand(
        nodes, date(2021, 1, 1), n_days,
        config["demand"], config["tempo"], config["items"],
        config["troops"], Scenario.S1, {}, rng_demand,
    )
    inventory = generate_inventory(
        nodes, demand, date(2021, 1, 1), n_days,
        config["inventory"], config["items"],
        Scenario.S1, {}, rng_inv,
    )
    return inventory


def test_inventory_conservation():
    """Closing stock = opening + replenishment - consumed.

    Where consumed = min(demand, opening + replenishment).
    Skip NaN records (S4 IoT dropout).
    """
    inv = _make_inventory()
    for rec in inv:
        if math.isnan(rec.opening_stock) or math.isnan(rec.closing_stock):
            continue
        consumed = min(
            rec.demand_units, rec.opening_stock + rec.replenishment_units,
        )
        expected_closing = (
            rec.opening_stock + rec.replenishment_units - consumed
        )
        assert abs(rec.closing_stock - expected_closing) < 0.1, (
            f"Conservation violated: {rec}"
        )


def test_inventory_no_negative_stock():
    """Closing stock must not be negative (skip NaN)."""
    inv = _make_inventory()
    for rec in inv:
        if math.isnan(rec.closing_stock):
            continue
        assert rec.closing_stock >= -0.01, f"Negative stock: {rec}"


def test_unmet_demand_non_negative():
    """Unmet demand must be non-negative."""
    inv = _make_inventory()
    for rec in inv:
        assert rec.unmet_demand_units >= -0.01
