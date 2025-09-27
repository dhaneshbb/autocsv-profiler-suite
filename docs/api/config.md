# config

Configuration management system for AutoCSV Profiler Suite.

## Table of Contents

- [Overview](#overview)
- [Classes](#classes)
- [Configuration Structure](#configuration-structure)
- [Configuration Validation](#configuration-validation)
- [Exceptions](#exceptions)
- [Usage Patterns](#usage-patterns)
- [Integration with Other Components](#integration-with-other-components)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

The `config` module provides configuration system that loads settings from YAML files and environment variables. It uses a singleton pattern to ensure consistent configuration access across all components.

## Classes

### Settings

Singleton class for managing configuration settings with YAML file loading and environment variable overrides.

```python
from autocsv_profiler.config import settings

# Access configuration values
chunk_size = settings.get("performance.chunk_size", 10000)
memory_limit = settings.get("performance.memory_limit_gb", 1)

# Get entire sections
performance_config = settings.get_section("performance")
```

#### Initialization

The Settings class is a singleton that loads configuration on first access:

```python
from autocsv_profiler.config import Settings, settings

# Global instance
current_settings = settings

# Create new instance (returns the singleton)
settings_instance = Settings()
```

**Loading Process:**
1. Loads `config/master_config.yml` from project root
2. Extracts the `app` section for runtime settings
3. Applies environment variable overrides
4. Validates configuration values

#### Methods

##### `get(key, default=None)`

Retrieve configuration values using dot notation.

```python
# Basic usage
chunk_size = settings.get("performance.chunk_size")
memory_limit = settings.get("performance.memory_limit_gb", 1.0)

# Nested access
confidence = settings.get("delimiter_detection.confidence_threshold", 0.7)
sample_lines = settings.get("delimiter_detection.sample_lines", 20)
```

**Parameters:**
- `key` (str): Configuration key using dot notation (e.g., "performance.chunk_size")
- `default` (Any): Default value if key is not found

**Returns:**
- `Any`: Configuration value or default if not found

##### `set(key, value)`

Set configuration values at runtime using dot notation.

```python
# Update performance settings
settings.set("performance.chunk_size", 20000)
settings.set("performance.memory_limit_gb", 2.0)

# Update nested values
settings.set("delimiter_detection.confidence_threshold", 0.8)
```

**Parameters:**
- `key` (str): Configuration key using dot notation
- `value` (Any): Value to set

**Features:**
- Creates nested dictionaries
- Logs configuration changes
- Does not persist changes to file

##### `get_section(section)`

Retrieve entire configuration sections.

```python
# Get performance configuration
perf_config = settings.get_section("performance")
print(f"Chunk size: {perf_config.get('chunk_size', 10000)}")

# Get logging configuration
log_config = settings.get_section("logging")
log_level = log_config.get("level", "INFO")
```

**Parameters:**
- `section` (str): Top-level configuration section name

**Returns:**
- `ConfigDict`: Dictionary containing the section configuration

##### `reload()`

Reload configuration from files and environment variables.

```python
# Reload configuration after changes
settings.reload()
```

**Use cases:**
- Configuration file changes during runtime
- Environment variable updates
- Testing with different configurations

##### `to_dict()`

Get the entire configuration as a dictionary.

```python
# Export current configuration
config_dict = settings.to_dict()

# Print all settings
import json
print(json.dumps(config_dict, indent=2))
```

**Returns:**
- `SettingsDict`: Complete configuration dictionary

##### `reset_instance()` (Class Method)

Reset the singleton instance for testing purposes.

```python
# Reset for testing
Settings.reset_instance()

# New instance will reload configuration
new_settings = Settings()
```

**Use cases:**
- Unit testing with different configurations
- Testing configuration validation
- Development and debugging

#### Attribute Access

Settings can also be accessed as attributes:

```python
# Attribute access
try:
    project_name = settings.project.name
    app_version = settings.project.version
except AttributeError:
    print("Setting not found")
```

**Note:** Raises `AttributeError` if the setting is not found.

## Configuration Structure

### Master Configuration File

Settings are loaded from `config/master_config.yml`:

```yaml
app:
  performance:
    chunk_size: 10000
    memory_limit_gb: 1
    max_file_size_mb: 500
    small_file_threshold_mb: 50
    chunk_estimate_factor: 1024

  delimiter_detection:
    enabled: true
    confidence_threshold: 0.7
    sample_lines: 20
    common_delimiters: [",", ";", "\t", "|", ":"]

  analysis:
    high_cardinality_threshold: 20
    decimal_precision: 4
    quantiles: [0.25, 0.50, 0.75]

  validation:
    max_chunk_size: 100000
    max_memory_limit_gb: 32
    min_confidence_threshold: 0.1

  logging:
    level: "INFO"
    file:
      enabled: true
      path: "logs/autocsv_profiler.log"
      max_bytes: 10485760  # 10MB
      backup_count: 5
    console:
      enabled: true
      format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

project:
  name: "autocsv-profiler-suite"
  version: "2.0.0"
  author: "AutoCSV Team"
```

### Environment Variable Overrides

Environment variables can override any configuration value using the format `AUTOCSV_<SECTION>_<KEY>`:

```bash
# Override performance settings
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=20000
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=2

# Override delimiter detection
export AUTOCSV_DELIMITER_DETECTION_CONFIDENCE_THRESHOLD=0.8

# Override logging level
export AUTOCSV_LOGGING_LEVEL=DEBUG
```

**Features:**
- Automatic type conversion (int, float, bool, str)
- Supports nested configuration paths
- Overrides take precedence over file values
- Changes are logged

### Type Conversion

Environment variables are automatically converted to appropriate types:

| String Value | Converted Type | Result |
|--------------|----------------|---------|
| "true", "yes", "1", "on" | bool | True |
| "false", "no", "0", "off" | bool | False |
| "123" | int | 123 |
| "12.34" | float | 12.34 |
| "text" | str | "text" |

## Configuration Validation

### Automatic Validation

The Settings class automatically validates configuration values on load:

```python
# Validation errors raise ConfigValidationError
try:
    settings = Settings()
except ConfigValidationError as e:
    print(f"Configuration error: {e}")
```

### Validation Rules

**Performance Settings:**
- `chunk_size`: Must be positive integer
- `memory_limit_gb`: Must be positive number
- `chunk_estimate_factor`: Must be positive number

**Delimiter Detection:**
- `confidence_threshold`: Must be between 0 and 1
- `sample_lines`: Must be positive integer

**Analysis Settings:**
- `high_cardinality_threshold`: Must be positive number
- `decimal_precision`: Must be non-negative integer

**Validation Limits:**
- `max_chunk_size`: Must be positive
- `max_memory_limit_gb`: Must be positive

**Logging Settings:**
- `level`: Must be valid logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `file.max_bytes`: Must be positive
- `file.backup_count`: Must be non-negative

### Custom Validation

Add custom validation by extending the `_validate_config` method:

```python
class CustomSettings(Settings):
    def _validate_config(self):
        super()._validate_config()

        # Add custom validation
        custom_value = self.get("custom.value", 0)
        if custom_value < 0:
            raise ConfigValidationError("custom.value must be non-negative")
```

## Exceptions

### ConfigValidationError

Raised when configuration validation fails.

```python
from autocsv_profiler.config import ConfigValidationError

try:
    settings.set("performance.chunk_size", -1000)
    settings._validate_config()
except ConfigValidationError as e:
    print(f"Validation error: {e}")
```

**Common scenarios:**
- Invalid value ranges (negative numbers where positive expected)
- Invalid logging levels
- Invalid file paths or permissions
- Type mismatches in configuration

## Usage Patterns

### Basic Configuration Access

```python
from autocsv_profiler.config import settings

def process_large_file(csv_path):
    # Get performance settings
    chunk_size = settings.get("performance.chunk_size", 10000)
    memory_limit = settings.get("performance.memory_limit_gb", 1.0)

    # Use settings in processing logic
    for chunk in read_csv_chunks(csv_path, chunk_size=chunk_size):
        if get_memory_usage() > memory_limit:
            break
        process_chunk(chunk)
```

### Configuration-Aware Components

```python
from autocsv_profiler.config import settings

class ConfigurableAnalyzer:
    def __init__(self):
        # Load settings once during initialization
        self.chunk_size = settings.get("performance.chunk_size", 10000)
        self.memory_limit = settings.get("performance.memory_limit_gb", 1.0)
        self.decimal_precision = settings.get("analysis.decimal_precision", 4)

    def analyze_data(self, data):
        # Use configured precision
        results = data.describe().round(self.decimal_precision)
        return results
```

### Environment-Specific Configuration

```python
import os
from autocsv_profiler.config import settings

# Development environment
if os.getenv("ENVIRONMENT") == "development":
    settings.set("logging.level", "DEBUG")
    settings.set("performance.chunk_size", 1000)  # Smaller chunks for testing

# Production environment
elif os.getenv("ENVIRONMENT") == "production":
    settings.set("logging.level", "WARNING")
    settings.set("performance.memory_limit_gb", 4.0)  # More memory available
```

### Testing with Custom Configuration

```python
import unittest
from autocsv_profiler.config import Settings, ConfigValidationError

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        # Reset singleton for each test
        Settings.reset_instance()

    def test_memory_limit_validation(self):
        settings = Settings()

        # Test invalid memory limit
        settings.set("performance.memory_limit_gb", -1)
        with self.assertRaises(ConfigValidationError):
            settings._validate_config()

    def test_custom_chunk_size(self):
        # Set environment variable for test
        os.environ["AUTOCSV_PERFORMANCE_CHUNK_SIZE"] = "5000"

        settings = Settings()
        self.assertEqual(settings.get("performance.chunk_size"), 5000)

        # Clean up
        del os.environ["AUTOCSV_PERFORMANCE_CHUNK_SIZE"]
```

### Runtime Configuration Updates

```python
from autocsv_profiler.config import settings

def optimize_for_large_dataset(file_size_gb):
    """Adjust configuration based on dataset size."""
    if file_size_gb > 5:
        # Large dataset optimization
        settings.set("performance.chunk_size", 5000)  # Smaller chunks
        settings.set("performance.memory_limit_gb", 8.0)  # More memory
    elif file_size_gb < 0.1:
        # Small dataset optimization
        settings.set("performance.chunk_size", 50000)  # Larger chunks
        settings.set("performance.memory_limit_gb", 0.5)  # Less memory needed
```

## Integration with Other Components

### Base Profiler Integration

```python
from autocsv_profiler.base import BaseProfiler
from autocsv_profiler.config import settings

class ConfiguredProfiler(BaseProfiler):
    def __init__(self, csv_path, delimiter, output_dir):
        # Use configuration for defaults
        chunk_size = settings.get("performance.chunk_size", 10000)
        memory_limit = settings.get("performance.memory_limit_gb", 1.0)

        super().__init__(csv_path, delimiter, output_dir, chunk_size, memory_limit)
```

### Engine Integration

```python
# In engines that support configuration
try:
    from autocsv_profiler.config import settings
    HAS_SETTINGS = True
except ImportError:
    settings = None
    HAS_SETTINGS = False

def get_chunk_size():
    if HAS_SETTINGS and settings:
        return settings.get("performance.chunk_size", 10000)
    return 10000  # Fallback default
```

### UI Integration

```python
from autocsv_profiler.config import settings
from autocsv_profiler.ui import CleanCSVInterface

class ConfigurableInterface(CleanCSVInterface):
    def __init__(self):
        super().__init__()

        # Configure based on settings
        self.sample_lines = settings.get("delimiter_detection.sample_lines", 20)
        self.confidence_threshold = settings.get("delimiter_detection.confidence_threshold", 0.7)

    def detect_delimiter(self, file_path):
        # Use configured values for detection
        return super().detect_delimiter(file_path, self.sample_lines, self.confidence_threshold)
```

## Performance Considerations

### Singleton Pattern

The Settings class uses the singleton pattern for efficiency:

```python
# Multiple imports return the same instance
from autocsv_profiler.config import settings as settings1
from autocsv_profiler.config import Settings

settings2 = Settings()
print(settings1 is settings2)  # True - same instance
```

### Configuration Caching

Configuration values are cached after loading:

```python
# First access loads from file
chunk_size = settings.get("performance.chunk_size")

# Subsequent accesses use cached values (fast)
memory_limit = settings.get("performance.memory_limit_gb")
```

### Environment Variable Processing

Environment variables are processed once during initialization:

```bash
# Set before application starts for best performance
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=20000
python bin/run_analysis.py
```

## Troubleshooting

### Common Configuration Issues

**File Not Found:**
```python
# Master configuration file missing
try:
    settings = Settings()
except FileNotFoundError as e:
    print(f"Configuration file missing: {e}")
    # Check config/master_config.yml exists
```

**Validation Errors:**
```python
# Invalid configuration values
try:
    settings = Settings()
except ConfigValidationError as e:
    print(f"Configuration error: {e}")
    # Check master_config.yml for invalid values
```

**Environment Variable Issues:**
```bash
# Check environment variables
env | grep AUTOCSV_

# Verify type conversion
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=invalid
python -c "from autocsv_profiler.config import settings; print(settings.get('performance.chunk_size'))"
```

### Debug Configuration

```python
from autocsv_profiler.config import settings
import json

# Print current configuration
config = settings.to_dict()
print("Current configuration:")
print(json.dumps(config, indent=2))

# Check specific values
print(f"Chunk size: {settings.get('performance.chunk_size')}")
print(f"Memory limit: {settings.get('performance.memory_limit_gb')}")
```

## See Also

- [autocsv_profiler](autocsv_profiler.md) - Main package interface
- [base](base.md) - BaseProfiler integration
- [core modules](README.md#core-modules) - Core utilities and exceptions
- [engines](engines/) - Engine implementations
- [ui](ui/) - User interface components