import logging
import os
from pathlib import Path
from typing import Any, List, Optional, Union, cast

import yaml

from autocsv_profiler.types import ConfigDict, SettingsDict


class ConfigValidationError(Exception):
    """Exception raised for configuration validation errors."""


class Settings:
    _instance: Optional["Settings"] = None
    _settings: SettingsDict

    def __new__(cls) -> "Settings":
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._load_settings()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance - useful for testing."""
        cls._instance = None

    def _load_settings(self) -> None:
        """Load configuration from master_config.yml and environment variables."""
        # Load master configuration directly
        master_config_path = (
            Path(__file__).parent.parent.parent / "config" / "master_config.yml"
        )

        if not master_config_path.exists():
            raise FileNotFoundError(
                f"Master configuration file not found: {master_config_path}"
            )

        try:
            with open(master_config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                # Extract the app configuration section which contains runtime settings
                self._settings = config.get("app", {})

                # Also store project metadata for access
                if "project" in config:
                    self._settings["project"] = config["project"]

        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing master configuration file: {e}")

        # Apply environment variable overrides
        self._apply_env_overrides()

        # Validate configuration
        self._validate_config()

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides."""
        # Environment variables should be in format: AUTOCSV_<SECTION>_<KEY>
        prefix: str = "AUTOCSV_"

        for env_key, env_value in os.environ.items():
            if not env_key.startswith(prefix):
                continue

            # Convert env key to config path (remove AUTOCSV_ prefix)
            config_path = env_key[len(prefix) :].lower().replace("_", ".")

            # Try to convert value to appropriate type
            converted_value: Union[str, int, float, bool] = self._convert_env_value(
                env_value
            )

            # Set the value in config
            self._set_nested_value(self._settings, config_path, converted_value)

            logging.info(
                f"Applied environment override: {config_path} = {converted_value}"
            )

    def _convert_env_value(self, value: str) -> Union[str, int, float, bool]:
        """Convert environment variable string to appropriate type."""
        # Try boolean conversion first
        if value.lower() in ("true", "yes", "1", "on"):
            return True
        if value.lower() in ("false", "no", "0", "off"):
            return False

        # Try numeric conversion
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass

        return value

    def _set_nested_value(self, config: ConfigDict, path: str, value: Any) -> None:
        """Set a nested value in the configuration dictionary."""
        parts: List[str] = path.split(".")
        current: ConfigDict = config

        # Navigate to the parent of the target key
        for part in parts[:-1]:
            if (part not in current) or (not isinstance(current[part], dict)):
                current[part] = {}
            current = cast(ConfigDict, current[part])

        # Set the final value
        current[parts[-1]] = value

    def _validate_config(self) -> None:
        """Validate configuration values."""
        try:
            # Validate performance settings
            perf_config = self._settings.get("performance", {})
            if isinstance(perf_config, dict):
                chunk_size = perf_config.get("chunk_size", 10000)
                memory_limit = perf_config.get("memory_limit_gb", 1)

                if isinstance(chunk_size, (int, float)) and chunk_size <= 0:
                    raise ConfigValidationError(
                        "performance.chunk_size must be positive"
                    )
                if isinstance(memory_limit, (int, float)) and memory_limit <= 0:
                    raise ConfigValidationError(
                        "performance.memory_limit_gb must be positive"
                    )

                estimate_factor = perf_config.get("chunk_estimate_factor", 1024)
                if isinstance(estimate_factor, (int, float)) and estimate_factor <= 0:
                    raise ConfigValidationError(
                        "performance.chunk_estimate_factor must be positive"
                    )

            # Validate delimiter detection settings
            delim_config = self._settings.get("delimiter_detection", {})
            if isinstance(delim_config, dict):
                confidence = delim_config.get("confidence_threshold", 0.7)
                if isinstance(confidence, (int, float)) and not (0 <= confidence <= 1):
                    raise ConfigValidationError(
                        "delimiter_detection.confidence_threshold must be "
                        "between 0 and 1"
                    )

            # Validate analysis settings
            analysis_config = self._settings.get("analysis", {})
            if isinstance(analysis_config, dict):
                threshold = analysis_config.get("high_cardinality_threshold", 20)
                if isinstance(threshold, (int, float)) and threshold <= 0:
                    raise ConfigValidationError(
                        "analysis.high_cardinality_threshold must be positive"
                    )

            # Validate validation limits
            validation_config = self._settings.get("validation", {})
            if isinstance(validation_config, dict):
                max_chunk = validation_config.get("max_chunk_size", 100000)
                if isinstance(max_chunk, (int, float)) and max_chunk <= 0:
                    raise ConfigValidationError(
                        "validation.max_chunk_size must be positive"
                    )

                max_memory = validation_config.get("max_memory_limit_gb", 32)
                if isinstance(max_memory, (int, float)) and max_memory <= 0:
                    raise ConfigValidationError(
                        "validation.max_memory_limit_gb must be positive"
                    )

            # Validate logging settings
            log_config = self._settings.get("logging", {})
            if isinstance(log_config, dict):
                valid_levels = [
                    "DEBUG",
                    "INFO",
                    "WARNING",
                    "ERROR",
                    "CRITICAL",
                ]

                level_value = log_config.get("level", "INFO")
                if (
                    isinstance(level_value, str)
                    and level_value.upper() not in valid_levels
                ):
                    raise ConfigValidationError(
                        f"logging.level must be one of: {valid_levels}"
                    )

                # Check file logging config
                file_config = log_config.get("file", {})
                if isinstance(file_config, dict):
                    max_bytes = file_config.get("max_bytes", 10485760)
                    if isinstance(max_bytes, (int, float)) and max_bytes <= 0:
                        raise ConfigValidationError(
                            "logging.file.max_bytes must be positive"
                        )

                    backup_count = file_config.get("backup_count", 5)
                    if isinstance(backup_count, (int, float)) and backup_count < 0:
                        raise ConfigValidationError(
                            "logging.file.backup_count must be non-negative"
                        )

                # Check console logging format
                console_config = log_config.get("console", {})
                if isinstance(console_config, dict):
                    console_format = console_config.get("format", "")
                    if console_format and not isinstance(console_format, str):
                        raise ConfigValidationError(
                            "logging.console.format must be a string"
                        )

            logging.info("Configuration validation passed")

        except Exception as e:
            raise ConfigValidationError(f"Configuration validation failed: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a setting by its key. Supports dot notation for nested keys."""
        parts: List[str] = key.split(".")
        current: Any = self._settings
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value at runtime. Supports dot notation."""
        self._set_nested_value(self._settings, key, value)
        logging.info(f"Runtime configuration update: {key} = {value}")

    def reload(self) -> None:
        """Reload configuration from files and environment."""
        self._load_settings()
        logging.info("Configuration reloaded")

    def get_section(self, section: str) -> ConfigDict:
        """Get an entire configuration section."""
        result = self.get(section, {})
        if isinstance(result, dict):
            return cast(ConfigDict, result)
        return {}

    def __getattr__(self, name: str) -> Any:
        """Allows accessing settings as attributes (e.g., settings.project.name)."""
        value: Any = self.get(name)
        if value is None:
            raise AttributeError(f"Setting '{name}' not found.")
        return value

    def to_dict(self) -> SettingsDict:
        """Return the entire configuration as a dictionary."""
        return self._settings.copy()


# Global settings instance
settings = Settings()
