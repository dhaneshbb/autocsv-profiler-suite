"""
Functional tests for statistics functionality.

Tests the actual statistical analysis functions and data processing.
"""

import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from autocsv_profiler.stats import (  # noqa: E402
    analyze_data,
    calculate_statistics,
    researchpy_descriptive_stats,
)
from autocsv_profiler.summarize import cat_summary, num_summary  # noqa: E402


class TestStatisticsFunctional:
    """Functional tests for statistics functionality."""

    @pytest.fixture
    def numerical_dataframe(self):
        """Create DataFrame with numerical data for testing."""
        np.random.seed(42)  # For reproducible results

        data = {
            "id": range(1, 101),
            "age": np.random.normal(35, 10, 100).clip(18, 80).astype(int),
            "salary": np.random.normal(60000, 15000, 100).clip(30000, 120000),
            "score": np.random.normal(75, 15, 100).clip(0, 100),
            "rating": np.random.uniform(1, 5, 100),
        }
        return pd.DataFrame(data)

    @pytest.fixture
    def categorical_dataframe(self):
        """Create DataFrame with categorical data for testing."""
        np.random.seed(42)

        categories = ["A", "B", "C", "D"]
        departments = ["Engineering", "Sales", "Marketing", "HR", "Finance"]

        data = {
            "id": range(1, 101),
            "category": np.random.choice(categories, 100),
            "department": np.random.choice(departments, 100),
            "status": np.random.choice(["Active", "Inactive"], 100, p=[0.7, 0.3]),
            "level": np.random.choice(
                ["Junior", "Mid", "Senior"], 100, p=[0.4, 0.4, 0.2]
            ),
        }
        return pd.DataFrame(data)

    @pytest.fixture
    def mixed_dataframe(self):
        """Create DataFrame with mixed data types."""
        np.random.seed(42)

        data = {
            "id": range(1, 51),
            "name": [f"Person_{i}" for i in range(1, 51)],
            "age": np.random.normal(30, 8, 50).clip(20, 60).astype(int),
            "salary": np.random.normal(55000, 12000, 50).clip(35000, 90000),
            "department": np.random.choice(["Tech", "Sales", "Marketing"], 50),
            "active": np.random.choice([True, False], 50, p=[0.8, 0.2]),
            "rating": np.random.uniform(1.0, 5.0, 50),
        }
        return pd.DataFrame(data)

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        temp_dir = Path(tempfile.mkdtemp(prefix="stats_test_"))
        yield temp_dir

        # Cleanup
        import shutil

        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    def test_num_summary_basic(self, numerical_dataframe):
        """Test numerical summary generation."""
        result = num_summary(numerical_dataframe)

        assert isinstance(result, pd.DataFrame)
        assert not result.empty

        # Should have summary statistics for numerical columns
        expected_columns = ["id", "age", "salary", "score", "rating"]
        for col in expected_columns:
            assert col in result.index

        # Check that basic statistics are present
        expected_stats = ["Count", "Mean", "Std", "Min", "Max", "Mode"]
        for stat in expected_stats:
            assert stat in result.columns

    def test_num_summary_statistical_accuracy(self, numerical_dataframe):
        """Test accuracy of numerical summaries."""
        result = num_summary(numerical_dataframe)

        # Verify age statistics (we know the distribution)
        age_stats = result.loc["age"]
        assert age_stats["Count"] == 100
        assert 18 <= age_stats["Min"] <= 25  # Should be clipped
        assert 70 <= age_stats["Max"] <= 80  # Should be clipped
        assert 30 <= age_stats["Mean"] <= 40  # Normal distribution around 35

    def test_cat_summary_basic(self, categorical_dataframe):
        """Test categorical summary generation."""
        result = cat_summary(categorical_dataframe)

        assert isinstance(result, pd.DataFrame)
        assert not result.empty

        # Should have summary for categorical columns (excluding id)
        expected_columns = ["category", "department", "status", "level"]
        for col in expected_columns:
            assert col in result.index

        # Check that basic statistics are present
        expected_stats = ["Count", "Unique", "Top", "Freq"]
        for stat in expected_stats:
            assert stat in result.columns

    def test_cat_summary_statistical_accuracy(self, categorical_dataframe):
        """Test accuracy of categorical summaries."""
        result = cat_summary(categorical_dataframe)

        # Verify category statistics
        category_stats = result.loc["category"]
        assert category_stats["Count"] == 100
        assert category_stats["Unique"] == 4  # A, B, C, D

        # Status should have 2 unique values
        status_stats = result.loc["status"]
        assert status_stats["Unique"] == 2  # Active, Inactive

    def test_calculate_statistics_functionality(self, numerical_dataframe):
        """Test calculate_statistics function."""
        age_series = numerical_dataframe["age"]
        stats = calculate_statistics(age_series)

        assert isinstance(stats, dict)

        # Check all expected statistics are present
        expected_keys = [
            "Count",
            "Mean",
            "Std",
            "Min",
            "25%",
            "50%",
            "75%",
            "Max",
            "Mode",
            "Range",
            "IQR",
            "Variance",
            "Skewness",
            "Kurtosis",
        ]

        for key in expected_keys:
            assert key in stats
            assert isinstance(stats[key], (int, float, np.integer, np.floating))

    def test_calculate_statistics_accuracy(self, numerical_dataframe):
        """Test accuracy of calculate_statistics."""
        salary_series = numerical_dataframe["salary"]
        stats = calculate_statistics(salary_series)

        # Verify calculations
        assert stats["Count"] == len(salary_series)
        assert abs(stats["Mean"] - salary_series.mean()) < 1e-10
        assert abs(stats["Std"] - salary_series.std()) < 1e-10
        assert stats["Min"] == salary_series.min()
        assert stats["Max"] == salary_series.max()
        assert abs(stats["Range"] - (salary_series.max() - salary_series.min())) < 1e-10

    def test_researchpy_descriptive_stats_functionality(
        self, mixed_dataframe, temp_output_dir
    ):
        """Test researchpy descriptive stats function."""
        researchpy_descriptive_stats(mixed_dataframe, temp_output_dir)

        # Check output files are created
        numerical_file = temp_output_dir / "numerical_stats.csv"
        categorical_file = temp_output_dir / "categorical_stats.csv"

        assert numerical_file.exists()
        assert categorical_file.exists()

        # Check file contents
        numerical_df = pd.read_csv(numerical_file)
        categorical_df = pd.read_csv(categorical_file)

        assert not numerical_df.empty
        assert not categorical_df.empty

    def test_researchpy_descriptive_stats_content(
        self, mixed_dataframe, temp_output_dir
    ):
        """Test content of researchpy descriptive stats output."""
        researchpy_descriptive_stats(mixed_dataframe, temp_output_dir)

        # Read and validate numerical stats
        numerical_file = temp_output_dir / "numerical_stats.csv"
        numerical_df = pd.read_csv(numerical_file)

        # Should have age, salary, rating columns
        expected_vars = ["age", "salary", "rating"]
        for var in expected_vars:
            assert var in numerical_df["Variable"].values

        # Read and validate categorical stats
        categorical_file = temp_output_dir / "categorical_stats.csv"
        categorical_df = pd.read_csv(categorical_file)

        # Should have name, department columns
        expected_vars = ["name", "department"]
        for var in expected_vars:
            assert var in categorical_df["Variable"].values

    def test_researchpy_with_custom_delimiter(self, mixed_dataframe, temp_output_dir):
        """Test researchpy stats with custom delimiter."""
        researchpy_descriptive_stats(mixed_dataframe, temp_output_dir, delimiter=";")

        # Files should be created with semicolon delimiter
        numerical_file = temp_output_dir / "numerical_stats.csv"

        # Read file content as text to check delimiter
        content = numerical_file.read_text()
        assert ";" in content

        # Should still be readable as CSV with correct separator
        df = pd.read_csv(numerical_file, sep=";")
        assert not df.empty

    def test_analyze_data_output(self, mixed_dataframe, capsys):
        """Test analyze_data function output."""
        analyze_data(mixed_dataframe)

        # Capture printed output
        captured = capsys.readouterr()
        output = captured.out

        # Should contain analysis sections
        assert "Numerical Analysis" in output or "Categorical Analysis" in output

        # Should contain table format
        assert "|" in output  # Markdown table format

    def test_statistics_with_missing_values(self):
        """Test statistics handling of missing values."""
        # Create data with NaN values
        data = {
            "values": [1, 2, np.nan, 4, 5, np.nan, 7, 8, 9, 10],
            "category": ["A", "B", None, "A", "B", "C", None, "A", "B", "C"],
        }
        df = pd.DataFrame(data)

        # Numerical summary should handle NaN values
        num_result = num_summary(df)
        if not num_result.empty:
            values_stats = num_result.loc["values"]
            assert values_stats["Count"] == 8  # Non-null count

        # Categorical summary should handle NaN values
        cat_result = cat_summary(df)
        if not cat_result.empty:
            category_stats = cat_result.loc["category"]
            assert category_stats["Count"] == 7  # Non-null count

    def test_statistics_edge_cases(self):
        """Test statistics with edge cases."""
        # Empty DataFrame
        empty_df = pd.DataFrame()
        num_result = num_summary(empty_df)
        cat_result = cat_summary(empty_df)

        # Should return empty DataFrames without errors
        assert isinstance(num_result, pd.DataFrame)
        assert isinstance(cat_result, pd.DataFrame)

        # Single row DataFrame
        single_row = pd.DataFrame({"num_col": [42], "cat_col": ["A"]})

        num_result = num_summary(single_row)
        cat_result = cat_summary(single_row)

        assert not num_result.empty
        assert not cat_result.empty

        # Verify single row statistics
        assert num_result.loc["num_col", "Count"] == 1
        assert cat_result.loc["cat_col", "Count"] == 1

    def test_statistics_data_types(self):
        """Test statistics with various data types."""
        data = {
            "int_col": [1, 2, 3, 4, 5],
            "float_col": [1.1, 2.2, 3.3, 4.4, 5.5],
            "str_col": ["a", "b", "c", "d", "e"],
            "bool_col": [True, False, True, False, True],
        }
        df = pd.DataFrame(data)

        num_result = num_summary(df)
        cat_result = cat_summary(df)

        # Numerical columns should be processed
        assert "int_col" in num_result.index
        assert "float_col" in num_result.index

        # String columns should be processed as categorical
        assert "str_col" in cat_result.index
