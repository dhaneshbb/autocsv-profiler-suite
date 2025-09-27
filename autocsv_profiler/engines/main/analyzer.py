import os
import sys
import warnings

# Only suppress warnings if not in debug mode
if os.environ.get("DEBUG") != "1":
    warnings.filterwarnings("ignore", category=FutureWarning, module="researchpy")
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="tableone")
    warnings.filterwarnings(
        "ignore", category=PendingDeprecationWarning, module="seaborn"
    )
    warnings.filterwarnings("ignore", category=FutureWarning, module="dataprep")
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="dask")
    warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")
import contextlib  # noqa: E402
import logging  # noqa: E402
from io import StringIO  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import Any, Optional, Union  # noqa: E402

try:
    from rich.console import Console
except ImportError:
    # Create a dummy Console class when Rich is not available
    class Console:  # type: ignore
        pass


project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd  # noqa: E402

PathLike = Union[str, Path]

from autocsv_profiler.core.dataset_info import (  # noqa: E402
    data_table_range_min_max_distinct,
    distinct_val_tabular_txt,
    generate_complete_report,
)
from autocsv_profiler.core.utils import exclude_columns, memory_usage  # noqa: E402
from autocsv_profiler.plots import select_and_execute_visualizations  # noqa: E402
from autocsv_profiler.stats import (  # noqa: E402
    TableOne_groupby_column,
    researchpy_descriptive_stats,
)

try:
    from autocsv_profiler.ui.components import (
        TableOne_groupby_column_styled,
        exclude_columns_styled,
        select_and_execute_visualizations_styled,
    )

    HAS_UI_COMPONENTS = True
except ImportError:
    # Create compatible wrapper functions for fallbacks
    def exclude_columns_styled(
        data_copy: Any,
        save_dir: str,
        console: Optional[Console] = None,
        delimiter: str = ",",
    ) -> Any:
        return exclude_columns(data_copy, save_dir, delimiter)

    def TableOne_groupby_column_styled(
        data_copy: Any, save_dir: str, console: Optional[Console] = None
    ) -> Any:
        TableOne_groupby_column(data_copy, save_dir)
        return data_copy

    def select_and_execute_visualizations_styled(
        data_copy: Any, save_dir: str, console: Optional[Console] = None
    ) -> None:
        select_and_execute_visualizations(data_copy, save_dir)

    HAS_UI_COMPONENTS = False

from autocsv_profiler.core.exceptions import FileProcessingError  # noqa: E402
from autocsv_profiler.core.warnings import auto_configure_warnings  # noqa: E402

auto_configure_warnings()

# In debug mode, show all warnings but reduce matplotlib verbosity for readability
if os.environ.get("DEBUG") == "1":
    # Still suppress extremely verbose matplotlib logs even in debug mode for readability
    logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)
    logging.getLogger("matplotlib.pyplot").setLevel(logging.WARNING)
    logging.getLogger("matplotlib.ticker").setLevel(logging.WARNING)
    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.WARNING)
    print("[DEBUG] Warning filters disabled - all warnings will be shown for debugging")

import psutil  # noqa: E402
from tqdm import tqdm  # noqa: E402


