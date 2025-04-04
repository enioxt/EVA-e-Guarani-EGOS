#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Interactive Interface
This module implements the interactive user interface for the Telegram bot.
"""

import os
import sys
import json
import logging
import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/interactive_ui.log"), logging.StreamHandler()],
)
logger = logging.getLogger("interactive_ui")

# Constants for UI types
UI_TYPES = {
    "MAIN_MENU": "main_menu",
    "SETTINGS": "settings",
    "HELP": "help",
    "THEMES": "themes",
    "MODELS": "models",
    "FEEDBACK": "feedback",
    "GALLERY": "gallery",
    "CONFIRMATION": "confirmation",
}

# Available themes
THEMES = {
    "default": {
        "primary_color": "#3498db",
        "secondary_color": "#2ecc71",
        "highlight_color": "#e74c3c",
        "text_color": "#333333",
        "main_emoji": "✨",
        "secondary_emoji": "🌟",
    },
    "quantum": {
        "primary_color": "#9b59b6",
        "secondary_color": "#3498db",
        "highlight_color": "#f39c12",
        "text_color": "#2c3e50",
        "main_emoji": "✧",
        "secondary_emoji": "∞",
    },
}


# Classes to represent Telegram UI components
class InlineKeyboardButton:
    """Class to represent a Telegram inline button."""

    def __init__(self, text, **kwargs):
        self.text = text
        for key, value in kwargs.items():
            setattr(self, key, value)


class InlineKeyboardMarkup:
    """Class to represent a Telegram inline keyboard."""

    def __init__(self, inline_keyboard):
        self.inline_keyboard = inline_keyboard


class ReplyKeyboardMarkup:
    """Class to represent a Telegram reply keyboard."""

    def __init__(self, keyboard, **kwargs):
        self.keyboard = keyboard
        for key, value in kwargs.items():
            setattr(self, key, value)


class ReplyKeyboardRemove:
    """Class to represent the removal of a Telegram reply keyboard."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TelegramUIBuilder:
    """Class for building Telegram interfaces."""

    def __init__(self, theme: str = "default"):
        """Initializes the UI builder with the specified theme."""
        self.theme = theme
        self.theme_config = THEMES.get(theme, THEMES["default"])
        logger.info(f"UI Builder initialized with theme: {theme}")

    def set_theme(self, theme: str) -> None:
        """Sets a new theme."""
        if theme in THEMES:
            self.theme = theme
            self.theme_config = THEMES[theme]
            logger.info(f"Theme changed to: {theme}")
        else:
            logger.warning(f"Theme not found: {theme}")

    def create_main_menu(self) -> Tuple[str, InlineKeyboardMarkup]:
        """Creates the main menu."""
        emoji = self.theme_config["main_emoji"]
        message = f"""
{emoji}{emoji}{emoji} EVA & GUARANI {emoji}{emoji}{emoji}

🤖 *MAIN MENU* 🤖

Choose an option below:
        """

        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("💬 Chat", callback_data="chat")],
                [InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
                [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
                [InlineKeyboardButton("📊 Status", callback_data="status")],
            ]
        )

        return message, buttons

    def create_settings_menu(self) -> Tuple[str, InlineKeyboardMarkup]:
        """Creates the settings menu."""
        emoji = self.theme_config["main_emoji"]
        message = f"""
{emoji}{emoji}{emoji} EVA & GUARANI {emoji}{emoji}{emoji}

⚙️ *SETTINGS* ⚙️

Customize the bot's behavior:
        """

        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🎨 Change Theme", callback_data="config_theme")],
                [InlineKeyboardButton("🧠 AI Models", callback_data="config_models")],
                [InlineKeyboardButton("🔄 Back", callback_data="main_menu")],
            ]
        )

        return message, buttons


class InteractiveUI:
    """Main class for managing the interactive interface."""

    def __init__(self, theme: str = "quantum"):
        """Initializes the interface with the specified theme."""
        self.theme = theme
        self.theme_config = THEMES.get(theme, THEMES["default"])
        logger.info(f"Interface initialized with theme: {theme}")

    def get_theme(self) -> str:
        """Returns the current theme."""
        return self.theme

    def set_theme(self, theme: str) -> None:
        """Sets a new theme."""
        if theme in THEMES:
            self.theme = theme
            self.theme_config = THEMES[theme]
            logger.info(f"Theme changed to: {theme}")
        else:
            logger.warning(f"Theme not found: {theme}")

    def format_message(self, message: str) -> str:
        """Formats a message with the current theme's style."""
        emoji = self.theme_config["main_emoji"]
        return f"{emoji} {message} {emoji}"

    def create_main_menu(self) -> Tuple[str, Dict[str, Any]]:
        """Creates the main menu."""
        message = self.format_message("Main Menu EVA & GUARANI")
        buttons = {
            "inline_keyboard": [
                [{"text": "💬 Chat", "callback_data": "chat"}],
                [{"text": "⚙️ Settings", "callback_data": "settings"}],
                [{"text": "ℹ️ Help", "callback_data": "help"}],
                [{"text": "📊 Status", "callback_data": "status"}],
            ]
        }
        return message, buttons


# Add the InteractiveUIManager class to complete the implementation
class InteractiveUIManager:
    """Interactive interface manager for the bot."""

    def __init__(self, default_theme: str = "default"):
        """Initializes the UI manager."""
        self.ui_builder = TelegramUIBuilder(default_theme)
        self.sessions = {}
        self.callback_handlers = {}
        logger.info(f"UI Manager initialized with default theme: {default_theme}")

    def register_callback_handler(self, prefix: str, handler) -> None:
        """Registers a handler for a specific callback prefix."""
        self.callback_handlers[prefix] = handler
        logger.info(f"Handler registered for prefix: {prefix}")

    def get_session(self, user_id: int, username: str) -> "InteractiveSession":
        """Gets or creates a session for the user."""
        if user_id not in self.sessions:
            self.sessions[user_id] = InteractiveSession(user_id, username)
            logger.info(f"New session created for user: {username} ({user_id})")

        return self.sessions[user_id]


# Class to manage interactive sessions
class InteractiveSession:
    """Class to manage user interactive sessions."""

    def __init__(self, user_id: int, username: str):
        """Initializes a new session for the user."""
        self.user_id = user_id
        self.username = username
        self.current_state = UI_TYPES["MAIN_MENU"]
        self.state_history = [self.current_state]
        self.data = {}
        self.last_interaction = datetime.datetime.now()
        self.session_start = datetime.datetime.now()
        logger.info(f"Session started for {username} ({user_id})")

    def update_state(self, new_state: str) -> None:
        """Updates the current session state."""
        self.current_state = new_state
        self.state_history.append(new_state)
        self.last_interaction = datetime.datetime.now()
        logger.info(f"State updated to {new_state} - User: {self.username}")

    def revert_state(self) -> str:
        """Reverts to the previous state."""
        if len(self.state_history) > 1:
            self.state_history.pop()  # Remove the current state
            self.current_state = self.state_history[-1]  # Set the previous state as current
            self.last_interaction = datetime.datetime.now()
            logger.info(f"Reverting to state {self.current_state} - User: {self.username}")
            return self.current_state
        return self.current_state
