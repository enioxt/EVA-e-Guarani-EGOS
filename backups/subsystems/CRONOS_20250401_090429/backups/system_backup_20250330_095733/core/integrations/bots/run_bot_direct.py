#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Direct Telegram Bot Runner
=========================================

Simple script to run the Telegram bot directly.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0.0
"""

import os
import sys
import subprocess
import logging
import importlib

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("direct_bot_runner")


def install_package(package):
    """Install a package using pip"""
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print(f"Successfully installed {package}")


# First, install required packages
try:
    install_package("python-telegram-bot==13.15")
    install_package("requests")
    install_package("openai")
except Exception as e:
    print(f"Error installing packages: {e}")
    print("Please install them manually and try again.")
    sys.exit(1)

# Set up the paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))

# Add to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

tools_path = os.path.join(project_root, "tools", "utilities")
if tools_path not in sys.path:
    sys.path.insert(0, tools_path)

modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

quantum_path = os.path.join(project_root, "modules", "quantum")
if quantum_path not in sys.path:
    sys.path.insert(0, quantum_path)

# Create necessary directories
os.makedirs(os.path.join(current_dir, "logs"), exist_ok=True)
os.makedirs(os.path.join(project_root, "data", "payments"), exist_ok=True)

# Change to the current directory
os.chdir(current_dir)

print("\n✧༺❀༻∞ EVA & GUARANI - Direct Telegram Bot Runner ∞༺❀༻✧\n")
print("Starting EVA & GUARANI Telegram Bot (avatechartbot)...")
print("Bot logs will be saved to: logs/telegram_bot.log")
print("Press Ctrl+C to stop the bot.")
print()

# Try to import and run the bot
try:
    # Force reimport of telegram module
    if "telegram" in sys.modules:
        del sys.modules["telegram"]

    # Validate python-telegram-bot is properly installed
    import telegram

    print(f"Using python-telegram-bot version: {telegram.__version__}")

    # Execute the simple_telegram_bot.py directly
    bot_script_path = os.path.join(current_dir, "simple_telegram_bot.py")

    with open(bot_script_path, "r", encoding="utf-8") as f:
        bot_code = f.read()

    # Execute the script
    print("Executing bot script...")
    exec(bot_code)

except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all dependencies are properly installed.")
    sys.exit(1)
except Exception as e:
    print(f"Error running the bot: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n✧༺❀༻∞ Bot execution ended ∞༺❀༻✧\n")
