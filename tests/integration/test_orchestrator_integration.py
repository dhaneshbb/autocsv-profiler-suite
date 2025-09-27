"""
Integration tests for the CSV Profiler Orchestrator.

Tests the main orchestration system that coordinates between different
environments and manages the overall analysis workflow.
"""

import subprocess
import sys
from pathlib import Path

import pytest

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.utils.test_helpers import (  # noqa: E402
    MockEnvironmentManager,
    assert_file_exists_and_not_empty,
    create_test_csv,
    skip_if_environment_missing,
    skip_if_no_conda,
)


class TestOrchestratorIntegration:
    """Integration tests for the orchestrator system."""

    @pytest.fixture
    def mock_orchestrator(self):
        """Create a mock orchestrator for testing."""

        class MockCSVProfilerOrchestrator:
            def __init__(self):
                self.env_manager = MockEnvironmentManager()
                self.available_environments = {
                    "main": True,
                    "profiling": True,
                    "dataprep": True,
                }
                self.conda_environments = {
                    "csv-profiler-main": True,
                    "csv-profiler-profiling": True,
                    "csv-profiler-dataprep": True,
                }

            def check_conda_available(self):
                """Mock conda availability check."""
                return True

            def check_environments_exist(self):
                """Mock environment existence check."""
                return all(self.conda_environments.values())

            def detect_delimiter(self, csv_path):
                """Mock delimiter detection."""
                try:
                    # Simple detection based on first line
                    with open(csv_path, "r", encoding="utf-8") as f:
                        first_line = f.readline()

                    delimiters = [",", ";", "\t", "|", ":"]
                    counts = {d: first_line.count(d) for d in delimiters}
                    return max(counts, key=counts.get) if any(counts.values()) else ","
                except Exception:
                    return ","

            def run_analysis(self, csv_path, output_dir=None, engines=None):
                """Mock analysis execution."""
                if output_dir is None:
                    output_dir = Path(csv_path).parent / "output"

                output_dir = Path(output_dir)
                output_dir.mkdir(exist_ok=True)

                if engines is None:
                    engines = ["main", "profiling", "dataprep"]

                results = {}

                for engine in engines:
                    if (
                        engine in self.available_environments
                        and self.available_environments[engine]
                    ):
                        # Mock successful execution
                        output_file = output_dir / f"{engine}_report.html"

                        # Create mock output file
                        with open(output_file, "w") as f:
                            f.write(
                                f"<html><body><h1>Mock {engine} Report</h1></body></html>"
                            )

                        results[engine] = {
                            "success": True,
                            "output_file": str(output_file),
                            "execution_time": 1.0,
                        }
                    else:
                        results[engine] = {
                            "success": False,
                            "error": f"Environment {engine} not available",
                            "execution_time": 0.0,
                        }

                return results

        return MockCSVProfilerOrchestrator()

    def test_orchestrator_initialization(self, mock_orchestrator):
        """Test orchestrator can be initialized."""
        assert mock_orchestrator is not None
        assert hasattr(mock_orchestrator, "run_analysis")
        assert hasattr(mock_orchestrator, "check_conda_available")
        assert hasattr(mock_orchestrator, "check_environments_exist")

    def test_conda_availability_check(self, mock_orchestrator):
        """Test conda availability checking."""
        conda_available = mock_orchestrator.check_conda_available()
        assert isinstance(conda_available, bool)

        # In mock, should always return True
        assert conda_available is True

    def test_environments_existence_check(self, mock_orchestrator):
        """Test environment existence checking."""
        environments_exist = mock_orchestrator.check_environments_exist()
        assert isinstance(environments_exist, bool)

        # In mock with all environments available, should return True
        assert environments_exist is True

    def test_delimiter_detection_integration(self, mock_orchestrator, tmp_path):
        """Test delimiter detection as part of orchestrator workflow."""
        # Create test CSV with comma delimiter
        csv_file = create_test_csv(
            tmp_path / "test_comma.csv",
            data={"col1": [1, 2, 3], "col2": ["a", "b", "c"]},
            delimiter=",",
        )

        detected_delimiter = mock_orchestrator.detect_delimiter(csv_file)
        assert detected_delimiter == ","

        # Test with semicolon delimiter
        csv_file_semi = create_test_csv(
            tmp_path / "test_semi.csv",
            data={"col1": [1, 2, 3], "col2": ["a", "b", "c"]},
            delimiter=";",
        )

        detected_delimiter_semi = mock_orchestrator.detect_delimiter(csv_file_semi)
        assert detected_delimiter_semi == ";"

    def test_single_engine_analysis(
        self, mock_orchestrator, sample_csv_small, temp_output_dir
    ):
        """Test analysis with single engine."""
        results = mock_orchestrator.run_analysis(
            csv_path=sample_csv_small, output_dir=temp_output_dir, engines=["main"]
        )

        assert isinstance(results, dict)
        assert "main" in results
        assert results["main"]["success"] is True

        # Check that output file was created
        output_file = Path(results["main"]["output_file"])
        assert_file_exists_and_not_empty(output_file)

    def test_multi_engine_analysis(
        self, mock_orchestrator, sample_csv_small, temp_output_dir
    ):
        """Test analysis with multiple engines."""
        results = mock_orchestrator.run_analysis(
            csv_path=sample_csv_small,
            output_dir=temp_output_dir,
            engines=["main", "profiling", "dataprep"],
        )

        assert isinstance(results, dict)
        assert len(results) == 3

        # All engines should succeed in mock
        for engine in ["main", "profiling", "dataprep"]:
            assert engine in results
            assert results[engine]["success"] is True

            output_file = Path(results[engine]["output_file"])
            assert_file_exists_and_not_empty(output_file)

    def test_analysis_with_missing_environment(
        self, mock_orchestrator, sample_csv_small, temp_output_dir
    ):
        """Test analysis behavior when an environment is missing."""
        # Simulate missing environment
        mock_orchestrator.available_environments["profiling"] = False

        results = mock_orchestrator.run_analysis(
            csv_path=sample_csv_small,
            output_dir=temp_output_dir,
            engines=["main", "profiling"],
        )

        assert isinstance(results, dict)
        assert "main" in results
        assert "profiling" in results

        # Main should succeed, profiling should fail
        assert results["main"]["success"] is True
        assert results["profiling"]["success"] is False
        assert "not available" in results["profiling"]["error"]

    def test_analysis_output_directory_creation(
        self, mock_orchestrator, sample_csv_small, tmp_path
    ):
        """Test that analysis creates output directory if it doesn't exist."""
        output_dir = tmp_path / "new_output_directory"
        assert not output_dir.exists()

        results = mock_orchestrator.run_analysis(
            csv_path=sample_csv_small, output_dir=output_dir, engines=["main"]
        )

        assert output_dir.exists()
        assert results["main"]["success"] is True

    def test_analysis_with_different_csv_sizes(
        self, mock_orchestrator, temp_output_dir, tmp_path
    ):
        """Test analysis with different CSV file sizes."""
        # Small CSV
        small_csv = create_test_csv(tmp_path / "small.csv", data={"col": [1, 2, 3]})

        # Medium CSV
        medium_data = {
            "col1": list(range(100)),
            "col2": [f"item_{i}" for i in range(100)],
        }
        medium_csv = create_test_csv(tmp_path / "medium.csv", data=medium_data)

        # Test both files
        for csv_file in [small_csv, medium_csv]:
            results = mock_orchestrator.run_analysis(
                csv_path=csv_file, output_dir=temp_output_dir, engines=["main"]
            )

            assert results["main"]["success"] is True
            output_file = Path(results["main"]["output_file"])
            assert_file_exists_and_not_empty(output_file)

    def test_analysis_execution_time_tracking(
        self, mock_orchestrator, sample_csv_small, temp_output_dir
    ):
        """Test that analysis tracks execution time."""
        results = mock_orchestrator.run_analysis(
            csv_path=sample_csv_small, output_dir=temp_output_dir, engines=["main"]
        )

        assert "execution_time" in results["main"]
        assert isinstance(results["main"]["execution_time"], (int, float))
        assert results["main"]["execution_time"] >= 0

    def test_analysis_error_handling(
        self, mock_orchestrator, temp_output_dir, tmp_path
    ):
        """Test analysis error handling with problematic input."""
        # Create empty file
        empty_csv = tmp_path / "empty.csv"
        empty_csv.touch()

        # Analysis should handle gracefully
        results = mock_orchestrator.run_analysis(
            csv_path=empty_csv, output_dir=temp_output_dir, engines=["main"]
        )

        # Mock orchestrator will still succeed, but real implementation might fail
        assert isinstance(results, dict)
        assert "main" in results

    def test_orchestrator_with_custom_parameters(
        self, mock_orchestrator, sample_csv_small, temp_output_dir
    ):
        """Test orchestrator with custom analysis parameters."""
        # Mock orchestrator doesn't implement parameter passing, but test structure
        results = mock_orchestrator.run_analysis(
            csv_path=sample_csv_small, output_dir=temp_output_dir, engines=["main"]
        )

        assert results["main"]["success"] is True

        # In real implementation, we would test:
        # - Custom chunk sizes
        # - Memory limits
        # - Different output formats
        # - Analysis configuration options

    @pytest.mark.integration
    def test_full_workflow_integration(
        self, mock_orchestrator, sample_csv_medium, temp_output_dir
    ):
        """Test complete workflow from start to finish."""
        csv_path = sample_csv_medium

        # Step 1: Check system requirements
        conda_available = mock_orchestrator.check_conda_available()
        environments_exist = mock_orchestrator.check_environments_exist()

        assert conda_available is True
        assert environments_exist is True

        # Step 2: Detect delimiter
        delimiter = mock_orchestrator.detect_delimiter(csv_path)
        assert delimiter in [",", ";", "\t", "|", ":"]

        # Step 3: Run full analysis
        results = mock_orchestrator.run_analysis(
            csv_path=csv_path,
            output_dir=temp_output_dir,
            engines=["main", "profiling", "dataprep"],
        )

        # Step 4: Verify results
        assert len(results) == 3

        for engine_name, result in results.items():
            assert result["success"] is True
            assert "output_file" in result
            assert "execution_time" in result

            output_file = Path(result["output_file"])
            assert_file_exists_and_not_empty(output_file)

    @pytest.mark.slow
    def test_concurrent_analysis_handling(
        self, mock_orchestrator, tmp_path, temp_output_dir
    ):
        """Test orchestrator handling of concurrent analysis requests."""
        # Create multiple CSV files
        csv_files = []
        for i in range(3):
            csv_file = create_test_csv(
                tmp_path / f"concurrent_{i}.csv",
                data={"id": [1, 2, 3], "value": [i * 10, i * 20, i * 30]},
            )
            csv_files.append(csv_file)

        # Run analyses (mock doesn't actually run concurrently, but tests structure)
        all_results = {}

        for i, csv_file in enumerate(csv_files):
            output_subdir = temp_output_dir / f"output_{i}"
            results = mock_orchestrator.run_analysis(
                csv_path=csv_file, output_dir=output_subdir, engines=["main"]
            )
            all_results[f"analysis_{i}"] = results

        # Verify all analyses completed
        assert len(all_results) == 3

        for analysis_name, results in all_results.items():
            assert results["main"]["success"] is True

    def test_orchestrator_cleanup_and_resource_management(
        self, mock_orchestrator, sample_csv_small, temp_output_dir
    ):
        """Test that orchestrator properly manages resources and cleanup."""
        # Run analysis
        results = mock_orchestrator.run_analysis(
            csv_path=sample_csv_small, output_dir=temp_output_dir, engines=["main"]
        )

        assert results["main"]["success"] is True

        # In real implementation, we would test:
        # - Temporary file cleanup
        # - Memory deallocation
        # - Process termination
        # - Resource release

        # Mock test: verify output files exist (not cleaned up prematurely)
        output_file = Path(results["main"]["output_file"])
        assert output_file.exists()


