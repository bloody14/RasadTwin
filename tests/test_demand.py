"""Tests for synthetic demand generation."""
from datetime import date

import numpy as np

from rasadtwin.sim.demand import generate_demand
from rasadtwin.sim.graph import generate_nodes
from rasadtwin.sim.schemas import Item, Scenario, TempoState
from rasadtwin.sim.world import load_world_config

CONFIG_PATH = "config/world.yaml"


def _make_demand(seed: int = 42, n_days: int = 30):
    config = load_world_config(CONFIG_PATH)
    rng_graph = np.random.default_rng(seed)
    nodes = generate_nodes(8, config["graph"], rng_graph)
    rng_demand = np.random.default_rng(seed + 1)
    return generate_demand(
        nodes, date(2021, 1, 1), n_days,
        config["demand"], config["tempo"], config["items"],
        config["troops"], Scenario.S1, {}, rng_demand,
    )


def test_demand_non_negative():
    """All demand values must be non-negative."""
    demand = _make_demand()
    for d in demand:
        assert d.demand_units >= 0.0


def test_demand_has_all_items():
    """Demand records cover all four item categories."""
    demand = _make_demand()
    items_seen = {d.item for d in demand}
    assert Item.RATIONS in items_seen
    assert Item.POL in items_seen
    assert Item.MEDICAL in items_seen
    assert Item.SPARES in items_seen


def test_demand_tempo_states_valid():
    """All tempo states are valid enum members."""
    demand = _make_demand()
    for d in demand:
        assert d.tempo_state in TempoState


def test_demand_troops_positive():
    """Troop counts must be positive integers."""
    demand = _make_demand()
    for d in demand:
        assert d.troops > 0
