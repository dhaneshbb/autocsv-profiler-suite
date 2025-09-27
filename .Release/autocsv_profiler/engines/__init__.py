"""
Multi-Environment Profiling Engines

This package organizes profiling scripts by their conda environment requirements.
Each subdirectory contains modules that run in specific environments to handle
dependency conflicts between profiling engines.

Environments:
- main/: Core analysis scripts (Python 3.11.7, pandas 1.5+)
- profiling/: YData & SweetViz scripts (Python 3.10.4, constrained versions)
- dataprep/: DataPrep scripts (Python 3.10.4, dataprep-specific deps)
"""

# Import base classes that are environment-agnostic
try:
    pass

    __all__ = ["BaseProfiler"]
except ImportError:
    # Graceful fallback if base classes not available in this environment
    __all__ = []
