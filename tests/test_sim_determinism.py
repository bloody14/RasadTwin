"""Tests proving deterministic generation for HimalayaSim."""
from datetime import date

import numpy as np

from rasadtwin.sim.demand import generate_demand
from rasadtwin.sim.disruptions import generate_disruptions
from rasadtwin.sim.graph import generate_edges, generate_nodes
from rasadtwin.sim.schemas import Scenario
from rasadtwin.sim.weather import generate_weather
from rasadtwin.sim.world import load_world_config

CONFIG_PATH = "config/world.yaml"


def _make_rngs(seed: int) -> dict:
    ss = np.random.SeedSequence(seed)
    children = ss.spawn(4)
    return {
        "graph": np.random.default_rng(children[0]),
        "weather": np.random.default_rng(children[1]),
        "demand": np.random.default_rng(children[2]),
        "disruptions": np.random.default_rng(children[3]),
    }


def _generate_all(seed: int, config: dict):
    rngs = _make_rngs(seed)
    nodes = generate_nodes(8, config["graph"], rngs["graph"])
    edges = generate_edges(nodes, config["modes"], rngs["graph"])
    weather = generate_weather(
        nodes, date(2021, 1, 1), 30, config["weather"], rngs["weather"],
    )
    demand = generate_demand(
        nodes, date(2021, 1, 1), 30,
        config["demand"], config["tempo"], config["items"],
        config["troops"], Scenario.S1, {}, rngs["demand"],
    )
    disruptions = generate_disruptions(
        edges, weather, date(2021, 1, 1), 30,
        config["disruptions"], rngs["disruptions"],
    )
    return nodes, edges, weather, demand, disruptions


def test_same_seed_identical():
    """Same seed + same config must produce identical outputs."""
    config = load_world_config(CONFIG_PATH)
    r1 = _generate_all(42, config)
    r2 = _generate_all(42, config)

    for a, b in zip(r1, r2):
        assert len(a) == len(b)
        for ra, rb in zip(a, b):
            assert ra == rb


def test_different_seed_differs():
    """Different seed must change at least one stochastic output."""
    config = load_world_config(CONFIG_PATH)
    r1 = _generate_all(42, config)
    r2 = _generate_all(99, config)

    # At least one subsystem should differ
    any_diff = False
    for a, b in zip(r1, r2):
        if len(a) != len(b):
            any_diff = True
            break
        for ra, rb in zip(a, b):
            if ra != rb:
                any_diff = True
                break
        if any_diff:
            break
    assert any_diff, "Different seeds produced identical output"
