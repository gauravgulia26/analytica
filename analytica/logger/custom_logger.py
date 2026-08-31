"""
Colored logging system with support for both terminal and file outputs.
"""

from datetime import datetime
import logging
from pathlib import Path
import sys
from typing import ClassVar

from analytica.core.constants.paths_constants import DEFAULT_LOG_DIR
from analytica.core.constants.project_constants import (
    DEFAULT_CONSOLE_LOG_FORMAT,
    DEFAULT_DATE_FORMAT,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_LEVEL,
    PROJECT_NAME,
)
from analytica.utils.get_root import get_project_root


class ColoredFormatter(logging.Formatter):
    """
    Logging formatter that adds ANSI color escape codes for terminal outputs.
    """

    RESET = "\033[0m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BOLD_RED = "\033[1;31m"
    BLUE = "\033[34m"
    GRAY = "\033[90m"

    # Per-level format templates with ANSI color codes
    FORMATS: ClassVar[dict[int, str]] = {
        logging.DEBUG: f"{GRAY}[%(asctime)s]{RESET} {CYAN}%(levelname)-8s{RESET} {BLUE}[%(filename)s:%(lineno)d]{RESET} - %(message)s",
        logging.INFO: f"{GRAY}[%(asctime)s]{RESET} {GREEN}%(levelname)-8s{RESET} {BLUE}[%(filename)s:%(lineno)d]{RESET} - %(message)s",
        logging.WARNING: f"{GRAY}[%(asctime)s]{RESET} {YELLOW}%(levelname)-8s{RESET} {BLUE}[%(filename)s:%(lineno)d]{RESET} - %(message)s",
        logging.ERROR: f"{GRAY}[%(asctime)s]{RESET} {RED}%(levelname)-8s{RESET} {BLUE}[%(filename)s:%(lineno)d]{RESET} - {RED}%(message)s{RESET}",
        logging.CRITICAL: f"{GRAY}[%(asctime)s]{RESET} {BOLD_RED}%(levelname)-8s{RESET} {BLUE}[%(filename)s:%(lineno)d]{RESET} - {BOLD_RED}%(message)s{RESET}",
    }

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        use_color: bool = True,
    ) -> None:
        super().__init__(datefmt=datefmt or DEFAULT_DATE_FORMAT)
        self.fmt = fmt
        self.use_color = use_color
        self.datefmt = datefmt or DEFAULT_DATE_FORMAT

    def format(self, record: logging.LogRecord) -> str:
        if self.use_color:
            log_fmt = self.FORMATS.get(record.levelno, self.fmt or DEFAULT_CONSOLE_LOG_FORMAT)
        else:
            log_fmt = self.fmt or DEFAULT_LOG_FORMAT

        formatter = logging.Formatter(fmt=log_fmt, datefmt=self.datefmt)
        return formatter.format(record)


def resolve_log_dir(log_dir: str | Path = DEFAULT_LOG_DIR) -> Path:
    """
    Resolve the log directory path. If a relative path is given, it is resolved
    relative to the project root.

    Args:
        log_dir: Directory path for logs (default is 'log').

    Returns:
        Path: Absolute path to existing log directory.
    """
    path = Path(log_dir)
    if not path.is_absolute():
        path = get_project_root() / path
    path.mkdir(parents=True, exist_ok=True)
    return path


def setup_logger(
    name: str = PROJECT_NAME,
    log_dir: str | Path = DEFAULT_LOG_DIR,
    log_file: str | None = None,
    level: int | str = DEFAULT_LOG_LEVEL,
    console_output: bool = True,
    file_output: bool = True,
) -> logging.Logger:
    """
    Configure and return a logger with colored console output and clean file output.

    Args:
        name: Name of the logger.
        log_dir: Directory path to store log files (defaults to 'log').
        log_file: Optional specific log file name. If omitted, uses date-based filename.
        level: Logging level (e.g. INFO, DEBUG, logging.INFO).
        console_output: Enable colored console stream output.
        file_output: Enable log file output.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger_instance = logging.getLogger(name)

    # Convert string level to int if necessary
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    logger_instance.setLevel(level)

    # Clear existing handlers associated with this logger to prevent duplicates
    if logger_instance.hasHandlers():
        logger_instance.handlers.clear()

    # Prevent propagation to root logger if custom handlers are attached
    logger_instance.propagate = False

    # 1. Terminal / Console Handler (Colored)
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(
            ColoredFormatter(
                fmt=DEFAULT_CONSOLE_LOG_FORMAT,
                datefmt=DEFAULT_DATE_FORMAT,
                use_color=True,
            )
        )
        logger_instance.addHandler(console_handler)

    # 2. File Handler (Clean Plaintext, No ANSI Codes)
    if file_output:
        resolved_log_dir = resolve_log_dir(log_dir)
        if log_file is None:
            today_str = datetime.now().astimezone().strftime("%Y_%m_%d")
            log_file = f"{name}_{today_str}.log"

        log_file_path = resolved_log_dir / log_file
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter(
                fmt=DEFAULT_LOG_FORMAT,
                datefmt=DEFAULT_DATE_FORMAT,
            )
        )
        logger_instance.addHandler(file_handler)

    return logger_instance


def get_logger(
    name: str = PROJECT_NAME,
    log_dir: str | Path = DEFAULT_LOG_DIR,
    log_file: str | None = None,
    level: int | str = DEFAULT_LOG_LEVEL,
) -> logging.Logger:
    """
    Get or initialize a logger instance.

    Args:
        name: Name of the logger.
        log_dir: Directory path for logs (default 'log').
        log_file: Optional log filename.
        level: Logging level.

    Returns:
        logging.Logger: Logger instance.
    """
    logger_instance = logging.getLogger(name)
    if not logger_instance.handlers:
        return setup_logger(
            name=name,
            log_dir=log_dir,
            log_file=log_file,
            level=level,
        )
    return logger_instance


# Default global logger instance
logger = get_logger()
