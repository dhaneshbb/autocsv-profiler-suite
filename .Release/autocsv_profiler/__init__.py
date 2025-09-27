"""AutoCSV Profiler Suite - Automated CSV Data Analysis.

A toolkit for automated CSV data analysis using multiple profiling engines.
Provides statistical analysis, visualization, and profiling reports across
multiple environments with conflicting dependencies.

LICENSE NOTICE: This software is distributed as source code and configuration
only. Users are responsible for installing conda environments and complying
with licenses of packages they install. See LICENSE and NOTICE files.
"""

from typing import Any, Optional, Tuple

# Import package components
from .config import ConfigValidationError, Settings, settings
from .core import (
    AutoCSVProfilerError,
    DelimiterDetectionError,
    FileProcessingError,
    ReportGenerationError,
    get_logger,
    log_print,
)

# Import version information
from .version import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __status__,
    __title__,
    __url__,
    __version__,
    __version_info__,
    check_python_version,
    get_dependency_versions,
    get_full_version_info,
    get_version_info,
    get_version_string,
)

# Lazy import placeholders - engines loaded on demand
auto_csv_main = None
run_analysis = None
analyze_csv = None
generate_ydata_profiling_report = None
generate_sweetviz_report = None
generate_dataprep_report = None
ProfilerBase = None


# Engine loading functions for environment-aware imports
def _load_main_engine() -> Tuple[Any, Any, Any]:
    """
    Lazy load main analysis engine.

    This function loads the main analysis engine and its convenience imports.
    It handles the case where the main engine is not available (e.g., when
    the required packages are not installed) and returns `None` in that case.

    Returns:
        A tuple containing the main analysis engine, the `run_analysis` function,
        and the `analyze_csv` function.
    """
    global auto_csv_main, run_analysis, analyze_csv
    if auto_csv_main is None:
        try:
            # Convenience imports for easier usage
            from .engines.main.analyzer import main as analyze_csv
            from .engines.main.analyzer import main as auto_csv_main
            from .engines.main.analyzer import run_analysis
        except ImportError:
            auto_csv_main = None
            run_analysis = None
            analyze_csv = None
    return auto_csv_main, run_analysis, analyze_csv


def _load_ydata_engine() -> Any:
    """
    Lazy load YData profiling engine.

    This function loads the YData profiling engine and handles the case where the
    engine is not available (e.g., when the required packages are not installed).
    It returns `None` in that case.

    Returns:
        The YData profiling engine or `None` if the engine is not available.
    """
    global generate_ydata_profiling_report
    if generate_ydata_profiling_report is None:
        try:
            # Load the YData profiling engine
            from .engines.profiling.ydata_report import generate_ydata_profiling_report
        except ImportError:
            # Set the engine to None if it can't be imported
            generate_ydata_profiling_report = None
    return generate_ydata_profiling_report


def _load_sweetviz_engine() -> Any:
    """
    Lazy load SweetViz engine.
    """
    global generate_sweetviz_report
    if generate_sweetviz_report is None:
        try:
            from .engines.profiling.sweetviz_report import generate_sweetviz_report
        except ImportError:
            generate_sweetviz_report = None
    return generate_sweetviz_report


def _load_dataprep_engine() -> Any:
    """
    Lazy load DataPrep engine.
    """
    global generate_dataprep_report
    if generate_dataprep_report is None:
        try:
            from .engines.dataprep.dataprep_report import generate_dataprep_report
        except ImportError:
            generate_dataprep_report = None
    return generate_dataprep_report


def _load_base_profiler() -> Any:
    """
    Lazy load base profiler class.
    """
    global ProfilerBase
    if ProfilerBase is None:
        try:
            from .base import BaseProfiler as ProfilerBase
        except ImportError:
            ProfilerBase = None
    return ProfilerBase


# Package metadata

# Define public API
__all__ = [
    # Version information
    "__version__",
    "__version_info__",
    "__title__",
    "__description__",
    "__author__",
    "__author_email__",
    "__license__",
    "__copyright__",
    "__url__",
    "__status__",
    "get_version_info",
    "get_version_string",
    "get_full_version_info",
    "check_python_version",
    "get_dependency_versions",
    # Main profiling functions
    "run_analysis",
    "auto_csv_main",
    "generate_ydata_profiling_report",
    "generate_sweetviz_report",
    "generate_dataprep_report",
    # Base classes
    "ProfilerBase",
    # Configuration
    "Settings",
    "ConfigValidationError",
    "settings",
    # Core utilities and exceptions
    "AutoCSVProfilerError",
    "FileProcessingError",
    "DelimiterDetectionError",
    "ReportGenerationError",
    "get_logger",
    "log_print",
    # Convenience functions
    "analyze_csv",
    "run_analysis",
]


# Convenience functions for quick access
def profile_csv(
    csv_file_path: str, output_dir: Optional[str] = None, engine: str = "auto"
) -> str:
    """Profile a CSV file using the specified engine.

    Args:
        csv_file_path: Path to the CSV file to analyze
        output_dir: Directory to save outputs (optional)
        engine: Profiling engine ('auto', 'ydata', 'sweetviz', 'dataprep')

    Returns:
        Path to the generated report file

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        AutoCSVProfilerError: If profiling fails
        ImportError: If required profiling engine is not available

    Example:
        >>> from autocsv_profiler import profile_csv
        >>> report_path = profile_csv("data.csv", "reports/")
        >>> ydata_report = profile_csv("data.csv", engine="ydata")
    """
    if engine.lower() == "auto":
        # Lazy load main engine only when needed
        _, run_analysis_func, _ = _load_main_engine()
        if run_analysis_func is None:
            raise ImportError(
                "Main analysis engine not available. Use bin/run_analysis.py"
            )
        result = run_analysis_func(csv_file_path, output_dir)
        return str(result) if result else ""
    elif engine.lower() == "ydata":
        # Lazy load YData engine only when needed
        ydata_func = _load_ydata_engine()
        if ydata_func is None:
            raise ImportError("YData Profiling not available in this environment.")
        result = ydata_func(csv_file_path, output_dir)
        return str(result) if result else ""
    elif engine.lower() == "sweetviz":
        # Lazy load SweetViz engine only when needed
        sweetviz_func = _load_sweetviz_engine()
        if sweetviz_func is None:
            raise ImportError("SweetViz not available in this environment.")
        result = sweetviz_func(csv_file_path, output_dir)
        return str(result) if result else ""
    elif engine.lower() == "dataprep":
        # Lazy load DataPrep engine only when needed
        dataprep_func = _load_dataprep_engine()
        if dataprep_func is None:
            raise ImportError("DataPrep not available in this environment.")
        result = dataprep_func(csv_file_path, output_dir)
        return str(result) if result else ""
    else:
        raise ValueError(f"Unknown profiling engine: {engine}")


# Add convenience function to exports
__all__.append("profile_csv")
