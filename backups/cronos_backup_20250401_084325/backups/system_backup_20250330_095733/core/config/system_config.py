#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - System Configuration Management
This module provides a unified interface for managing system-wide configurations.

Version: 1.0.0
Date: 2025-03-20
"""

import os
import json
import yaml
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("system_config.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

@dataclass
class EthicsConfig:
    """Configuration for the Ethics system."""
    shield_strength: float = 0.97
    validation_accuracy: float = 0.96
    processing_power: float = 0.95
    consciousness_level: float = 0.98
    love_quotient: float = 0.99
    
    def validate(self) -> bool:
        """Validate ethics configuration."""
        return all(0 <= value <= 1 for value in [
            self.shield_strength,
            self.validation_accuracy,
            self.processing_power,
            self.consciousness_level,
            self.love_quotient
        ])

@dataclass
class ArtConfig:
    """Configuration for the Artistic system."""
    creativity_level: float = 0.95
    aesthetic_sensitivity: float = 0.93
    innovation_factor: float = 0.92
    harmony_index: float = 0.94
    evolution_rate: float = 0.91
    
    def validate(self) -> bool:
        """Validate art configuration."""
        return all(0 <= value <= 1 for value in [
            self.creativity_level,
            self.aesthetic_sensitivity,
            self.innovation_factor,
            self.harmony_index,
            self.evolution_rate
        ])

@dataclass
class SystemConfig:
    """Main system configuration."""
    version: str = "8.0.0"
    ethics: EthicsConfig = field(default_factory=EthicsConfig)
    art: ArtConfig = field(default_factory=ArtConfig)
    backup_enabled: bool = True
    debug_mode: bool = False
    log_level: str = "INFO"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "version": self.version,
            "ethics": {
                "shield_strength": self.ethics.shield_strength,
                "validation_accuracy": self.ethics.validation_accuracy,
                "processing_power": self.ethics.processing_power,
                "consciousness_level": self.ethics.consciousness_level,
                "love_quotient": self.ethics.love_quotient
            },
            "art": {
                "creativity_level": self.art.creativity_level,
                "aesthetic_sensitivity": self.art.aesthetic_sensitivity,
                "innovation_factor": self.art.innovation_factor,
                "harmony_index": self.art.harmony_index,
                "evolution_rate": self.art.evolution_rate
            },
            "backup_enabled": self.backup_enabled,
            "debug_mode": self.debug_mode,
            "log_level": self.log_level
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemConfig':
        """Create configuration from dictionary."""
        ethics_data = data.get("ethics", {})
        art_data = data.get("art", {})
        
        return cls(
            version=data.get("version", "8.0.0"),
            ethics=EthicsConfig(
                shield_strength=ethics_data.get("shield_strength", 0.97),
                validation_accuracy=ethics_data.get("validation_accuracy", 0.96),
                processing_power=ethics_data.get("processing_power", 0.95),
                consciousness_level=ethics_data.get("consciousness_level", 0.98),
                love_quotient=ethics_data.get("love_quotient", 0.99)
            ),
            art=ArtConfig(
                creativity_level=art_data.get("creativity_level", 0.95),
                aesthetic_sensitivity=art_data.get("aesthetic_sensitivity", 0.93),
                innovation_factor=art_data.get("innovation_factor", 0.92),
                harmony_index=art_data.get("harmony_index", 0.94),
                evolution_rate=art_data.get("evolution_rate", 0.91)
            ),
            backup_enabled=data.get("backup_enabled", True),
            debug_mode=data.get("debug_mode", False),
            log_level=data.get("log_level", "INFO")
        )

class ConfigManager:
    """System configuration manager."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration manager."""
        self.config_dir = config_dir or Path(__file__).parent
        self.config_file = self.config_dir / "system_config.yaml"
        self.config = SystemConfig()
    
    def load_config(self) -> bool:
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                self.config = SystemConfig.from_dict(data)
                logging.info("Configuration loaded successfully")
                return True
            else:
                logging.warning("Configuration file not found, using defaults")
                return False
        except Exception as e:
            logging.error(f"Error loading configuration: {str(e)}")
            return False
    
    def save_config(self) -> bool:
        """Save configuration to file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.config.to_dict(), f, default_flow_style=False)
            logging.info("Configuration saved successfully")
            return True
        except Exception as e:
            logging.error(f"Error saving configuration: {str(e)}")
            return False
    
    def validate_config(self) -> bool:
        """Validate current configuration."""
        try:
            if not self.config.ethics.validate():
                logging.error("Ethics configuration validation failed")
                return False
            
            if not self.config.art.validate():
                logging.error("Art configuration validation failed")
                return False
            
            logging.info("Configuration validation successful")
            return True
        except Exception as e:
            logging.error(f"Error validating configuration: {str(e)}")
            return False
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration with new values."""
        try:
            current_dict = self.config.to_dict()
            current_dict.update(updates)
            self.config = SystemConfig.from_dict(current_dict)
            
            if self.validate_config():
                return self.save_config()
            return False
        except Exception as e:
            logging.error(f"Error updating configuration: {str(e)}")
            return False
    
    def generate_default_config(self) -> bool:
        """Generate default configuration file."""
        try:
            if not self.config_file.exists():
                return self.save_config()
            logging.warning("Configuration file already exists")
            return False
        except Exception as e:
            logging.error(f"Error generating default configuration: {str(e)}")
            return False

def main():
    """Main execution function."""
    logging.info("=== INITIALIZING SYSTEM CONFIGURATION ===")
    
    try:
        config_manager = ConfigManager()
        
        # Generate default configuration if it doesn't exist
        if not config_manager.config_file.exists():
            if config_manager.generate_default_config():
                logging.info("Default configuration generated successfully")
            else:
                logging.error("Failed to generate default configuration")
                return
        
        # Load and validate configuration
        if config_manager.load_config() and config_manager.validate_config():
            logging.info("System configuration initialized successfully")
        else:
            logging.error("System configuration initialization failed")
            
    except Exception as e:
        logging.error(f"Error in configuration management: {str(e)}")
        
    logging.info("=== SYSTEM CONFIGURATION PROCESS COMPLETED ===")

if __name__ == "__main__":
    main() 