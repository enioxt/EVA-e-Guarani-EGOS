#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI system settings.

This module contains the main system settings, loaded from the config.json file
and complemented with default values and initialization logic.

Author: EVA & GUARANI
Date: 19/03/2025
Version: 1.0
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system_config.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SystemConfig")

# Path to the project's root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Path to the configuration file
CONFIG_FILE = BASE_DIR / "core" / "config" / "config.json"

# Default values for important settings
DEFAULT_CONFIG = {
    "system": {
        "name": "EVA & GUARANI",
        "version": "8.0.0",
        "environment": "development",
        "debug": True,
        "log_level": "info"
    },
    "paths": {
        "data_dir": "./data",
        "logs_dir": "./data/logs",
    },
    "core": {
        "egos": {
            "enabled": True,
            "auto_start": True
        }
    },
    "security": {
        "auth_required": False
    }
}

def load_config() -> Dict[str, Any]:
    """
    Loads the settings from the config.json file.
    If the file does not exist or is invalid, uses the default settings.
    """
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.info(f"Settings loaded from {CONFIG_FILE}")
                return config
        else:
            logger.warning(f"Configuration file {CONFIG_FILE} not found. Using default values.")
            return DEFAULT_CONFIG
    except Exception as e:
        logger.error(f"Error loading settings: {e}")
        return DEFAULT_CONFIG

def get_config_value(path: str, default: Any = None) -> Any:
    """
    Retrieves a specific configuration value using a path notation.
    
    Args:
        path: Path to the value, in the format "section.subsection.key"
        default: Default value if the path does not exist
        
    Returns:
        The configuration value or the default value
    """
    keys = path.split('.')
    config_copy = CONFIG
    
    try:
        for key in keys:
            config_copy = config_copy[key]
        return config_co    except (KeyError, TypeError):
        return default

def update_config(path: str, value: Any, save: bool = False) -> bool:
    """
    Updates a specific configuration value.
    
    Args:
        path: Path to the value, in the format "section.subsection.key"
        value: New value
        save: If True, saves the changes to the configuration file
        
    Returns:
        True if the update was successful, False otherwise
    """
    keys = path.split('.')
    config_copy = CONFIG
    
    try:
        # Navigate to the penultimate level
        for key in keys[:-1]:
            if key not in config_copy:
                config_copy[key] = {}
            config_copy = config_copy[key]
        
        # Update the value
        config_copy[keys[-1]] = value
        
        if save:
            save_config()
        
        return True
    except Exception as e:
        logger.error(f"Error updating configuration {path}: {e}")
        return False

def save_config() -> bool:
    """
    Saves the current settings to the config.json file.
    
    Returns:
        True if the save was successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(CONFIG, f, ensure_ascii=False, indent=2)
        logger.info(f"Settings saved to {CONFIG_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error saving settings: {e}")
        return False

def get_environment() -> str:
    """
    Returns the current environment (development, testing, production).
    
    Returns:
        String representing the environment
    """
    return get_config_value('system.environment', 'development')

def is_development() -> bool:
    """Checks if the environment is development."""
    return get_environment() == 'development'

def is_production() -> bool:
    """Checks if the environment is production."""
    return get_environment() == 'production'

def is_testing() -> bool:
    """Checks if the environment is testing."""
    return get_environment() == 'testing'

def get_log_level() -> int:
    """
    Returns the configured log level.
    
    Returns:
        Logging level constant
    """
    level_str = get_config_value('system.log_level', 'info').upper()
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    return levels.get(level_str, logging.INFO)

def initialize() -> None:
    """
    Initializes the system settings.
    """
    global CONFIG
    CONFIG = load_config()
    
    # Set the log level
    logging.getLogger().setLevel(get_log_level())
    
    # Create necessary directories
    for path_key in ['data_dir', 'logs_dir', 'models_dir', 'backup_dir', 'exports_dir', 'temp_dir']:
        path = get_config_value(f'paths.{path_key}')
        if path:
            os.makedirs(Path(BASE_DIR) / path, exist_ok=True)
    
    logger.info(f"System {get_config_value('system.name')} v{get_config_value('system.version')} initialized in environment {get_environment()}")

# Initialize settings when importing the module
CONFIG = {}
initialize()

# Export useful constants and functions
VERSION = get_config_value('system.version', '8.0.0')
DEBUG = get_config_value('system.debug', False)
SYSTEM_NAME = get_config_value('system.name', 'EVA & GUARANI')
DATA_DIR = Path(BASE_DIR) / get_config_value('paths.data_dir', 'data')
LOGS_DIR = Path(BASE_DIR) / get_config_value('paths.logs_dir', 'data/logs')