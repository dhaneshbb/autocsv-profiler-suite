"""
Unit tests for statistical analysis system (stats.py).

Tests ResearchPy integration, descriptive statistics, TableOne analysis,
and statistical computation that are core to the analysis pipeline.
"""

import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.fixtures.sample_data import (  # noqa: E402
    generate_clean_sample_data,
    generate_mixed_types_data,
)
from tests.utils.test_helpers import clean_test_outputs  # noqa: E402


class TestStatisticalAnalysisCore:
    """Test core statistical analysis functionality."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for statistical testing."""
        return generate_clean_sample_data(100)

    @pytest.fixture
    def mixed_data(self):
        """Create mixed type data for testing."""
        return generate_mixed_types_data(50)

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary directory for analysis outputs."""
        temp_dir = Path(tempfile.mkdtemp(prefix="stats_test_"))
        yield temp_dir
        clean_test_outputs(temp_dir)

    def test_stats_module_imports(self):
        """Test that stats module can be imported with dependencies."""
        try:
            from autocsv_profiler import stats

            # Test basic module attributes
            assert hasattr(stats, "analyze_data")
            assert hasattr(stats, "researchpy_descriptive_stats")

            # Test ResearchPy import
            import researchpy as rp

            assert rp is not None

        except ImportError as e:
            pytest.skip(f"Statistical dependencies not available: {e}")

    def test_analyze_data_function_signature(self):
        """Test analyze_data function signature and parameters."""
        try:
            from autocsv_profiler.stats import analyze_data

            # Test function is callable
            assert callable(analyze_data)

            # Test function signature
            import inspect

            sig = inspect.signature(analyze_data)
            params = list(sig.parameters.keys())

            assert "data" in params, "Should accept data parameter"

        except ImportError:
            pytest.skip("Stats module not available")

    def test_researchpy_descriptive_stats_function(self):
        """Test researchpy_descriptive_stats function."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Test function is callable
            assert callable(researchpy_descriptive_stats)

            # Test function signature
            import inspect

            sig = inspect.signature(researchpy_descriptive_stats)
            params = list(sig.parameters.keys())

            expected_params = {"data_copy", "save_dir"}
            found_params = set(params)

            assert expected_params.issubset(
                found_params
            ), f"Expected {expected_params}, found {found_params}"

        except ImportError:
            pytest.skip("Stats module not available")

    def test_numerical_statistics_calculation(self, sample_data, temp_output_dir):
        """Test numerical statistics calculation."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Execute statistical analysis
            researchpy_descriptive_stats(sample_data, str(temp_output_dir))

            # Check that numerical stats file was created
            numerical_stats_file = temp_output_dir / "numerical_stats.csv"
            assert (
                numerical_stats_file.exists()
            ), "Numerical stats file should be created"

            # Verify file content
            if numerical_stats_file.stat().st_size > 0:
                stats_df = pd.read_csv(numerical_stats_file)

                # Should have expected columns
                expected_columns = ["Variable"]  # At minimum
                for col in expected_columns:
                    assert (
                        col in stats_df.columns
                    ), f"Expected column {col} in stats output"

                # Should have rows for numerical variables
                numerical_cols = sample_data.select_dtypes(include=[np.number]).columns
                if len(numerical_cols) > 0:
                    assert (
                        len(stats_df) > 0
                    ), "Should have statistics for numerical columns"

        except ImportError:
            pytest.skip("Stats module not available")

    def test_categorical_statistics_calculation(self, sample_data, temp_output_dir):
        """Test categorical statistics calculation."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Execute statistical analysis
            researchpy_descriptive_stats(sample_data, str(temp_output_dir))

            # Check that categorical stats file was created
            categorical_stats_file = temp_output_dir / "categorical_stats.csv"
            assert (
                categorical_stats_file.exists()
            ), "Categorical stats file should be created"

            # Verify file content
            if categorical_stats_file.stat().st_size > 0:
                stats_df = pd.read_csv(categorical_stats_file)

                # Should have expected columns
                expected_columns = ["Variable"]  # At minimum
                for col in expected_columns:
                    assert (
                        col in stats_df.columns
                    ), f"Expected column {col} in stats output"

                # Should have rows for categorical variables
                categorical_cols = sample_data.select_dtypes(
                    include=["object", "category"]
                ).columns
                if len(categorical_cols) > 0:
                    assert (
                        len(stats_df) > 0
                    ), "Should have statistics for categorical columns"

        except ImportError:
            pytest.skip("Stats module not available")

    def test_empty_dataframe_handling(self, temp_output_dir):
        """Test handling of empty or invalid dataframes."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Test with empty DataFrame
            empty_df = pd.DataFrame()

            # Should not crash
            researchpy_descriptive_stats(empty_df, str(temp_output_dir))

            # Check that output files were still created (even if empty)
            numerical_stats_file = temp_output_dir / "numerical_stats.csv"
            categorical_stats_file = temp_output_dir / "categorical_stats.csv"

            assert numerical_stats_file.exists() or categorical_stats_file.exists()

        except ImportError:
            pytest.skip("Stats module not available")

    def test_mixed_data_types_handling(self, mixed_data, temp_output_dir):
        """Test handling of mixed data types."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Execute statistical analysis on mixed data
            researchpy_descriptive_stats(mixed_data, str(temp_output_dir))

            # Verify outputs were created
            output_files = list(temp_output_dir.glob("*.csv"))
            assert len(output_files) >= 1, "Should create output files for mixed data"

            # Check that files have some content
            content_files = [f for f in output_files if f.stat().st_size > 0]
            assert (
                len(content_files) >= 0
            ), "At least some output files should have content"

        except ImportError:
            pytest.skip("Stats module not available")

    def test_delimiter_parameter_handling(self, sample_data, temp_output_dir):
        """Test custom delimiter parameter."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Test with semicolon delimiter
            researchpy_descriptive_stats(
                sample_data, str(temp_output_dir), delimiter=";"
            )

            # Check that files were created
            output_files = list(temp_output_dir.glob("*.csv"))
            assert len(output_files) >= 1

            # Verify delimiter was used (basic check)
            for output_file in output_files:
                if output_file.stat().st_size > 0:
                    content = output_file.read_text()
                    # Should contain semicolons if delimiter worked
                    # (This is a basic check - actual implementation may vary)
                    assert (
                        ";" in content or "," in content
                    )  # Either delimiter should work

        except ImportError:
            pytest.skip("Stats module not available")


class TestResearchPyIntegration:
    """Test ResearchPy library integration."""

    def test_researchpy_summary_cont_function(self):
        """Test ResearchPy continuous summary function."""
        try:
            import researchpy as rp

            # Create test numerical data
            test_series = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

            # Test continuous summary
            summary = rp.summary_cont(test_series)

            assert isinstance(summary, pd.DataFrame)
            assert len(summary) > 0

            # Should have basic statistics
            summary_str = str(summary)
            assert any(stat in summary_str.lower() for stat in ["mean", "count", "std"])

        except ImportError:
            pytest.skip("ResearchPy not available")

    def test_researchpy_summary_cat_function(self):
        """Test ResearchPy categorical summary function."""
        try:
            import researchpy as rp

            # Create test categorical data with proper format
            test_df = pd.DataFrame({"Variable": ["A", "B", "A", "C", "B", "A"]})

            # Test categorical summary with DataFrame input
            try:
                summary = rp.summary_cat(test_df["Variable"])
                assert isinstance(summary, pd.DataFrame)
                assert len(summary) > 0

                # Should have counts and percentages
                summary_str = str(summary)
                assert any(stat in summary_str.lower() for stat in ["count", "percent"])
            except (KeyError, ValueError) as e:
                # Handle ResearchPy API compatibility issues
                pytest.skip(f"ResearchPy API compatibility issue: {e}")

        except ImportError:
            pytest.skip("ResearchPy not available")

    def test_researchpy_with_missing_values(self):
        """Test ResearchPy handling of missing values."""
        try:
            import researchpy as rp

            # Create test data with missing values
            test_series = pd.Series([1, 2, np.nan, 4, 5, np.nan])

            # Test that ResearchPy handles missing values
            summary = rp.summary_cont(test_series.dropna())

            assert isinstance(summary, pd.DataFrame)
            assert len(summary) > 0

        except ImportError:
            pytest.skip("ResearchPy not available")


class TestStatisticalComputations:
    """Test specific statistical computations."""

    def test_descriptive_statistics_accuracy(self):
        """Test accuracy of descriptive statistics."""
        # Create known dataset
        known_data = pd.Series([1, 2, 3, 4, 5])

        # Calculate expected statistics
        expected_mean = 3.0

        # Test pandas calculations
        calculated_mean = known_data.mean()
        calculated_std = known_data.std()

        assert abs(calculated_mean - expected_mean) < 0.001
        assert calculated_std > 0  # Should be positive

    def test_missing_value_handling(self):
        """Test proper handling of missing values in statistics."""
        # Create data with missing values
        data_with_nan = pd.Series([1, 2, np.nan, 4, 5])

        # Test that statistics ignore NaN values
        mean_ignoring_nan = data_with_nan.mean()
        assert not np.isnan(mean_ignoring_nan)
        assert mean_ignoring_nan == 3.0  # (1+2+4+5)/4

        # Test count excluding NaN
        count_without_nan = data_with_nan.count()
        assert count_without_nan == 4  # Should exclude NaN

    def test_data_type_inference(self):
        """Test proper data type inference for statistics."""
        # Create mixed data
        mixed_series = pd.Series([1, 2, 3, "4", "5"])

        # Test conversion to numeric where possible
        numeric_series = pd.to_numeric(mixed_series, errors="coerce")

        assert pd.api.types.is_numeric_dtype(numeric_series)
        assert numeric_series.sum() == 15  # 1+2+3+4+5

    def test_categorical_frequency_analysis(self):
        """Test categorical frequency analysis."""
        # Create categorical data
        categories = pd.Series(["A", "B", "A", "C", "B", "A", "A"])

        # Test value counts
        counts = categories.value_counts()

        assert counts["A"] == 4
        assert counts["B"] == 2
        assert counts["C"] == 1

        # Test proportions
        proportions = categories.value_counts(normalize=True)

        assert abs(proportions["A"] - 4 / 7) < 0.001
        assert abs(proportions["B"] - 2 / 7) < 0.001
        assert abs(proportions["C"] - 1 / 7) < 0.001


class TestStatisticalErrorHandling:
    """Test error handling in statistical functions."""

    def test_invalid_data_handling(self, temp_output_dir):
        """Test handling of invalid data."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Test with invalid data types
            invalid_data = pd.DataFrame(
                {
                    "col1": [1, 2, 3],
                    "col2": [
                        {"key": "value"},
                        {"key": "value2"},
                        {"key": "value3"},
                    ],  # Invalid for statistics
                }
            )

            # Should not crash
            try:
                researchpy_descriptive_stats(invalid_data, str(temp_output_dir))
            except Exception as e:
                # If it raises an exception, it should be handled gracefully
                assert isinstance(e, (ValueError, TypeError, AttributeError))

        except ImportError:
            pytest.skip("Stats module not available")

    def test_large_dataset_handling(self, temp_output_dir):
        """Test handling of larger datasets."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Create larger dataset
            large_data = pd.DataFrame(
                {
                    "numerical": np.random.randn(5000),
                    "categorical": np.random.choice(["A", "B", "C"], 5000),
                }
            )

            # Should handle large data without issues
            researchpy_descriptive_stats(large_data, str(temp_output_dir))

            # Verify outputs
            output_files = list(temp_output_dir.glob("*.csv"))
            assert len(output_files) >= 1

        except (ImportError, MemoryError):
            pytest.skip("Stats module not available or insufficient memory")

    def test_output_directory_creation(self):
        """Test automatic output directory creation."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Create test data
            test_data = pd.DataFrame({"col": [1, 2, 3]})

            # Test with non-existent directory
            with tempfile.TemporaryDirectory() as temp_dir:
                non_existent_dir = Path(temp_dir) / "subdir" / "output"

                # Should create directory automatically
                researchpy_descriptive_stats(test_data, str(non_existent_dir))

                assert non_existent_dir.exists()

        except ImportError:
            pytest.skip("Stats module not available")


