# API Reference

This document provides detailed information about the AutoCSV Profiler Python API.

## Package Overview

```python
import autocsv_profiler

# Main analysis function
from autocsv_profiler import analyze_csv

# Delimiter detection
from autocsv_profiler import detect_delimiter

# Version information
print(autocsv_profiler.__version__)
```

## Core Functions

### analyze_csv()

Main function for comprehensive CSV data analysis.

#### Signature
```python
def analyze_csv(csv_path: str, output_dir: str) -> None
```

#### Parameters
- **csv_path** (`str`): Path to the CSV file to analyze
- **output_dir** (`str`): Directory where analysis results will be saved

#### Returns
- `None`: Results are saved to the specified output directory

#### Raises
- `FileNotFoundError`: If the CSV file doesn't exist
- `ValueError`: If the CSV file cannot be parsed
- `PermissionError`: If unable to write to output directory
- `MemoryError`: If the dataset is too large for available memory

#### Example Usage
```python
from autocsv_profiler import analyze_csv

# Basic usage
analyze_csv("data.csv", "analysis_output")

# With error handling
try:
    analyze_csv("large_dataset.csv", "results")
    print("Analysis completed successfully")
except FileNotFoundError:
    print("CSV file not found")
except MemoryError:
    print("Dataset too large - consider sampling")
```

#### Generated Outputs
The function creates the following files in the output directory:

**Text Reports:**
- `dataset_info.txt` - Basic dataset information
- `summary_statistics_all.txt` - Comprehensive statistics
- `categorical_summary.txt` - Categorical variable analysis
- `missing_values_report.txt` - Missing data analysis
- `outliers_summary.txt` - Outlier detection results

**Interactive Reports:**
- `distinct_values_count_by_dtype.html` - Interactive value explorer

**Visualizations:**
- `visualization/box_plots/` - Box plot visualizations
- `visualization/histograms/` - Distribution histograms
- `visualization/correlation_matrices/` - Correlation heatmaps

### detect_delimiter()

Automatic delimiter detection for CSV files.

#### Signature
```python
def detect_delimiter(csv_file: str) -> str
```

#### Parameters
- **csv_file** (`str`): Path to the CSV file

#### Returns
- `str`: Detected delimiter character

#### Raises
- `FileNotFoundError`: If the CSV file doesn't exist
- `ValueError`: If delimiter cannot be determined

#### Example Usage
```python
from autocsv_profiler import detect_delimiter

# Detect delimiter
delimiter = detect_delimiter("data.csv")
print(f"Detected delimiter: '{delimiter}'")

# Use with pandas
import pandas as pd
df = pd.read_csv("data.csv", delimiter=delimiter)
```

#### Supported Delimiters
The function can detect:
- `,` (comma) - Standard CSV
- `;` (semicolon) - European CSV standard
- `\t` (tab) - Tab-separated values
- `|` (pipe) - Pipe-separated values
- `:` (colon) - Colon-separated values

#### Detection Algorithm

