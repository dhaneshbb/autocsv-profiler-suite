"""Configuration module for AutoCSV Profiler Suite

Contains all configuration-related components:
- Settings management and validation
- Visualization configuration
- Default configuration files
"""

# Import main configuration components
try:
    from .settings import ConfigValidationError, Settings, settings

    __all__ = ["Settings", "ConfigValidationError", "settings"]
except ImportError:
    ConfigValidationError = None  # type: ignore
    Settings = None  # type: ignore
    settings = None  # type: ignore
    __all__ = []