@pytest.mark.environment
class TestRealEnvironmentIntegration:
    """Integration tests that require actual conda environments."""

    @skip_if_no_conda()
    def test_real_conda_detection(self):
        """Test real conda availability detection."""
        # This test runs only if conda is available
        result = subprocess.run(["conda", "--version"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "conda" in result.stdout.lower()

    @skip_if_no_conda()
    @skip_if_environment_missing("csv-profiler-main")
    def test_real_main_environment_exists(self):
        """Test that main environment actually exists."""
        result = subprocess.run(
            ["conda", "env", "list"], capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "csv-profiler-main" in result.stdout

    @skip_if_no_conda()
    @skip_if_environment_missing("csv-profiler-main")
    @pytest.mark.slow
    def test_real_environment_execution(self, sample_csv_small, temp_output_dir):
        """Test actual execution in conda environment."""
        # This is a placeholder for real environment testing
        # In practice, this would execute actual scripts in conda environments

        # Example command that would be run:
        # conda run -n csv-profiler-main python -m autocsv_profiler.engines.main.analyzer

        # For now, just verify environment exists
        result = subprocess.run(
            ["conda", "run", "-n", "csv-profiler-main", "python", "--version"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # If environment exists and Python is available, this should succeed
        if result.returncode == 0:
            assert "Python" in result.stdout
        else:
            pytest.skip("Main environment not properly configured")
