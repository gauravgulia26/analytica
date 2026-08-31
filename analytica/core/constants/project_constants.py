"""
Project-level constants for the Analytica framework.
"""

PROJECT_NAME = "analytica"
PROJECT_VERSION = "0.0.1"
PROJECT_DESCRIPTION = (
    "A modular multi-agent AI system for automated data analysis, exploration, "
    "and insight generation."
)

# Encoding & localization
DEFAULT_ENCODING = "utf-8"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_TIMEZONE = "UTC"

# Logging constants
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "[%(asctime)s] %(levelname)-8s [%(filename)s:%(lineno)d] - %(message)s"
DEFAULT_CONSOLE_LOG_FORMAT = (
    "[%(asctime)s] %(levelname)-8s [%(filename)s:%(lineno)d] - %(message)s"
)

# Environment constants
DEFAULT_ENVIRONMENT = "development"
ENV_VARIABLE_NAME = "ANALYTICA_ENV"
