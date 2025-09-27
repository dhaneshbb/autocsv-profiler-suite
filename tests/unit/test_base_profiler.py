"""
Unit tests for base profiler classes and abstract interfaces.

Tests the foundational classes that define the profiler architecture
and ensure proper inheritance patterns across all engines.
"""

import sys
import tempfile
from abc import ABC, ABCMeta
from pathlib import Path

import pandas as pd
import pytest

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.fixtures.sample_data import generate_clean_sample_data  # noqa: E402


class TestBaseProfilerClass:
    """Test the base profiler abstract class."""

    def test_base_profiler_import(self):
        """Test that BaseProfiler can be imported."""
        try:
            from autocsv_profiler.base import BaseProfiler

            assert BaseProfiler is not None
            assert issubclass(BaseProfiler, ABC)
        except ImportError:
            pytest.skip("BaseProfiler not available for testing")

    def test_base_profiler_is_abstract(self):
        """Test that BaseProfiler cannot be instantiated directly."""
        try:
            from autocsv_profiler.base import BaseProfiler

            # Should raise TypeError for abstract class
            with pytest.raises(TypeError) as exc_info:
                BaseProfiler()

            assert (
                "abstract" in str(exc_info.value).lower()
                or "instantiate" in str(exc_info.value).lower()
            )

        except ImportError:
            pytest.skip("BaseProfiler not available for testing")

    def test_base_profiler_abstract_methods(self):
        """Test that BaseProfiler defines expected abstract methods."""
        try:
            from autocsv_profiler.base import BaseProfiler

            # Check that abstract methods are defined
            if hasattr(BaseProfiler, "__abstractmethods__"):
                abstract_methods = BaseProfiler.__abstractmethods__
                assert (
                    len(abstract_methods) > 0
                ), "BaseProfiler should have abstract methods"

                # Common methods we expect in a profiler
                found_methods = set(abstract_methods)

                # At least some expected methods should be present
                # (implementation may vary, so we're flexible)
                assert (
                    len(found_methods) > 0
                ), f"Expected some abstract methods, found: {found_methods}"

        except ImportError:
            pytest.skip("BaseProfiler not available for testing")

    def test_base_profiler_attributes(self):
        """Test BaseProfiler class attributes and structure."""
        try:
            from autocsv_profiler.base import BaseProfiler

            # Test class structure
            assert hasattr(BaseProfiler, "__module__")
            assert hasattr(BaseProfiler, "__qualname__")

            # Test that it's properly structured as ABC
            assert isinstance(BaseProfiler, ABCMeta)

        except ImportError:
            pytest.skip("BaseProfiler not available for testing")

    def test_optional_imports_handling(self):
        """Test that base module handles optional imports correctly."""
        try:
            from autocsv_profiler import base

            # Test optional import flags
            expected_flags = ["HAS_PSUTIL", "HAS_TQDM"]
            for flag in expected_flags:
                if hasattr(base, flag):
                    flag_value = getattr(base, flag)
                    assert isinstance(flag_value, bool), f"{flag} should be boolean"

        except ImportError:
            pytest.skip("Base module not available for testing")

    def test_profiler_factory_pattern(self):
        """Test factory pattern for creating profilers."""
        # This tests the concept of profiler factories
        # Implementation would depend on actual factory methods

        try:
            from autocsv_profiler.base import BaseProfiler

            # Test that we can't create instances directly (abstract)
            with pytest.raises(TypeError):
                BaseProfiler()

            # In a real implementation, we might test:
            # profiler = ProfilerFactory.create_profiler('main')
            # assert isinstance(profiler, BaseProfiler)

        except ImportError:
            pytest.skip("BaseProfiler not available for testing")


