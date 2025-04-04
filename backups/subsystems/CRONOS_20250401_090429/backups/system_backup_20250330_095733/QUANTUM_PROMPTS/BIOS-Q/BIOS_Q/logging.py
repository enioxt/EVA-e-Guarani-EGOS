#!/usr/bin/env python3
"""
EVA & GUARANI - Logging Configuration
---------------------------------
This module provides logging configuration for the
EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

import os
import sys
import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Union

from .config import config


def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    max_size: Optional[int] = None,
    backup_count: Optional[int] = None,
):
    """Set up logging configuration."""
    try:
        # Get configuration values with defaults
        level_str = str(level or config.get("logging.level", "INFO"))
        log_file = str(Path(log_file or config.get("logging.file", "logs/bios_q.log")))
        max_size = int(max_size or config.get("logging.max_size", 10485760))  # 10MB
        backup_count = int(backup_count or config.get("logging.backup_count", 5))

        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.getLevelName(level_str))

        # Create formatters
        file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")

        # Configure file handler
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file, maxBytes=max_size, backupCount=backup_count
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

        # Configure console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

        # Create logger for this module
        logger = logging.getLogger(__name__)
        logger.info("Logging configured successfully")

        # Log configuration details
        logger.debug(f"Log level: {level_str}")
        logger.debug(f"Log file: {log_file}")
        logger.debug(f"Max size: {max_size} bytes")
        logger.debug(f"Backup count: {backup_count}")

    except Exception as e:
        print(f"Error setting up logging: {str(e)}", file=sys.stderr)
        raise


class LoggerAdapter(logging.LoggerAdapter):
    """Custom logger adapter with context information."""

    def process(self, msg, kwargs):
        """Process the logging message and keyword arguments."""
        extra = kwargs.get("extra", {})
        context = {
            "timestamp": extra.get("timestamp", ""),
            "component": extra.get("component", ""),
            "operation": extra.get("operation", ""),
            "correlation_id": extra.get("correlation_id", ""),
            "user_id": extra.get("user_id", ""),
        }

        # Add context information to message
        if any(context.values()):
            context_str = " ".join(f"{k}={v}" for k, v in context.items() if v)
            msg = f"{msg} [{context_str}]"

        return msg, kwargs


def get_logger(name: str) -> LoggerAdapter:
    """Get a logger with the custom adapter."""
    logger = logging.getLogger(name)
    return LoggerAdapter(logger, {})
