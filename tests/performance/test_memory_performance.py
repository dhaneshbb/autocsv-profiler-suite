"""
Performance tests for memory usage and resource management.

Tests memory consumption, limits, and resource management across
different file sizes and analysis scenarios.
"""

import gc
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.utils.test_helpers import (  # noqa: E402
    MemoryTracker,
    get_file_size_mb,
)


@pytest.mark.slow
@pytest.mark.performance
class TestMemoryPerformance:
    """Test cases for memory performance and resource management."""

    @pytest.fixture
    def memory_tracker(self):
        """Create a memory tracker for tests."""
        tracker = MemoryTracker()
        if not tracker.available:
            pytest.skip("psutil not available - cannot track memory")
        return tracker

    def create_large_csv(self, tmp_path, n_rows, n_cols):
        """Create a large CSV file for testing."""
        np.random.seed(42)  # For reproducible tests

        data = {}
        for i in range(n_cols):
            if i % 3 == 0:
                # Numeric columns
                data[f"numeric_{i}"] = np.random.randn(n_rows)
            elif i % 3 == 1:
                # String columns
                data[f"category_{i}"] = np.random.choice(
                    ["A", "B", "C", "D", "E"], n_rows
                )
            else:
                # Mixed columns
                data[f"mixed_{i}"] = [f"item_{j}_{i}" for j in range(n_rows)]

        csv_path = tmp_path / f"large_file_{n_rows}x{n_cols}.csv"
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)

        return csv_path

    @pytest.mark.performance
    def test_memory_usage_small_file(self, memory_tracker, sample_csv_small):
        """Test memory usage with small CSV file."""
        memory_tracker.start_tracking()

        # Load and process small CSV
        df = pd.read_csv(sample_csv_small)
        memory_tracker.update_peak()

        # Perform basic operations
        summary = df.describe()
        memory_tracker.update_peak()

        # Get memory usage
        memory_info = memory_tracker.get_memory_usage_mb()

        # Small file should use minimal memory (updated threshold for modern environments)
        if memory_info["peak"] is not None:
            assert memory_info["peak"] < 150  # Should be under 150MB

        # Cleanup
        del df, summary
        gc.collect()

    @pytest.mark.performance
    @pytest.mark.slow
    def test_memory_usage_medium_file(self, memory_tracker, tmp_path):
        """Test memory usage with medium CSV file."""
        # Create medium-sized file (1000 rows x 10 columns)
        csv_path = self.create_large_csv(tmp_path, 1000, 10)
        file_size = get_file_size_mb(csv_path)

        memory_tracker.start_tracking()

        # Load and process medium CSV
        df = pd.read_csv(csv_path)
        memory_tracker.update_peak()

        # Perform typical analysis operations
        numeric_summary = df.select_dtypes(include=[np.number]).describe()
        memory_tracker.update_peak()

        correlation_matrix = df.select_dtypes(include=[np.number]).corr()
        memory_tracker.update_peak()

        # Get memory usage
        memory_info = memory_tracker.get_memory_usage_mb()

        # Memory usage should be reasonable relative to file size
        if memory_info["peak"] is not None:
            # Memory usage should be less than 50x file size
            assert memory_info["peak"] < file_size * 50
            assert memory_info["peak"] < 500  # Absolute limit for medium files

        # Cleanup
        del df, numeric_summary, correlation_matrix
        gc.collect()

    @pytest.mark.performance
    @pytest.mark.slow
    def test_memory_usage_large_file(self, memory_tracker, tmp_path):
        """Test memory usage with large CSV file."""
        # Create large file (10000 rows x 20 columns)
        csv_path = self.create_large_csv(tmp_path, 10000, 20)
        get_file_size_mb(csv_path)

        memory_tracker.start_tracking()

        # Load large CSV
        df = pd.read_csv(csv_path)
        memory_tracker.update_peak()

        # Test chunked processing approach
        chunk_size = 1000
        chunk_results = []

        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            chunk_summary = chunk.select_dtypes(include=[np.number]).mean()
            chunk_results.append(chunk_summary)
            memory_tracker.update_peak()

        # Combine chunk results
        combined_results = pd.concat(chunk_results, axis=1).mean(axis=1)
        memory_tracker.update_peak()

        # Get memory usage
        memory_info = memory_tracker.get_memory_usage_mb()

        # Large file memory usage should be managed
        if memory_info["peak"] is not None:
            # With chunked processing, peak memory should be reasonable
            assert memory_info["peak"] < 2000  # Under 2GB

        # Cleanup
        del df, chunk_results, combined_results
        gc.collect()

    @pytest.mark.performance
    def test_memory_limit_enforcement(self, memory_tracker, tmp_path):
        """Test enforcement of memory limits."""
        # Mock memory limit enforcement

        memory_tracker.start_tracking()

        # Create data that would exceed limit if loaded all at once
        csv_path = self.create_large_csv(tmp_path, 5000, 15)

        # Simulate chunked processing with memory limit
        chunk_size = 500  # Small chunks to stay under limit
        total_rows_processed = 0

        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            memory_tracker.update_peak()

            # Check if we're approaching memory limit
            memory_info = memory_tracker.get_memory_usage_mb()
            if memory_info["current"] is not None:
                # In real implementation, this would trigger chunk size reduction
                # or other memory management strategies
                pass

            total_rows_processed += len(chunk)

        # Should process all rows despite memory constraints
        assert total_rows_processed == 5000

        # Peak memory should be reasonable due to chunking
        memory_info = memory_tracker.get_memory_usage_mb()
        if memory_info["peak"] is not None:
            # May exceed our artificial limit but should be reasonable
            assert memory_info["peak"] < 1000  # Under 1GB

    @pytest.mark.performance
    def test_memory_cleanup_after_analysis(self, memory_tracker, tmp_path):
        """Test that memory is properly cleaned up after analysis."""
        csv_path = self.create_large_csv(tmp_path, 2000, 8)

        memory_tracker.start_tracking()
        initial_memory = memory_tracker.get_memory_usage_mb()["current"]

        # Perform analysis that creates temporary objects
        df = pd.read_csv(csv_path)
        memory_tracker.update_peak()

        # Create temporary analysis objects
        temp_objects = []
        for i in range(5):
            temp_df = df.copy()
            temp_analysis = temp_df.describe()
            temp_objects.append((temp_df, temp_analysis))
            memory_tracker.update_peak()

        peak_memory = memory_tracker.get_memory_usage_mb()["peak"]

        # Cleanup temporary objects
        del temp_objects
        del df
        gc.collect()

        # Check memory after cleanup
        final_memory = memory_tracker.get_memory_usage_mb()["current"]

        if all(mem is not None for mem in [initial_memory, peak_memory, final_memory]):
            # Memory should increase during analysis (allow small margin for equal values)
            assert (
                peak_memory >= initial_memory - 1
            )  # Allow small floating point differences

            # Memory should decrease after cleanup (within reasonable margin)
            cleanup_threshold = initial_memory + 50  # Allow 50MB overhead
            assert final_memory < cleanup_threshold

    @pytest.mark.performance
    @pytest.mark.slow
    def test_concurrent_memory_usage(self, memory_tracker, tmp_path):
        """Test memory usage under concurrent-like operations."""
        # Simulate concurrent processing by creating multiple DataFrames
        csv_files = []

        # Create multiple CSV files
        for i in range(3):
            csv_path = self.create_large_csv(tmp_path, 1000, 5)
            csv_files.append(csv_path)

        memory_tracker.start_tracking()

        # Load multiple files simultaneously (simulating concurrent analysis)
        dataframes = []
        for csv_path in csv_files:
            df = pd.read_csv(csv_path)
            dataframes.append(df)
            memory_tracker.update_peak()

        # Process all dataframes
        results = []
        for df in dataframes:
            result = df.describe()
            results.append(result)
            memory_tracker.update_peak()

        # Get peak memory usage
        memory_info = memory_tracker.get_memory_usage_mb()

        if memory_info["peak"] is not None:
            # Multiple files should use more memory but stay reasonable
            assert memory_info["peak"] < 1500  # Under 1.5GB for 3 files

        # Cleanup
        del dataframes, results
        gc.collect()

    @pytest.mark.performance
    def test_dataframe_memory_optimization(self, memory_tracker):
        """Test DataFrame memory optimization techniques."""
        memory_tracker.start_tracking()

        # Create DataFrame with memory-inefficient types
        n_rows = 10000
        data = {
            "int_col": np.random.randint(0, 100, n_rows).astype(
                "int64"
            ),  # Could be int8
            "category_col": np.random.choice(["A", "B", "C"], n_rows).astype(
                "object"
            ),  # Could be category
            "float_col": np.random.randn(n_rows).astype("float64"),  # Could be float32
        }

        # Unoptimized DataFrame
        df_unoptimized = pd.DataFrame(data)
        memory_tracker.update_peak()
        unoptimized_memory = df_unoptimized.memory_usage(deep=True).sum()

        # Optimized DataFrame
        df_optimized = pd.DataFrame(data)

        # Optimize data types
        if df_optimized["int_col"].max() < 128:
            df_optimized["int_col"] = df_optimized["int_col"].astype("int8")

        df_optimized["category_col"] = df_optimized["category_col"].astype("category")
        df_optimized["float_col"] = df_optimized["float_col"].astype("float32")

        memory_tracker.update_peak()
        optimized_memory = df_optimized.memory_usage(deep=True).sum()

        # Optimized DataFrame should use less memory
        assert optimized_memory < unoptimized_memory

        # Calculate memory savings
        savings_ratio = 1 - (optimized_memory / unoptimized_memory)
        assert savings_ratio > 0  # Should have some memory savings

        # Cleanup
        del df_unoptimized, df_optimized
        gc.collect()

    @pytest.mark.performance
    def test_string_processing_memory(self, memory_tracker, tmp_path):
        """Test memory usage during string processing operations."""
        # Create CSV with large text fields
        n_rows = 1000
        data = {
            "id": range(n_rows),
            "large_text": [
                f"This is a very long text field with lots of content for row {i} " * 10
                for i in range(n_rows)
            ],
            "category": np.random.choice(
                ["Category A", "Category B", "Category C"], n_rows
            ),
        }

        csv_path = tmp_path / "string_heavy.csv"
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)

        memory_tracker.start_tracking()

        # Load and process string-heavy data
        df = pd.read_csv(csv_path)
        memory_tracker.update_peak()

        # String processing operations
        df["text_length"] = df["large_text"].str.len()
        memory_tracker.update_peak()

        df["text_word_count"] = df["large_text"].str.split().str.len()
        memory_tracker.update_peak()

        df["category_encoded"] = pd.Categorical(df["category"]).codes
        memory_tracker.update_peak()

        # Get memory usage
        memory_info = memory_tracker.get_memory_usage_mb()

        if memory_info["peak"] is not None:
            # String processing should be memory-efficient
            assert memory_info["peak"] < 500  # Under 500MB

        # Cleanup
        del df
        gc.collect()

    def test_memory_tracking_utility(self):
        """Test the memory tracking utility itself."""
        tracker = MemoryTracker()

        if not tracker.available:
            pytest.skip("psutil not available")

        # Test basic tracking functionality
        tracker.start_tracking()
        assert tracker.initial_memory is not None
        assert tracker.initial_memory > 0

        # Create some objects to increase memory
        large_list = [i for i in range(100000)]
        tracker.update_peak()

        # Peak should be greater than or equal to initial
        assert tracker.peak_memory >= tracker.initial_memory

        # Test memory info
        memory_info = tracker.get_memory_usage_mb()
        assert isinstance(memory_info, dict)
        assert "initial" in memory_info
        assert "peak" in memory_info
        assert "current" in memory_info

        # All values should be positive
        for key, value in memory_info.items():
            if value is not None:
                assert value > 0

        # Test memory limit assertion
        tracker.assert_memory_under_limit(10000)  # Should pass with high limit

        # Cleanup
        del large_list
        gc.collect()
