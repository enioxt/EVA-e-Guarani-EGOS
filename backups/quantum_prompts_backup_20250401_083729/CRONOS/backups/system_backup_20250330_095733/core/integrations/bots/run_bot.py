#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Telegram Bot Runner
===================================

Script to run the EVA & GUARANI Telegram bot (avatechartbot).
This script helps set up the environment and run the bot.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0.0
"""

import os
import sys
import subprocess
import importlib.util
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("bot_runner")


def ensure_dependencies():
    """Ensure required dependencies are installed"""
    required_packages = ["python-telegram-bot==13.15", "requests", "openai"]

    for package in required_packages:
        package_name = package.split("==")[0]
        try:
            importlib.util.find_spec(package_name)
            logger.info(f"✅ {package_name} is already installed")
        except ImportError:
            logger.warning(f"⚠️ {package_name} not found, installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                logger.info(f"✅ {package_name} installed successfully")
            except Exception as e:
                logger.error(f"❌ Error installing {package_name}: {e}")
                return False

    return True


def setup_environment():
    """Setup the environment for the bot"""
    # Get script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../.."))

    # Add necessary directories to Python path
    sys.path.append(project_root)
    sys.path.append(os.path.join(project_root, "modules"))
    sys.path.append(os.path.join(project_root, "modules/quantum"))
    sys.path.append(os.path.join(project_root, "tools/utilities"))

    # Create necessary directories
    os.makedirs(os.path.join(script_dir, "logs"), exist_ok=True)
    os.makedirs(os.path.join(project_root, "data/payments"), exist_ok=True)

    # Change to script directory
    os.chdir(script_dir)

    return True


def run_bot():
    """Run the Telegram bot"""
    try:
        # Import the bot module
        from simple_telegram_bot import main

        # Run the bot
        main()

        return True
    except ImportError:
        logger.error("❌ Could not import the bot module. Make sure simple_telegram_bot.py exists.")
        return False
    except Exception as e:
        logger.error(f"❌ Error running the bot: {e}")
        return False


def main():
    """Main function"""
    print("\n✧༺❀༻∞ EVA & GUARANI - Telegram Bot Runner ∞༺❀༻✧\n")

    # Ensure dependencies
    if not ensure_dependencies():
        logger.error("Failed to ensure dependencies. Please install them manually.")
        return

    # Setup environment
    if not setup_environment():
        logger.error("Failed to setup environment.")
        return

    # Print bot information
    print("Starting EVA & GUARANI Telegram Bot (avatechartbot)...")
    print("Bot logs will be saved to: logs/telegram_bot.log")
    print("Press Ctrl+C to stop the bot.")
    print()

    # Run the bot
    run_bot()

    print("\n✧༺❀༻∞ Bot execution ended ∞༺❀༻✧\n")


if __name__ == "__main__":
    main()
