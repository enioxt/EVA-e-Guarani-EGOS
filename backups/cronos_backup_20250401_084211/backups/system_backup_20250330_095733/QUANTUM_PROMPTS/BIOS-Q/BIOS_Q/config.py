#!/usr/bin/env python3
"""
EVA & GUARANI - Configuration Module
---------------------------------
This module provides configuration management for the
EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for EVA & GUARANI BIOS-Q."""

    def __init__(self):
        """Initialize configuration manager."""
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self):
        """Load configuration from environment variables and config files."""
        try:
            # Load environment variables
            self.config.update(
                {
                    "version": "7.5",
                    "created": "2025-03-26",
                    "web": {
                        "host": os.getenv("WEB_HOST", "localhost"),
                        "port": int(os.getenv("WEB_PORT", "8000")),
                        "debug": os.getenv("WEB_DEBUG", "false").lower() == "true",
                    },
                    "monitoring": {
                        "prometheus_port": int(os.getenv("PROMETHEUS_PORT", "9090")),
                        "grafana_url": os.getenv("GRAFANA_URL", "http://localhost:3000"),
                        "grafana_api_key": os.getenv("GRAFANA_API_KEY", ""),
                    },
                    "quantum_search": {
                        "index_path": os.getenv("SEARCH_INDEX_PATH", "data/search_index"),
                        "max_results": int(os.getenv("SEARCH_MAX_RESULTS", "100")),
                        "min_relevance": float(os.getenv("SEARCH_MIN_RELEVANCE", "0.5")),
                    },
                    "translator": {
                        "cache_path": os.getenv("TRANSLATOR_CACHE_PATH", "data/translations"),
                        "max_cache_size": int(os.getenv("TRANSLATOR_MAX_CACHE", "10000")),
                        "default_source_lang": os.getenv("TRANSLATOR_DEFAULT_SOURCE", "en"),
                    },
                    "mycelium": {
                        "max_nodes": int(os.getenv("MYCELIUM_MAX_NODES", "100")),
                        "max_connections": int(os.getenv("MYCELIUM_MAX_CONNECTIONS", "1000")),
                        "update_interval": float(os.getenv("MYCELIUM_UPDATE_INTERVAL", "1.0")),
                    },
                    "security": {
                        "jwt_secret": os.getenv("JWT_SECRET", ""),
                        "jwt_algorithm": os.getenv("JWT_ALGORITHM", "HS256"),
                        "jwt_expiry": int(os.getenv("JWT_EXPIRY", "3600")),
                        "rate_limit_authenticated": int(os.getenv("RATE_LIMIT_AUTH", "100")),
                        "rate_limit_anonymous": int(os.getenv("RATE_LIMIT_ANON", "10")),
                    },
                    "logging": {
                        "level": os.getenv("LOG_LEVEL", "INFO"),
                        "file": os.getenv("LOG_FILE", "logs/bios_q.log"),
                        "max_size": int(os.getenv("LOG_MAX_SIZE", "10485760")),  # 10MB
                        "backup_count": int(os.getenv("LOG_BACKUP_COUNT", "5")),
                    },
                }
            )

            # Load config file if it exists
            config_path = Path("config.json")
            if config_path.exists():
                with open(config_path, "r") as f:
                    file_config = json.load(f)
                    self.config.update(file_config)

            logger.info("Configuration loaded successfully")

        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        try:
            # Support nested keys with dot notation
            keys = key.split(".")
            value = self.config
            for k in keys:
                value = value.get(k, default)
                if value is None:
                    return default
            return value

        except Exception as e:
            logger.error(f"Error getting configuration value for {key}: {str(e)}")
            return default

    def set(self, key: str, value: Any):
        """Set configuration value by key."""
        try:
            # Support nested keys with dot notation
            keys = key.split(".")
            config = self.config
            for k in keys[:-1]:
                config = config.setdefault(k, {})
            config[keys[-1]] = value
            logger.info(f"Configuration value set: {key} = {value}")

        except Exception as e:
            logger.error(f"Error setting configuration value for {key}: {str(e)}")
            raise

    def save(self, path: Optional[str] = None):
        """Save configuration to file."""
        try:
            save_path = Path(path) if path else Path("config.json")
            with open(save_path, "w") as f:
                json.dump(self.config, f, indent=4)
            logger.info(f"Configuration saved to {save_path}")

        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            raise

    def validate(self) -> bool:
        """Validate configuration."""
        try:
            # Check required values
            required = [
                "web.host",
                "web.port",
                "monitoring.prometheus_port",
                "monitoring.grafana_url",
                "quantum_search.index_path",
                "translator.cache_path",
                "mycelium.max_nodes",
                "security.jwt_secret",
            ]

            for key in required:
                if self.get(key) is None:
                    logger.error(f"Missing required configuration: {key}")
                    return False

            # Validate port numbers
            ports = ["web.port", "monitoring.prometheus_port"]

            for key in ports:
                port = self.get(key)
                if not (isinstance(port, int) and 1 <= port <= 65535):
                    logger.error(f"Invalid port number for {key}: {port}")
                    return False

            # Validate numeric values
            numeric = [
                ("quantum_search.min_relevance", 0.0, 1.0),
                ("mycelium.update_interval", 0.1, 60.0),
                ("security.jwt_expiry", 60, 86400),
            ]

            for key, min_val, max_val in numeric:
                value = self.get(key)
                if not (isinstance(value, (int, float)) and min_val <= value <= max_val):
                    logger.error(f"Invalid value for {key}: {value}")
                    return False

            logger.info("Configuration validation successful")
            return True

        except Exception as e:
            logger.error(f"Error validating configuration: {str(e)}")
            return False

    def __str__(self) -> str:
        """Return string representation of configuration."""
        return json.dumps(self.config, indent=4)


# Global configuration instance
config = Config()
