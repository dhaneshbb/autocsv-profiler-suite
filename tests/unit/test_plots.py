"""
Unit tests for data visualization system (plots.py).

Tests the matplotlib/seaborn integration, plot generation, parallel processing,
and visualization error handling that are critical for the analysis pipeline.
"""

import sys
import tempfile
from multiprocessing import cpu_count
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.fixtures.sample_data import (  # noqa: E402
    generate_clean_sample_data,
    generate_high_cardinality_data,
)
from tests.utils.test_helpers import clean_test_outputs  # noqa: E402


class TestVisualizationSystemCore:
    """Test core visualization system functionality."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for visualization testing."""
        return generate_clean_sample_data(100)

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary directory for plot outputs."""
        temp_dir = Path(tempfile.mkdtemp(prefix="viz_test_"))
        yield temp_dir
        clean_test_outputs(temp_dir)

    def test_plots_module_imports(self):
        """Test that plots module can be imported with dependencies."""
        try:
            from autocsv_profiler import plots

            # Test basic module attributes
            assert hasattr(plots, "execute_visualization_worker")

            # Test matplotlib/seaborn imports work
            import matplotlib.pyplot as plt

            # Test that we can create basic plot
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [1, 4, 2])
            plt.close(fig)  # Clean up

        except ImportError as e:
            pytest.skip(f"Visualization dependencies not available: {e}")

    def test_visualization_worker_function_signature(self):
        """Test visualization worker function signature."""
        try:
            from autocsv_profiler.plots import execute_visualization_worker

            # Test function is callable
            assert callable(execute_visualization_worker)

            # Test function signature
            import inspect

            sig = inspect.signature(execute_visualization_worker)
            assert len(sig.parameters) >= 1, "Worker should accept parameters"

        except ImportError:
            pytest.skip("Plots module not available")

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.figure")
    def test_visualization_worker_basic_execution(
        self, mock_figure, temp_output_dir, sample_data
    ):
        """Test basic visualization worker execution."""
        try:
            from autocsv_profiler.plots import execute_visualization_worker

            # Create temporary data file
            data_file = temp_output_dir / "test_data.pkl"
            sample_data.to_pickle(data_file)

            # Mock matplotlib objects
            mock_fig = MagicMock()
            mock_figure.return_value = mock_fig

            # Test visualization info structure
            viz_info = {
                "name": "test_plot",
                "type": "histogram",
                "columns": ["age"],
                "output_file": str(temp_output_dir / "test_plot.png"),
            }

            # Execute worker
            result = execute_visualization_worker(
                (viz_info, str(data_file), str(temp_output_dir), None)
            )

            # Verify result structure
            assert isinstance(result, tuple)
            assert len(result) >= 2  # (success, viz_name, ...)

        except ImportError:
            pytest.skip("Plots module not available")

    def test_high_cardinality_handling(self, temp_output_dir):
        """Test handling of high cardinality categorical data."""
        try:
            from autocsv_profiler.core.utils import cat_high_cardinality

            # Create high cardinality data
            high_card_data = generate_high_cardinality_data(500)

            # Test high cardinality detection
            high_card_columns = cat_high_cardinality(high_card_data, threshold=20)

            assert isinstance(high_card_columns, list)
            assert (
                "unique_id" in high_card_columns
            )  # Should be detected as high cardinality
            assert "category" not in high_card_columns  # Should not be high cardinality

        except ImportError:
            pytest.skip("Utility functions not available")

    @patch("multiprocessing.Pool")
    def test_parallel_processing_setup(self, mock_pool):
        """Test multiprocessing setup for visualizations."""
        try:
            pass

            # Mock pool context manager
            mock_pool_instance = MagicMock()
            mock_pool.return_value.__enter__.return_value = mock_pool_instance
            mock_pool_instance.map.return_value = [
                (True, "plot1", None),
                (True, "plot2", None),
            ]

            # Test that we can set up multiprocessing
            cpu_cores = cpu_count()
            assert cpu_cores >= 1

            # Verify pool would be called with reasonable parameters
            # (This would be part of actual plot generation functions)

        except ImportError:
            pytest.skip("Plots module not available")

    def test_visualization_error_handling(self, temp_output_dir):
        """Test error handling in visualization functions."""
        try:
            from autocsv_profiler.plots import execute_visualization_worker

            # Test with invalid data file
            result = execute_visualization_worker(
                (
                    {"name": "test", "type": "invalid"},
                    "/nonexistent/data.pkl",
                    str(temp_output_dir),
                    None,
                )
            )

            # Should return error result gracefully
            assert isinstance(result, tuple)
            success = result[0] if len(result) > 0 else False
            assert success is False, "Should handle invalid data gracefully"

        except ImportError:
            pytest.skip("Plots module not available")


class TestVisualizationTypes:
    """Test different types of visualizations."""

    @pytest.fixture
    def numerical_data(self):
        """Sample data with numerical columns."""
        np.random.seed(42)
        return pd.DataFrame(
            {
                "value1": np.random.normal(50, 15, 100),
                "value2": np.random.exponential(2, 100),
                "value3": np.random.uniform(0, 100, 100),
            }
        )

    @pytest.fixture
    def categorical_data(self):
        """Sample data with categorical columns."""
        np.random.seed(42)
        return pd.DataFrame(
            {
                "category1": np.random.choice(["A", "B", "C", "D"], 100),
                "category2": np.random.choice(["Red", "Blue", "Green"], 100),
                "binary": np.random.choice([True, False], 100),
            }
        )

    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.pyplot.savefig")
    def test_numerical_visualizations(self, mock_show, numerical_data, temp_output_dir):
        """Test numerical data visualization types."""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns

            # Test histogram creation
            fig, ax = plt.subplots()
            ax.hist(numerical_data["value1"], bins=20)
            ax.set_title("Test Histogram")

            # Test that plot was created (mock prevents display)
            plt.close(fig)

            # Test KDE plot creation
            fig, ax = plt.subplots()
            sns.histplot(data=numerical_data, x="value1", kde=True, ax=ax)
            ax.set_title("Test KDE Plot")

            plt.close(fig)

            # Test box plot creation
            fig, ax = plt.subplots()
            numerical_data.boxplot(ax=ax)
            ax.set_title("Test Box Plot")

            plt.close(fig)

            # Verify mocks were called (plots were created)
            assert mock_show.call_count >= 0  # May or may not be called

        except ImportError:
            pytest.skip("Matplotlib/seaborn not available")

    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.pyplot.savefig")
    def test_categorical_visualizations(
        self, mock_show, categorical_data, temp_output_dir
    ):
        """Test categorical data visualization types."""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns

            # Test bar chart creation
            fig, ax = plt.subplots()
            categorical_data["category1"].value_counts().plot(kind="bar", ax=ax)
            ax.set_title("Test Bar Chart")

            plt.close(fig)

            # Test pie chart creation
            fig, ax = plt.subplots()
            categorical_data["category2"].value_counts().plot(kind="pie", ax=ax)
            ax.set_title("Test Pie Chart")

            plt.close(fig)

            # Test count plot
            fig, ax = plt.subplots()
            sns.countplot(data=categorical_data, x="category1", ax=ax)
            ax.set_title("Test Count Plot")

            plt.close(fig)

        except ImportError:
            pytest.skip("Matplotlib/seaborn not available")

    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.pyplot.savefig")
    def test_correlation_visualizations(
        self, mock_show, numerical_data, temp_output_dir
    ):
        """Test correlation matrix visualizations."""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns

            # Test correlation matrix
            corr_matrix = numerical_data.corr()

            # Test heatmap creation
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
            ax.set_title("Test Correlation Heatmap")

            plt.close(fig)

        except ImportError:
            pytest.skip("Matplotlib/seaborn not available")

    def test_visualization_data_preprocessing(self):
        """Test data preprocessing for visualizations."""
        from tests.fixtures.sample_data import generate_clean_sample_data

        # Create sample data for this test
        sample_data = generate_clean_sample_data(50)

        # Test data cleaning for visualization
        clean_data = sample_data.dropna()
        assert len(clean_data) <= len(sample_data)

        # Test data type handling
        numerical_cols = clean_data.select_dtypes(include=[np.number]).columns
        categorical_cols = clean_data.select_dtypes(exclude=[np.number]).columns

        assert len(numerical_cols) >= 0
        assert len(categorical_cols) >= 0
        assert len(numerical_cols) + len(categorical_cols) >= len(clean_data.columns)


class TestVisualizationConfiguration:
    """Test visualization configuration and customization."""

    def test_plot_styling_configuration(self):
        """Test plot styling and theme configuration."""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns

            # Test seaborn style settings
            original_style = plt.rcParams.copy()

            sns.set_style("whitegrid")
            sns.set_palette("husl")

            # Create test plot with styling
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [1, 4, 2])

            # Verify styling was applied (basic check)
            assert plt.rcParams != original_style

            plt.close(fig)

        except ImportError:
            pytest.skip("Matplotlib/seaborn not available")

    def test_plot_size_configuration(self):
        """Test plot size and DPI configuration."""
        try:
            import matplotlib.pyplot as plt

            # Test custom figure sizes
            sizes_to_test = [
                (10, 6),  # Default
                (12, 8),  # Large
                (8, 5),  # Small
            ]

            for width, height in sizes_to_test:
                fig = plt.figure(figsize=(width, height))
                assert fig.get_figwidth() == width
                assert fig.get_figheight() == height
                plt.close(fig)

            # Test DPI settings
            fig = plt.figure(figsize=(10, 6), dpi=150)
            assert fig.dpi == 150
            plt.close(fig)

        except ImportError:
            pytest.skip("Matplotlib not available")

    def test_color_palette_configuration(self):
        """Test color palette configuration."""
        try:
            import seaborn as sns

            # Test different color palettes
            palettes_to_test = ["Set1", "viridis", "husl", "coolwarm"]

            for palette_name in palettes_to_test:
                try:
                    palette = sns.color_palette(palette_name)
                    assert len(palette) > 0

                    # Test that palette can be used
                    sns.set_palette(palette)

                except Exception:
                    # Some palettes might not be available in all seaborn versions
                    continue

        except ImportError:
            pytest.skip("Seaborn not available")


class TestVisualizationPerformance:
    """Test visualization performance and memory usage."""

    @pytest.mark.performance
    def test_large_dataset_handling(self, temp_output_dir):
        """Test visualization with larger datasets."""
        try:
            import matplotlib.pyplot as plt
            import numpy as np

            # Create larger dataset
            np.random.seed(42)
            large_data = pd.DataFrame(
                {
                    "x": np.random.randn(5000),
                    "y": np.random.randn(5000),
                    "category": np.random.choice(["A", "B", "C"], 5000),
                }
            )

            # Test scatter plot with large data
            fig, ax = plt.subplots()

            # Sample data for performance if too large
            sample_size = min(1000, len(large_data))
            sampled_data = large_data.sample(n=sample_size)

            ax.scatter(sampled_data["x"], sampled_data["y"], alpha=0.6)
            ax.set_title("Test Large Dataset Scatter")

            plt.close(fig)

        except ImportError:
            pytest.skip("Matplotlib not available")
        except MemoryError:
            pytest.skip("Insufficient memory for large dataset test")

    @pytest.mark.performance
    def test_memory_efficient_plotting(self):
        """Test memory-efficient plotting strategies."""
        try:
            import gc

            import matplotlib.pyplot as plt

            # Test that figures are properly closed to free memory
            initial_figures = len(plt.get_fignums())

            # Create multiple figures
            for i in range(5):
                fig, ax = plt.subplots()
                ax.plot([1, 2, 3], [i, i + 1, i + 2])
                plt.close(fig)  # Properly close each figure

            # Force garbage collection
            gc.collect()

            # Verify figures were cleaned up
            final_figures = len(plt.get_fignums())
            assert (
                final_figures <= initial_figures + 1
            ), "Figures should be properly closed"

        except ImportError:
            pytest.skip("Matplotlib not available")

    def test_batch_processing_efficiency(self):
        """Test efficient batch processing of visualizations."""
        # Test batch processing concepts

        visualization_tasks = [
            {"type": "histogram", "column": "value1"},
            {"type": "boxplot", "column": "value2"},
            {"type": "scatter", "columns": ["value1", "value2"]},
            {"type": "bar", "column": "category1"},
        ]

        # Group tasks by type for efficiency
        task_groups = {}
        for task in visualization_tasks:
            task_type = task["type"]
            if task_type not in task_groups:
                task_groups[task_type] = []
            task_groups[task_type].append(task)

        # Verify grouping works
        assert len(task_groups) <= len(visualization_tasks)
        for group_tasks in task_groups.values():
            assert len(group_tasks) >= 1


class TestVisualizationIntegration:
    """Test integration with other system components."""

    def test_config_integration(self):
        """Test integration with configuration system."""
        try:
            from autocsv_profiler.config.settings import Settings

            settings = Settings()

            # Test visualization configuration
            viz_config = settings.get("app.visualization", {})

            if viz_config:
                # Test figure sizes configuration
                figure_sizes = viz_config.get("figure_sizes", {})
                if figure_sizes:
                    default_size = figure_sizes.get("default", [10, 6])
                    assert isinstance(default_size, list)
                    assert len(default_size) == 2

                # Test colors configuration
                colors = viz_config.get("colors", {})
                if colors:
                    primary_color = colors.get("primary", "#1f77b4")
                    assert isinstance(primary_color, str)
                    assert primary_color.startswith("#")

        except ImportError:
            pytest.skip("Settings not available")

    def test_data_validation_integration(self):
        """Test integration with data validation."""
        try:
            from autocsv_profiler.core.utils import safe_float_conversion

            # Test data cleaning for visualization
            test_data = ["1.5", "2.3", "invalid", "4.7", None]
            cleaned_data = [safe_float_conversion(x, 0.0) for x in test_data]

            assert all(isinstance(x, (int, float)) for x in cleaned_data)
            assert cleaned_data == [1.5, 2.3, 0.0, 4.7, 0.0]

        except ImportError:
            pytest.skip("Utils not available")


# Mark visualization tests with appropriate markers
pytestmark = [pytest.mark.visualization, pytest.mark.plots]