<img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLXJvbGVkZXNjcmlwdGlvbj0iZmxvd2NoYXJ0LXYyIiByb2xlPSJncmFwaGljcy1kb2N1bWVudCBkb2N1bWVudCIgdmlld0JveD0iMCAwIDUzOC4wMjM0Mzc1IDkwMi40Mzc1IiBzdHlsZT0ibWF4LXdpZHRoOiA1MzguMDIzcHg7IGJhY2tncm91bmQtY29sb3I6IHdoaXRlOyIgY2xhc3M9ImZsb3djaGFydCIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCUiIGlkPSJteS1zdmciPjxzdHlsZT4jbXktc3Zne2ZvbnQtZmFtaWx5OiJ0cmVidWNoZXQgbXMiLHZlcmRhbmEsYXJpYWwsc2Fucy1zZXJpZjtmb250LXNpemU6MTZweDtmaWxsOiMzMzM7fUBrZXlmcmFtZXMgZWRnZS1hbmltYXRpb24tZnJhbWV7ZnJvbXtzdHJva2UtZGFzaG9mZnNldDowO319QGtleWZyYW1lcyBkYXNoe3Rve3N0cm9rZS1kYXNob2Zmc2V0OjA7fX0jbXktc3ZnIC5lZGdlLWFuaW1hdGlvbi1zbG93e3N0cm9rZS1kYXNoYXJyYXk6OSw1IWltcG9ydGFudDtzdHJva2UtZGFzaG9mZnNldDo5MDA7YW5pbWF0aW9uOmRhc2ggNTBzIGxpbmVhciBpbmZpbml0ZTtzdHJva2UtbGluZWNhcDpyb3VuZDt9I215LXN2ZyAuZWRnZS1hbmltYXRpb24tZmFzdHtzdHJva2UtZGFzaGFycmF5OjksNSFpbXBvcnRhbnQ7c3Ryb2tlLWRhc2hvZmZzZXQ6OTAwO2FuaW1hdGlvbjpkYXNoIDIwcyBsaW5lYXIgaW5maW5pdGU7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7fSNteS1zdmcgLmVycm9yLWljb257ZmlsbDojNTUyMjIyO30jbXktc3ZnIC5lcnJvci10ZXh0e2ZpbGw6IzU1MjIyMjtzdHJva2U6IzU1MjIyMjt9I215LXN2ZyAuZWRnZS10aGlja25lc3Mtbm9ybWFse3N0cm9rZS13aWR0aDoxcHg7fSNteS1zdmcgLmVkZ2UtdGhpY2tuZXNzLXRoaWNre3N0cm9rZS13aWR0aDozLjVweDt9I215LXN2ZyAuZWRnZS1wYXR0ZXJuLXNvbGlke3N0cm9rZS1kYXNoYXJyYXk6MDt9I215LXN2ZyAuZWRnZS10aGlja25lc3MtaW52aXNpYmxle3N0cm9rZS13aWR0aDowO2ZpbGw6bm9uZTt9I215LXN2ZyAuZWRnZS1wYXR0ZXJuLWRhc2hlZHtzdHJva2UtZGFzaGFycmF5OjM7fSNteS1zdmcgLmVkZ2UtcGF0dGVybi1kb3R0ZWR7c3Ryb2tlLWRhc2hhcnJheToyO30jbXktc3ZnIC5tYXJrZXJ7ZmlsbDojMzMzMzMzO3N0cm9rZTojMzMzMzMzO30jbXktc3ZnIC5tYXJrZXIuY3Jvc3N7c3Ryb2tlOiMzMzMzMzM7fSNteS1zdmcgc3Zne2ZvbnQtZmFtaWx5OiJ0cmVidWNoZXQgbXMiLHZlcmRhbmEsYXJpYWwsc2Fucy1zZXJpZjtmb250LXNpemU6MTZweDt9I215LXN2ZyBwe21hcmdpbjowO30jbXktc3ZnIC5sYWJlbHtmb250LWZhbWlseToidHJlYnVjaGV0IG1zIix2ZXJkYW5hLGFyaWFsLHNhbnMtc2VyaWY7Y29sb3I6IzMzMzt9I215LXN2ZyAuY2x1c3Rlci1sYWJlbCB0ZXh0e2ZpbGw6IzMzMzt9I215LXN2ZyAuY2x1c3Rlci1sYWJlbCBzcGFue2NvbG9yOiMzMzM7fSNteS1zdmcgLmNsdXN0ZXItbGFiZWwgc3BhbiBwe2JhY2tncm91bmQtY29sb3I6dHJhbnNwYXJlbnQ7fSNteS1zdmcgLmxhYmVsIHRleHQsI215LXN2ZyBzcGFue2ZpbGw6IzMzMztjb2xvcjojMzMzO30jbXktc3ZnIC5ub2RlIHJlY3QsI215LXN2ZyAubm9kZSBjaXJjbGUsI215LXN2ZyAubm9kZSBlbGxpcHNlLCNteS1zdmcgLm5vZGUgcG9seWdvbiwjbXktc3ZnIC5ub2RlIHBhdGh7ZmlsbDojRUNFQ0ZGO3N0cm9rZTojOTM3MERCO3N0cm9rZS13aWR0aDoxcHg7fSNteS1zdmcgLnJvdWdoLW5vZGUgLmxhYmVsIHRleHQsI215LXN2ZyAubm9kZSAubGFiZWwgdGV4dCwjbXktc3ZnIC5pbWFnZS1zaGFwZSAubGFiZWwsI215LXN2ZyAuaWNvbi1zaGFwZSAubGFiZWx7dGV4dC1hbmNob3I6bWlkZGxlO30jbXktc3ZnIC5ub2RlIC5rYXRleCBwYXRoe2ZpbGw6IzAwMDtzdHJva2U6IzAwMDtzdHJva2Utd2lkdGg6MXB4O30jbXktc3ZnIC5yb3VnaC1ub2RlIC5sYWJlbCwjbXktc3ZnIC5ub2RlIC5sYWJlbCwjbXktc3ZnIC5pbWFnZS1zaGFwZSAubGFiZWwsI215LXN2ZyAuaWNvbi1zaGFwZSAubGFiZWx7dGV4dC1hbGlnbjpjZW50ZXI7fSNteS1zdmcgLm5vZGUuY2xpY2thYmxle2N1cnNvcjpwb2ludGVyO30jbXktc3ZnIC5yb290IC5hbmNob3IgcGF0aHtmaWxsOiMzMzMzMzMhaW1wb3J0YW50O3N0cm9rZS13aWR0aDowO3N0cm9rZTojMzMzMzMzO30jbXktc3ZnIC5hcnJvd2hlYWRQYXRoe2ZpbGw6IzMzMzMzMzt9I215LXN2ZyAuZWRnZVBhdGggLnBhdGh7c3Ryb2tlOiMzMzMzMzM7c3Ryb2tlLXdpZHRoOjIuMHB4O30jbXktc3ZnIC5mbG93Y2hhcnQtbGlua3tzdHJva2U6IzMzMzMzMztmaWxsOm5vbmU7fSNteS1zdmcgLmVkZ2VMYWJlbHtiYWNrZ3JvdW5kLWNvbG9yOnJnYmEoMjMyLDIzMiwyMzIsIDAuOCk7dGV4dC1hbGlnbjpjZW50ZXI7fSNteS1zdmcgLmVkZ2VMYWJlbCBwe2JhY2tncm91bmQtY29sb3I6cmdiYSgyMzIsMjMyLDIzMiwgMC44KTt9I215LXN2ZyAuZWRnZUxhYmVsIHJlY3R7b3BhY2l0eTowLjU7YmFja2dyb3VuZC1jb2xvcjpyZ2JhKDIzMiwyMzIsMjMyLCAwLjgpO2ZpbGw6cmdiYSgyMzIsMjMyLDIzMiwgMC44KTt9I215LXN2ZyAubGFiZWxCa2d7YmFja2dyb3VuZC1jb2xvcjpyZ2JhKDIzMiwgMjMyLCAyMzIsIDAuNSk7fSNteS1zdmcgLmNsdXN0ZXIgcmVjdHtmaWxsOiNmZmZmZGU7c3Ryb2tlOiNhYWFhMzM7c3Ryb2tlLXdpZHRoOjFweDt9I215LXN2ZyAuY2x1c3RlciB0ZXh0e2ZpbGw6IzMzMzt9I215LXN2ZyAuY2x1c3RlciBzcGFue2NvbG9yOiMzMzM7fSNteS1zdmcgZGl2Lm1lcm1haWRUb29sdGlwe3Bvc2l0aW9uOmFic29sdXRlO3RleHQtYWxpZ246Y2VudGVyO21heC13aWR0aDoyMDBweDtwYWRkaW5nOjJweDtmb250LWZhbWlseToidHJlYnVjaGV0IG1zIix2ZXJkYW5hLGFyaWFsLHNhbnMtc2VyaWY7Zm9udC1zaXplOjEycHg7YmFja2dyb3VuZDpoc2woODAsIDEwMCUsIDk2LjI3NDUwOTgwMzklKTtib3JkZXI6MXB4IHNvbGlkICNhYWFhMzM7Ym9yZGVyLXJhZGl1czoycHg7cG9pbnRlci1ldmVudHM6bm9uZTt6LWluZGV4OjEwMDt9I215LXN2ZyAuZmxvd2NoYXJ0VGl0bGVUZXh0e3RleHQtYW5jaG9yOm1pZGRsZTtmb250LXNpemU6MThweDtmaWxsOiMzMzM7fSNteS1zdmcgcmVjdC50ZXh0e2ZpbGw6bm9uZTtzdHJva2Utd2lkdGg6MDt9I215LXN2ZyAuaWNvbi1zaGFwZSwjbXktc3ZnIC5pbWFnZS1zaGFwZXtiYWNrZ3JvdW5kLWNvbG9yOnJnYmEoMjMyLDIzMiwyMzIsIDAuOCk7dGV4dC1hbGlnbjpjZW50ZXI7fSNteS1zdmcgLmljb24tc2hhcGUgcCwjbXktc3ZnIC5pbWFnZS1zaGFwZSBwe2JhY2tncm91bmQtY29sb3I6cmdiYSgyMzIsMjMyLDIzMiwgMC44KTtwYWRkaW5nOjJweDt9I215LXN2ZyAuaWNvbi1zaGFwZSByZWN0LCNteS1zdmcgLmltYWdlLXNoYXBlIHJlY3R7b3BhY2l0eTowLjU7YmFja2dyb3VuZC1jb2xvcjpyZ2JhKDIzMiwyMzIsMjMyLCAwLjgpO2ZpbGw6cmdiYSgyMzIsMjMyLDIzMiwgMC44KTt9I215LXN2ZyAubGFiZWwtaWNvbntkaXNwbGF5OmlubGluZS1ibG9jaztoZWlnaHQ6MWVtO292ZXJmbG93OnZpc2libGU7dmVydGljYWwtYWxpZ246LTAuMTI1ZW07fSNteS1zdmcgLm5vZGUgLmxhYmVsLWljb24gcGF0aHtmaWxsOmN1cnJlbnRDb2xvcjtzdHJva2U6cmV2ZXJ0O3N0cm9rZS13aWR0aDpyZXZlcnQ7fSNteS1zdmcgOnJvb3R7LS1tZXJtYWlkLWZvbnQtZmFtaWx5OiJ0cmVidWNoZXQgbXMiLHZlcmRhbmEsYXJpYWwsc2Fucy1zZXJpZjt9PC9zdHlsZT48Zz48bWFya2VyIG9yaWVudD0iYXV0byIgbWFya2VySGVpZ2h0PSI4IiBtYXJrZXJXaWR0aD0iOCIgbWFya2VyVW5pdHM9InVzZXJTcGFjZU9uVXNlIiByZWZZPSI1IiByZWZYPSI1IiB2aWV3Qm94PSIwIDAgMTAgMTAiIGNsYXNzPSJtYXJrZXIgZmxvd2NoYXJ0LXYyIiBpZD0ibXktc3ZnX2Zsb3djaGFydC12Mi1wb2ludEVuZCI+PHBhdGggc3R5bGU9InN0cm9rZS13aWR0aDogMTsgc3Ryb2tlLWRhc2hhcnJheTogMSwgMDsiIGNsYXNzPSJhcnJvd01hcmtlclBhdGgiIGQ9Ik0gMCAwIEwgMTAgNSBMIDAgMTAgeiIvPjwvbWFya2VyPjxtYXJrZXIgb3JpZW50PSJhdXRvIiBtYXJrZXJIZWlnaHQ9IjgiIG1hcmtlcldpZHRoPSI4IiBtYXJrZXJVbml0cz0idXNlclNwYWNlT25Vc2UiIHJlZlk9IjUiIHJlZlg9IjQuNSIgdmlld0JveD0iMCAwIDEwIDEwIiBjbGFzcz0ibWFya2VyIGZsb3djaGFydC12MiIgaWQ9Im15LXN2Z19mbG93Y2hhcnQtdjItcG9pbnRTdGFydCI+PHBhdGggc3R5bGU9InN0cm9rZS13aWR0aDogMTsgc3Ryb2tlLWRhc2hhcnJheTogMSwgMDsiIGNsYXNzPSJhcnJvd01hcmtlclBhdGgiIGQ9Ik0gMCA1IEwgMTAgMTAgTCAxMCAwIHoiLz48L21hcmtlcj48bWFya2VyIG9yaWVudD0iYXV0byIgbWFya2VySGVpZ2h0PSIxMSIgbWFya2VyV2lkdGg9IjExIiBtYXJrZXJVbml0cz0idXNlclNwYWNlT25Vc2UiIHJlZlk9IjUiIHJlZlg9IjExIiB2aWV3Qm94PSIwIDAgMTAgMTAiIGNsYXNzPSJtYXJrZXIgZmxvd2NoYXJ0LXYyIiBpZD0ibXktc3ZnX2Zsb3djaGFydC12Mi1jaXJjbGVFbmQiPjxjaXJjbGUgc3R5bGU9InN0cm9rZS13aWR0aDogMTsgc3Ryb2tlLWRhc2hhcnJheTogMSwgMDsiIGNsYXNzPSJhcnJvd01hcmtlclBhdGgiIHI9IjUiIGN5PSI1IiBjeD0iNSIvPjwvbWFya2VyPjxtYXJrZXIgb3JpZW50PSJhdXRvIiBtYXJrZXJIZWlnaHQ9IjExIiBtYXJrZXJXaWR0aD0iMTEiIG1hcmtlclVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgcmVmWT0iNSIgcmVmWD0iLTEiIHZpZXdCb3g9IjAgMCAxMCAxMCIgY2xhc3M9Im1hcmtlciBmbG93Y2hhcnQtdjIiIGlkPSJteS1zdmdfZmxvd2NoYXJ0LXYyLWNpcmNsZVN0YXJ0Ij48Y2lyY2xlIHN0eWxlPSJzdHJva2Utd2lkdGg6IDE7IHN0cm9rZS1kYXNoYXJyYXk6IDEsIDA7IiBjbGFzcz0iYXJyb3dNYXJrZXJQYXRoIiByPSI1IiBjeT0iNSIgY3g9IjUiLz48L21hcmtlcj48bWFya2VyIG9yaWVudD0iYXV0byIgbWFya2VySGVpZ2h0PSIxMSIgbWFya2VyV2lkdGg9IjExIiBtYXJrZXJVbml0cz0idXNlclNwYWNlT25Vc2UiIHJlZlk9IjUuMiIgcmVmWD0iMTIiIHZpZXdCb3g9IjAgMCAxMSAxMSIgY2xhc3M9Im1hcmtlciBjcm9zcyBmbG93Y2hhcnQtdjIiIGlkPSJteS1zdmdfZmxvd2NoYXJ0LXYyLWNyb3NzRW5kIj48cGF0aCBzdHlsZT0ic3Ryb2tlLXdpZHRoOiAyOyBzdHJva2UtZGFzaGFycmF5OiAxLCAwOyIgY2xhc3M9ImFycm93TWFya2VyUGF0aCIgZD0iTSAxLDEgbCA5LDkgTSAxMCwxIGwgLTksOSIvPjwvbWFya2VyPjxtYXJrZXIgb3JpZW50PSJhdXRvIiBtYXJrZXJIZWlnaHQ9IjExIiBtYXJrZXJXaWR0aD0iMTEiIG1hcmtlclVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgcmVmWT0iNS4yIiByZWZYPSItMSIgdmlld0JveD0iMCAwIDExIDExIiBjbGFzcz0ibWFya2VyIGNyb3NzIGZsb3djaGFydC12MiIgaWQ9Im15LXN2Z19mbG93Y2hhcnQtdjItY3Jvc3NTdGFydCI+PHBhdGggc3R5bGU9InN0cm9rZS13aWR0aDogMjsgc3Ryb2tlLWRhc2hhcnJheTogMSwgMDsiIGNsYXNzPSJhcnJvd01hcmtlclBhdGgiIGQ9Ik0gMSwxIGwgOSw5IE0gMTAsMSBsIC05LDkiLz48L21hcmtlcj48ZyBjbGFzcz0icm9vdCI+PGcgY2xhc3M9ImNsdXN0ZXJzIi8+PGcgY2xhc3M9ImVkZ2VQYXRocyI+PHBhdGggbWFya2VyLWVuZD0idXJsKCNteS1zdmdfZmxvd2NoYXJ0LXYyLXBvaW50RW5kKSIgc3R5bGU9IiIgY2xhc3M9ImVkZ2UtdGhpY2tuZXNzLW5vcm1hbCBlZGdlLXBhdHRlcm4tc29saWQgZWRnZS10aGlja25lc3Mtbm9ybWFsIGVkZ2UtcGF0dGVybi1zb2xpZCBmbG93Y2hhcnQtbGluayIgaWQ9IkxfQV9CXzAiIGQ9Ik0yNjYuMzk4LDYyTDI2Ni4zOTgsNjYuMTY3QzI2Ni4zOTgsNzAuMzMzLDI2Ni4zOTgsNzguNjY3LDI2Ni4zOTgsODYuMzMzQzI2Ni4zOTgsOTQsMjY2LjM5OCwxMDEsMjY2LjM5OCwxMDQuNUwyNjYuMzk4LDEwOCIvPjxwYXRoIG1hcmtlci1lbmQ9InVybCgjbXktc3ZnX2Zsb3djaGFydC12Mi1wb2ludEVuZCkiIHN0eWxlPSIiIGNsYXNzPSJlZGdlLXRoaWNrbmVzcy1ub3JtYWwgZWRnZS1wYXR0ZXJuLXNvbGlkIGVkZ2UtdGhpY2tuZXNzLW5vcm1hbCBlZGdlLXBhdHRlcm4tc29saWQgZmxvd2NoYXJ0LWxpbmsiIGlkPSJMX0JfQ18wIiBkPSJNMjY2LjM5OCwxNjZMMjY2LjM5OCwxNzAuMTY3QzI2Ni4zOTgsMTc0LjMzMywyNjYuMzk4LDE4Mi42NjcsMjY2LjQ2OSwxOTAuNDE3QzI2Ni41MzksMTk4LjE2NywyNjYuNjc5LDIwNS4zMzQsMjY2Ljc1LDIwOC45MTdMMjY2LjgyLDIxMi41MDEiLz48cGF0aCBtYXJrZXItZW5kPSJ1cmwoI215LXN2Z19mbG93Y2hhcnQtdjItcG9pbnRFbmQpIiBzdHlsZT0iIiBjbGFzcz0iZWRnZS10aGlja25lc3Mtbm9ybWFsIGVkZ2UtcGF0dGVybi1zb2xpZCBlZGdlLXRoaWNrbmVzcy1ub3JtYWwgZWRnZS1wYXR0ZXJuLXNvbGlkIGZsb3djaGFydC1saW5rIiBpZD0iTF9DX0RfMCIgZD0iTTIyMy4wOTIsMzM5LjEzMUwyMDguMDM5LDM1Mi41MTVDMTkyLjk4NiwzNjUuOSwxNjIuODc5LDM5Mi42NjksMTQ3LjgyNiw0MTEuNTUzQzEzMi43NzMsNDMwLjQzOCwxMzIuNzczLDQ0MS40MzgsMTMyLjc3Myw0NDYuOTM4TDEzMi43NzMsNDUyLjQzOCIvPjxwYXRoIG1hcmtlci1lbmQ9InVybCgjbXktc3ZnX2Zsb3djaGFydC12Mi1wb2ludEVuZCkiIHN0eWxlPSIiIGNsYXNzPSJlZGdlLXRoaWNrbmVzcy1ub3JtYWwgZWRnZS1wYXR0ZXJuLXNvbGlkIGVkZ2UtdGhpY2tuZXNzLW5vcm1hbCBlZGdlLXBhdHRlcm4tc29saWQgZmxvd2NoYXJ0LWxpbmsiIGlkPSJMX0NfRV8wIiBkPSJNMzEwLjcwNSwzMzkuMTMxTDMyNS41OTIsMzUyLjUxNUMzNDAuNDc4LDM2NS45LDM3MC4yNTEsMzkyLjY2OSwzODUuMTM3LDQxMS41NTNDNDAwLjAyMyw0MzAuNDM4LDQwMC4wMjMsNDQxLjQzOCw0MDAuMDIzLDQ0Ni45MzhMNDAwLjAyMyw0NTIuNDM4Ii8+PHBhdGggbWFya2VyLWVuZD0idXJsKCNteS1zdmdfZmxvd2NoYXJ0LXYyLXBvaW50RW5kKSIgc3R5bGU9IiIgY2xhc3M9ImVkZ2UtdGhpY2tuZXNzLW5vcm1hbCBlZGdlLXBhdHRlcm4tc29saWQgZWRnZS10aGlja25lc3Mtbm9ybWFsIGVkZ2UtcGF0dGVybi1zb2xpZCBmbG93Y2hhcnQtbGluayIgaWQ9IkxfRV9GXzAiIGQ9Ik00MDAuMDIzLDUxMC40MzhMNDAwLjAyMyw1MTQuNjA0QzQwMC4wMjMsNTE4Ljc3MSw0MDAuMDIzLDUyNy4xMDQsNDAwLjAyMyw1MzQuNzcxQzQwMC4wMjMsNTQyLjQzOCw0MDAuMDIzLDU0OS40MzgsNDAwLjAyMyw1NTIuOTM4TDQwMC4wMjMsNTU2LjQzOCIvPjxwYXRoIG1hcmtlci1lbmQ9InVybCgjbXktc3ZnX2Zsb3djaGFydC12Mi1wb2ludEVuZCkiIHN0eWxlPSIiIGNsYXNzPSJlZGdlLXRoaWNrbmVzcy1ub3JtYWwgZWRnZS1wYXR0ZXJuLXNvbGlkIGVkZ2UtdGhpY2tuZXNzLW5vcm1hbCBlZGdlLXBhdHRlcm4tc29saWQgZmxvd2NoYXJ0LWxpbmsiIGlkPSJMX0ZfR18wIiBkPSJNNDAwLjAyMyw2MzguNDM4TDQwMC4wMjMsNjQyLjYwNEM0MDAuMDIzLDY0Ni43NzEsNDAwLjAyMyw2NTUuMTA0LDQwMC4wMjMsNjYyLjc3MUM0MDAuMDIzLDY3MC40MzgsNDAwLjAyMyw2NzcuNDM4LDQwMC4wMjMsNjgwLjkzOEw0MDAuMDIzLDY4NC40MzgiLz48cGF0aCBtYXJrZXItZW5kPSJ1cmwoI215LXN2Z19mbG93Y2hhcnQtdjItcG9pbnRFbmQpIiBzdHlsZT0iIiBjbGFzcz0iZWRnZS10aGlja25lc3Mtbm9ybWFsIGVkZ2UtcGF0dGVybi1zb2xpZCBlZGdlLXRoaWNrbmVzcy1ub3JtYWwgZWRnZS1wYXR0ZXJuLXNvbGlkIGZsb3djaGFydC1saW5rIiBpZD0iTF9HX0hfMCIgZD0iTTQwMC4wMjMsNzY2LjQzOEw0MDAuMDIzLDc3MC42MDRDNDAwLjAyMyw3NzQuNzcxLDQwMC4wMjMsNzgzLjEwNCw0MDAuMDIzLDc5MC43NzFDNDAwLjAyMyw3OTguNDM4LDQwMC4wMjMsODA1LjQzOCw0MDAuMDIzLDgwOC45MzhMNDAwLjAyMyw4MTIuNDM4Ii8+PC9nPjxnIGNsYXNzPSJlZGdlTGFiZWxzIj48ZyBjbGFzcz0iZWRnZUxhYmVsIj48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLCAwKSIgY2xhc3M9ImxhYmVsIj48Zm9yZWlnbk9iamVjdCBoZWlnaHQ9IjAiIHdpZHRoPSIwIj48ZGl2IHN0eWxlPSJkaXNwbGF5OiB0YWJsZS1jZWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyBsaW5lLWhlaWdodDogMS41OyBtYXgtd2lkdGg6IDIwMHB4OyB0ZXh0LWFsaWduOiBjZW50ZXI7IiBjbGFzcz0ibGFiZWxCa2ciIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIj48c3BhbiBjbGFzcz0iZWRnZUxhYmVsIj48L3NwYW4+PC9kaXY+PC9mb3JlaWduT2JqZWN0PjwvZz48L2c+PGcgY2xhc3M9ImVkZ2VMYWJlbCI+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwgMCkiIGNsYXNzPSJsYWJlbCI+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSIwIiB3aWR0aD0iMCI+PGRpdiBzdHlsZT0iZGlzcGxheTogdGFibGUtY2VsbDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgbGluZS1oZWlnaHQ6IDEuNTsgbWF4LXdpZHRoOiAyMDBweDsgdGV4dC1hbGlnbjogY2VudGVyOyIgY2xhc3M9ImxhYmVsQmtnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCI+PHNwYW4gY2xhc3M9ImVkZ2VMYWJlbCI+PC9zcGFuPjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PC9nPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDEzMi43NzM0Mzc1LCA0MTkuNDM3NSkiIGNsYXNzPSJlZGdlTGFiZWwiPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMS4zMjgxMjUsIC0xMikiIGNsYXNzPSJsYWJlbCI+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSIyNCIgd2lkdGg9IjIyLjY1NjI1Ij48ZGl2IHN0eWxlPSJkaXNwbGF5OiB0YWJsZS1jZWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyBsaW5lLWhlaWdodDogMS41OyBtYXgtd2lkdGg6IDIwMHB4OyB0ZXh0LWFsaWduOiBjZW50ZXI7IiBjbGFzcz0ibGFiZWxCa2ciIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIj48c3BhbiBjbGFzcz0iZWRnZUxhYmVsIj48cD5ZZXM8L3A+PC9zcGFuPjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PC9nPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDQwMC4wMjM0Mzc1LCA0MTkuNDM3NSkiIGNsYXNzPSJlZGdlTGFiZWwiPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC05LjM5ODQzNzUsIC0xMikiIGNsYXNzPSJsYWJlbCI+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSIyNCIgd2lkdGg9IjE4Ljc5Njg3NSI+PGRpdiBzdHlsZT0iZGlzcGxheTogdGFibGUtY2VsbDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgbGluZS1oZWlnaHQ6IDEuNTsgbWF4LXdpZHRoOiAyMDBweDsgdGV4dC1hbGlnbjogY2VudGVyOyIgY2xhc3M9ImxhYmVsQmtnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCI+PHNwYW4gY2xhc3M9ImVkZ2VMYWJlbCI+PHA+Tm88L3A+PC9zcGFuPjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PC9nPjxnIGNsYXNzPSJlZGdlTGFiZWwiPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAsIDApIiBjbGFzcz0ibGFiZWwiPjxmb3JlaWduT2JqZWN0IGhlaWdodD0iMCIgd2lkdGg9IjAiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IHRhYmxlLWNlbGw7IHdoaXRlLXNwYWNlOiBub3dyYXA7IGxpbmUtaGVpZ2h0OiAxLjU7IG1heC13aWR0aDogMjAwcHg7IHRleHQtYWxpZ246IGNlbnRlcjsiIGNsYXNzPSJsYWJlbEJrZyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiPjxzcGFuIGNsYXNzPSJlZGdlTGFiZWwiPjwvc3Bhbj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjwvZz48ZyBjbGFzcz0iZWRnZUxhYmVsIj48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLCAwKSIgY2xhc3M9ImxhYmVsIj48Zm9yZWlnbk9iamVjdCBoZWlnaHQ9IjAiIHdpZHRoPSIwIj48ZGl2IHN0eWxlPSJkaXNwbGF5OiB0YWJsZS1jZWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyBsaW5lLWhlaWdodDogMS41OyBtYXgtd2lkdGg6IDIwMHB4OyB0ZXh0LWFsaWduOiBjZW50ZXI7IiBjbGFzcz0ibGFiZWxCa2ciIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIj48c3BhbiBjbGFzcz0iZWRnZUxhYmVsIj48L3NwYW4+PC9kaXY+PC9mb3JlaWduT2JqZWN0PjwvZz48L2c+PGcgY2xhc3M9ImVkZ2VMYWJlbCI+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwgMCkiIGNsYXNzPSJsYWJlbCI+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSIwIiB3aWR0aD0iMCI+PGRpdiBzdHlsZT0iZGlzcGxheTogdGFibGUtY2VsbDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgbGluZS1oZWlnaHQ6IDEuNTsgbWF4LXdpZHRoOiAyMDBweDsgdGV4dC1hbGlnbjogY2VudGVyOyIgY2xhc3M9ImxhYmVsQmtnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCI+PHNwYW4gY2xhc3M9ImVkZ2VMYWJlbCI+PC9zcGFuPjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PC9nPjwvZz48ZyBjbGFzcz0ibm9kZXMiPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDI2Ni4zOTg0Mzc1LCAzNSkiIGlkPSJmbG93Y2hhcnQtQS0wIiBjbGFzcz0ibm9kZSBkZWZhdWx0Ij48cmVjdCBoZWlnaHQ9IjU0IiB3aWR0aD0iMTUxLjI4MTI1IiB5PSItMjciIHg9Ii03NS42NDA2MjUiIHN0eWxlPSIiIGNsYXNzPSJiYXNpYyBsYWJlbC1jb250YWluZXIiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNDUuNjQwNjI1LCAtMTIpIiBzdHlsZT0iIiBjbGFzcz0ibGFiZWwiPjxyZWN0Lz48Zm9yZWlnbk9iamVjdCBoZWlnaHQ9IjI0IiB3aWR0aD0iOTEuMjgxMjUiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IHRhYmxlLWNlbGw7IHdoaXRlLXNwYWNlOiBub3dyYXA7IGxpbmUtaGVpZ2h0OiAxLjU7IG1heC13aWR0aDogMjAwcHg7IHRleHQtYWxpZ246IGNlbnRlcjsiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIj48c3BhbiBjbGFzcz0ibm9kZUxhYmVsIj48cD5SZWFkIFNhbXBsZTwvcD48L3NwYW4+PC9kaXY+PC9mb3JlaWduT2JqZWN0PjwvZz48L2c+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjY2LjM5ODQzNzUsIDEzOSkiIGlkPSJmbG93Y2hhcnQtQi0xIiBjbGFzcz0ibm9kZSBkZWZhdWx0Ij48cmVjdCBoZWlnaHQ9IjU0IiB3aWR0aD0iMTY1LjcxODc1IiB5PSItMjciIHg9Ii04Mi44NTkzNzUiIHN0eWxlPSIiIGNsYXNzPSJiYXNpYyBsYWJlbC1jb250YWluZXIiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNTIuODU5Mzc1LCAtMTIpIiBzdHlsZT0iIiBjbGFzcz0ibGFiZWwiPjxyZWN0Lz48Zm9yZWlnbk9iamVjdCBoZWlnaHQ9IjI0IiB3aWR0aD0iMTA1LjcxODc1Ij48ZGl2IHN0eWxlPSJkaXNwbGF5OiB0YWJsZS1jZWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyBsaW5lLWhlaWdodDogMS41OyBtYXgtd2lkdGg6IDIwMHB4OyB0ZXh0LWFsaWduOiBjZW50ZXI7IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCI+PHNwYW4gY2xhc3M9Im5vZGVMYWJlbCI+PHA+VHJ5IENTViBTbmlmZmVyPC9wPjwvc3Bhbj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjwvZz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgyNjYuMzk4NDM3NSwgMjk5LjIxODc1KSIgaWQ9ImZsb3djaGFydC1DLTMiIGNsYXNzPSJub2RlIGRlZmF1bHQiPjxwb2x5Z29uIHRyYW5zZm9ybT0idHJhbnNsYXRlKC04My4yMTg3NSw4My4yMTg3NSkiIGNsYXNzPSJsYWJlbC1jb250YWluZXIiIHBvaW50cz0iODMuMjE4NzUsMCAxNjYuNDM3NSwtODMuMjE4NzUgODMuMjE4NzUsLTE2Ni40Mzc1IDAsLTgzLjIxODc1Ii8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTU2LjIxODc1LCAtMTIpIiBzdHlsZT0iIiBjbGFzcz0ibGFiZWwiPjxyZWN0Lz48Zm9yZWlnbk9iamVjdCBoZWlnaHQ9IjI0IiB3aWR0aD0iMTEyLjQzNzUiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IHRhYmxlLWNlbGw7IHdoaXRlLXNwYWNlOiBub3dyYXA7IGxpbmUtaGVpZ2h0OiAxLjU7IG1heC13aWR0aDogMjAwcHg7IHRleHQtYWxpZ246IGNlbnRlcjsiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIj48c3BhbiBjbGFzcz0ibm9kZUxhYmVsIj48cD5TbmlmZmVyIFN1Y2Nlc3M/PC9wPjwvc3Bhbj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjwvZz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMzIuNzczNDM3NSwgNDgzLjQzNzUpIiBpZD0iZmxvd2NoYXJ0LUQtNSIgY2xhc3M9Im5vZGUgZGVmYXVsdCI+PHJlY3QgaGVpZ2h0PSI1NCIgd2lkdGg9IjI0OS41NDY4NzUiIHk9Ii0yNyIgeD0iLTEyNC43NzM0Mzc1IiBzdHlsZT0iZmlsbDojZThmNWU4ICFpbXBvcnRhbnQiIGNsYXNzPSJiYXNpYyBsYWJlbC1jb250YWluZXIiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtOTQuNzczNDM3NSwgLTEyKSIgc3R5bGU9IiIgY2xhc3M9ImxhYmVsIj48cmVjdC8+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSIyNCIgd2lkdGg9IjE4OS41NDY4NzUiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IHRhYmxlLWNlbGw7IHdoaXRlLXNwYWNlOiBub3dyYXA7IGxpbmUtaGVpZ2h0OiAxLjU7IG1heC13aWR0aDogMjAwcHg7IHRleHQtYWxpZ246IGNlbnRlcjsiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIj48c3BhbiBjbGFzcz0ibm9kZUxhYmVsIj48cD5SZXR1cm4gRGV0ZWN0ZWQgRGVsaW1pdGVyPC9wPjwvc3Bhbj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjwvZz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0MDAuMDIzNDM3NSwgNDgzLjQzNzUpIiBpZD0iZmxvd2NoYXJ0LUUtNyIgY2xhc3M9Im5vZGUgZGVmYXVsdCI+PHJlY3QgaGVpZ2h0PSI1NCIgd2lkdGg9IjE4NC45NTMxMjUiIHk9Ii0yNyIgeD0iLTkyLjQ3NjU2MjUiIHN0eWxlPSIiIGNsYXNzPSJiYXNpYyBsYWJlbC1jb250YWluZXIiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNjIuNDc2NTYyNSwgLTEyKSIgc3R5bGU9IiIgY2xhc3M9ImxhYmVsIj48cmVjdC8+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSIyNCIgd2lkdGg9IjEyNC45NTMxMjUiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IHRhYmxlLWNlbGw7IHdoaXRlLXNwYWNlOiBub3dyYXA7IGxpbmUtaGVpZ2h0OiAxLjU7IG1heC13aWR0aDogMjAwcHg7IHRleHQtYWxpZ246IGNlbnRlcjsiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIj48c3BhbiBjbGFzcz0ibm9kZUxhYmVsIj48cD5NYW51YWwgRGV0ZWN0aW9uPC9wPjwvc3Bhbj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjwvZz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0MDAuMDIzNDM3NSwgNTk5LjQzNzUpIiBpZD0iZmxvd2NoYXJ0LUYtOSIgY2xhc3M9Im5vZGUgZGVmYXVsdCI+PHJlY3QgaGVpZ2h0PSI3OCIgd2lkdGg9IjI2MCIgeT0iLTM5IiB4PSItMTMwIiBzdHlsZT0iIiBjbGFzcz0iYmFzaWMgbGFiZWwtY29udGFpbmVyIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEwMCwgLTI0KSIgc3R5bGU9IiIgY2xhc3M9ImxhYmVsIj48cmVjdC8+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSI0OCIgd2lkdGg9IjIwMCI+PGRpdiBzdHlsZT0iZGlzcGxheTogdGFibGU7IHdoaXRlLXNwYWNlOiBicmVhay1zcGFjZXM7IGxpbmUtaGVpZ2h0OiAxLjU7IG1heC13aWR0aDogMjAwcHg7IHRleHQtYWxpZ246IGNlbnRlcjsgd2lkdGg6IDIwMHB4OyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiPjxzcGFuIGNsYXNzPSJub2RlTGFiZWwiPjxwPkNvdW50IERlbGltaXRlciBPY2N1cnJlbmNlczwvcD48L3NwYW4+PC9kaXY+PC9mb3JlaWduT2JqZWN0PjwvZz48L2c+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNDAwLjAyMzQzNzUsIDcyNy40Mzc1KSIgaWQ9ImZsb3djaGFydC1HLTExIiBjbGFzcz0ibm9kZSBkZWZhdWx0Ij48cmVjdCBoZWlnaHQ9Ijc4IiB3aWR0aD0iMjYwIiB5PSItMzkiIHg9Ii0xMzAiIHN0eWxlPSIiIGNsYXNzPSJiYXNpYyBsYWJlbC1jb250YWluZXIiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTAwLCAtMjQpIiBzdHlsZT0iIiBjbGFzcz0ibGFiZWwiPjxyZWN0Lz48Zm9yZWlnbk9iamVjdCBoZWlnaHQ9IjQ4IiB3aWR0aD0iMjAwIj48ZGl2IHN0eWxlPSJkaXNwbGF5OiB0YWJsZTsgd2hpdGUtc3BhY2U6IGJyZWFrLXNwYWNlczsgbGluZS1oZWlnaHQ6IDEuNTsgbWF4LXdpZHRoOiAyMDBweDsgdGV4dC1hbGlnbjogY2VudGVyOyB3aWR0aDogMjAwcHg7IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCI+PHNwYW4gY2xhc3M9Im5vZGVMYWJlbCI+PHA+Q2hlY2sgQ29uc2lzdGVuY3kgQWNyb3NzIExpbmVzPC9wPjwvc3Bhbj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjwvZz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0MDAuMDIzNDM3NSwgODU1LjQzNzUpIiBpZD0iZmxvd2NoYXJ0LUgtMTMiIGNsYXNzPSJub2RlIGRlZmF1bHQiPjxyZWN0IGhlaWdodD0iNzgiIHdpZHRoPSIyNjAiIHk9Ii0zOSIgeD0iLTEzMCIgc3R5bGU9ImZpbGw6I2U4ZjVlOCAhaW1wb3J0YW50IiBjbGFzcz0iYmFzaWMgbGFiZWwtY29udGFpbmVyIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEwMCwgLTI0KSIgc3R5bGU9IiIgY2xhc3M9ImxhYmVsIj48cmVjdC8+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSI0OCIgd2lkdGg9IjIwMCI+PGRpdiBzdHlsZT0iZGlzcGxheTogdGFibGU7IHdoaXRlLXNwYWNlOiBicmVhay1zcGFjZXM7IGxpbmUtaGVpZ2h0OiAxLjU7IG1heC13aWR0aDogMjAwcHg7IHRleHQtYWxpZ246IGNlbnRlcjsgd2lkdGg6IDIwMHB4OyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiPjxzcGFuIGNsYXNzPSJub2RlTGFiZWwiPjxwPlJldHVybiBNb3N0IENvbnNpc3RlbnQgRGVsaW1pdGVyPC9wPjwvc3Bhbj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjwvZz48L2c+PC9nPjwvZz48L3N2Zz4=" alt="Detection Algorithm" width="600">

