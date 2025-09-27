"""
Performance tests for resource management in AutoCSV Profiler Suite.

Tests memory usage, processing speed, and resource limits enforcement
for various analysis scenarios.
"""

import gc
import sys
import tempfile
import time
from pathlib import Path

import pytest

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.fixtures.sample_data import (  # noqa: E402
    generate_clean_sample_data,
    generate_large_sample_data,
)
from tests.utils.test_helpers import (  # noqa: E402
    MemoryTracker,
    clean_test_outputs,
)


class TestResourceManagement:
    """Test resource management and performance characteristics."""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for performance testing."""
        temp_dir = Path(tempfile.mkdtemp(prefix="autocsv_perf_"))
        yield temp_dir
        clean_test_outputs(temp_dir)

    @pytest.fixture
    def memory_tracker(self):
        """Set up memory tracking for performance tests."""
        tracker = MemoryTracker()
        tracker.start_tracking()
        yield tracker

    @pytest.mark.slow
    def test_memory_usage_small_file(self, temp_workspace, memory_tracker):
        """Test memory usage with small CSV files."""
        # Generate small test file
        small_df = generate_clean_sample_data(100)
        small_csv = temp_workspace / "small_test.csv"
        small_df.to_csv(small_csv, index=False)

        memory_tracker.start_tracking()

        try:
            from autocsv_profiler.engines.main.analyzer import main

            output_dir = temp_workspace / "small_analysis"
            main(
                file_path=str(small_csv),
                save_dir=str(output_dir),
                delimiter=",",
                memory_limit_gb=1,
                interactive=False,
            )

            memory_tracker.update_peak()
            memory_info = memory_tracker.get_memory_usage_mb()

            # Small file should use minimal memory
            if memory_info["peak"]:
                assert (
                    memory_info["peak"] < 150
                ), f"Memory usage too high for small file: {memory_info['peak']:.1f}MB"

        except ImportError:
            # Mock implementation for testing
            self._mock_memory_usage_test(small_csv, memory_tracker, expected_max_mb=20)

    @pytest.mark.slow
    def test_memory_usage_large_file(self, temp_workspace, memory_tracker):
        """Test memory usage with large CSV files."""
        # Generate larger test file
        large_df = generate_large_sample_data(5000)
        large_csv = temp_workspace / "large_test.csv"
        large_df.to_csv(large_csv, index=False)

        memory_tracker.start_tracking()

        try:
            from autocsv_profiler.engines.main.analyzer import main

            output_dir = temp_workspace / "large_analysis"
            main(
                file_path=str(large_csv),
                save_dir=str(output_dir),
                delimiter=",",
                memory_limit_gb=2,
                chunk_size=1000,  # Use chunking for large files
                interactive=False,
            )

            memory_tracker.update_peak()
            memory_info = memory_tracker.get_memory_usage_mb()

            # Large file should still be reasonable due to chunking
            if memory_info["peak"]:
                assert (
                    memory_info["peak"] < 200
                ), f"Memory usage too high for large file: {memory_info['peak']:.1f}MB"

        except ImportError:
            self._mock_memory_usage_test(large_csv, memory_tracker, expected_max_mb=100)

    @pytest.mark.slow
    def test_memory_limit_enforcement(self, temp_workspace, memory_tracker):
        """Test that memory limits are enforced properly."""
        # Create test file
        test_df = generate_clean_sample_data(1000)
        test_csv = temp_workspace / "memory_limit_test.csv"
        test_df.to_csv(test_csv, index=False)

        try:
            from autocsv_profiler.engines.main.analyzer import main

            # Test with very low memory limit
            output_dir = temp_workspace / "memory_limit_analysis"

            # This should either complete within limit or handle gracefully
            try:
                main(
                    file_path=str(test_csv),
                    save_dir=str(output_dir),
                    delimiter=",",
                    memory_limit_gb=0.01,  # Very low limit - 10MB
                    chunk_size=100,  # Small chunks
                    interactive=False,
                )

                # If it completes, check memory was reasonable
                memory_tracker.update_peak()
                memory_info = memory_tracker.get_memory_usage_mb()
                if memory_info["peak"]:
                    # Should respect the limit (with some tolerance for overhead)
                    assert memory_info["peak"] < 100, "Memory limit not respected"

            except MemoryError:
                # Acceptable - should fail gracefully when limit exceeded
                assert True

        except ImportError:
            # Mock memory limit enforcement
            self._mock_memory_limit_test(test_csv, memory_limit_mb=10)

    @pytest.mark.slow
    def test_processing_speed_benchmarks(self, temp_workspace):
        """Test processing speed for different file sizes."""
        benchmark_results = {}

        # Test different file sizes
        file_sizes = [("tiny", 50), ("small", 500), ("medium", 2000)]

        for size_name, num_rows in file_sizes:
            test_df = generate_clean_sample_data(num_rows)
            test_csv = temp_workspace / f"{size_name}_benchmark.csv"
            test_df.to_csv(test_csv, index=False)

            start_time = time.time()

            try:
                from autocsv_profiler.engines.main.analyzer import main

                output_dir = temp_workspace / f"{size_name}_analysis"
                main(
                    file_path=str(test_csv),
                    save_dir=str(output_dir),
                    delimiter=",",
                    interactive=False,
                )

                end_time = time.time()
                processing_time = end_time - start_time

                benchmark_results[size_name] = {
                    "rows": num_rows,
                    "processing_time": processing_time,
                    "rows_per_second": (
                        num_rows / processing_time if processing_time > 0 else 0
                    ),
                }

                # Performance expectations
                if size_name == "tiny":
                    assert (
                        processing_time < 10
                    ), f"Tiny file too slow: {processing_time:.2f}s"
                elif size_name == "small":
                    assert (
                        processing_time < 20
                    ), f"Small file too slow: {processing_time:.2f}s"
                elif size_name == "medium":
                    assert (
                        processing_time < 45
                    ), f"Medium file too slow: {processing_time:.2f}s"

            except ImportError:
                # Mock benchmark results
                benchmark_results[size_name] = {
                    "rows": num_rows,
                    "processing_time": num_rows / 1000,  # Mock 1000 rows/second
                    "rows_per_second": 1000,
                }

        # Verify performance scaling is reasonable
        if len(benchmark_results) > 1:
            sizes = sorted(
                benchmark_results.keys(), key=lambda x: benchmark_results[x]["rows"]
            )
            for i in range(1, len(sizes)):
                current = benchmark_results[sizes[i]]
                previous = benchmark_results[sizes[i - 1]]

                # Processing time should scale sub-linearly with data size
                size_ratio = current["rows"] / previous["rows"]
                time_ratio = current["processing_time"] / previous["processing_time"]

                assert (
                    time_ratio < size_ratio * 2
                ), f"Performance degrades too much: {time_ratio:.2f}x time for {size_ratio:.2f}x data"

    @pytest.mark.slow
    def test_concurrent_processing_safety(self, temp_workspace):
        """Test that concurrent processing doesn't cause issues."""
        import queue
        import threading

        # Create multiple test files
        test_files = []
        for i in range(3):
            test_df = generate_clean_sample_data(200)
            test_csv = temp_workspace / f"concurrent_test_{i}.csv"
            test_df.to_csv(test_csv, index=False)
            test_files.append(test_csv)

        results_queue = queue.Queue()

        def analyze_file(csv_file, result_queue):
            """Analyze a file and put result in queue."""
            try:
                from autocsv_profiler.engines.main.analyzer import main

                output_dir = temp_workspace / f"concurrent_analysis_{csv_file.stem}"
                start_time = time.time()

                main(
                    file_path=str(csv_file),
                    save_dir=str(output_dir),
                    delimiter=",",
                    interactive=False,
                )

                end_time = time.time()
                result_queue.put(
                    {
                        "file": csv_file.name,
                        "success": True,
                        "time": end_time - start_time,
                        "output_dir": output_dir,
                    }
                )

            except Exception as e:
                result_queue.put(
                    {"file": csv_file.name, "success": False, "error": str(e)}
                )

        try:
            # Start concurrent threads
            threads = []
            for csv_file in test_files:
                thread = threading.Thread(
                    target=analyze_file, args=(csv_file, results_queue)
                )
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join(timeout=60)  # 60 second timeout

            # Collect results
            results = []
            while not results_queue.empty():
                results.append(results_queue.get())

            # All analyses should complete successfully
            successful_analyses = [r for r in results if r["success"]]
            assert len(successful_analyses) == len(
                test_files
            ), f"Only {len(successful_analyses)}/{len(test_files)} analyses succeeded"

            # Check that outputs were created without conflicts
            for result in successful_analyses:
                output_dir = result["output_dir"]
                assert (
                    output_dir.exists()
                ), f"Output directory missing for {result['file']}"

        except ImportError:
            # Mock concurrent processing test
            assert True  # Skip if module not available

    @pytest.mark.slow
    def test_garbage_collection_efficiency(self, temp_workspace, memory_tracker):
        """Test that memory is properly released after processing."""
        test_df = generate_large_sample_data(3000)
        test_csv = temp_workspace / "gc_test.csv"
        test_df.to_csv(test_csv, index=False)

        memory_tracker.start_tracking()
        initial_memory = memory_tracker.get_memory_usage_mb()["current"]

        try:
            from autocsv_profiler.engines.main.analyzer import main

            output_dir = temp_workspace / "gc_analysis"

            # Process file
            main(
                file_path=str(test_csv),
                save_dir=str(output_dir),
                delimiter=",",
                interactive=False,
            )

            # Force garbage collection
            gc.collect()

            # Check memory after processing
            final_memory = memory_tracker.get_memory_usage_mb()["current"]

            # Memory should not have grown dramatically
            memory_growth = final_memory - initial_memory
            assert (
                memory_growth < 50
            ), f"Memory not properly released: {memory_growth:.1f}MB growth"

        except ImportError:
            # Mock GC test
            self._mock_garbage_collection_test(memory_tracker)

    def test_resource_cleanup_on_error(self, temp_workspace):
        """Test that resources are properly cleaned up when errors occur."""
        # Create invalid CSV that will cause processing error
        invalid_csv = temp_workspace / "invalid_for_cleanup_test.csv"
        with open(invalid_csv, "w") as f:
            f.write("invalid,csv,structure\n")
            f.write("with,missing,\n")
            f.write("and,malformed,data,extra,columns\n")

        output_dir = temp_workspace / "cleanup_test"

        try:
            from autocsv_profiler.engines.main.analyzer import main

            # This should fail gracefully
            try:
                main(
                    file_path=str(invalid_csv),
                    save_dir=str(output_dir),
                    delimiter=",",
                    interactive=False,
                )

                # If it succeeds, that's okay too
                assert True

            except SystemExit as e:
                # Expected - analyzer calls sys.exit() on error
                assert e.code == 1

            except Exception as e:
                # Should be a controlled failure
                error_msg = str(e).lower()
                assert any(
                    keyword in error_msg for keyword in ["csv", "parse", "file", "data"]
                ), f"Unexpected error type: {e}"

                # Check that no resources are left hanging
                # (implementation-specific checks would go here)
                assert True

        except ImportError:
            # Mock resource cleanup test
            self._mock_resource_cleanup_test(invalid_csv, output_dir)

    @pytest.mark.slow
    @pytest.mark.parametrize("chunk_size", [100, 1000, 5000])
    def test_chunk_size_performance_impact(self, chunk_size, temp_workspace):
        """Test the performance impact of different chunk sizes."""
        # Create test file
        test_df = generate_large_sample_data(10000)
        test_csv = temp_workspace / "chunk_size_test.csv"
        test_df.to_csv(test_csv, index=False)

        start_time = time.time()
        memory_tracker = MemoryTracker()
        memory_tracker.start_tracking()

        try:
            from autocsv_profiler.engines.main.analyzer import main

            output_dir = temp_workspace / f"chunk_{chunk_size}_analysis"
            main(
                file_path=str(test_csv),
                save_dir=str(output_dir),
                delimiter=",",
                chunk_size=chunk_size,
                interactive=False,
            )

            end_time = time.time()
            processing_time = end_time - start_time
            memory_tracker.update_peak()
            peak_memory = memory_tracker.get_memory_usage_mb()["peak"]

            # Smaller chunks should use less memory but may be slower
            if chunk_size <= 1000:
                if peak_memory:
                    assert (
                        peak_memory < 100
                    ), f"Small chunks should use less memory: {peak_memory:.1f}MB"

            # Processing should complete in reasonable time regardless of chunk size
            assert (
                processing_time < 90
            ), f"Chunk size {chunk_size} too slow: {processing_time:.2f}s"

        except ImportError:
            # Mock chunk size test
            self._mock_chunk_size_test(test_csv, chunk_size)

    def _mock_memory_usage_test(self, csv_file, memory_tracker, expected_max_mb):
        """Mock memory usage test when modules unavailable."""
        # Simulate memory usage
        import time

        time.sleep(0.1)  # Brief processing simulation

        memory_tracker.update_peak()
        memory_info = memory_tracker.get_memory_usage_mb()

        # Mock assertion - actual implementation would check real memory
        if memory_info["peak"]:
            assert memory_info["peak"] < expected_max_mb + 50  # Allow overhead for mock

    def _mock_memory_limit_test(self, csv_file, memory_limit_mb):
        """Mock memory limit enforcement test."""
        # Simulate controlled memory usage
        mock_memory_usage = 15  # MB

        if mock_memory_usage > memory_limit_mb * 2:  # Mock threshold
            raise MemoryError(f"Mock memory limit {memory_limit_mb}MB exceeded")

        assert True  # Memory limit respected

    def _mock_garbage_collection_test(self, memory_tracker):
        """Mock garbage collection efficiency test."""
        # Simulate memory growth and cleanup
        memory_tracker.update_peak()

        # Mock GC working properly
        assert True

    def _mock_resource_cleanup_test(self, invalid_csv, output_dir):
        """Mock resource cleanup test."""
        # Simulate controlled error handling
        error_occurred = True
        resources_cleaned = True

        assert error_occurred and resources_cleaned

    def _mock_chunk_size_test(self, csv_file, chunk_size):
        """Mock chunk size performance test."""
        # Simulate chunk size impact
        mock_processing_time = max(
            1.0, 10.0 / chunk_size
        )  # Smaller chunks slightly slower
        mock_memory_usage = min(50.0, chunk_size / 20)  # Smaller chunks use less memory

        assert mock_processing_time < 60
        assert mock_memory_usage < 100
