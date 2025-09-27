"""Centralized logging system for AutoCSV Profiler Suite."""

import json
import logging
import logging.handlers
import os
from pathlib import Path

# Import types and settings with optional fallback
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from autocsv_profiler.config.settings import Settings

# Try to import settings, but make it optional for subprocess environments
SETTINGS_AVAILABLE = False
settings: Optional["Settings"] = None

try:
    from autocsv_profiler.config.settings import settings

    SETTINGS_AVAILABLE = True
except ImportError:
    pass  # settings remains None


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging with JSON output."""

    def format(self, record: logging.LogRecord) -> str:
        try:
            structured_debug = settings and settings.get(
                "logging.app.structured_debug", False
            )
        except (AttributeError, KeyError, TypeError):
            structured_debug = False

        if structured_debug:
            log_data = {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }

            if hasattr(record, "extra_data"):
                log_data.update(getattr(record, "extra_data"))

            return json.dumps(log_data)
        else:
            return super().format(record)


class LoggingManager:
    """Centralized logging management system."""

    def __init__(self) -> None:
        self._loggers: Dict[str, logging.Logger] = {}
        self._initialized = False

    def initialize(self) -> None:
        """Initialize the logging system based on configuration."""
        if self._initialized:
            return

        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Check for DEBUG environment variable to override log level
        debug_mode = os.environ.get("DEBUG") == "1"

        if SETTINGS_AVAILABLE and settings:
            try:
                log_level_str = settings.get("logging.level", "INFO").upper()
            except Exception:
                log_level_str = "INFO"
        else:
            # Fallback if settings not available in subprocess
            log_level_str = "INFO"

        if debug_mode:
            log_level_str = "DEBUG"
            print("[DEBUG] Debug mode enabled - setting log level to DEBUG")

        log_level = getattr(logging, log_level_str)
        root_logger.setLevel(log_level)

        # Use fallbacks in case settings aren't available
        if SETTINGS_AVAILABLE and settings:
            try:
                console_enabled = settings.get("logging.console.enabled", True)
                file_enabled = settings.get("logging.file.enabled", True)
            except Exception:
                console_enabled = True
                file_enabled = True
        else:
            # Default fallback values for subprocess environments
            console_enabled = True
            file_enabled = True

        if console_enabled:
            self._setup_console_logging()

        if file_enabled:
            self._setup_file_logging()

        self._initialized = True

    def _setup_console_logging(self) -> None:
        """Setup console logging handler."""
        import os

        console_handler = logging.StreamHandler()

        if SETTINGS_AVAILABLE and settings:
            try:
                console_level = settings.get("logging.console.level", "INFO")
                console_format = settings.get(
                    "logging.console.format",
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                )
            except Exception:
                console_level = "INFO"
                console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        else:
            # Fallback values for subprocess environments
            console_level = "INFO"
            console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # Override console level in debug mode
        if os.environ.get("DEBUG") == "1":
            console_level = "DEBUG"
            console_format = "%(asctime)s - %(name)s - %(levelname)s - [%(module)s:%(funcName)s:%(lineno)d] - %(message)s"

        console_handler.setLevel(getattr(logging, console_level.upper()))
        console_formatter = StructuredFormatter(console_format)
        console_handler.setFormatter(console_formatter)

        logging.getLogger().addHandler(console_handler)

    def _setup_file_logging(self) -> None:
        """Setup file logging with rotation."""
        # Use absolute path to ensure all subprocess engines write to the same log file
        import os

        project_root = Path(__file__).parent.parent.parent
        log_dir = project_root / "logs"
        log_dir.mkdir(exist_ok=True)

        # Use fallback values in case settings aren't available in subprocess
        if SETTINGS_AVAILABLE and settings:
            try:
                log_filename = settings.get(
                    "logging.file.filename", "autocsv_profiler.log"
                )
                max_bytes = settings.get("logging.file.max_bytes", 10485760)  # 10MB
                backup_count = settings.get("logging.file.backup_count", 5)
                file_level = settings.get("logging.file.level", "DEBUG")
                file_format = settings.get(
                    "logging.file.format",
                    "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                )
            except Exception:
                # Fallback configuration for subprocess environments
                log_filename = "autocsv_profiler.log"
                max_bytes = 10485760  # 10MB
                backup_count = 5
                file_level = "DEBUG"
                file_format = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        else:
            # Fallback configuration for subprocess environments
            log_filename = "autocsv_profiler.log"
            max_bytes = 10485760  # 10MB
            backup_count = 5
            file_level = "DEBUG"
            file_format = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"

        log_file = log_dir / log_filename

        # Debug: Print log file path when in debug mode
        if os.environ.get("DEBUG") == "1":
            print(f"[DEBUG] Logging to absolute path: {log_file}")

        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )

        file_handler.setLevel(getattr(logging, file_level.upper()))
        file_formatter = StructuredFormatter(file_format)
        file_handler.setFormatter(file_formatter)

        logging.getLogger().addHandler(file_handler)

    def get_logger(self, name: str) -> logging.Logger:
        """Get or create a logger with the specified name."""
        if not self._initialized:
            self.initialize()

        if name not in self._loggers:
            self._loggers[name] = logging.getLogger(name)

        return self._loggers[name]

    def log_user_interaction(
        self, message: str, extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log user interaction events if enabled."""
        enabled = True  # Default to enabled
        if SETTINGS_AVAILABLE and settings:
            try:
                enabled = settings.get("logging.app.user_interaction", True)
            except (AttributeError, KeyError, TypeError):
                enabled = True

        if enabled:
            logger = self.get_logger("user_interaction")
            if extra_data:
                logger.info(message, extra={"extra_data": extra_data})
            else:
                logger.info(message)

    def log_analysis_progress(
        self, message: str, extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log analysis progress events if enabled."""
        enabled = True  # Default to enabled
        if SETTINGS_AVAILABLE and settings:
            try:
                enabled = settings.get("logging.app.analysis_progress", True)
            except (AttributeError, KeyError, TypeError):
                enabled = True

        if enabled:
            logger = self.get_logger("analysis_progress")
            if extra_data:
                logger.info(message, extra={"extra_data": extra_data})
            else:
                logger.info(message)

    def log_performance(self, message: str, metrics: Dict[str, Any]) -> None:
        """Log performance metrics if enabled."""
        enabled = False  # Default to disabled
        if SETTINGS_AVAILABLE and settings:
            try:
                enabled = settings.get("logging.app.performance_metrics", False)
            except (AttributeError, KeyError, TypeError):
                enabled = False

        if enabled:
            logger = self.get_logger("performance")
            logger.info(message, extra={"extra_data": metrics})


# Global logging manager instance
logging_manager = LoggingManager()


def get_logger(name: str) -> logging.Logger:
    """Convenience function to get a logger."""
    return logging_manager.get_logger(name)


def log_print(message: str, level: str = "INFO", logger_name: str = "autocsv") -> None:
    """Print message to console and log it."""
    print(message)
    logger = get_logger(logger_name)
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.log(log_level, message)


def log_user_input(prompt: str, user_input: str, context: str = "") -> None:
    """Log user input interactions."""
    logging_manager.log_user_interaction(
        f"User Input - {prompt}: {user_input}",
        {"prompt": prompt, "input": user_input, "context": context},
    )


def log_analysis_step(step: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Log analysis step progress."""
    logging_manager.log_analysis_progress(f"Analysis Step: {step}", details)


def log_performance_metric(operation: str, **metrics: Any) -> None:
    """Log performance metrics."""
    logging_manager.log_performance(f"Performance - {operation}", metrics)


def log_structured(
    logger_name: str, level: str, message: str, **extra_fields: Any
) -> None:
    """Log with structured data."""
    logger = get_logger(logger_name)
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.log(log_level, message, extra={"extra_data": extra_fields})


# Initialize logging on import if settings are available
try:
    logging_manager.initialize()
except Exception:
    pass
