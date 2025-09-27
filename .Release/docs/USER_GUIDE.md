# User Guide

Reference guide for AutoCSV Profiler Suite usage, configuration, and troubleshooting.

## Table of Contents

- [Getting Started](#getting-started)
- [Usage Modes](#usage-modes)
- [Engine Selection Guide](#engine-selection-guide)
- [File Format Requirements](#file-format-requirements)
- [Output Interpretation](#output-interpretation)
- [Advanced Configuration Options](#advanced-configuration-options)
- [Performance Tuning](#performance-tuning)

## Getting Started

Initial setup: Complete the [Getting Started Tutorial](tutorials/getting_started.md) for step-by-step instructions.

Overview: AutoCSV Profiler Suite analyzes CSV files using specialized engines in isolated conda environments.

## Usage Modes

### Interactive Mode

Guided workflow with file validation and engine selection.

```bash
python bin/run_analysis.py
```

Features:
- Delimiter detection with manual override
- File validation and preprocessing
- Engine availability checking
- Progress tracking and error handling

### Command-Line Mode

Direct file analysis for automation and scripting.

```bash
# Direct file analysis
python bin/run_analysis.py /path/to/data.csv

# Debug mode with interactive interface
python bin/run_analysis.py --debug

# Direct analysis with debug mode
python bin/run_analysis.py /path/to/data.csv --debug

# Help
python bin/run_analysis.py --help
```

### Individual Engine Execution

See [Engine Testing Guide](api/engines/ENGINE_TESTING.md) for complete engine testing instructions.

### Programmatic Usage

Command-line interface usage (handles multi-environment setup automatically):

```bash
# Interactive mode with guided workflow
python bin/run_analysis.py

# Direct file analysis
python bin/run_analysis.py data.csv
```

Python API usage (limitations may exist in multi-environment setup):

```python
# Note: May raise ImportError due to isolated environments
try:
    from autocsv_profiler import profile_csv
    report_path = profile_csv("data.csv", "output_directory/")
except ImportError:
    print("CLI usage: python bin/run_analysis.py data.csv")
```

For API documentation, see [API Documentation](api/).

## Engine Selection Guide

Choose the engine based on analysis needs.

### Available Engines

| Engine | Environment | Speed | Best For |
|--------|-------------|-------|----------|
| Main | Python 3.11 | Balanced | Statistical analysis, research |
| YData | Python 3.10 | Slow | Data profiling, data quality |
| SweetViz | Python 3.10 | Fast | Data overviews, presentations |
| DataPrep | Python 3.10 | Medium | EDA, legacy compatibility |

### Quick Selection Guide

- Comprehensive analysis: Use YData for detailed data profiling and quality assessment
- Fast overview: Use SweetViz for quick data exploration and presentations
- Statistical research: Use Main engine for advanced statistics and custom analysis
- Legacy compatibility: Use DataPrep for older pandas workflows

For detailed engine specifications, features, and usage examples, see [Engines Documentation](api/engines/).

## File Format Requirements

### Supported Formats

CSV files with extensions: `.csv`, `.txt`
- Encoding: UTF-8, UTF-8-BOM, Latin1, ISO-8859-1, CP1252, ASCII
- File size: Up to 500MB (configurable in master config)
- Delimiters: Comma, semicolon, tab, pipe, colon, space also non-normal characters etc...(auto-detected)

### Data Quality Requirements

Minimum: 2+ rows, consistent columns, valid encoding
Recommended: Header row, consistent data types, escaped quotes
Handled: Mixed line endings, BOM markers, trailing empty rows/columns

### File Size Processing

- Small (< 50MB): Direct loading, fastest processing
- Medium (50-500MB): Automatic chunking (10K rows), progress tracking
- Large (> 500MB): Configuration adjustment required

## Output Interpretation

Understanding the generated analysis files and reports.

### Directory Structure

Each analysis creates a directory with outputs:
```
test_output/
├── bank-additional.csv          # Source data file
├── dataset_analysis.txt         # Main engine overview
├── numerical_summary.csv        # Main engine numerical stats
├── categorical_summary.csv      # Main engine categorical stats
├── numerical_stats.csv          # Advanced numerical analysis
├── categorical_stats.csv        # Advanced categorical analysis
├── distinct_values.txt          # Unique value analysis
├── excluded_columns.csv         # Excluded column analysis
├── modified_dataset.csv         # Processed dataset
├── tableone_groupby_y.csv       # Grouped analysis results
├── ydata_profiling_report.html  # YData interactive report
├── sweetviz_report.html         # SweetViz interactive report
├── dataprep_eda_report.html     # DataPrep interactive report
├── bar_charts/                  # Bar chart visualizations
├── box_plots/                   # Box plot visualizations
├── kde_plots/                   # KDE plot visualizations
├── pie_charts/                  # Pie chart visualizations
└── qq_plots/                    # Q-Q plot visualizations
```

### Main Engine Files

- dataset_analysis.txt: Dataset overview with shape, memory usage, encoding
- numerical_summary.csv: Statistical summaries (mean, std, quartiles)
- categorical_summary.csv: Category counts, unique values, frequency analysis
- numerical_stats.csv: Advanced statistical metrics
- categorical_stats.csv: Detailed categorical analysis
- distinct_values.txt: Unique value analysis

### Interactive HTML Reports

- YData Profiling: Overview, variables, correlations, missing values, sample data
- SweetViz: Dataset summary, variable analysis, associations
- DataPrep: Overview, distributions, correlations, missing value patterns

### Visualization Files

Generated charts in `visualizations/` directory:
- Correlation matrices and heatmaps
- Distribution plots and histograms
- Missing value patterns

## Configuration Options

Customize the analysis behavior through configuration files and parameters.

### Master Configuration File

Edit `config/master_config.yml` to modify global settings:

Performance settings:
```yaml
app:
  performance:
    chunk_size: 10000              # Rows per chunk
    memory_limit_gb: 1             # Memory limit
    max_file_size_mb: 500          # Maximum file size
    small_file_threshold_mb: 50    # Small file threshold
```

Delimiter detection:
```yaml
  delimiter_detection:
    enabled: true                  # Enable auto-detection
    confidence_threshold: 0.7      # Minimum confidence
    sample_lines: 20              # Lines to sample
    common_delimiters: [",", ";", "\t", "|"]
```

Analysis settings:
```yaml
  analysis:
    high_cardinality_threshold: 20 # High cardinality threshold
    decimal_precision: 4           # Decimal precision
    quantiles: [0.25, 0.50, 0.75] # Quantiles to calculate
```

### Environment Customization

Add custom packages to environments:

1. Edit `config/master_config.yml`
2. Add packages to the appropriate environment:
```yaml
environments:
  main:
    conda_packages:
      - "python=3.11.7"
      - "pandas=2.3.1"
      - "your-custom-package=1.0.0"
```

3. Regenerate environments:

For complete environment management commands, see [Installation Guide](INSTALLATION.md#environment-management).

Basic commands:
```bash
# Regenerate configurations and recreate environments
python bin/setup_environments.py generate
python bin/setup_environments.py recreate --parallel
```

### Runtime Configuration

Environment variables:
```bash
# Enable debug mode
export DEBUG=1

# Set memory limit
export MEMORY_LIMIT_GB=2

# Set chunk size
export CHUNK_SIZE=20000
```

Command-line options:
```bash
# Debug mode
python bin/run_analysis.py --debug

# Individual engine parameters (when running directly)
python autocsv_profiler/engines/main/analyzer.py data.csv "," output/ --memory-limit 2 --chunk-size 20000
```

## Performance Tuning

### Memory Optimization

Configuration adjustments in `config/master_config.yml`:
- Large files: Smaller chunks (5000 rows), more memory (2GB)
- Small files: Larger chunks (50000 rows), higher threshold
- Memory-constrained: Smaller chunks (5000), lower limits (0.5GB)

### Engine Performance Characteristics

| Engine | Speed | Detail Level | Best For |
|--------|-------|--------------|----------|
| Main | Balanced | High | Routine analysis, large files |
| YData | Slow | Highest | Detailed exploration, quality assessment |
| SweetViz | Fast | Medium | Quick overviews, presentations |
| DataPrep | Moderate | Medium | EDA, distribution analysis |

### Optimization Strategies

- Select appropriate engines for use case
- Adjust chunk size and memory limits for file size
- Enable performance monitoring for bottleneck identification
- Use SSD storage for improved I/O performance

---

## See Also

- [Installation Guide](INSTALLATION.md) - Complete setup instructions
- [Getting Started Tutorial](tutorials/getting_started.md) - Step-by-step walkthrough
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions
- [API Documentation](api/) - Complete API reference
