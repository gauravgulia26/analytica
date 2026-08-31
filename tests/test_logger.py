"""
Unit tests for colored logger and file logging.
"""

import logging
from pathlib import Path
import pytest

from analytica.logger.custom_logger import (
    ColoredFormatter,
    get_logger,
    logger,
    resolve_log_dir,
    setup_logger,
)


def test_resolve_log_dir(tmp_path: Path):
    custom_dir = tmp_path / "test_logs"
    resolved = resolve_log_dir(custom_dir)
    assert resolved.exists()
    assert resolved == custom_dir


def test_setup_logger_file_and_console(tmp_path: Path):
    test_logger = setup_logger(
        name="test_logger",
        log_dir=tmp_path,
        log_file="test.log",
        level=logging.DEBUG,
    )

    test_logger.info("Test info message")
    test_logger.warning("Test warning message")

    log_file_path = tmp_path / "test.log"
    assert log_file_path.exists()
    content = log_file_path.read_text(encoding="utf-8")
    assert "Test info message" in content
    assert "Test warning message" in content
    # Ensure ANSI codes are not written to file
    assert "\033[" not in content


def test_colored_formatter():
    formatter = ColoredFormatter(use_color=True)
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Sample message",
        args=(),
        exc_info=None,
    )
    formatted = formatter.format(record)
    assert "Sample message" in formatted
    assert "\033[" in formatted