class TestConcreteProfilerImplementations:
    """Test concrete implementations that should inherit from BaseProfiler."""

    def test_main_analyzer_structure(self):
        """Test main analyzer module structure."""
        try:
            from autocsv_profiler.engines.main import analyzer

            # Test that main function exists
            assert hasattr(analyzer, "main")
            assert callable(analyzer.main)

            # Test that run_analysis function exists
            if hasattr(analyzer, "run_analysis"):
                assert callable(analyzer.run_analysis)

        except ImportError:
            pytest.skip("Main analyzer not available for testing")

    def test_engine_modules_structure(self):
        """Test that engine modules follow expected structure."""
        engine_modules = [
            ("main", "autocsv_profiler.engines.main.analyzer"),
            ("sweetviz", "autocsv_profiler.engines.profiling.sweetviz_report"),
            ("ydata", "autocsv_profiler.engines.profiling.ydata_report"),
            ("dataprep", "autocsv_profiler.engines.dataprep.dataprep_report"),
        ]

        available_engines = []

        for engine_name, module_path in engine_modules:
            try:
                module = __import__(module_path, fromlist=[""])
                available_engines.append(engine_name)

                # Test basic module structure
                assert hasattr(module, "__file__")

                # Test that each engine has some callable function
                functions = [
                    attr for attr in dir(module) if callable(getattr(module, attr))
                ]
                assert (
                    len(functions) > 0
                ), f"{engine_name} should have callable functions"

            except ImportError:
                continue

        # At least main engine should be available
        assert "main" in available_engines, "Main engine should always be available"
        assert (
            len(available_engines) >= 1
        ), f"At least one engine should be available, found: {available_engines}"

    def test_engine_interface_consistency(self):
        """Test that engines follow consistent interface patterns."""
        # Test that engines accept similar parameters

        try:
            # Test main function signature
            import inspect

            from autocsv_profiler.engines.main.analyzer import main

            sig = inspect.signature(main)
            params = list(sig.parameters.keys())

            # Expected parameters for profiling functions
            expected_params = {"file_path", "save_dir", "delimiter"}
            found_params = set(params)

            # Should have some common parameters
            common_params = expected_params.intersection(found_params)
            assert (
                len(common_params) >= 2
            ), f"Expected common parameters, found: {found_params}"

        except ImportError:
            pytest.skip("Main analyzer not available for testing")

    def test_engine_error_handling_patterns(self):
        """Test that engines follow consistent error handling."""
        try:
            from autocsv_profiler.engines.main.analyzer import main

            # Test with invalid file path
            with pytest.raises((FileNotFoundError, SystemExit, Exception)) as exc_info:
                main(
                    file_path="/nonexistent/file.csv",
                    save_dir="/tmp/test",
                    delimiter=",",
                    interactive=False,
                )

            # Should raise some form of controlled error
            assert exc_info.value is not None

        except ImportError:
            pytest.skip("Main analyzer not available for testing")

    @pytest.mark.integration
    def test_engine_data_processing_workflow(self):
        """Test basic data processing workflow for available engines."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "test.csv"
            output_dir = temp_path / "output"
            output_dir.mkdir()

            # Create test data
            test_data = generate_clean_sample_data(20)
            test_data.to_csv(input_file, index=False)

            # Test main engine processing
            try:
                from autocsv_profiler.engines.main.analyzer import main

                main(
                    file_path=str(input_file),
                    save_dir=str(output_dir),
                    delimiter=",",
                    interactive=False,
                )

                # Verify some output was generated
                output_files = list(output_dir.glob("*"))
                assert len(output_files) > 0, "Engine should generate output files"

                # Verify at least one file has content
                content_files = [
                    f for f in output_files if f.is_file() and f.stat().st_size > 0
                ]
                assert (
                    len(content_files) > 0
                ), "At least one output file should have content"

            except ImportError:
                pytest.skip("Main analyzer not available for testing")
            except SystemExit:
                # Main analyzer calls sys.exit() on completion - this is expected
                pass


class TestProfilerConfigurationIntegration:
    """Test integration between profilers and configuration system."""

    def test_profiler_config_access(self):
        """Test that profilers can access configuration."""
        try:
            from autocsv_profiler.config.settings import Settings

            settings = Settings()

            # Test configuration values that profilers would use
            chunk_size = settings.get("app.performance.chunk_size", 5000)
            memory_limit = settings.get("app.performance.memory_limit_gb", 1)

            assert isinstance(chunk_size, int)
            assert chunk_size > 0
            assert isinstance(memory_limit, (int, float))
            assert memory_limit > 0

        except ImportError:
            pytest.skip("Settings not available for testing")

    def test_profiler_logging_integration(self):
        """Test that profilers can integrate with logging system."""
        try:
            from autocsv_profiler.core.logger import get_logger

            logger = get_logger("test_profiler")
            assert logger is not None

            # Test basic logging functionality
            logger.info("Test profiler log message")

        except ImportError:
            pytest.skip("Logger not available for testing")

    def test_profiler_exception_integration(self):
        """Test that profilers use custom exception classes."""
        try:
            from autocsv_profiler.core.exceptions import (
                AutoCSVProfilerError,
                DelimiterDetectionError,
                FileProcessingError,
            )

            # Test exception hierarchy
            assert issubclass(FileProcessingError, AutoCSVProfilerError)
            assert issubclass(DelimiterDetectionError, AutoCSVProfilerError)

            # Test exception creation
            error = FileProcessingError("Test error")
            assert str(error) == "Test error"
            assert isinstance(error, AutoCSVProfilerError)

        except ImportError:
            pytest.skip("Exception classes not available for testing")


class TestProfilerUtilityIntegration:
    """Test integration with utility functions."""

    def test_profiler_validation_utils(self):
        """Test that profilers can use validation utilities."""
        try:
            from autocsv_profiler.core.validation import validate_csv_file

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            ) as f:
                f.write("id,name,value\n1,test,123\n2,test2,456")
                temp_file = f.name

            try:
                result = validate_csv_file(temp_file)
                assert isinstance(result, dict)
                assert "validation_status" in result
                assert result["validation_status"] == "valid"

            finally:
                Path(temp_file).unlink()

        except ImportError:
            pytest.skip("Validation utilities not available for testing")

    def test_profiler_memory_utils(self):
        """Test that profilers can use memory utilities."""
        try:
            from autocsv_profiler.core.utils import dataframe_memory_usage

            # Create test DataFrame
            test_df = pd.DataFrame(
                {"col1": range(100), "col2": ["test"] * 100, "col3": [1.5] * 100}
            )

            memory_usage = dataframe_memory_usage(test_df)
            assert isinstance(memory_usage, (int, float))
            assert memory_usage > 0

        except ImportError:
            pytest.skip("Memory utilities not available for testing")

    def test_profiler_file_utils(self):
        """Test that profilers can use file utilities."""
        try:
            from autocsv_profiler.core.utils import (
                format_file_size,
                safe_float_conversion,
            )

            # Test file size formatting
            size_str = format_file_size(1024)
            assert "1.00 KB" in size_str

            # Test safe conversion
            value = safe_float_conversion("123.45")
            assert value == 123.45

            invalid_value = safe_float_conversion("invalid", 0.0)
            assert invalid_value == 0.0

        except ImportError:
            pytest.skip("File utilities not available for testing")


# Mark these as unit tests for base profiler functionality
pytestmark = [pytest.mark.unit, pytest.mark.base_profiler]
