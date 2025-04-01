#!/usr/bin/env python3
import logging
import os
from pathlib import Path
from typing import Optional

def setup_logger(level: int = logging.INFO, log_file: Optional[str] = None):
    """
    Setup the logger for the translator module
    
    Args:
        level: Logging level (default: INFO)
        log_file: Path to log file (default: None)
    """
    # Configure the root logger
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get the logger for our module
    logger = logging.getLogger('modules.translator_dev')
    logger.setLevel(level)
    
    # If a log file is specified, add a file handler
    if log_file:
        # Create the log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            
        # Add a file handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        )
        logger.addHandler(file_handler)
    
    return logger 