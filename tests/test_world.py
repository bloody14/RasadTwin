"""Tests for world configuration loading."""
import pytest

from rasadtwin.sim.world import load_world_config

CONFIG_PATH = "config/world.yaml"


def test_load_config_success():
    """Config loads without errors and has required keys."""
    config = load_world_config(CONFIG_PATH)
    assert "world" in config
    assert "graph" in config
    assert "modes" in config
    assert "items" in config
    assert "weather" in config
    assert "demand" in config
    assert "tempo" in config
    assert "disruptions" in config
    assert "inventory" in config
    assert "scenarios" in config


def test_load_config_missing_file():
    """Non-existent config raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_world_config("nonexistent.yaml")


def test_transport_modes_present():
    """All four approved transport modes exist in config."""
    config = load_world_config(CONFIG_PATH)
    modes = config["modes"]
    for m in ["road", "mule", "heli", "drone"]:
        assert m in modes, f"Missing mode: {m}"


def test_items_present():
    """All four item categories exist."""
    config = load_world_config(CONFIG_PATH)
    items = config["items"]
    for i in ["rations", "POL", "medical", "spares"]:
        assert i in items, f"Missing item: {i}"


def test_scenarios_present():
    """All four scenario labels exist."""
    config = load_world_config(CONFIG_PATH)
    scenarios = config["scenarios"]
    for s in ["S1", "S2", "S3", "S4"]:
        assert s in scenarios, f"Missing scenario: {s}"