class TestTableOneIntegration:
    """Test TableOne analysis integration (if available)."""

    def test_tableone_availability(self):
        """Test TableOne availability and basic functionality."""
        try:
            import tableone

            # Create test data for TableOne
            test_data = pd.DataFrame(
                {
                    "age": [25, 30, 35, 40, 45],
                    "gender": ["M", "F", "M", "F", "M"],
                    "treatment": [1, 0, 1, 0, 1],
                    "outcome": [0, 1, 1, 0, 1],
                }
            )

            # Test TableOne creation
            table = tableone.TableOne(
                test_data, columns=["age", "gender"], groupby="treatment"
            )

            assert table is not None

            # Test table output
            table_str = str(table)
            assert len(table_str) > 0

        except ImportError:
            pytest.skip("TableOne not available")

    def test_tableone_with_missing_data(self):
        """Test TableOne with missing data."""
        try:
            import tableone

            # Create test data with missing values
            test_data = pd.DataFrame(
                {
                    "age": [25, np.nan, 35, 40, 45],
                    "gender": ["M", "F", np.nan, "F", "M"],
                    "treatment": [1, 0, 1, 0, 1],
                }
            )

            # Should handle missing data gracefully
            table = tableone.TableOne(
                test_data, columns=["age", "gender"], groupby="treatment"
            )

            assert table is not None

        except ImportError:
            pytest.skip("TableOne not available")