## Module Reference

### autocsv_profiler.auto_csv_profiler

Main analysis module containing the comprehensive data analysis functionality.

#### Functions

##### main()
```python
def main(csv_path: str, output_dir: str) -> None
```
Internal main function called by `analyze_csv()`. Handles the complete analysis workflow.

##### check_and_install_packages()
```python
def check_and_install_packages(packages: list) -> None
```
Utility function to check and install required packages.

##### data_info()
```python
def data_info(data_copy: pd.DataFrame, save_dir: str) -> None
```
Generate basic dataset information report.

#### Classes and Data Structures

##### Colors
```python
class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
```

### autocsv_profiler.recognize_delimiter

Delimiter detection module.

#### Functions

##### detect_delimiter()
```python
def detect_delimiter(csv_file: str) -> str
```
Main delimiter detection function (exported to package level).

##### print_csv_head()
```python
def print_csv_head(csv_file: str) -> None
```
Print first few lines of CSV file for manual inspection.

### autocsv_profiler.cli

Command-line interface module.

#### Functions

##### main()
```python
def main() -> None
```
Command-line entry point. Handles argument parsing and execution.

## Data Analysis Components

### Statistical Analysis

#### Descriptive Statistics
```python
# Generated statistics include:
statistics = {
    'count': int,           # Number of non-null values
    'mean': float,          # Arithmetic mean
    'std': float,           # Standard deviation
    'min': float,           # Minimum value
    '25%': float,           # First quartile
    '50%': float,           # Median
    '75%': float,           # Third quartile
    'max': float,           # Maximum value
    'skewness': float,      # Distribution skewness
    'kurtosis': float,      # Distribution kurtosis
    'unique': int,          # Number of unique values
    'mode': float,          # Most frequent value
}
```

