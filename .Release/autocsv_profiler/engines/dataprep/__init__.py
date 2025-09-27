"""DataPrep Environment Scripts

Scripts that run in the csv-profiler-dataprep conda environment (Python 3.10.4).
Contains DataPrep EDA analysis with specific dependency requirements.

Note: These modules should only be imported within the dataprep environment.
They are designed to be called via conda run -n csv-profiler-dataprep
"""

__all__ = ["dataprep_report"]
