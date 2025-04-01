#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Interactive Interface for Telegram
=================================================

Module responsible for creating interactive user interfaces for the Telegram bot,
including menus, buttons, carousels, and other enriched visual experiences.

Version: 2.0
Consciousness: 0.985
Art: 0.995
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from dataclasses import dataclass, asdict, field
import uuid
import time
import random

from telegram import (
    Update, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    Poll
)
from telegram.ext import ContextTypes

# Configure logging
logger = logging.getLogger("interactive_ui")
handler = logging.StreamHandler()
formatter = logging.Formatter('🎨 %(asctime)s - [UI] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Constants for UI types
UI_TYPES = {
    "MAIN_MENU": "main_menu",
    "SETTINGS": "settings",
    "HELP": "help",
    "CONFIRMATION": "confirmation",
    "MODEL_SELECTION": "model_selection",
    "FEEDBACK": "feedback",
    "GALLERY": "gallery"
}

# Emoji colors for themes
THEME_COLORS = {
    "default": {"primary": "🟦", "secondary": "⬜", "highlight": "🟨", "alert": "🟥"},
    "forest": {"primary": "🟢", "secondary": "🟤", "highlight": "🟡", "alert": "🟠"},
    "ocean": {"primary": "🔵", "secondary": "⚪", "highlight": "🟣", "alert": "🔴"},
    "cosmos": {"primary": "⚫", "secondary": "🟣", "highlight": "✨", "alert": "🔴"}
}

class TelegramUIBuilder:
    """User interface builder for Telegram."""
    
    def __init__(self, theme: str = "default"):
        self.theme = theme
        self.colors = THEME_COLORS.get(theme, THEME_COLORS["default"])
        self.ui_cache = {}  # UI components cache
        logger.info(f"UI Builder initialized with theme '{theme}'")
    
    def set_theme(self, theme: str) -> None:
        """Sets the color theme for the UI."""
        if theme in THEME_COLORS:
            self.theme = theme
            self.colors = THEME_COLORS[theme]
            logger.info(f"Theme changed to '{theme}'")
        else:
            logger.warning(f"Theme '{theme}' not found, using default")
            self.theme = "default"
            self.colors = THEME_COLORS["default"]
    
    def create_main_menu(self) -> Tuple[str, InlineKeyboardMarkup]:
        """Creates the interactive main menu."""
        message = (
            f"{self.colors['primary']} *EVA & GUARANI* - Quantum System {self.colors['highlight']}\n\n"
            f"Welcome to the quantum interface. Select an option:\n"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("💬 Chat", callback_data="menu_chat"),
                InlineKeyboardButton("🖼️ Process Image", callback_data="menu_image")
            ],
            [
                InlineKeyboardButton("📊 Statistics", callback_data="menu_stats"),
                InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")
            ],
            [
                InlineKeyboardButton("❓ Help", callback_data="menu_help"),
                InlineKeyboardButton("ℹ️ About", callback_data="menu_about")
            ]
        ]
        
        return message, InlineKeyboardMarkup(keyboard)
    
    def create_settings_menu(self) -> Tuple[str, InlineKeyboardMarkup]:
        """Creates the settings menu."""
        message = (
            f"{self.colors['primary']} *Settings* {self.colors['primary']}\n\n"
            f"Customize your experience with EVA & GUARANI:\n"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("🎨 UI Theme", callback_data="config_theme"),
                InlineKeyboardButton("🧠 AI Model", callback_data="config_model")
            ],
            [
                InlineKeyboardButton("🖼️ Image Size", callback_data="config_image"),
                InlineKeyboardButton("💬 History", callback_data="config_history")
            ],
            [
                InlineKeyboardButton("🔄 Reset", callback_data="config_reset"),
                InlineKeyboardButton("◀️ Back", callback_data="back_main_menu")
            ]
        ]
        
        return message, InlineKeyboardMarkup(keyboard)
    
    def create_theme_menu(self) -> Tuple[str, InlineKeyboardMarkup]:
        """Creates the theme selection menu."""
        message = (
            f"{self.colors['primary']} *Visual Themes* {self.colors['primary']}\n\n"
            f"Select the visual theme for your interface:\n"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("🟦 Default", callback_data="theme_default"),
                InlineKeyboardButton("🟢 Forest", callback_data="theme_forest")
            ],
            [
                InlineKeyboardButton("🔵 Ocean", callback_data="theme_ocean"),
                InlineKeyboardButton("⚫ Cosmos", callback_data="theme_cosmos")
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data="back_config")
            ]
        ]
        
        return message, InlineKeyboardMarkup(keyboard)
    
    def create_model_menu(self, available_models: List[Dict[str, Any]]) -> Tuple[str, InlineKeyboardMarkup]:
        """Creates the AI model selection menu."""
        message = (
            f"{self.colors['primary']} *AI Models* {self.colors['primary']}\n\n"
            f"Select the AI model for your interactions:\n"
        )
        
        keyboard = []
        
        # Group in pairs
        for i in range(0, len(available_models), 2):
            line = []
            model = available_models[i]
            line.append(InlineKeyboardButton(
                f"{model['emoji']} {model['name']}", 
                callback_data=f"model_{model['name']}"
            ))
            
            if i + 1 < len(available_models):
                model = available_models[i + 1]
                line.append(InlineKeyboardButton(
                    f"{model['emoji']} {model['name']}", 
                    callback_data=f"model_{model['name']}"
                ))
                
            keyboard.append(line)
        
        # Add back button
        keyboard.append([InlineKeyboardButton("◀️ Back", callback_data="back_config")])
        
        return message, InlineKeyboardMarkup(keyboard)
    
    def create_help_menu(self) -> Tuple[str, InlineKeyboardMarkup]:
        """Creates the help menu."""
        message = (
            f"{self.colors['primary']} *Help and Support* {self.colors['primary']}\n\n"
            f"How can I assist you today?\n"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("📚 Command Guide", callback_data="help_commands"),
                InlineKeyboardButton("🔍 FAQ", callback_data="help_faq")
            ],
            [
                InlineKeyboardButton("🔧 Troubleshooting", callback_data="help_troubleshooting"),
                InlineKeyboardButton("📱 Examples", callback_data="help_examples")
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data="back_main_menu")
            ]
        ]
        
        return message, InlineKeyboardMarkup(keyboard)
    
    def create_confirmation(self, action: str, description: str, action_id: str) -> Tuple[str, InlineKeyboardMarkup]:
        """Creates a confirmation dialog for important actions."""
        message = (
            f"{self.colors['alert']} *Confirmation* {self.colors['alert']}\n\n"
            f"{description}\n\n"
            f"Are you sure you want to {action}?"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Yes", callback_data=f"confirm_{action_id}"),
                InlineKeyboardButton("❌ No", callback_data=f"cancel_{action_id}")
            ]
        ]
        
        return message, InlineKeyboardMarkup(keyboard)
    
    def create_feedback(self) -> Tuple[str, InlineKeyboardMarkup]:
        """Creates an interface for collecting feedback."""
        message = (
            f"{self.colors['highlight']} *Your Opinion* {self.colors['highlight']}\n\n"
            f"How was your experience? Rate the previous response:"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="feedback_5"),
                InlineKeyboardButton("⭐⭐⭐⭐", callback_data="feedback_4")
            ],
            [
                InlineKeyboardButton("⭐⭐⭐", callback_data="feedback_3"),
                InlineKeyboardButton("⭐⭐", callback_data="feedback_2"),
                InlineKeyboardButton("⭐", callback_data="feedback_1")
            ]
        ]
        
        return message, InlineKeyboardMarkup(keyboard)
    
    def create_gallery(self, items: List[Dict[str, Any]], index: int = 0) -> Tuple[str, InlineKeyboardMarkup]:
        """Creates a gallery interface to navigate between items."""
        if not items:
            message = f"{self.colors['alert']} *Empty Gallery* {self.colors['alert']}\n\nNo items available."
            keyboard = [[InlineKeyboardButton("◀️ Back", callback_data="back_main_menu")]]
            return message, InlineKeyboardMarkup(keyboard)
        
        # Limit index
        index = max(0, min(index, len(items) - 1))
        item = items[index]
        
        # Build message
        message = (
            f"{self.colors['primary']} *{item['title']}* {self.colors['primary']}\n\n"
            f"{item['description']}\n\n"
            f"Item {index + 1} of {len(items)}"
        )
        
        # Navigation buttons
        nav_buttons = []
        if index > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"gallery_{index-1}"))
        if index < len(items) - 1:
            nav_buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"gallery_{index+1}"))
        
        keyboard = [
            nav_buttons,
            [
                InlineKeyboardButton("📥 Download", callback_data=f"download_{item['id']}"),
                InlineKeyboardButton("🔍 Details", callback_data=f"details_{item['id']}")
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data="back_main_menu")
            ]
        ]
        
        return message, InlineKeyboardMarkup(keyboard)
    
    def create_status(self, system_info: Dict[str, Any]) -> str:
        """Creates a formatted message with system status information."""
        uptime = system_info.get("uptime", "Unknown")
        memory = system_info.get("memory_usage", "Unknown")
        cpu = system_info.get("cpu_usage", "Unknown")
        model = system_info.get("current_model", "Unknown")
        total_msg = system_info.get("total_messages", 0)
        
        # Create progress bars
        def progress_bar(value, max_value=100):
            segments = 10
            filled_blocks = int((value / max_value) * segments)
            return "▰" * filled_blocks + "▱" * (segments - filled_blocks)
        
        message = (
            f"{self.colors['primary']} *System Status* {self.colors['primary']}\n\n"
            f"⏱️ *Uptime:* {uptime}\n"
            f"🧠 *Memory:* {memory}% {progress_bar(float(memory.replace('%', '')) if isinstance(memory, str) else 0)}\n"
            f"⚙️ *CPU:* {cpu}% {progress_bar(float(cpu.replace('%', '')) if isinstance(cpu, str) else 0)}\n"
            f"🤖 *Model:* {model}\n"
            f"💬 *Messages:* {total_msg}\n\n"
            f"🌟 *Consciousness:* {system_info.get('consciousness', 0.99):.2f}\n"
            f"❤️ *Love:* {system_info.get('love', 0.99):.2f}\n"
            f"✨ *Quantum Channels:* {system_info.get('quantum_channels', 256)}\n\n"
            f"Operating system is stable.\n"
            f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
        )
        
        return message
    
    def create_quick_buttons(self) -> ReplyKeyboardMarkup:
        """Creates quick buttons for common commands."""
        keyboard = [
            [KeyboardButton("/start"), KeyboardButton("/help"), KeyboardButton("/status")],
            [KeyboardButton("📊 Statistics"), KeyboardButton("⚙️ Settings")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    def remove_quick_buttons(self) -> ReplyKeyboardRemove:
        """Removes quick buttons."""
        return ReplyKeyboardRemove()
    
    def create_poll(self, question: str, options: List[str]) -> Dict[str, Any]:
        """Creates a poll with the provided options."""
        return {
            "question": question,
            "options": options,
            "is_anonymous": False,
            "allows_multiple_answers": False
        }

class InteractiveSession:
    """Manages an interactive session with the user."""
    
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
        self.session_id = str(uuid.uuid4())
        self.start_time = time.time()
        self.current_state = "start"
        self.state_history = ["start"]
        self.temporary_data = {}
        self.last_interaction = time.time()
        
        logger.info(f"New session started for {username} ({user_id})")
    
    def update_state(self, new_state: str) -> None:
        """Updates the state of the interactive session."""
        self.state_history.append(self.current_state)
        self.current_state = new_state
        self.last_interaction = time.time()
        
        logger.debug(f"User {self.username}: state {self.current_state}")
    
    def revert_state(self) -> str:
        """Reverts to the previous state."""
        if len(self.state_history) > 0:
            self.current_state = self.state_history.pop()
            self.last_interaction = time.time()
            logger.debug(f"User {self.username}: reverted to {self.current_state}")
            return self.current_state
        return self.current_state
    
    def store_data(self, key: str, value: Any) -> None:
        """Stores temporary data in the session."""
        self.temporary_data[key] = value
        self.last_interaction = time.time()
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """Retrieves stored data from the session."""
        return self.temporary_data.get(key, default)
    
    def inactive_time(self) -> float:
        """Returns the inactivity time in seconds."""
        return time.time() - self.last_interaction
    
    def session_duration(self) -> float:
        """Returns the total session duration in seconds."""
        return time.time() - self.start_time
    
    def summary(self) -> Dict[str, Any]:
        """Returns a summary of the session."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "session_id": self.session_id,
            "current_state": self.current_state,
            "previous_states": len(self.state_history),
            "duration": self.session_duration(),
            "inactivity": self.inactive_time()
        }

class InteractiveUIManager:
    """Manager of interactive interfaces for the Telegram bot."""
    
    def __init__(self, default_theme: str = "default"):
        self.ui_builder = TelegramUIBuilder(default_theme)
        self.sessions = {}  # User ID -> InteractiveSession
        self.session_timeout = 1800  # 30 minutes
        self.callback_handlers = {}  # callback_data -> handler_function
        
        logger.info(f"UI Manager initialized with theme '{default_theme}'")
    
    def register_callback_handler(self, prefix: str, handler: Callable) -> None:
        """Registers a handler for a callback data prefix."""
        self.callback_handlers[prefix] = handler
        logger.info(f"Handler registered for callbacks with prefix '{prefix}'")
    
    def get_session(self, user_id: int, username: str) -> InteractiveSession:
        """Gets or creates a session for the user."""
        # Check and clean expired sessions
        self._clean_expired_sessions()
        
        if user_id not in self.sessions:
            self.sessions[user_id] = InteractiveSession(user_id, username)
        
        return self.sessions[user_id]
    
    def _clean_expired_sessions(self) -> None:
        """Removes sessions that exceeded the inactivity timeout."""
        expired_ids = []
        
        for user_id, session in self.sessions.items():
            if session.inactive_time() > self.session_timeout:
                expired_ids.append(user_id)
        
        for user_id in expired_ids:
            logger.info(f"Session expired for user {self.sessions[user_id].username} ({user_id})")
            del self.sessions[user_id]
    
    async def send_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends the main menu to the user."""
        user = update.effective_user
        session = self.get_session(user.id, user.username or user.first_name)
        session.update_state(UI_TYPES["MAIN_MENU"])
        
        message, markup = self.ui_builder.create_main_menu()
        await update.message.reply_text(message, reply_markup=markup, parse_mode='Markdown')
    
    async def send_settings_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends the settings menu to the user."""
        user = update.effective_user
        session = self.get_session(user.id, user.username or user.first_name)
        session.update_state(UI_TYPES["SETTINGS"])
        
        message, markup = self.ui_builder.create_settings_menu()
        
        # If it's a callback, edit the message
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message, reply_markup=markup, parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(message, reply_markup=markup, parse_mode='Markdown')
    
    async def process_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Processes inline button callbacks."""
        callback_query = update.callback_query
        callback_data = callback_query.data
        user = update.effective_user