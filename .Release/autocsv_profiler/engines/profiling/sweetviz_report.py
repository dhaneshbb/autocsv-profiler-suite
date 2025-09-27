#!/usr/bin/env python3
"""Standalone SweetViz engine"""

import sys
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import pandas as pd

# Suppress warnings only if not in debug mode
import os

if os.environ.get("DEBUG") != "1":
    warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")
    warnings.filterwarnings("ignore", category=UserWarning, module="sweetviz")
else:
    print("[DEBUG] SweetViz warnings enabled for debugging")

# Import sweetviz
try:
    import sweetviz as sv
except ImportError:
    sv = None

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


# Simple debug function
def debug_print(message: str) -> None:
    if os.environ.get("DEBUG") == "1":
        print(f"[DEBUG SweetViz] {message}")


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


class SweetvizProfiler(StandaloneProfilerBase):
    def generate_report(self) -> str:
        debug_print("Starting SweetViz report generation")
        debug_print(f"Dataset shape: {self.df.shape}")

        if sv is None:
            debug_print("ERROR: sweetviz not available")
            raise ReportGenerationError("sweetviz not available")

        try:
            debug_print("Creating SweetViz analyze report")
            report = sv.analyze(self.df)
            report_file = self.output_dir / "sweetviz_report.html"
            debug_print(f"Saving report to: {report_file}")
            report.show_html(filepath=str(report_file), open_browser=False)
            debug_print("SweetViz report generation completed successfully")
            return str(report_file)
        except Exception as e:
            debug_print(f"ERROR: Failed to generate SweetViz report: {e}")
            raise ReportGenerationError(f"Failed to generate SweetViz report: {e}")

    def get_report_name(self) -> str:
        return "SweetViz"


def generate_sweetviz_report(
    csv_path: str, delimiter: str, output_dir: str
) -> Optional[str]:
    """Generate SweetViz profiling report.

    Args:
        csv_path: Path to CSV file
        delimiter: CSV delimiter character
        output_dir: Output directory for report

    Returns:
        Path to generated HTML report, or None if failed

    Environment:
        Requires csv-profiler-profiling conda environment

    Example:
        >>> generate_sweetviz_report("data.csv", ",", "output/")
        'output/sweetviz_report.html'
    """
    try:
        profiler = SweetvizProfiler(csv_path, delimiter, output_dir)
        return profiler.run()
    except Exception as e:
        print(f"Error generating SweetViz report: {e}")
        return None


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python sweetviz_report.py <csv_path> <delimiter> <output_dir>")
        sys.exit(1)

    debug_print(f"main() called with args: {sys.argv[1:]}")

    profiler = SweetvizProfiler(sys.argv[1], sys.argv[2], sys.argv[3])
    profiler.run()


if __name__ == "__main__":
    main()
