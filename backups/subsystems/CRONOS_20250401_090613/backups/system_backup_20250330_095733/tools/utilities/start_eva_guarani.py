#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Initialization Script
This script starts the Telegram bot and ensures it keeps running.
"""

import os
import sys
import time
import json
import logging
import subprocess
import signal
import argparse
from datetime import datetime

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/startup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("startup")

# Load configuration
CONFIG_PATH = os.path.join("config", "eva_guarani_config.json")

def load_config():
    """Loads the bot configuration."""
    try:
        if not os.path.exists(CONFIG_PATH):
            logger.error(f"Configuration file not found: {CONFIG_PATH}")
            return None
        
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return None

def check_dependencies():
    """Checks if all dependencies are installed."""
    required_packages = [
        "python-telegram-bot",
        "openai",
        "pillow",
        "requests",
        "psutil"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(packages):
    """Installs missing dependencies."""
    try:
        for package in packages:
            logger.info(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except Exception as e:
        logger.error(f"Error installing dependencies: {e}")
        return False

def is_bot_running():
    """Checks if the bot is already running."""
    try:
        import psutil
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and any('unified_telegram_bot' in cmd for cmd in cmdline if cmd):
                    return True, proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return False, None
    except ImportError:
        logger.warning("psutil module not found. Cannot check processes.")
        return False, None
    except Exception as e:
        logger.error(f"Error checking processes: {e}")
        return False, None

def start_bot(detached=True):
    """Starts the Telegram bot."""
    try:
        bot_script = os.path.join("bot", "unified_telegram_bot_utf8.py")
        
        if not os.path.exists(bot_script):
            logger.error(f"Bot script not found: {bot_script}")
            return False, None
        
        logger.info(f"Starting bot: {bot_script}")
        
        if detached:
            # Start in detached mode (background)
            if sys.platform == 'win32':
                # On Windows, use 'start' command to open in a new window
                # Ensure paths with spaces are handled correctly
                python_exe = f'"{sys.executable}"'
                bot_script_path = f'"{bot_script}"'
                process = subprocess.Popen(
                    f'start "EVA & GUARANI Bot" /min {python_exe} {bot_script_path}',
                    shell=True
                )
                return True, process.pid
            else:
                # On Linux/Mac, use nohup to run in background
                log_file = os.path.join("logs", "bot_output.log")
                python_exe = f'"{sys.executable}"'
                bot_script_path = f'"{bot_script}"'
                process = subprocess.Popen(
                    f'nohup {python_exe} {bot_script_path} > "{log_file}" 2>&1 &',
                    shell=True,
                    preexec_fn=os.setpgrp
                )
                return True, process.pid
        else:
            # Start in attached mode (foreground)
            process = subprocess.Popen([sys.executable, bot_script])
            return True, process.pid
    
    except Exception as e:
        logger.error(f"Error starting the bot: {e}")
        return False, None

def stop_bot():
    """Stops the Telegram bot if it is running."""
    try:
        import psutil
        
        running, pid = is_bot_running()
        
        if running and pid:
            logger.info(f"Stopping bot with PID {pid}...")
            
            try:
                process = psutil.Process(pid)
                process.terminate()
                
                # Wait up to 5 seconds for the process to terminate
                process.wait(timeout=5)
                logger.info(f"Bot stopped successfully.")
                return True
            except psutil.NoSuchProcess:
                logger.info(f"Process {pid} no longer exists.")
                return True
            except psutil.TimeoutExpired:
                logger.warning(f"Timeout waiting for process to terminate. Forcing...")
                process.kill()
                return True
            except Exception as e:
                logger.error(f"Error stopping process {pid}: {e}")
                return False
        else:
            logger.info("Bot is not running.")
            return True
    
    except ImportError:
        logger.warning("psutil module not found. Cannot stop the bot.")
        return False
    except Exception as e:
        logger.error(f"Error stopping the bot: {e}")
        return False

def restart_bot(detached=True):
    """Restarts the Telegram bot."""
    stop_bot()
    time.sleep(2)  # Wait a bit to ensure the previous process has terminated
    return start_bot(detached)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Start the EVA & GUARANI bot')
    parser.add_argument('--restart', action='store_true', help='Restart the bot if it is already running')
    parser.add_argument('--stop', action='store_true', help='Stop the bot if it is running')
    parser.add_argument('--foreground', action='store_true', help='Run the bot in the foreground')
    args = parser.parse_args()
    
    print("=" * 50)
    print("EVA & GUARANI - Initialization System")
    print("=" * 50)
    
    # Check if the bot should be stopped
    if args.stop:
        print("Stopping the bot...")
        if stop_bot():
            print("✅ Bot stopped successfully.")
        else:
            print("❌ Failed to stop the bot.")
        return
    
    # Check dependencies
    print("\nChecking dependencies...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"⚠️ Missing dependencies: {', '.join(missing_packages)}")
        print("Installing dependencies...")
        
        if install_dependencies(missing_packages):
            print("✅ Dependencies installed successfully.")
        else:
            print("❌ Failed to install dependencies.")
            return
    else:
        print("✅ All dependencies are installed.")
    
    # Check configuration
    print("\nChecking configuration...")
    config = load_config()
    
    if not config:
        print("❌ Failed to load configuration.")
        return
    
    print("✅ Configuration loaded successfully.")
    
    # Check if the bot is already running
    print("\nChecking if the bot is already running...")
    running, pid = is_bot_running()
    
    if running:
        print(f"⚠️ Bot is already running (PID: {pid}).")
        
        if args.restart:
            print("Restarting the bot...")
            success, new_pid = restart_bot(not args.foreground)
            
            if success:
                print(f"✅ Bot restarted successfully (New PID: {new_pid}).")
            else:
                print("❌ Failed to restart the bot.")
        else:
            print("Use --restart to force a restart.")
    else:
        print("Bot is not running. Starting...")
        success, new_pid = start_bot(not args.foreground)
        
        if success:
            print(f"✅ Bot started successfully (PID: {new_pid}).")
            
            if not args.foreground:
                print("\nThe bot is running in the background.")
                print("To check the status: python check_bot_status.py")
                print("To stop the bot: python start_eva_guarani.py --stop")
        else:
            print("❌ Failed to start the bot.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()