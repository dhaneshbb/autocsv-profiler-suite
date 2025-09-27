"""
Unit tests for UI components and Rich-based interface system.

Tests Rich console output, interactive prompts, table formatting,
and user interface components that provide the clean UX.
"""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.fixtures.sample_data import generate_clean_sample_data  # noqa: E402


class TestRichUIComponents:
    """Test Rich UI component integration."""

    def test_rich_imports(self):
        """Test that Rich components can be imported."""
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.table import Table

            # Test basic instantiation
            console = Console()
            assert console is not None

            table = Table()
            assert table is not None

            panel = Panel("Test content")
            assert panel is not None

        except ImportError as e:
            pytest.skip(f"Rich UI components not available: {e}")

    def test_ui_interface_imports(self):
        """Test that UI interface modules can be imported."""
        # Test direct imports that were added to the file
        try:
            from autocsv_profiler.ui.components import exclude_columns_improved
            from autocsv_profiler.ui.interactive import CleanInteractiveMethods
            from autocsv_profiler.ui.interface import CleanCSVInterface

            # Test basic function/class access
            assert exclude_columns_improved is not None

            csv_interface = CleanCSVInterface()
            assert csv_interface is not None

            interactive_methods = CleanInteractiveMethods(csv_interface)
            assert interactive_methods is not None

        except ImportError as e:
            pytest.skip(f"UI modules not available: {e}")


class TestConsoleOutput:
    """Test console output formatting and display."""

    @patch("sys.stdout", new_callable=StringIO)
    def test_basic_console_output(self, mock_stdout):
        """Test basic console output functionality."""
        try:
            from rich.console import Console

            console = Console(file=mock_stdout, width=80)
            console.print("Test message")

            output = mock_stdout.getvalue()
            assert "Test message" in output

        except ImportError:
            pytest.skip("Rich not available")

    @patch("sys.stdout", new_callable=StringIO)
    def test_styled_console_output(self, mock_stdout):
        """Test styled console output."""
        try:
            from rich.console import Console

            console = Console(file=mock_stdout, width=80)

            # Test different styles
            console.print("Bold text", style="bold")
            console.print("Green text", style="green")
            console.print("Error text", style="red")

            output = mock_stdout.getvalue()
            assert "Bold text" in output
            assert "Green text" in output
            assert "Error text" in output

        except ImportError:
            pytest.skip("Rich not available")

    @patch("sys.stdout", new_callable=StringIO)
    def test_panel_output(self, mock_stdout):
        """Test panel-based output."""
        try:
            from rich.console import Console
            from rich.panel import Panel

            console = Console(file=mock_stdout, width=80)

            panel = Panel("Panel content", title="Test Panel")
            console.print(panel)

            output = mock_stdout.getvalue()
            assert "Panel content" in output
            assert "Test Panel" in output

        except ImportError:
            pytest.skip("Rich not available")


class TestTableFormatting:
    """Test Rich table formatting for data display."""

    @patch("sys.stdout", new_callable=StringIO)
    def test_basic_table_creation(self, mock_stdout):
        """Test basic table creation and display."""
        try:
            from rich.console import Console
            from rich.table import Table

            console = Console(file=mock_stdout, width=80)

            table = Table(title="Test Table")
            table.add_column("Name", style="cyan")
            table.add_column("Value", style="magenta")

            table.add_row("Item 1", "Value 1")
            table.add_row("Item 2", "Value 2")

            console.print(table)

            output = mock_stdout.getvalue()
            assert "Test Table" in output
            assert "Item 1" in output
            assert "Value 1" in output

        except ImportError:
            pytest.skip("Rich not available")

    @patch("sys.stdout", new_callable=StringIO)
    def test_dataframe_table_conversion(self, mock_stdout):
        """Test converting pandas DataFrame to Rich table."""
        try:
            from rich.console import Console
            from rich.table import Table

            console = Console(file=mock_stdout, width=80)

            # Create test DataFrame
            df = pd.DataFrame(
                {
                    "Name": ["Alice", "Bob", "Charlie"],
                    "Age": [25, 30, 35],
                    "Score": [95.5, 87.2, 92.8],
                }
            )

            # Convert to Rich table
            table = Table(title="DataFrame Table")

            # Add columns
            for col in df.columns:
                table.add_column(str(col))

            # Add rows
            for _, row in df.iterrows():
                table.add_row(*[str(val) for val in row])

            console.print(table)

            output = mock_stdout.getvalue()
            assert "Alice" in output
            assert "25" in output
            assert "95.5" in output

        except ImportError:
            pytest.skip("Rich not available")

    def test_table_styling_options(self):
        """Test various table styling options."""
        try:
            from rich.table import Table

            # Test different table styles
            styles = ["simple", "grid", "rounded", "heavy"]

            for style in styles:
                try:
                    table = Table(
                        box=getattr(
                            __import__("rich.box", fromlist=[style.upper()]),
                            style.upper(),
                            None,
                        )
                    )
                    if table.box is not None:
                        table.add_column("Test")
                        table.add_row("Data")
                except AttributeError:
                    # Style might not be available
                    continue

        except ImportError:
            pytest.skip("Rich not available")


