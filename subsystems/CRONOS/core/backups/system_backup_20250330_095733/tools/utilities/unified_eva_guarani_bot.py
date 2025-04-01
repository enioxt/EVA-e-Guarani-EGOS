#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Unified Telegram Bot
====================================

This file contains a unified and simplified implementation of the Telegram bot
that integrates directly with the EVA & GUARANI system. The architecture has been reorganized
to minimize dependencies between files and facilitate debugging.

Author: EVA & GUARANI
Version: 2.0
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
import traceback
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional, List, Callable, Union

# Import the payment gateway
from payment_gateway import get_payment_gateway

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/eva_guarani_bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("eva_guarani_bot")

# Try to import python-telegram-bot
try:
    import telegram
    from telegram import Update, Bot
    from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters, CallbackQueryHandler
    TELEGRAM_AVAILABLE = True
except ImportError:
    logger.warning("Module python-telegram-bot not found. Trying to install...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==13.15"])
        import telegram
        from telegram import Update, Bot
        from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters, CallbackQueryHandler
        TELEGRAM_AVAILABLE = True
        logger.info("python-telegram-bot installed successfully!")
    except Exception as e:
        logger.error(f"Error installing python-telegram-bot: {e}")
        # Define empty variables to avoid errors
        TELEGRAM_AVAILABLE = False
        telegram = None
        # These classes are just to avoid syntax errors
        # and will be replaced by the real ones when the module is imported
        class Update: pass
        class Bot: pass
        class Updater: pass
        class CommandHandler: pass
        class MessageHandler: pass
        class CallbackContext: pass
        class CallbackQueryHandler: pass
        class Filters:
            text = None
            command = None

# ASCII Banner
BANNER = """
============================================================
     ✧༺❀༻∞ EVA & GUARANI UNIFIED TELEGRAM BOT ∞༺❀༻✧
============================================================
"""

# Constants
DEFAULT_CONFIG_PATH = "config/telegram_config.json"
DEFAULT_QUANTUM_CONFIG_PATH = "config/quantum_config.json"

