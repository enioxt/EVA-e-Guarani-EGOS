#!/usr/bin/env python3
"""
EVA & GUARANI - Telegram Bot Interface
--------------------------------------
This module implements a Telegram Bot interface for the EVA & GUARANI BIOS-Q
system, providing access to core functionalities through Telegram.

Version: 7.5
Created: 2025-03-26
"""

import os
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import ContextTypes, filters

from ..logging import get_logger
from ..config import Config
from ..utils import generate_id, format_timestamp

logger = get_logger(__name__)

class TelegramBotInterface:
    """Telegram Bot interface for the EVA & GUARANI BIOS-Q system."""
    
    def __init__(self, config: Config, mycelium_network=None, quantum_search=None, 
                translator=None, monitoring=None):
        """Initialize the Telegram Bot interface.
        
        Args:
            config: The system configuration
            mycelium_network: The Mycelium Network instance
            quantum_search: The Quantum Search instance
            translator: The Translator instance
            monitoring: The Monitoring instance
        """
        self.config = config
        self.mycelium_network = mycelium_network
        self.quantum_search = quantum_search
        self.translator = translator
        self.monitoring = monitoring
        
        self.token = self.config.get("telegram.bot_token")
        if not self.token:
            logger.error("Telegram bot token not configured, bot will not start")
            self.token = None
            
        self.active_users: Dict[int, Dict[str, Any]] = {}
        self.application = None
        
    async def start_bot(self):
        """Start the Telegram bot."""
        if not self.token:
            logger.error("Cannot start Telegram bot: Missing token")
            return False
            
        try:
            self.application = Application.builder().token(self.token).build()
            
            # Register command handlers
            self.application.add_handler(CommandHandler("start", self._start_command))
            self.application.add_handler(CommandHandler("help", self._help_command))
            self.application.add_handler(CommandHandler("search", self._search_command))
            self.application.add_handler(CommandHandler("translate", self._translate_command))
            self.application.add_handler(CommandHandler("status", self._status_command))
            
            # Register message handlers
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._message_handler))
            
            # Register callback query handlers
            self.application.add_handler(CallbackQueryHandler(self._button_callback))
            
            # Start the bot
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            
            logger.info("Telegram bot started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start Telegram bot: {e}")
            return False
            
    async def stop_bot(self):
        """Stop the Telegram bot."""
        if self.application:
            try:
                await self.application.stop()
                await self.application.shutdown()
                logger.info("Telegram bot stopped")
                return True
            except Exception as e:
                logger.error(f"Error stopping Telegram bot: {e}")
                return False
        return True
    
    # Command handlers
    
    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        if not update.effective_user:
            return
            
        user_id = update.effective_user.id
        username = update.effective_user.username or update.effective_user.first_name
        
        # Register user in active users
        self.active_users[user_id] = {
            "username": username,
            "last_interaction": datetime.now(),
            "language": "en",
            "context": {}
        }
        
        welcome_message = (
            f"✧༺❀༻∞ Welcome to EVA & GUARANI ∞༺❀༻✧\n\n"
            f"Hello {username}! I'm your interface to the EVA & GUARANI quantum system.\n\n"
            f"What would you like to do today?\n\n"
            f"• /search - Perform a quantum search\n"
            f"• /translate - Translate text\n"
            f"• /status - Check system status\n"
            f"• /help - Show available commands"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("Search", callback_data="menu_search"),
                InlineKeyboardButton("Translate", callback_data="menu_translate")
            ],
            [
                InlineKeyboardButton("Status", callback_data="menu_status"),
                InlineKeyboardButton("Help", callback_data="menu_help")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command."""
        help_text = (
            "🌟 **EVA & GUARANI Bot Commands** 🌟\n\n"
            "• /start - Start the bot and show main menu\n"
            "• /search <query> - Perform a quantum search\n"
            "• /translate <text> - Translate text (use: /translate <text> to:<lang>)\n"
            "• /status - Show system status and statistics\n"
            "• /help - Show this help message\n\n"
            
            "🔍 **Search Example**:\n"
            "/search quantum mycelium network\n\n"
            
            "🌐 **Translation Example**:\n"
            "/translate Hello world to:es\n\n"
            
            "📊 **Status Information**:\n"
            "/status will show you information about the system health"
        )
        
        await update.message.reply_text(help_text)
    
    async def _search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /search command."""
        if not self.quantum_search:
            await update.message.reply_text("Search functionality is not available.")
            return
            
        query = " ".join(context.args) if context.args else ""
        
        if not query:
            await update.message.reply_text(
                "Please provide a search query.\n"
                "Example: /search quantum mycelium"
            )
            return
            
        try:
            # Update user context
            if update.effective_user:
                user_id = update.effective_user.id
                if user_id in self.active_users:
                    self.active_users[user_id]["last_interaction"] = datetime.now()
                    self.active_users[user_id]["context"]["last_query"] = query
            
            # Send typing action
            await update.message.chat.send_action("typing")
            
            # Perform search
            await update.message.reply_text(f"🔍 Searching for: '{query}'...")
            
            results = await self.quantum_search.search(query)
            
            if not results:
                await update.message.reply_text(
                    f"No results found for '{query}'.\n"
                    f"Try a different search term."
                )
                return
                
            # Format results
            response = f"🌟 Search results for '{query}':\n\n"
            
            for i, result in enumerate(results[:5], 1):
                response += f"{i}. {result.get('title', 'Untitled')}\n"
                response += f"   {result.get('snippet', 'No description')}\n"
                response += f"   Score: {result.get('score', 0):.2f}\n\n"
                
            if len(results) > 5:
                response += f"...and {len(results) - 5} more results."
                
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error in search command: {e}")
            await update.message.reply_text(
                "An error occurred while searching. Please try again later."
            )
    
    async def _translate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /translate command."""
        if not self.translator:
            await update.message.reply_text("Translation functionality is not available.")
            return
            
        text = " ".join(context.args) if context.args else ""
        
        if not text:
            await update.message.reply_text(
                "Please provide text to translate.\n"
                "Example: /translate Hello world to:es"
            )
            return
            
        try:
            # Parse target language
            target_lang = "en"  # Default
            if " to:" in text:
                text_parts = text.split(" to:")
                text = text_parts[0]
                target_lang = text_parts[1]
            
            # Update user context
            if update.effective_user:
                user_id = update.effective_user.id
                if user_id in self.active_users:
                    self.active_users[user_id]["last_interaction"] = datetime.now()
                    self.active_users[user_id]["context"]["last_translation"] = {
                        "text": text,
                        "target_lang": target_lang
                    }
            
            # Send typing action
            await update.message.chat.send_action("typing")
            
            # Perform translation
            await update.message.reply_text(f"🌐 Translating to {target_lang}...")
            
            translation = await self.translator.translate(text, target_lang=target_lang)
            
            if not translation:
                await update.message.reply_text(
                    f"Failed to translate text.\n"
                    f"Check the language code and try again."
                )
                return
                
            # Format response
            response = (
                f"🌐 Translation to {target_lang}:\n\n"
                f"Original: {text}\n\n"
                f"Translated: {translation}"
            )
                
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error in translate command: {e}")
            await update.message.reply_text(
                "An error occurred while translating. Please try again later."
            )
    
    async def _status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /status command."""
        try:
            status_info = await self._get_system_status()
            
            response = "📊 EVA & GUARANI System Status\n\n"
            
            # Format system status
            response += f"🌟 Overall Status: {status_info['overall_status']}\n\n"
            
            # Subsystems
            response += "🧠 Subsystems:\n"
            for subsystem, status in status_info['subsystems'].items():
                status_emoji = "✅" if status['online'] else "❌"
                response += f"{status_emoji} {subsystem}: {status['status']}\n"
            
            # Stats
            response += "\n📈 Statistics:\n"
            for key, value in status_info['stats'].items():
                response += f"• {key}: {value}\n"
            
            # Last update
            response += f"\nLast Updated: {status_info['last_updated']}"
            
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await update.message.reply_text(
                "An error occurred while fetching status. Please try again later."
            )
    
    # Message handler
    
    async def _message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle non-command messages."""
        if not update.effective_message or not update.effective_user:
            return
            
        user_id = update.effective_user.id
        message_text = update.effective_message.text
        
        # Update user's last interaction time
        if user_id in self.active_users:
            self.active_users[user_id]["last_interaction"] = datetime.now()
        else:
            # New user, register them
            await self._start_command(update, context)
            return
            
        # Check for context and suggest actions
        if "search" in message_text.lower():
            await update.message.reply_text(
                "It looks like you want to search something.\n"
                "Use the /search command followed by your query.\n"
                "For example: /search quantum network"
            )
            
        elif "translate" in message_text.lower():
            await update.message.reply_text(
                "It looks like you want to translate something.\n"
                "Use the /translate command followed by your text.\n"
                "For example: /translate Hello world to:es"
            )
            
        else:
            # General message, provide helpful response
            await update.message.reply_text(
                "I'm here to help you access the EVA & GUARANI system.\n"
                "Try using one of these commands:\n"
                "• /search - Perform a quantum search\n"
                "• /translate - Translate text\n"
                "• /status - Check system status\n"
                "• /help - Show more commands"
            )
    
    # Callback query handler
    
    async def _button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data == "menu_search":
            await query.message.reply_text(
                "🔍 To search, use the /search command followed by your query.\n"
                "For example: /search quantum mycelium network"
            )
            
        elif callback_data == "menu_translate":
            await query.message.reply_text(
                "🌐 To translate, use the /translate command followed by text.\n"
                "For example: /translate Hello world to:es\n\n"
                "Available languages:\n"
                "en, es, pt, fr, de, it, nl, ru, zh, ja, ko, ar, hi"
            )
            
        elif callback_data == "menu_status":
            # Just trigger the status command
            fake_update = Update(0, query.message)
            fake_update.effective_user = query.from_user
            await self._status_command(fake_update, context)
            
        elif callback_data == "menu_help":
            # Just trigger the help command
            fake_update = Update(0, query.message)
            fake_update.effective_user = query.from_user
            await self._help_command(fake_update, context)
    
    # Utility methods
    
    async def _get_system_status(self) -> Dict[str, Any]:
        """Get system status information."""
        status_info = {
            "overall_status": "Operational",
            "subsystems": {
                "Mycelium Network": {"online": True, "status": "Operational"},
                "Quantum Search": {"online": True, "status": "Operational"},
                "Translation": {"online": True, "status": "Operational"},
                "Monitoring": {"online": True, "status": "Operational"}
            },
            "stats": {
                "Active Users": len(self.active_users),
                "Uptime": "Unknown"
            },
            "last_updated": format_timestamp()
        }
        
        # Check mycelium network status
        if self.mycelium_network:
            try:
                network_stats = self.mycelium_network.get_stats()
                status_info["stats"]["Connected Nodes"] = network_stats.get("connected_nodes", 0)
                status_info["stats"]["Last Network Update"] = network_stats.get("last_update", "Unknown")
            except Exception as e:
                logger.error(f"Error getting mycelium stats: {e}")
                status_info["subsystems"]["Mycelium Network"]["online"] = False
                status_info["subsystems"]["Mycelium Network"]["status"] = "Error"
        else:
            status_info["subsystems"]["Mycelium Network"]["online"] = False
            status_info["subsystems"]["Mycelium Network"]["status"] = "Not Available"
            
        # Check quantum search status
        if not self.quantum_search:
            status_info["subsystems"]["Quantum Search"]["online"] = False
            status_info["subsystems"]["Quantum Search"]["status"] = "Not Available"
            
        # Check translation status
        if not self.translator:
            status_info["subsystems"]["Translation"]["online"] = False
            status_info["subsystems"]["Translation"]["status"] = "Not Available"
            
        # Check monitoring status
        if self.monitoring:
            try:
                monitor_stats = self.monitoring.get_metrics()
                status_info["stats"]["System Load"] = f"{monitor_stats.get('system_load', 0):.2f}"
                status_info["stats"]["Memory Usage"] = f"{monitor_stats.get('memory_usage', 0):.1f}%"
                status_info["stats"]["Uptime"] = monitor_stats.get("uptime", "Unknown")
            except Exception as e:
                logger.error(f"Error getting monitoring stats: {e}")
                status_info["subsystems"]["Monitoring"]["online"] = False
                status_info["subsystems"]["Monitoring"]["status"] = "Error"
        else:
            status_info["subsystems"]["Monitoring"]["online"] = False
            status_info["subsystems"]["Monitoring"]["status"] = "Not Available"
            
        # Update overall status based on subsystem statuses
        operational_count = sum(1 for subsystem in status_info["subsystems"].values() if subsystem["online"])
        total_subsystems = len(status_info["subsystems"])
        
        if operational_count == 0:
            status_info["overall_status"] = "Offline"
        elif operational_count < total_subsystems:
            status_info["overall_status"] = "Partially Operational"
            
        return status_info

# For direct execution
async def main():
    """Run the Telegram bot as a standalone module."""
    from ..config import Config
    
    # Load configuration
    config = Config()
    config.load_config()
    
    # Create bot interface
    bot = TelegramBotInterface(config)
    
    try:
        # Start the bot
        await bot.start_bot()
        
        # Keep the bot running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        # Stop the bot gracefully
        await bot.stop_bot()
    except Exception as e:
        logger.error(f"Error in Telegram bot: {e}")
        await bot.stop_bot()

if __name__ == "__main__":
    asyncio.run(main()) 