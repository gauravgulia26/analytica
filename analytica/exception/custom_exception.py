"""
Custom general exception implementation with automated traceback extraction and logging.
"""

import inspect
import logging
from pathlib import Path
import sys
from typing import Any

CURRENT_EXCEPTION_FILE = Path(__file__).resolve()


def get_error_message_detail(
    error: str | Exception,
    error_detail: Any | None = None,
) -> tuple[str, str, int, str]:
    """
    Extracts the file name, line number, and formats the error message.

    Args:
        error: The error message string or an Exception instance.
        error_detail: Optional detail source (such as `sys`, traceback object, or original exception).

    Returns:
        tuple: (formatted_error_message, file_name, line_number, raw_message)
    """
    # 1. Determine the raw message
    if isinstance(error, Exception):
        raw_message = str(error) or error.__class__.__name__
    else:
        raw_message = str(error)

    if isinstance(error_detail, Exception) and not isinstance(error, Exception):
        raw_message = (
            f"{raw_message} (Caused by: {error_detail.__class__.__name__}: {error_detail})"
        )

    file_name: str | None = None
    line_number: int | None = None
    exc_tb = None

    # 2. Check error_detail for traceback information (e.g. sys module or exc_info tuple)
    if error_detail is not None:
        if hasattr(error_detail, "exc_info"):
            _, _, exc_tb = error_detail.exc_info()
        elif isinstance(error_detail, tuple) and len(error_detail) == 3:
            _, _, exc_tb = error_detail
        elif isinstance(error_detail, Exception) and error_detail.__traceback__ is not None:
            exc_tb = error_detail.__traceback__

    # 3. Check if error itself is an Exception with an attached traceback
    if exc_tb is None and isinstance(error, Exception):
        if error.__traceback__ is not None:
            exc_tb = error.__traceback__
        else:
            _, active_val, active_tb = sys.exc_info()
            if active_val is error and active_tb is not None:
                exc_tb = active_tb

    # 4. Extract file name and line number from traceback if available
    if exc_tb is not None:
        frames = []
        curr = exc_tb
        while curr is not None:
            frames.append((curr.tb_frame.f_code.co_filename, curr.tb_lineno))
            curr = curr.tb_next

        # Prefer the deepest frame in user/project code (skip third-party site-packages)
        chosen_frame = None
        for fn, ln in reversed(frames):
            frame_str = str(Path(fn).resolve())
            if "site-packages" not in frame_str and frame_str != str(CURRENT_EXCEPTION_FILE):
                chosen_frame = (fn, ln)
                break

        if chosen_frame is not None:
            file_name, line_number = chosen_frame
        elif frames:
            file_name, line_number = frames[-1]

    # 5. Fallback to caller stack inspection if no traceback was specified
    if file_name is None or line_number is None:
        stack = inspect.stack()
        for frame_info in stack:
            frame_path = Path(frame_info.filename).resolve()
            if frame_path != CURRENT_EXCEPTION_FILE:
                file_name = frame_info.filename
                line_number = frame_info.lineno
                break

        if file_name is None:
            if len(stack) > 1:
                file_name = stack[1].filename
                line_number = stack[1].lineno
            else:
                file_name = "unknown"
                line_number = 0

    formatted_message = (
        f"Error occurred in python script name [{file_name}] "
        f"line number [{line_number}] error message [{raw_message}]"
    )

    return formatted_message, file_name, line_number, raw_message


class AnalyticaException(Exception):
    """
    Custom general exception for Analytica.

    Automatically extracts the filename and line number where the error occurred,
    formats a detailed error message, and logs it via the project logger upon creation.
    """

    def __init__(
        self,
        error: str | Exception,
        error_detail: Any | None = None,
        auto_log: bool = True,
    ) -> None:
        """
        Initialize AnalyticaException.

        Args:
            error: Error message string or caught Exception.
            error_detail: Optional `sys` module, tuple from `sys.exc_info()`, or underlying Exception.
            auto_log: Whether to automatically log this exception upon instantiation (default: True).
        """
        formatted_message, file_name, line_number, raw_message = get_error_message_detail(
            error=error,
            error_detail=error_detail,
        )

        super().__init__(formatted_message)

        self.error_message = formatted_message
        self.file_name = file_name
        self.line_number = line_number
        self.raw_message = raw_message
        self.original_exception = (
            error
            if isinstance(error, Exception)
            else (error_detail if isinstance(error_detail, Exception) else None)
        )

        if auto_log:
            try:
                from analytica.logger.custom_logger import logger

                logger.error(self.error_message)
            except (ImportError, AttributeError, RuntimeError):
                # Fallback to module logger if project logger import fails
                logging.getLogger("analytica").error(self.error_message)

    def __str__(self) -> str:
        return self.error_message

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"file_name={self.file_name!r}, "
            f"line_number={self.line_number}, "
            f"message={self.raw_message!r})"
        )


# Aliases for flexibility and standard conventions
AppException = AnalyticaException
CustomException = AnalyticaException


def _analytica_excepthook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, AnalyticaException):
        # The exception has already been logged upon instantiation; exit cleanly without raw traceback
        sys.exit(1)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = _analytica_excepthook