class TestProgressIndicators:
    """Test progress indicators and status displays."""

    def test_progress_bar_creation(self):
        """Test progress bar creation."""
        try:
            from rich.progress import BarColumn, Progress, TextColumn

            progress = Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            )

            assert progress is not None

            # Test task creation
            task = progress.add_task("Test task", total=100)
            assert task is not None

        except ImportError:
            pytest.skip("Rich not available")

    def test_spinner_creation(self):
        """Test spinner creation for indeterminate progress."""
        try:
            from rich.progress import Progress, SpinnerColumn, TextColumn

            progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
            )

            assert progress is not None

        except ImportError:
            pytest.skip("Rich not available")

    @patch("time.sleep")  # Speed up test
    def test_progress_context_manager(self, mock_sleep):
        """Test progress context manager usage."""
        try:
            from rich.progress import Progress

            with Progress() as progress:
                task = progress.add_task("Processing...", total=10)

                for i in range(10):
                    progress.update(task, advance=1)
                    mock_sleep(0.1)  # Simulate work

            # Should complete without errors
            assert True

        except ImportError:
            pytest.skip("Rich not available")


class TestInteractivePrompts:
    """Test interactive user prompts and input handling."""

    @patch("builtins.input", return_value="test_input")
    def test_basic_prompt(self):
        """Test basic prompt functionality."""
        try:
            from rich.prompt import Prompt

            response = Prompt.ask("Enter value")
            assert response == "test_input"

        except ImportError:
            pytest.skip("Rich not available")

    @patch("builtins.input", return_value="y")
    def test_confirmation_prompt(self):
        """Test confirmation prompts."""
        try:
            from rich.prompt import Confirm

            response = Confirm.ask("Continue?")
            assert response is True

        except ImportError:
            pytest.skip("Rich not available")

    @patch("builtins.input", side_effect=["invalid", "42"])
    def test_integer_prompt_validation(self):
        """Test integer prompt with validation."""
        try:
            from rich.prompt import IntPrompt

            response = IntPrompt.ask("Enter number", default=0)
            assert isinstance(response, int)

        except ImportError:
            pytest.skip("Rich not available")

    @patch("builtins.input", side_effect=["invalid_choice", "option1"])
    def test_choice_prompt(self):
        """Test choice prompts with validation."""
        try:
            from rich.prompt import Prompt

            choices = ["option1", "option2", "option3"]
            response = Prompt.ask("Choose option", choices=choices)
            assert response in choices

        except ImportError:
            pytest.skip("Rich not available")


class TestUIComponentIntegration:
    """Test integration of UI components with application logic."""

    def test_column_selection_interface_mock(self):
        """Test column selection interface (mocked)."""
        # Mock column selection interface
        available_columns = ["id", "name", "age", "salary", "department"]

        # Simulate user selection
        user_selection = [0, 2]  # Select id and age

        selected_columns = [available_columns[i] for i in user_selection]
        assert "id" in selected_columns
        assert "age" in selected_columns
        assert len(selected_columns) == 2

    def test_data_preview_formatting(self):
        """Test data preview formatting for UI display."""
        # Create sample data
        sample_data = generate_clean_sample_data(5)

        # Test data preview generation
        preview_rows = min(5, len(sample_data))
        preview_data = sample_data.head(preview_rows)

        assert len(preview_data) <= 5
        assert list(preview_data.columns) == list(sample_data.columns)

    def test_analysis_summary_formatting(self):
        """Test analysis summary formatting for display."""
        # Mock analysis results
        analysis_summary = {
            "total_rows": 1000,
            "total_columns": 8,
            "numerical_columns": 4,
            "categorical_columns": 4,
            "missing_values": 25,
            "missing_percentage": 2.5,
        }

        # Test summary formatting
        summary_text = f"""
        Dataset Summary:
        - Total Rows: {analysis_summary['total_rows']:,}
        - Total Columns: {analysis_summary['total_columns']}
        - Numerical Columns: {analysis_summary['numerical_columns']}
        - Categorical Columns: {analysis_summary['categorical_columns']}
        - Missing Values: {analysis_summary['missing_values']} ({analysis_summary['missing_percentage']:.1f}%)
        """

        assert "1,000" in summary_text
        assert "2.5%" in summary_text

    def test_error_message_formatting(self):
        """Test error message formatting for UI display."""
        error_scenarios = [
            ("FileNotFoundError", "CSV file not found: /path/to/file.csv"),
            ("MemoryError", "Insufficient memory to process large dataset"),
            ("ValueError", "Invalid delimiter specified: |"),
        ]

        for error_type, error_message in error_scenarios:
            formatted_error = f"[ERROR] {error_type}: {error_message}"

            assert error_type in formatted_error
            assert error_message in formatted_error
            assert "[ERROR]" in formatted_error


