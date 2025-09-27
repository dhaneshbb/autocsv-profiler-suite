"""AutoCSV Profiler Base Classes.

Base classes for all profiling engines in the AutoCSV Profiler Suite. Supports
both package integration and standalone engine execution.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

import pandas as pd

# Configuration import
if TYPE_CHECKING:
    from autocsv_profiler.config.settings import Settings

    _Settings = Settings
else:
    _Settings = None

settings: Optional[_Settings] = None

try:
    from autocsv_profiler.config import settings as _settings

    settings = _settings
    HAS_SETTINGS = True
except ImportError:
    settings = None
    HAS_SETTINGS = False

# Optional imports
try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    from tqdm import tqdm

    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


class ProfilerError(Exception):
    """Base exception for profiler errors."""


class FileProcessingError(ProfilerError):
    """Exception raised for file processing errors."""


class ReportGenerationError(ProfilerError):
    """Exception raised for report generation errors."""


class BaseProfiler(ABC):
    """Base class for all CSV profiling engines.

    Provides common functionality for loading data, error handling, and report
    generation.
    """

    def __init__(
        self,
        csv_path: Union[str, Path],
        delimiter: str,
        output_dir: Union[str, Path],
        chunk_size: int = 10000,
        memory_limit_gb: float = 1.0,
    ):
        """Initialize the profiler.

        Args:
            csv_path: Path to the CSV file to profile
            delimiter: CSV delimiter character
            output_dir: Directory to save reports
            chunk_size: Chunk size for processing large files
            memory_limit_gb: Memory limit in GB
        """
        self.csv_path = Path(csv_path)
        self.delimiter = delimiter
        self.output_dir = Path(output_dir)
        self.chunk_size = chunk_size
        self.memory_limit_gb = memory_limit_gb

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.df = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        """Load CSV data with chunking and memory management."""
        try:
            if not self.csv_path.exists():
                raise FileProcessingError(f"File not found: {self.csv_path}")

            file_size = self.csv_path.stat().st_size

            # Determine processing strategy based on file size
            # Small files: direct loading for better performance
            # Large files: chunked processing to manage memory
            if HAS_SETTINGS and settings:
                small_file_threshold = (
                    settings.get("performance.small_file_threshold_mb", 50)
                    * 1024
                    * 1024
                )
            else:
                default_threshold_mb = 50  # 50MB fallback when settings unavailable
                small_file_threshold = default_threshold_mb * 1024 * 1024

            if file_size < small_file_threshold:
                # Direct loading for small files - faster and simpler
                return pd.read_csv(self.csv_path, sep=self.delimiter)

            # Chunked processing for large files to prevent memory exhaustion
            chunks = []
            chunk_iterator = pd.read_csv(
                self.csv_path, sep=self.delimiter, chunksize=self.chunk_size
            )

            # Add progress tracking if tqdm is available
            if HAS_TQDM:
                if HAS_SETTINGS and settings:
                    estimate_factor = settings.get(
                        "performance.chunk_estimate_factor", 1024
                    )
                else:
                    estimate_factor = 1024  # Conservative estimate for chunk count

                # Estimate total chunks for progress bar (approximate)
                total_chunks = max(1, file_size // (self.chunk_size * estimate_factor))
                chunk_iterator = tqdm(
                    chunk_iterator,
                    total=total_chunks,
                    desc="Loading data",
                    unit="chunk",
                )

            for chunk in chunk_iterator:
                # Monitor memory usage to prevent system overload
                if HAS_PSUTIL:
                    memory_usage = psutil.Process().memory_info().rss / (1024**3)
                    if memory_usage > self.memory_limit_gb:
                        raise MemoryError(
                            f"Memory usage exceeded {self.memory_limit_gb}GB"
                        )

                chunks.append(chunk)

            return pd.concat(chunks, ignore_index=True)

        except FileNotFoundError:
            raise FileProcessingError(f"File not found: {self.csv_path}")
        except pd.errors.ParserError as e:
            raise FileProcessingError(f"Error parsing CSV file: {e}")
        except Exception as e:
            raise FileProcessingError(f"Unexpected error loading data: {e}")

    @abstractmethod
    def generate_report(self) -> str:
        """Generate the profiling report.

        Returns:
            Path to the generated report file
        """

    @abstractmethod
    def get_report_name(self) -> str:
        """Return the name/type of the report.

        Returns:
            Report name (e.g., "YData Profiling", "SweetViz", etc.)
        """

    def _truncate_path(self, path_str: str) -> str:
        r"""Truncate long file paths for cleaner display.

        Args:
            path_str: Full path string to truncate

        Returns:
            Truncated path string with format like 'D:\Projects\...\parent\filename'
        """
        try:
            path = Path(path_str)
            parts = path.parts
            if len(parts) > 4:
                # Keep first 2 parts, last 2 parts: D:\Projects\...\parent\filename
                truncated = str(Path(*parts[:2]) / "..." / Path(*parts[-2:]))
                return truncated
            return path_str
        except Exception:
            # Fallback for non-path strings or errors
            return path_str

    def run(self) -> Optional[str]:
        """Execute the profiling and generate the report.

        Returns:
            Path to generated report, or None if failed
        """
        try:
            report_path = self.generate_report()
            truncated_path = self._truncate_path(str(report_path))
            print(
                f"SUCCESS: {self.get_report_name()} report saved to: {truncated_path}"
            )
            return report_path

        except ReportGenerationError as e:
            print(f"Error generating {self.get_report_name()} report: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get_data_summary(self) -> dict:
        """Get basic summary of the loaded data."""
        return {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "memory_usage_mb": (self.df.memory_usage(deep=True).sum() / (1024 * 1024)),
            "column_names": list(self.df.columns),
            "dtypes": dict(self.df.dtypes.astype(str)),
        }
