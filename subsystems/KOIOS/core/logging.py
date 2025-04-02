#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - KOIOS Logging Utility
=====================================

Provides a standardized way to configure and obtain loggers across EGOS subsystems,
ensuring consistent formatting and output as defined in KOIOS standards.

Version: 1.0.0
"""

import logging
import sys
from typing import Optional, Dict, Any

# Default log format adhering to standards (Timestamp, Level, Logger Name, Message)
DEFAULT_LOG_FORMAT = "%(asctime)s [%(levelname)-8s] [%(name)-20s] %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Cache for configured loggers to avoid duplicate handlers
_configured_loggers = set()

def get_koios_logger(
    name: str,
    config: Optional[Dict[str, Any]] = None,
    level: Optional[int] = None,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
    log_to_console: bool = True,
    log_file: Optional[str] = None # Optional path to a file
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
        log_level_str = config.get('level', 'INFO').upper()
        _level = getattr(logging, log_level_str, logging.INFO)
        _format = config.get('format', DEFAULT_LOG_FORMAT)
        _date_fmt = config.get('date_format', DEFAULT_DATE_FORMAT)
        _console = config.get('log_to_console', log_to_console)
        _file = config.get('log_file', log_file)
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
            console_handler.setLevel(_level) # Handler level should match logger level initially
            logger.addHandler(console_handler)
            # logger.debug(f"Added Console Handler to logger '{name}'")

        if _file:
            try:
                file_handler = logging.FileHandler(_file, encoding='utf-8')
                file_handler.setFormatter(formatter)
                file_handler.setLevel(_level)
                logger.addHandler(file_handler)
                # logger.debug(f"Added File Handler ('{_file}') to logger '{name}'")
            except Exception as e:
                # Log error to console if possible, even if file logging fails
                console_logger = logging.getLogger("KoiosLoggerSetupError")
                console_logger.error(f"Failed to create file handler for '{_file}': {e}", exc_info=True)

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
if __name__ == '__main__':
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
            log_file="_test_koios_log.log" # Creates file in current dir
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
        'level': 'DEBUG',
        'format': '[%(asctime)s] %(name)s %(levelname)s - %(message)s',
        'date_format': '%H:%M:%S',
        'log_to_console': True,
        'log_file': None
    }
    log4 = get_koios_logger("EGOS.Test.Config", config=config_dict)
    log4.debug("This logger was configured via a dictionary.")

    # Test getting the same logger again (should not add handlers)
    log1_again = get_koios_logger("EGOS.Test.Basic")
    log1_again.info("Testing getting the same logger again.")
    assert len(log1.handlers) == len(log1_again.handlers)

    print("--- Testing Complete --- ") 