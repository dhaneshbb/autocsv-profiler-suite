"""
Pytest configuration and shared fixtures for AutoCSV Profiler Suite tests.

This module provides:
- Test fixtures for sample CSV files
- Environment setup/teardown
- Configuration mocking
- Shared utilities for testing
"""

import os
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest
import yaml

# Add project root to Python path for testing
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_path():
    """Return the project root directory path."""
    return project_root


@pytest.fixture(scope="session")
def test_data_dir(project_root_path):
    """Return the test data directory path."""
    test_data_path = project_root_path / "tests" / "fixtures"
    test_data_path.mkdir(parents=True, exist_ok=True)
    return test_data_path


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_csv_small(test_data_dir):
    """Create a small sample CSV file for testing."""
    csv_path = test_data_dir / "sample_small.csv"

    # Create sample data
    data = {
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "age": [25, 30, 35, 28, 32],
        "salary": [50000, 60000, 70000, 55000, 65000],
        "department": ["IT", "HR", "IT", "Finance", "IT"],
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

    yield csv_path

    # Cleanup
    if csv_path.exists():
        csv_path.unlink()


@pytest.fixture
def sample_csv_medium(test_data_dir):
    """Create a medium-sized sample CSV file for testing."""
    csv_path = test_data_dir / "sample_medium.csv"

    # Create sample data with more rows
    import numpy as np

    np.random.seed(42)  # For reproducible tests

    n_rows = 1000
    data = {
        "id": range(1, n_rows + 1),
        "value": np.random.randn(n_rows),
        "category": np.random.choice(["A", "B", "C", "D"], n_rows),
        "score": np.random.uniform(0, 100, n_rows),
        "flag": np.random.choice([True, False], n_rows),
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

    yield csv_path

    # Cleanup
    if csv_path.exists():
        csv_path.unlink()


@pytest.fixture
def sample_csv_large(test_data_dir):
    """Create a large sample CSV file for memory testing."""
    csv_path = test_data_dir / "sample_large.csv"

    # Create sample data with many rows (for memory testing)
    import numpy as np

    np.random.seed(42)

    n_rows = 10000  # Reasonable size for testing without being too slow
    data = {
        "id": range(1, n_rows + 1),
        "data1": np.random.randn(n_rows),
        "data2": np.random.randn(n_rows),
        "data3": np.random.randn(n_rows),
        "category": np.random.choice(["X", "Y", "Z"], n_rows),
        "timestamp": pd.date_range("2020-01-01", periods=n_rows, freq="H"),
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

    yield csv_path

    # Cleanup
    if csv_path.exists():
        csv_path.unlink()


@pytest.fixture
def malformed_csv(test_data_dir):
    """Create a malformed CSV file for error handling tests."""
    csv_path = test_data_dir / "malformed.csv"

    # Create a CSV with inconsistent columns and delimiters
    malformed_content = """id,name,age
1,Alice,25
2;Bob;30,extra
3,Charlie
4,Diana,28,Finance,extra_field
"5","Eve with,comma",32"""

    with open(csv_path, "w") as f:
        f.write(malformed_content)

    yield csv_path

    # Cleanup
    if csv_path.exists():
        csv_path.unlink()


@pytest.fixture
def different_delimiter_csvs(test_data_dir):
    """Create CSV files with different delimiters for delimiter detection testing."""
    csv_files = {}

    # Sample data
    data = [
        ["id", "name", "value"],
        ["1", "Alice", "100"],
        ["2", "Bob", "200"],
        ["3", "Charlie", "300"],
    ]

    # Different delimiters to test
    delimiters = {
        "comma": ",",
        "semicolon": ";",
        "tab": "\t",
        "pipe": "|",
        "colon": ":",
    }

    for name, delimiter in delimiters.items():
        csv_path = test_data_dir / f"sample_{name}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            for row in data:
                f.write(delimiter.join(row) + "\n")
        csv_files[name] = csv_path

    yield csv_files

    # Cleanup
    for csv_path in csv_files.values():
        if csv_path.exists():
            csv_path.unlink()


@pytest.fixture
def mock_config_file(temp_output_dir):
    """Create a mock configuration file for testing."""
    config_path = temp_output_dir / "test_config.yml"

    config_data = {
        "analysis": {"chunk_size": 5000, "memory_limit_gb": 2, "max_file_size_mb": 100},
        "output": {"format": "html", "include_plots": True, "save_intermediate": False},
        "environments": {
            "main": "csv-profiler-main",
            "profiling": "csv-profiler-profiling",
            "dataprep": "csv-profiler-dataprep",
        },
    }

    with open(config_path, "w") as f:
        yaml.dump(config_data, f, default_flow_style=False)

    yield config_path


@pytest.fixture
def mock_conda_environments():
    """Mock conda environment detection for testing."""
    return {
        "csv-profiler-main": True,
        "csv-profiler-profiling": True,
        "csv-profiler-dataprep": True,
    }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment before each test."""
    # Set environment variables for testing
    original_env = os.environ.copy()
    os.environ["TESTING"] = "1"
    os.environ["DEBUG"] = "1"

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def suppress_warnings():
    """Suppress common warnings during testing."""
    import warnings

    # Suppress specific warnings that are expected during testing
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, module="pkg_resources"
    )
    warnings.filterwarnings("ignore", message=".*pkg_resources.*deprecated.*")
    warnings.filterwarnings("ignore", message=".*declare_namespace.*deprecated.*")
    warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

    yield

    # Reset warning filters
    warnings.resetwarnings()


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line(
        "markers", "environment: marks tests that require specific conda environments"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests that check performance characteristics"
    )
    config.addinivalue_line(
        "markers", "platform: marks tests for platform-specific functionality"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names and paths."""
    for item in items:
        # Add slow marker to tests that are likely to be slow
        if "large" in item.name or "performance" in item.name:
            item.add_marker(pytest.mark.slow)

        # Add integration marker to integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Add environment marker to environment tests
        if "environment" in item.name or "conda" in item.name:
            item.add_marker(pytest.mark.environment)

        # Add performance marker to performance tests
        if "memory" in item.name or "performance" in item.name:
            item.add_marker(pytest.mark.performance)
