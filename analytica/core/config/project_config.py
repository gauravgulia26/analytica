"""
Project configuration variables.
"""

import os

from dotenv import load_dotenv

from analytica.core.config.paths import ENV_FILE
from analytica.core.constants.paths_constants import DEFAULT_LOG_DIR
from analytica.core.constants.project_constants import (
    DEFAULT_ENVIRONMENT,
    DEFAULT_LOG_LEVEL,
    ENV_VARIABLE_NAME,
    PROJECT_DESCRIPTION,
    PROJECT_VERSION,
)
from analytica.core.constants.project_constants import (
    PROJECT_NAME as CONST_PROJECT_NAME,
)

# Load environment variables
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    load_dotenv()

# Project metadata variables
PROJECT_NAME: str = CONST_PROJECT_NAME
VERSION: str = PROJECT_VERSION
DESCRIPTION: str = PROJECT_DESCRIPTION

# Runtime environment settings
ENVIRONMENT: str = os.getenv(ENV_VARIABLE_NAME, DEFAULT_ENVIRONMENT)
DEBUG: bool = os.getenv("DEBUG", "false").strip().lower() in ("true", "1", "t", "yes")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()
LOG_DIR: str = os.getenv("LOG_DIR", DEFAULT_LOG_DIR)

__all__ = [
    "DEBUG",
    "DESCRIPTION",
    "ENVIRONMENT",
    "LOG_DIR",
    "LOG_LEVEL",
    "PROJECT_NAME",
    "VERSION",
]
