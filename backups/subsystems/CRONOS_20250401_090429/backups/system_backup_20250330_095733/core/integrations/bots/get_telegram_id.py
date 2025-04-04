#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Obtain Telegram ID
This script helps to obtain the user's ID on Telegram.
"""

import os
import sys
import json
import logging
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/get_id.log"), logging.StreamHandler()],
)
logger = logging.getLogger("get_id")

# Load configuration
CONFIG_PATH = os.path.join("config", "eva_guarani_config.json")


def load_config():
    """Loads the bot configuration."""
    try:
        if not os.path.exists(CONFIG_PATH):
            logger.error(f"Configuration file not found: {CONFIG_PATH}")
            return None

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the /start command is issued."""
    user = update.effective_user
    user_id = user.id
    username = user.username or "No username"
    first_name = user.first_name or "No name"

    await update.message.reply_text(
        f"Hello, {first_name}!\n\n"
        f"Your Telegram ID is: {user_id}\n"
        f"Your username is: @{username}\n\n"
        "Add this ID to the config/eva_guarani_config.json file in the 'admin_users' list."
    )

    logger.info(f"User ID {first_name} (@{username}): {user_id}")


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the user's ID when the /id command is issued."""
    user = update.effective_user
    user_id = user.id

    await update.message.reply_text(f"Your Telegram ID is: {user_id}")
    logger.info(f"User ID requested: {user_id}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes text messages."""
    user = update.effective_user
    user_id = user.id

    await update.message.reply_text(
        f"Your Telegram ID is: {user_id}\n\n"
        "Use this ID in the config/eva_guarani_config.json file in the 'admin_users' list."
    )
    logger.info(f"User ID sent in response to message: {user_id}")


async def main() -> None:
    """Main function."""
    # Load configuration
    config = load_config()
    if not config:
        logger.error("Failed to load configuration. Exiting.")
        return

    # Get bot token
    bot_token = config.get("telegram", {}).get("bot_token") or config.get("bot_token")
    if not bot_token:
        logger.error("Bot token not found in configuration.")
        return

    # Create application
    application = Application.builder().token(bot_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("id", get_id))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start bot
    print("ID retrieval bot started. Send /start or /id on Telegram.")
    print(f"Bot token: {bot_token}")

    await application.initialize()
    await application.start()

    try:
        # Keep the bot running until Ctrl+C
        await asyncio.Event().wait()
    finally:
        await application.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        logger.error(f"Error running the bot: {e}")
        import traceback

        traceback.print_exc()
