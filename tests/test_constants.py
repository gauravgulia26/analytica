"""
Unit tests for project and path constants.
"""

from analytica.core.constants.paths_constants import (
    DEFAULT_CONFIG_DIR,
    DEFAULT_DATA_DIR,
    DEFAULT_LOG_DIR,
    DEFAULT_LOG_FILE,
    DEFAULT_MODELS_DIR,
    DEFAULT_REPORTS_DIR,
)
from analytica.core.constants.project_constants import (
    PROJECT_NAME,
    PROJECT_VERSION,
)


def test_path_constants():
    assert DEFAULT_LOG_DIR == "log"
    assert DEFAULT_LOG_FILE == "analytica.log"
    assert DEFAULT_DATA_DIR == "data"
    assert DEFAULT_MODELS_DIR == "models"
    assert DEFAULT_REPORTS_DIR == "reports"
    assert DEFAULT_CONFIG_DIR == "config"


def test_project_constants():
    assert PROJECT_NAME == "analytica"
    assert PROJECT_VERSION == "0.0.1"
