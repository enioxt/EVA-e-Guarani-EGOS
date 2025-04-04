#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Bridge Telegram-ElizaOS
=======================================

This script creates a bridge between the Telegram bot and ElizaOS,
allowing communication between the two systems.

Author: EVA & GUARANI
Version: 1.0
"""

import os
import sys
import json
import time
import signal
import asyncio
import logging
import argparse
import threading
import subprocess
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional, List, Callable, Union

# Import QuantumIntegration
from bot.quantum_integration import QuantumIntegration

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/telegram_eliza_bridge.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("telegram_eliza_bridge")

# Check if the logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs", exist_ok=True)
    logger.info("Logs directory created: logs/")

# Try to import necessary modules
try:
    from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
    from telegram import Update, Bot
    # Correct imports for version 13.15
    from telegram.ext import Filters
except ImportError:
    logger.error("Module 'python-telegram-bot' not found. Installing...")

    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==13.15"])

        from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
        from telegram import Update, Bot
        from telegram.ext import Filters
    except Exception as e:
        logger.error(f"Failed to install python-telegram-bot: {e}")
        sys.exit(1)

# Import ElizaIntegration module
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), "bot"))
    from bot.eliza_integration import ElizaBot, ElizaIntegration
except ImportError:
    logger.warning("Module 'eliza_integration' not found. The bridge will run in standalone mode.")
    ElizaIntegration = None
    ElizaBot = None

# Try to import bot_package
try:
    # Import the eva_guarani_main module directly
    import bot.eva_guarani_main as eva_guarani_module
    logger.info("EVA & GUARANI main module imported successfully")
except ImportError as e:
    logger.warning(f"Could not import the EVA & GUARANI module: {e}")
    eva_guarani_module = None

# Try to import bot modules
try:
    from bot.unified_telegram_bot_utf8 import setup_bot
    logger.info("unified_telegram_bot_utf8 module imported successfully")
except ImportError as e:
    logger.warning(f"Could not import the unified_telegram_bot_utf8 module: {e}")

class TelegramElizaBridge:
    """Bridge between the Telegram bot and ElizaOS"""

    def __init__(self, config_path: str = "config/telegram_config.json"):
        """
        Initializes the Telegram-ElizaOS bridge

        Args:
            config_path: Path to the Telegram configuration file
        """
        self.config_path = config_path
        self.is_running = False
        self.eliza_integration = None
        self.eliza_bot = None
        self.updater = None
        self.bot = None
        self.bot_token = None
        self.allowed_users = []
        self.admin_users = []
        self._last_response_time = 0  # Initialize the last response time

        # Initialize quantum integration
        self.quantum_integration = QuantumIntegration()

        # Load configuration
        self._load_config()

        # Set up signal handler
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        logger.info("TelegramElizaBridge initialized")

    def _signal_handler(self, sig, frame):
        """Handler for termination signals"""
        logger.info(f"Signal received: {sig}")
        self.stop()
        sys.exit(0)

    def _load_config(self) -> Dict[str, Any]:
        """Loads the Telegram configuration"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            logger.info(f"Configuration loaded from {self.config_path}")
            self.bot_token = config.get("bot_token", "")
            self.admin_users = config.get("admin_users", [])
            self.allowed_users = config.get("allowed_users", [])
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return {}

    def _setup_telegram_bot(self) -> bool:
        """Sets up the Telegram bot"""
        logger.info("Setting up Telegram bot...")

        if not self.bot_token:
            logger.error("Telegram token not configured!")
            return False

        try:
            # Correct Updater configuration for version 13.15
            # Increase connection timeout to avoid frequent disconnections
            request_kwargs = {
                'read_timeout': 30,
                'connect_timeout': 30
            }
            self.updater = Updater(self.bot_token, request_kwargs=request_kwargs)
            self.bot = self.updater.bot
            dispatcher = self.updater.dispatcher

            # Register command handlers
            dispatcher.add_handler(CommandHandler("start", self._handle_start))
            dispatcher.add_handler(CommandHandler("help", self._handle_help))
            dispatcher.add_handler(CommandHandler("status", self._handle_status))
            dispatcher.add_handler(CommandHandler("restart", self._handle_restart))

            # Register handler for text messages that are not commands
            text_filter = Filters.text & ~Filters.command
            dispatcher.add_handler(MessageHandler(text_filter, self._handle_message))

            # Register error handler
            dispatcher.add_error_handler(self._handle_error)

            logger.info("Telegram bot configured successfully!")
            return True
        except Exception as e:
            logger.error(f"Error setting up Telegram bot: {e}")
            traceback.print_exc()
            return False

    def _setup_eliza(self) -> bool:
        """Sets up the integration with ElizaOS"""
        try:
            logger.info("Setting up integration with ElizaOS...")

            if not ElizaIntegration:
                logger.error("ElizaIntegration module not available")
                return False

            # Create instance of ElizaIntegration
            self.eliza_integration = ElizaIntegration(
                telegram_config_path=self.config_path,
                eliza_config_path="config/eliza_config.json"
            )

            # Check if ElizaOS is installed
            if not self.eliza_integration.is_eliza_installed():
                logger.warning("ElizaOS is not installed or not configured correctly")
                self.eliza_integration = None
                return False

            # Start ElizaOS
            if not self.eliza_integration.start():
                logger.error("Failed to start ElizaOS")
                self.eliza_integration = None
                return False

            # Set up ElizaOS bot
            self.eliza_bot = ElizaBot(integration=self.eliza_integration)

            # Register handlers
            self.eliza_bot.register_update_handler(self._handle_eliza_response)

            logger.info("Integration with ElizaOS configured successfully")
            return True
        except Exception as e:
            logger.error(f"Error setting up integration with ElizaOS: {e}")
            self.eliza_integration = None
            self.eliza_bot = None
            return False

    def _handle_start(self, update: Update, context: CallbackContext) -> None:
        """Handles the /start command"""
        if not update or not update.effective_message:
            return

        user_id = update.effective_message.from_user.id if update.effective_message.from_user else None
        logger.info(f"/start command received from {user_id}")

        if self._is_user_allowed(user_id):
            update.effective_message.reply_text(
                "🌟 *Welcome to the EVA & GUARANI Telegram Bot* 🌟\n\n"
                "I am connected to the ElizaOS system to provide advanced assistance.\n\n"
                "Use /help to see available commands.",
                parse_mode="Markdown"
            )
        else:
            update.effective_message.reply_text(
                "⚠️ *Unauthorized access* ⚠️\n\n"
                "You do not have permission to use this bot.",
                parse_mode="Markdown"
            )

    def _handle_help(self, update: Update, context: CallbackContext) -> None:
        """Handles the /help command"""
        if not update or not update.effective_message:
            return

        user_id = update.effective_message.from_user.id if update.effective_message.from_user else None
        logger.info(f"/help command received from {user_id}")

        if self._is_user_allowed(user_id):
            update.effective_message.reply_text(
                "📋 *Available Commands* 📋\n\n"
                "/start - Starts the conversation\n"
                "/help - Shows this help\n"
                "/status - Checks the system status\n"
                "/restart - Restarts the integration (admin only)\n\n"
                "You can also send messages directly to interact with the system.",
                parse_mode="Markdown"
            )

    def _handle_status(self, update: Update, context: CallbackContext) -> None:
        """Handles the /status command"""
        if not update or not update.effective_message:
            return

        user_id = update.effective_message.from_user.id if update.effective_message.from_user else None
        logger.info(f"/status command received from {user_id}")

        if self._is_user_allowed(user_id):
            eliza_status = "✅ Connected" if self.eliza_integration and hasattr(self.eliza_integration, "is_running") and self.eliza_integration.is_running else "❌ Disconnected"

            update.effective_message.reply_text(
                "🔄 *System Status* 🔄\n\n"
                f"• Telegram Bot: ✅ Online\n"
                f"• ElizaOS: {eliza_status}\n"
                f"• Bridge: ✅ Running\n"
                f"• Mode: {'Integrated' if self.eliza_integration else 'Standalone'}\n",
                parse_mode="Markdown"
            )

    def _handle_restart(self, update: Update, context: CallbackContext) -> None:
        """Handles the /restart command"""
        if not update or not update.effective_message:
            return

        user_id = update.effective_message.from_user.id if update.effective_message.from_user else None
        logger.info(f"/restart command received from {user_id}")

        if self._is_user_admin(user_id):
            update.effective_message.reply_text(
                "🔄 *Restarting integration with ElizaOS* 🔄\n\n"
                "Please wait...",
                parse_mode="Markdown"
            )

            # Create thread to restart the integration
            threading.Thread(target=self._restart_eliza).start()
        else:
            update.effective_message.reply_text(
                "⚠️ *Access denied* ⚠️\n\n"
                "Only administrators can restart the system.",
                parse_mode="Markdown"
            )

    def _restart_eliza(self) -> None:
        """Restarts the integration with ElizaOS"""
        try:
            logger.info("Restarting integration with ElizaOS...")

            # Stop the current integration
            if self.eliza_integration:
                try:
                    self.eliza_integration.stop()
                    logger.info("ElizaOS stopped successfully")
                except Exception as e:
                    logger.error(f"Error stopping ElizaOS: {e}")

            # Initialize new integration
            if self._setup_eliza():
                logger.info("ElizaOS restarted successfully")
            else:
                logger.error("Failed to restart ElizaOS")

            # Notify admins
            if not self.bot:
                logger.error("Bot not initialized to send notifications")
                return

            for admin_id in self.admin_users:
                try:
                    self.bot.send_message(
                        chat_id=admin_id,
                        text="✅ *Integration with ElizaOS restarted successfully* ✅",
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    logger.error(f"Error sending message to admin {admin_id}: {e}")
        except Exception as e:
            logger.error(f"Error restarting ElizaOS: {e}")

    def _handle_message(self, update: Update, context: CallbackContext) -> None:
        """
        Handles regular messages sent to the bot
        """
        try:
            # Check if the user has permission
            if update.effective_user.id not in self.allowed_users:
                logger.warning(f"Unauthorized user attempted to send message: {update.effective_user.id}")
                update.message.reply_text("You are not authorized to use this bot.")
                return

            logger.info(f"Message received from {update.effective_user.id}: {update.message.text}")

            if self.eliza_integration and self.eliza_integration.is_running:
                # Prepare the message for ElizaOS
                eliza_update = self._convert_to_eliza_update(update)

                # Send the message to ElizaOS
                logger.debug(f"Sending message to ElizaOS: {eliza_update}")
                try:
                    self.eliza_bot.process_update(eliza_update)

                    # Wait for a response from ElizaOS (up to 2 seconds)
                    wait_time = 2
                    start_time = time.time()
                    current_time = time.time()

                    # Check if we received a response in the last 2 seconds
                    while current_time - start_time < wait_time:
                        if self._last_response_time > start_time:
                            logger.info("Response from ElizaOS received and processed")
                            return
                        time.sleep(0.1)
                        current_time = time.time()

                    # If we reach here, ElizaOS did not respond in the expected time
                    logger.warning("ElizaOS did not respond in the expected time, using fallback EVA & GUARANI")
                    self._respond_with_eva_guarani(update, context)

                except Exception as e:
                    logger.error(f"Error processing message with ElizaOS: {e}")
                    self._respond_with_eva_guarani(update, context)
            else:
                logger.warning("ElizaOS is not running, using fallback EVA & GUARANI")
                self._respond_with_eva_guarani(update, context)
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            try:
                update.message.reply_text("An error occurred while processing your message. Please try again later.")
            except Exception as reply_error:
                logger.error(f"Error sending error message: {reply_error}")

    def _respond_with_eva_guarani(self, update: Update, context: CallbackContext) -> None:
        """
        Responds with EVA & GUARANI when ElizaOS does not provide a response
        """
        try:
            user_id = update.effective_user.id
            user_name = update.effective_user.first_name
            user_message = update.message.text

            logger.info(f"Processing message for quantum response from {user_name} ({user_id})")

            # Get the conversation history from the context
            if not hasattr(context.user_data, 'conversation_history'):
                context.user_data['conversation_history'] = []

            # Limit the history to the last 10 messages to maintain context without overloading
            conversation_history = context.user_data.get('conversation_history', [])[-10:]

            # Prepare context data
            context_data = {
                "platform": "telegram",
                "previous_messages": len(conversation_history)
            }

            # Process the message using the quantum system
            try:
                # Create an event loop to run the coroutine synchronously
                loop = asyncio.new_event_loop()

                # Run the coroutine synchronously
                quantum_response = loop.run_until_complete(
                    self.quantum_integration.process_message(
                        user_id=user_id,
                        username=user_name,
                        message=user_message if user_message else "",
                        conversation_history=conversation_history,
                        context=context_data
                    )
                )
                loop.close()

                # Extract the response from the returned object
                if isinstance(quantum_response, dict):
                    response = quantum_response.get('response', '')
                    # Add to conversation
                    conversation_history.append({"role": "user", "content": user_message})
                    conversation_history.append({"role": "assistant", "content": response})
                    context.user_data['conversation_history'] = conversation_history
                else:
                    response = "Sorry, an error occurred while processing your message."
                    logger.error(f"Unexpected quantum response: {quantum_response}")
            except Exception as process_error:
                logger.error(f"Error processing message with quantum: {process_error}")
                # Fallback if quantum processing fails
                response = f"Hello {user_name}! Currently, I am operating in contingency mode. How can I assist you?"

            # Remove the signature if it's not the first message
            if len(conversation_history) > 2 and "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧" in response:
                response = response.replace("\n\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧", "")
                response = response.replace("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧", "")

            # Send the response
            update.message.reply_text(response)
            logger.info(f"Sent quantum fallback response to {user_id}")
        except Exception as e:
            logger.error(f"Error sending EVA & GUARANI response: {e}")
            try:
                update.message.reply_text("An error occurred while processing your message. Please try again later.")
            except Exception as reply_error:
                logger.error(f"Error sending error message: {reply_error}")

    def _handle_eliza_response(self, data: Dict[str, Any]) -> None:
        """
        Handles responses from ElizaOS
        """
        try:
            # Log that we received a response
            logger.debug(f"Response received from ElizaOS: {data}")
            self._last_response_time = time.time()

            if not data:
                logger.warning("Empty response received from ElizaOS")
                return

            method = data.get("method", "")

            if method == "sendMessage":
                chat_id = data.get("chat_id")
                if not chat_id:
                    logger.warning("Chat ID not provided in response from ElizaOS")
                    return

                if not self.bot:
                    logger.warning("Telegram bot not initialized")
