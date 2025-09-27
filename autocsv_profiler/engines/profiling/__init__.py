"""Profiling Environment Scripts

Scripts that run in the csv-profiler-profiling conda environment (Python 3.10.4).
Contains YData Profiling and SweetViz report generation with version constraints.

Note: These modules should only be imported within the profiling environment.
They are designed to be called via conda run -n csv-profiler-profiling
"""

__all__ = ["ydata_report", "sweetviz_report"]
