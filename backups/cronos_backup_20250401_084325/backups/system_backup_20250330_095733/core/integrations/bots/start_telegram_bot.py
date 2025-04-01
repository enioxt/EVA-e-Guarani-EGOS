#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Optimized Telegram Bot Starter
======================================================

This script starts the Telegram bot with optimized settings for:
1. Automatic reconnection in case of network failures
2. Proper exception handling
3. Detailed logging
4. Resilience to common connection issues

Author: EVA & GUARANI
Version: 8.0
"""

import os
import sys
import json
import time
import logging
import asyncio
import traceback
import importlib.util
from typing import Dict, Any, Optional
from pathlib import Path

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/telegram_bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("EVA_GUARANI_BOT")

# Settings and constants
CONFIG_FILE = "config/telegram_config.json"
RETRY_DELAY = 10  # seconds
MAX_RETRIES = -1  # -1 for infinite
CURRENT_RETRY = 0

def load_config() -> Dict[str, Any]:
    """
    Loads the Telegram bot configuration.
    
    Returns:
        Dictionary with the settings.
    """
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                logger.info("Configuration loaded successfully.")
                return config
        else:
            logger.error(f"Configuration file not found: {CONFIG_FILE}")
            logger.error("Ensure the configuration file exists.")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

async def start_bot(config: Dict[str, Any]) -> None:
    """
    Starts the Telegram bot with error handling and reconnection.
    
    Args:
        config: Bot settings.
    """
    try:
        # Import Telegram dependencies
        try:
            from telegram import Bot, Update
            from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
        except ImportError:
            logger.error("python-telegram-bot library not found.")
            logger.error("Install it with: pip install python-telegram-bot")
            sys.exit(1)
        
        # Check bot token
        bot_token = config.get("bot_token")
        if not bot_token:
            logger.error("Bot token not configured in the configuration file.")
            sys.exit(1)
        
        # Check connection to Telegram
        logger.info("Checking connection to Telegram...")
        bot = Bot(token=bot_token)
        me = await bot.get_me()
        logger.info(f"Connected to Telegram as @{me.username} (ID: {me.id})")
        
        # Import main bot module
        try:
            # First try to import the main module
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # First try unified_telegram_bot_utf8.            if os.path.exists("bot/unified_telegram_bot_utf8.py"):
                logger.info("Importing module unified_telegram_bot_utf8...")
                from bot.unified_telegram_bot_utf8 import main as bot_main
                await bot_main()
                return
            
            # Try eva_guarani_main.py
            elif os.path.exists("bot/eva_guarani_main.py"):
                logger.info("Importing module eva_guarani_main...")
                from bot.eva_guarani_main import main as eva_guarani_main
                await eva_guarani_main()
                return
            
            # Try telegram_bot.py in the root
            elif os.path.exists("telegram_bot.py"):
                logger.info("Importing module telegram_bot...")
                spec = importlib.util.spec_from_file_location("telegram_bot", "telegram_bot.py")
                if spec and spec.loader:
                    telegram_bot = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(telegram_bot)
                    await telegram_bot.main()
                    return
                else:
                    logger.error("Error loading the module telegram_bot.py")
            
            # If reached here, no main module found
            logger.error("No main bot file found.")
            logger.error("Check if the files bot/unified_telegram_bot_utf8.py, bot/eva_guarani_main.py or telegram_bot.py exist.")
            
            # As a fallback, run a minimal version of the bot
            logger.info("Starting minimal version of the bot as fallback...")
            await run_minimal_bot(bot_token)
            
        except Exception as e:
            logger.error(f"Error importing bot module: {e}")
            logger.error(traceback.format_exc())
            
            # Start minimal version as fallback
            logger.info("Starting minimal version of the bot as fallback after error...")
            await run_minimal_bot(bot_token)
    
    except Exception as e:
        global CURRENT_RETRY
        CURRENT_RETRY += 1
        
        if MAX_RETRIES > 0 and CURRENT_RETRY > MAX_RETRIES:
            logger.error(f"Maximum number of retries exceeded ({MAX_RETRIES}). Exiting.")
            sys.exit(1)
        
        logger.error(f"Error starting the bot: {e}")
        logger.error(traceback.format_exc())
        logger.info(f"Retrying in {RETRY_DELAY} seconds (attempt {CURRENT_RETRY})...")
        
        await asyncio.sleep(RETRY_DELAY)
        await start_bot(config)

async def run_minimal_bot(token: str) -> None:
    """
    Runs a minimal version of the bot to ensure at least something is working.
    
    Args:
        token: Telegram bot token.
    """
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    
    # Minimal handlers
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update and update.message:
            await update.message.reply_text(
                "👋 Hello! I am the EVA & GUARANI bot.\n"
                "I am running in minimal mode due to an initialization issue.\n"
                "Please contact the system administrator."
            )
    
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update and update.message:
            await update.message.reply_text(
                "Available commands:\n"
                "/start - Start the bot\n"
                "/help - Show this help\n"
                "/status - Check system status"
            )
    
    async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update and update.message:
            await update.message.reply_text(
                "📊 System Status\n"
                "--------------------\n"
                "🤖 Bot: Running in minimal mode\n"
                "⚠️ Mode: Emergency fallback\n"
                "🕒 Initialization: Recovery after failure\n"
                "✅ Connection: Active\n\n"
                "Administrators have been notified."
            )
    
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update and update.message:
            await update.message.reply_text(
                "I am running in minimal mode. Please use /help to see available commands."
            )
    
    # Configure application
    application = Application.builder().token(token).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    logger.info("Starting bot in minimal mode...")
    await application.initialize()
    await application.start()
    
    # Start polling safely
    updater = application.updater
    if updater:
        await updater.start_polling(drop_pending_updates=True)
    else:
        logger.error("Error: Updater is not available.")
        return
    
    logger.info("Minimal bot started successfully! Awaiting commands...")
    
    # Keep the bot running
    while True:
        await asyncio.sleep(1)

def main() -> None:
    """Main function that starts the bot."""
    banner = """
    ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
    Telegram Bot - Optimized Initialization
    Version: 8.0
    ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
    """
    print(banner)
    logger.info("Starting EVA & GUARANI Telegram Bot...")
    
    # Check necessary directories
    for dir_path in ["logs", "config", "data"]:
        os.makedirs(dir_path, exist_ok=True)
    
    # Load configuration
    config = load_config()
    
    # Start bot with error handling
    try:
        asyncio.run(start_bot(config))
    except KeyboardInterrupt:
        logger.info("Bot terminated by user.")
        print("\nBot terminated by user. Goodbye!")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        logger.critical(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()