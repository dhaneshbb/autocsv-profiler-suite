"""
Functional tests for configuration system.

Tests the actual configuration loading, validation, and environment handling.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from autocsv_profiler import settings as global_settings  # noqa: E402
from autocsv_profiler.config.settings import Settings  # noqa: E402


class TestConfigurationFunctional:
    """Functional tests for configuration system."""

    @pytest.fixture
    def temp_config_file(self):
        """Create temporary configuration file."""
        temp_dir = Path(tempfile.mkdtemp(prefix="config_test_"))
        config_file = temp_dir / "test_config.yml"

        config_data = {
            "analysis": {"decimal_precision": 3, "quantiles": [0.1, 0.5, 0.9]},
            "processing": {"memory_limit_gb": 2, "chunk_size": 5000},
            "output": {"formats": ["csv", "json"], "include_plots": True},
            "engines": {
                "main": {"enabled": True, "priority": 1},
                "profiling": {"enabled": False, "priority": 2},
            },
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        yield config_file

        # Cleanup
        if config_file.exists():
            config_file.unlink()
        if temp_dir.exists():
            temp_dir.rmdir()

    def test_settings_initialization(self):
        """Test that settings object initializes correctly."""
        settings_obj = Settings()

        # Should have default values
        assert settings_obj.get("analysis.decimal_precision") is not None
        assert settings_obj.get("processing.memory_limit_gb") is not None

    def test_settings_load_from_file(self, temp_config_file):
        """Test loading configuration from file."""
        settings_obj = Settings(config_file=temp_config_file)

        # Should load values from file
        assert settings_obj.get("analysis.decimal_precision") == 3
        assert settings_obj.get("processing.memory_limit_gb") == 2
        assert settings_obj.get("output.include_plots") is True

    def test_settings_get_with_defaults(self, temp_config_file):
        """Test getting values with default fallbacks."""
        settings_obj = Settings(config_file=temp_config_file)

        # Existing value
        assert settings_obj.get("analysis.decimal_precision") == 3

        # Non-existing value with default
        assert settings_obj.get("nonexistent.key", "default_value") == "default_value"

        # Non-existing value without default
        assert settings_obj.get("nonexistent.key") is None

    def test_settings_set_values(self, temp_config_file):
        """Test setting configuration values."""
        settings_obj = Settings(config_file=temp_config_file)

        # Set new value
        settings_obj.set("test.new_key", "test_value")
        assert settings_obj.get("test.new_key") == "test_value"

        # Update existing value
        settings_obj.set("analysis.decimal_precision", 5)
        assert settings_obj.get("analysis.decimal_precision") == 5

    def test_settings_nested_access(self, temp_config_file):
        """Test nested configuration access."""
        settings_obj = Settings(config_file=temp_config_file)

        # Deep nested access
        assert settings_obj.get("engines.main.enabled") is True
        assert settings_obj.get("engines.profiling.priority") == 2

        # Set nested value
        settings_obj.set("engines.dataprep.enabled", True)
        assert settings_obj.get("engines.dataprep.enabled") is True

    def test_environment_variable_override(self):
        """Test configuration override via environment variables."""
        # Set environment variable
        env_key = "AUTOCSV_ANALYSIS__DECIMAL_PRECISION"
        original_value = os.environ.get(env_key)

        try:
            os.environ[env_key] = "6"
            settings_obj = Settings()

            # Environment variable should override default
            precision = settings_obj.get("analysis.decimal_precision")
            assert precision == 6

        finally:
            # Restore original environment
            if original_value is not None:
                os.environ[env_key] = original_value
            elif env_key in os.environ:
                del os.environ[env_key]

    def test_environment_variable_type_conversion(self):
        """Test automatic type conversion for environment variables."""
        test_cases = [
            ("AUTOCSV_TEST__INTEGER", "42", 42),
            ("AUTOCSV_TEST__FLOAT", "3.14", 3.14),
            ("AUTOCSV_TEST__BOOLEAN_TRUE", "true", True),
            ("AUTOCSV_TEST__BOOLEAN_FALSE", "false", False),
            ("AUTOCSV_TEST__STRING", "hello world", "hello world"),
        ]

        settings_obj = Settings()
        original_values = {}

        try:
            for env_key, env_value, expected in test_cases:
                # Store original value
                original_values[env_key] = os.environ.get(env_key)

                # Set test value
                os.environ[env_key] = env_value

                # Force reload settings
                settings_obj._load_environment_overrides()

                # Check conversion
                config_key = env_key.replace("AUTOCSV_", "").replace("__", ".").lower()
                actual = settings_obj.get(config_key)
                assert (
                    actual == expected
                ), f"Expected {expected}, got {actual} for {config_key}"

        finally:
            # Restore environment
            for env_key, original_value in original_values.items():
                if original_value is not None:
                    os.environ[env_key] = original_value
                elif env_key in os.environ:
                    del os.environ[env_key]

    def test_global_settings_object(self):
        """Test that global settings object works correctly."""
        # Global settings should be accessible
        assert global_settings is not None

        # Should have reasonable defaults
        precision = global_settings.get("analysis.decimal_precision", 4)
        assert isinstance(precision, int)
        assert precision > 0

        memory_limit = global_settings.get("processing.memory_limit_gb", 1)
        assert isinstance(memory_limit, (int, float))
        assert memory_limit > 0

    def test_config_validation_functionality(self, temp_config_file):
        """Test configuration validation."""
        settings_obj = Settings(config_file=temp_config_file)

        # Valid numeric values should work
        settings_obj.set("processing.memory_limit_gb", 4)
        assert settings_obj.get("processing.memory_limit_gb") == 4

        settings_obj.set("processing.chunk_size", 10000)
        assert settings_obj.get("processing.chunk_size") == 10000

    def test_config_persistence_behavior(self, temp_config_file):
        """Test configuration persistence behavior."""
        # Load initial settings
        settings_obj1 = Settings(config_file=temp_config_file)
        initial_precision = settings_obj1.get("analysis.decimal_precision")

        # Modify settings
        settings_obj1.set("analysis.decimal_precision", initial_precision + 1)

        # Create new settings object with same file
        settings_obj2 = Settings(config_file=temp_config_file)

        # Should still have original file values (not in-memory changes)
        assert settings_obj2.get("analysis.decimal_precision") == initial_precision

    def test_config_error_handling(self):
        """Test configuration error handling."""
        # Non-existent config file should not crash
        non_existent = Path("non_existent_config.yml")
        settings_obj = Settings(config_file=non_existent)

        # Should work with defaults
        assert settings_obj.get("analysis.decimal_precision", 4) == 4

    def test_malformed_config_handling(self):
        """Test handling of malformed configuration files."""
        temp_dir = Path(tempfile.mkdtemp(prefix="malformed_config_"))
        config_file = temp_dir / "malformed.yml"

        # Create malformed YAML
        config_file.write_text("invalid: yaml: content: [")

        try:
            # Should handle gracefully
            settings_obj = Settings(config_file=config_file)

            # Should fall back to defaults
            precision = settings_obj.get("analysis.decimal_precision", 4)
            assert precision == 4

        finally:
            # Cleanup
            if config_file.exists():
                config_file.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()

    def test_nested_config_structures(self, temp_config_file):
        """Test complex nested configuration structures."""
        settings_obj = Settings(config_file=temp_config_file)

        # Test deeply nested access
        quantiles = settings_obj.get("analysis.quantiles")
        assert isinstance(quantiles, list)
        assert len(quantiles) == 3

        # Test setting deeply nested values
        settings_obj.set("engines.custom.parameters.timeout", 30)
        assert settings_obj.get("engines.custom.parameters.timeout") == 30

    def test_config_default_values(self):
        """Test that reasonable defaults are provided."""
        settings_obj = Settings()

        # Check critical default values exist
        defaults_to_check = [
            ("analysis.decimal_precision", int),
            ("processing.memory_limit_gb", (int, float)),
            ("processing.chunk_size", int),
        ]

        for key, expected_type in defaults_to_check:
            value = settings_obj.get(key)
            if value is not None:  # Allow None for optional settings
                assert isinstance(
                    value, expected_type
                ), f"{key} should be {expected_type}, got {type(value)}"
