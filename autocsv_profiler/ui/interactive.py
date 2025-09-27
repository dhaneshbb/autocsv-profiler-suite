"""
Clean Interactive Methods for CSV Profiler

Simple, effective interactive methods that work with the clean interface
without complex layout conflicts.
"""

import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from rich import box
from rich.prompt import Confirm, Prompt
from rich.table import Table

from .interface import CleanCSVInterface


class CleanInteractiveMethods:
    """
    Clean interactive methods that work with the clean interface.

    Provides all interactive functionality with simple console interactions
    and clear visual feedback without layout conflicts.
    """

    def __init__(self, clean_interface: CleanCSVInterface):
        self.ui = clean_interface

    def _show_workflow_step(
        self, step_number: int, step_name: str, description: str
    ) -> None:
        """Display standardized workflow step header."""
        from rich import box
        from rich.panel import Panel
        from rich.text import Text

        step_header = Text.assemble(
            (f"Step {step_number}: ", f"bold {self.ui.theme['primary']}"),
            (f"{step_name}", f"bold {self.ui.theme['primary']}"),
            (f"\n{description}", f"{self.ui.theme['muted']}"),
        )

        step_panel = Panel(
            step_header,
            border_style=self.ui.theme["primary"],
            box=box.ROUNDED,
            padding=(0, 1),
        )

        self.ui.console.print()
        self.ui.console.print(step_panel)

    def display_welcome_banner(self) -> bool:
        """Display welcome banner."""
        self.ui.set_step("welcome")
        self.ui.show_welcome()
        return True

    def get_csv_path(self) -> Optional[Path]:
        """Get CSV file path from user."""
        self.ui.set_step("file_selection")

        # Show step header with consistent formatting
        self._show_workflow_step(
            1, "File Selection", "Select your CSV file for analysis"
        )

        while True:
            try:
                # Prompt for file path
                csv_path_str = Prompt.ask(
                    f"[{self.ui.theme['primary']}]Enter the path to your CSV file[/]",
                    console=self.ui.console,
                )

                if not csv_path_str.strip():
                    self.ui.log("WARNING", "No file path entered")
                    continue

                csv_path = Path(csv_path_str.strip().strip("\"'"))

                if not csv_path.exists():
                    self.ui.log("ERROR", f"File not found: {csv_path}")
                    retry = Confirm.ask(
                        f"[{self.ui.theme['warning']}]Would you like to try again?[/]",
                        console=self.ui.console,
                    )
                    if not retry:
                        return None
                    continue

                if not csv_path.suffix.lower() == ".csv":
                    self.ui.log(
                        "WARNING",
                        f"File doesn't have .csv extension: {csv_path}",
                    )
                    proceed = Confirm.ask(
                        f"[{self.ui.theme['warning']}]Continue anyway?[/]",
                        console=self.ui.console,
                    )
                    if not proceed:
                        continue

                # File is valid
                self.ui.set_csv_file(csv_path)
                self.ui.log("SUCCESS", f"Selected file: {csv_path.name}")
                self.ui.console.print()
                return csv_path

            except KeyboardInterrupt:
                self.ui.log("INFO", "File selection cancelled by user")
                return None
            except Exception as e:
                self.ui.log("ERROR", f"Error processing file path: {e}")
                return None

    def setup_output_directory(self, csv_path: Path) -> Tuple[Path, str]:
        """Setup output directory for results."""
        # Show step header with consistent formatting
        self._show_workflow_step(
            2, "Output Directory Setup", "Configure analysis output location"
        )

        csv_folder = csv_path.parent
        filename_no_ext = csv_path.stem

        output_dir = csv_folder / filename_no_ext
        output_dir.mkdir(exist_ok=True)

        # Copy original CSV to output directory
        original_csv_path = output_dir / csv_path.name
        if not original_csv_path.exists():
            import shutil

            shutil.copy2(csv_path, original_csv_path)

        self.ui.log("SUCCESS", f"Output directory created: {output_dir}")
        self.ui.console.print()
        return output_dir, str(original_csv_path)

    def detect_delimiter(self, csv_path: Path) -> Optional[str]:
        """Detect or get delimiter from user."""
        self.ui.set_step("delimiter_detection")

        # Show step header with consistent formatting
        self._show_workflow_step(
            3,
            "Delimiter Detection",
            "Automatically detect or specify CSV delimiter",
        )

        # Try automatic delimiter detection using structural analysis
        try:
            self.ui.log("INFO", "Attempting automatic delimiter detection...")

            delimiter = self._detect_delimiter_structural(csv_path)

            if delimiter:
                self.ui.set_delimiter(delimiter)
                self.ui.log(
                    "SUCCESS",
                    f"Auto-detected delimiter: {repr(delimiter)}",
                )
                self.ui.console.print()
                return delimiter

        except Exception as e:
            self.ui.log("WARNING", f"Auto-detection failed: {e}")

        # Manual delimiter input
        self.ui.console.print(
            "[yellow]Auto-detection failed. Please specify manually.[/yellow]"
        )
        self.ui.console.print()

        while True:
            delimiter = Prompt.ask(
                f"[{self.ui.theme['warning']}]Enter the delimiter used in your CSV file[/] "
                f"[{self.ui.theme['muted']}](common: ',' or ';' or '\\t')[/]",
                console=self.ui.console,
                default=",",
            )

            # Process escape sequences (delimiter cannot be None due to default value)
            assert delimiter is not None
            delimiter = delimiter.replace("\\t", "\t").replace("\\n", "\n")

            if self._is_valid_delimiter(delimiter):
                self.ui.set_delimiter(delimiter)
                self.ui.log("SUCCESS", f"Delimiter set to: {repr(delimiter)}")
                self.ui.console.print()
                return delimiter
            else:
                self.ui.log("ERROR", f"Invalid delimiter: {repr(delimiter)}")
                retry = Confirm.ask(
                    f"[{self.ui.theme['warning']}]Try again?[/]",
                    console=self.ui.console,
                )
                if not retry:
                    return None

    def _detect_delimiter_structural(self, csv_path: Path) -> Optional[str]:
        """Structural delimiter detection by analyzing file structure.

        Uses multi-stage analysis to accurately detect CSV delimiters without
        external dependencies. Analyzes character frequency, consistency, and
        validates with built-in CSV tools.

        Args:
            csv_path: Path to the CSV file

        Returns:
            Detected delimiter or None if detection fails
        """
        import csv
        from collections import Counter

        # Detect file encoding first
        try:
            from charset_normalizer import from_bytes

            with open(csv_path, "rb") as file_handle:
                raw_data = file_handle.read(10000)  # Read first 10KB for detection
                result = from_bytes(raw_data).best()
                if result:
                    detected_encoding = result.encoding
                else:
                    detected_encoding = "utf-8"
        except ImportError:
            detected_encoding = "utf-8"

        with open(
            csv_path, "r", encoding=detected_encoding, errors="replace"
        ) as csvfile:
            # Read substantial sample for analysis (16KB)
            sample = csvfile.read(16384)
            if not sample:
                return None

        lines = [line for line in sample.split("\n") if line.strip()]
        if len(lines) < 2:
            return None

        # Find ALL potential delimiter characters
        # Exclude alphanumeric, quotes, and common text characters
        all_chars = set(sample)
        potential_delimiters = set()

        for char in all_chars:
            # Skip letters, numbers, quotes, and whitespace (except tab)
            if char.isalnum() or char in "\"'`\n\r":
                continue
            # Include printable punctuation and tab
            if char.isprintable() or char == "\t":
                potential_delimiters.add(char)

        best_delimiter = None
        best_score = 0.0

        for delimiter in potential_delimiters:
            # Calculate consistency score
            column_counts = []
            valid_lines = 0

            for line in lines[:20]:  # Analyze first 20 lines
                if not line.strip():
                    continue

                # Count delimiter occurrences
                count = line.count(delimiter)
                if count > 0:
                    column_counts.append(count)
                    valid_lines += 1

            if valid_lines < 2 or not column_counts:
                continue

            # Check consistency (most lines should have same delimiter count)
            most_common_count = Counter(column_counts).most_common(1)[0][0]
            consistency_ratio = column_counts.count(most_common_count) / len(
                column_counts
            )

            # Score: consistency × frequency × coverage
            frequency = most_common_count
            coverage = valid_lines / min(len(lines), 20)

            # Only consider if high consistency (>80%) and multiple columns
            if consistency_ratio >= 0.8 and frequency >= 1:
                score = consistency_ratio * frequency * coverage

                # Bonus for common CSV delimiters
                if delimiter in ",;\t|":
                    score *= 1.2

                if score > best_score:
                    best_score = score
                    best_delimiter = delimiter

        # Validate with csv.Sniffer if we found a candidate
        if best_delimiter:
            try:
                sniffer = csv.Sniffer()
                # Test if our delimiter works with csv module
                dialect = sniffer.sniff(sample[:1024], delimiters=best_delimiter)
                if dialect.delimiter == best_delimiter:
                    return best_delimiter
            except Exception:
                pass

            # Even if sniffer fails, return our best guess if score is high
            if best_score > 2.0:
                return best_delimiter

        # Fallback: try pandas read with auto-detection
        try:
            import pandas as pd

            # Let pandas try to detect delimiter automatically
            df = pd.read_csv(
                csv_path,
                sep=None,
                engine="python",
                nrows=5,
                encoding="utf-8",
                on_bad_lines="skip",
            )
            if hasattr(df, "columns") and len(df.columns) > 1:
                # Try to reverse-engineer the delimiter pandas used
                with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
                    first_line = f.readline().strip()
                    for char in potential_delimiters:
                        if first_line.count(char) == len(df.columns) - 1:
                            return char
        except Exception:
            pass

        return None

    def _is_valid_delimiter(self, delimiter: str) -> bool:
        """Check if delimiter is valid."""
        if not delimiter:
            return False
        if len(delimiter) > 3:  # Reasonable limit
            return False
        return True

    def display_engine_selection_menu(self) -> List[Dict[str, Any]]:
        """Display engine selection menu."""
        self.ui.set_step("engine_selection")

        # Show step header with consistent formatting
        self._show_workflow_step(
            4, "Engine Selection", "Choose analysis engines to run"
        )

        scripts = self.ui.config.get("scripts", [])
        if not scripts:
            self.ui.log("ERROR", "No analysis engines found in configuration")
            return []

        # Display available engines table with consistent styling
        engine_table = Table(
            title="[bold]Available Analysis Engines[/bold]",
            show_header=True,
            header_style=f"bold {self.ui.theme['primary']}",
            box=box.ROUNDED,
            border_style=self.ui.theme["primary"],
        )
        engine_table.add_column(
            "ID", style=self.ui.theme["accent"], width=6, justify="center"
        )
        engine_table.add_column("Engine", style=self.ui.theme["secondary"], width=30)
        engine_table.add_column(
            "Environment",
            style=self.ui.theme["info"],
            width=15,
            justify="center",
        )
        engine_table.add_column("Description", style=self.ui.theme["muted"])

        for script in scripts:
            # Clean up engine name for display
            engine_name = script["name"].replace("engines/", "").replace(".py", "")
            environment = script.get("environment", "main")
            description = script.get("description", "Analysis engine")

            engine_table.add_row(
                str(script["id"]),
                engine_name,
                f"[bold]{environment}[/bold]",
                description,
            )

        self.ui.console.print(engine_table)
        self.ui.console.print()

        # Get user selection
        selected_engines = []
        while True:
            try:
                selection = Prompt.ask(
                    f"[{self.ui.theme['accent']}]Enter engine IDs to run[/] "
                    f"[{self.ui.theme['muted']}](comma-separated, e.g., '1,2,3' or 'all')[/]",
                    console=self.ui.console,
                )

                if selection.lower().strip() == "all":
                    selected_engines = scripts.copy()
                    break

                # Parse individual IDs
                try:
                    engine_ids = [
                        int(id.strip()) for id in selection.split(",") if id.strip()
                    ]

                    for engine_id in engine_ids:
                        engine = next(
                            (s for s in scripts if s["id"] == engine_id), None
                        )
                        if engine:
                            selected_engines.append(engine)
                        else:
                            self.ui.log("WARNING", f"Engine ID {engine_id} not found")

                    if selected_engines:
                        break
                    else:
                        self.ui.log("ERROR", "No valid engines selected")
                        continue

                except ValueError:
                    self.ui.log(
                        "ERROR",
                        "Invalid selection format. Use numbers separated by commas.",
                    )
                    continue

            except KeyboardInterrupt:
                self.ui.log("INFO", "Engine selection cancelled")
                return []

        self.ui.set_selected_engines(selected_engines)
        self.ui.log("SUCCESS", f"Selected {len(selected_engines)} engines for analysis")
        self.ui.console.print()
        return selected_engines

    def run_engines(
        self,
        engines: List[Dict[str, Any]],
        csv_path: Path,
        delimiter: str,
        output_dir: Path,
    ) -> List[Dict[str, Any]]:
        """Run selected engines with progress tracking."""
        self.ui.set_step("analysis_running")

        # Show step header with consistent formatting
        self._show_workflow_step(
            5,
            "Analysis Execution",
            f"Running {len(engines)} analysis engines in parallel",
        )

        results = []
        total_engines = len(engines)

        for i, engine in enumerate(engines, 1):
            engine_name = engine["name"]
            self.ui.console.print(
                f"\n[{self.ui.theme['accent']}]Running engine {i}/{total_engines}: {engine_name}[/]"
            )

            interactive_engine = "main/analyzer.py" in engine_name

            # Stop all progress bars before running engine to avoid conflicts
            self.ui.stop_progress()

            try:
                # Get environment and script info
                env_name = self.ui.config["environments"][
                    engine.get("environment", "main")
                ]["name"]
                script_path = self.ui.project_root / "autocsv_profiler" / engine["name"]

                # Check if a modified dataset exists (from main engine column exclusion)
                modified_csv_path = output_dir / "modified_dataset.csv"
                current_csv_path = csv_path

                # Use modified CSV if it exists and this is not the main engine
                if modified_csv_path.exists() and not interactive_engine:
                    current_csv_path = modified_csv_path
                    self.ui.log(
                        "INFO",
                        f"Using modified dataset (with column exclusions) for {engine_name}",
                    )

                # Determine argument format - restore interactive mode
                args_type = engine.get("args_type", "csv_delimiter_output")

                if args_type == "csv_delimiter_output":
                    cmd_args = [
                        str(current_csv_path),
                        delimiter,
                        str(output_dir),
                    ]
                else:
                    cmd_args = [str(current_csv_path), str(output_dir)]

                # Run the engine with better error handling
                cmd = [
                    "conda",
                    "run",
                    "--no-capture-output",
                    "-n",
                    env_name,
                    "python",
                    str(script_path),
                ] + cmd_args

                # Apply backup project's interactive method
                self.ui.console.print(f"\n[blue]Starting {engine_name}...[/blue]")

                # Special handling for interactive main engine
                if interactive_engine:
                    from rich import box
                    from rich.panel import Panel

                    interactive_panel = Panel(
                        "[bold yellow]Interactive Analysis Phase[/bold yellow]\n\n"
                        "The main engine will now prompt you for:\n"
                        "- Column exclusion preferences\n"
                        "- Statistical grouping options\n"
                        "- Visualization selections\n\n"
                        "[dim]Please respond to each prompt as it appears below...[/dim]",
                        title="[bold]User Input Required[/bold]",
                        border_style="yellow",
                        box=box.ROUNDED,
                    )
                    self.ui.console.print(interactive_panel)

                # Use backup project's method: full terminal access for interactive engines
                import os
                import sys

                # Pass current environment variables to subprocess (including debug settings)
                env = os.environ.copy()

                result = subprocess.run(
                    cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, env=env
                )

                # Check result and handle success/failure
                if result.returncode == 0:
                    self.ui.log("SUCCESS", f"{engine_name} completed successfully")
                    results.append(
                        {
                            "engine": engine_name,
                            "success": True,
                            "output": f"{engine_name} completed successfully",
                        }
                    )
                else:
                    self.ui.log(
                        "ERROR",
                        f"{engine_name} failed with exit code {result.returncode}",
                    )
                    results.append(
                        {
                            "engine": engine_name,
                            "success": False,
                            "error": f"Failed with exit code {result.returncode}",
                        }
                    )
            except subprocess.CalledProcessError as e:
                self.ui.log("ERROR", f"Failed to run {engine_name}: {e}")
                results.append(
                    {
                        "engine": engine_name,
                        "success": False,
                        "error": f"Failed to run {engine_name}: {e}",
                    }
                )
            except KeyboardInterrupt:
                self.ui.log("WARNING", f"{engine_name} interrupted by user")
                results.append(
                    {
                        "engine": engine_name,
                        "success": False,
                        "error": "Interrupted by user",
                    }
                )
                break  # Stop running other engines
            except Exception as e:
                self.ui.log("ERROR", f"{engine_name} error: {str(e)}")
                results.append(
                    {"engine": engine_name, "success": False, "error": str(e)}
                )

        # Ensure all progress is completely stopped
        self.ui.stop_progress()
        self.ui.console.print()
        return results

    def display_completion_summary(self, output_dir: Path, results: List[Dict]) -> None:
        """Display analysis completion summary."""
        self.ui.set_step("completed")

        # Show completion summary
        self.ui.show_completion_summary(output_dir, results)

        # Show final status
        successful = len([r for r in results if r["success"]])
        total = len(results)

        self.ui.log(
            "INFO",
            f"Analysis workflow completed: {successful}/{total} engines successful",
        )

        if successful < total:
            self.ui.console.print()
            self.ui.console.print(
                "[yellow]Some engines failed. Check the logs above for details.[/yellow]"
            )

        # Ensure all progress is completely stopped
        self.ui.stop_progress()

    def run_analysis_direct(self, csv_file_path: str) -> bool:
        """Run analysis workflow directly with provided CSV file path."""
        try:
            csv_path = Path(csv_file_path)
            if not csv_path.exists():
                self.ui.log("ERROR", f"CSV file not found: {csv_file_path}")
                return False

            self.ui.log("INFO", f"Starting analysis of: {csv_path.name}")

            # Setup output directory
            output_dir, _ = self.setup_output_directory(csv_path)

            # Detect delimiter
            delimiter = self.detect_delimiter(csv_path)
            if not delimiter:
                self.ui.log("ERROR", "Could not determine delimiter")
                return False

            # Use all available engines by default for CLI mode - fix structure to match config
            engines = [
                {
                    "id": 1,
                    "name": "engines/main/analyzer.py",
                    "environment": "main",
                    "description": "Core statistical analysis",
                },
                {
                    "id": 2,
                    "name": "engines/profiling/ydata_report.py",
                    "environment": "profiling",
                    "description": "YData profiling report",
                },
                {
                    "id": 3,
                    "name": "engines/profiling/sweetviz_report.py",
                    "environment": "profiling",
                    "description": "SweetViz report",
                },
                {
                    "id": 4,
                    "name": "engines/dataprep/dataprep_report.py",
                    "environment": "dataprep",
                    "description": "DataPrep EDA report",
                },
            ]

            # Run engines
            results = self.run_engines(engines, csv_path, delimiter, output_dir)

            # Display results - fix parameter order
            self.display_completion_summary(output_dir, results)

            return True

        except Exception as e:
            self.ui.log("ERROR", f"Analysis failed: {e}")
            return False

    def run_analysis(self) -> bool:
        """Run the complete analysis workflow."""
        try:
            # Welcome and setup
            if not self.display_welcome_banner():
                return False

            # Get CSV file
            csv_path = self.get_csv_path()
            if not csv_path:
                self.ui.log("ERROR", "No CSV file selected")
                return False

            # Setup output directory
            output_dir, _ = self.setup_output_directory(csv_path)

            # Detect delimiter
            delimiter = self.detect_delimiter(csv_path)
            if not delimiter:
                self.ui.log("ERROR", "Could not determine delimiter")
                return False

            # Select engines
            engines = self.display_engine_selection_menu()
            if not engines:
                self.ui.log("ERROR", "No engines selected")
                return False

            # Run analysis
            results = self.run_engines(engines, csv_path, delimiter, output_dir)

            # Display completion summary
            self.display_completion_summary(output_dir, results)

            return True

        except KeyboardInterrupt:
            self.ui.console.print("\\n[yellow]Analysis cancelled by user.[/yellow]")
            return False
        except Exception as e:
            self.ui.log("ERROR", f"Unexpected error during analysis: {e}")
            return False