class EVAGuaraniBot:
    """
    Unified implementation of the Telegram bot for the EVA & GUARANI system.
    This class centralizes all interaction logic with Telegram and the quantum system.
    """
    
    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        """
        Initializes the unified bot.
        
        Args:
            config_path: Path to the configuration file.
        """
        self.config_path = config_path
        self.is_running = False
        self.last_response_time = 0
        self.quantum_integration = None
        
        # Configurations loaded from the file
        self.bot_token = None
        self.allowed_users = []
        self.admin_users = []
        
        # Bot objects
        self.bot = None
        self.updater = None
        
        # Register handler for SIGINT
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Load configuration
        self.config = self._load_config()
        if self.config:
            self.bot_token = self.config.get("bot_token")
            self.allowed_users = self.config.get("allowed_users", [])
            self.admin_users = self.config.get("admin_users", [])
        
        logger.info(f"EVAGuaraniBot initialized")
    
    def _signal_handler(self, sig, frame):
        """
        Handler for interrupt signal (CTRL+C).
        """
        logger.info("Interrupt signal received. Stopping the bot...")
        self.stop()
        sys.exit(0)
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the configuration from the JSON file.
        
        Returns:
            Dictionary with the configurations or an empty dictionary in case of error.
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading configuration from {self.config_path}: {e}")
            return {}  # Return empty dictionary instead of None
    
    def _setup_telegram_bot(self) -> bool:
        """
        Sets up the Telegram bot.
        
        Returns:
            True if configured successfully, False otherwise.
        """
        try:
            if not TELEGRAM_AVAILABLE:
                logger.error("Library python-telegram-bot is not available")
                return False
            
            # Get bot token
            bot_token = self.config.get("bot_token") or self.config.get("token")
            if not bot_token:
                logger.error("Bot token not configured")
                return False
            
            # Create updater and dispatcher
            self.updater = Updater(bot_token, use_context=True)
            # Set the bot explicitly
            self.bot = self.updater.bot
            dp = self.updater.dispatcher
            
            # Register handlers for commands
            dp.add_handler(CommandHandler("start", self._handle_start))
            dp.add_handler(CommandHandler("help", self._handle_help))
            dp.add_handler(CommandHandler("status", self._handle_status))
            dp.add_handler(CommandHandler("reset", self._handle_reset))
            dp.add_handler(CommandHandler("upgrade", self._handle_upgrade))
            dp.add_handler(CommandHandler("payment", self._handle_payment))
            dp.add_handler(CommandHandler("credits", self._handle_credits))
            dp.add_handler(CommandHandler("language", self._handle_language))
            dp.add_handler(CommandHandler("image", self._handle_image))
            
            # Register handler for text messages
            dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self._handle_message))
            
            # Register handler for errors
            dp.add_error_handler(self._handle_error)
            
            # Add handler for inline button callbacks
            if TELEGRAM_AVAILABLE:
                dp.add_handler(CallbackQueryHandler(self._handle_button_press))
            
            logger.info("Telegram bot configured successfully")
            return True
        except Exception as e:
            logger.error(f"Error configuring Telegram bot: {e}")
            traceback.print_exc()
            return False

    def _setup_quantum_integration(self) -> bool:
        """
        Sets up the integration with the EVA & GUARANI quantum system.
        
        Returns:
            True if configured successfully, False otherwise.
        """
        try:
            # Import QuantumIntegration directly here to avoid cyclic dependencies
            from bot.quantum_integration import QuantumIntegration
            
            # Initialize the quantum system
            self.quantum_integration = QuantumIntegration()
            logger.info("Integration with quantum system configured successfully")
            return True
        except Exception as e:
            logger.error(f"Error configuring integration with quantum system: {e}")
            return False
    
    def _handle_start(self, update: Update, context: CallbackContext) -> None:
        """
        Handles the /start command.
        """
        try:
            user_id = update.effective_user.id
            
            if not self._is_user_allowed(user_id):
                logger.warning(f"Unauthorized user attempted to start the bot: {user_id}")
                update.effective_message.reply_text(
                    "⛔ You are not authorized to use this bot. Please contact the administrator for access.",
                    parse_mode="Markdown"
                )
                return
            
            # Get payment gateway information
            payment_gateway = get_payment_gateway()
            freemium_enabled = payment_gateway.config.get("freemium_enabled", False)
            
            # Basic welcome message
            welcome_message = (
                f"🌟 *Welcome to EVA & GUARANI Bot!* 🌟\n\n"
                f"Hello, {update.effective_user.first_name}! I am a quantum assistant designed to help "
                f"with modular analysis, systemic mapping, and evolutionary preservation.\n\n"
            )
            
            # Add information about the FREEMIUM system if enabled
            if freemium_enabled:
                # Get user limits
                tier = payment_gateway.get_user_tier(user_id)
                limits = payment_gateway.get_user_limits(user_id)
                credits = payment_gateway.get_user_credits(user_id)
                
                welcome_message += (
                    "📊 *FREEMIUM System* 📊\n\n"
                    f"You are on the *{tier.upper()}* plan with the following daily limits:\n"
                    f"• Messages: {limits['messages_per_day']} per day\n"
                    f"• Special Calls: {limits['special_calls_per_day']} per day\n"
                    f"• Internet Calls: {limits['internet_calls_per_day']} per day\n\n"
                    
                    "💳 *Your Current Credits* 💳\n"
                    f"• Special Calls: {credits['special_calls']}\n"
                    f"• Internet Calls: {credits['internet_calls']}\n\n"
                    
                    "ℹ️ *How Credits Work* ℹ️\n"
                    "• Special Calls: Image generation, detailed analyses, code creation\n"
                    "• Internet Calls: Web searches, news, updated information\n"
                    f"• Each recharge adds {payment_gateway.config.get('credits_per_recharge', 10)} credits\n"
                    f"• Minimum recharge amount: R$ {payment_gateway.config.get('recharge_amount', 5.0):.2f}\n\n"
                    
                    "💡 *Tips to Save Credits* 💡\n"
                    "• Be specific in your questions\n"
                    "• Use special calls only when necessary\n"
                    "• Check your credits with the /credits command\n\n"
                )
            
            # Add information about available commands
            welcome_message += (
                "🤖 *Available Commands* 🤖\n"
                "• /start - Displays this welcome message\n"
                "• /help - Shows help information\n"
                "• /upgrade - Information about plans and payments\n"
            )
            
            # Add credits command if FREEMIUM is enabled
            if freemium_enabled:
                welcome_message += "• /credits - Check your available credits\n"
            
            welcome_message += (
                "\nI am ready to help! Send a message to start our conversation.\n\n"
                "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            )
            
            # Send the welcome message
            update.effective_message.reply_text(
                welcome_message,
                parse_mode="Markdown"
            )
            
            logger.info(f"/start command processed for user {user_id}")
        except Exception as e:
            logger.error(f"Error processing /start command: {e}")
            update.effective_message.reply_text(
                "❌ An error occurred while processing the command. Please try again later.",
                parse_mode="Markdown"
            )
    
    def _handle_help(self, update: Update, context: CallbackContext) -> None:
        """
        Handles the /help command.
        """
        try:
            user_id = update.effective_user.id
            
            if not self._is_user_allowed(user_id):
                logger.warning(f"Unauthorized user attempted to use the help command: {user_id}")
                update.effective_message.reply_text(
                    "⛔ You are not authorized to use this bot. Please contact the administrator for access.",
                    parse_mode="Markdown"
                )
                return
            
            # Get payment gateway information
            from payment_gateway import get_payment_gateway
            payment_gateway = get_payment_gateway()
            freemium_enabled = payment_gateway.config.get("freemium_enabled", False)
            
            # Basic help message
            help_message = (
                "🤖 *EVA & GUARANI Help* 🤖\n\n"
                
                "Hello! I am your quantum AI-based assistant for generating creative and accurate responses.\n\n"
                
                "📝 *Available Commands*:\n"
                "• /start - Starts the bot and displays the welcome message\n"
                "• /help - Displays this help message\n"
                "• /upgrade - Information about plans and payments\n"
                "• /status - Checks the bot status\n"
                "• /reset - Restarts the bot\n"
                "• /language - Chooses the interaction language\n"
            )
            
            # Add image command
            help_message += "• /image - Generates images with DALL-E from your description\n"
            
            # Add information about the FREEMIUM system if enabled
            if freemium_enabled:
                help_message += (
                    "• /credits - Checks your credits and limits\n"
                    "• /payment - Registers a payment\n\n"
                    
                    "📊 *FREEMIUM System*:\n"
                    "This bot uses a FREEMIUM system that offers free access to basic features, "
                    "while advanced resources consume credits.\n\n"
                    
                    "📋 *Types of Calls*:\n"
                    "• *Regular Messages*: Basic conversations, no special processing\n"
                    "• *Special Calls*: Advanced processing, code generation, analyses, image generation\n"
                    "• *Internet Calls*: Web search, updated information\n\n"
                    
                    "💡 *Tips to Save Credits*:\n"
                    "• Be specific in your questions\n"
                    "• Use special and internet calls only when necessary\n"
                    "• Check your credits regularly with /credits\n\n"
                    
                    "📱 *Recharge Credits*:\n"
                    f"• Minimum recharge amount: R$ {payment_gateway.config.get('recharge_amount', 5.0):.2f}\n"
                    f"• Each recharge adds {payment_gateway.config.get('credits_per_recharge', 10)} credits\n"
                    "• Use the /upgrade command to see payment options\n\n"
                )
            
            # Add usage information
            help_message += (
                "🔄 *How to use*:\n"
                "1. To chat with me, just send regular messages\n"
                "2. To generate an image, use the /image command followed by the image description\n"
                "3. To change the language, use the /language command\n"
                "4. To check your credits, use the /credits command\n\n"
                
                "If you need additional help, please contact the administrator.\n\n"
                
                "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            )
            
            # Send the help message
            update.effective_message.reply_text(
                help_message,
                parse_mode="Markdown"
            )
            
            logger.info(f"/help command processed for user {user_id}")
        except Exception as e:
            logger.error(f"Error processing /help command: {e}")
            update.effective_message.reply_text(
                "❌ An error occurred while processing the command. Please try again later.",
                parse_mode="Markdown"
            )
    
    def _handle_status(self, update: Update, context: CallbackContext) -> None:
        """
        Handles the /status command.
        """
        try:
            user_id = update.effective_user.id
            
            if self._is_user_allowed(user_id):
                quantum_status = "✅ Active" if self.quantum_integration else "❌ Inactive"
                
                update.effective_message.reply_text(
                    "🔄 *System Status* 🔄\n\n"
                    f"• Telegram Bot: ✅ Online\n"
                    f"• Quantum System: {quantum_status}\n"
                    f"• Bridge: ✅ Working\n",
                    parse_mode="Markdown"
                )
        except Exception as e:
            logger.error(f"Error handling status command: {e}")
    
    def _handle_reset(self, update: Update, context: CallbackContext) -> None:
        """
        Handles the /reset command.
        """
        try:
            user_id = update.effective_user.id
            
            if self._is_user_admin(user_id):
                update.effective_message.reply_text(
                    "🔄 *Restarting quantum system* 🔄\n\n"
                    "Please wait...",
                    parse_mode="Markdown"
                )
                
                # Create thread to restart the integration
                threading.Thread(target=self._restart_quantum).start()
            else:
                update.effective_message.reply_text(
                    "⚠️ *Access denied* ⚠️\n\n"
                    "Only administrators can restart the system.",
                    parse_mode="Markdown"
                )
        except Exception as e:
            logger.error(f"Error handling reset command: {e}")
    
    def _restart_quantum(self) -> None:
        """
        Restarts the integration with the quantum system.
        """
        try:
            logger.info("Restarting integration with quantum system...")
            
            # If there is an active integration, clear it
            self.quantum_integration = None
            
            # Wait a moment
            time.sleep(2)
            
            # Set up new integration
            quantum_configured = self._setup_quantum_integration()
            
            # Notify administrators
            status_msg = "✅ Quantum system restarted successfully" if quantum_configured else "❌ Failed to restart quantum system"
            
            for admin_id in self.admin_users:
                try:
                    self.bot.send_message(
                        chat_id=admin_id,
                        text=f"{status_msg}",
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    logger.error(f"Error sending message to admin {admin_id}: {e}")
        except Exception as e:
            logger.error(f"Error restarting quantum system: {e}")
    
    def _process_message_with_quantum(self, user_id: int, message_text: str) -> str:
        """
        Processes a message using the quantum integration.
        
        Args:
            user_id: User ID on Telegram.
            message_text: Text of the message.
            
        Returns:
            Processed response.
        """
        try:
            # Check if the message contains special commands
            contains_special_command = self._check_for_special_command(message_text)
            contains_internet_command = self._check_for_internet_command(message_text)
            
            # Check credits for special commands
            if contains_special_command:
                payment_gateway = get_payment_gateway()
                if not payment_gateway.check_user_usage(user_id, "special_calls"):
                    credits = payment_gateway.get_user_credits(user_id)
                    return (
                        "⚠️ *Insufficient Credits for Special Call* ⚠️\n\n"
                        f"You do not have enough credits to use special calls.\n\n"
                        f"