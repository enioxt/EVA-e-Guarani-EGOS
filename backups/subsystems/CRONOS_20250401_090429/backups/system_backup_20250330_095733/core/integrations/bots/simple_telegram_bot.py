#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Telegram Bot (avatechartbot)
============================================

Telegram bot for EVA & GUARANI that combines AI capabilities with image/video
generation, knowledge base access, and more. The bot provides a user-friendly
interface to the powerful EVA & GUARANI system.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.1.0
"""

import os
import json
import logging
import datetime
import sys
import traceback
import requests
import asyncio
import random
import base64
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "modules/quantum"))
sys.path.append(os.path.join(project_root, "tools/utilities"))

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

# Import telegram bot package
try:
    from telegram import Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
    from telegram.ext import (
        Updater, CommandHandler, MessageHandler, Filters,
        CallbackContext, ConversationHandler, CallbackQueryHandler
    )
    TELEGRAM_AVAILABLE = True
except ImportError:
    logger.error("Python-telegram-bot not found. Run: pip install python-telegram-bot==13.15")
    sys.exit(1)

# Try to import OpenAI for responding to messages
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    logger.warning("OpenAI not available. Bot will use fallback responses.")
    OPENAI_AVAILABLE = False

# Try to import Pillow for image processing
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    logger.warning("Pillow not available. Image processing features will be limited.")
    PILLOW_AVAILABLE = False

# Try to import quantum knowledge system
QUANTUM_KNOWLEDGE_AVAILABLE = False
try:
    # We import it dynamically to avoid problems with module resolution
    sys.path.append(os.path.join(project_root, "modules", "quantum"))
    # Import conditionally to avoid errors
    QuantumKnowledgeHub = None

    # Try to dynamically load the class
    def get_quantum_class():
        try:
            from modules.quantum.quantum_knowledge_hub import QuantumKnowledgeHub as QKH
            return QKH
        except ImportError:
            try:
                # Alternative paths
                from quantum_knowledge_hub import QuantumKnowledgeHub as QKH
                return QKH
            except ImportError:
                return None

    QuantumKnowledgeHub = get_quantum_class()
    if QuantumKnowledgeHub is not None:
        QUANTUM_KNOWLEDGE_AVAILABLE = True
    else:
        logger.warning("Could not locate QuantumKnowledgeHub class.")
except Exception as e:
    logger.warning(f"Quantum knowledge system not found: {e}")

# Try to import payment module
PAYMENT_AVAILABLE = False
try:
    from tools.utilities.payment_gateway import PaymentGateway
    PAYMENT_AVAILABLE = True
except ImportError:
    logger.warning("Payment system not available. Credit-based features will be limited.")

# Conversation states
STANDARD = 0
IMAGE_GEN = 1
VIDEO_GEN = 2
KNOWLEDGE_QUERY = 3
PAYMENT = 4

class EvaTelegramBot:
    """
    Enhanced Telegram Bot for EVA & GUARANI with media generation and knowledge access.
    """

    def __init__(self, config_path: str = os.path.join(current_dir, "telegram_config.json")):
        """Initialize the bot"""
        self.logger = logger
        self.logger.info("Initializing EVA & GUARANI Telegram Bot")

        # Load configuration
        self.config_path = Path(config_path)
        self.config = self._load_config()

        # Initialize state
        self.conversations = {}  # {chat_id: [messages]}
        self.user_states = {}    # {user_id: state}
        self.started = False
        self.start_time = datetime.datetime.now()

        # Initialize token from config
        self.token = self.config.get("token", "")
        self.bot_name = self.config.get("bot_name", "avatechartbot")
        if not self.token:
            self.logger.error("Bot token not configured in telegram_config.json")
            raise ValueError("Bot token not configured")

        # Initialize knowledge hub if available
        self.knowledge_hub = None
        if QUANTUM_KNOWLEDGE_AVAILABLE and self.config.get("knowledge", {}).get("enabled", True):
            try:
                hub_config_path = self.config.get("knowledge", {}).get("hub_config_path", "")
                if QuantumKnowledgeHub is not None:
                    self.knowledge_hub = QuantumKnowledgeHub(hub_config_path)
                    self.logger.info("Quantum Knowledge Hub initialized")
            except Exception as e:
                self.logger.error(f"Error initializing Knowledge Hub: {e}")

        # Initialize payment gateway if available
        self.payment_gateway = None
        if PAYMENT_AVAILABLE and self.config.get("payment", {}).get("enabled", True):
            try:
                payment_config_path = self.config.get("payment", {}).get("config_path", "")
                if payment_config_path:
                    self.payment_gateway = PaymentGateway(payment_config_path)
                    self.logger.info("Payment Gateway initialized")
            except Exception as e:
                self.logger.error(f"Error initializing payment gateway: {e}")

        self.logger.info(f"EVA & GUARANI Telegram Bot '{self.bot_name}' initialized")

    def _load_config(self):
        """Load configuration from file"""
        default_config = {
            "token": "",
            "bot_name": "avatechartbot",
            "admin_users": [],
            "allowed_users": [],
            "max_conversation_history": 10,
            "startup_notification": True
        }

        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            else:
                self.logger.warning(f"Config file not found at {self.config_path}")
                return default_config
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return default_config

    def start(self):
        """Start the bot"""
        self.logger.info("Starting EVA & GUARANI Telegram Bot")

        # Initialize the updater with bot token
        updater = Updater(self.token, use_context=True)
        dp = updater.dispatcher

        # Add handlers for commands
        dp.add_handler(CommandHandler("start", self._handle_start))
        dp.add_handler(CommandHandler("help", self._handle_help))
        dp.add_handler(CommandHandler("status", self._handle_status))
        dp.add_handler(CommandHandler("credits", self._handle_credits))

        # Add callback query handler for inline keyboards
        dp.add_handler(CallbackQueryHandler(self._handle_callback))

        # Payment handlers
        payment_conv_handler = ConversationHandler(
            entry_points=[CommandHandler('payment', self._handle_payment)],
            states={
                PAYMENT: [
                    MessageHandler(
                        Filters.text & ~Filters.command,
                        self._handle_payment_confirmation
                    )
                ],
            },
            fallbacks=[CommandHandler('cancel', self._handle_cancel)]
        )
        dp.add_handler(payment_conv_handler)

            # Create simple conversation handler for image command
            image_conv_handler = ConversationHandler(
                entry_points=[CommandHandler('image', self._handle_image_command)],
                states={
                    IMAGE_GEN: [MessageHandler(Filters.text & ~Filters.command, self._handle_image_prompt)],
                },
                fallbacks=[CommandHandler('cancel', self._handle_cancel)],
            )
        dp.add_handler(image_conv_handler)

            # Register basic message handler
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self._handle_message))

            # Register error handler
        dp.add_error_handler(self._handle_error)

            # Start the bot
            updater.start_polling()
            self.started = True
            self.logger.info(f"Bot '{self.bot_name}' started successfully")

            # Send startup notification to admin users
            if self.config.get("startup_notification", True):
                self._send_startup_notification(updater.bot)

            # Keep the bot running
            updater.idle()

    def _send_startup_notification(self, bot):
        """Send notification to admin users when the bot starts"""
        try:
            admin_users = self.config.get("admin_users", [])
            for admin_id in admin_users:
                bot.send_message(
                    chat_id=admin_id,
                    text=(
                        f"🤖 *{self.bot_name} is now online!* 🤖\n\n"
                        f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"Version: 1.1.0\n\n"
                        f"Features enabled:\n"
                        f"• AI Chat: {'✅' if OPENAI_AVAILABLE else '❌'}\n"
                        f"• Knowledge Base: {'✅' if QUANTUM_KNOWLEDGE_AVAILABLE and self.knowledge_hub else '❌'}\n"
                        f"• Image Generation: {'✅' if self.config.get('media_generation', {}).get('enabled', False) else '❌'}\n\n"
                        f"Ready to serve users!\n\n"
                        f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                self.logger.info(f"Startup notification sent to admin {admin_id}")
        except Exception as e:
            self.logger.error(f"Error sending startup notification: {e}")

    def _handle_start(self, update: Update, context: CallbackContext):
        """Handle the /start command"""
        if update is None or update.effective_user is None:
            return

        user_id = update.effective_user.id
        chat_id = update.effective_chat.id if update.effective_chat else None

        # Check if user is allowed
        if not self._is_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return

        # Reset conversation history
        if chat_id:
            self.conversations[chat_id] = []

        # Send welcome message
        welcome_message = (
            f"Hello! I'm *{self.bot_name}*, the EVA & GUARANI AI assistant.\n\n"
            "I can help you with a wide range of tasks including:\n"
            "• AI conversations with ethical foundations\n"
            "• Image and video generation\n"
            "• Knowledge base access\n\n"
            "Use /help to see all available commands."
        )

        # Create quick access buttons
        keyboard = [
            [InlineKeyboardButton("🖼️ Generate Image", callback_data="cmd_image")],
            [InlineKeyboardButton("🔍 Access Knowledge", callback_data="cmd_knowledge")]
        ]

        update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def _handle_help(self, update: Update, context: CallbackContext):
        """Handle the /help command"""
        if update is None or update.effective_user is None:
            return

        user_id = update.effective_user.id

        # Check if user is allowed
        if not self._is_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return

        help_message = (
            "🌟 *EVA & GUARANI Commands* 🌟\n\n"
            "Basic Commands:\n"
            "• /start - Start or restart conversation\n"
            "• /help - Show this help message\n"
            "• /status - Check bot status\n"
            "• /credits - About EVA & GUARANI\n\n"
            "Media Generation:\n"
            "• /image - Generate images from text descriptions\n\n"
            "You can also simply chat with me by typing a message!\n\n"
            "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
        )

        update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)

    def _handle_credits(self, update: Update, context: CallbackContext):
        """Handle the /credits command"""
        if update is None or update.effective_user is None:
            return

        user_id = update.effective_user.id

        # Check if user is allowed
        if not self._is_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return

        # Check if payment system is available
        if not self.payment_gateway or not PAYMENT_AVAILABLE:
            update.message.reply_text(
                "Credit system is not enabled. All features are freely available.\n\n"
            "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
        )
            return

        try:
            # Get user tier
            user_tier = self.payment_gateway.get_user_tier(user_id)

            # Get user credits
            user_credits = self.payment_gateway.get_user_credits(user_id)

            # Get user limits
            user_limits = self.payment_gateway.get_user_limits(user_id)

            # Format tier name for display
            tier_display = {
                "free_tier": "🔹 Free Tier",
                "supporter_tier": "🔶 Supporter Tier",
                "premium_tier": "💎 Premium Tier"
            }.get(user_tier, "Unknown Tier")

            # Format message
            message = (
                f"💰 *Credits & Usage Information* 💰\n\n"
                f"*Current Tier:* {tier_display}\n\n"
                f"*Available Credits:*\n"
                f"• Special calls: {user_credits.get('special_calls', 0)}\n"
                f"• Internet calls: {user_credits.get('internet_calls', 0)}\n\n"
                f"*Daily Limits:*\n"
                f"• Messages: {user_limits.get('messages_per_day', 0)} per day\n"
                f"• Special calls: {user_limits.get('special_calls_per_day', 0)} per day\n"
                f"• Internet calls: {user_limits.get('internet_calls_per_day', 0)} per day\n\n"
                f"To add more credits, use the /payment command.\n\n"
                f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            )

            # Create keyboard
            keyboard = [
                [InlineKeyboardButton("💰 Add Credits", callback_data="payment")]
            ]

            update.message.reply_text(
                message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            self.logger.error(f"Error getting user credits: {e}")
            update.message.reply_text(
                "Sorry, there was an error retrieving your credit information.\n\n"
                "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            )

    def _handle_status(self, update: Update, context: CallbackContext):
        """Handle the /status command"""
        if update is None or update.effective_user is None:
            return

        user_id = update.effective_user.id

        # Check if user is allowed
        if not self._is_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return

        # Calculate uptime
        uptime = datetime.datetime.now() - self.start_time
        days, seconds = uptime.days, uptime.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"

        status_message = (
            f"🤖 *{self.bot_name} Status* 🤖\n\n"
            f"Bot version: 1.1.0\n"
            f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Uptime: {uptime_str}\n\n"
            "*System Status:*\n"
            f"• Telegram API: ✅ Connected\n"
            f"• OpenAI Integration: {'✅ Active' if OPENAI_AVAILABLE else '❌ Inactive'}\n"
            f"• Knowledge Base: {'✅ Active' if QUANTUM_KNOWLEDGE_AVAILABLE and self.knowledge_hub else '❌ Inactive'}\n"
            f"• Image Generation: {'✅ Active' if self.config.get('media_generation', {}).get('enabled', False) else '❌ Inactive'}\n\n"
            "*Your Account:*\n"
            f"• User ID: `{user_id}`\n"
        )

        update.message.reply_text(status_message, parse_mode=ParseMode.MARKDOWN)

    def _handle_image_command(self, update: Update, context: CallbackContext):
        """Handle the /image command"""
        if update is None or update.effective_user is None:
            return ConversationHandler.END

        user_id = update.effective_user.id

        # Check if user is allowed
        if not self._is_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return ConversationHandler.END

        # Check if image generation is enabled
        if not self.config.get("media_generation", {}).get("enabled", False):
            update.message.reply_text(
                "❌ Image generation is currently disabled.\n\n"
                "Please try again later or contact the administrator."
            )
            return ConversationHandler.END

        # Send instructions
        update.message.reply_text(
            "🖼️ *Image Generation* 🖼️\n\n"
            "Please describe the image you'd like me to create.\n"
            "Be detailed and specific for best results.\n\n"
            "Examples:\n"
            "• \"A mystical forest with glowing mushrooms and a small cabin\"\n"
            "• \"A futuristic city with flying cars and holographic billboards\"\n\n"
            "Send /cancel to cancel this operation.",
            parse_mode=ParseMode.MARKDOWN
        )

        # Set user state
        self.user_states[user_id] = IMAGE_GEN

        return IMAGE_GEN

    def _handle_image_prompt(self, update: Update, context: CallbackContext):
        """Handle image generation prompt"""
        if update is None or update.effective_user is None:
            return ConversationHandler.END

        user_id = update.effective_user.id
        chat_id = update.effective_chat.id if update.effective_chat else None
        prompt = update.message.text.strip()

        # Set processing message
        processing_message = update.message.reply_text(
            "🔄 Processing your image request... This may take a moment."
        )

        try:
            # Check if the user has enough credits for image generation
            if PAYMENT_AVAILABLE and self.payment_gateway:
                # Check if user has credits for special calls
                if not self.payment_gateway.check_user_usage(user_id, "special_calls"):
                    processing_message.edit_text(
                        "❌ You don't have enough credits for image generation.\n\n"
                        "Please use /payment to add more credits to your account.\n\n"
                        "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                    )
                    return ConversationHandler.END

            # Get available image APIs
            image_apis = self.config.get("media_generation", {}).get("image_apis", {})

            # Try to generate image with any available API
            image_generated = False
            error_message = ""

            # Try Stable Diffusion API first
            if "stable_diffusion" in image_apis and image_apis["stable_diffusion"].get("key") not in ["", "YOUR_KEY_HERE"]:
                try:
                    # Call Stable Diffusion API
                    sd_api = image_apis["stable_diffusion"]
                    sd_url = sd_api.get("url", "https://stablediffusionapi.com/api/v3/text2img")
                    sd_key = sd_api.get("key", "")

                    payload = {
                        "key": sd_key,
                        "prompt": prompt,
                        "negative_prompt": "watermark, text, poor quality, deformed",
                        "width": "512",
                        "height": "512",
                        "samples": "1",
                        "num_inference_steps": "30",
                        "safety_checker": "yes",
                        "enhance_prompt": "yes",
                        "guidance_scale": 7.5
                    }

                    response = requests.post(sd_url, json=payload)
                    response_data = response.json()

                    if response.status_code == 200 and response_data.get("status") == "success":
                        # Get image URL
                        image_url = response_data.get("output", [])[0]

                        # Send image to user
                        context.bot.send_photo(
                            chat_id=chat_id,
                            photo=image_url,
                            caption=f"🖼️ Image generated based on your prompt:\n\n\"{prompt}\"\n\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                        )

                        # Mark as successful
                        image_generated = True

                        # Deduct credits if payment system is available
                        if PAYMENT_AVAILABLE and self.payment_gateway:
                            self.payment_gateway._check_credits(user_id, "special_calls")
                    else:
                        error_message = f"Stable Diffusion API error: {response_data.get('message', 'Unknown error')}"
                        self.logger.error(f"Stable Diffusion API error: {response_data}")
                except Exception as e:
                    error_message = f"Error with Stable Diffusion API: {str(e)}"
                    self.logger.error(f"Error with Stable Diffusion API: {e}")

            # If Stable Diffusion failed, try Unsplash for real photos
            if not image_generated and "unsplash" in image_apis and image_apis["unsplash"].get("key") not in ["", "YOUR_KEY_HERE"]:
                try:
                    # Call Unsplash API
                    unsplash_api = image_apis["unsplash"]
                    unsplash_url = unsplash_api.get("url", "https://api.unsplash.com/photos/random")
                    unsplash_key = unsplash_api.get("key", "")

                    # Prepare parameters
                    params = {
                        "query": prompt,
                        "count": 1,
                        "client_id": unsplash_key
                    }

                    response = requests.get(unsplash_url, params=params)

                    if response.status_code == 200:
                        response_data = response.json()
                        if isinstance(response_data, list) and len(response_data) > 0:
                            # Get image URL
                            image_data = response_data[0]
                            image_url = image_data.get("urls", {}).get("regular", "")

                            if image_url:
                                # Send image to user
                                context.bot.send_photo(
                                    chat_id=chat_id,
                                    photo=image_url,
                                    caption=(
                                        f"📸 Photo from Unsplash based on your prompt:\n\n"
                                        f"\"{prompt}\"\n\n"
                                        f"Photo by: {image_data.get('user', {}).get('name', 'Unknown')}\n\n"
                                        f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                                    )
                                )

                                # Mark as successful
                                image_generated = True

                                # Deduct credits if payment system is available
                                if PAYMENT_AVAILABLE and self.payment_gateway:
                                    self.payment_gateway._check_credits(user_id, "special_calls")
                    else:
                        error_message += f"\nUnsplash API error: {response.status_code}"
                        self.logger.error(f"Unsplash API error: {response.text}")
                except Exception as e:
                    error_message += f"\nError with Unsplash API: {str(e)}"
                    self.logger.error(f"Error with Unsplash API: {e}")

            # If nothing worked, try Pexels as last resort
            if not image_generated and "pexels" in image_apis and image_apis["pexels"].get("key") not in ["", "YOUR_KEY_HERE"]:
                try:
                    # Call Pexels API
                    pexels_api = image_apis["pexels"]
                    pexels_url = pexels_api.get("url", "https://api.pexels.com/v1/search")
                    pexels_key = pexels_api.get("key", "")

                    # Prepare headers and parameters
                    headers = {
                        "Authorization": pexels_key
                    }

                    params = {
                        "query": prompt,
                        "per_page": 1
                    }

                    response = requests.get(pexels_url, headers=headers, params=params)

                    if response.status_code == 200:
                        response_data = response.json()
                        photos = response_data.get("photos", [])

                        if photos and len(photos) > 0:
                            # Get image URL
                            photo = photos[0]
                            image_url = photo.get("src", {}).get("original", "")

                            if image_url:
                                # Send image to user
                                context.bot.send_photo(
                                    chat_id=chat_id,
                                    photo=image_url,
                                    caption=(
                                        f"📸 Stock photo from Pexels based on your prompt:\n\n"
                                        f"\"{prompt}\"\n\n"
                                        f"Photo by: {photo.get('photographer', 'Unknown')}\n\n"
                                        f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                                    )
                                )

                                # Mark as successful
                                image_generated = True

                                # Deduct credits if payment system is available
                                if PAYMENT_AVAILABLE and self.payment_gateway:
                                    self.payment_gateway._check_credits(user_id, "special_calls")
                    else:
                        error_message += f"\nPexels API error: {response.status_code}"
                        self.logger.error(f"Pexels API error: {response.text}")
                except Exception as e:
                    error_message += f"\nError with Pexels API: {str(e)}"
                    self.logger.error(f"Error with Pexels API: {e}")

            # If all APIs failed, send error message
            if not image_generated:
                # Check if keys are just placeholders
                all_keys_placeholder = True
                for api_name, api_config in image_apis.items():
                    if api_config.get("key") not in ["", "YOUR_KEY_HERE"]:
                        all_keys_placeholder = False
                        break

                if all_keys_placeholder:
            processing_message.edit_text(
                "🖼️ *Image Generation* 🖼️\n\n"
                        "Image generation is currently being configured. API keys need to be set up by the administrator.\n\n"
                        "Your request has been noted for future implementation once the API keys are set.\n\n"
                        "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧",
                parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    processing_message.edit_text(
                        f"❌ Sorry, I couldn't generate an image based on your prompt.\n\n"
                        f"Error details: {error_message}\n\n"
                        f"Please try again with a different prompt.\n\n"
                        f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                    )
            else:
                # If we sent an image, update the processing message
                processing_message.edit_text(
                    "✅ Image generation successful!\n\n"
                    "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                )

            # Add the prompt to conversation history
            if chat_id:
                self._add_to_conversation(chat_id, "user", f"/image {prompt}")
                if image_generated:
                    self._add_to_conversation(chat_id, "assistant", "Image generated successfully based on your prompt.")
                else:
                    self._add_to_conversation(chat_id, "assistant", "Failed to generate image based on your prompt.")

        except Exception as e:
            self.logger.error(f"Error generating image: {e}")
            processing_message.edit_text(
                "❌ Sorry, there was an error processing your image request. Please try again later.\n\n"
                "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            )

        # Reset user state
        self.user_states[user_id] = STANDARD

        return ConversationHandler.END

    def _handle_cancel(self, update: Update, context: CallbackContext):
        """Handle the /cancel command"""
        if update is None or update.effective_user is None:
            return ConversationHandler.END

        user_id = update.effective_user.id

        # Reset user state
        self.user_states[user_id] = STANDARD

        update.message.reply_text(
            "✅ Operation cancelled."
        )

        return ConversationHandler.END

    def _handle_message(self, update: Update, context: CallbackContext):
        """Handle general messages"""
        if update is None or update.effective_user is None or update.effective_chat is None:
            return

        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        message_text = update.message.text

        # Check if user is allowed
        if not self._is_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return

        # Add message to conversation history
        self._add_to_conversation(chat_id, "user", message_text)

        # Show typing indicator
        context.bot.send_chat_action(chat_id=chat_id, action="typing")

        try:
            # Generate response
            response = self._generate_response(chat_id, message_text)

            # Send response (ensuring it's not None)
            if response:
                update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
                # Add response to conversation history
                self._add_to_conversation(chat_id, "assistant", response)
            else:
                update.message.reply_text(
                    "I'm sorry, I couldn't generate a response at this time. Please try again later.\n\n"
                    "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                )

        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
            update.message.reply_text(
                "Sorry, I encountered an error processing your message. Please try again."
            )

    def _handle_error(self, update, context):
        """Handle errors"""
        self.logger.error(f"Update {update} caused error {context.error}")
        try:
            if update and hasattr(update, 'effective_chat') and update.effective_chat:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Sorry, an error occurred. Please try again later."
                )
        except Exception as e:
            self.logger.error(f"Error sending error message: {e}")

    def _generate_response(self, chat_id, message):
        """Generate a response to a message"""
        if OPENAI_AVAILABLE:
            try:
                # Format history for OpenAI
                history = self._get_conversation_history(chat_id)
                formatted_history = []

                # Add system message
                formatted_history.append({
                    "role": "system",
                    "content": (
                        "You are EVA & GUARANI, an ethical AI assistant designed with a focus on "
                        "providing helpful, accurate, and ethically-aligned information. You maintain "
                        "a balance between being informative and respecting ethical boundaries. "
                        "Always respond in a professional yet friendly tone. Sign your responses with "
                        "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                    )
                })

                # Add conversation history
                formatted_history.extend(history)

                # Call OpenAI API (using v1 client)
                client = openai.OpenAI()
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=formatted_history
                )

                if response and response.choices and len(response.choices) > 0:
                    return response.choices[0].message.content
                else:
                    return None

            except Exception as e:
                self.logger.error(f"Error generating response with OpenAI: {e}")

        # Fallback response
        return (
            "Thank you for your message. I'm currently operating in simple mode without external AI services.\n\n"
            "I can help with basic commands, but for more advanced assistance, "
            "the administrator needs to set up OpenAI integration.\n\n"
            "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
        )

    def _get_conversation_history(self, chat_id):
        """Get conversation history for a chat"""
        if chat_id not in self.conversations:
            self.conversations[chat_id] = []
        return self.conversations[chat_id]

    def _add_to_conversation(self, chat_id, role, content):
        """Add a message to the conversation history"""
        if chat_id not in self.conversations:
            self.conversations[chat_id] = []

        # Add message to history
        self.conversations[chat_id].append({
            "role": role,
            "content": content
        })

        # Limit history size
        max_history = self.config.get("max_conversation_history", 10)
        if len(self.conversations[chat_id]) > max_history:
            self.conversations[chat_id] = self.conversations[chat_id][-max_history:]

    def _is_user_allowed(self, user_id):
        """Check if a user is allowed to use the bot"""
        allowed_users = self.config.get("allowed_users", [])
        admin_users = self.config.get("admin_users", [])

        # If no restrictions are set, allow everyone
        if not allowed_users and not admin_users:
            return True

        return user_id in allowed_users or user_id in admin_users

    def _handle_payment(self, update: Update, context: CallbackContext):
        """Handle the /payment command"""
        if update is None or update.effective_user is None:
            return ConversationHandler.END

        user_id = update.effective_user.id

        # Check if user is allowed
        if not self._is_user_allowed(user_id):
            update.message.reply_text("Sorry, you are not authorized to use this bot.")
            return ConversationHandler.END

        # Check if payment system is available
        if not self.payment_gateway or not PAYMENT_AVAILABLE:
            update.message.reply_text(
                "Payment system is not enabled. All features are freely available."
            )
            return ConversationHandler.END

        # Load payment config
        payment_config = self.payment_gateway.config

        # Format payment methods
        pix_info = payment_config.get("pix", {})
        crypto_info = payment_config.get("crypto", {})

        # Create message
        payment_amount = payment_config.get("pricing", {}).get("recharge_amount", 2.0)
        credits = payment_config.get("pricing", {}).get("credits_per_recharge", 10)

        payment_message = (
            f"💰 *Add Credits - R$ {payment_amount:.2f} for {credits} credits* 💰\n\n"
            f"Please choose one of the payment methods below:\n\n"
        )

        # Add PIX info if available
        if pix_info.get("enabled", False):
            payment_message += (
                f"*🇧🇷 PIX:*\n"
                f"Key: `{pix_info.get('key', '')}`\n"
                f"Name: {pix_info.get('name', '')}\n\n"
            )

        # Add crypto info if available
        if crypto_info:
            payment_message += "*💎 Cryptocurrency:*\n"

            for crypto, info in crypto_info.items():
                if info.get("enabled", False):
                    payment_message += (
                        f"\n*{crypto.upper()}* ({info.get('network', '')})\n"
                        f"`{info.get('address', '')}`\n"
                    )

        payment_message += (
            f"\n\nAfter making the payment, please respond with the transaction ID or hash.\n\n"
            f"Send /cancel to cancel this operation."
        )

        # Send payment message
        update.message.reply_text(
            payment_message,
            parse_mode=ParseMode.MARKDOWN
        )

        return PAYMENT

    def _handle_payment_confirmation(self, update: Update, context: CallbackContext):
        """Handle payment confirmation"""
        if update is None or update.effective_user is None:
            return ConversationHandler.END

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
        payment_amount = self.config.get("payment", {}).get("payment_amount", 2.0)
        credits_per_payment = self.config.get("payment", {}).get("credits_per_payment", 10)

        # Determine payment method (simple detection)
        payment_method = "pix"
        currency = "BRL"
        if payment_reference.startswith("0x") or len(payment_reference) >= 40:
            payment_method = "crypto"
            if "tx.ethereum" in payment_reference or payment_reference.startswith("0x"):
                currency = "ETH"
            elif "txid.bitcoin" in payment_reference:
                currency = "BTC"
            elif "solscan" in payment_reference:
                currency = "SOL"

        # Register payment in the gateway
        success = self.payment_gateway.register_payment(
            user_id=user_id,
            amount=payment_amount,
            currency=currency,
            payment_method=payment_method,
            transaction_id=payment_reference
        )

        if success:
            # Send confirmation
            update.message.reply_text(
                f"✅ Payment registration successful!\n\n"
                f"• Reference: `{payment_reference}`\n"
                f"• Amount: {payment_amount:.2f} {currency}\n"
                f"• Credits: {credits_per_payment}\n\n"
                f"Your credits have been added to your account. "
                f"Use /credits to check your balance.\n\n"
                f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧",
                parse_mode=ParseMode.MARKDOWN
            )

            # Notify admin
            for admin_id in self.config.get("admin_users", []):
                try:
                    if admin_id != user_id:
                        context.bot.send_message(
                            chat_id=admin_id,
                            text=(
                                f"🔔 *New payment registered*\n\n"
                                f"• User ID: `{user_id}`\n"
                                f"• Reference: `{payment_reference}`\n"
                                f"• Amount: {payment_amount:.2f} {currency}\n"
                                f"• Method: {payment_method}\n"
                                f"• Credits: {credits_per_payment}\n\n"
                                f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                            ),
                            parse_mode=ParseMode.MARKDOWN
                        )
                except Exception as e:
                    self.logger.error(f"Error sending admin notification: {e}")
        else:
            # Send error message
            update.message.reply_text(
                "❌ Error registering payment. Please try again or contact the administrator.\n\n"
                "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            )

        return ConversationHandler.END

    def _handle_callback(self, update: Update, context: CallbackContext):
        """Handle callback queries from inline keyboards"""
        if update is None or update.callback_query is None:
            return

        query = update.callback_query
        user_id = query.from_user.id
        data = query.data

        # Check if user is allowed
        if not self._is_user_allowed(user_id):
            query.answer("Sorry, you are not authorized to use this bot.")
            return

        try:
            # Handle different callback data
            if data == "payment":
                # Answer the callback query
                query.answer("Opening payment options...")

                # Forward to payment command
                self._handle_payment(update, context)
            elif data == "help":
                # Answer the callback query
                query.answer("Opening help...")

                # Forward to help command
                self._handle_help(update, context)
            elif data == "status":
                # Answer the callback query
                query.answer("Checking status...")

                # Forward to status command
                self._handle_status(update, context)
            elif data == "credits":
                # Answer the callback query
                query.answer("Checking credits...")

                # Forward to credits command
                self._handle_credits(update, context)
            else:
                query.answer("Unknown command")

        except Exception as e:
            self.logger.error(f"Error handling callback: {e}")
            query.answer("Error processing request")


def main():
    """Main function"""
    print(f"✧༺❀༻∞ EVA & GUARANI - Telegram Bot (avatechartbot) ∞༺❀༻✧")
    print("Starting...")

    try:
        bot = EvaTelegramBot()
        bot.start()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
