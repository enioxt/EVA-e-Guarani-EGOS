#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - KOIOS Logging Utility
=====================================

Provides a standardized way to configure and obtain loggers across EGOS subsystems,
ensuring consistent formatting and output as defined in KOIOS standards.

Version: 1.0.0
"""

import json
import logging
import logging.config
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional

# Module-level set to track configured loggers
_configured_loggers = set()

# --- Configuration --- #
# TODO: Load configuration from a KOIOS config file
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_DIR = Path("./logs")  # Relative to project root
LOG_FILE_NAME = "egos_system.log"
LOG_WHEN = "midnight"
LOG_INTERVAL = 1
LOG_BACKUP_COUNT = 7
STRUCTURED_LOGGING = False  # Set to True to enable JSON logging

# Ensure log directory exists
LOG_FILE_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE_PATH = LOG_FILE_DIR / LOG_FILE_NAME


class JsonFormatter(logging.Formatter):
    """Formats log records as JSON."""

    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            # Add other fields if necessary, e.g., filename, lineno
            # "filename": record.pathname,
            # "lineno": record.lineno,
        }
        # Handle exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


class KoiosLogger:
    """Provides standardized logging configuration for EGOS subsystems."""

    _loggers = {}
    _initialized = False

    @staticmethod
    def _initialize():
        """Sets up the root logger configuration."""
        if KoiosLogger._initialized:
            return

        root_logger = logging.getLogger()  # Get root logger
        root_logger.setLevel(DEFAULT_LOG_LEVEL)  # Set root level

        # --- Console Handler --- #
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(DEFAULT_LOG_LEVEL)  # Console logs at default level

        # --- File Handler (Rotating) --- #
        file_handler = TimedRotatingFileHandler(
            LOG_FILE_PATH,
            when=LOG_WHEN,
            interval=LOG_INTERVAL,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)  # Log DEBUG and above to file

        # --- Formatter --- #
        if STRUCTURED_LOGGING:
            formatter = JsonFormatter(datefmt=DEFAULT_DATE_FORMAT)
        else:
            formatter = logging.Formatter(DEFAULT_LOG_FORMAT, datefmt=DEFAULT_DATE_FORMAT)

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # --- Add Handlers to Root Logger --- #
        # Clear existing handlers (important if re-initializing or in certain environments)
        if root_logger.hasHandlers():
            root_logger.handlers.clear()

        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

        KoiosLogger._initialized = True
        root_logger.info("KoiosLogger initialized. Logging to console and %s", LOG_FILE_PATH)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Gets a logger instance with the specified name.

        Initializes the root logger configuration on the first call.
        Ensures loggers inherit the root configuration.

        Args:
            name (str): The name for the logger (e.g., 'ATLAS.Core').

        Returns:
            logging.Logger: The configured logger instance.
        """
        if not KoiosLogger._initialized:
            KoiosLogger._initialize()

        if name not in KoiosLogger._loggers:
            logger = logging.getLogger(name)
            # Logger level is typically controlled by the root logger's level
            # and the handlers' levels. Setting level here might override that.
            # logger.setLevel(DEFAULT_LOG_LEVEL)
            KoiosLogger._loggers[name] = logger
            logger.debug(f"Logger '{name}' created.")  # Log creation at DEBUG level

        return KoiosLogger._loggers[name]


# Example Usage (can be removed later)
if __name__ == "__main__":
    logger1 = KoiosLogger.get_logger("SUBSYSTEM_A.Module1")
    logger2 = KoiosLogger.get_logger("SUBSYSTEM_B")
    logger3 = KoiosLogger.get_logger("SUBSYSTEM_A.Module2")

    logger1.debug("This is a debug message from A.1")
    logger1.info("This is an info message from A.1")
    logger2.info("This is an info message from B")
    logger3.warning("This is a warning from A.2")
    logger2.error("This is an error from B")

    try:
        x = 1 / 0
    except ZeroDivisionError:
        logger1.exception("Caught an exception in A.1")

    print(f"Check log file at: {LOG_FILE_PATH}")


