"""
Utility for locating the project root directory dynamically.
"""

from collections.abc import Sequence
from pathlib import Path


def get_project_root(
    marker_files: Sequence[str] = ("pyproject.toml", ".git", ".env"),
) -> Path:
    """
    Get the absolute path to the project root directory.

    First attempts to locate the root by traversing upwards from the current file
    looking for known marker files/directories. If not found, falls back to the
    standard parent traversal depth (2 levels up from this file).

    Args:
        marker_files: Sequence of file or directory names indicating the project root.

    Returns:
        Path: Absolute path to the project root directory.
    """
    current_path = Path(__file__).resolve()

    # Search upwards for root marker files
    for parent in [current_path.parent] + list(current_path.parents):
        if any((parent / marker).exists() for marker in marker_files):
            return parent

    # Fallback to standard 2-level parent directory (analytica/utils/get_root.py -> root)
    return current_path.parents[2]


def get_root() -> Path:
    """
    Alias for get_project_root().

    Returns:
        Path: Absolute path to the project root directory.
    """
    return get_project_root()


if __name__ == "__main__":
    print(f"Project root: {get_project_root()}")
