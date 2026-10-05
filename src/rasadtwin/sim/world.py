"""World configuration loading and validation."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_world_config(config_path: str | Path) -> dict[str, Any]:
    """Load and return the world configuration from a YAML file.

    Args:
        config_path: Path to the world YAML configuration file.

    Returns:
        Parsed configuration dictionary.

    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If required top-level keys are missing.
    """
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    required_keys = [
        "world", "graph", "modes", "items",
        "troops", "weather", "demand", "tempo",
        "disruptions", "inventory", "scenarios",
    ]
    missing = [k for k in required_keys if k not in config]
    if missing:
        raise ValueError(f"Missing config keys: {missing}")

    return config