#### Missing Value Analysis
```python
# Missing value metrics
missing_info = {
    'column_name': str,
    'missing_count': int,
    'missing_percentage': float,
    'missing_pattern': str,     # 'random', 'structured', 'block'
    'imputation_suggestion': str # 'mean', 'median', 'mode', 'forward_fill'
}
```

#### Outlier Detection
```python
# Outlier detection results
outlier_info = {
    'column_name': str,
    'outlier_count': int,
    'outlier_percentage': float,
    'outlier_threshold_lower': float,
    'outlier_threshold_upper': float,
    'outlier_method': str,      # 'IQR', 'Z-score', 'Modified Z-score'
}
```

### Visualization Components

#### Plot Generation
```python
# Generated visualizations
visualizations = {
    'histograms': {
        'file_pattern': '{column}_histogram.png',
        'description': 'Distribution histogram with KDE overlay'
    },
    'box_plots': {
        'file_pattern': '{column}_boxplot.png', 
        'description': 'Box plot showing quartiles and outliers'
    },
    'correlation_matrix': {
        'file_pattern': 'correlation_heatmap.png',
        'description': 'Correlation heatmap for numerical variables'
    },
    'missing_patterns': {
        'file_pattern': 'missing_values_matrix.png',
        'description': 'Missing value pattern visualization'
    }
}
```

