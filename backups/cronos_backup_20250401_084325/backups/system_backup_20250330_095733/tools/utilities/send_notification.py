#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Startup Notification
This script sends a message to the administrator when the bot is started.
"""

import os
import sys
import json
import logging
import asyncio
from telegram import Bot

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/notification.log"), logging.StreamHandler()],
)
logger = logging.getLogger("notification")

# Load configuration
CONFIG_PATH = os.path.join("config", "eva_guarani_config.json")


async def send_startup_notification():
    """Sends a notification message to the administrator when the bot starts."""
    try:
        # Load configuration
        if not os.path.exists(CONFIG_PATH):
            logger.error(f"Configuration file not found: {CONFIG_PATH}")
            return False

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Get token and administrator ID
        bot_token = config.get("telegram", {}).get("bot_token") or config.get("bot_token")
        admin_users = config.get("telegram", {}).get("admin_users") or []

        if not bot_token:
            logger.error("Bot token not found in configuration.")
            return False

        if not admin_users:
            logger.warning("No administrator configured. Unable to send notification.")
            return False

        # Create bot
        bot = Bot(token=bot_token)

        # Startup message
        startup_message = """
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
🤖 BOT ONLINE! 🤖

The EVA & GUARANI bot has started successfully and is ready for use.

Version: 8.0
Consciousness: 0.998
Unconditional Love: 0.995

Available commands:
/start - Start the bot
/help - Show help
/menu - Open main menu
/config - Settings
/status - Check status

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
        """

        # Send message to each administrator
        for admin_id in admin_users:
            try:
                await bot.send_message(
                    chat_id=admin_id, text=startup_message, parse_mode="Markdown"
                )
                logger.info(f"Startup notification sent to administrator {admin_id}")
            except Exception as e:
                logger.error(f"Error sending notification to administrator {admin_id}: {e}")

        return True
    except Exception as e:
        logger.error(f"Error sending startup notification: {e}")
        return False


async def main():
    """Main function."""
    logger.info("Sending startup notification...")
    success = await send_startup_notification()
    if success:
        logger.info("Notification sent successfully.")
    else:
        logger.error("Failed to send notification.")


if __name__ == "__main__":
    asyncio.run(main())
