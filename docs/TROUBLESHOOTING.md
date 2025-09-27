# Troubleshooting Guide

Guide to diagnosing and resolving common issues with AutoCSV Profiler Suite.

## Table of Contents

- [Environment Setup Issues](#environment-setup-issues)
- [Import and Dependency Errors](#import-and-dependency-errors)
- [Memory and Performance Problems](#memory-and-performance-problems)
- [File Processing Errors](#file-processing-errors)
- [Engine-Specific Issues](#engine-specific-issues)
- [Debug Mode Usage](#debug-mode-usage)
- [Log Analysis Guide](#log-analysis-guide)

## Environment Setup Issues

### Issue 1: Conda Command Not Found

**Error Messages**:
```text
conda: command not found
'conda' is not recognized as an internal or external command
```

**Causes**:
- Conda not installed
- Conda not in system PATH
- Terminal not restarted after conda installation

**Solutions**:

1. **Verify conda installation**:
   ```bash
   # Check if conda is installed
   which conda  # Linux/macOS
   where conda  # Windows
   ```

2. **Add conda to PATH**:
   ```bash
   # Linux/macOS - add to ~/.bashrc or ~/.zshrc
   export PATH="$HOME/anaconda3/bin:$PATH"
   source ~/.bashrc

   # Windows - add to system PATH
   # Add C:\Anaconda3\Scripts to your PATH environment variable
   ```

3. **Initialize conda**:
   ```bash
   ~/anaconda3/bin/conda init
   # Restart terminal
   ```

4. **Reinstall conda** if necessary:
   - Download from [Anaconda Download](https://www.anaconda.com/download)
   - Follow platform-specific installation instructions

### Issue 2: Environment Creation Fails

**Error Messages**:
```
CondaHTTPError: HTTP 000 CONNECTION FAILED
PackagesNotFoundError: The following packages are not available
CondaValueError: The channel is not accessible
```

**Diagnostic Commands**:
```bash
# Check conda version
conda --version

# Check channels
conda config --show channels

# Test internet connectivity
ping conda-forge.org
```

**Solutions**:

**Conda troubleshooting procedures available in [Installation Guide - Common Installation Issues](INSTALLATION.md#common-installation-issues).**

Additional troubleshooting:

1. **Reset conda configuration**:
   ```bash
   conda config --remove-key channels
   conda config --add channels conda-forge
   conda config --add channels defaults
   ```

2. **Use sequential installation**:
   ```bash
   # View options first
   python bin/setup_environments.py --help

   # Try sequential installation
   python bin/setup_environments.py create
   # Instead of parallel: create --parallel
   ```

5. **Check firewall/proxy settings**:
   ```bash
   # If behind corporate firewall
   conda config --set proxy_servers.http http://proxy.company.com:8080
   conda config --set proxy_servers.https https://proxy.company.com:8080
   ```

### Issue 3: Environment Already Exists

**Error Messages**:
```
CondaValueError: prefix already exists
```

**Solutions**:

1. **Remove existing environments**:
   ```bash
   python bin/setup_environments.py remove --parallel
   ```

2. **Recreate specific environment**:
   ```bash
   python bin/setup_environments.py recreate csv-profiler-main
   ```

3. **Manual removal**:
   ```bash
   conda env remove -n csv-profiler-main
   conda env remove -n csv-profiler-profiling
   conda env remove -n csv-profiler-dataprep
   ```

### Issue 4: Permission Errors During Setup

**Error Messages**:
```
PermissionError: [Errno 13] Permission denied
OSError: [Errno 13] Permission denied: '/opt/anaconda3/envs/'
```

**Solutions**:

1. **Use user-level conda installation** (preferred):
   - Install Anaconda/Miniconda in your home directory
   - No admin rights required

2. **Fix conda permissions** (Linux/macOS):
   ```bash
   sudo chown -R $USER:$USER ~/anaconda3
   ```

3. **Change conda environment location**:
   ```bash
   # Create environments in user-writable location
   conda config --add envs_dirs ~/conda-envs
   ```

## Import and Dependency Errors

### Issue 5: Module Import Errors

**Error Messages**:
```
ImportError: No module named 'autocsv_profiler'
ImportError: cannot import name 'CleanInteractiveMethods'
ModuleNotFoundError: No module named 'ydata_profiling'
```

**Diagnostic Commands**:
```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Test base requirements
python -c "import pandas, yaml, rich, psutil; print('Base imports OK')"

# Check environment packages
conda list -n csv-profiler-main | grep pandas
conda list -n csv-profiler-profiling | grep ydata-profiling
```

**Solutions**:

1. **Follow installation guide**: Complete the [Installation Guide](INSTALLATION.md) steps
2. **Recreate environments**: `python bin/setup_environments.py recreate csv-profiler-profiling`
3. **Check environment activation**: `conda info --envs`
4. **Fix project path**: Ensure you're in the project root directory

### Issue 6: Version Conflicts

**Error Messages**:
```
ImportError: cannot import name 'ProfileReport' from 'ydata_profiling'
TypeError: 'module' object has no attribute 'create_report'
```

**Diagnostic Commands**: See [Engine Testing Guide](api/engines/ENGINE_TESTING.md) for comprehensive diagnostic commands.

**Solutions**:

1. **Regenerate environment configurations**:
   ```bash
   python bin/setup_environments.py generate
   python bin/setup_environments.py recreate csv-profiler-profiling
   ```

2. **Manual package installation**:
   ```bash
   conda activate csv-profiler-profiling
   conda install ydata-profiling=4.16.1 sweetviz=2.3.1
   ```

3. **Check environment specification**:
   ```bash
   # Verify environment files match master config
   cat config/environment_profiling.yml
   ```

## Memory and Performance Problems

### Issue 7: Out of Memory Errors

**Error Messages**:
```
MemoryError: Unable to allocate array
pandas.errors.ParserError: Error tokenizing data
MemoryError: Memory limit exceeded
```

**Diagnostic Commands**:
```bash
# Check available memory
free -h  # Linux
vm_stat  # macOS
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory  # Windows

# Check file size
ls -lh data.csv  # Linux/macOS
dir data.csv     # Windows
```

**Solutions**:

1. **Increase memory limits**: Edit `config/master_config.yml` to increase `memory_limit_gb` and decrease `chunk_size`. See [User Guide Configuration](USER_GUIDE.md#advanced-configuration-options) for details.

2. **Use smaller chunks**:
   ```bash
   # Regenerate environments with new settings
   python bin/setup_environments.py generate
   ```

3. **Free system memory**:
   ```bash
   # Close other applications
   # Clear browser cache
   # Restart system if necessary
   ```

4. **Process files in parts**:
   ```bash
   # Split large CSV files
   split -l 10000 large_file.csv part_
   ```

### Issue 8: Slow Performance

**Symptoms**:
- Analysis takes hours for medium files
- System becomes unresponsive
- High CPU usage

**Diagnostic Commands**:
```bash
# Monitor resource usage during analysis
top    # Linux/macOS
taskmgr  # Windows

# Check file characteristics
wc -l data.csv      # Line count
file data.csv       # File type and encoding
```

**Solutions**:

1. **Optimize chunk size**: Adjust `chunk_size` in `config/master_config.yml` based on your system and file size. See [User Guide Performance Tuning](USER_GUIDE.md#performance-tuning) for optimization strategies.

2. **Use selective engines**:
   ```bash
   # Run only fast engines
   # In interactive mode, select: 1,3 (Main + SweetViz)
   # Skip YData Profiling for large files
   ```

3. **Enable performance monitoring**:
   ```yaml
   # config/master_config.yml
   app:
     logging:
       app:
         performance_metrics: true
   ```

### Issue 9: Disk Space Issues

**Error Messages**:
```
OSError: [Errno 28] No space left on device
IOError: [Errno 28] No space left on device
```

**Solutions**:

1. **Check available space**:
   ```bash
   df -h       # Linux/macOS
   dir C:\     # Windows
   ```

2. **Clean conda cache**:
   ```bash
   conda clean --packages --tarballs --index-cache
   ```

3. **Change output location**:
   ```bash
   # Move to drive with more space
   python bin/run_analysis.py /path/to/data.csv
   # When prompted, specify output directory with more space
   ```

4. **Remove old environments**:
   ```bash
   python bin/setup_environments.py remove --parallel
   ```

## File Processing Errors

### Issue 10: File Not Found Errors

**Error Messages**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
FileProcessingError: File not found: /path/to/data.csv
```

**Solutions**:

1. **Check file path**:
   ```bash
   # Verify file exists
   ls -la data.csv         # Linux/macOS
   dir data.csv           # Windows

   # Use absolute path
   python bin/run_analysis.py /full/path/to/data.csv
   ```

2. **Check file permissions**:
   ```bash
   # Linux/macOS
   chmod 644 data.csv

   # Windows - right-click file -> Properties -> Security
   ```

3. **Handle special characters**:
   ```bash
   # Quote paths with spaces
   python bin/run_analysis.py "/path/with spaces/data.csv"
   ```

### Issue 11: Encoding Errors

**Error Messages**:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
UnicodeDecodeError: 'charmap' codec can't decode byte
pandas.errors.ParserError: Error tokenizing data
```

**Diagnostic Commands**:
```bash
# Check file encoding
file -bi data.csv       # Linux/macOS
python -c "import chardet; print(chardet.detect(open('data.csv', 'rb').read()))"
```

**Solutions**:

1. **Automatic encoding detection** (built-in):
   - The system automatically detects encoding using `charset-normalizer`
   - Supports UTF-8, UTF-8-BOM, Latin1, ISO-8859-1, CP1252, ASCII

2. **Manual encoding conversion**:
   ```bash
   # Convert to UTF-8
   iconv -f ISO-8859-1 -t UTF-8 data.csv > data_utf8.csv

   # Using Python
   python -c "
   with open('data.csv', 'r', encoding='iso-8859-1') as f:
       content = f.read()
   with open('data_utf8.csv', 'w', encoding='utf-8') as f:
       f.write(content)
   "
   ```

### Issue 12: Delimiter Detection Failures

**Error Messages**:
```
DelimiterDetectionError: Could not determine delimiter
pandas.errors.ParserError: Error tokenizing data
Detected delimiter: None (confidence: 0.0)
```

**Diagnostic Commands**:
```bash
# Inspect first few lines
head -5 data.csv
```

**Solutions**:

1. **Manual delimiter specification**:
   ```bash
   # When prompted during interactive mode
   # Enter delimiter manually: ; or \t or |
   ```

2. **Adjust detection settings**:
   ```yaml
   # config/master_config.yml
   app:
     delimiter_detection:
       confidence_threshold: 0.5   # Lower threshold
       sample_lines: 50            # More sample lines
   ```

3. **Use common delimiters**:
   - Comma: `,`
   - Semicolon: `;`
   - Tab: `\t` or type `tab`
   - Pipe: `|`
   - Space: type `space`

### Issue 13: Malformed CSV Files

**Error Messages**:
```
pandas.errors.ParserError: Error tokenizing data. C error: Expected X fields, got Y
pandas.errors.ParserError: EOF inside string starting at row X
```

**Diagnostic Commands**:
```bash
# Check line consistency
awk -F',' '{print NF}' data.csv | sort -nu  # Count fields per line
```

**Solutions**:

1. **Clean data format**:
   ```python
   # Python script to fix common issues
   import pandas as pd
   import csv

   # Read with error handling
   df = pd.read_csv('data.csv', error_bad_lines=False, warn_bad_lines=True)
   df.to_csv('data_cleaned.csv', index=False)
   ```

2. **Use robust parsing**:
   ```python
   # For problematic files, pandas automatically handles many issues
   # The system includes error handling for malformed data
   ```

## Engine-Specific Issues

### Issue 14: YData Profiling Errors

**Error Messages**:
```
ImportError: cannot import name 'ProfileReport' from 'ydata_profiling'
AttributeError: module 'ydata_profiling' has no attribute 'ProfileReport'
```

**Solutions**:

1. **Check YData version**:
   ```bash
   conda activate csv-profiler-profiling
   python -c "import ydata_profiling; print(ydata_profiling.__version__)"
   # Should be 4.16.1
   ```

2. **Reinstall YData Profiling**:
   ```bash
   conda activate csv-profiler-profiling
   conda remove ydata-profiling
   conda install ydata-profiling=4.16.1
   ```

3. **Test YData manually**: See [Engine Testing Guide](api/engines/ENGINE_TESTING.md) for testing commands.

### Issue 15: SweetViz Errors

**Error Messages**:
```
ImportError: No module named 'sweetviz'
AttributeError: module 'sweetviz' has no attribute 'analyze'
```

**Solutions**:

1. **Reinstall SweetViz**:
   ```bash
   conda activate csv-profiler-profiling
   conda install sweetviz=2.3.1
   ```

2. **Test SweetViz manually**: See [Engine Testing Guide](api/engines/ENGINE_TESTING.md) for testing commands.

### Issue 16: DataPrep Errors

**Error Messages**:
```
ImportError: No module named 'dataprep'
AttributeError: module 'dataprep' has no attribute 'eda'
```

**Solutions**:

1. **Check DataPrep environment**:
   ```bash
   conda activate csv-profiler-dataprep
   python -c "import dataprep; print(dataprep.__version__)"
   # Should be 0.4.5
   ```

2. **Reinstall DataPrep**:
   ```bash
   conda activate csv-profiler-dataprep
   conda install dataprep=0.4.5
   ```

### Issue 17: Main Engine Statistical Errors

**Error Messages**:
```
ImportError: No module named 'scipy'
ImportError: No module named 'researchpy'
ImportError: No module named 'tableone'
```

**Solutions**:

1. **Check main environment packages**:
   ```bash
   conda activate csv-profiler-main
   conda list | grep -E "scipy|numpy|pandas|researchpy|tableone"
   ```

2. **Reinstall statistical packages**:
   ```bash
   conda activate csv-profiler-main
   conda install scipy=1.13.1 numpy=2.2.6 researchpy=0.3.6 tableone=0.9.5
   ```

## Debug Mode Usage

### Enabling Debug Mode

**Command-line debug mode**:
```bash
python bin/run_analysis.py --debug
```

**Environment variable**:
```bash
export DEBUG=1
python bin/run_analysis.py
```

**Engine-specific debugging**: See [Engine Testing Guide](api/engines/ENGINE_TESTING.md#debug-mode-options) for detailed debug commands.

### Debug Output Interpretation

**Debug messages format**:
```
[DEBUG Main] Main analyzer started
[DEBUG Main] File path: /path/to/data.csv
[DEBUG Main] Memory limit: 1GB, Chunk size: 10000
[DEBUG YData] YData Profiling report generation started
[DEBUG YData] Loading data with delimiter: ,
```

**Key debug information**:
- File paths and validation results
- Memory usage and limits
- Chunk processing progress
- Engine-specific operations
- Error stack traces

### Debug Log Locations

**Console output**: Real-time debug messages
**Log files**:
```bash
# Check for log files in project directory
ls -la *.log
cat autocsv_profiler.log  # If logging to file is enabled
```

## Log Analysis Guide

### Log Configuration

**Enable detailed logging**:
```yaml
# config/master_config.yml
app:
  logging:
    level: "DEBUG"
    file:
      enabled: true
      level: "DEBUG"
      filename: "autocsv_profiler.log"
    app:
      performance_metrics: true
      structured_debug: true
```

### Common Log Patterns

**Successful analysis**:
```
INFO - Analysis started for: data.csv
INFO - Delimiter detected: , (confidence: 0.95)
INFO - Engine main/analyzer completed successfully
INFO - Engine profiling/ydata_report completed successfully
INFO - Analysis completed in 45.2 seconds
```

**Memory issues**:
```
WARNING - Memory usage high: 85% of limit
ERROR - MemoryError: Memory limit exceeded
DEBUG - Chunk size reduced from 10000 to 5000
```

**File processing issues**:
```
ERROR - FileProcessingError: File not found: data.csv
WARNING - Encoding detection confidence low: 0.4
ERROR - DelimiterDetectionError: Could not determine delimiter
```

**Environment issues**:
```
ERROR - ImportError: No module named 'ydata_profiling'
WARNING - Engine profiling/ydata_report failed, skipping
INFO - Continuing with available engines
```

### Log Analysis Commands

**Search for errors**:
```bash
grep -i error autocsv_profiler.log
grep -i "memory\|performance" autocsv_profiler.log
grep -E "ImportError|ModuleNotFoundError" autocsv_profiler.log
```

**Performance analysis**:
```bash
grep -i "completed in\|processing time" autocsv_profiler.log
grep -i "memory usage\|chunk size" autocsv_profiler.log
```

**Environment diagnostics**:
```bash
grep -i "environment\|conda" autocsv_profiler.log
grep -E "main|profiling|dataprep" autocsv_profiler.log
```

### When to Contact Support

If you've tried the solutions above and still have issues:

1. **Gather diagnostic information**:
   ```bash
   # System information
   python --version
   conda --version
   conda env list

   # Run with debug mode
   python bin/run_analysis.py --debug > debug_output.txt 2>&1
   ```

2. **Create minimal test case**:
   ```bash
   # Create small test file
   echo "name,age,city" > test.csv
   echo "John,25,NYC" >> test.csv

   # Test with debug
   python bin/run_analysis.py test.csv --debug
   ```

3. **Submit issue with**:
   - Operating system and version
   - Python and conda versions
   - Error messages and debug output
   - Steps to reproduce
   - Test file (if possible)

## Quick Reference

### Common Commands

```bash
# View all available options
python bin/setup_environments.py --help

# Restart from scratch - see INSTALLATION.md for complete options
python bin/setup_environments.py recreate --parallel  # Recommended approach

# Test individual components
# Test environment health
# For detailed testing commands, see Engine Testing Guide
python -c "import pandas, yaml, rich; print('Base OK')"

# Debug mode
python bin/run_analysis.py --debug

# Check environment health
conda list -n csv-profiler-main --explicit
```

### Emergency Reset

**Complete system reset** (use as last resort):
1. Remove environments: `python bin/setup_environments.py remove --parallel`
2. Clean conda: `conda clean --all`
3. Reinstall: Follow [Installation Guide](INSTALLATION.md) from step 2

---

## Still Having Issues?

- **Check [Installation Guide](INSTALLATION.md)** for setup issues
- **Review [User Guide](USER_GUIDE.md)** for usage questions
- **Use [Engine Testing Guide](api/engines/ENGINE_TESTING.md)** for engine-specific debugging
- **Search [GitHub Issues](https://github.com/dhaneshbb/autocsv-profiler-suite/issues)**
- **Create new issue** with debug output and system information
- **Join [GitHub Discussions](https://github.com/dhaneshbb/autocsv-profiler-suite/discussions)** for community help