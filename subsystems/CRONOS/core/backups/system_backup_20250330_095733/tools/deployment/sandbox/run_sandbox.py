#!/usr/bin/env python3
# ==================================================================
# COMBINED FILE FROM MULTIPLE SIMILAR FILES
# Date: 2025-03-22 08:37:43
# Combined files:
# - deployment\sandbox\run_sandbox.py (kept)
# - sandbox\run_sandbox.py (moved to quarantine)
# ==================================================================

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Script to start the Sandbox environment
This script configures and starts the sandbox environment for experimentation
"""

import os
import sys
import webbrowser
import subprocess
import time
import argparse
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent
API_DIR = BASE_DIR / "api" / "flask_api"
FRONTEND_DIR = BASE_DIR / "frontend" / "html_basic"
PORT = 5000

def check_dependencies():
    """Check if necessary dependencies are installed"""
    try:
        import flask
        print("✓ Flask is installed")
        return True
    except ImportError:
        print("✗ Flask is not installed.")
        print("  Install dependencies with: pip install -r requirements.txt")
        return False

def find_core_modules():
    """Try to locate EVA & GUARANI core modules"""
    # Check if the core directory exists from project root
    project_root = BASE_DIR.parent
    
    # Check if the core folder exists
    core_dir = project_root / "core"
    if not core_dir.exists():
        return None
    
    modules = {
        "atlas": (core_dir / "atlas").exists(),
        "nexus": (core_dir / "nexus").exists(),
        "cronos": (core_dir / "cronos").exists(),
        "ethik": (core_dir / "ethik").exists()
    }
    
    # Count how many modules are available
    available = sum(1 for m in modules.values() if m)
    
    print(f"Modules found: {available}/4")
    for name, exists in modules.items():
        print(f"  {'✓' if exists else '✗'} {name.upper()}")
    
    return core_dir if any(modules.values()) else None

def start_flask_api(debug=False):
    """Start the Flask API"""
    env = os.environ.copy()
    
    # Add project directory to PYTHONPATH if core modules were found
    core_path = find_core_modules()
    if core_path:
        print(f"Core modules found in: {core_path}")
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = f"{core_path.parent};{env['PYTHONPATH']}"
        else:
            env['PYTHONPATH'] = f"{core_path.parent}"
    else:
        print("Core modules not found. Running in simulation mode.")
    
    # Set Flask environment
    env['FLASK_APP'] = str(API_DIR / "app.py")
    if debug:
        env['FLASK_DEBUG'] = "1"
    
    # Command to start Flask
    cmd = [sys.executable, "-m", "flask", "run", "--port", str(PORT)]
    if debug:
        cmd.append("--reload")
    
    # Start Flask process
    print(f"Starting Flask API at http://localhost:{PORT}...")
    return subprocess.Popen(cmd, env=env, cwd=str(API_DIR))

def open_browser():
    """Open browser with sandbox interface"""
    url = f"http://localhost:{PORT}"
    print(f"Opening browser at {url}")
    webbrowser.open(url)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Start the EVA & GUARANI sandbox environment")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    parser.add_argument("--debug", action="store_true", help="Run Flask in debug mode")
    args = parser.parse_args()
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Start Flask server
    flask_process = start_flask_api(debug=args.debug)
    
    # Wait a bit for the server to start
    time.sleep(2)
    
    # Open browser unless --no-browser is specified
    if not args.no_browser:
        open_browser()
    
    try:
        print("\nPress Ctrl+C to stop the server")
        # Keep the script running until user presses Ctrl+C
        flask_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        flask_process.terminate()
        flask_process.wait()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 