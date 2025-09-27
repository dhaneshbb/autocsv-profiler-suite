# Performance Guide

Performance documentation for the AutoCSV Profiler Suite, including benchmarks, optimization techniques, and resource management strategies.

## Table of Contents

- [Performance Overview](#performance-overview)
- [Memory Management](#memory-management)
- [Processing Benchmarks](#processing-benchmarks)
- [Engine Performance Characteristics](#engine-performance-characteristics)
- [Large File Handling](#large-file-handling)
- [Optimization Techniques](#optimization-techniques)
- [System Requirements](#system-requirements)
- [Configuration Tuning](#configuration-tuning)
- [Troubleshooting Performance Issues](#troubleshooting-performance-issues)

## Performance Overview

The AutoCSV Profiler Suite is designed for CSV analysis across different system configurations. Key performance features:

- **Memory Management**: Configurable memory limits with automatic chunking (default: 1GB limit)
- **Multi-Environment Architecture**: Isolated conda environments prevent dependency conflicts
- **Chunked Processing**: Automatic data chunking for large files (default: 10,000 rows per chunk)
- **Resource Monitoring**: Memory usage tracking with psutil integration
- **Engine Optimization**: Each engine optimized for different use cases

### Default Performance Settings

**For complete configuration examples, see [User Guide - Configuration](USER_GUIDE.md#advanced-configuration-options).**

Key performance settings:
- **chunk_size**: 10000 rows per chunk (adjustable for memory constraints)
- **memory_limit_gb**: 1GB default limit (increase for large files)
- **max_file_size_mb**: 500MB maximum (configurable)
- **small_file_threshold_mb**: 50MB threshold for optimization

## Memory Management

### Memory Usage Patterns

Based on performance tests (`tests/performance/test_memory_performance.py`):

| File Size | Typical Memory Usage | Peak Memory | Chunking Strategy |
|-----------|---------------------|-------------|-------------------|
| Small (<1MB) | <150MB | <150MB | Single load |
| Medium (1-50MB) | <500MB | <500MB | 10K row chunks |
| Large (>50MB) | <2GB | <2GB | 1K-5K row chunks |

### Memory Techniques

#### 1. Automatic Chunking

The system automatically chunks large files to stay within memory limits:

```python
# From autocsv_profiler/base.py
def get_data_summary(self) -> dict:
    return {
        "memory_usage_mb": (self.df.memory_usage(deep=True).sum() / (1024 * 1024)),
        # ... other metrics
    }
```

#### 2. Data Type Optimization

Memory usage can be reduced by optimizing pandas data types:

```python
# Example optimization from performance tests
if df["int_col"].max() < 128:
    df["int_col"] = df["int_col"].astype("int8")  # 87.5% memory savings

df["category_col"] = df["category_col"].astype("category")  # 60-80% savings
df["float_col"] = df["float_col"].astype("float32")  # 50% memory savings
```

#### 3. Environment Variables for Memory Control

```bash
# Configure memory limits
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=2.0
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=5000
export AUTOCSV_PERFORMANCE_MAX_FILE_SIZE_MB=1000
```

### Memory Monitoring

Real-time memory monitoring with psutil integration:

```python
# Example from docs/examples/advanced/performance_optimization.py
def monitor_memory_usage():
    if psutil:
        memory = psutil.virtual_memory()
        print(f"Available memory: {memory.available / (1024**3):.1f} GB")
        print(f"Memory usage: {memory.percent:.1f}%")
```

## Processing Benchmarks

### Performance Test Results

Based on `tests/performance/test_resource_management.py`:

| File Size | Rows | Processing Time | Memory Peak | Throughput |
|-----------|------|----------------|-------------|------------|
| Tiny (50 rows) | 50 | <10s | <20MB | >5 rows/s |
| Small (500 rows) | 500 | <20s | <50MB | >25 rows/s |
| Medium (2,000 rows) | 2,000 | <45s | <100MB | >45 rows/s |
| Large (10,000 rows) | 10,000 | <90s | <200MB | >110 rows/s |

### Scaling Characteristics

- **Time Complexity**: Processing time scales sub-linearly with data size
- **Memory Efficiency**: Memory usage controlled through chunking
- **Engine Isolation**: No cross-contamination between engine environments

### Concurrent Processing

The system supports concurrent analysis with proper resource isolation:

```python
# From performance tests
def test_concurrent_processing():
    # Multiple files can be processed simultaneously
    # Each analysis uses separate conda environment
    # Memory usage scales appropriately
```

## Engine Performance Characteristics

### Performance Comparison

| Engine | Speed | Memory Usage | Report Quality | Use Case |
|--------|-------|--------------|---------------|---------------|
| **Main** | Fast | Low | High | Statistical analysis, large files |
| **YData** | Slow | High | Highest | Data profiling, data quality |
| **SweetViz** | Fast | Medium | High | Data overviews, presentations |
| **DataPrep** | Medium | Medium | High | EDA, distribution analysis |

### Engine-Specific Optimizations

#### Main Engine
- **Environment**: Python 3.11, latest pandas/numpy
- **Strengths**: Fast statistical computation, memory efficient
- **Memory usage**: 20-150MB depending on file size
- **Processing time**: 1-30s for typical files

#### YData Profiling Engine
- **Environment**: Python 3.10, YData Profiling 4.16.1
- **Strengths**: Most analysis
- **Memory usage**: 100-1000MB for reports
- **Processing time**: 30s-5min depending on complexity

#### SweetViz Engine
- **Environment**: Python 3.10, SweetViz 2.3.1
- **Strengths**: Fast visual reports
- **Memory usage**: 50-300MB
- **Processing time**: 5-60s for typical files

#### DataPrep Engine
- **Environment**: Python 3.10, pandas 1.5.3
- **Strengths**: Balanced features and performance
- **Memory usage**: 50-500MB
- **Processing time**: 10s-2min

## Large File Handling

### Chunking Strategy

The system uses intelligent chunking for large files:

```python
# Adaptive chunk sizing based on available memory
def calculate_optimal_chunk_size(file_size_mb, memory_limit_gb):
    if memory_limit_gb < 1:
        return 1000  # Conservative for low memory
    elif memory_limit_gb < 4:
        return 5000  # Medium memory systems
    else:
        return 10000  # High memory systems
```

### Large File Performance Guidelines

| System Memory | Recommended Chunk Size | Max File Size | Expected Performance |
|---------------|----------------------|---------------|---------------------|
| <2GB | 1,000-2,000 rows | 100MB | Slower but stable |
| 2-8GB | 5,000-10,000 rows | 500MB | Good performance |
| >8GB | 10,000-20,000 rows | 1GB+ | Optimal performance |

### Memory-Constrained Environments

For systems with limited memory:

```bash
# Environment configuration for low memory
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=0.5
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=2000
export AUTOCSV_PERFORMANCE_MAX_FILE_SIZE_MB=100
```

## Optimization Techniques

### 1. System-Level Optimizations

```bash
# Use SSD storage for temporary files
export TMPDIR="/path/to/ssd/tmp"

# Increase available memory
# Close unnecessary applications before analysis

# Use parallel processing when available
python docs/examples/advanced/batch_processing.py --parallel
```

### 2. Engine Selection Optimization

Choose engines based on requirements:

```python
# For speed - use main or sweetviz engines
analysis_result = profile_csv("data.csv", "output/", engine="main")

# For memory efficiency - use main engine with small chunks
os.environ["AUTOCSV_PERFORMANCE_CHUNK_SIZE"] = "1000"
analysis_result = profile_csv("data.csv", "output/", engine="main")

# For data analysis - use ydata with adequate resources
analysis_result = profile_csv("data.csv", "output/", engine="ydata")
```

### 3. Data Preprocessing Optimization

```python
# Remove unnecessary columns before analysis
df = df.drop(['unused_column1', 'unused_column2'], axis=1)

# Optimize data types before analysis
df['category'] = df['category'].astype('category')
df['large_int'] = df['large_int'].astype('int32')
```

### 4. Configuration Optimization

Create environment-specific configurations:

```python
# For development/testing - speed optimized
development_config = {
    "chunk_size": 5000,
    "memory_limit_gb": 1,
    "engines": ["main", "sweetviz"]
}

# For production - quality optimized
production_config = {
    "chunk_size": 10000,
    "memory_limit_gb": 4,
    "engines": ["main", "ydata", "sweetviz", "dataprep"]
}
```

## System Requirements

### Minimum Requirements

- **CPU**: Dual-core processor
- **RAM**: 4GB (8GB recommended)
- **Storage**: 5GB free space for conda environments
- **Python**: 3.10 or higher
- **Conda**: Anaconda or Miniconda

### Recommended Configuration

- **CPU**: Quad-core processor or higher
- **RAM**: 16GB or higher
- **Storage**: SSD with 10GB+ free space
- **Python**: 3.11 for optimal performance
- **Network**: Internet connection for initial setup

### Platform-Specific Considerations

#### Windows
- Use conda environments on SSD drives
- Disable Windows Defender real-time scanning for conda directories
- Configure adequate virtual memory

#### macOS
- Ensure conda is in system PATH
- Use homebrew-installed conda for performance
- Configure adequate swap space

#### Linux
- Use conda with appropriate permissions
- Configure swap for memory-intensive operations
- Consider using tmpfs for temporary files

## Configuration Tuning

### Performance Tuning Examples

#### High-Memory System (16GB+)
```bash
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=8.0
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=20000
export AUTOCSV_PERFORMANCE_MAX_FILE_SIZE_MB=2000
```

#### Low-Memory System (<4GB)
```bash
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=0.5
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=1000
export AUTOCSV_PERFORMANCE_MAX_FILE_SIZE_MB=50
```

#### SSD-Optimized Configuration
```bash
export TMPDIR="/ssd/tmp"
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=15000
export AUTOCSV_LOGGING_FILE_ENABLED=false  # Reduce disk I/O
```

### Dynamic Configuration

```python
# Runtime performance adjustment based on system resources
from autocsv_profiler.config import Settings

settings = Settings()

# Adjust based on available memory
import psutil
available_gb = psutil.virtual_memory().available / (1024**3)

if available_gb > 8:
    settings.set("performance.memory_limit_gb", 4.0)
    settings.set("performance.chunk_size", 15000)
elif available_gb > 4:
    settings.set("performance.memory_limit_gb", 2.0)
    settings.set("performance.chunk_size", 10000)
else:
    settings.set("performance.memory_limit_gb", 1.0)
    settings.set("performance.chunk_size", 5000)
```

## Troubleshooting Performance Issues

### Common Performance Problems

#### 1. High Memory Usage

**Symptoms:**
- System becomes unresponsive during analysis
- Out of memory errors
- Excessive swap usage

**Solutions:**
```bash
# Reduce memory limit and chunk size
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=1.0
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=2000

# Use memory-efficient engine
python bin/run_analysis.py --engine main data.csv
```

#### 2. Slow Processing

**Symptoms:**
- Analysis takes much longer than expected
- High CPU usage without progress
- Frequent disk access

**Solutions:**
```bash
# Increase chunk size (if memory allows)
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=20000

# Use faster engine
python bin/run_analysis.py --engine sweetviz data.csv

# Check disk space and use SSD
df -h
export TMPDIR="/path/to/ssd/tmp"
```

#### 3. Engine Failures

**Symptoms:**
- Import errors in specific engines
- Conda environment issues
- Dependency conflicts

**Solutions:**
```bash
# Recreate conda environments
python bin/setup_environments.py create --force

# Check environment status
conda env list | grep csv-profiler

# For engine testing commands, see [Engine Testing Guide](api/engines/ENGINE_TESTING.md)
```

#### 4. Resource Exhaustion

**Symptoms:**
- System runs out of disk space
- Temporary files not cleaned up
- Multiple failed attempts

**Solutions:**
```bash
# Clean temporary files
rm -rf /tmp/autocsv_*
rm -rf ~/.cache/autocsv_profiler/

# Monitor disk usage during analysis
df -h; python bin/run_analysis.py data.csv; df -h

# Configure temporary directory with adequate space
export TMPDIR="/path/to/large/disk/tmp"
```

### Performance Monitoring

Use the built-in performance examples to monitor and optimize:

```bash
# Run performance optimization analysis
python docs/examples/advanced/performance_optimization.py

# Compare engine performance
python docs/examples/basic/engine_comparison.py your_data.csv

# Test memory constraints
python docs/examples/basic/large_file_processing.py large_data.csv
```

### Performance Logging

Enable performance metrics logging:

```bash
# Enable performance logging
export AUTOCSV_LOGGING_PERFORMANCE_METRICS=true

# Check logs for performance information
tail -f autocsv_profiler.log | grep -i performance
```

## Advanced Performance Topics

### Memory Pool Management

The system manages memory pools for different operations:

- **DataFrame operations**: Managed by pandas
- **Statistical computations**: Managed by numpy/scipy
- **Visualization**: Managed by matplotlib with Agg backend
- **Report generation**: Managed by individual engines

### Garbage Collection Optimization

```python
# Force garbage collection after large operations
import gc

def analyze_with_cleanup(csv_file):
    # Perform analysis
    result = profile_csv(csv_file, "output/")

    # Force cleanup
    gc.collect()

    return result
```

### Multi-Processing Considerations

While the system uses multi-environment architecture, it runs engines sequentially within each environment to avoid resource conflicts. For true parallel processing, use the batch processing examples:

```python
# Parallel analysis of multiple files
python docs/examples/advanced/batch_processing.py --parallel /path/to/csv/files/
```

This guide provides comprehensive performance information based on actual system capabilities and test results. For specific performance questions or optimization needs, refer to the performance test suite in `tests/performance/` and the optimization examples in `docs/examples/`.