from rasadtwin.utils.metadata import (
    generate_experiment_metadata,
    get_config_hash,
)


def test_config_hash_deterministic():
    """
    Test that identical dictionaries produce identical hashes,
    and different dictionaries produce different hashes.
    """
    config1 = {"a": 1, "b": "test", "c": [1, 2, 3]}
    config2 = {"c": [1, 2, 3], "a": 1, "b": "test"}  # Different key order
    config3 = {"a": 1, "b": "test", "c": [1, 2, 4]}  # Different value

    hash1 = get_config_hash(config1)
    hash2 = get_config_hash(config2)
    hash3 = get_config_hash(config3)

    assert hash1 == hash2
    assert hash1 != hash3


def test_experiment_metadata_schema():
    """
    Test that the generated metadata dictionary has the required keys and types.
    """
    config = {"param": "value"}
    seed = 42

    metadata = generate_experiment_metadata(config, seed)

    assert "git_commit" in metadata
    assert "config_hash" in metadata
    assert "seed" in metadata
    assert "timestamp" in metadata
    assert "python_version" in metadata

    assert metadata["seed"] == 42
    assert isinstance(metadata["timestamp"], str)
    assert isinstance(metadata["python_version"], str)
