from pathlib import Path
from typing import Any

import yaml


def load_yaml_key(
    file_path: str | Path,
    key: str,
) -> Any:
    """Load a YAML file and return the value associated with a key."""
    file_path = Path(file_path)

    with file_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config[key]
