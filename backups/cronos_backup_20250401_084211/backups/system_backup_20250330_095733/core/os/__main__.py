#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Main Entry Point
This file serves as the main entry point for the bot when executed as a Python module.
Usage example: python -m bot
"""

import os
import sys
import asyncio
import logging
import traceback
from datetime import datetime

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/main_execution.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("bot_main")

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Add the parent directory to the path to allow relative imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    logger.info(f"Added parent directory to path: {parent_dir}")

# Initialization banner
def print_banner():
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║     ███████╗██╗   ██╗ █████╗      ██████╗                 ║
    ║     ██╔════╝██║   ██║██╔══██╗    ██╔════╝                 ║
    ║     █████╗  ██║   ██║███████║    ██║  ███╗                ║
    ║     ██╔══╝  ╚██╗ ██╔╝██╔══██║    ██║   ██║                ║
    ║     ███████╗ ╚████╔╝ ██║  ██║    ╚██████╔╝                ║
    ║     ╚══════╝  ╚═══╝  ╚═╝  ╚═╝     ╚═════╝                 ║
    ║                                                            ║
    ║     ██████╗ ██╗   ██╗ █████╗ ██████╗  █████╗ ███╗   ██╗   ║
    ║    ██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗████╗  ██║   ║
    ║    ██║  ███╗██║   ██║███████║██████╔╝███████║██╔██╗ ██║   ║
    ║    ██║   ██║██║   ██║██╔══██║██╔══██╗██╔══██║██║╚██╗██║   ║
    ║    ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║  ██║██║ ╚████║   ║
    ║     ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ║
    ║                                                            ║
    ║                 UNIFIED TELEGRAM BOT                       ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    logger.info("Starting EVA & GUARANI - UNIFIED TELEGRAM BOT")
    print(banner)

# Main function
async def main():
    print_banner()
    
    logger.info("Checking main bot files...")
    
    # Check if the eva_guarani_main.py file exists
    eva_guarani_file = os.path.join(os.path.dirname(__file__), "eva_guarani_main.py")
    if os.path.exists(eva_guarani_file):
        logger.info(f"EVA & GUARANI main file found: {eva_guarani_file}")
        try:
            logger.info("Importing module eva_guarani_main...")
            from bot.eva_guarani_main import main as eva_guarani_main
            logger.info("Running EVA & GUARANI main...")
            await eva_guarani_main()
            return
        except ImportError as e:
            logger.error(f"Error importing eva_guarani_main: {e}")
            traceback.print_exc()
    else:
        logger.warning(f"EVA & GUARANI main file not found: {eva_guarani_file}")
    
    # If not found or failed, try unified_telegram_bot_utf8.    bot_file = os.path.join(os.path.dirname(__file__), "unified_telegram_bot_utf8.py")
    if os.path.exists(bot_file):
        logger.info(f"Main bot file found: {bot_file}")
        try:
            logger.info("Importing module unified_telegram_bot_utf8...")
            from bot.unified_telegram_bot_utf8 import main as bot_main
            logger.info("Running main bot...")
            await bot_main()
            return
        except ImportError as e:
            logger.error(f"Error importing unified_telegram_bot_utf8: {e}")
            traceback.print_exc()
    else:
        logger.error(f"Main bot file not found: {bot_file}")
        print("ERROR: Could not find the main bot files.")
        print("Check if the files are present in the 'bot' directory.")
        return

# Entry point
if __name__ == "__main__":
    try:
        logger.info("Starting asyncio event loop...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
        print("\nBot interrupted by user. Goodbye!")
    except Exception as e:
        logger.critical(f"Fatal error during bot execution: {e}")
        traceback.print_exc()
        print(f"\nFATAL ERROR: {e}")
        print("Check the logs for more details.")