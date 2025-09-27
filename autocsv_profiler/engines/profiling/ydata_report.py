#!/usr/bin/env python3
"""Standalone YData Profiling engine"""

import sys
import warnings
from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import pandas as pd

# Suppress warnings and promotional messages only if not in debug mode
import os

if os.environ.get("DEBUG") != "1":
    warnings.filterwarnings("ignore", category=FutureWarning, module="ydata_profiling")
    warnings.filterwarnings("ignore", category=UserWarning, module="ydata_profiling")
else:
    print("[DEBUG] YData Profiling warnings enabled for debugging")

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


# Simple debug function
def debug_print(message: str) -> None:
    if os.environ.get("DEBUG") == "1":
        print(f"[DEBUG YData] {message}")


# Import ydata_profiling
try:
    with redirect_stdout(StringIO()):
        from ydata_profiling import ProfileReport
except ImportError:
    ProfileReport = None


class ReportGenerationError(Exception):
    pass


class StandaloneProfilerBase(ABC):
    def __init__(
        self,
        csv_path: str,
        delimiter: str,
        output_dir: str,
        chunk_size: int = 10000,
        memory_limit_gb: float = 1.0,
    ) -> None:
        self.csv_path = Path(csv_path)
        self.delimiter = delimiter
        self.output_dir = Path(output_dir)

        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.df = self._load_data()

    def _load_data(self) -> "pd.DataFrame":
        import pandas as pd

        try:
            return pd.read_csv(self.csv_path, delimiter=self.delimiter)
        except Exception as e:
            raise ReportGenerationError(f"Failed to load CSV file: {e}")

    @abstractmethod
    def generate_report(self) -> str:
        """Generate profiling report and return path to the report file."""

    @abstractmethod
    def get_report_name(self) -> str:
        """Return the name of the report for display purposes."""

    def _truncate_path(self, path_str: str) -> str:
        """Truncate long file paths for cleaner display."""
        try:
            path = Path(path_str)
            parts = path.parts
            if len(parts) > 4:
                # Keep first 2 parts, last 2 parts: D:\Projects\...\parent\filename
                truncated = str(Path(*parts[:2]) / "..." / Path(*parts[-2:]))
                return truncated
            return path_str
        except Exception:
            return path_str

    def run(self) -> Optional[str]:
        try:
            report_path = self.generate_report()
            truncated_path = self._truncate_path(str(report_path))
            print(
                f"SUCCESS: {self.get_report_name()} report saved to: {truncated_path}"
            )
            return report_path
        except Exception as e:
            print(f"Error generating {self.get_report_name()} report: {e}")
            return None


class YDataProfilingProfiler(StandaloneProfilerBase):
    def generate_report(self) -> str:
        debug_print("Starting YData Profiling report generation")
        debug_print(f"Dataset shape: {self.df.shape}")

        if ProfileReport is None:
            debug_print("ERROR: ydata_profiling not available")
            raise ReportGenerationError("ydata_profiling not available")

        try:
            debug_print("Creating YData ProfileReport")
            with redirect_stdout(StringIO()):
                profile = ProfileReport(
                    self.df, title="YData Profiling Report", explorative=True
                )

            report_file = self.output_dir / "ydata_profiling_report.html"
            debug_print(f"Saving report to: {report_file}")
            profile.to_file(str(report_file))
            debug_print("YData Profiling report generation completed successfully")
            return str(report_file)
        except Exception as e:
            debug_print(f"ERROR: Failed to generate YData Profiling report: {e}")
            raise ReportGenerationError(
                f"Failed to generate YData Profiling report: {e}"
            )

    def get_report_name(self) -> str:
        return "YData Profiling"


def generate_ydata_profiling_report(
    csv_path: str, delimiter: str, output_dir: str
) -> Optional[str]:
    """Generate YData Profiling report.

    Args:
        csv_path: Path to CSV file
        delimiter: CSV delimiter character
        output_dir: Output directory for report

    Returns:
        Path to generated HTML report, or None if failed

    Environment:
        Requires csv-profiler-profiling conda environment

    Example:
        >>> generate_ydata_profiling_report("data.csv", ",", "output/")
        'output/ydata_profiling_report.html'
    """
    try:
        profiler = YDataProfilingProfiler(csv_path, delimiter, output_dir)
        return profiler.run()
    except Exception as e:
        print(f"Error generating YData Profiling report: {e}")
        return None


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python ydata_report.py <csv_path> <delimiter> <output_dir>")
        sys.exit(1)

    debug_print(f"main() called with args: {sys.argv[1:]}")
    debug_print("Starting YData Profiling report generation")

    profiler = YDataProfilingProfiler(sys.argv[1], sys.argv[2], sys.argv[3])
    profiler.run()


if __name__ == "__main__":
    main()
