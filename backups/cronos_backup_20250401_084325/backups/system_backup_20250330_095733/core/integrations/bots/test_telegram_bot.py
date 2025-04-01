#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Minimal bot to test the connection with Telegram
"""

import logging
import os
import sys
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token (use the same token as your current bot)
TOKEN = "7642662485:AAHqu2VIY2sCLKMNvqO5o8thbjhyr1aimiw"

# Define the function for the /start command
def start(update: Update, context: CallbackContext) -> None:
    """Function executed when the user sends the /start command"""
    user = update.effective_user
    update.message.reply_text(f'Hello {user.first_name}! I am working. I am EVA & GUARANI.')

# Define the function for the /help command
def help_command(update: Update, context: CallbackContext) -> None:
    """Function executed when the user sends the /help command"""
    update.message.reply_text('Help: \n/start - Start the bot\n/help - Display this message')

# Define the function to process text messages
def echo(update: Update, context: CallbackContext) -> None:
    """Function executed when the user sends a text message"""
    update.message.reply_text(f"I received your message: {update.message.text}")
    logger.info(f"Message received: {update.message.text}")

def main() -> None:
    """Main function to start the bot"""
    try:
        # Create the Updater object and pass the bot token
        # Adding configurations to avoid connection issues
        request_kwargs = {
            'read_timeout': 30,
            'connect_timeout': 30,
            'pool_timeout': 30
        }
        
        updater = Updater(TOKEN, request_kwargs=request_kwargs)
        
        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # Register handlers
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

        # Start the bot
        logger.info("Starting the bot...")
        updater.start_polling(drop_pending_updates=True, timeout=30)
        
        # Display bot information on the console
        bot_info = updater.bot.get_me()
        logger.info(f"Bot started! Name: {bot_info.first_name}, Username: @{bot_info.username}")
        logger.info("Press Ctrl+C to stop.")
        
        # Keep the bot running until Ctrl+C is received
        updater.idle()
    
    except Exception as e:
        logger.error(f"Error starting the bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()