"""Tests for synthetic weather generation."""
from datetime import date

import numpy as np

from rasadtwin.sim.graph import generate_nodes
from rasadtwin.sim.weather import generate_weather
from rasadtwin.sim.world import load_world_config

CONFIG_PATH = "config/world.yaml"


def test_weather_record_count():
    """Weather generates one record per node per day."""
    config = load_world_config(CONFIG_PATH)
    rng = np.random.default_rng(42)
    nodes = generate_nodes(8, config["graph"], rng)
    n_days = 30
    weather = generate_weather(
        nodes, date(2021, 1, 1), n_days, config["weather"],
        np.random.default_rng(42),
    )
    assert len(weather) == len(nodes) * n_days


def test_weather_visibility_bounded():
    """Visibility must be at least the configured minimum."""
    config = load_world_config(CONFIG_PATH)
    rng = np.random.default_rng(42)
    nodes = generate_nodes(8, config["graph"], rng)
    weather = generate_weather(
        nodes, date(2021, 1, 1), 90, config["weather"],
        np.random.default_rng(42),
    )
    vis_min = config["weather"]["visibility_min_km"]
    for w in weather:
        assert w.visibility_km >= vis_min


def test_weather_wind_non_negative():
    """Wind speed must be non-negative."""
    config = load_world_config(CONFIG_PATH)
    rng = np.random.default_rng(42)
    nodes = generate_nodes(8, config["graph"], rng)
    weather = generate_weather(
        nodes, date(2021, 1, 1), 90, config["weather"],
        np.random.default_rng(42),
    )
    for w in weather:
        assert w.wind_kph >= 0.0
