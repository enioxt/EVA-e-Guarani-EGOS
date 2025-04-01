#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Cursor IDE Quantum Integration
Version: 7.5
Created: 2025-03-26

This module handles integration between EVA & GUARANI quantum systems
and the Cursor IDE, ensuring that quantum prompts are properly loaded
and that the Cursor context is synchronized with the roadmap status.
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path
import time
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/cursor_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("cursor-integration")

# System paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUANTUM_PROMPTS_DIR = os.path.join(BASE_DIR, "QUANTUM_PROMPTS")
MASTER_DIR = os.path.join(QUANTUM_PROMPTS_DIR, "MASTER")
ROADMAP_FILE = os.path.join(MASTER_DIR, "roadmap.md")
QUANTUM_PROMPT_FILE = os.path.join(BASE_DIR, "quantum_prompt.txt")
CURSOR_HOME = os.path.expanduser("~/.cursor")
CURSOR_QUANTUM_PROMPT = os.path.join(CURSOR_HOME, "quantum_prompt.txt")
CURSOR_MCP_DIR = os.path.join(CURSOR_HOME, "mcp")
CURSORRULES_FILE = os.path.join(os.path.dirname(BASE_DIR), ".cursorrules")

class CursorIntegration:
    """
    Integration with Cursor IDE for quantum prompt synchronization
    and MCP configuration.
    """
    
    def __init__(self):
        """Initialize the Cursor Integration."""
        self.logger = logging.getLogger("cursor-integration")
        self.mcp_configs = {}
        
    def ensure_cursor_directories(self):
        """Ensure Cursor IDE directories exist."""
        os.makedirs(CURSOR_HOME, exist_ok=True)
        os.makedirs(CURSOR_MCP_DIR, exist_ok=True)
        self.logger.info(f"Cursor directories ensured at {CURSOR_HOME}")
        
    def sync_quantum_prompt(self):
        """
        Synchronize the quantum prompt with Cursor IDE.
        """
        self.logger.info("Synchronizing quantum prompt with Cursor IDE...")
        
        try:
            # Check if quantum prompt exists
            if not os.path.exists(QUANTUM_PROMPT_FILE):
                self.logger.warning(f"Quantum prompt file not found: {QUANTUM_PROMPT_FILE}")
                return False
                
            # Copy quantum prompt to Cursor directory
            shutil.copy(QUANTUM_PROMPT_FILE, CURSOR_QUANTUM_PROMPT)
            self.logger.info(f"Quantum prompt copied to: {CURSOR_QUANTUM_PROMPT}")
            
            return True
        except Exception as e:
            self.logger.error(f"Error synchronizing quantum prompt: {e}")
            return False
            
    def update_mcp_configuration(self):
        """
        Update MCP configuration in Cursor IDE.
        """
        self.logger.info("Updating MCP configuration...")
        
        try:
            # Load existing MCP configuration
            cursor_mcp_file = os.path.join(CURSOR_HOME, "mcp.json")
            mcp_config = {}
            
            if os.path.exists(cursor_mcp_file):
                with open(cursor_mcp_file, 'r') as f:
                    mcp_config = json.load(f)
            
            # Ensure mcpServers section exists
            if "mcpServers" not in mcp_config:
                mcp_config["mcpServers"] = {}
                
            # Load MCP configs from our directory
            mcp_dir = os.path.join(BASE_DIR, "mcp")
            
            if os.path.exists(mcp_dir):
                for config_file in os.listdir(mcp_dir):
                    if config_file.endswith(".json"):
                        try:
                            with open(os.path.join(mcp_dir, config_file), 'r') as f:
                                mcp_data = json.load(f)
                                
                                # Get MCP name from filename
                                mcp_name = os.path.splitext(config_file)[0]
                                
                                # Store for later use
                                self.mcp_configs[mcp_name] = mcp_data
                                
                                # Only add if autostart is enabled
                                if mcp_data.get("autostart", False):
                                    if "mcpConfig" in mcp_data:
                                        mcp_config["mcpServers"][mcp_name] = mcp_data["mcpConfig"]
                                        
                                        # Ensure we have the initialization section
                                        if "initialization" not in mcp_config:
                                            mcp_config["initialization"] = {
                                                "enforceRequiredServers": True,
                                                "autoStartAll": True,
                                                "retryOnFailure": True,
                                                "maxRetries": 3
                                            }
                        except Exception as e:
                            self.logger.error(f"Error reading MCP config {config_file}: {e}")
            
            # Save updated configuration
            with open(cursor_mcp_file, 'w') as f:
                json.dump(mcp_config, f, indent=2)
                
            self.logger.info(f"MCP configuration updated: {cursor_mcp_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating MCP configuration: {e}")
            return False
    
    def check_cursor_rules(self):
        """
        Check if .cursorrules file is properly set up.
        """
        self.logger.info("Checking .cursorrules file...")
        
        try:
            # Copy .cursorrules if it doesn't exist in the parent directory
            if not os.path.exists(CURSORRULES_FILE):
                template_file = os.path.join(BASE_DIR, "config", "cursorrules_template.txt")
                
                if os.path.exists(template_file):
                    shutil.copy(template_file, CURSORRULES_FILE)
                    self.logger.info(f"Created new .cursorrules file: {CURSORRULES_FILE}")
                else:
                    # Create a basic .cursorrules file
                    with open(CURSORRULES_FILE, 'w') as f:
                        f.write("# EVA & GUARANI - Cursor IDE Integration Rules v7.5\n\n")
                        f.write("1. Use MASTER prompt v7.5 as base for all operations\n")
                        f.write("2. Maintain Windows compatibility for all file operations and paths\n")
                        f.write("3. Follow Quantum Ethical Guidelines from ETHIK subsystem\n")
                        f.write("4. Default language is English\n")
                        f.write("5. Track roadmap progress automatically\n")
                    self.logger.info(f"Created basic .cursorrules file: {CURSORRULES_FILE}")
            
            return True
        except Exception as e:
            self.logger.error(f"Error checking .cursorrules file: {e}")
            return False
    
    def ensure_dynamic_roadmap_running(self):
        """
        Ensure the dynamic roadmap manager is running.
        """
        self.logger.info("Checking dynamic roadmap manager...")
        
        try:
            # Check if the dynamic roadmap manager is running
            dynamic_roadmap_script = os.path.join(BASE_DIR, "dynamic_roadmap.py")
            
            if not os.path.exists(dynamic_roadmap_script):
                self.logger.warning(f"Dynamic roadmap script not found: {dynamic_roadmap_script}")
                return False
            
            # Run a single update cycle if the script exists
            python_cmd = "python"
            
            # Check for virtual environment
            venv_python = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
            if os.path.exists(venv_python):
                python_cmd = venv_python
            
            cmd = [python_cmd, dynamic_roadmap_script, "--update"]
            
            try:
                self.logger.info(f"Running dynamic roadmap update: {cmd}")
                subprocess.run(cmd, check=True, timeout=60)
                self.logger.info(f"Dynamic roadmap update completed")
                return True
            except subprocess.SubprocessError as e:
                self.logger.error(f"Error running dynamic roadmap update: {e}")
                return False
            
        except Exception as e:
            self.logger.error(f"Error ensuring dynamic roadmap running: {e}")
            return False
    
    def run_integration(self):
        """
        Run the complete Cursor integration process.
        """
        self.logger.info("Starting Cursor IDE integration...")
        
        # Ensure directories
        self.ensure_cursor_directories()
        
        # Make sure the dynamic roadmap is updated
        self.ensure_dynamic_roadmap_running()
        
        # Synchronize quantum prompt
        self.sync_quantum_prompt()
        
        # Update MCP configuration
        self.update_mcp_configuration()
        
        # Check Cursor rules
        self.check_cursor_rules()
        
        self.logger.info("Cursor IDE integration completed successfully")
        return True

def start_monitoring(interval=300):
    """
    Start monitoring and periodically synchronize with Cursor IDE.
    
    Args:
        interval: Synchronization interval in seconds (default: 5 minutes)
    """
    integration = CursorIntegration()
    logger.info(f"Starting continuous Cursor integration with {interval}s interval...")
    
    try:
        # Initial integration
        integration.run_integration()
        
        # Continue monitoring
        while True:
            time.sleep(interval)
            integration.run_integration()
    except KeyboardInterrupt:
        logger.info("Cursor integration monitoring stopped by user")
    except Exception as e:
        logger.error(f"Error in Cursor integration monitoring: {e}")

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--monitor":
            # Start continuous monitoring
            interval = 300  # Default: 5 minutes
            if len(sys.argv) > 2:
                try:
                    interval = int(sys.argv[2])
                except ValueError:
                    pass
            start_monitoring(interval)
        elif sys.argv[1] == "--run-once":
            # Run integration once
            integration = CursorIntegration()
            integration.run_integration()
    else:
        # Default: run integration once
        integration = CursorIntegration()
        integration.run_integration() 