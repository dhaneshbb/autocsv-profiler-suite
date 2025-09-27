"""Version management for AutoCSV Profiler Suite."""

import sys
from typing import NamedTuple, Optional, Tuple

# Version information
__version__ = "2.0.0"
__version_info__ = (2, 0, 0)

# Package metadata
__title__ = "AutoCSV Profiler Suite"
__description__ = (
    "Orchestrator for automated CSV data analysis using multiple profiling engines"
)
__author__ = "dhaneshbb"
__author_email__ = "dhaneshbb5@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2025 dhaneshbb"

# URLs
__url__ = "https://github.com/dhaneshbb/autocsv-profiler-suite"
__download_url__ = "https://github.com/dhaneshbb/autocsv-profiler-suite/releases"
__documentation_url__ = "https://github.com/dhaneshbb/autocsv-profiler-suite"

__status__ = "Beta"

# Define public API
__all__ = [
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
    "VersionInfo",
]


class VersionInfo(NamedTuple):
    """
    Version information structure.
    """

    major: int
    minor: int
    patch: int
    pre_release: str = ""
    build: str = ""


def get_version_info() -> VersionInfo:
    """
    Get structured version information.
    """
    return VersionInfo(*__version_info__)


def get_version_string() -> str:
    """
    Get version string.
    """
    return __version__


def get_full_version_info() -> dict:
    """
    Get complete version and environment information.
    """
    return {
        "version": __version__,
        "version_info": __version_info__,
        "python_version": sys.version,
        "python_version_info": sys.version_info,
        "platform": sys.platform,
        "title": __title__,
        "description": __description__,
        "author": __author__,
        "license": __license__,
        "status": __status__,
    }


def check_python_version(min_version: Optional[Tuple[int, int]] = None) -> bool:
    """
    Check if Python version meets minimum requirements.
    """
    if min_version is None:
        # Try to get minimum version from config
        try:
            from autocsv_profiler.config import settings

            min_version_str = settings.get("project.min_python_version", "3.10")
            major, minor = map(int, min_version_str.split("."))
            min_version = (major, minor)
        except (ImportError, ValueError, AttributeError):
            # Fallback to default if config unavailable
            min_version = (3, 10)

    return sys.version_info[:2] >= min_version


def get_dependency_versions() -> dict:
    """
    Get versions of key dependencies.
    """
    versions = {}

    try:
        import pandas as pd

        versions["pandas"] = pd.__version__
    except ImportError:
        versions["pandas"] = "Not installed"

    try:
        import numpy as np

        versions["numpy"] = np.__version__
    except ImportError:
        versions["numpy"] = "Not installed"

    try:
        import matplotlib

        versions["matplotlib"] = matplotlib.__version__
    except ImportError:
        versions["matplotlib"] = "Not installed"

    try:
        import seaborn as sns

        versions["seaborn"] = sns.__version__
    except ImportError:
        versions["seaborn"] = "Not installed"

    try:
        import charset_normalizer

        versions["charset-normalizer"] = charset_normalizer.__version__
    except ImportError:
        versions["charset-normalizer"] = "Not installed"

    return versions


# Compatibility check
if not check_python_version():
    import warnings

    warnings.warn(
        f"AutoCSV Profiler Suite {__version__} requires Python 3.10 "
        f"or higher. "
        f"You are using Python {sys.version}",
        UserWarning,
    )
