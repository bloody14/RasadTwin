import os

import yaml


def test_config_loader():
    """
    Test that configuration yaml files can be loaded.
    """
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "world.yaml")

    with open(config_path, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)

    # Content might be None if it's just comments, which it is currently.
    # We just ensure it reads properly without raising exceptions.
    assert content is None or isinstance(content, dict)
