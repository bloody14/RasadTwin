import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from typing import Any, Dict


def get_git_commit() -> str:
    """
    Retrieve the current git commit hash.
    Returns 'unknown' if not in a git repository or command fails.
    """
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        )
        return commit.decode("utf-8").strip()
    except Exception:
        return "unknown"


def get_config_hash(config: Dict[str, Any]) -> str:
    """
    Compute a deterministic SHA-256 hash of a configuration dictionary.
    """
    config_str = json.dumps(config, sort_keys=True)
    return hashlib.sha256(config_str.encode("utf-8")).hexdigest()


def get_python_version() -> str:
    """
    Get the Python version string.
    """
    return platform.python_version()


def get_timestamp() -> str:
    """
    Get the current UTC timestamp in ISO 8601 format.
    """
    return datetime.now(timezone.utc).isoformat()


def generate_experiment_metadata(config: Dict[str, Any], seed: int) -> Dict[str, Any]:
    """
    Generate reproducibility metadata for an experiment run.
    """
    return {
        "git_commit": get_git_commit(),
        "config_hash": get_config_hash(config),
        "seed": seed,
        "timestamp": get_timestamp(),
        "python_version": get_python_version(),
    }
