#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Open Telegram Web
=================================

Script to open Telegram Web to interact with the bot directly in the browser.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0.0
"""

import os
import sys
import json
import webbrowser
import time

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load configuration
config_path = os.path.join(current_dir, "telegram_config.json")
try:
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    bot_name = config.get("bot_name", "avatechartbot")
    print(f"✅ Loaded configuration for bot: {bot_name}")
    
except Exception as e:
    print(f"❌ Error loading config: {e}")
    bot_name = "avatechartbot"

# Telegram web URL to the bot
telegram_web_url = f"https://t.me/{bot_name}"

print("\n✧༺❀༻∞ EVA & GUARANI - Telegram Bot Access ∞༺❀༻✧\n")
print(f"Opening Telegram Web to interact with {bot_name}...")
print(f"Bot URL: {telegram_web_url}")
print()
print("Instructions:")
print("1. If prompted, click 'Open in Web' or 'Cancel' and use 'Open in web app'")
print("2. Log in to your Telegram account if necessary")
print("3. Start chatting with the bot")
print("4. Use commands like /start, /help, /status, or /credits")
print()
print("Opening browser in 3 seconds...")
print()

# Wait a moment
time.sleep(3)

# Open the URL in the default browser
try:
    webbrowser.open(telegram_web_url)
    print("✅ Browser opened successfully!")
except Exception as e:
    print(f"❌ Error opening browser: {e}")
    print(f"Please manually visit: {telegram_web_url}")

print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n") 