"""
YAML and configuration file loader utilities.
"""

from pathlib import Path
from typing import Any

import yaml

from analytica.core.config.paths import DEFAULT_PROMPT_DIR_PATH


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


def load_prompt(prompt_name: str) -> str:
    """Load a prompt from a Markdown file.

    Args:
        prompt_name: Name of the prompt file without the .md extension.

    Returns:
        The prompt content as a string.

    Raises:
        FileNotFoundError: If the prompt file does not exist.
        ValueError: If prompt_name is empty or attempts path traversal.
    """
    if not prompt_name or not prompt_name.strip():
        raise ValueError("prompt_name cannot be empty.")

    prompt_name = prompt_name.strip()

    # Prevent paths such as ../../secret.md
    if Path(prompt_name).name != prompt_name:
        raise ValueError("prompt_name must be a simple filename.")

    prompt_path = DEFAULT_PROMPT_DIR_PATH / f"{prompt_name}.md"
    if not prompt_path.is_file():
        raise FileNotFoundError(f"Prompt '{prompt_name}' not found in {DEFAULT_PROMPT_DIR_PATH}")

    return prompt_path.read_text(encoding="utf-8").strip()
