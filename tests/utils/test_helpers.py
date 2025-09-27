"""
Test helper utilities for AutoCSV Profiler Suite.

Provides common functions and utilities used across multiple test modules.
"""

import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import pytest


def is_conda_available() -> bool:
    """Check if conda is available in the system."""
    try:
        result = subprocess.run(
            ["conda", "--version"], capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_environment_exists(env_name: str) -> bool:
    """Check if a conda environment exists."""
    try:
        result = subprocess.run(
            ["conda", "env", "list"], capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return env_name in result.stdout
        return False
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def get_available_test_environments() -> List[str]:
    """Get list of available test environments."""
    environments = []
    expected_envs = [
        "csv-profiler-main",
        "csv-profiler-profiling",
        "csv-profiler-dataprep",
    ]

    for env_name in expected_envs:
        if check_environment_exists(env_name):
            environments.append(env_name)

    return environments


def create_test_csv(
    file_path: Path,
    data: Optional[Dict[str, List]] = None,
    delimiter: str = ",",
    encoding: str = "utf-8",
    include_header: bool = True,
) -> Path:
    """Create a test CSV file with specified parameters."""
    if data is None:
        # Default test data
        data = {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
            "value": [10.5, 20.3, 15.7, 30.2, 25.1],
        }

    df = pd.DataFrame(data)
    df.to_csv(
        file_path, sep=delimiter, index=False, encoding=encoding, header=include_header
    )

    return file_path


def validate_csv_structure(
    file_path: Path,
    expected_columns: Optional[List[str]] = None,
    expected_rows: Optional[int] = None,
    delimiter: Optional[str] = None,
) -> bool:
    """Validate the structure of a CSV file."""
    try:
        # Try to read the CSV
        if delimiter:
            df = pd.read_csv(file_path, sep=delimiter)
        else:
            df = pd.read_csv(file_path)

        # Check columns if specified
        if expected_columns is not None:
            if list(df.columns) != expected_columns:
                return False

        # Check row count if specified
        if expected_rows is not None:
            if len(df) != expected_rows:
                return False

        return True

    except Exception:
        return False


def get_file_size_mb(file_path: Path) -> float:
    """Get file size in megabytes."""
    if file_path.exists():
        return file_path.stat().st_size / (1024 * 1024)
    return 0.0


def run_in_environment(
    env_name: str, command: str, timeout: int = 60
) -> Dict[str, Any]:
    """Run a command in a specific conda environment."""
    if not is_conda_available():
        return {
            "success": False,
            "stdout": "",
            "stderr": "Conda not available",
            "returncode": -1,
        }

    if not check_environment_exists(env_name):
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Environment {env_name} does not exist",
            "returncode": -1,
        }

    cmd = ["conda", "run", "-n", env_name] + command.split()
    returncode, stdout, stderr = run_subprocess_with_timeout(cmd, timeout)

    return {
        "success": returncode == 0,
        "stdout": stdout,
        "stderr": stderr,
        "returncode": returncode,
    }


def run_subprocess_with_timeout(
    cmd: List[str], timeout: int = 60, cwd: Optional[Path] = None
) -> Tuple[int, str, str]:
    """Run a subprocess with timeout and return results."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Process timed out"
    except Exception as e:
        return -1, "", str(e)


def mock_conda_run(env_name: str, script_path: str, args: List[str] = None) -> str:
    """Mock conda run command for testing without actual conda execution."""
    if args is None:
        args = []

    mock_output = f"Mock execution in environment '{env_name}'\n"
    mock_output += f"Script: {script_path}\n"
    mock_output += f"Args: {' '.join(args)}\n"
    mock_output += "Mock analysis completed successfully."

    return mock_output


def assert_file_exists_and_not_empty(file_path: Path, min_size_bytes: int = 1):
    """Assert that a file exists and has minimum size."""
    assert file_path.exists(), f"File does not exist: {file_path}"
    assert file_path.stat().st_size >= min_size_bytes, f"File is too small: {file_path}"


def assert_valid_html_file(file_path: Path):
    """Assert that a file is a valid HTML file."""
    assert_file_exists_and_not_empty(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Basic HTML validation
    assert "<html" in content.lower(), "File does not contain HTML structure"
    assert "</html>" in content.lower(), "File does not contain closing HTML tag"


def assert_valid_csv_file(file_path: Path, expected_delimiter: str = ","):
    """Assert that a file is a valid CSV file."""
    assert_file_exists_and_not_empty(file_path)

    try:
        df = pd.read_csv(
            file_path, sep=expected_delimiter, nrows=5
        )  # Read first 5 rows for validation
        assert len(df) > 0, "CSV file appears to be empty"
        assert len(df.columns) > 0, "CSV file has no columns"
    except Exception as e:
        pytest.fail(f"Failed to read CSV file {file_path}: {str(e)}")


def clean_test_outputs(output_dir: Path):
    """Clean up test output files and directories."""
    if output_dir.exists():
        shutil.rmtree(output_dir)


def skip_if_no_conda():
    """Decorator to skip test if conda is not available."""
    return pytest.mark.skipif(
        not is_conda_available(),
        reason="Conda not available - skipping conda-dependent test",
    )


def skip_if_environment_missing(env_name: str):
    """Decorator to skip test if specific conda environment is missing."""
    return pytest.mark.skipif(
        not check_environment_exists(env_name),
        reason=f"Conda environment '{env_name}' not available - skipping test",
    )


def parametrize_delimiters():
    """Provide common delimiter parametrization for tests."""
    return pytest.mark.parametrize("delimiter", [",", ";", "\t", "|", ":"])


def parametrize_file_sizes():
    """Provide common file size parametrization for tests."""
    return pytest.mark.parametrize("file_size", ["small", "medium", "large"])


class MockEnvironmentManager:
    """Mock environment manager for testing without actual conda environments."""

    def __init__(self):
        self.available_environments = {
            "csv-profiler-main": True,
            "csv-profiler-profiling": True,
            "csv-profiler-dataprep": True,
        }
        self.execution_log = []

    def is_environment_available(self, env_name: str) -> bool:
        """Check if environment is available."""
        return self.available_environments.get(env_name, False)

    def run_in_environment(
        self, env_name: str, command: str, timeout: int = 60
    ) -> Dict[str, Any]:
        """Mock conda run execution."""
        if not self.is_environment_available(env_name):
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Environment {env_name} not available",
                "returncode": -1,
            }

        execution_record = {
            "environment": env_name,
            "command": command,
            "timeout": timeout,
        }
        self.execution_log.append(execution_record)

        return {
            "success": True,
            "stdout": f"Mock execution in {env_name}: {command}",
            "stderr": "",
            "returncode": 0,
        }

    def execute_in_environment(
        self, env_name: str, script: str, args: List[str] = None
    ) -> str:
        """Mock execution in environment (legacy method)."""
        if not self.is_environment_available(env_name):
            raise RuntimeError(f"Environment '{env_name}' not available")

        if args is None:
            args = []

        execution_record = {"environment": env_name, "script": script, "args": args}
        self.execution_log.append(execution_record)

        return f"Mock execution in {env_name}: {script} {' '.join(args)}"

    def get_execution_log(self) -> List[Dict]:
        """Get log of all executions."""
        return self.execution_log.copy()

    def clear_log(self):
        """Clear execution log."""
        self.execution_log.clear()


class MemoryTracker:
    """Helper class for tracking memory usage during tests."""

    def __init__(self):
        try:
            import psutil

            self.psutil = psutil
            self.available = True
        except ImportError:
            self.psutil = None
            self.available = False

        self.initial_memory = None
        self.peak_memory = None

    def start_tracking(self):
        """Start memory tracking."""
        if self.available:
            process = self.psutil.Process()
            self.initial_memory = process.memory_info().rss
            self.peak_memory = self.initial_memory

    def update_peak(self):
        """Update peak memory usage."""
        if self.available:
            process = self.psutil.Process()
            current_memory = process.memory_info().rss
            if current_memory > self.peak_memory:
                self.peak_memory = current_memory

    def get_memory_usage_mb(self) -> Dict[str, Optional[float]]:
        """Get memory usage in MB."""
        if not self.available:
            return {"initial": None, "peak": None, "current": None}

        process = self.psutil.Process()
        current_memory = process.memory_info().rss

        return {
            "initial": (
                self.initial_memory / (1024 * 1024) if self.initial_memory else None
            ),
            "peak": self.peak_memory / (1024 * 1024) if self.peak_memory else None,
            "current": current_memory / (1024 * 1024),
        }

    def assert_memory_under_limit(self, limit_mb: float):
        """Assert that peak memory usage is under specified limit."""
        if self.available and self.peak_memory:
            peak_mb = self.peak_memory / (1024 * 1024)
            assert (
                peak_mb <= limit_mb
            ), f"Memory usage {peak_mb:.1f}MB exceeded limit {limit_mb}MB"