## Advanced Usage Patterns

### Custom Analysis Pipeline

```python
import pandas as pd
from autocsv_profiler import detect_delimiter, analyze_csv
import os

class CSVAnalyzer:
    """Custom CSV analysis wrapper"""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.delimiter = None
        self.data = None
        self.analysis_dir = None
    
    def load_data(self):
        """Load CSV data with automatic delimiter detection"""
        self.delimiter = detect_delimiter(self.csv_path)
        self.data = pd.read_csv(self.csv_path, delimiter=self.delimiter)
        return self.data
    
    def quick_info(self):
        """Get quick dataset information"""
        if self.data is None:
            self.load_data()
        
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': dict(self.data.dtypes),
            'missing_values': self.data.isnull().sum().sum(),
            'memory_usage': self.data.memory_usage(deep=True).sum()
        }
    
    def run_analysis(self, output_dir: str = None):
        """Run comprehensive analysis"""
        if output_dir is None:
            base_name = os.path.splitext(os.path.basename(self.csv_path))[0]
            output_dir = f"{base_name}_analysis"
        
        self.analysis_dir = output_dir
        analyze_csv(self.csv_path, output_dir)
        return output_dir
    
    def get_results(self):
        """Get analysis results as dictionary"""
        if self.analysis_dir is None:
            raise ValueError("Analysis not run yet. Call run_analysis() first.")
        
        results = {}
        
        # Read text reports
        report_files = [
            'dataset_info.txt',
            'summary_statistics_all.txt', 
            'categorical_summary.txt',
            'missing_values_report.txt',
            'outliers_summary.txt'
        ]
        
        for report_file in report_files:
            file_path = os.path.join(self.analysis_dir, report_file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    results[report_file] = f.read()
        
        return results

# Usage example
analyzer = CSVAnalyzer("sales_data.csv")
info = analyzer.quick_info()
print(f"Dataset: {info['shape'][0]} rows, {info['shape'][1]} columns")

output_dir = analyzer.run_analysis()
results = analyzer.get_results()
```