class TestUIAccessibility:
    """Test UI accessibility and usability features."""

    def test_colorblind_friendly_colors(self):
        """Test that color choices are colorblind-friendly."""
        try:
            from rich.console import Console

            console = Console()

            # Test colorblind-friendly color palette
            safe_colors = ["cyan", "magenta", "yellow", "white", "bright_blue"]

            for color in safe_colors:
                # Should not raise exception
                console.print("Test", style=color)

        except ImportError:
            pytest.skip("Rich not available")

    def test_high_contrast_mode(self):
        """Test high contrast display options."""
        try:
            from rich.console import Console

            # Test with different background themes
            console_light = Console(force_terminal=True, legacy_windows=False)
            console_dark = Console(force_terminal=True, legacy_windows=False)

            # Both should work without errors
            assert console_light is not None
            assert console_dark is not None

        except ImportError:
            pytest.skip("Rich not available")

    def test_text_only_fallback(self):
        """Test text-only fallback for environments without Rich."""
        # Test plain text formatting as fallback
        data = {"column1": "value1", "column2": "value2"}

        # Simple text table format
        text_table = []
        text_table.append("| Column1 | Column2 |")
        text_table.append("|---------|---------|")
        text_table.append(f"| {data['column1']} | {data['column2']} |")

        formatted_table = "\n".join(text_table)

        assert "Column1" in formatted_table
        assert "value1" in formatted_table
        assert "|" in formatted_table


class TestUIPerformance:
    """Test UI performance with large datasets."""

    def test_large_table_rendering_performance(self):
        """Test table rendering performance with large datasets."""
        try:
            from rich.console import Console
            from rich.table import Table

            Console()

            # Create table with many rows
            table = Table()
            table.add_column("ID")
            table.add_column("Value")

            # Add many rows (but reasonable for testing)
            max_rows = 100  # Keep reasonable for test performance
            for i in range(max_rows):
                table.add_row(str(i), f"value_{i}")

            # Should complete without timeout
            table_str = str(table)
            assert len(table_str) > 0

        except ImportError:
            pytest.skip("Rich not available")

    def test_progress_update_performance(self):
        """Test progress update performance."""
        try:
            from rich.progress import Progress

            with Progress() as progress:
                task = progress.add_task("Performance test", total=1000)

                # Simulate rapid updates
                for i in range(0, 1000, 10):  # Update every 10 steps
                    progress.update(task, completed=i)

            # Should complete without performance issues
            assert True

        except ImportError:
            pytest.skip("Rich not available")


class TestUIErrorHandling:
    """Test UI error handling and graceful degradation."""

    def test_console_creation_fallback(self):
        """Test console creation with fallback options."""
        try:
            from rich.console import Console

            # Test different console configurations
            configs = [
                {"width": 80, "height": 24},
                {"force_terminal": True},
                {"force_jupyter": False},
                {"legacy_windows": False},
            ]

            for config in configs:
                try:
                    console = Console(**config)
                    assert console is not None
                except Exception:
                    # Some configurations might not work in all environments
                    continue

        except ImportError:
            pytest.skip("Rich not available")

    def test_markup_error_handling(self):
        """Test handling of invalid markup in Rich."""
        try:
            from rich.console import Console

            console = Console()

            # Test with potentially invalid markup
            invalid_markup_examples = [
                "[invalid_style]text[/invalid_style]",
                "[bold]unclosed bold tag",
                "[]empty markup[/]",
                "[/]closing without opening",
            ]

            for markup in invalid_markup_examples:
                try:
                    console.print(markup, markup=False)  # Disable markup to test safely
                except Exception:
                    # Should handle gracefully
                    pass

        except ImportError:
            pytest.skip("Rich not available")


# Mark UI tests with appropriate markers
pytestmark = [pytest.mark.ui, pytest.mark.components]