def get_koios_logger(
    name: str,
    config: Optional[Dict[str, Any]] = None,
    level: Optional[int] = None,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
    log_to_console: bool = True,
    log_file: Optional[str] = None,  # Optional path to a file
) -> logging.Logger:
    """Configures and returns a standardized logger instance.

    Args:
        name (str): The name for the logger (e.g., 'EGOS.NEXUS.Core', 'ATLAS_Service').
                    Hierarchical names using dots are recommended.
        config (Optional[Dict[str, Any]]): A configuration dictionary. If provided,
                                           it overrides other parameters.
                                           Expected keys: 'level', 'format', 'date_format',
                                                          'log_to_console', 'log_file'.
        level (Optional[int]): The logging level (e.g., logging.INFO, logging.DEBUG).
                               Defaults to logging.INFO.
        log_format (Optional[str]): The format string for log messages.
                                    Defaults to DEFAULT_LOG_FORMAT.
        date_format (Optional[str]): The format string for timestamps.
                                     Defaults to DEFAULT_DATE_FORMAT.
        log_to_console (bool): Whether to add a StreamHandler to output logs to console.
                               Defaults to True.
        log_file (Optional[str]): Path to a file where logs should also be written.
                                  Defaults to None (no file logging).

    Returns:
        logging.Logger: A configured Logger instance.
    """
    logger = logging.getLogger(name)

    # --- Determine Configuration --- #
    if config:
        log_level_str = config.get("level", "INFO").upper()
        _level = getattr(logging, log_level_str, logging.INFO)
        _format = config.get("format", DEFAULT_LOG_FORMAT)
        _date_fmt = config.get("date_format", DEFAULT_DATE_FORMAT)
        _console = config.get("log_to_console", log_to_console)
        _file = config.get("log_file", log_file)
    else:
        _level = level if level is not None else logging.INFO
        _format = log_format or DEFAULT_LOG_FORMAT
        _date_fmt = date_format or DEFAULT_DATE_FORMAT
        _console = log_to_console
        _file = log_file
    # ----------------------------- #

    # Set level ONLY if it's higher than the current level or not set
    # Avoid lowering the level if already configured by a parent logger
    if logger.level == logging.NOTSET or _level > logger.level:
        logger.setLevel(_level)

    # Prevent adding duplicate handlers if logger was already configured
    if name in _configured_loggers:
        # logger.debug(f"Logger '{name}' already configured. Skipping handler setup.")
        return logger

    # --- Configure Handlers --- #
    # Avoid adding handlers if the logger *already* has some (e.g., configured globally)
    if not logger.handlers:
        formatter = logging.Formatter(_format, datefmt=_date_fmt)

        if _console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(_level)  # Handler level should match logger level initially
            logger.addHandler(console_handler)
            # logger.debug(f"Added Console Handler to logger '{name}'")

        if _file:
            try:
                file_handler = logging.FileHandler(_file, encoding="utf-8")
                file_handler.setFormatter(formatter)
                file_handler.setLevel(_level)
                logger.addHandler(file_handler)
                # logger.debug(f"Added File Handler ('{_file}') to logger '{name}'")
            except Exception as e:
                # Log error to console if possible, even if file logging fails
                console_logger = logging.getLogger("KoiosLoggerSetupError")
                console_logger.error(
                    f"Failed to create file handler for '{_file}': {e}", exc_info=True
                )

        # Prevent messages from propagating to the root logger if handlers were added
        if logger.handlers:
            logger.propagate = False
            _configured_loggers.add(name)
            logger.debug(f"Configured handlers for logger '{name}'")
        else:
            # If no handlers were added (e.g., console=False, file=None), allow propagation
            logger.propagate = True
            logger.debug(f"No handlers added for logger '{name}'; propagation enabled.")
    else:
        # logger.debug(f"Logger '{name}' already has handlers. Skipping setup.")
        # Mark as configured even if we didn't add handlers this time
        _configured_loggers.add(name)

    # -------------------------- #

    return logger


# Example Usage (can be run standalone for testing)
if __name__ == "__main__":
    print("--- Testing Koios Logger --- ")

    # Basic logger
    log1 = get_koios_logger("EGOS.Test.Basic")
    log1.info("This is an INFO message from the basic logger.")
    log1.debug("This DEBUG message might not appear (default level is INFO).")

    # Logger with debug level
    log2 = get_koios_logger("EGOS.Test.Debug", level=logging.DEBUG)
    log2.debug("This is a DEBUG message.")
    log2.info("This is an INFO message.")

    # Logger with custom format and file output
    custom_format = "%(levelname)s - %(name)s: %(message)s"
    try:
        log3 = get_koios_logger(
            "EGOS.Test.File",
            level=logging.INFO,
            log_format=custom_format,
            log_file="_test_koios_log.log",  # Creates file in current dir
        )
        log3.warning("This message goes to console and _test_koios_log.log with custom format.")
        print("Check for '_test_koios_log.log' in the current directory.")
        # Clean up test file
        # import os
        # if os.path.exists("_test_koios_log.log"): os.remove("_test_koios_log.log")
    except Exception as e:
        print(f"File logging test failed: {e}")

    # Logger configured via dictionary
    config_dict = {
        "level": "DEBUG",
        "format": "[%(asctime)s] %(name)s %(levelname)s - %(message)s",
        "date_format": "%H:%M:%S",
        "log_to_console": True,
        "log_file": None,
    }
    log4 = get_koios_logger("EGOS.Test.Config", config=config_dict)
    log4.debug("This logger was configured via a dictionary.")

    # Test getting the same logger again (should not add handlers)
    log1_again = get_koios_logger("EGOS.Test.Basic")
    log1_again.info("Testing getting the same logger again.")
    assert len(log1.handlers) == len(log1_again.handlers)

    print("--- Testing Complete --- ")