### Batch Processing Framework

```python
from autocsv_profiler import analyze_csv, detect_delimiter
import os
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

class BatchCSVAnalyzer:
    """Batch processing for multiple CSV files"""
    
    def __init__(self, input_dir: str, output_base_dir: str, max_workers: int = 4):
        self.input_dir = input_dir
        self.output_base_dir = output_base_dir
        self.max_workers = max_workers
        self.results = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def find_csv_files(self):
        """Find all CSV files in input directory"""
        pattern = os.path.join(self.input_dir, "*.csv")
        return glob.glob(pattern)
    
    def analyze_single_file(self, csv_path: str):
        """Analyze a single CSV file"""
        filename = os.path.basename(csv_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_dir = os.path.join(self.output_base_dir, f"{name_without_ext}_analysis")
        
        try:
            self.logger.info(f"Starting analysis: {filename}")
            
            # Quick validation
            delimiter = detect_delimiter(csv_path)
            self.logger.info(f"Detected delimiter for {filename}: '{delimiter}'")
            
            # Run analysis
            analyze_csv(csv_path, output_dir)
            
            return {
                'file': filename,
                'status': 'success',
                'output_dir': output_dir,
                'delimiter': delimiter
            }
            
        except Exception as e:
            self.logger.error(f"Failed to analyze {filename}: {e}")
            return {
                'file': filename,
                'status': 'failed',
                'error': str(e)
            }
    
    def run_batch_analysis(self):
        """Run analysis on all CSV files"""
        csv_files = self.find_csv_files()
        
        if not csv_files:
            self.logger.warning(f"No CSV files found in {self.input_dir}")
            return {}
        
        self.logger.info(f"Found {len(csv_files)} CSV files to analyze")
        
        # Create output directory
        os.makedirs(self.output_base_dir, exist_ok=True)
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(self.analyze_single_file, csv_file): csv_file 
                for csv_file in csv_files
            }
            
            for future in as_completed(future_to_file):
                result = future.result()
                self.results[result['file']] = result
                
                if result['status'] == 'success':
                    self.logger.info(f"✓ Completed: {result['file']}")
                else:
                    self.logger.error(f"✗ Failed: {result['file']}")
        
        return self.results
    
    def generate_summary_report(self):
        """Generate summary report of batch analysis"""
        if not self.results:
            return "No analysis results available"
        
        total_files = len(self.results)
        successful = sum(1 for r in self.results.values() if r['status'] == 'success')
        failed = total_files - successful
        
        summary = f"""
Batch Analysis Summary
=====================
Total files processed: {total_files}
Successful analyses: {successful}
Failed analyses: {failed}
Success rate: {(successful/total_files)*100:.1f}%

Detailed Results:
"""
        
        for filename, result in self.results.items():
            if result['status'] == 'success':
                summary += f"✓ {filename} -> {result['output_dir']}\n"
            else:
                summary += f"✗ {filename} -> {result['error']}\n"
        
        # Save summary
        summary_path = os.path.join(self.output_base_dir, "batch_analysis_summary.txt")
        with open(summary_path, 'w') as f:
            f.write(summary)
        
        return summary

# Usage example
batch_analyzer = BatchCSVAnalyzer("./data", "./batch_results", max_workers=2)
results = batch_analyzer.run_batch_analysis()
summary = batch_analyzer.generate_summary_report()
print(summary)
```

