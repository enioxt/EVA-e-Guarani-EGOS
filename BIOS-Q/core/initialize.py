#!/usr/bin/env python3
"""
BIOS-Q Initialization Module
Handles system initialization and context management for EVA & GUARANI
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

class BiosQ:
    """Basic Input/Output System - Quantum for EVA & GUARANI"""
    
    def __init__(self, config_path: str = "../src/data/eva_guarani_config.json"):
        """Initialize BIOS-Q system"""
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Configure logging for BIOS-Q"""
        logger = logging.getLogger("BIOS-Q")
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def load_config(self) -> Dict[str, Any]:
        """Load system configuration"""
        try:
            config_path = Path(self.config_path)
            if not config_path.exists():
                example_path = config_path.parent / "eva_guarani_config.example.json"
                if example_path.exists():
                    self.logger.warning(
                        f"Config file not found at {config_path}. "
                        f"Please copy {example_path} to {config_path} "
                        "and update with your settings."
                    )
                else:
                    self.logger.error(
                        f"Neither config file nor example config found. "
                        f"Please ensure proper configuration setup."
                    )
                return {}
                
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
                self.logger.info("Configuration loaded successfully")
                return self.config
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            return {}
    
    def initialize_directories(self) -> bool:
        """Create necessary directory structure"""
        try:
            required_dirs = [
                "BIOS-Q/logs",
                "BIOS-Q/resources",
                "src/data",
                ".metadata",
                "external/logs",
                "external/backups",
                "logs"
            ]
            
            for directory in required_dirs:
                Path(directory).mkdir(parents=True, exist_ok=True)
                self.logger.info(f"Created directory: {directory}")
            
            return True
        except Exception as e:
            self.logger.error(f"Error creating directories: {str(e)}")
            return False
    
    def verify_environment(self) -> bool:
        """Verify system environment and dependencies"""
        try:
            # Check Python version
            import sys
            if sys.version_info < (3, 11):
                self.logger.error("Python 3.11 or higher is required")
                return False
            
            # Check required packages
            import pkg_resources
            required_packages = [
                "pyyaml>=6.0.1",
                "tqdm>=4.66.1",
                "colorama>=0.4.6",
                "rich>=13.7.0",
                "requests>=2.31.0",
                "python-dotenv>=1.0.0"
            ]
            
            pkg_resources.require(required_packages)
            self.logger.info("All required packages are installed")
            
            return True
        except pkg_resources.VersionConflict as e:
            self.logger.error(f"Package version conflict: {str(e)}")
            return False
        except pkg_resources.DistributionNotFound as e:
            self.logger.error(f"Required package not found: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Environment verification error: {str(e)}")
            return False
    
    def initialize_system(self) -> bool:
        """Complete system initialization"""
        self.logger.info("Starting EVA & GUARANI initialization...")
        
        # Load configuration
        if not self.load_config():
            return False
        
        # Create directory structure
        if not self.initialize_directories():
            return False
        
        # Verify environment
        if not self.verify_environment():
            return False
        
        self.logger.info("EVA & GUARANI initialization completed successfully")
        return True

def main():
    """Main entry point for BIOS-Q initialization"""
    bios = BiosQ()
    if bios.initialize_system():
        print("\n✧༺❀༻∞ EVA & GUARANI initialized successfully ∞༺❀༻✧\n")
    else:
        print("\nInitialization failed. Please check the logs for details.\n")

if __name__ == "__main__":
    main() 