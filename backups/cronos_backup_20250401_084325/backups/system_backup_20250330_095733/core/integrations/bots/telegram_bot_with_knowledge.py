#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Telegram Bot with Quantum Knowledge
===================================================

Telegram Bot for EVA & GUARANI that uses the quantum knowledge system
to process messages, maintaining the system's identity and ethics while
using more economical models. This bot demonstrates how to integrate the
quantum knowledge system into a real application.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0
"""

import os
import json
import logging
import asyncio
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/telegram_bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("telegram_bot")

# Try to import python-telegram-bot
try:
    from telegram import Update, ParseMode
    from telegram.ext import (
        Updater, CommandHandler, MessageHandler, Filters, 
        CallbackContext, ConversationHandler
    )
    TELEGRAM_AVAILABLE = True
except ImportError:
    logger.warning("python-telegram-bot not found. Run: pip install python-telegram-bot==13.15")
    TELEGRAM_AVAILABLE = False

# Try to import quantum knowledge system
try:
    from quantum_knowledge_integrator import QuantumKnowledgeIntegrator
    from quantum_knowledge_hub import QuantumKnowledgeHub
    QUANTUM_KNOWLEDGE_AVAILABLE = True
except ImportError:
    logger.warning("Quantum knowledge system not found.")
    QUANTUM_KNOWLEDGE_AVAILABLE = False

class TelegramBotWithKnowledge:
    """
    Telegram Bot for EVA & GUARANI with quantum knowledge system.
    """
    
    def __init__(self, config_path: str = "config/telegram_bot.json"):
        """
        Initializes the Telegram bot.
        
        Args:
            config_path: Path to the configuration file
        """
        self.logger = logger
        self.logger.info("Initializing Telegram bot with Quantum Knowledge")
        
        # Check dependencies
        if not TELEGRAM_AVAILABLE:
            self.logger.error("python-telegram-bot is required. Run: pip install python-telegram-bot==13.15")
            raise ImportError("python-telegram-bot not found")
            
        # Paths
        self.config_path = Path(config_path)
        
        # Internal state
        self.config = self._load_config()
        self.updater = None
        self.dispatcher = None
        self.conversations = {}
        self.started = False
        
        # Quantum knowledge system
        self.quantum_knowledge_integrator = None
        self.quantum_integration = None
        if QUANTUM_KNOWLEDGE_AVAILABLE:
            self.logger.info("Quantum knowledge system available")
        else:
            self.logger.warning("Quantum knowledge system not available")
            
        self.logger.info("Telegram bot initialized")
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the bot configuration.
        
        Returns:
            Dictionary with the configurations
        """
        # Default configuration
        default_config = {
            "version": "1.0",
            "token": "",  # Telegram Bot Token (get it from BotFather)
            "use_quantum_knowledge": True,  # Use quantum knowledge system
            "use_webhook": False,  # Use webhook instead of polling
            "webhook_url": "",  # Webhook URL (if use_webhook=True)
            "webhook_port": 8443,  # Webhook port (if use_webhook=True)
            "admin_users": [],  # IDs of admin users
            "max_conversation_history": 20,  # Maximum conversation history size
            "response_time_limit": 30,  # Response time limit (seconds)
            "commands": {
                "start": "Start conversation with the bot",
                "help": "Display help message",
                "restart": "Restart the conversation"
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
                self.logger.warning("Configure the Telegram token in config/telegram_bot.json")
                return default_config
                
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return default_config
            
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
            # Initialize integrator
            self.quantum_knowledge_integrator = QuantumKnowledgeIntegrator()
            
            # Initialize knowledge hub
            await self.quantum_knowledge_integrator.initialize_hub()
            
            # Integrate with quantum integration system, if available
            if hasattr(self, 'quantum_integration') and self.quantum_integration is not None:
                await self.quantum_knowledge_integrator.connect_quantum_integration(self.quantum_integration)
                
            self.logger.info("Quantum knowledge system initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing quantum knowledge system: {e}")
            return False
            
    def setup_handlers(self) -> None:
        """
        Sets up the bot handlers.
        """
        # Check if dispatcher is available
        if not self.dispatcher:
            self.logger.error("Dispatcher not available")
            return
            
        # Start handler
        self.dispatcher.add_handler(CommandHandler("start", self._handle_start))
        
        # Help handler
        self.dispatcher.add_handler(CommandHandler("help", self._handle_help))
        
        # Restart handler
        self.dispatcher.add_handler(CommandHandler("restart", self._handle_restart))
        
        # Message handler
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self._handle_message))
        
        # Error handler
        self.dispatcher.add_error_handler(self._handle_error)
        
        self.logger.info("Handlers configured")
        
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
            "timestamp": datetime.now().isoformat()
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
        
    def _handle_start(self, update: Update, context: CallbackContext) -> None:
        """
        Handler for the /start command.
        
        Args:
            update: Telegram update
            context: Callback context
        """
        chat_id = update.effective_chat.id
        user_name = update.effective_user.first_name
        
        # Clear conversation history
        self.clear_conversation_history(chat_id)
        
        # Send welcome message
        welcome_message = f"""
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧

Hello, {user_name}! 

I am EVA & GUARANI, your universal quantum assistant.

I am here to help with information, guidance, and meaningful conversations on various topics.

How can I assist you today?

Type /help to see more information.
"""
        
        # Send message
        update.message.reply_text(welcome_message)
        
        # Add to history
        self.add_to_conversation_history(chat_id, "assistant", welcome_message)
        
    def _handle_help(self, update: Update, context: CallbackContext) -> None:
        """
        Handler for the /help command.
        
        Args:
            update: Telegram update
            context: Callback context
        """
        chat_id = update.effective_chat.id
        
        # Construct help message
        help_message = """
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧

**Available Commands:**

/start - Start or restart our conversation
/help - Display this help message
/restart - Clear the current conversation history

You can ask me questions on various topics. I am here to help with information, guidance, and meaningful conversations.

I am powered by a quantum knowledge system that allows me to maintain my unique identity even when using economical AI models.
"""
        
        # Send message
        update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)
        
        # Add to history
        self.add_to_conversation_history(chat_id, "assistant", help_message)
        
    def _handle_restart(self, update: Update, context: CallbackContext) -> None:
        """
        Handler for the /restart command.
        
        Args:
            update: Telegram update
            context: Callback context
        """
        chat_id = update.effective_chat.id
        
        # Clear conversation history
        self.clear_conversation_history(chat_id)
        
        # Send message
        restart_message = "Conversation restarted. How can I help now?"
        update.message.reply_text(restart_message)
        
        # Add to history
        self.add_to_conversation_history(chat_id, "assistant", restart_message)
        
    async def _process_message_with_knowledge(self, message: str, chat_id: int, user_id: int) -> str:
        """
        Processes a message using the quantum knowledge system.
        
        Args:
            message: Message to be processed
            chat_id: Chat ID
            user_id: User ID
            
        Returns:
            Processed response
        """
        if not QUANTUM_KNOWLEDGE_AVAILABLE or not self.quantum_knowledge_integrator:
            self.logger.warning("Quantum knowledge system not available for processing")
            return "Sorry, the quantum knowledge system is not available at the moment. Please try again later."
            
        try:
            # Get conversation history
            conversation_history = self.get_conversation_history(chat_id)
            
            # Context data
            context_data = {
                "user_id": user_id,
                "conversation_id": str(chat_id),
                "platform": "telegram",
                "timestamp": datetime.now().isoformat()
            }
            
            # Process message
            start_time = time.time()
            result = await self.quantum_knowledge_integrator.process_message(
                message=message,
                conversation_history=conversation_history,
                context_data=context_data
            )
            end_time = time.time()
            
            # Log processing time
            processing_time = end_time - start_time
            self.logger.info(f"Processing time: {processing_time:.2f}s")
            
            # Check result
            if "response" in result and result["response"]:
                return result["response"]
            elif "error" in result:
                self.logger.error(f"Error processing message: {result['error']}")
                return f"Sorry, there was an error processing your message: {result['error']}"
            else:
                self.logger.warning("No response or error returned by the quantum knowledge system")
                return "Sorry, I couldn't process your message properly. Please try again with another question."
                
        except Exception as e:
            self.logger.error(f"Error processing message with quantum knowledge: {e}")
            return f"Sorry, there was an error processing your message: {str(e)}"
            
    def _handle_message(self, update: Update, context: CallbackContext) -> None:
        """
        Handler for text messages.
        
        Args:
            update: Telegram update
            context: Callback context
        """
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        message = update.message.text
        
        # Add message to history
        self.add_to_conversation_history(chat_id, "user", message)
        
        # Check if quantum knowledge system is enabled
        if QUANTUM_KNOWLEDGE_AVAILABLE and self.config.get("use_quantum_knowledge", True) and self.quantum_knowledge_integrator:
            # Indicate typing
            context.bot.send_chat_action(chat_id=chat_id, action="typing")
            
            # Process message asynchronously
            asyncio.create_task(self._async_process_and_reply(message, chat_id, user_id, update, context))
        else:
            # Fallback to simple response
            response = "Sorry, the quantum knowledge system is not available at the moment. Please try again later."
            update.message.reply_text(response)
            self.add_to_conversation_history(chat_id, "assistant", response)
            
    async def _async_process_and_reply(self, message: str, chat_id: int, user_id: int, update: Update, context: CallbackContext) -> None:
        """
        Processes the message asynchronously and sends the response.
        
        Args:
            message: Message to be processed
            chat_id: Chat ID
            user_id: User ID
            update: Telegram update
            context: Callback context
        """
        try:
            # Process message with quantum knowledge system
            response = await self._process_message_with_knowledge(message, chat_id, user_id)
            
            # Check time limit
            time_limit = self.config.get("response_time_limit", 30)
            if len(response) > 4000:
                # Split message if too large
                chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
                for chunk in chunks:
                    context.bot.send_message(chat_id=chat_id, text=chunk, parse_mode=ParseMode.MARKDOWN)
                    await asyncio.sleep(0.5)  # Small pause between messages
            else:
                # Send response
                context.bot.send_message(chat_id=chat_id, text=response, parse_mode=ParseMode.MARKDOWN)
                
            # Add response to history
            self.add_to_conversation_history(chat_id, "assistant", response)
            
        except Exception as e:
            self.logger.error(f"Error processing message asynchronously: {e}")
            error_message = "Sorry, there was an error processing your message. Please try again."
            context.bot.send_message(chat_id=chat_id, text=error_message)
            self.add_to_conversation_history(chat_id, "assistant", error_message)
            
    def _handle_error(self, update: Update, context: CallbackContext) -> None:
        """
        Handler for errors.
        
        Args:
            update: Telegram update
            context: Callback context
        """
        # Log error
        self.logger.error(f"Error processing update: {context.error}")
        
        # Try to get chat_id
        try:
            chat_id = update.effective_chat.id
        except:
            chat_id = None
            
        # Send error message if chat_id is available
        if chat_id:
            error_message = "Sorry, there was an error processing your request. Please try again later."
            context.bot.send_message(chat_id=chat_id, text=error_message)
            
    async def start(self) -> None:
        """
        Starts the bot.
        """
        # Check token
        if not self.config.get("token"):
            self.logger.error("Telegram token not configured. Configure it in config/telegram_bot.json")
            return
            
        try:
            # Initialize quantum knowledge system
            if QUANTUM_KNOWLEDGE_AVAILABLE and self.config.get("use_quantum_knowledge", True):
                await self.initialize_quantum_knowledge()
                
            # Create Updater
            self.updater = Updater(self.config["token"], use_context=True)
            self.dispatcher = self.updater.dispatcher
            
            # Configure handlers
            self.setup_handlers()
            
            # Start bot
            use_webhook = self.config.get("use_webhook", False)
            if use_webhook:
                # Webhook mode
                webhook_url = self.config.get("webhook_url", "")
                webhook_port = self.config.get("webhook_port", 8443)
                
                if not webhook_url:
                    self.logger.error("Webhook URL not configured. Configure it in config/telegram_bot.json")
                    return
                    
                self.updater.start_webhook(
                    listen="0.0.0.0",
                    port=webhook_port,
                    url_path=self.config["token"],
                    webhook_url=webhook_url + self.config["token"]
                )
                self.logger.info(f"Bot started in webhook mode on port {webhook_port}")
            else:
                # Polling mode
                self.updater.start_polling()
                self.logger.info("Bot started in polling mode")
                
            self.started = True
            
            # Keep the bot running
            self.updater.idle()
            
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            
    def stop(self) -> None:
        """
        Stops the bot.
        """
        if self.updater:
            self.updater.stop()
            self.started = False
            self.logger.info("Bot stopped")
            
        # Close quantum knowledge integrator
        if self.quantum_knowledge_integrator:
            self.quantum_knowledge_integrator.close()
            self.logger.info("Quantum knowledge integr