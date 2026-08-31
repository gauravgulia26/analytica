"""
Unit tests for project utils and root detection.
"""

from pathlib import Path
import pytest

from analytica.utils.get_root import get_project_root, get_root


def test_get_project_root():
    root = get_project_root()
    assert isinstance(root, Path)
    assert root.exists()
    assert (root / "pyproject.toml").exists()


def test_get_root_alias():
    root = get_root()
    assert root == get_project_root()
