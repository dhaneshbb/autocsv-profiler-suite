# base

Abstract base classes and common functionality for all profiling engines.

## Table of Contents

- [Overview](#overview)
- [Classes](#classes)
- [Exceptions](#exceptions)
- [Dependencies and Optional Features](#dependencies-and-optional-features)
- [Usage Patterns](#usage-patterns)
- [Memory Management](#memory-management)
- [Standalone Usage](#standalone-usage)
- [Integration with Engines](#integration-with-engines)
- [See Also](#see-also)

## Overview

The `base` module provides the foundation for all CSV profiling engines in the AutoCSV Profiler Suite. It defines abstract base classes, exceptions, and shared functionality for data loading, memory management, and report generation.

## Classes

### BaseProfiler

Abstract base class for all CSV profiling engines.

```python
from autocsv_profiler.base import BaseProfiler
from pathlib import Path

class CustomProfiler(BaseProfiler):
    def generate_report(self) -> str:
        # Custom implementation
        report_path = self.output_dir / "custom_report.html"
        self._save_report(analysis_result, report_path)
        return str(report_path)

    def get_report_name(self) -> str:
        return "Custom Profiler"
```

#### Constructor

```python
def __init__(
    self,
    csv_path: Union[str, Path],
    delimiter: str,
    output_dir: Union[str, Path],
    chunk_size: int = 10000,
    memory_limit_gb: float = 1.0,
)
```

**Parameters:**
- `csv_path`: Path to the CSV file to profile
- `delimiter`: CSV delimiter character (e.g., ",", ";", "\t")
- `output_dir`: Directory to save reports (created if doesn't exist)
- `chunk_size`: Number of rows per chunk for large files (default: 10,000)
- `memory_limit_gb`: Memory limit in GB for processing (default: 1.0)

**Attributes:**
- `csv_path`: Path object for the CSV file
- `delimiter`: Delimiter character used for parsing
- `output_dir`: Path object for output directory
- `chunk_size`: Chunk size for memory management
- `memory_limit_gb`: Memory limit threshold
- `df`: Loaded pandas DataFrame

#### Abstract Methods

##### `generate_report()`

Must be implemented by subclasses to generate the profiling report.

```python
@abstractmethod
def generate_report(self) -> str:
    """Generate the profiling report.

    Returns:
        Path to the generated report file
    """
```

**Returns:**
- `str`: Absolute path to the generated report file

**Should raise:**
- `ReportGenerationError`: If report generation fails

##### `get_report_name()`

Must be implemented by subclasses to return the report type name.

```python
@abstractmethod
def get_report_name(self) -> str:
    """Return the name/type of the report.

    Returns:
        Report name (e.g., "YData Profiling", "SweetViz", etc.)
    """
```

**Returns:**
- `str`: Human-readable name of the profiling engine

#### Instance Methods

##### `run()`

Execute the profiling workflow and generate the report.

```python
profiler = CustomProfiler("data.csv", ",", "output/")
report_path = profiler.run()
if report_path:
    print(f"Report generated: {report_path}")
```

**Returns:**
- `Optional[str]`: Path to generated report, or None if failed

**Features:**
- Calls `generate_report()` with error handling
- Prints success/failure messages with truncated paths
- Returns None on any failure for error handling

##### `get_data_summary()`

Get basic summary information about the loaded dataset.

```python
profiler = CustomProfiler("data.csv", ",", "output/")
summary = profiler.get_data_summary()
print(f"Dataset: {summary['rows']} rows, {summary['columns']} columns")
print(f"Memory usage: {summary['memory_usage_mb']:.2f} MB")
```

**Returns:**
- `dict`: Dictionary containing:
  - `rows` (int): Number of rows in the dataset
  - `columns` (int): Number of columns in the dataset
  - `memory_usage_mb` (float): Memory usage in megabytes
  - `column_names` (List[str]): List of column names
  - `dtypes` (Dict[str, str]): Column data types

#### Private Methods

##### `_load_data()`

Loads CSV data with automatic chunking and memory management.

**Features:**
- **Small File Loading**: Files under threshold (default 50MB) loaded directly
- **Chunking**: Large files processed in chunks to manage memory
- **Progress Tracking**: Uses tqdm for progress bars when available
- **Memory Monitoring**: Monitors memory usage with psutil when available
- **Configuration**: Respects settings for thresholds and chunk sizes
- **Error Handling**: Error handling for file and parsing issues

**Configuration (when settings available):**
- `performance.small_file_threshold_mb`: Threshold for direct loading (default: 50MB)
- `performance.chunk_estimate_factor`: Factor for chunk count estimation (default: 1024)

**Raises:**
- `FileProcessingError`: If file not found, parsing fails, or other issues
- `MemoryError`: If memory usage exceeds configured limit

##### `_truncate_path()`

Truncates long file paths for display in output messages.

```python
# Input: "D:\Projects\devoloper\autocsv-profiler-suite\v2.0.0\output\analysis\report.html"
# Output: "D:\Projects\...\analysis\report.html"
```

**Algorithm:**
- Keeps first 2 path parts and last 2 path parts
- Inserts "..." in between for paths with more than 4 parts
- Handles errors by returning original string

## Exceptions

### ProfilerError

Base exception class for all profiler-related errors.

```python
from autocsv_profiler.base import ProfilerError

try:
    # Profiling operations
    pass
except ProfilerError as e:
    print(f"Profiler error: {e}")
```

**Inheritance:** `Exception`

### FileProcessingError

Exception raised for file processing errors (reading, parsing, validation).

```python
from autocsv_profiler.base import FileProcessingError

try:
    profiler = CustomProfiler("nonexistent.csv", ",", "output/")
except FileProcessingError as e:
    print(f"File processing error: {e}")
```

**Inheritance:** `ProfilerError`

**Common scenarios:**
- File not found
- CSV parsing errors (malformed data, encoding issues)
- Permission errors
- Unexpected file format issues

### ReportGenerationError

Exception raised for report generation errors.

```python
from autocsv_profiler.base import ReportGenerationError

class CustomProfiler(BaseProfiler):
    def generate_report(self) -> str:
        try:
            # Report generation logic
            pass
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate report: {e}")
```

**Inheritance:** `ProfilerError`

**Common scenarios:**
- Template rendering failures
- Output file writing errors
- Missing dependencies for report generation
- Visualization creation errors

## Dependencies and Optional Features

### Optional Dependencies

The base module gracefully handles optional dependencies:

```python
# Optional imports with fallback behavior
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
```

**Available Features by Dependency:**

| Dependency | Feature | Fallback Behavior |
|------------|---------|-------------------|
| `psutil` | Memory monitoring during data loading | No memory monitoring |
| `tqdm` | Progress bars for chunk loading | Silent loading |
| `settings` | Configuration-based thresholds | Hard-coded defaults |

### Configuration Integration

When the settings module is available, BaseProfiler uses configuration values:

```python
# Configuration-aware thresholds
if HAS_SETTINGS and settings:
    small_file_threshold = settings.get("performance.small_file_threshold_mb", 50) * 1024 * 1024
else:
    small_file_threshold = 50 * 1024 * 1024  # Fallback
```

## Usage Patterns

### Basic Custom Engine

```python
from autocsv_profiler.base import BaseProfiler, ReportGenerationError
import pandas as pd

class SimpleStatsProfiler(BaseProfiler):
    def generate_report(self) -> str:
        try:
            # Generate basic statistics
            stats = {
                'shape': self.df.shape,
                'dtypes': dict(self.df.dtypes),
                'missing_values': dict(self.df.isnull().sum()),
                'numeric_summary': self.df.describe().to_dict()
            }

            # Save to JSON
            import json
            report_path = self.output_dir / "simple_stats.json"
            with open(report_path, 'w') as f:
                json.dump(stats, f, indent=2, default=str)

            return str(report_path)

        except Exception as e:
            raise ReportGenerationError(f"Failed to generate simple stats: {e}")

    def get_report_name(self) -> str:
        return "Simple Statistics"

# Usage
profiler = SimpleStatsProfiler("data.csv", ",", "output/")
report_path = profiler.run()
```

### Advanced Custom Engine with Configuration

```python
from autocsv_profiler.base import BaseProfiler, settings, HAS_SETTINGS

class ConfigurableProfiler(BaseProfiler):
    def __init__(self, csv_path, delimiter, output_dir, **kwargs):
        # Use configuration if available
        if HAS_SETTINGS and settings:
            chunk_size = settings.get("performance.chunk_size", 10000)
            memory_limit = settings.get("performance.memory_limit_gb", 1.0)
        else:
            chunk_size = kwargs.get("chunk_size", 10000)
            memory_limit = kwargs.get("memory_limit_gb", 1.0)

        super().__init__(csv_path, delimiter, output_dir, chunk_size, memory_limit)

    def generate_report(self) -> str:
        # Custom report generation with configuration awareness
        summary = self.get_data_summary()

        # Use configured decimal precision if available
        if HAS_SETTINGS and settings:
            precision = settings.get("analysis.decimal_precision", 4)
        else:
            precision = 4

        # Generate report with configured precision
        report_content = f"""
        Dataset Summary:
        Rows: {summary['rows']:,}
        Columns: {summary['columns']:,}
        Memory: {summary['memory_usage_mb']:.{precision}f} MB
        """

        report_path = self.output_dir / "configurable_report.txt"
        with open(report_path, 'w') as f:
            f.write(report_content)

        return str(report_path)
```

### Error Handling Patterns

```python
from autocsv_profiler.base import BaseProfiler, FileProcessingError, ReportGenerationError

def safe_profiling(csv_path, delimiter, output_dir):
    try:
        profiler = CustomProfiler(csv_path, delimiter, output_dir)

        # Check data was loaded successfully
        summary = profiler.get_data_summary()
        if summary['rows'] == 0:
            print("Warning: No data rows found in CSV file")
            return None

        return profiler.run()

    except FileProcessingError as e:
        print(f"File processing failed: {e}")
        return None
    except ReportGenerationError as e:
        print(f"Report generation failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Memory Management

### Automatic Chunking

The BaseProfiler automatically handles large files through chunking:

```python
# For files larger than threshold (default 50MB):
# 1. File is read in chunks of configurable size (default 10,000 rows)
# 2. Progress is tracked with tqdm if available
# 3. Memory usage is monitored with psutil if available
# 4. Chunks are concatenated into final DataFrame
```

### Memory Monitoring

```python
# During chunk processing (if psutil available):
memory_usage = psutil.Process().memory_info().rss / (1024**3)
if memory_usage > self.memory_limit_gb:
    raise MemoryError(f"Memory usage exceeded {self.memory_limit_gb}GB")
```

### Configuration Options

Memory management can be configured through settings:

```yaml
# config/master_config.yml
app:
  performance:
    chunk_size: 10000                    # Rows per chunk
    memory_limit_gb: 1.0                 # Memory limit
    small_file_threshold_mb: 50          # Direct loading threshold
    chunk_estimate_factor: 1024          # Chunk count estimation
```

## Standalone Usage

The base module can be used independently without the full package:

```python
# Direct import without package context
from base import BaseProfiler, FileProcessingError

class StandaloneProfiler(BaseProfiler):
    def generate_report(self) -> str:
        # Implementation
        pass

    def get_report_name(self) -> str:
        return "Standalone Profiler"

# Works without configuration or optional dependencies
profiler = StandaloneProfiler("data.csv", ",", "output/")
```

## Integration with Engines

The BaseProfiler is used by all built-in engines:

- **Main Engine** (`engines/main/analyzer.py`): Statistical analysis engine
- **YData Engine** (`engines/profiling/ydata_report.py`): YData Profiling integration
- **SweetViz Engine** (`engines/profiling/sweetviz_report.py`): SweetViz integration
- **DataPrep Engine** (`engines/dataprep/dataprep_report.py`): DataPrep integration

Each engine inherits from BaseProfiler and implements the abstract methods while leveraging the common data loading and error handling functionality.

## See Also

- [autocsv_profiler](autocsv_profiler.md) - Main package interface
- [config](config.md) - Configuration system
- [core modules](README.md#core-modules) - Core utilities and exceptions
- [engines](engines/) - Engine implementations
- [ui](ui/) - User interface components