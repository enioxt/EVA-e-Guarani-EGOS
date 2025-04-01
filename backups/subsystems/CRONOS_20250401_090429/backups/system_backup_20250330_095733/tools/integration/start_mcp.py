#!/usr/bin/env python3
import os
import sys
import subprocess
import logging
from pathlib import Path

def setup_logging():
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    log_file = log_dir / "mcp_service.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return log_file

def start_mcp_service():
    try:
        # Setup logging
        log_file = setup_logging()
        logging.info("Starting MCP Service...")
        
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent
        
        # Activate virtual environment if it exists
        venv_activate = project_root / "venv" / "Scripts" / "activate.bat"
        if venv_activate.exists():
            logging.info("Activating virtual environment...")
            subprocess.run([str(venv_activate)], shell=True, check=True)
        
        # Install required packages
        logging.info("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "websockets", "python-dotenv", "aiohttp"], check=True)
        
        # Start the MCP server
        logging.info("Starting MCP server...")
        server_process = subprocess.Popen(
            [sys.executable, "-m", "tools.integration.mcp_server"],
            stdout=open(log_file, 'a', encoding='utf-8'),
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        
        logging.info(f"MCP service started successfully. Process ID: {server_process.pid}")
        logging.info(f"Logs will be written to: {log_file}")
        
        # Keep the script running
        server_process.wait()
        
    except Exception as e:
        logging.error(f"Error starting MCP service: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_mcp_service() 