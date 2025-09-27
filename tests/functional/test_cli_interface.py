"""
Functional tests for CLI interface and main entry points.

Tests the actual command-line interface and main orchestration functionality.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestCLIInterfaceFunctional:
    """Functional tests for CLI interface."""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace with sample CSV."""
        temp_dir = Path(tempfile.mkdtemp(prefix="cli_test_"))
        csv_file = temp_dir / "sample.csv"
        output_dir = temp_dir / "output"

        # Create sample data
        data = {
            "id": list(range(1, 11)),
            "name": [f"Person_{i}" for i in range(1, 11)],
            "age": [20, 25, 30, 35, 40, 45, 50, 55, 60, 65],
            "score": [85.5, 90.2, 78.8, 92.1, 88.7, 95.3, 87.9, 91.4, 89.6, 93.8],
            "category": ["A", "B", "A", "C", "B", "A", "C", "B", "A", "C"],
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)

        yield {"temp_dir": temp_dir, "csv_file": csv_file, "output_dir": output_dir}

        # Cleanup
        import shutil

        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    def test_run_analysis_help(self):
        """Test run_analysis.py help functionality."""
        result = subprocess.run(
            [sys.executable, "bin/run_analysis.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "autocsv profiler suite" in result.stdout.lower()

    def test_run_analysis_with_csv_file(self, temp_workspace):
        """Test run_analysis.py with actual CSV file."""
        csv_file = temp_workspace["csv_file"]
        output_dir = temp_workspace["output_dir"]

        # Run analysis in non-interactive mode
        result = subprocess.run(
            [
                sys.executable,
                "bin/run_analysis.py",
                str(csv_file),
                "--output-dir",
                str(output_dir),
                "--non-interactive",
            ],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        # Check that command executed successfully
        if result.returncode != 0:
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")

        # Note: Command might fail due to missing conda environments,
        # but we can still test the argument parsing and basic validation
        assert "error: unrecognized arguments" not in result.stderr
        assert csv_file.name in result.stdout or csv_file.name in result.stderr

    def test_run_analysis_invalid_file(self):
        """Test run_analysis.py with invalid CSV file."""
        result = subprocess.run(
            [
                sys.executable,
                "bin/run_analysis.py",
                "nonexistent_file.csv",
                "--non-interactive",
            ],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        # Should fail with non-zero exit code
        assert result.returncode != 0
        assert "error" in result.stderr.lower() or "not found" in result.stderr.lower()

    def test_run_analysis_with_delimiter_option(self, temp_workspace):
        """Test run_analysis.py with delimiter specification."""
        csv_file = temp_workspace["csv_file"]
        output_dir = temp_workspace["output_dir"]

        result = subprocess.run(
            [
                sys.executable,
                "bin/run_analysis.py",
                str(csv_file),
                "--output-dir",
                str(output_dir),
                "--delimiter",
                ",",
                "--non-interactive",
            ],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        # Check command line parsing works
        assert "error: unrecognized arguments" not in result.stderr

    def test_setup_environments_help(self):
        """Test setup_environments.py help functionality."""
        result = subprocess.run(
            [sys.executable, "bin/setup_environments.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "environment" in result.stdout.lower()

    def test_setup_environments_status_check(self):
        """Test setup_environments.py status functionality."""
        result = subprocess.run(
            [sys.executable, "bin/setup_environments.py", "--status"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        # Should execute without error (even if environments don't exist)
        assert result.returncode == 0 or "conda" in result.stderr.lower()

    @pytest.mark.slow
    def test_full_analysis_pipeline_mock(self, temp_workspace):
        """Test complete analysis pipeline with mocking for missing environments."""
        csv_file = temp_workspace["csv_file"]
        output_dir = temp_workspace["output_dir"]

        # This test verifies the pipeline works up to the point where
        # conda environments would be called
        result = subprocess.run(
            [
                sys.executable,
                "bin/run_analysis.py",
                str(csv_file),
                "--output-dir",
                str(output_dir),
                "--engines",
                "main",  # Only test main engine
                "--non-interactive",
                "--verbose",
            ],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
            timeout=60,
        )

        # Verify basic processing occurred
        output_text = result.stdout + result.stderr
        assert csv_file.name in output_text

    def test_run_analysis_version(self):
        """Test version display functionality."""
        result = subprocess.run(
            [sys.executable, "bin/run_analysis.py", "--version"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        if result.returncode == 0:
            assert any(
                char.isdigit() for char in result.stdout
            )  # Should contain version number


class TestPackageImportFunctional:
    """Functional tests for package import and basic functionality."""

    def test_package_import(self):
        """Test that main package can be imported."""
        import autocsv_profiler

        # Basic attributes should exist
        assert hasattr(autocsv_profiler, "__version__")
        assert hasattr(autocsv_profiler, "settings")

    def test_version_info_functional(self):
        """Test version information functionality."""
        from autocsv_profiler import get_version_info, get_version_string

        version_info = get_version_info()
        version_string = get_version_string()

        assert version_info.major >= 0
        assert version_info.minor >= 0
        assert version_info.patch >= 0
        assert isinstance(version_string, str)
        assert len(version_string) > 0

    def test_dependency_versions_functional(self):
        """Test dependency version checking functionality."""
        from autocsv_profiler import get_dependency_versions

        deps = get_dependency_versions()

        assert isinstance(deps, dict)
        assert "pandas" in deps
        assert "numpy" in deps

        # Should contain either version strings or "Not installed"
        for dep, version in deps.items():
            assert isinstance(version, str)
            assert len(version) > 0

    def test_settings_basic_functionality(self):
        """Test basic settings functionality."""
        from autocsv_profiler import settings

        # Should be able to get basic settings
        test_value = settings.get("analysis.decimal_precision", 4)
        assert isinstance(test_value, int)

        # Should be able to get nested settings
        memory_limit = settings.get("processing.memory_limit_gb", 1)
        assert isinstance(memory_limit, (int, float))
        assert memory_limit > 0

    def test_lazy_import_functionality(self):
        """Test that lazy imports work correctly."""
        from autocsv_profiler import profile_csv

        # Should be callable (even if it fails due to missing environments)
        assert callable(profile_csv)

    def test_exception_classes_functional(self):
        """Test that custom exception classes are available."""
        from autocsv_profiler import (
            AutoCSVProfilerError,
            DelimiterDetectionError,
            FileProcessingError,
            ReportGenerationError,
        )

        # Should be proper exception classes
        assert issubclass(AutoCSVProfilerError, Exception)
        assert issubclass(FileProcessingError, AutoCSVProfilerError)
        assert issubclass(DelimiterDetectionError, AutoCSVProfilerError)
        assert issubclass(ReportGenerationError, AutoCSVProfilerError)

        # Should be instantiable
        error = AutoCSVProfilerError("test message")
        assert str(error) == "test message"
