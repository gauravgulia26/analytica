"""
Unit tests for configuration variables.
"""

from pathlib import Path
import pytest

from analytica.core.config.paths import (
    DATA_DIR,
    LOG_DIR,
    RAW_DATA_DIR,
    ROOT_DIR,
)
from analytica.core.config.project_config import (
    DEBUG,
    ENVIRONMENT,
    LOG_LEVEL,
    PROJECT_NAME,
    VERSION,
)


def test_paths_variables():
    assert isinstance(ROOT_DIR, Path)
    assert ROOT_DIR.exists()
    assert DATA_DIR == ROOT_DIR / "data"
    assert RAW_DATA_DIR == ROOT_DIR / "data" / "raw"
    assert LOG_DIR == ROOT_DIR / "log"


def test_project_config_variables():
    assert PROJECT_NAME == "analytica"
    assert VERSION == "0.0.1"
    assert isinstance(ENVIRONMENT, str)
    assert isinstance(DEBUG, bool)
    assert isinstance(LOG_LEVEL, str)
