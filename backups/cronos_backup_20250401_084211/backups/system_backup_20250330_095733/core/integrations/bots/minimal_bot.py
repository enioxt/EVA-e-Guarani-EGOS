#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Minimal Telegram Bot
====================================

A minimal implementation of the Telegram bot for testing.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0.0
"""

import os
import sys
import json
import logging
import datetime

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("minimal_bot")

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.append(project_root)

# Create logs directory
logs_dir = os.path.join(current_dir, "logs")
os.makedirs(logs_dir, exist_ok=True)

# Load configuration
config_path = os.path.join(current_dir, "telegram_config.json")
try:
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    token = config.get("token", "")
    bot_name = config.get("bot_name", "avatechartbot")

    if not token:
        logger.error("Bot token not configured in telegram_config.json")
        sys.exit(1)

    logger.info(f"Loaded configuration for bot: {bot_name}")

except Exception as e:
    logger.error(f"Error loading config: {e}")
    sys.exit(1)

# Try to import Telegram
try:
    from telegram import Bot, Update, ParseMode
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

    logger.info("Successfully imported python-telegram-bot")
except ImportError:
    logger.error(
        "Failed to import python-telegram-bot. Please install it: pip install python-telegram-bot==13.15"
    )
    sys.exit(1)


def start_command(update: Update, context: CallbackContext):
    """Handle the /start command"""
    if update.effective_chat:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f"Hello! I'm *{bot_name}*, the EVA & GUARANI AI assistant.\n\n"
                "I'm running in minimal mode for testing.\n\n"
                "Commands:\n"
                "• /start - Show this message\n"
                "• /status - Show bot status\n\n"
                "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            ),
            parse_mode=ParseMode.MARKDOWN,
        )


def status_command(update: Update, context: CallbackContext):
    """Handle the /status command"""
    if update.effective_chat:
        uptime = datetime.datetime.now() - start_time
        days, seconds = uptime.days, uptime.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f"🤖 *{bot_name} Status* 🤖\n\n"
                f"• Mode: Minimal (Testing)\n"
                f"• Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"• Uptime: {days}d {hours}h {minutes}m {seconds}s\n\n"
                f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            ),
            parse_mode=ParseMode.MARKDOWN,
        )


def text_message(update: Update, context: CallbackContext):
    """Handle text messages"""
    if update.effective_chat and update.message and update.message.text:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "I received your message, but I'm currently running in minimal mode for testing.\n\n"
                "Please use /start or /status to interact with me.\n\n"
                "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            ),
        )


def main():
    """Main function to run the bot"""
    global start_time
    start_time = datetime.datetime.now()

    print("\n✧༺❀༻∞ EVA & GUARANI - Minimal Telegram Bot ∞༺❀༻✧\n")
    print(f"Starting minimal bot: {bot_name}")
    print(f"Token: {token[:6]}...{token[-4:]}")
    print("Press Ctrl+C to stop the bot.")
    print()

    # Create the Updater and dispatcher
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("status", status_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))

    # Start the bot
    updater.start_polling()
    print("Bot is running!")

    # Run the bot until Ctrl+C is pressed
    updater.idle()

    print("\n✧༺❀༻∞ Bot stopped ∞༺❀༻✧\n")


if __name__ == "__main__":
    main()
