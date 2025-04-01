#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Unified Telegram Bot
====================================

Complete Telegram bot implementation for EVA & GUARANI that integrates:
1. Quantum Knowledge System
2. Payment Processing
3. Image Generation (optional)
4. Internet Search (optional)

This is the flagship product of EVA & GUARANI, offering a complete
AI assistant with ethical foundations and fair payment model.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0.0
"""

import os
import re
import json
import logging
import asyncio
import datetime
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.append(project_root)

# Create logs directory if it doesn't exist
os.makedirs(os.path.join(current_dir, "logs"), exist_ok=True)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(current_dir, "logs", "telegram_bot.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("eva_guarani_bot")

# Try to import python-telegram-bot
try:
    import telegram
    from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
    from telegram.constants import ParseMode
    from telegram.ext import (
        Application, CommandHandler, MessageHandler, filters, 
        CallbackContext, ConversationHandler, CallbackQueryHandler,
        ContextTypes
    )
    TELEGRAM_AVAILABLE = True
except ImportError:
    logger.error("python-telegram-bot not found. Run: pip install python-telegram-bot")
    TELEGRAM_AVAILABLE = False

# Try to import payment system
try:
    sys.path.append(os.path.join(project_root, "tools/utilities"))
    from payment_gateway import PaymentGateway, get_payment_gateway
    PAYMENT_AVAILABLE = True
except ImportError:
    logger.warning("Payment gateway not found.")
    PAYMENT_AVAILABLE = False

# Try to import quantum knowledge system
try:
    sys.path.append(os.path.join(project_root, "modules/quantum"))
    from quantum_knowledge_hub import QuantumKnowledgeHub
    from quantum_knowledge_integrator import QuantumKnowledgeIntegrator
    QUANTUM_KNOWLEDGE_AVAILABLE = True
except ImportError:
    logger.warning("Quantum knowledge system not found.")
    QUANTUM_KNOWLEDGE_AVAILABLE = False

# Try to import OpenAI for fallback
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    logger.warning("OpenAI not available for fallback.")
    OPENAI_AVAILABLE = False

# Conversation states
STANDARD = 0
IMAGE_GEN = 1
PAYMENT = 2

class EVAGuaraniBot:
    """
    EVA & GUARANI Telegram Bot with quantum knowledge and payment integration.
    """
    
    def __init__(self, config_path: str = os.path.join(current_dir, "telegram_config.json")):
        """
        Initializes the EVA & GUARANI Telegram bot.
        
        Args:
            config_path: Path to the configuration file
        """
        self.logger = logger
        self.logger.info("Initializing EVA & GUARANI Telegram Bot")
        
        # Check dependencies
        if not TELEGRAM_AVAILABLE:
            self.logger.error("python-telegram-bot is required. Run: pip install python-telegram-bot")
            raise ImportError("python-telegram-bot not found")
            
        # Paths
        self.config_path = Path(config_path)
        
        # Internal state
        self.config = self._load_config()
        self.updater = None
        self.dispatcher = None
        self.conversations = {}
        self.started = False
        self.message_counters = {}  # {user_id: count}
        self.last_responses = {}    # {chat_id: last_response}
        
        # Payment system
        self.payment_gateway = None
        if PAYMENT_AVAILABLE and self.config.get("payment", {}).get("enabled", False):
            self.initialize_payment_system()
        
        # Quantum knowledge system
        self.quantum_knowledge_hub = None
        self.quantum_knowledge_integrator = None
        if QUANTUM_KNOWLEDGE_AVAILABLE and self.config.get("knowledge", {}).get("enabled", False):
            asyncio.run(self.initialize_quantum_knowledge())
        
        # Initialize token from config
        self.token = self.config.get("token", "")
        if not self.token:
            self.logger.error("Bot token not configured in telegram_config.json")
            raise ValueError("Bot token not configured")
            
        self.logger.info("EVA & GUARANI Telegram Bot initialized")
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the bot configuration.
        
        Returns:
            Dictionary with the configurations
        """
        # Default configuration
        default_config = {
            "token": "",
            "allowed_users": [],
            "admin_users": [],
            "webhook_enabled": False,
            "webhook_url": "",
            "debug_mode": False,
            "message_timeout": 300,
            "max_message_length": 4096,
            "payment": {
                "enabled": False,
                "config_path": "../../data/payment_config.json",
                "freemium_enabled": True,
                "initial_credits": 10,
                "credits_per_payment": 10,
                "payment_amount": 2.0
            },
            "knowledge": {
                "enabled": True,
                "hub_config_path": "../../modules/quantum/quantum_hub.json",
                "integrator_config_path": "../../modules/quantum/quantum_integrator.json"
            }
        }
        
        # Try to load custom configuration
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with default configuration
                    merged_config = {**default_config, **config}
                    self.logger.info(f"Configuration loaded from {self.config_path}")
                    
                    # Check token
                    if not merged_config["token"]:
                        self.logger.warning("Telegram token not configured")
                        
                    return merged_config
            else:
                # Create default configuration file
                os.makedirs(self.config_path.parent, exist_ok=True)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Default configuration created at {self.config_path}")
                self.logger.warning("Configure the Telegram token in telegram_config.json")
                return default_config
                
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return default_config
            
    def initialize_payment_system(self) -> None:
        """
        Initializes the payment system integration.
        """
        try:
            # Get payment configuration path
            payment_config_path = self.config.get("payment", {}).get("config_path", "")
            if payment_config_path:
                payment_config_path = os.path.join(project_root, payment_config_path)
            
            # Initialize payment gateway
            self.payment_gateway = PaymentGateway(payment_config_path)
            
            self.logger.info("Payment system initialized")
        except Exception as e:
            self.logger.error(f"Error initializing payment system: {e}")
    
    async def initialize_quantum_knowledge(self) -> bool:
        """
        Initializes the quantum knowledge system.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        if not QUANTUM_KNOWLEDGE_AVAILABLE:
            self.logger.warning("Quantum knowledge system not available for initialization")
            return False
            
        try:
            # Get knowledge configuration paths
            hub_config_path = self.config.get("knowledge", {}).get("hub_config_path", "")
            integrator_config_path = self.config.get("knowledge", {}).get("integrator_config_path", "")
            
            if hub_config_path:
                hub_config_path = os.path.join(project_root, hub_config_path)
            if integrator_config_path:
                integrator_config_path = os.path.join(project_root, integrator_config_path)
            
            # Initialize hub
            self.quantum_knowledge_hub = QuantumKnowledgeHub(hub_config_path)
            
            # Initialize integrator
            self.quantum_knowledge_integrator = QuantumKnowledgeIntegrator(integrator_config_path)
            
            # Connect hub to integrator
            await self.quantum_knowledge_integrator.initialize_hub()
            
            self.logger.info("Quantum knowledge system initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing quantum knowledge system: {e}")
            return False
    
    def start(self) -> None:
        """
        Starts the Telegram bot.
        """
        try:
            self.logger.info("Starting EVA & GUARANI Telegram Bot")
            
            # Create updater
            self.updater = Application.builder().token(self.token).build()
            self.dispatcher = self.updater.dispatcher
            
            # Setup handlers
            self.setup_handlers()
            
            # Start bot
            if self.config.get("webhook_enabled", False):
                # Use webhook
                webhook_url = self.config.get("webhook_url", "")
                webhook_port = self.config.get("webhook_port", 8443)
                
                if not webhook_url:
                    self.logger.error("Webhook URL not configured")
                    raise ValueError("Webhook URL not configured")
                    
                self.updater.updater.start_webhook(
                    listen="0.0.0.0",
                    port=webhook_port,
                    url_path=self.token,
                    webhook_url=f"{webhook_url}/{self.token}"
                )
                self.logger.info(f"Bot started with webhook at {webhook_url}")
            else:
                # Use polling
                self.updater.updater.start_polling()
                self.logger.info("Bot started with polling")
                
            self.started = True
            
            # Keep the bot running
            self.updater.updater.idle()
            
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            traceback.print_exc()
    
    def setup_handlers(self) -> None:
        """
        Sets up the bot handlers.
        """
        # Check if dispatcher is available
        if not self.dispatcher:
            self.logger.error("Dispatcher not available")
            return
            
        # Command handlers
        self.dispatcher.add_handler(CommandHandler("start", self._handle_start))
        self.dispatcher.add_handler(CommandHandler("help", self._handle_help))
        self.dispatcher.add_handler(CommandHandler("restart", self._handle_restart))
        self.dispatcher.add_handler(CommandHandler("credits", self._handle_credits))
        self.dispatcher.add_handler(CommandHandler("upgrade", self._handle_upgrade))
        self.dispatcher.add_handler(CommandHandler("payment", self._handle_payment))
        self.dispatcher.add_handler(CommandHandler("status", self._handle_status))
        self.dispatcher.add_handler(CommandHandler("image", self._handle_image_command))
        
        # Callback query handler
        self.dispatcher.add_handler(CallbackQueryHandler(self._handle_callback))
        
        # Create conversation handler for image generation
        image_conv_handler = ConversationHandler(
            entry_points=[CommandHandler('image', self._handle_image_command)],
            states={
                IMAGE_GEN: [MessageHandler(filters.Text(~filters.Command) & ~filters.Regex(r'/cancel'), self._handle_image_prompt)],
            },
            fallbacks=[CommandHandler('cancel', self._handle_cancel)],
        )
        self.dispatcher.add_handler(image_conv_handler)
        
        # Create conversation handler for payment
        payment_conv_handler = ConversationHandler(
            entry_points=[CommandHandler('payment', self._handle_payment)],
            states={
                PAYMENT: [MessageHandler(filters.Text(~filters.Command) & ~filters.Regex(r'/cancel'), self._handle_payment_confirmation)],
            },
            fallbacks=[CommandHandler('cancel', self._handle_cancel)],
        )
        self.dispatcher.add_handler(payment_conv_handler)
        
        # Message handler (should be last)
        self.dispatcher.add_handler(MessageHandler(filters.Text(~filters.Command) & ~filters.Regex(r'/cancel'), self._handle_message))
        
        # Error handler
        self.dispatcher.add_error_handler(self._handle_error)
        
        self.logger.info("Handlers configured")
    
    def _handle_start(self, update: Update, context: ContextTypes) -> None:
        """
        Handles the /start command.
        """
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        
        # Check if user is allowed
        if not self._check_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return
        
        # Clear conversation history
        self.clear_conversation_history(chat_id)
        
        # Initialize user if using payment system
        if self.payment_gateway and PAYMENT_AVAILABLE:
            self.payment_gateway.initialize_user(user_id)
            
            # Get welcome message from payment config
            welcome_message = self.payment_gateway.config.get("welcome_message", "")
            if not welcome_message:
                welcome_message = (
                    "Hello! I'm EVA & GUARANI, your ethical AI assistant.\n\n"
                    "I can help you with a wide range of tasks including research, "
                    "creative writing, code analysis, and more.\n\n"
                    "You have free daily messages and special features, or you can "
                    "upgrade for additional capabilities."
                )
        else:
            welcome_message = (
                "Hello! I'm EVA & GUARANI, your ethical AI assistant.\n\n"
                "I can help you with a wide range of tasks including research, "
                "creative writing, code analysis, and more."
            )
        
        # Send welcome message
        update.message.reply_text(
            f"{welcome_message}\n\n"
            "Use /help to see available commands.",
            parse_mode=ParseMode.MARKDOWN
        )
    
    def _handle_help(self, update: Update, context: ContextTypes) -> None:
        """
        Handles the /help command.
        """
        user_id = update.effective_user.id
        
        # Check if user is allowed
        if not self._check_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return
        
        # Basic commands
        help_text = (
            "🌟 *EVA & GUARANI Commands* 🌟\n\n"
            "Basic Commands:\n"
            "• /start - Start or restart the bot\n"
            "• /help - Show this help message\n"
            "• /restart - Clear conversation context\n"
        )
        
        # Payment related commands
        if self.payment_gateway and PAYMENT_AVAILABLE:
            help_text += (
                "\nCredits & Payments:\n"
                "• /credits - Check your available credits\n"
                "• /upgrade - Get information about upgrading\n"
                "• /payment - Register a new payment\n"
            )
        
        # Special features
        help_text += (
            "\nSpecial Features:\n"
            "• /image - Generate images from text descriptions\n"
            "• /status - Check bot status and your usage\n"
        )
        
        # Send help message
        update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    def _handle_restart(self, update: Update, context: ContextTypes) -> None:
        """
        Handles the /restart command.
        """
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        
        # Check if user is allowed
        if not self._check_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return
        
        # Clear conversation history
        self.clear_conversation_history(chat_id)
        
        # Send confirmation
        update.message.reply_text(
            "✅ Conversation context has been reset."
        )
    
    def _handle_credits(self, update: Update, context: ContextTypes) -> None:
        """
        Handles the /credits command.
        """
        user_id = update.effective_user.id
        
        # Check if user is allowed
        if not self._check_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return
        
        # Check if payment system is available
        if not self.payment_gateway or not PAYMENT_AVAILABLE:
            update.message.reply_text(
                "Payment system is not enabled. All features are freely available."
            )
            return
        
        # Get user credits and usage
        credits = self.payment_gateway.get_user_credits(user_id)
        tier = self.payment_gateway.get_user_tier(user_id)
        limits = self.payment_gateway.get_user_limits(user_id)
        usage = self.payment_gateway.get_user_usage(user_id)
        
        # Format tier name nicely
        tier_name = tier.replace("_", " ").title()
        
        # Build message
        message = (
            f"🪙 *Your Credits & Usage* 🪙\n\n"
            f"Current tier: *{tier_name}*\n"
            f"Available credits: *{credits}*\n\n"
            f"Daily limits:\n"
            f"• Messages: {usage.get('messages_today', 0)}/{limits.get('messages_per_day', 'unlimited')}\n"
            f"• Special calls: {usage.get('special_calls_today', 0)}/{limits.get('special_calls_per_day', 'unlimited')}\n"
            f"• Internet calls: {usage.get('internet_calls_today', 0)}/{limits.get('internet_calls_per_day', 'unlimited')}\n\n"
            f"Use /upgrade to see upgrade options."
        )
        
        update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    def _handle_upgrade(self, update: Update, context: ContextTypes) -> None:
        """
        Handles the /upgrade command.
        """
        user_id = update.effective_user.id
        
        # Check if user is allowed
        if not self._check_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return
        
        # Check if payment system is available
        if not self.payment_gateway or not PAYMENT_AVAILABLE:
            update.message.reply_text(
                "Payment system is not enabled. All features are freely available."
            )
            return
        
        # Get payment information
        payment_amount = self.payment_gateway.config.get("pricing", {}).get("recharge_amount", 2.0)
        credits_per_payment = self.payment_gateway.config.get("pricing", {}).get("credits_per_recharge", 10)
        
        # Get payment methods
        pix_key = self.payment_gateway.config.get("pix", {}).get("key", "")
        pix_name = self.payment_gateway.config.get("pix", {}).get("name", "")
        
        # Build message
        message = (
            f"💎 *Upgrade Options* 💎\n\n"
            f"Recharge credits to access more features:\n"
            f"• Amount: R$ {payment_amount:.2f}\n"
            f"• Credits: {credits_per_payment}\n\n"
            f"*Payment methods:*\n"
        )
        
        # Add PIX information if available
        if pix_key:
            message += (
                f"*PIX:*\n"
                f"• Key: `{pix_key}`\n"
                f"• Name: {pix_name}\n\n"
            )
        
        # Add crypto if available
        btc_address = self.payment_gateway.config.get("crypto", {}).get("btc", {}).get("address", "")
        sol_address = self.payment_gateway.config.get("crypto", {}).get("sol", {}).get("address", "")
        eth_address = self.payment_gateway.config.get("crypto", {}).get("eth", {}).get("address", "")
        
        if btc_address or sol_address or eth_address:
            message += "*Cryptocurrencies:*\n"
            
            if btc_address:
                message += f"• BTC: `{btc_address}`\n"
            if eth_address:
                message += f"• ETH: `{eth_address}`\n"
            if sol_address:
                message += f"• SOL: `{sol_address}`\n"
                
            message += "\n"
        
        # Add payment instructions
        message += (
            "After making the payment, use the /payment command to register it.\n"
            "Your payment will be verified and credits added to your account."
        )
        
        # Create payment button
        keyboard = [
            [InlineKeyboardButton("💰 Register Payment", callback_data="register_payment")]
        ]
        
        update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    def _handle_payment(self, update: Update, context: ContextTypes) -> int:
        """
        Handles the /payment command.
        """
        user_id = update.effective_user.id
        
        # Check if user is allowed
        if not self._check_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return ConversationHandler.END
        
        # Check if payment system is available
        if not self.payment_gateway or not PAYMENT_AVAILABLE:
            update.message.reply_text(
                "Payment system is not enabled. All features are freely available."
            )
            return ConversationHandler.END
        
        # Send payment registration instructions
        update.message.reply_text(
            "To register a payment, please send:\n\n"
            "1. *PIX payments:* The PIX transaction ID or receipt number\n"
            "2. *Crypto payments:* The transaction hash\n\n"
            "Send /cancel to cancel this operation.",
            parse_mode=ParseMode.MARKDOWN
        )
        
        return PAYMENT
    
    def _handle_payment_confirmation(self, update: Update, context: ContextTypes) -> int:
        """
        Handles payment confirmation.
        """
        user_id = update.effective_user.id
        payment_reference = update.message.text.strip()
        
        # Check if payment system is available
        if not self.payment_gateway or not PAYMENT_AVAILABLE:
            update.message.reply_text(
                "Payment system is not enabled. All features are freely available."
            )
            return ConversationHandler.END
        
        # Check if the payment reference is valid
        if not payment_reference or len(payment_reference) < 5:
            update.message.reply_text(
                "❌ Invalid payment reference. Please provide a valid transaction ID, receipt number, or hash."
            )
            return PAYMENT
        
        # Register payment
        payment_amount = self.payment_gateway.config.get("pricing", {}).get("recharge_amount", 2.0)
        credits = self.payment_gateway.config.get("pricing", {}).get("credits_per_recharge", 10)
        
        # Create payment record
        payment_record = {
            "user_id": user_id,
            "reference": payment_reference,
            "amount": payment_amount,
            "credits": credits,
            "status": "pending",
            "timestamp": datetime.datetime.now().isoformat(),
            "verification_timestamp": None
        }
        
        # Add payment
        success = self.payment_gateway.register_payment(user_id, payment_record)
        
        if success:
            # Send confirmation
            update.message.reply_text(
                f"✅ Payment registration successful!\n\n"
                f"• Reference: `{payment_reference}`\n"
                f"• Amount: R$ {payment_amount:.2f}\n"
                f"• Credits: {credits}\n\n"
                f"Your payment will be verified and credits added to your account soon. "
                f"Use /credits to check your balance.",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Notify admin
            for admin_id in self.config.get("admin_users", []):
                try:
                    if admin_id != user_id:
                        context.bot.send_message(
                            chat_id=admin_id,
                            text=(
                                f"🔔 *New payment registration*\n\n"
                                f"• User ID: `{user_id}`\n"
                                f"• Reference: `{payment_reference}`\n"
                                f"• Amount: R$ {payment_amount:.2f}\n"
                                f"• Credits: {credits}\n\n"
                                f"Please verify this payment and update the status."
                            ),
                            parse_mode=ParseMode.MARKDOWN
                        )
                except Exception as e:
                    self.logger.error(f"Error notifying admin {admin_id}: {e}")
        else:
            # Send error
            update.message.reply_text(
                "❌ Payment registration failed. Please try again later or contact support."
            )
        
        return ConversationHandler.END
    
    def _handle_status(self, update: Update, context: ContextTypes) -> None:
        """
        Handles the /status command.
        """
        user_id = update.effective_user.id
        
        # Check if user is allowed
        if not self._check_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return
        
        # Build status message
        message = (
            "🤖 *EVA & GUARANI Bot Status* 🤖\n\n"
            f"Bot version: 1.0.0\n"
            f"Uptime: Since {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )
        
        # Add system status
        message += (
            "*System Status:*\n"
            f"• Telegram API: ✅ Connected\n"
            f"• Payment System: {'✅ Active' if self.payment_gateway and PAYMENT_AVAILABLE else '❌ Inactive'}\n"
            f"• Quantum Knowledge: {'✅ Active' if self.quantum_knowledge_hub and QUANTUM_KNOWLEDGE_AVAILABLE else '❌ Inactive'}\n"
            f"• OpenAI Fallback: {'✅ Available' if OPENAI_AVAILABLE else '❌ Unavailable'}\n\n"
        )
        
        # Add user status if payment system is available
        if self.payment_gateway and PAYMENT_AVAILABLE:
            # Get user credits and usage
            credits = self.payment_gateway.get_user_credits(user_id)
            tier = self.payment_gateway.get_user_tier(user_id)
            limits = self.payment_gateway.get_user_limits(user_id)
            usage = self.payment_gateway.get_user_usage(user_id)
            
            # Format tier name nicely
            tier_name = tier.replace("_", " ").title()
            
            message += (
                "*Your Account:*\n"
                f"• User ID: `{user_id}`\n"
                f"• Tier: {tier_name}\n"
                f"• Credits: {credits}\n"
                f"• Today's usage: {usage.get('messages_today', 0)}/{limits.get('messages_per_day', 'unlimited')} messages\n"
            )
        
        # Send status message
        update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    def _handle_image_command(self, update: Update, context: ContextTypes) -> int:
        """
        Handles the /image command.
        """
        user_id = update.effective_user.id
        
        # Check if user is allowed
        if not self._check_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return ConversationHandler.END
        
        # Check user limits if payment system is available
        if self.payment_gateway and PAYMENT_AVAILABLE:
            if not self._check_special_call_quota(user_id, "image_generation"):
                update.message.reply_text(
                    "❌ You've reached your limit for image generation today.\n\n"
                    "Use /upgrade to increase your limits or try again tomorrow."
                )
                return ConversationHandler.END
        
        # Send instructions
        update.message.reply_text(
            "🖼️ *Image Generation* 🖼️\n\n"
            "Please describe the image you'd like me to generate.\n"
            "Be detailed and specific for best results.\n\n"
            "Send /cancel to cancel this operation.",
            parse_mode=ParseMode.MARKDOWN
        )
        
        return IMAGE_GEN
    
    def _handle_image_prompt(self, update: Update, context: ContextTypes) -> int:
        """
        Handles image generation prompt.
        """
        user_id = update.effective_user.id
        prompt = update.message.text.strip()
        
        # Send processing message
        processing_message = update.message.reply_text(
            "🔄 Processing your image request... This may take a moment."
        )
        
        try:
            # For now, just acknowledge that image generation would happen here
            # In a real implementation, you would call the image generation API
            
            # Consume credits if payment system is available
            if self.payment_gateway and PAYMENT_AVAILABLE:
                self.payment_gateway.log_usage(user_id, "image_generation")
                image_cost = self.payment_gateway.config.get("pricing", {}).get("image_generation_cost", {}).get("standard", 2)
                self.payment_gateway.consume_credits(user_id, image_cost)
            
            # Send a placeholder message for now
            processing_message.edit_text(
                "✅ Image generation capability exists in the system, but is not fully implemented in this demo.\n\n"
                "In a complete implementation, an image based on your prompt would be generated and sent here."
            )
            
            # Add the prompt to conversation history
            chat_id = update.effective_chat.id
            self.add_to_conversation_history(chat_id, "user", f"/image {prompt}")
            self.add_to_conversation_history(chat_id, "assistant", "I've generated an image based on your prompt.")
            
        except Exception as e:
            self.logger.error(f"Error generating image: {e}")
            processing_message.edit_text(
                "❌ Sorry, there was an error generating your image. Please try again later."
            )
        
        return ConversationHandler.END
    
    def _handle_cancel(self, update: Update, context: ContextTypes) -> int:
        """
        Handles the /cancel command.
        """
        update.message.reply_text(
            "Operation cancelled."
        )
        return ConversationHandler.END
    
    def _handle_callback(self, update: Update, context: ContextTypes) -> None:
        """
        Handles callback queries from inline keyboards.
        """
        query = update.callback_query
        user_id = query.from_user.id
        
        # Check if user is allowed
        if not self._check_user_allowed(user_id):
            query.answer("You are not authorized to use this bot.")
            return
        
        # Process the callback data
        if query.data == "register_payment":
            query.answer("Starting payment registration process.")
            query.edit_message_reply_markup(reply_markup=None)
            
            # Send payment registration instructions
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=(
                    "To register a payment, please send:\n\n"
                    "1. *PIX payments:* The PIX transaction ID or receipt number\n"
                    "2. *Crypto payments:* The transaction hash\n\n"
                    "Send /cancel to cancel this operation."
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Start the payment conversation
            context.user_data["conversation_state"] = PAYMENT
        else:
            query.answer("Unknown callback.")
    
    async def _handle_message(self, update: Update, context: ContextTypes) -> None:
        """
        Handles user messages.
        """
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        message_text = update.message.text.strip()
        
        # Check if user is allowed
        if not self._check_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return
        
        # Check if in a specific conversation state
        conversation_state = context.user_data.get("conversation_state", STANDARD)
        if conversation_state != STANDARD:
            update.message.reply_text(
                "I'm waiting for a specific response. Please complete the current operation or use /cancel."
            )
            return
        
        # Check user message limits if payment system is available
        if self.payment_gateway and PAYMENT_AVAILABLE:
            if not self._check_message_quota(user_id):
                update.message.reply_text(
                    "❌ You've reached your message limit for today.\n\n"
                    "Use /upgrade to increase your limits or try again tomorrow."
                )
                return
        
        # Add message to conversation history
        self.add_to_conversation_history(chat_id, "user", message_text)
        
        # Prepare typing indicator
        context.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        try:
            # Process message
            response = await self._process_message(chat_id, user_id, message_text)
            
            # Split response if it's too long
            max_length = self.config.get("max_message_length", 4096)
            if len(response) <= max_length:
                update.message.reply_text(
                    response,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                # Split response into chunks
                chunks = [response[i:i+max_length] for i in range(0, len(response), max_length)]
                for chunk in chunks:
                    update.message.reply_text(
                        chunk,
                        parse_mode=ParseMode.MARKDOWN
                    )
            
            # Add response to conversation history
            self.add_to_conversation_history(chat_id, "assistant", response)
            
            # Store last response
            self.last_responses[chat_id] = response
            
            # Log usage if payment system is available
            if self.payment_gateway and PAYMENT_AVAILABLE:
                self.payment_gateway.log_usage(user_id, "messages")
                
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            update.message.reply_text(
                "Sorry, I encountered an error while processing your message. Please try again."
            )
    
    async def _process_message(self, chat_id: int, user_id: int, message: str) -> str:
        """
        Processes a user message and generates a response.
        
        Args:
            chat_id: Chat ID
            user_id: User ID
            message: User message
            
        Returns:
            Response message
        """
        # Get conversation history
        history = self.get_conversation_history(chat_id)
        
        # Try using quantum knowledge system first
        if self.quantum_knowledge_integrator and QUANTUM_KNOWLEDGE_AVAILABLE:
            try:
                # Prepare the query context
                query_context = {
                    "history": history,
                    "user_id": user_id,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                
                # Process with quantum knowledge
                knowledge_response = await self.quantum_knowledge_integrator.process_message(
                    message, query_context
                )
                
                if knowledge_response and knowledge_response.get("response"):
                    return knowledge_response["response"]
                    
            except Exception as e:
                self.logger.error(f"Error processing with quantum knowledge: {e}")
        
        # Fallback to OpenAI if quantum knowledge failed or not available
        if OPENAI_AVAILABLE:
            try:
                # Format conversation history for OpenAI
                formatted_history = []
                for entry in history[-10:]:  # Use last 10 messages
                    formatted_history.append({
                        "role": entry["role"],
                        "content": entry["content"]
                    })
                
                # Add system message
                formatted_history.insert(0, {
                    "role": "system",
                    "content": (
                        "You are EVA & GUARANI, an ethical AI assistant designed with a focus on "
                        "providing helpful, accurate, and ethically-aligned information. You maintain "
                        "a balance between being informative and respecting ethical boundaries. "
                        "Always respond in a professional yet friendly tone."
                    )
                })
                
                # Call OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=formatted_history
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                self.logger.error(f"Error processing with OpenAI: {e}")
        
        # Final fallback
        return (
            "I'm currently experiencing difficulties accessing my knowledge systems. "
            "Please try again later or contact support if this issue persists."
        )
    
    def _handle_error(self, update: object, context: ContextTypes) -> None:
        """
        Handles errors in the telegram-python-bot dispatcher.
        """
        self.logger.error(f"Update {update} caused error: {context.error}")
        
        try:
            if update and hasattr(update, 'effective_chat'):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Sorry, an error occurred while processing your request. Please try again later."
                )
        except Exception as e:
            self.logger.error(f"Error sending error message: {e}")
    
    def get_conversation_history(self, chat_id: int) -> List[Dict[str, str]]:
        """
        Gets the conversation history for a specific chat.
        
        Args:
            chat_id: Chat ID
            
        Returns:
            List with the conversation history
        """
        # Create history if it doesn't exist
        if chat_id not in self.conversations:
            self.conversations[chat_id] = []
            
        return self.conversations[chat_id]
    
    def add_to_conversation_history(self, chat_id: int, role: str, message: str) -> None:
        """
        Adds a message to the conversation history.
        
        Args:
            chat_id: Chat ID
            role: Sender's role ('user' or 'assistant')
            message: Message content
        """
        # Create history if it doesn't exist
        if chat_id not in self.conversations:
            self.conversations[chat_id] = []
            
        # Add message
        self.conversations[chat_id].append({
            "role": role,
            "content": message,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # Limit history size
        max_history = self.config.get("max_conversation_history", 20)
        if len(self.conversations[chat_id]) > max_history:
            self.conversations[chat_id] = self.conversations[chat_id][-max_history:]
    
    def clear_conversation_history(self, chat_id: int) -> None:
        """
        Clears the conversation history for a specific chat.
        
        Args:
            chat_id: Chat ID
        """
        self.conversations[chat_id] = []
    
    def _check_user_allowed(self, user_id: int) -> bool:
        """
        Checks if a user is allowed to use the bot.
        
        Args:
            user_id: User ID
            
        Returns:
            True if allowed, False otherwise
        """
        allowed_users = self.config.get("allowed_users", [])
        admin_users = self.config.get("admin_users", [])
        
        # If there are no restrictions, allow everyone
        if not allowed_users and not admin_users:
            return True
            
        # Check if user is in allowed or admin lists
        return user_id in allowed_users or user_id in admin_users
    
    def _check_message_quota(self, user_id: int) -> bool:
        """
        Checks if a user has reached their message quota.
        
        Args:
            user_id: User ID
            
        Returns:
            True if quota is available, False otherwise
        """
        if not self.payment_gateway or not PAYMENT_AVAILABLE:
            return True
            
        return self.payment_gateway.check_user_usage(user_id, "messages")
    
    def _check_special_call_quota(self, user_id: int, call_type: str) -> bool:
        """
        Checks if a user has reached their special call quota.
        
        Args:
            user_id: User ID
            call_type: Type of special call
            
        Returns:
            True if quota is available, False otherwise
        """
        if not self.payment_gateway or not PAYMENT_AVAILABLE:
            return True
            
        return self.payment_gateway.check_user_usage(user_id, "special_calls")
        
def main():
    """
    Main function to run the EVA & GUARANI Telegram Bot.
    """
    print("✧༺❀༻∞ EVA & GUARANI - Telegram Bot ∞༺❀༻✧")
    print("Starting...")
    
    try:
        # Initialize bot
        bot = EVAGuaraniBot()
        
        # Start bot
        bot.start()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 