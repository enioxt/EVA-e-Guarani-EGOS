#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration module for EVA & GUARANI Translator.

This module provides the configuration handling for the translator,
including loading and saving settings, and default configuration values.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

# Set up logging
logger = logging.getLogger(__name__)


class Config:
    """Configuration handler for the translator."""

    # Default configuration
    DEFAULT_CONFIG = {
        # General settings
        "general": {
            "source_language": "pt",
            "target_language": "en",
            "backup_files": True,
            "backup_extension": ".bak",
            "show_progress": True,
            "concurrent_translations": 5,
            "show_summary": True,
        },
        # Engine settings
        "engines": {
            "default": "huggingface",
            "huggingface": {
                "enabled": True,
                "model": "Helsinki-NLP/opus-mt-pt-en",
                "device": "cpu",
                "batch_size": 8,
            },
            "openai": {
                "enabled": False,
                "model": "gpt-3.5-turbo",
                "api_key": "",
                "max_tokens": 4096,
                "temperature": 0.3,
                "max_cost": 10.0,
            },
        },
        # Cache settings
        "cache": {"enabled": True, "max_size_mb": 500, "ttl_days": 30},
        # File handling
        "files": {
            "extensions": [".txt", ".md", ".py", ".js", ".html", ".css", ".json", ".xml"],
            "ignore_patterns": ["node_modules", "venv", "__pycache__", "*.min.*", "*.bak"],
            "batch_size": 1000,
        },
        # Terminology settings
        "terminology": {
            "enabled": True,
            "glossary_file": "terminology.json",
            "case_sensitive": False,
        },
    }

    def __init__(self, config_file: Optional[str] = None):
        """Initialize the configuration.

        Args:
            config_file: Path to the configuration file. If None, the default config file will be used.
        """
        self.logger = logging.getLogger(__name__)

        # Set up configuration paths
        self.config_dir = os.path.join(Path(__file__).parent.parent, "data", "config")

        # Create config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)

        # Set up config file path
        if config_file is None:
            self.config_file = os.path.join(self.config_dir, "translator_config.json")
        else:
            self.config_file = config_file

        # Initialize settings with defaults
        self.settings = dict(self.DEFAULT_CONFIG)

        # Load configuration
        self.load()

    def load(self) -> bool:
        """Load configuration from file.

        Returns:
            True if configuration was loaded successfully, False otherwise
        """
        # Check if config file exists
        if not os.path.exists(self.config_file):
            self.logger.info(f"Configuration file not found: {self.config_file}")
            return self.save()  # Create default config

        try:
            # Load config from file
            with open(self.config_file, "r", encoding="utf-8") as f:
                loaded_config = json.load(f)

            # Update settings with loaded config
            self._merge_configs(self.settings, loaded_config)

            self.logger.info(f"Configuration loaded from {self.config_file}")
            return True

        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            return False

    def save(self) -> bool:
        """Save configuration to file.

        Returns:
            True if configuration was saved successfully, False otherwise
        """
        try:
            # Ensure config directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            # Save config to file
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)

            self.logger.info(f"Configuration saved to {self.config_file}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving configuration: {str(e)}")
            return False

    def _merge_configs(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """Recursively merge two configurations.

        Args:
            base: Base configuration
            update: Configuration to merge into base
        """
        for key, value in update.items():
            if key in base and isinstance(value, dict) and isinstance(base[key], dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value

    def reset(self) -> bool:
        """Reset configuration to defaults.

        Returns:
            True if configuration was reset successfully, False otherwise
        """
        # Reset settings to defaults
        self.settings = dict(self.DEFAULT_CONFIG)

        # Save defaults to file
        return self.save()

    def get_engine_config(self, engine_name: Optional[str] = None) -> Dict[str, Any]:
        """Get configuration for the specified engine.

        Args:
            engine_name: Name of the engine to get configuration for.
                        If None, the default engine will be used.

        Returns:
            Dictionary with engine configuration
        """
        if engine_name is None:
            engine_name = self.settings["engines"]["default"]

        # Check if engine exists
        if engine_name not in self.settings["engines"]:
            self.logger.warning(f"Engine {engine_name} not found in configuration")
            return {}

        return self.settings["engines"][engine_name]

    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions.

        Returns:
            List of supported file extensions
        """
        return self.settings["files"]["extensions"]

    def is_extension_supported(self, file_path: str) -> bool:
        """Check if the file extension is supported.

        Args:
            file_path: Path to the file

        Returns:
            True if the file extension is supported, False otherwise
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.settings["files"]["extensions"]

    def should_ignore_file(self, file_path: str) -> bool:
        """Check if the file should be ignored based on ignore patterns.

        Args:
            file_path: Path to the file

        Returns:
            True if the file should be ignored, False otherwise
        """
        import fnmatch

        # Check if file matches any ignore pattern
        for pattern in self.settings["files"]["ignore_patterns"]:
            if fnmatch.fnmatch(file_path, pattern):
                return True

        return False
