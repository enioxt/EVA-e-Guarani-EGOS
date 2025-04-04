#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Config (Configuration Management System)
Core implementation of the configuration management system.

This module provides the foundational capabilities for:
- System settings
- Environment management
- Parameter control
- Integration setup
"""

import logging
import json
import yaml
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ConfigType(Enum):
    """Types of configuration settings."""

    SYSTEM = "system"
    ENVIRONMENT = "environment"
    MODULE = "module"
    INTEGRATION = "integration"
    SECURITY = "security"
    QUANTUM = "quantum"


class ConfigFormat(Enum):
    """Supported configuration formats."""

    JSON = "json"
    YAML = "yaml"
    ENV = "env"


@dataclass
class ConfigValue:
    """Represents a configuration value."""

    key: str
    value: Any
    type: ConfigType
    description: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]


@dataclass
class ConfigGroup:
    """Represents a group of related configurations."""

    id: str
    name: str
    type: ConfigType
    description: str
    values: Dict[str, ConfigValue]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]


class ConfigCore:
    """Core implementation of the Config system."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize the Config system.

        Args:
            config_dir: Directory for storing configuration files
        """
        self.config_dir = config_dir or Path.home() / ".eva_guarani" / "config"
        self.groups: Dict[str, ConfigGroup] = {}
        self.lock = threading.Lock()
        self._initialize_storage()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Config Core initialized with love and consciousness")

    def _initialize_storage(self):
        """Initialize configuration storage."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            for config_type in ConfigType:
                (self.config_dir / config_type.value).mkdir(exist_ok=True)
            self.logger.info(f"Initialized configuration storage at {self.config_dir}")
        except Exception as e:
            self.logger.error(f"Error initializing storage: {str(e)}")
            raise

    def create_group(
        self,
        name: str,
        type: ConfigType,
        description: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Create a new configuration group.

        Args:
            name: Group name
            type: Configuration type
            description: Group description
            metadata: Additional metadata

        Returns:
            str: Group ID if successful, None otherwise
        """
        try:
            with self.lock:
                group_id = f"group_{type.value}_{name.lower()}"

                if group_id in self.groups:
                    self.logger.warning(f"Group {group_id} already exists")
                    return None

                group = ConfigGroup(
                    id=group_id,
                    name=name,
                    type=type,
                    description=description,
                    values={},
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    metadata=metadata or {},
                )

                self.groups[group_id] = group
                self._save_group(group)

                self.logger.info(f"Created configuration group {group_id}")
                return group_id
        except Exception as e:
            self.logger.error(f"Error creating group: {str(e)}")
            return None

    def set_value(
        self,
        group_id: str,
        key: str,
        value: Any,
        description: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Set a configuration value.

        Args:
            group_id: ID of the configuration group
            key: Configuration key
            value: Configuration value
            description: Value description
            metadata: Additional metadata

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.lock:
                if group_id not in self.groups:
                    self.logger.error(f"Group {group_id} not found")
                    return False

                group = self.groups[group_id]

                config_value = ConfigValue(
                    key=key,
                    value=value,
                    type=group.type,
                    description=description,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    metadata=metadata or {},
                )

                group.values[key] = config_value
                group.updated_at = datetime.now()

                self._save_group(group)

                self.logger.info(f"Set configuration value {key} in group {group_id}")
                return True
        except Exception as e:
            self.logger.error(f"Error setting value: {str(e)}")
            return False

    def get_value(self, group_id: str, key: str) -> Optional[Any]:
        """Get a configuration value.

        Args:
            group_id: ID of the configuration group
            key: Configuration key

        Returns:
            Any: Configuration value if found, None otherwise
        """
        try:
            if group_id not in self.groups:
                self.logger.error(f"Group {group_id} not found")
                return None

            group = self.groups[group_id]

            if key not in group.values:
                self.logger.error(f"Key {key} not found in group {group_id}")
                return None

            return group.values[key].value
        except Exception as e:
            self.logger.error(f"Error getting value: {str(e)}")
            return None

    def export_group(
        self, group_id: str, format: ConfigFormat = ConfigFormat.JSON
    ) -> Optional[str]:
        """Export a configuration group to a file.

        Args:
            group_id: ID of the configuration group
            format: Export format

        Returns:
            str: Path to exported file if successful, None otherwise
        """
        try:
            if group_id not in self.groups:
                self.logger.error(f"Group {group_id} not found")
                return None

            group = self.groups[group_id]
            export_data = {
                "id": group.id,
                "name": group.name,
                "type": group.type.value,
                "description": group.description,
                "values": {
                    k: {"value": v.value, "description": v.description, "metadata": v.metadata}
                    for k, v in group.values.items()
                },
                "metadata": group.metadata,
                "updated_at": group.updated_at.isoformat(),
            }

            export_path = self.config_dir / group.type.value / f"{group.id}.{format.value}"

            if format == ConfigFormat.JSON:
                with export_path.open("w") as f:
                    json.dump(export_data, f, indent=2)
            elif format == ConfigFormat.YAML:
                with export_path.open("w") as f:
                    yaml.dump(export_data, f)

            self.logger.info(f"Exported group {group_id} to {export_path}")
            return str(export_path)
        except Exception as e:
            self.logger.error(f"Error exporting group: {str(e)}")
            return None

    def import_group(self, file_path: Union[str, Path], format: ConfigFormat) -> Optional[str]:
        """Import a configuration group from a file.

        Args:
            file_path: Path to the configuration file
            format: File format

        Returns:
            str: Group ID if successful, None otherwise
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.error(f"File {file_path} not found")
                return None

            with file_path.open("r") as f:
                if format == ConfigFormat.JSON:
                    data = json.load(f)
                elif format == ConfigFormat.YAML:
                    data = yaml.safe_load(f)
                else:
                    self.logger.error(f"Unsupported format: {format.value}")
                    return None

            group_id = data["id"]
            group = ConfigGroup(
                id=group_id,
                name=data["name"],
                type=ConfigType(data["type"]),
                description=data["description"],
                values={},
                created_at=datetime.now(),
                updated_at=datetime.fromisoformat(data["updated_at"]),
                metadata=data["metadata"],
            )

            for key, value_data in data["values"].items():
                group.values[key] = ConfigValue(
                    key=key,
                    value=value_data["value"],
                    type=group.type,
                    description=value_data["description"],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    metadata=value_data["metadata"],
                )

            self.groups[group_id] = group
            self._save_group(group)

            self.logger.info(f"Imported group {group_id} from {file_path}")
            return group_id
        except Exception as e:
            self.logger.error(f"Error importing group: {str(e)}")
            return None

    def _save_group(self, group: ConfigGroup):
        """Save a configuration group to storage."""
        try:
            group_path = self.config_dir / group.type.value / f"{group.id}.json"
            with group_path.open("w") as f:
                json.dump(asdict(group), f, default=str)
        except Exception as e:
            self.logger.error(f"Error saving group: {str(e)}")
            raise


if __name__ == "__main__":
    # Example usage
    config = ConfigCore()

    # Create a system configuration group
    group_id = config.create_group(
        name="system_settings",
        type=ConfigType.SYSTEM,
        description="Core system settings",
        metadata={"version": "1.0.0"},
    )

    if group_id:
        # Set configuration values
        config.set_value(
            group_id=group_id,
            key="consciousness_level",
            value=0.95,
            description="System consciousness level",
            metadata={"min": 0.0, "max": 1.0},
        )

        config.set_value(
            group_id=group_id,
            key="love_quotient",
            value=0.98,
            description="System love quotient",
            metadata={"min": 0.0, "max": 1.0},
        )

        # Get configuration value
        consciousness_level = config.get_value(group_id, "consciousness_level")
        if consciousness_level is not None:
            print(f"Consciousness Level: {consciousness_level}")

        # Export configuration
        export_path = config.export_group(group_id, ConfigFormat.JSON)
        if export_path:
            print(f"Exported configuration to: {export_path}")

            # Import configuration
            imported_group_id = config.import_group(export_path, ConfigFormat.JSON)
            if imported_group_id:
                print(f"Imported configuration group: {imported_group_id}")
