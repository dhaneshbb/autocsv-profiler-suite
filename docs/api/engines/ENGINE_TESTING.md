# Engine Testing Guide

Guide for testing individual profiling engines in their conda environments.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Engine Testing Commands](#engine-testing-commands)
- [Environment Verification](#environment-verification)
- [Sample Test Data](#sample-test-data)
- [Common Testing Scenarios](#common-testing-scenarios)
- [Troubleshooting Engine Issues](#troubleshooting-engine-issues)
- [Automation Scripts](#automation-scripts)
- [Performance Benchmarks](#performance-benchmarks)
- [Integration Testing](#integration-testing)
- [Related Documentation](#related-documentation)

## Overview

AutoCSV Profiler Suite uses isolated conda environments for each engine. Instructions for testing engines individually for:

- Development and debugging
- Environment validation
- Performance testing
- Troubleshooting engine-specific issues

## Prerequisites

- Conda environments must be created:
  - **Quick Setup**: `python bin/setup_environments.py create --parallel`
  - **Complete Instructions**: See [Installation Guide](../../INSTALLATION.md)
- Verify environments exist: `conda env list | grep csv-profiler`

## Engine Testing Commands

### Main Engine (Statistical Analysis)

**Environment**: `csv-profiler-main` (Python 3.11)

```bash
# Activate environment and test
conda activate csv-profiler-main
python autocsv_profiler/engines/main/analyzer.py test.csv "," output/

# With debug output
DEBUG=1 python autocsv_profiler/engines/main/analyzer.py test.csv "," output/

# Test with different delimiter
python autocsv_profiler/engines/main/analyzer.py data.csv ";" output/
```

### YData Profiling Engine

**Environment**: `csv-profiler-profiling` (Python 3.10)

```bash
# Activate environment and test
conda activate csv-profiler-profiling
python autocsv_profiler/engines/profiling/ydata_report.py test.csv "," output/

# Debug mode (shows warning details)
DEBUG=1 python autocsv_profiler/engines/profiling/ydata_report.py test.csv "," output/

# Test with custom output directory
python autocsv_profiler/engines/profiling/ydata_report.py data.csv "," /path/to/custom/output/
```

### SweetViz Engine

**Environment**: `csv-profiler-profiling` (Python 3.10)

```bash
# Activate environment and test
conda activate csv-profiler-profiling
python autocsv_profiler/engines/profiling/sweetviz_report.py test.csv "," output/

# Debug mode
DEBUG=1 python autocsv_profiler/engines/profiling/sweetviz_report.py test.csv "," output/
```

### DataPrep Engine

**Environment**: `csv-profiler-dataprep` (Python 3.10)

```bash
# Activate environment and test
conda activate csv-profiler-dataprep
python autocsv_profiler/engines/dataprep/dataprep_report.py test.csv "," output/

# Debug mode (verbose output)
DEBUG=1 python autocsv_profiler/engines/dataprep/dataprep_report.py test.csv "," output/

# Test with different backend
MPLBACKEND=Agg python autocsv_profiler/engines/dataprep/dataprep_report.py test.csv "," output/
```

## Environment Verification

### Check Environment Status

```bash
# List all csv-profiler environments
conda env list | grep csv-profiler

# Check specific environment packages
conda list -n csv-profiler-main pandas numpy scipy
conda list -n csv-profiler-profiling ydata-profiling sweetviz
conda list -n csv-profiler-dataprep dataprep pandas
```

### Test Environment Package Imports

```bash
# Test main environment
conda activate csv-profiler-main
python -c "import pandas, numpy, scipy, matplotlib; print('Main env OK')"

# Test profiling environment
conda activate csv-profiler-profiling
python -c "import ydata_profiling, sweetviz; print('Profiling env OK')"

# Test dataprep environment
conda activate csv-profiler-dataprep
python -c "import dataprep; print('DataPrep env OK')"
```

## Sample Test Data

### Create Test CSV

```python
# Create test data for engine testing
import pandas as pd
import numpy as np

# Small test file
data = {
    'id': range(1, 101),
    'name': [f'User_{i}' for i in range(1, 101)],
    'age': np.random.randint(18, 80, 100),
    'score': np.random.uniform(0, 100, 100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
}
df = pd.DataFrame(data)
df.to_csv('test_data.csv', index=False)
```

### Different Delimiter Test Files

```bash
# Create comma-separated file
echo -e "id,name,value\n1,Alice,100\n2,Bob,200" > test_comma.csv

# Create semicolon-separated file
echo -e "id;name;value\n1;Alice;100\n2;Bob;200" > test_semicolon.csv

# Create tab-separated file
echo -e "id\tname\tvalue\n1\tAlice\t100\n2\tBob\t200" > test_tab.csv
```

## Common Testing Scenarios

### Memory Testing

```bash
# Test with large file (adjust path as needed)
python autocsv_profiler/engines/main/analyzer.py large_dataset.csv "," output/

# Monitor memory usage during processing
conda activate csv-profiler-main
python -c "
import psutil
import time
while True:
    memory = psutil.Process().memory_info().rss / 1024**2
    print(f'Memory usage: {memory:.1f} MB')
    time.sleep(1)
" &
python autocsv_profiler/engines/main/analyzer.py large_file.csv "," output/
```

### Performance Benchmarking

```bash
# Time engine execution
time conda activate csv-profiler-main && python autocsv_profiler/engines/main/analyzer.py test.csv "," output/

# Multiple runs for average
for i in {1..3}; do
    echo "Run $i:"
    time python autocsv_profiler/engines/profiling/ydata_report.py test.csv "," output/
done
```

### Error Testing

```bash
# Test with invalid file
python autocsv_profiler/engines/main/analyzer.py nonexistent.csv "," output/

# Test with invalid delimiter
python autocsv_profiler/engines/main/analyzer.py test.csv "invalid" output/

# Test with unreadable directory
python autocsv_profiler/engines/main/analyzer.py test.csv "," /invalid/path/
```

## Troubleshooting Engine Issues

For general troubleshooting and common issues, see the [Troubleshooting Guide](../../TROUBLESHOOTING.md).

### Engine-Specific Issues

### Common Problems

**Environment not found:**
```bash
# Recreate specific environment
python bin/setup_environments.py recreate csv-profiler-main
```

**Import errors:**
```bash
# Verify package installation
conda activate csv-profiler-main
conda list pandas
```

**Permission errors:**
```bash
# Check output directory permissions
ls -la output/
mkdir -p output && chmod 755 output
```

**Memory errors:**
```bash
# Test with smaller file or increased memory limit
# Adjust chunk_size in config/master_config.yml
```

### Debug Mode Options

```bash
# Enable debug for specific engine
DEBUG=1 python autocsv_profiler/engines/main/analyzer.py test.csv "," output/

# Verbose conda output
conda activate csv-profiler-main --verbose

# Python verbose imports
python -v -c "import pandas"
```

## Automation Scripts

### Batch Testing Script

```bash
#!/bin/bash
# test_all_engines.sh

echo "Testing engines with test data..."

# Create test data
echo "id,name,value" > test.csv
echo "1,Alice,100" >> test.csv
echo "2,Bob,200" >> test.csv

# Test main engine
echo "Testing main engine..."
conda activate csv-profiler-main
python autocsv_profiler/engines/main/analyzer.py test.csv "," output_main/

# Test profiling engines
echo "Testing YData engine..."
conda activate csv-profiler-profiling
python autocsv_profiler/engines/profiling/ydata_report.py test.csv "," output_ydata/

echo "Testing SweetViz engine..."
python autocsv_profiler/engines/profiling/sweetviz_report.py test.csv "," output_sweetviz/

# Test DataPrep engine
echo "Testing DataPrep engine..."
conda activate csv-profiler-dataprep
python autocsv_profiler/engines/dataprep/dataprep_report.py test.csv "," output_dataprep/

echo "Engine tests completed!"
```

### Environment Health Check

```bash
#!/bin/bash
# check_environments.sh

echo "Checking conda environments..."

for env in csv-profiler-main csv-profiler-profiling csv-profiler-dataprep; do
    echo "Checking $env..."
    if conda env list | grep -q $env; then
        echo "  ✓ Environment exists"
        conda activate $env
        python -c "import sys; print(f'  ✓ Python {sys.version_info.major}.{sys.version_info.minor}')"
    else
        echo "  ✗ Environment missing"
    fi
done
```

## Performance Benchmarks

### Performance Benchmarks

| Engine | Small File (<1MB) | Medium File (10MB) | Large File (100MB) |
|--------|------------------|-------------------|-------------------|
| Main | 2-5 seconds | 10-30 seconds | 1-5 minutes |
| YData | 5-15 seconds | 30-90 seconds | 5-15 minutes |
| SweetViz | 3-8 seconds | 15-45 seconds | 2-8 minutes |
| DataPrep | 10-25 seconds | 45-120 seconds | 8-20 minutes |

### Memory Usage

| Engine | Standard Usage | Peak Usage |
|--------|--------------|------------|
| Main | 100-300 MB | 500 MB |
| YData | 200-500 MB | 1 GB |
| SweetViz | 150-400 MB | 700 MB |
| DataPrep | 300-600 MB | 1.2 GB |

## Integration Testing

### Full Workflow Test

```bash
# Test analysis pipeline
python bin/run_analysis.py test.csv

# Test with specific engines
python -c "
from autocsv_profiler import profile_csv
result = profile_csv('test.csv', 'output/', 'ydata')
print(f'Report generated: {result}')
"
```

### Continuous Integration

```bash
# CI testing (non-interactive)
python bin/run_analysis.py --batch test.csv output/

# Test engines in sequence
for engine in main ydata sweetviz dataprep; do
    echo "Testing $engine engine..."
    python -c "
from autocsv_profiler import profile_csv
try:
    result = profile_csv('test.csv', 'output_$engine/', '$engine')
    print(f'✓ $engine: {result}')
except Exception as e:
    print(f'✗ $engine: {e}')
"
done
```

## Related Documentation

- [Architecture Guide](../../ARCHITECTURE.md) - Understanding the multi-environment design
- [Troubleshooting Guide](../../TROUBLESHOOTING.md) - Common issues and solutions
- [Development Guide](../../DEVELOPMENT.md) - Development workflow and standards
- [Performance Guide](../../PERFORMANCE.md) - Performance optimization and tuning