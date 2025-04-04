#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Initialization Script
====================================

This script sets up the environment and starts the EVA & GUARANI bot.
"""

import os
import sys
import logging
import importlib
import subprocess
import asyncio
from pathlib import Path

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/startup.log", encoding="utf-8"), logging.StreamHandler()],
)

logger = logging.getLogger("startup")
logger_bot = logging.getLogger("bot_package")
logger_bot.setLevel(logging.INFO)


def check_dependencies():
    """Checks and installs necessary dependencies."""
    packages = ["python-telegram-bot", "openai"]

    for package in packages:
        try:
            # For python-telegram-bot, we check the telegram module
            if package == "python-telegram-bot":
                importlib.import_module("telegram")
            else:
                importlib.import_module(package.replace("-", "_"))
            logger.info(f"[OK] Package {package} is already installed")
        except ImportError:
            logger.warning(f"Package {package} not found. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                logger.info(f"[OK] Package {package} installed successfully")
            except subprocess.CalledProcessError:
                logger.error(f"[ERROR] Failed to install {package}")


def setup_environment():
    """Sets up the environment for the bot."""
    # Add the current directory to PYTHONPATH
    current_dir = os.path.abspath(os.path.dirname(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        logger.info(f"[OK] Current directory added to PYTHONPATH: {current_dir}")

    # Create necessary directories
    directories = ["logs", "config", "data", "temp"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"[OK] Directory {directory} checked/created")


async def start_bot():
    """Starts the EVA & GUARANI bot."""
    logger.info("Starting EVA & GUARANI Bot...")

    try:
        logger.info("Attempting to start the bot as a Python module...")
        logger_bot.info("EVA & GUARANI Bot package v8.0 initialized")

        # Check if the main files exist
        bot_file = os.path.join("bot", "unified_telegram_bot_utf8.py")
        eva_file = os.path.join("bot", "eva_guarani_main.py")

        if os.path.exists(bot_file):
            logger_bot.info(f"Bot main file found: {os.path.abspath(bot_file)}")

        if os.path.exists(eva_file):
            logger_bot.info(f"EVA & GUARANI main file found: {os.path.abspath(eva_file)}")

        # Import and execute the main module
        import bot.__main__

        logger.info("[OK] Bot module imported successfully")
        await bot.__main__.main()
    except ImportError as e:
        logger.error(f"[ERROR] Failed to import bot module: {e}")

        # Try to execute the script directly
        try:
            logger.info("Attempting to run the bot script directly...")
            if os.path.exists(bot_file):
                subprocess.run([sys.executable, bot_file])
            else:
                logger.error(f"[ERROR] Bot file not found: {bot_file}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to execute the bot script: {e}")
    except Exception as e:
        logger.error(f"[ERROR] Error starting the bot: {e}")


if __name__ == "__main__":
    print("==================================================")
    print("EVA & GUARANI - System Initialization")
    print("==================================================")

    try:
        setup_environment()
        check_dependencies()
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Initialization interrupted by user")
    except Exception as e:
        logger.error(f"[ERROR] Initialization failed: {e}")
        import traceback

        logger.error(traceback.format_exc())
