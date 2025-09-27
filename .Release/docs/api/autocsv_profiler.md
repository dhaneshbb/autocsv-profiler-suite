# autocsv_profiler

Main package interface providing unified access to CSV analysis engines.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Public API](#public-api)
- [Configuration and Settings](#configuration-and-settings)
- [Exception Hierarchy](#exception-hierarchy)
- [Logging System](#logging-system)
- [Version Information](#version-information)
- [Lazy Loading Architecture](#lazy-loading-architecture)
- [Usage Patterns](#usage-patterns)
- [Environment Requirements](#environment-requirements)
- [Performance Considerations](#performance-considerations)
- [Integration Examples](#integration-examples)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

The `autocsv_profiler` module serves as the entry point for the AutoCSV Profiler Suite. It implements lazy loading architecture to handle environment-specific dependencies and provides unified API across multiple conda environments.

## Key Features

- **Lazy Loading**: Engines are imported only when needed to reduce startup time
- **Environment Awareness**: Handling of missing dependencies across conda environments
- **API**: Single interface for multiple profiling engines
- **Error Handling**: Exception hierarchy for error conditions

## Public API

### Primary Functions

#### `profile_csv(csv_file_path, output_dir=None, engine="auto")`

Main function for CSV analysis.

**⚠️ Multi-Environment Limitation:** This function may not work reliably due to the multi-environment architecture. Engines run in isolated conda environments and may not be available in the base Python environment.

**Recommended Approach:** Use the command-line interface:

```bash
# Interactive mode (recommended)
python bin/run_analysis.py

# Direct file analysis
python bin/run_analysis.py data.csv

# Debug mode with detailed output
python bin/run_analysis.py --debug
```

**Python API Usage** (with error handling):

```python
try:
    from autocsv_profiler import profile_csv

    # This may raise ImportError for specific engines
    report_path = profile_csv("data.csv", "output_directory/")

except ImportError as e:
    print(f"Engine not available: {e}")
    print("Use CLI: python bin/run_analysis.py data.csv")
```

**Parameters:**
- `csv_file_path` (str): Path to the CSV file to analyze
- `output_dir` (Optional[str]): Directory to save outputs. If None, creates timestamped directory
- `engine` (str): Profiling engine to use. Options: "auto", "ydata", "sweetviz", "dataprep"

**Returns:**
- `str`: Path to the generated report

**Raises:**
- `FileNotFoundError`: If CSV file doesn't exist
- `AutoCSVProfilerError`: If profiling fails
- `ImportError`: If required profiling engine is not available
- `ValueError`: If unknown engine specified

### Internal Implementation

Engine loading functions are internal implementation details and not part of the public API. Use the main `profile_csv()` function for usage.

## Configuration and Settings

### Settings Management

```python
from autocsv_profiler import settings, Settings

# Access configuration values
chunk_size = settings.get("performance.chunk_size", 10000)
memory_limit = settings.get("performance.memory_limit_gb", 1)

# Check feature availability
if settings.get("delimiter_detection.enabled", True):
    # Use automatic delimiter detection
    pass
```

### Configuration Classes

- `Settings`: Main configuration class for accessing YAML-based settings
- `ConfigValidationError`: Exception raised for configuration validation errors

## Exception Hierarchy

### Core Exceptions

```python
from autocsv_profiler import (
    AutoCSVProfilerError,
    FileProcessingError,
    DelimiterDetectionError,
    ReportGenerationError
)

try:
    result = profile_csv("data.csv", "output/")
except FileProcessingError as e:
    print(f"File error: {e}")
except ReportGenerationError as e:
    print(f"Report generation failed: {e}")
except AutoCSVProfilerError as e:
    print(f"General profiler error: {e}")
```

- `AutoCSVProfilerError`: Base exception for all profiler errors
- `FileProcessingError`: File-related errors (reading, parsing, validation)
- `DelimiterDetectionError`: Delimiter detection failures
- `ReportGenerationError`: Report generation failures

## Logging System

### Logger Access

```python
from autocsv_profiler import get_logger, log_print

logger = get_logger(__name__)
logger.info("Starting analysis")

# Alternative logging with console support
log_print("Processing data...", level="info")
```

## Version Information

### Version Functions

```python
from autocsv_profiler import (
    __version__,
    __version_info__,
    get_version_info,
    get_full_version_info,
    check_python_version
)

print(f"AutoCSV Profiler Suite v{__version__}")
print(get_version_info())
check_python_version()  # Validates Python 3.10+ requirement
```

### Available Version Attributes

- `__version__`: Version string (e.g., "2.0.0")
- `__version_info__`: Version tuple for programmatic comparison
- `__title__`: Package title
- `__description__`: Package description
- `__author__`: Author information
- `__author_email__`: Author contact email
- `__license__`: License type (MIT)
- `__copyright__`: Copyright notice
- `__url__`: Project URL
- `__status__`: Development status

## Lazy Loading Architecture

### Implementation Pattern

The package uses lazy loading to handle environment-specific dependencies:

```python
# Global placeholders
auto_csv_main = None
run_analysis = None
generate_ydata_profiling_report = None

def _load_main_engine():
    global auto_csv_main, run_analysis, analyze_csv
    if auto_csv_main is None:
        try:
            from .engines.main.analyzer import main as analyze_csv
            from .engines.main.analyzer import run_analysis
            auto_csv_main = analyze_csv
        except ImportError:
            auto_csv_main = None
            run_analysis = None
    return auto_csv_main, run_analysis, analyze_csv
```

### Benefits

1. **Minimal Startup Time**: Only imports modules when actually used
2. **Environment Isolation**: Handles missing dependencies gracefully
3. **Memory Efficiency**: Avoids loading unused engines
4. **Graceful Degradation**: Continues working with partial functionality

## Usage Patterns

### Basic Analysis

```python
from autocsv_profiler import profile_csv

# Simple analysis with automatic engine selection
report_path = profile_csv("sales_data.csv")
print(f"Report saved to: {report_path}")
```

### Engine-Specific Analysis

```python
from autocsv_profiler import profile_csv

# Use specific engines for different purposes
quick_overview = profile_csv("data.csv", "outputs/", engine="sweetviz")
detailed_analysis = profile_csv("data.csv", "outputs/", engine="ydata")
eda_report = profile_csv("data.csv", "outputs/", engine="dataprep")
```

### Error Handling

```python
from autocsv_profiler import profile_csv, AutoCSVProfilerError

engines = ["ydata", "sweetviz", "dataprep"]
for engine in engines:
    try:
        result = profile_csv("data.csv", "outputs/", engine=engine)
        print(f"{engine} analysis completed: {result}")
        break
    except ImportError:
        print(f"{engine} engine not available")
    except AutoCSVProfilerError as e:
        print(f"{engine} analysis failed: {e}")
```

### Batch Processing

```python
import pandas as pd
from pathlib import Path
from autocsv_profiler import profile_csv

def analyze_multiple_files(csv_files, output_base_dir):
    results = {}
    for csv_file in csv_files:
        try:
            output_dir = f"{output_base_dir}/{csv_file.stem}"
            report_path = profile_csv(str(csv_file), output_dir)
            results[csv_file.name] = {"success": True, "path": report_path}
        except Exception as e:
            results[csv_file.name] = {"success": False, "error": str(e)}
    return results

# Usage
csv_files = Path("data").glob("*.csv")
results = analyze_multiple_files(csv_files, "analysis_outputs")
```

## Environment Requirements

### Conda Environments

The package requires specific conda environments for different engines to resolve dependency conflicts.

**For environment specifications and dependency conflict details, see [Architecture Guide](../ARCHITECTURE.md#dependency-conflict-resolution).**

## Performance Considerations

### Memory Management

The package includes automatic memory management:

```python
from autocsv_profiler import settings

# Check current memory limits
memory_limit = settings.get("performance.memory_limit_gb", 1)
chunk_size = settings.get("performance.chunk_size", 10000)

# Large files are automatically chunked based on these settings
```

### Engine Selection for Performance

- **SweetViz**: Fastest, for data overviews
- **Main Engine**: Balanced performance and detail
- **YData Profiling**: Most detailed, slowest
- **DataPrep**: Moderate speed, good visualizations

## Integration Examples

### Jupyter Notebook Integration

```python
# In Jupyter notebook
from autocsv_profiler import profile_csv
import pandas as pd
from IPython.display import HTML, display

# Generate report
report_path = profile_csv("data.csv", engine="ydata")

# Display in notebook
with open(report_path, 'r') as f:
    display(HTML(f.read()))
```

### Flask Application Integration

```python
from flask import Flask, request, send_file
from autocsv_profiler import profile_csv
import tempfile
import os

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_csv():
    file = request.files['csv_file']
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        file.save(tmp.name)
        try:
            report_path = profile_csv(tmp.name, engine="sweetviz")
            return send_file(report_path, as_attachment=True)
        finally:
            os.unlink(tmp.name)
```

## Troubleshooting

### Common Import Errors

```python
from autocsv_profiler import profile_csv

try:
    result = profile_csv("data.csv", engine="ydata")
except ImportError as e:
    if "YData Profiling not available" in str(e):
        # Fallback to SweetViz
        result = profile_csv("data.csv", engine="sweetviz")
    else:
        # Use main engine
        result = profile_csv("data.csv", engine="auto")
```

### Environment Verification

```python
from autocsv_profiler import (
    _load_main_engine,
    _load_ydata_engine,
    _load_sweetviz_engine,
    _load_dataprep_engine
)

# Check engine availability
engines = {
    "main": _load_main_engine()[0],
    "ydata": _load_ydata_engine(),
    "sweetviz": _load_sweetviz_engine(),
    "dataprep": _load_dataprep_engine()
}

available_engines = [name for name, engine in engines.items() if engine is not None]
print(f"Available engines: {available_engines}")
```

## See Also

- [base](base.md) - BaseProfiler abstract class
- [config](config.md) - Configuration system
- [core modules](README.md#core-modules) - Core utilities and exceptions
- [engines](engines/) - Engine implementations
- [ui](ui/) - User interface components
- [version](../../autocsv_profiler/version.py) - Version management