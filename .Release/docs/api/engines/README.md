# engines

Analysis engine implementations for different profiling libraries.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Engine Implementations](#engine-implementations)
- [Engine Selection Criteria](#engine-selection-criteria)
- [Common Patterns](#common-patterns)
- [Configuration Integration](#configuration-integration)
- [Memory Management](#memory-management)
- [Dependency Management](#dependency-management)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

The `engines` package contains isolated profiling engines that run in dedicated conda environments to handle dependency conflicts. Each engine implements the `BaseProfiler` abstract class and provides specialized data analysis capabilities.

## Architecture

### Multi-Environment Design

Each engine runs in its dedicated conda environment to resolve dependency conflicts:

```
engines/
├── main/          # Main environment (Python 3.11)
│   └── analyzer.py
├── profiling/     # Profiling environment (Python 3.10)
│   ├── ydata_report.py
│   └── sweetviz_report.py
└── dataprep/      # DataPrep environment (Python 3.10)
    └── dataprep_report.py
```

### Environment Isolation

Each engine runs in its dedicated conda environment to resolve dependency conflicts. For complete environment specifications and dependency conflict details, see [Architecture Guide](../../ARCHITECTURE.md#dependency-conflict-resolution).

## Engine Implementations

### Main Engine (`main/analyzer.py`)

Statistical analysis engine using Python libraries.

**Environment**: `csv-profiler-main` (Python 3.11)

**Features:**
- Statistical analysis with scipy 1.13.1 and numpy 2.2.6
- Visualizations with matplotlib 3.10 and seaborn 0.13.2
- TableOne analysis for medical/research data
- Statistical calculations with researchpy
- Memory management with automatic chunking
- Console interface with progress tracking

**Generated Outputs:**
- `dataset_analysis.txt` - Dataset overview
- `numerical_summary.csv` - Numerical column statistics
- `categorical_summary.csv` - Categorical column analysis
- `numerical_stats.csv` - Numerical analysis
- `categorical_stats.csv` - Categorical analysis
- `distinct_values.txt` - Unique value analysis
- `visualizations/` directory - Charts and graphs

**Usage:**
```python
from autocsv_profiler.engines.main.analyzer import main

# Function signature
main(
    file_path="data.csv",
    save_dir="output/",
    delimiter=",",
    chunk_size=10000,
    memory_limit_gb=1,
    interactive=True
)
```

**Standalone Execution:**
```bash
conda activate csv-profiler-main
python autocsv_profiler/engines/main/analyzer.py data.csv "," output_dir/
```

### YData Profiling Engine (`profiling/ydata_report.py`)

YData Profiling integration for data profiling.

**Environment**: `csv-profiler-profiling` (Python 3.10)

**Features:**
- Data quality assessment
- Missing value analysis with patterns
- Correlation matrices and analysis
- Distribution analysis for all variables
- Data type inference and validation
- Interactive HTML reports

**Generated Outputs:**
- `ydata_profiling_report.html` - Interactive HTML report

**Report Sections:**
- **Overview**: Dataset summary, variable types, warnings
- **Variables**: Detailed analysis of each column
- **Interactions**: Correlation matrices and scatter plots
- **Correlations**: Correlation analysis between variables
- **Missing values**: Missing value patterns and heatmaps
- **Sample**: First and last rows of the dataset

**Usage:**
```python
from autocsv_profiler.engines.profiling.ydata_report import generate_ydata_profiling_report

report_path = generate_ydata_profiling_report("data.csv", ",", "output/")
```

**Standalone Execution:**
```bash
conda activate csv-profiler-profiling
python autocsv_profiler/engines/profiling/ydata_report.py data.csv "," output_dir/
```

### SweetViz Engine (`profiling/sweetviz_report.py`)

SweetViz integration for data visualization and analysis.

**Environment**: `csv-profiler-profiling` (Python 3.10)

**Features:**
- Report generation for data overview
- Readable visualizations
- Target variable analysis capabilities
- Data type detection and validation
- Basic statistical summaries
- Comparative analysis between datasets

**Generated Outputs:**
- `sweetviz_report.html` - Interactive HTML report

**Report Sections:**
- **Dataset summary**: High-level overview
- **Variable analysis**: Individual column analysis with distributions
- **Associations**: Correlation and association metrics
- **Feature analysis**: Feature importance if target specified

**Usage:**
```python
from autocsv_profiler.engines.profiling.sweetviz_report import generate_sweetviz_report

report_path = generate_sweetviz_report("data.csv", ",", "output/")
```

**Standalone Execution:**
```bash
conda activate csv-profiler-profiling
python autocsv_profiler/engines/profiling/sweetviz_report.py data.csv "," output_dir/
```

### DataPrep Engine (`dataprep/dataprep_report.py`)

DataPrep integration for exploratory data analysis with pandas compatibility.

**Environment**: `csv-profiler-dataprep` (Python 3.10)

**Features:**
- Exploratory data analysis functions
- Distribution plots and statistical summaries
- Correlation analysis with multiple methods
- Missing value visualization
- Compatible with older data processing workflows
- Non-interactive matplotlib backend (Agg) for server compatibility

**Generated Outputs:**
- `dataprep_eda_report.html` - Interactive HTML report

**Report Sections:**
- **Overview**: Dataset characteristics and summary
- **Variables**: Distribution plots and detailed statistics
- **Correlations**: Multiple correlation analysis methods
- **Missing values**: Missing value analysis and patterns

**Usage:**
```python
from autocsv_profiler.engines.dataprep.dataprep_report import generate_dataprep_report

report_path = generate_dataprep_report("data.csv", ",", "output/")
```

**Standalone Execution:**
```bash
conda activate csv-profiler-dataprep
python autocsv_profiler/engines/dataprep/dataprep_report.py data.csv "," output_dir/
```

## Engine Selection Criteria

### Performance Characteristics

| Engine | Speed | Detail Level | Memory Usage | Best For |
|--------|-------|--------------|-------------|----------|
| **SweetViz** | Fast | Low-Medium | Low | Data overviews, presentations |
| **Main** | Fast | High | Medium | Statistical analysis, research |
| **DataPrep** | Medium | Medium | Medium | EDA, compatibility |
| **YData** | Slow | High | High | Data profiling |

### Use Case Recommendations

**Data Overview:**
- Use SweetViz for fast results
- Initial data exploration
- Presentation visualizations

**Data Analysis:**
- Use YData Profiling for detailed reports
- Data quality assessment
- Correlation and missing value analysis

**Statistical Research:**
- Use Main Engine for statistics
- Research analysis with Python libraries
- Visualizations and TableOne analysis

**System Integration:**
- Use DataPrep Engine for pandas compatibility
- Features and compatibility balance
- Server deployment with non-interactive backend

## Common Patterns

### Engine Loading

All engines support lazy loading through the main package:

```python
from autocsv_profiler import (
    _load_main_engine,
    _load_ydata_engine,
    _load_sweetviz_engine,
    _load_dataprep_engine
)

# Load specific engines
main_engine, run_analysis, analyze_csv = _load_main_engine()
ydata_engine = _load_ydata_engine()
sweetviz_engine = _load_sweetviz_engine()
dataprep_engine = _load_dataprep_engine()
```

### Error Handling

All engines implement consistent error handling:

```python
try:
    report_path = generate_ydata_profiling_report("data.csv", ",", "output/")
    if report_path:
        print(f"Report generated: {report_path}")
    else:
        print("Report generation failed")
except ImportError:
    print("YData Profiling not available in this environment")
except Exception as e:
    print(f"Error: {e}")
```

### Standalone Execution

All engines can run independently without the full package:

```bash
# Direct engine execution
conda activate csv-profiler-main
python -m autocsv_profiler.engines.main.analyzer data.csv "," output/

# Script-style execution
conda activate csv-profiler-profiling
python autocsv_profiler/engines/profiling/ydata_report.py data.csv "," output/
```

## Configuration Integration

### Environment-Specific Settings

Engines respect configuration when available:

```python
# In engines with settings access
if HAS_SETTINGS and settings:
    chunk_size = settings.get("performance.chunk_size", 10000)
    memory_limit = settings.get("performance.memory_limit_gb", 1.0)
else:
    # Fallback defaults
    chunk_size = 10000
    memory_limit = 1.0
```

### Debug Mode Support

All engines support debug mode through environment variables:

```bash
# Enable debug mode
export DEBUG=1
python autocsv_profiler/engines/main/analyzer.py data.csv "," output/

# Debug output example
[DEBUG Main] Main analyzer started
[DEBUG Main] File path: data.csv
[DEBUG Main] Memory limit: 1GB, Chunk size: 10000
```

## Memory Management

### Automatic Chunking

All engines implement memory-aware data loading:

1. **Small files** (< 50MB): Loaded directly into memory
2. **Large files** (>= 50MB): Processed in chunks with progress tracking
3. **Memory monitoring**: Uses psutil when available to track usage
4. **Configurable limits**: Memory limits and chunk sizes are configurable

### Progress Tracking

Engines provide progress feedback:

```python
# Example progress output
Loading data: 100%|████████████| 45/45 [00:02<00:00, 20.1chunk/s]
Generating visualizations: 100%|████████████| 12/12 [00:15<00:00, 1.3viz/s]
```

## Dependency Management

### Graceful Degradation

Each engine handles missing dependencies gracefully:

```python
# YData engine example
try:
    from ydata_profiling import ProfileReport
except ImportError:
    ProfileReport = None

def generate_ydata_profiling_report(csv_path, delimiter, output_dir):
    if ProfileReport is None:
        raise ImportError("YData Profiling not available in this environment")
    # Continue with report generation
```

### Environment Verification

Check engine availability before use:

```python
from autocsv_profiler import _load_ydata_engine

ydata_engine = _load_ydata_engine()
if ydata_engine is None:
    print("YData Profiling engine not available")
    # Fallback to another engine
else:
    report = ydata_engine("data.csv", ",", "output/")
```

## Troubleshooting

### Common Issues

**Import Errors:**
- Verify conda environment is activated
- Check environment-specific package installation
- Use environment verification commands

**Memory Errors:**
- Reduce chunk size in configuration
- Increase memory limit if system allows
- Use smaller data subsets for testing

**Report Generation Failures:**
- Check output directory permissions
- Verify CSV file format and encoding
- Review delimiter detection results

### Environment Debugging

```bash
# Check environment status
conda env list | grep csv-profiler

# Verify packages in environment
conda activate csv-profiler-main
conda list pandas numpy scipy

# Test engine directly
python -c "from autocsv_profiler.engines.main.analyzer import main; print('Main engine OK')"
```

## See Also

- [autocsv_profiler](../autocsv_profiler.md) - Main package interface
- [base](../base.md) - BaseProfiler abstract class
- [config](../config.md) - Configuration system
- [core modules](../README.md#core-modules) - Core utilities and exceptions