## Error Handling

### Common Exceptions

```python
from autocsv_profiler import analyze_csv, detect_delimiter

def robust_analysis(csv_path: str, output_dir: str):
    """Robust analysis with comprehensive error handling"""
    
    try:
        # Validate input file
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        if not csv_path.lower().endswith('.csv'):
            print("Warning: File doesn't have .csv extension")
        
        # Check file size
        file_size = os.path.getsize(csv_path)
        if file_size > 500 * 1024 * 1024:  # 500MB
            print(f"Warning: Large file ({file_size/1024/1024:.1f}MB)")
        
        # Detect delimiter
        delimiter = detect_delimiter(csv_path)
        print(f"Detected delimiter: '{delimiter}'")
        
        # Run analysis
        analyze_csv(csv_path, output_dir)
        print(f"Analysis completed successfully: {output_dir}")
        
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except MemoryError as e:
        print(f"Memory error: {e}")
        print("Try with a smaller dataset or more RAM")
    except ValueError as e:
        print(f"Data error: {e}")
        print("Check CSV format and delimiter")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

# Usage
robust_analysis("problematic_data.csv", "safe_analysis")
```

## Performance Considerations

### Memory Usage
```python
import psutil
import os
from autocsv_profiler import analyze_csv

def memory_aware_analysis(csv_path: str, output_dir: str, memory_limit_gb: float = 4.0):
    """Analyze CSV with memory monitoring"""
    
    # Check available memory
    available_memory = psutil.virtual_memory().available / (1024**3)  # GB
    
    if available_memory < memory_limit_gb:
        print(f"Warning: Low memory ({available_memory:.1f}GB available)")
    
    # Monitor memory during analysis
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / (1024**2)  # MB
    
    print(f"Starting analysis (Initial memory: {initial_memory:.1f}MB)")
    
    try:
        analyze_csv(csv_path, output_dir)
        
        final_memory = process.memory_info().rss / (1024**2)  # MB
        memory_used = final_memory - initial_memory
        
        print(f"Analysis complete (Memory used: {memory_used:.1f}MB)")
        
    except MemoryError:
        print("Memory error occurred. Consider:")
        print("1. Using a smaller sample of the data")
        print("2. Increasing available RAM") 
        print("3. Processing data in chunks")

# Usage
memory_aware_analysis("large_dataset.csv", "memory_analysis")
```

