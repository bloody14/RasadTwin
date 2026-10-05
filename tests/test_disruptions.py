"""Tests for disruption generation."""
from datetime import date

import numpy as np

from rasadtwin.sim.disruptions import generate_disruptions
from rasadtwin.sim.graph import generate_edges, generate_nodes
from rasadtwin.sim.schemas import TransportMode
from rasadtwin.sim.weather import generate_weather
from rasadtwin.sim.world import load_world_config

CONFIG_PATH = "config/world.yaml"


def _make_disruptions(seed: int = 42, n_days: int = 90):
    config = load_world_config(CONFIG_PATH)
    ss = np.random.SeedSequence(seed)
    children = ss.spawn(3)
    rng_graph = np.random.default_rng(children[0])
    rng_weather = np.random.default_rng(children[1])
    rng_disruptions = np.random.default_rng(children[2])

    nodes = generate_nodes(8, config["graph"], rng_graph)
    edges = generate_edges(nodes, config["modes"], rng_graph)
    weather = generate_weather(
        nodes, date(2021, 1, 1), n_days,
        config["weather"], rng_weather,
    )
    return generate_disruptions(
        edges, weather, date(2021, 1, 1), n_days,
        config["disruptions"], rng_disruptions,
    )


def test_disruption_durations_positive():
    """All disruption durations must be >= 1."""
    disruptions = _make_disruptions()
    for d in disruptions:
        assert d.duration_days >= 1


def test_disruption_types_valid():
    """All disruption types must be recognized."""
    valid_types = {
        "road_closure", "landslide",
        "heli_grounding", "drone_grounding",
    }
    disruptions = _make_disruptions()
    for d in disruptions:
        assert d.type in valid_types, f"Unknown type: {d.type}"


def test_disruptions_generated():
    """Over 90 days, at least some disruptions should occur."""
    disruptions = _make_disruptions()
    assert len(disruptions) > 0, "No disruptions generated in 90 days"


def test_graph_has_all_modes():
    """Generated edges include all four transport modes."""
    config = load_world_config(CONFIG_PATH)
    rng = np.random.default_rng(42)
    nodes = generate_nodes(8, config["graph"], rng)
    edges = generate_edges(nodes, config["modes"], rng)
    modes_found = {e.mode for e in edges}
    for m in TransportMode:
        assert m in modes_found, f"Missing mode: {m}"


def test_node_counts():
    """Generated node counts match configuration."""
    config = load_world_config(CONFIG_PATH)
    for n_posts in [8, 20, 50, 100]:
        rng = np.random.default_rng(42)
        nodes = generate_nodes(n_posts, config["graph"], rng)
        expected = (
            config["graph"]["rear_depots"]
            + config["graph"]["intermediate_depots"]
            + n_posts
        )
        assert len(nodes) == expected, (
            f"n_posts={n_posts}: got {len(nodes)}, expected {expected}"
        )


def test_forward_post_altitudes():
    """Forward post altitudes stay in configured range."""
    config = load_world_config(CONFIG_PATH)
    rng = np.random.default_rng(42)
    nodes = generate_nodes(50, config["graph"], rng)
    alt_min = config["graph"]["forward_post_altitude_min_m"]
    alt_max = config["graph"]["forward_post_altitude_max_m"]
    for n in nodes:
        if n.node_type.value == "forward_post":
            assert alt_min <= n.altitude_m <= alt_max, (
                f"{n.node_id}: altitude {n.altitude_m} out of range"
            )
