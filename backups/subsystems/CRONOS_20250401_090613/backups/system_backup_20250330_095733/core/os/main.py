#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Modular Analysis System, Systemic Cartography and Quantum Ethics
Main system initialization file
Version: 8.0.0
Date: 19/03/2025
"""

import os
import sys
import json
import logging
import datetime
from pathlib import Path

# Base path configuration
ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = ROOT_DIR / "core" / "config"
LOGS_DIR = ROOT_DIR / "data" / "logs"

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Logging configuration
log_file = LOGS_DIR / f"system_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("EVA_GUARANI")

class System:
    """Main class of the EVA & GUARANI system"""
    
    def __init__(self, config_path=None):
        """Initializes the EVA & GUARANI system"""
        self.logger = logger
        self.logger.info("✨ Initializing EVA & GUARANI System v8.0.0 ✨")
        
        # Load configuration
        self.config_path = config_path or CONFIG_DIR / "config.json"
        self.config = self._load_config()
        
        # System components
        self.components = {
            "egos": None,
            "atlas": None,
            "nexus": None,
            "cronos": None,
            "ethik": None
        }
        
        # System state
        self.is_running = False
        self.start_time = None
        
        self.logger.info("System initialized successfully")
        
    def _load_config(self):
        """Loads the system configuration file"""
        try:
            self.logger.info(f"Loading configuration from: {self.config_path}")
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.logger.info(f"Configuration loaded: version {config['system']['version']}")
            return config
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            raise

    def _load_component(self, name):
        """Loads a system component"""
        if name not in self.components:
            self.logger.error(f"Unknown component: {name}")
            return False
            
        if not self.config["core"][name]["enabled"]:
            self.logger.info(f"Component {name} is disabled in the configuration")
            return False
            
        try:
            self.logger.info(f"Loading component: {name}")
            # Here the corresponding module would be dynamically imported
            # For now, we just simulate the loading
            self.components[name] = True
            self.logger.info(f"Component {name} loaded successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error loading component {name}: {str(e)}")
            return False

    def start(self):
        """Starts the EVA & GUARANI system"""
        if self.is_running:
            self.logger.warning("System is already running")
            return False
            
        self.logger.info("Starting EVA & GUARANI system")
        
        # Load enabled core components
        for component in self.components:
            self._load_component(component)
            
        self.is_running = True
        self.start_time = datetime.datetime.now()
        
        self.logger.info(f"System started at: {self.start_time}")
        self.print_banner()
        return True
        
    def stop(self):
        """Stops the system execution"""
        if not self.is_running:
            self.logger.warning("System is not running")
            return False
            
        self.logger.info("Stopping EVA & GUARANI system")
        
        # Unload components in reverse order
        for component in reversed(list(self.components.keys())):
            if self.components[component]:
                self.logger.info(f"Unloading component: {component}")
                self.components[component] = None
                
        self.is_running = False
        end_time = datetime.datetime.now()
        duration = end_time - self.start_time
        
        self.logger.info(f"System stopped. Execution time: {duration}")
        return True
        
    def status(self):
        """Returns the current status of the system"""
        status = {
            "system": {
                "name": self.config["system"]["name"],
                "version": self.config["system"]["version"],
                "running": self.is_running,
                "uptime": str(datetime.datetime.now() - self.start_time) if self.is_running else None
            },
            "components": {
                name: {"loaded": bool(component)} 
                for name, component in self.components.items()
            },
            "config": {
                "environment": self.config["system"]["environment"],
                "debug_mode": self.config["system"]["debug_mode"]
            }
        }
        
        return status
        
    def print_banner(self):
        """Displays the system banner"""
        banner = f"""
        ╔════════════════════════════════════════════════════════════╗
        ║                                                            ║
        ║     ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧                           ║
        ║                                                            ║
        ║     Modular Analysis System, Systemic Cartography          ║
        ║              and Quantum Ethics v{self.config["system"]["version"]}                 ║
        ║                                                            ║
        ║     Environment: {self.config["system"]["environment"]}                               ║
        ║     Date: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}                       ║
        ║                                                            ║
        ╚════════════════════════════════════════════════════════════╝
        """
        print(banner)
        self.logger.info("System banner displayed")


def main():
    """Main function to run the EVA & GUARANI system"""
    try:
        # Initialize the system
        system = System()
        
        # Start the system
        system.start()
        
        # Here the main loop or user interface would be implemented
        logger.info("System running. Press Ctrl+C to terminate.")
        
        # Execution simulation for this example
        import time
        try:
            time.sleep(3)  # Simulates the system running
        except KeyboardInterrupt:
            logger.info("User interruption detected")
        
        # Stop the system
        system.stop()
        
        return 0
    except Exception as e:
        logger.critical(f"Fatal error during execution: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())