## Package Information

### Version Management
```python
import autocsv_profiler

# Get version information
print(f"AutoCSV Profiler version: {autocsv_profiler.__version__}")
print(f"Author: {autocsv_profiler.__author__}")
print(f"License: {autocsv_profiler.__license__}")

# Check if specific features are available
try:
    from autocsv_profiler import analyze_csv
    print("Core analysis available")
except ImportError:
    print("Core analysis not available")

try:
    from autocsv_profiler import detect_delimiter
    print("Delimiter detection available")
except ImportError:
    print("Delimiter detection not available")
```

### Dependencies
```python
# Check if required packages are available
def check_dependencies():
    """Check if all required packages are available"""
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'scipy', 'sklearn', 'statsmodels', 'tqdm',
        'tableone', 'missingno', 'tabulate'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {missing_packages}")
        print("Install with: pip install " + " ".join(missing_packages))
    else:
        print("All dependencies are available")

check_dependencies()
```

## Integration Examples

### Jupyter Notebook Integration
```python
# In Jupyter notebook cell
from autocsv_profiler import analyze_csv
import pandas as pd
from IPython.display import HTML, display

# Run analysis
csv_file = "notebook_data.csv"
output_dir = "notebook_analysis"
analyze_csv(csv_file, output_dir)

# Load and display summary
df = pd.read_csv(csv_file)
print(f"Dataset shape: {df.shape}")

# Display interactive report
html_report = f"{output_dir}/distinct_values_count_by_dtype.html"
with open(html_report, 'r') as f:
    display(HTML(f.read()))
```

### Flask Web Application Integration
```python
from flask import Flask, request, render_template, send_file
from autocsv_profiler import analyze_csv
import os
import tempfile

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_endpoint():
    """Web endpoint for CSV analysis"""
    
    if 'csv_file' not in request.files:
        return {'error': 'No file provided'}, 400
    
    file = request.files['csv_file']
    
    if file.filename == '':
        return {'error': 'No file selected'}, 400
    
    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
        file.save(tmp_file.name)
        
        # Create output directory
        output_dir = tempfile.mkdtemp()
        
        try:
            # Run analysis
            analyze_csv(tmp_file.name, output_dir)
            
            # Return analysis results
            return {
                'status': 'success',
                'output_dir': output_dir,
                'files': os.listdir(output_dir)
            }
            
        except Exception as e:
            return {'error': str(e)}, 500
        
        finally:
            # Clean up uploaded file
            os.unlink(tmp_file.name)

if __name__ == '__main__':
    app.run(debug=True)
```

This API reference provides comprehensive documentation for integrating AutoCSV Profiler into various Python applications and workflows.