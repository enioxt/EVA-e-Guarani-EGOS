#!/usr/bin/env python3
python
"""
Configuration module for secure credential management - EVA & GUARANI
-------------------------------------------------------------------------------
This module manages API keys and other external service configurations,
prioritizing the security and concealment of credentials.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    """
    Manages configurations and credentials for the EVA & GUARANI system.
    Prioritizes the security of API keys and other sensitive credentials.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initializes the configuration manager.
        
        Args:
            config_path: Path to the configuration file. If None,
                         uses the default within the EGOS directory.
        """
        if config_path is None:
            # Default directory for configurations
            egos_dir = Path(__file__).parent.parent
            self.config_path = egos_dir / "config" / "api_keys.json"
        else:
            self.config_path = Path(config_path)
            
        # Create configuration directory if it does not exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initial configurations
        self.config = self._load_config()
        
        # Perplexity key - prioritizes environment variable, then file
        perplexity_key = os.environ.get("PERPLEXITY_API_KEY")
        if perplexity_key:
            self.set_key("perplexity", perplexity_key)
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Loads configurations from the file if it exists.
        
        Returns:
            Dictionary with configurations
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error loading configuration file: {self.config_path}")
                return {"api_keys": {}}
        else:
            return {"api_keys": {}}
    
    def _save_config(self) -> None:
        """Saves the configurations to the file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_key(self, service: str) -> Optional[str]:
        """
        Obtains the API key for a specific service.
        
        Args:
            service: Name of the service (e.g., 'perplexity', 'openai')
            
        Returns:
            API key or None if not found
        """
        # First try to get from the environment variable
        env_key = os.environ.get(f"{service.upper()}_API_KEY")
        if env_key:
            return env_key
            
        # If not found in the environment, search in the configuration file
        return self.config.get("api_keys", {}).get(service)
    
    def set_key(self, service: str, api_key: str) -> None:
        """
        Sets the API key for a service.
        
        Args:
            service: Name of the service (e.g., 'perplexity', 'openai')
            api_key: API key to store
        """
        if "api_keys" not in self.config:
            self.config["api_keys"] = {}
            
        self.config["api_keys"][service] = api_key
        self._save_config()
        
    def clear_key(self, service: str) -> None:
        """
        Removes the API key for a service.
        
        Args:
            service: Name of the service (e.g., 'perplexity', 'openai')
        """
        if service in self.config.get("api_keys", {}):
            del self.config["api_keys"][service]
            self._save_config()
            
    def is_configured(self, service: str) -> bool:
        """
        Checks if the service is configured with an API key.
        
        Args:
            service: Name of the service (e.g., 'perplexity', 'openai')
            
        Returns:
            True if the service has a configured API key
        """
        # Check environment first
        env_key = os.environ.get(f"{service.upper()}_API_KEY")
        if env_key:
            return True
            
        # Then check the file
        return service in self.config.get("api_keys", {})


# Global instance of the configuration manager
config_manager = ConfigManager()

# Usage example:
if __name__ == "__main__":
    # This block only executes if the file is run directly
    
    # Configure Perplexity API key (example only)
    sample_key = "pplx-sample-key-for-testing"
    config_manager.set_key("perplexity", sample_key)
    
    # Check if configured
    if config_manager.is_configured("perplexity"):
        print("Perplexity API is configured.")
    else:
        print("Perplexity API is NOT configured.")