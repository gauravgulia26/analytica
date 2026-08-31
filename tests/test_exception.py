"""
Unit tests for custom general exception and automated logging.
"""

import sys
import pytest

from analytica.exception.custom_exception import (
    AnalyticaException,
    AppException,
    CustomException,
    get_error_message_detail,
)


def test_exception_direct_raise():
    try:
        raise AnalyticaException("Testing direct exception message")
    except AnalyticaException as exc:
        assert "Testing direct exception message" in exc.error_message
        assert "test_exception.py" in exc.file_name
        assert exc.line_number is not None
        assert exc.line_number > 0
        assert exc.raw_message == "Testing direct exception message"


def test_exception_with_sys_traceback():
    try:
        _ = 1 / 0
    except Exception as e:
        exc = AnalyticaException(e, sys)
        assert "division by zero" in exc.error_message
        assert "test_exception.py" in exc.file_name
        assert exc.line_number is not None
        assert exc.line_number > 0


def test_exception_aliases():
    assert AppException is AnalyticaException
    assert CustomException is AnalyticaException


def test_exception_string_and_repr():
    exc = AnalyticaException("Sample error", auto_log=False)
    assert str(exc) == exc.error_message
    assert "AnalyticaException(" in repr(exc)
