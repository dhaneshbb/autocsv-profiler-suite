# AutoCSV Profiler

A comprehensive toolkit for automated CSV data analysis providing statistical insights, data quality assessment, and interactive visualizations.

[![PyPI version](https://badge.fury.io/py/autocsv-profiler.svg)](https://badge.fury.io/py/autocsv-profiler)
[![Python Support](https://img.shields.io/pypi/pyversions/autocsv-profiler.svg)](https://pypi.org/project/autocsv-profiler/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Comprehensive Statistical Analysis**: Descriptive statistics, distributions, and data summaries
- **Data Quality Assessment**: Missing value analysis, outlier detection, and duplicate identification
- **Advanced Visualizations**: Box plots, histograms, correlation matrices, and KDE plots
- **Interactive Reports**: HTML reports with detailed insights and recommendations
- **Command-Line Interface**: Easy-to-use CLI for immediate analysis
- **Python API**: Programmatic access for integration into data pipelines

## Installation

```bash
pip install autocsv-profiler
```

## Quick Start

### Command Line Usage

```bash
# Basic analysis
autocsv-profiler data.csv

# Specify output directory
autocsv-profiler data.csv --output ./my_analysis

# Custom delimiter
autocsv-profiler data.csv --delimiter ";"
```

### Python API Usage

```python
from autocsv_profiler import auto_csv_profiler

# Run comprehensive analysis
auto_csv_profiler.main("data.csv", "output_directory")

# Or import specific functions
from autocsv_profiler.recognize_delimiter import detect_delimiter

delimiter = detect_delimiter("data.csv")
print(f"Detected delimiter: {delimiter}")
```

## Generated Outputs

### Statistical Reports
- **Dataset Overview**: Shape, data types, memory usage
- **Descriptive Statistics**: Mean, median, mode, standard deviation
- **Distribution Analysis**: Skewness, kurtosis, normality tests
- **Categorical Analysis**: Frequency tables and unique value counts

### Data Quality Assessment
- **Missing Values**: Patterns, counts, and visualizations
- **Outliers**: IQR-based detection with statistical summaries
- **Duplicates**: Identification and detailed reporting
- **Data Consistency**: Type validation and integrity checks

### Visualizations
- **Distribution Plots**: Histograms with KDE overlays
- **Box Plots**: Outlier visualization and quartile analysis
- **Correlation Analysis**: Heatmaps and relationship matrices
- **Missing Data Patterns**: Matrix plots and summary charts

### Interactive Reports
- **HTML Dashboard**: Comprehensive overview with navigation
- **Data Dictionary**: Detailed variable descriptions
- **Quality Summary**: Actionable insights and recommendations

## Output Structure

```
your_file_analysis/
├── your_file.csv                     # Copy of original data
├── dataset_info.txt                  # Basic dataset information
├── summary_statistics_all.txt        # Comprehensive statistics
├── categorical_summary.txt           # Categorical variable analysis
├── missing_values_report.txt         # Missing data analysis
├── outliers_summary.txt              # Outlier detection results
├── distinct_values_count_by_dtype.html # Interactive value explorer
└── visualization/                    # Generated plots and charts
    ├── box_plots/
    ├── histograms/
    └── correlation_matrices/
```

## Advanced Features

### Missing Value Analysis
- Automatic detection of missing value patterns
- Visualization of missing data distribution
- Imputation suggestions and options
- Missing value correlation analysis

### Outlier Detection
- IQR-based outlier identification
- Statistical summaries for outliers
- Visual outlier highlighting in plots
- Outlier impact assessment

### Statistical Testing
- Normality tests (Shapiro-Wilk)
- Correlation analysis (Pearson, Spearman)
- Chi-square tests for categorical variables
- Variance inflation factor (VIF) analysis

### Relationship Analysis
- Variable correlation matrices
- Target variable analysis (if specified)
- Feature importance insights
- Interaction effect detection

## Examples

### Basic CSV Analysis
```python
import autocsv_profiler

# Analyze sales data
autocsv_profiler.main("sales_data.csv", "sales_analysis")
```

### Custom Analysis Pipeline
```python
from autocsv_profiler import auto_csv_profiler
from autocsv_profiler.recognize_delimiter import detect_delimiter
import pandas as pd

# Load and analyze data
delimiter = detect_delimiter("customer_data.csv")
df = pd.read_csv("customer_data.csv", delimiter=delimiter)

# Run comprehensive analysis
auto_csv_profiler.main("customer_data.csv", "customer_analysis")
```

### Batch Processing
```python
import os
from autocsv_profiler import auto_csv_profiler

# Analyze all CSV files in a directory
for filename in os.listdir("data/"):
    if filename.endswith(".csv"):
        input_file = f"data/{filename}"
        output_dir = f"analysis/{filename[:-4]}_results"
        auto_csv_profiler.main(input_file, output_dir)
```

## Requirements

- Python 3.9 or higher
- pandas >= 1.5.0
- numpy >= 1.24.0
- matplotlib >= 3.6.0
- seaborn >= 0.12.0
- scipy >= 1.10.0
- scikit-learn >= 1.2.0
- statsmodels >= 0.13.0

All dependencies are automatically installed with pip.

## Performance Tips

- **Large Files**: For files > 100MB, consider sampling first
- **Memory Usage**: Monitor memory for datasets with many categorical variables
- **Output Management**: Clean old analysis directories to save disk space
- **Parallel Processing**: Use batch scripts for multiple files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/dhaneshbb/AutoCSV-Profiler-Suite/issues)
- **Documentation**: [GitHub Docs](https://github.com/dhaneshbb/AutoCSV-Profiler-Suite/tree/main/docs)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## Version

Current version: 1.1.0


See [CHANGELOG.md](CHANGELOG.md) for version history and updates.
