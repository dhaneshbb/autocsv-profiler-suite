# API Documentation

API reference for the AutoCSV Profiler Suite Python interface.

## Table of Contents

- [Core API Modules](#core-api-modules)
- [Core Modules](#core-modules)
- [Statistical Analysis Modules](#statistical-analysis-modules)
- [Utility Modules](#utility-modules)
- [Usage Examples](#usage-examples)
- [Engine Testing and Development](#engine-testing-and-development)
- [Related Documentation](#related-documentation)

## Core API Modules

### Main Package Interface
- **[autocsv_profiler](autocsv_profiler.md)** - Main package interface with lazy loading and API
- **[base](base.md)** - BaseProfiler abstract class for engine development
- **[config](config.md)** - Configuration system and settings management

### Engine Documentation
- **[engines](engines/)** - Analysis engine implementations and testing
- **[ui](ui/)** - Interface components and interactive features

## Core Modules

### autocsv_profiler.core

Core utilities and components for the profiling system.

#### autocsv_profiler.core.exceptions

Exception hierarchy for structured error handling.

**Classes:**
- `AutoCSVProfilerError` - Base exception for all profiler errors
- `FileProcessingError` - File-related processing errors
- `DelimiterDetectionError` - Delimiter detection failures
- `ReportGenerationError` - Report generation failures

#### autocsv_profiler.core.dataset_info

Dataset analysis and information functions.

**Functions:**
- `get_dataset_info(df)` - Extract DataFrame information
- `format_dataset_info(info)` - Format dataset info into readable text
- `generate_complete_report(df, output_dir)` - Generate analysis report
- `data_table_range_min_max_distinct(df, output_dir)` - Range and distinct value analysis
- `missing_inf_values(df, output_dir)` - Missing and infinite value analysis
- `distinct_val_tabular_txt(df, output_dir)` - Tabular distinct value analysis

#### autocsv_profiler.core.validation

Data validation utilities for CSV files and DataFrames.

#### autocsv_profiler.core.utils

Utility functions used across the profiling system.

**Key Functions:**
- `cat_high_cardinality` - Handle high cardinality categorical data

#### autocsv_profiler.core.logger

Logging configuration and utilities.

**Features:**
- Structured logging with console support
- Debug mode configuration
- Performance metrics logging
- Engine-specific log formatting

#### autocsv_profiler.core.warnings

Warning management for suppressing library output.

### Statistical Analysis Modules

#### autocsv_profiler.stats

Statistical analysis functions using ResearchPy and statistical methods.

**Functions:**
- `analyze_data(data)` - Numerical and categorical analysis
- `researchpy_descriptive_stats(data, save_dir)` - Descriptive statistics
- `TableOne_groupby_column(data, save_dir)` - Medical/research TableOne analysis
- `calculate_statistics(data)` - Core statistical calculations
- `iqr_trimmed_mean(data)` - IQR-based trimmed mean calculation
- `mad(data)` - Median Absolute Deviation calculation
- `num_var_analysis()` - Numerical variable analysis

#### autocsv_profiler.plots

Visualization and plotting functions for statistical analysis.

**Features:**
- Parallel visualization generation
- Statistical plots (histograms, box plots, correlations)
- Distribution analysis with normal testing
- Categorical data visualization
- Memory management for large datasets

**Key Functions:**
- `execute_visualization_worker(args)` - Parallel visualization worker
- Statistical distribution plots
- Correlation matrices and heatmaps
- Categorical frequency plots
- Q-Q plots and probability analysis

#### autocsv_profiler.summarize

Data summarization and aggregation functions.

**Features:**
- DataFrame summary generation
- Statistical aggregation methods
- Memory management summarization

### Utility Modules

#### autocsv_profiler.types

Type definitions and type aliases for the package.

**Type Aliases:**
- `PathLike` - Path-like objects (str, Path)
- Statistical type definitions
- Configuration type hints

#### autocsv_profiler.version

Version management and compatibility checking.

**Attributes:**
- `__version__` - Current version string
- `__version_info__` - Version tuple
- Package metadata constants

**Functions:**
- `get_version_info()` - Detailed version information
- `get_full_version_info()` - Complete version and dependency info
- `check_python_version()` - Validate Python version compatibility

## Usage Examples

### Basic API Usage

```python
from autocsv_profiler import profile_csv

# Basic analysis with engine selection
report_path = profile_csv("data.csv", "output_directory/")

# Engine-specific analysis
ydata_report = profile_csv("data.csv", "output/", engine="ydata")
sweetviz_report = profile_csv("data.csv", "output/", engine="sweetviz")
dataprep_report = profile_csv("data.csv", "output/", engine="dataprep")
```

### Advanced Statistical Analysis

```python
from autocsv_profiler.stats import analyze_data, calculate_statistics
from autocsv_profiler.core.dataset_info import get_dataset_info
import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Get basic dataset information
info = get_dataset_info(df)
print(f"Dataset: {info['num_rows']} rows, {info['num_columns']} columns")

# Statistical analysis
analyze_data(df)

# Calculate statistics for specific series
for col in df.select_dtypes(include=['number']).columns:
    stats = calculate_statistics(df[col])
    print(f"{col}: mean={stats['mean']:.2f}, std={stats['std']:.2f}")
```

### Custom Visualization

```python
from autocsv_profiler.plots import execute_visualization_worker
import pandas as pd
import tempfile
import pickle

# Prepare data
df = pd.read_csv("data.csv")
with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp:
    pickle.dump(df, tmp)
    temp_data_path = tmp.name

# Configure visualization
viz_config = {
    "type": "histogram",
    "column": "age",
    "bins": 30,
    "title": "Age Distribution"
}

# Generate visualization
args = (viz_config, temp_data_path, "output/viz/", "age")
success, viz_name, error = execute_visualization_worker(args)

if success:
    print(f"Generated: {viz_name}")
else:
    print(f"Failed: {error}")
```

### Error Handling

```python
from autocsv_profiler import profile_csv
from autocsv_profiler.core.exceptions import (
    AutoCSVProfilerError,
    FileProcessingError,
    ReportGenerationError
)

try:
    result = profile_csv("data.csv", "output/")
except FileProcessingError as e:
    print(f"File processing failed: {e}")
except ReportGenerationError as e:
    print(f"Report generation failed: {e}")
except AutoCSVProfilerError as e:
    print(f"General profiler error: {e}")
```

### Configuration Management

```python
from autocsv_profiler.config import settings

# Access configuration values
chunk_size = settings.get("performance.chunk_size", 10000)
memory_limit = settings.get("performance.memory_limit_gb", 1)
delimiter_detection = settings.get("delimiter_detection.enabled", True)

# Check feature availability
if delimiter_detection:
    print("Automatic delimiter detection enabled")
```

## Engine Testing and Development

For comprehensive engine testing documentation, see [Engine Testing Guide](engines/ENGINE_TESTING.md).

## Related Documentation

- [User Guide](../USER_GUIDE.md) - Complete usage instructions
- [Architecture Guide](../ARCHITECTURE.md) - Technical architecture details
- [Development Guide](../DEVELOPMENT.md) - Development workflow and standards
- [Installation Guide](../INSTALLATION.md) - Environment setup and installation
- [Troubleshooting Guide](../TROUBLESHOOTING.md) - Common issues and solutions