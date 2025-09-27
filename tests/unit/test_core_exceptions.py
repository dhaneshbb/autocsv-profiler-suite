"""
Unit tests for core exception classes.

Tests custom exceptions and error handling in the AutoCSV Profiler Suite.
"""

import sys
from pathlib import Path

import pytest

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from autocsv_profiler.core.exceptions import (  # noqa: E402
    AutoCSVProfilerError,
    DelimiterDetectionError,
    FileProcessingError,
    ReportGenerationError,
)


class TestCoreExceptions:
    """Test cases for core exception classes."""

    def test_autocsv_profiler_error_basic(self):
        """Test basic AutoCSVProfilerError functionality."""
        error_msg = "Test error message"
        error = AutoCSVProfilerError(error_msg)

        assert str(error) == error_msg
        assert isinstance(error, Exception)
        assert isinstance(error, AutoCSVProfilerError)

    def test_file_processing_error(self):
        """Test FileProcessingError functionality."""
        error_msg = "Failed to process file"
        error = FileProcessingError(error_msg)

        assert str(error) == error_msg
        assert isinstance(error, AutoCSVProfilerError)
        assert isinstance(error, FileProcessingError)

    def test_delimiter_detection_error(self):
        """Test DelimiterDetectionError functionality."""
        error_msg = "Could not detect delimiter"
        error = DelimiterDetectionError(error_msg)

        assert str(error) == error_msg
        assert isinstance(error, AutoCSVProfilerError)
        assert isinstance(error, DelimiterDetectionError)

    def test_report_generation_error(self):
        """Test ReportGenerationError functionality."""
        report_name = "test_report"
        original_exception = ValueError("Original error")
        error = ReportGenerationError(report_name, original_exception)

        assert report_name in str(error)
        assert "Original error" in str(error)
        assert isinstance(error, AutoCSVProfilerError)
        assert isinstance(error, ReportGenerationError)

    def test_exception_inheritance_chain(self):
        """Test that all custom exceptions inherit properly."""
        exceptions_to_test = [
            FileProcessingError,
            DelimiterDetectionError,
            ReportGenerationError,
        ]

        for exception_class in exceptions_to_test:
            if exception_class == ReportGenerationError:
                error = exception_class("test_report", ValueError("test error"))
            else:
                error = exception_class("test message")

            # Should inherit from both base Exception and AutoCSVProfilerError
            assert isinstance(error, Exception)
            assert isinstance(error, AutoCSVProfilerError)
            assert isinstance(error, exception_class)

    def test_exception_with_context(self):
        """Test exceptions with additional context information."""
        original_error = ValueError("Original error")

        try:
            raise FileProcessingError("Processing failed") from original_error
        except FileProcessingError as e:
            assert str(e) == "Processing failed"
            assert e.__cause__ is original_error

    def test_exception_raising_and_catching(self):
        """Test raising and catching custom exceptions."""

        # Test FileProcessingError
        with pytest.raises(FileProcessingError) as exc_info:
            raise FileProcessingError("File not found")

        assert "File not found" in str(exc_info.value)

        # Test DelimiterDetectionError
        with pytest.raises(DelimiterDetectionError) as exc_info:
            raise DelimiterDetectionError("No delimiter detected")

        assert "No delimiter detected" in str(exc_info.value)

        # Test ReportGenerationError
        with pytest.raises(ReportGenerationError) as exc_info:
            raise ReportGenerationError(
                "test_report", ValueError("Report generation failed")
            )

        assert "test_report" in str(exc_info.value)

    def test_exception_with_multiple_args(self):
        """Test exceptions with default and custom messages."""
        # Test FileProcessingError with custom message
        error1 = FileProcessingError("Custom error message")
        assert "Custom error message" in str(error1)

        # Test FileProcessingError with default message
        error2 = FileProcessingError()
        assert "Error processing file" in str(error2)

    def test_exception_repr(self):
        """Test string representation of exceptions."""
        error = DelimiterDetectionError("Delimiter detection failed")

        # String representation should be informative
        error_repr = repr(error)
        assert "DelimiterDetectionError" in error_repr
        assert "Delimiter detection failed" in error_repr