def main(
    file_path: PathLike,
    save_dir: PathLike,
    delimiter: Optional[str] = None,
    chunk_size: int = 10000,
    memory_limit_gb: int = 1,
    interactive: bool = True,
) -> None:
    """Execute the full data analysis workflow.

    Main engine for statistical analysis (Python 3.11 environment).

    Args:
        file_path: Path to the CSV file to analyze
        save_dir: Directory to save analysis results
        delimiter: CSV delimiter. If None, defaults to comma
        chunk_size: Rows to read at a time. Default: 10000
        memory_limit_gb: Memory limit in GB. Default: 1
        interactive: Whether to run in interactive mode

    Environment:
        Requires csv-profiler-main conda environment
    """
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

    # Simple debug function
    def debug_print(message: str) -> None:
        if os.environ.get("DEBUG") == "1":
            print(f"[DEBUG Main] {message}")

    # Debug messages
    debug_print("Main analyzer started")
    debug_print(f"File path: {file_path}")
    debug_print(f"Save dir: {save_dir}")
    debug_print(f"Delimiter: {delimiter}")
    debug_print(f"Memory limit: {memory_limit_gb}GB, Chunk size: {chunk_size}")
    debug_print(f"Interactive mode: {interactive}")

    try:
        try:
            file_size = os.path.getsize(file_path)
            total_chunks = file_size // (
                chunk_size * 1024
            )  # Approximate number of chunks

            # Detect file encoding first
            from charset_normalizer import from_bytes

            with open(file_path, "rb") as file_handle:
                raw_data = file_handle.read(10000)  # Read first 10KB for detection
                result = from_bytes(raw_data).best()
                if result:
                    detected_encoding = result.encoding
                    encoding_confidence = getattr(result, "confidence", 0.9)
                else:
                    detected_encoding = "utf-8"
                    encoding_confidence = 0.5

            chunks = []

            with tqdm(
                total=total_chunks, desc="Processing Chunks", unit="chunk"
            ) as pbar:
                # Use provided delimiter or default to comma
                if delimiter is None:
                    delimiter = ","
                    print(
                        "Info: No delimiter specified, using comma (',') - delimiter detection handled by orchestrator"
                    )

                print(
                    f"Info: Detected encoding: {detected_encoding} (confidence: {encoding_confidence:.2%})"
                )

                try:
                    for chunk in pd.read_csv(
                        file_path,
                        sep=delimiter,
                        chunksize=chunk_size,
                        encoding=detected_encoding,
                    ):
                        memory_usage_gb = psutil.Process(
                            os.getpid()
                        ).memory_info().rss / (1024**3)
                        if memory_usage_gb > memory_limit_gb:
                            raise MemoryError(
                                f"Memory usage exceeded {memory_limit_gb}GB"
                            )

                        chunks.append(chunk)
                        pbar.update(1)
                except Exception as csv_error:
                    print(
                        f"[ERROR] Failed to read CSV with delimiter {repr(delimiter)} and encoding {repr(detected_encoding)}: {csv_error}"
                    )
                    raise FileProcessingError(
                        f"CSV reading failed with delimiter {repr(delimiter)} and encoding {repr(detected_encoding)}: {csv_error}"
                    )

            if not chunks:
                raise FileProcessingError(
                    "No data chunks were loaded from the CSV file"
                )

            data = pd.concat(chunks, ignore_index=True)

            # Keep original data unchanged
            data_copy = data.copy()
        except FileNotFoundError:
            raise FileProcessingError(f"File not found: {file_path}")
        except pd.errors.ParserError as e:
            raise FileProcessingError(f"Error parsing CSV file: {e}")

        # Display encoding results
        print("\n[*] GENERATING ANALYSIS REPORTS")
        print("=" * 60)

        from rich.console import Console

        console = Console()
        console.print("[cyan]=== File Encoding Detection ===[/cyan]")
        console.print(
            f"[green]Encoding: {detected_encoding} (Confidence: {encoding_confidence:.2%})[/green]"
        )
        console.print()

        # Temporarily suppress all logging during progress display

        from rich.progress import (
            BarColumn,
            Progress,
            SpinnerColumn,
            TaskProgressColumn,
            TextColumn,
            TimeElapsedColumn,
        )

        original_level = logging.getLogger().level
        autocsv_logger = logging.getLogger("autocsv")
        original_autocsv_level = autocsv_logger.level

        logging.getLogger().setLevel(logging.CRITICAL)
        autocsv_logger.setLevel(logging.CRITICAL)

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(complete_style="green", finished_style="green"),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        ) as progress:
            task = progress.add_task("Initializing analysis...", total=4)
            saved_files = []

            # Generate reports with progress updates and suppressed output
            with (
                contextlib.redirect_stdout(StringIO()),
                contextlib.redirect_stderr(StringIO()),
            ):
                progress.update(
                    task,
                    description="Generating complete dataset report...",
                )
                generate_complete_report(
                    data_copy, str(save_dir), str(file_path), delimiter=delimiter
                )
                saved_files.extend(["dataset_analysis.txt"])
                progress.advance(task)

                progress.update(task, description="Computing statistical summaries...")
                data_table_range_min_max_distinct(
                    data_copy, str(save_dir), delimiter=delimiter
                )
                saved_files.extend(["numerical_summary.csv", "categorical_summary.csv"])
                progress.advance(task)

                progress.update(task, description="Creating descriptive statistics...")
                researchpy_descriptive_stats(data_copy, save_dir, delimiter=delimiter)
                saved_files.extend(["numerical_stats.csv", "categorical_stats.csv"])
                progress.advance(task)

                progress.update(
                    task, description="Generating distinct values analysis..."
                )
                distinct_val_tabular_txt(
                    data_copy, os.path.join(save_dir, "distinct_values.txt")
                )
                saved_files.extend(["distinct_values.txt"])
                progress.advance(task)

                progress.update(task, description="Analysis reports completed!")

        # Display saved files instead of generic message
        console.print("\n[bold green]Saved files:[/bold green]")
        for file_name in saved_files:
            console.print(f"[green]- {file_name}[/green]")
        if interactive:
            print("\n" + "[*] STARTING INTERACTIVE ANALYSIS PHASE")
            print("=" * 60)

            print("\n[Phase 1] Column Exclusion Selection")
            data_copy = exclude_columns_styled(
                data_copy, str(save_dir), delimiter=delimiter
            )

            print("\n[Phase 2] TableOne Groupby Analysis")
            data_copy = TableOne_groupby_column_styled(data_copy, str(save_dir))

            print("\n[Phase 3] Visualization Selection")
            select_and_execute_visualizations_styled(data_copy, str(save_dir))

            logging.getLogger().setLevel(original_level)
            autocsv_logger.setLevel(original_autocsv_level)
        else:
            print("\n" + "[*] RUNNING NON-INTERACTIVE ANALYSIS")
            print("Skipping interactive phases, generating standard analysis only")

            logging.getLogger().setLevel(original_level)
            autocsv_logger.setLevel(original_autocsv_level)

        # Final report generation summary with progress tracking
        print("\n[*] FINALIZING ANALYSIS REPORTS")
        print("=" * 60)

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(complete_style="green", finished_style="green"),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        ) as progress:
            task = progress.add_task("Scanning generated reports...", total=100)

            import glob

            all_files = []

            original_csv_name = os.path.basename(str(file_path))
            for ext in ["*.csv", "*.txt"]:
                files = glob.glob(os.path.join(save_dir, ext))
                for file_path in files:
                    filename = os.path.basename(file_path)
                    if not (ext == "*.csv" and filename == original_csv_name):
                        all_files.append(filename)

            # Check visualization subdirectories for PNG files
            viz_dirs = [
                "kde_plots",
                "box_plots",
                "qq_plots",
                "bar_charts",
                "pie_charts",
            ]
            for viz_dir in viz_dirs:
                viz_path = os.path.join(save_dir, viz_dir, "*.png")
                files = glob.glob(viz_path)
                for file_path in files:
                    rel_path = os.path.relpath(file_path, save_dir)
                    all_files.append(rel_path)

            progress.update(task, advance=100, description="Analysis complete!")

        console.print("\n[bold green]All saved files:[/bold green]")
        if all_files:
            for file_name in sorted(all_files):
                console.print(f"[green]- {file_name}[/green]")
        else:
            console.print("[yellow]No additional files found[/yellow]")

    except FileProcessingError as e:
        logging.error(f"Error during analysis: {e}")
        print(f"Error: {e}")
        sys.exit(1)
    except MemoryError as e:
        logging.error(f"Memory limit exceeded: {e}")
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        import traceback

        error_msg = str(e)
        logging.error(f"An unexpected error occurred: {error_msg}")
        logging.error(traceback.format_exc())

        # Print detailed error information for debugging
        print(f"An unexpected error occurred: {error_msg}")
        print(f"Arguments received: {sys.argv}")
        print("Traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    memory_usage()

    args = [arg for arg in sys.argv[1:] if arg != "--non-interactive"]
    non_interactive = "--non-interactive" in sys.argv[1:]

    if len(args) not in [2, 3]:
        print("Usage: python analyzer.py <file_path> <save_dir> [--non-interactive]")
        print(
            "   or: python analyzer.py <file_path> <delimiter> <save_dir> [--non-interactive]"
        )
        sys.exit(1)
    else:
        if len(args) == 2:
            file_path = args[0]
            save_dir = args[1]
            delimiter = None
        else:
            file_path = args[0]
            delimiter = args[1]
            save_dir = args[2]

        main(file_path, save_dir, delimiter, interactive=not non_interactive)

    memory_usage()


def run_analysis(
    file_path: PathLike,
    save_dir: Optional[PathLike] = None,
    delimiter: Optional[str] = None,
    chunk_size: int = 10000,
    memory_limit_gb: int = 1,
) -> str:
    """Run CSV analysis interactively.

    Args:
        file_path: Path to the CSV file to analyze
        save_dir: Directory to save results. If None, creates default directory.
        delimiter: CSV delimiter. If None, defaults to comma.
        chunk_size: Chunk size for processing. Defaults to 10000.
        memory_limit_gb: Memory limit in GB. Defaults to 1.

    Returns:
        Path to the analysis results directory
    """
    if save_dir is None:
        base_name = os.path.splitext(os.path.basename(str(file_path)))[0]
        save_dir = f"{base_name}_analysis"

    main(file_path, save_dir, delimiter, chunk_size, memory_limit_gb)
    return str(save_dir)