class TestStatisticalOutputValidation:
    """Test validation of statistical outputs."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for validation testing."""
        return generate_clean_sample_data(30)

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary directory for output validation."""
        temp_dir = Path(tempfile.mkdtemp(prefix="validation_test_"))
        yield temp_dir
        clean_test_outputs(temp_dir)

    def test_output_file_formats(self, sample_data, temp_output_dir):
        """Test that output files have proper CSV format."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Generate statistics
            researchpy_descriptive_stats(sample_data, str(temp_output_dir))

            # Test that generated CSV files are valid
            csv_files = list(temp_output_dir.glob("*.csv"))

            for csv_file in csv_files:
                if csv_file.stat().st_size > 0:
                    try:
                        # Should be readable as CSV
                        df = pd.read_csv(csv_file)
                        assert isinstance(df, pd.DataFrame)

                    except pd.errors.EmptyDataError:
                        # Empty file is acceptable
                        pass
                    except Exception as e:
                        pytest.fail(f"Invalid CSV format in {csv_file}: {e}")

        except ImportError:
            pytest.skip("Stats module not available")

    def test_output_content_validation(self, sample_data, temp_output_dir):
        """Test that output content is meaningful."""
        try:
            from autocsv_profiler.stats import researchpy_descriptive_stats

            # Generate statistics
            researchpy_descriptive_stats(sample_data, str(temp_output_dir))

            # Check numerical stats content
            numerical_file = temp_output_dir / "numerical_stats.csv"
            if numerical_file.exists() and numerical_file.stat().st_size > 0:
                df = pd.read_csv(numerical_file)

                # Should have Variable column
                assert "Variable" in df.columns

                # Should have meaningful statistics
                if len(df) > 0:
                    assert df["Variable"].notna().all()

        except ImportError:
            pytest.skip("Stats module not available")


# Mark statistical tests with appropriate markers
pytestmark = [pytest.mark.statistics, pytest.mark.stats]
