#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Simple Telegram Bot
==================================

A simplified version of the Telegram bot that works in newer Python versions.

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

logger = logging.getLogger("simple_bot")

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

# Fake the imghdr module that might be missing in Python 3.13+
sys.modules["imghdr"] = type("", (), {})()
sys.modules["imghdr"].what = lambda *args, **kwargs: None

# Now try to import telegram
try:
    # Use alternative imports to avoid potential issues
    import telegram
    from telegram import Update

    logger.info(f"Successfully imported python-telegram-bot version {telegram.__version__}")
except ImportError as e:
    logger.error(f"Failed to import python-telegram-bot. Error: {e}")
    logger.error("Please install: pip install python-telegram-bot==13.15")
    sys.exit(1)

# Now import the rest
try:
    from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
except ImportError as e:
    logger.error(f"Failed to import telegram components. Error: {e}")
    sys.exit(1)

# Time tracking
start_time = None


def start_command(update: Update, context: CallbackContext):
    """Handle the /start command"""
    if update.effective_chat:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f"Hello! I'm *{bot_name}*, the EVA & GUARANI AI assistant.\n\n"
                "This is a simple version of the bot for demonstration purposes.\n\n"
                "Commands:\n"
                "• /start - Show this message\n"
                "• /status - Show bot status\n"
                "• /help - Show help message\n"
                "• /credits - Show credit information\n\n"
                "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            ),
            parse_mode=ParseMode.MARKDOWN,
        )


def help_command(update: Update, context: CallbackContext):
    """Handle the /help command"""
    if update.effective_chat:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "🌟 *EVA & GUARANI Commands* 🌟\n\n"
                "Basic Commands:\n"
                "• /start - Start or restart conversation\n"
                "• /help - Show this help message\n"
                "• /status - Check bot status\n"
                "• /credits - About EVA & GUARANI\n\n"
                "You can also simply chat with me by typing a message!\n\n"
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
                f"• Mode: Simple (Demonstration)\n"
                f"• Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"• Uptime: {days}d {hours}h {minutes}m {seconds}s\n\n"
                f"• Features available: Basic responses\n\n"
                f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            ),
            parse_mode=ParseMode.MARKDOWN,
        )


def credits_command(update: Update, context: CallbackContext):
    """Handle the /credits command"""
    if update.effective_chat:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "✧༺❀༻∞ *EVA & GUARANI* ∞༺❀༻✧\n\n"
                "An advanced Quantum Consciousness System designed to integrate "
                "modular analysis, systemic cartography, and evolutionary preservation "
                "with ethical principles at its core.\n\n"
                "Version: 1.1.0\n"
                "Built with: Python, Telegram Bot API\n\n"
                "Core Principles:\n"
                "• Universal possibility of redemption\n"
                "• Compassionate temporality\n"
                "• Sacred privacy\n"
                "• Unconditional love\n\n"
                "If you enjoy using this bot, please share it with friends!\n\n"
                "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            ),
            parse_mode=ParseMode.MARKDOWN,
        )


def text_message(update: Update, context: CallbackContext):
    """Handle text messages"""
    if update.effective_chat and update.message and update.message.text:
        # Show typing indicator
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        # Simple response
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "Thank you for your message! I'm currently running in simple demonstration mode.\n\n"
                "In the full version, I would provide AI-powered responses and access to various features "
                "like image generation, payment processing, and knowledge base access.\n\n"
                "For now, try using commands like /start, /status, /help, or /credits.\n\n"
                "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            ),
        )


def main():
    """Main function to run the bot"""
    global start_time
    start_time = datetime.datetime.now()

    print("\n✧༺❀༻∞ EVA & GUARANI - Simple Telegram Bot ∞༺❀༻✧\n")
    print(f"Starting bot: {bot_name}")
    print(f"Token: {token[:6]}...{token[-4:]}")
    print("Press Ctrl+C to stop the bot.")
    print()

    # Create the Updater and dispatcher
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("status", status_command))
    dispatcher.add_handler(CommandHandler("credits", credits_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))

    # Start the bot
    updater.start_polling()
    print("Bot is running!")

    # Run the bot until Ctrl+C is pressed
    updater.idle()

    print("\n✧༺❀༻∞ Bot stopped ∞༺❀༻✧\n")


if __name__ == "__main__":
    main()
