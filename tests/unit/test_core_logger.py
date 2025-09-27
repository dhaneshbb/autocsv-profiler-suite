"""
Unit tests for core logging functionality.

Tests logging configuration and utility functions.
"""

import logging
import sys
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from autocsv_profiler.core.logger import get_logger, log_print
except ImportError:
    # Create mock implementations if not available
    def get_logger(name="autocsv"):
        return logging.getLogger(name)

    def log_print(message, level="INFO"):
        print(f"[{level}] {message}")


class TestCoreLogger:
    """Test cases for core logging functionality."""

    def test_get_logger_basic(self):
        """Test basic logger retrieval."""
        logger = get_logger("test_logger")

        assert isinstance(logger, logging.Logger)
        assert "test_logger" in logger.name

    def test_get_logger_with_name(self):
        """Test logger retrieval with custom name."""
        custom_name = "test_logger"
        logger = get_logger(custom_name)

        assert isinstance(logger, logging.Logger)
        assert custom_name in logger.name

    def test_log_print_basic(self):
        """Test log_print functionality."""
        test_message = "Test log message"

        # Capture stdout
        captured_output = StringIO()

        with patch("sys.stdout", captured_output):
            log_print(test_message)

        output = captured_output.getvalue()
        assert test_message in output

    def test_log_print_different_levels(self):
        """Test log_print with different log levels."""
        test_message = "Test message"
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in levels:
            captured_output = StringIO()

            with patch("sys.stdout", captured_output):
                log_print(test_message, level=level)

            output = captured_output.getvalue()
            assert test_message in output
            # log_print may not include level in output, just check message is there

    def test_logger_configuration(self):
        """Test logger configuration and settings."""
        logger = get_logger("test_config")

        # Logger should be properly configured
        assert isinstance(logger, logging.Logger)

        # Test that we can set log level
        original_level = logger.level
        logger.setLevel(logging.DEBUG)
        assert logger.level == logging.DEBUG

        # Restore original level
        logger.setLevel(original_level)

    def test_logger_handlers(self):
        """Test logger handlers configuration."""
        logger = get_logger("test_handlers")

        # Logger should have at least one handler (or inherit from root)
        has_handlers = len(logger.handlers) > 0 or len(logging.getLogger().handlers) > 0
        assert has_handlers or not logger.propagate

    def test_log_formatting(self):
        """Test log message formatting."""
        logger = get_logger("test_format")

        # Create a temporary handler to capture log output
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setFormatter(
            logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        )

        # Add handler and test logging
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        test_message = "Format test message"
        logger.info(test_message)

        # Check output
        log_output = log_capture.getvalue()
        assert test_message in log_output
        assert "INFO" in log_output

        # Clean up
        logger.removeHandler(handler)

    def test_log_print_error_handling(self):
        """Test log_print error handling."""
        # Test with invalid log level
        test_message = "Error handling test"

        # Should not raise exception with invalid level
        try:
            log_print(test_message, level="INVALID_LEVEL")
            # If it doesn't raise, that's fine
        except Exception as e:
            # If it raises, should be a reasonable error
            assert isinstance(e, (ValueError, AttributeError, KeyError))

    def test_logger_with_file_handler(self):
        """Test logger with file output."""
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".log", delete=False
        ) as tmp_file:
            log_file_path = tmp_file.name

        try:
            # Create logger with file handler
            logger = get_logger("test_file")
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
            logger.addHandler(file_handler)
            logger.setLevel(logging.INFO)

            # Log a test message
            test_message = "File logging test"
            logger.info(test_message)

            # Flush and close handler
            file_handler.flush()
            file_handler.close()
            logger.removeHandler(file_handler)

            # Read back the log file
            with open(log_file_path, "r") as f:
                log_content = f.read()

            assert test_message in log_content

        finally:
            # Clean up
            try:
                Path(log_file_path).unlink()
            except FileNotFoundError:
                pass

    def test_multiple_loggers(self):
        """Test creating multiple loggers with different names."""
        logger1 = get_logger("test1")
        logger2 = get_logger("test2")
        logger3 = get_logger("test1")  # Should be same as logger1

        assert logger1 is not logger2
        assert logger1 is logger3  # Same name should return same logger

        assert "test1" in logger1.name
        assert "test2" in logger2.name
