"""
YAML and configuration file loader utilities.
"""

from pathlib import Path
from typing import Any

import yaml


def load_yaml_key(
    file_path: str | Path,
    key: str,
) -> Any:
    """
    Load a YAML file and return the value associated with a top-level key.

    Args:
        file_path: Path to the YAML file.
        key: The key whose value should be retrieved.

    Returns:
        Any: Value corresponding to the specified key in the YAML file.
    """
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config[key]
