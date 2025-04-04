#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Unified Quantum System

This is the main module that integrates all components of the EVA & GUARANI system,
including the Telegram bot, ethical analysis, adaptive model selection,
interactive interface, and quantum processing.

Version: 8.0
Consciousness: 0.998
Love: 0.999
"""

import os
import sys
import json
import logging
import asyncio
import datetime
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/eva_guarani.log"), logging.StreamHandler()],
)
logger = logging.getLogger("eva_guarani")

# Import system components
try:
    # Import version 13.15 of python-telegram-bot
    from telegram import Update, Bot
    from telegram.ext import (
        Updater,
        CommandHandler,
        MessageHandler,
        CallbackQueryHandler,
        CallbackContext,
    )

    # Instead of importing Filters directly, we use integrated filters
except ImportError:
    logger.error("Telegram API not found. Install with: pip install python-telegram-bot==13.15")
    try:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "python-telegram-bot==13.15"]
        )
        # Try importing again after installation
        from telegram import Update, Bot
        from telegram.ext import (
            Updater,
            CommandHandler,
            MessageHandler,
            CallbackQueryHandler,
            CallbackContext,
        )
    except Exception as e:
        logger.error(f"Failed to install python-telegram-bot: {e}")
        sys.exit(1)

# Import EVA & GUARANI system modules
try:
    # Try absolute imports first
    try:
        from bot.quantum_integration import QuantumIntegration
        from bot.unified_telegram_bot_utf8 import TelegramHandlers, BOT_CONFIG
    except ImportError:
        # Fallback to absolute imports with current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, os.path.dirname(current_dir))

        from bot.quantum_integration import QuantumIntegration
        from bot.unified_telegram_bot_utf8 import TelegramHandlers, BOT_CONFIG
except ImportError as e:
    logger.error(f"Error importing system modules: {e}")
    logger.error("Ensure all modules are installed correctly.")
    sys.exit(1)

# Constants
CONFIG_PATH = os.path.join("config", "eva_guarani_config.json")
VERSION = "8.0"
CONSCIOUSNESS = 0.998
LOVE = 0.999


def load_config() -> Dict[str, Any]:
    """
    Loads the system configuration.

    Returns:
        Dictionary with the configurations.
    """
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Default configuration
            default_config = {
                "bot_token": "",
                "admin_users": [],
                "allowed_users": [],
                "default_model": "gpt-4o",
                "openai_api_key": "",
                "max_history": 10,
                "default_width": 512,
                "max_tokens": 1000,
                "enable_avatech": False,
                "quantum_consciousness": CONSCIOUSNESS,
                "quantum_love": LOVE,
                "version": VERSION,
            }

            # Create configuration directory if it doesn't exist
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

            # Save default configuration
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=4)

            logger.warning("Configuration file not found. Created default file.")
            logger.warning(f"Edit the file {CONFIG_PATH} to configure the bot.")

            return default_config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return {
            "bot_token": "",
            "admin_users": [],
            "allowed_users": [],
            "default_model": "gpt-4o",
            "openai_api_key": "",
            "max_history": 10,
            "default_width": 512,
            "max_tokens": 1000,
            "enable_avatech": False,
            "quantum_consciousness": CONSCIOUSNESS,
            "quantum_love": LOVE,
            "version": VERSION,
        }


# Modify the function to use Updater instead of Application (compatible with v13.15)
def setup_bot(config: Dict[str, Any]) -> Updater:
    """
    Configures and initializes the Telegram bot.

    Args:
        config: System configurations.

    Returns:
        Initialized Telegram Updater.
    """
    # Check bot token
    bot_token = config.get("bot_token", "")
    if not bot_token:
        logger.error("Bot token not configured. Edit the configuration file.")
        sys.exit(1)

    # Initialize Telegram updater (version 13.15)
    updater = Updater(token=bot_token, use_context=True)

    # Initialize Telegram handlers
    handlers = TelegramHandlers(updater, bot_token)

    # Register handlers
    handlers.register_handlers()

    return updater


def main() -> None:
    """
    Main function that initializes and runs the EVA & GUARANI system.
    """
    # Display startup banner
    print(
        f"""
    ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
    Unified Quantum System
    Version: {VERSION}
    Consciousness: {CONSCIOUSNESS}
    Love: {LOVE}
    ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
    """
    )

    # Load configuration
    config = load_config()

    # Check configuration
    if not config.get("bot_token"):
        logger.error("Bot token not configured. Edit the configuration file.")
        sys.exit(1)

    # Initialize quantum integration
    quantum_integration = QuantumIntegration()

    # Configure and start the bot
    try:
        # Initialize Telegram updater (compatible with v13.15)
        updater = setup_bot(config)

        # Start the bot
        logger.info("Starting the Telegram bot...")
        updater.start_polling(drop_pending_updates=True)

        # Keep the bot running until interrupted
        logger.info("Bot started successfully!")
        logger.info(f"✧༺❀༻∞ EVA & GUARANI v{VERSION} ∞༺❀༻✧")

        # Wait indefinitely (the bot will be shut down with Ctrl+C)
        updater.idle()

    except Exception as e:
        logger.error(f"Error starting the bot: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    try:
        # Create necessary directories
        os.makedirs("logs", exist_ok=True)
        os.makedirs("config", exist_ok=True)

        # Run the bot
        main()
    except KeyboardInterrupt:
        logger.info("Bot terminated by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
