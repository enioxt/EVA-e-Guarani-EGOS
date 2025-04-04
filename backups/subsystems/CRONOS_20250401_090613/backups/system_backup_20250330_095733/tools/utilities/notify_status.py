#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Status Notifier
This script checks if the Telegram bot is online and sends a notification.
"""

import os
import sys
import json
import logging
import requests
import argparse
from datetime import datetime

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/notification.log"), logging.StreamHandler()],
)
logger = logging.getLogger("notify_status")

# Load configuration
CONFIG_PATH = os.path.join("config", "eva_guarani_config.json")


def load_config():
    """Loads the bot configuration."""
    try:
        if not os.path.exists(CONFIG_PATH):
            logger.error(f"Configuration file not found: {CONFIG_PATH}")
            return None

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return None


def check_bot_status(bot_token):
    """Checks if the bot is online using the Telegram API."""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot_info = data.get("result", {})
                return True, bot_info
            else:
                return False, data.get("description", "Unknown error")
        else:
            return False, f"Telegram API error: {response.status_code}"
    except Exception as e:
        return False, f"Error checking bot status: {e}"


def is_bot_running():
    """Checks if the bot process is running."""
    try:
        import psutil

        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmdline = proc.info.get("cmdline", [])
                if cmdline and any("unified_telegram_bot" in cmd for cmd in cmdline if cmd):
                    return True, proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return False, None
    except ImportError:
        logger.warning("Module psutil not found. Unable to check processes.")
        return False, None
    except Exception as e:
        logger.error(f"Error checking processes: {e}")
        return False, None


def send_notification(bot_token, chat_ids, message, parse_mode="HTML"):
    """Sends a notification to the specified chat IDs."""
    success_count = 0

    for chat_id in chat_ids:
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {"chat_id": chat_id, "text": message, "parse_mode": parse_mode}

            response = requests.post(url, json=data, timeout=10)

            if response.status_code == 200:
                logger.info(f"Notification successfully sent to {chat_id}")
                success_count += 1
            else:
                logger.error(f"Error sending notification to {chat_id}: {response.text}")
        except Exception as e:
            logger.error(f"Error sending notification to {chat_id}: {e}")

    return success_count


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Check bot status and send notification")
    parser.add_argument("--message", help="Custom message to send")
    parser.add_argument(
        "--force", action="store_true", help="Force sending even if the bot is offline"
    )
    parser.add_argument("--chat-id", help="Specific chat ID to send the notification")
    args = parser.parse_args()

    # Load configuration
    config = load_config()
    if not config:
        print("❌ Failed to load configuration.")
        return 1

    # Get bot token
    bot_token = config.get("telegram", {}).get("bot_token") or config.get("bot_token")
    if not bot_token:
        print("❌ Bot token not found in configuration.")
        return 1

    # Get admin IDs
    admin_users = config.get("telegram", {}).get("admin_users", [])

    # If a specific chat_id was provided, use only it
    if args.chat_id:
        try:
            chat_id = int(args.chat_id)
            admin_users = [chat_id]
        except ValueError:
            print(f"❌ Invalid chat ID: {args.chat_id}")
            return 1

    if not admin_users:
        print("❌ No admin ID found in configuration.")
        return 1

    # Check bot status
    print("Checking bot status...")
    api_status, api_info = check_bot_status(bot_token)
    process_status, pid = is_bot_running()

    # Prepare message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if args.message:
        message = args.message
    else:
        if api_status and process_status:
            message = f"""
🟢 <b>BOT ONLINE</b> - {current_time}

<b>Name:</b> {api_info.get('first_name')}
<b>Username:</b> @{api_info.get('username')}
<b>ID:</b> {api_info.get('id')}
<b>PID:</b> {pid}

<b>Status:</b> The bot is functioning correctly.
<b>Available commands:</b> /start, /help, /status
"""
        elif api_status and not process_status:
            message = f"""
🟡 <b>BOT PARTIALLY ONLINE</b> - {current_time}

<b>Name:</b> {api_info.get('first_name')}
<b>Username:</b> @{api_info.get('username')}
<b>ID:</b> {api_info.get('id')}

<b>Status:</b> The bot is responding on the Telegram API, but the local process was not found.
<b>Recommended action:</b> Check if the bot is running on another server or restart it.
"""
        elif not api_status and process_status:
            message = f"""
🟡 <b>BOT PARTIALLY OFFLINE</b> - {current_time}

<b>PID:</b> {pid}

<b>Status:</b> The bot process is running, but it is not responding on the Telegram API.
<b>Recommended action:</b> Check logs and restart the bot.
<b>Error:</b> {api_info}
"""
        else:
            message = f"""
🔴 <b>BOT OFFLINE</b> - {current_time}

<b>Status:</b> The bot is not responding on the Telegram API and no process was found.
<b>Recommended action:</b> Start the bot using the command: python start_eva_guarani.<b>Error:</b> {api_info}
"""

    # Send notification
    if api_status or process_status or args.force:
        print(f"Sending notification to {len(admin_users)} administrators...")
        success_count = send_notification(bot_token, admin_users, message)

        if success_count > 0:
            print(
                f"✅ Notification successfully sent to {success_count}/{len(admin_users)} administrators."
            )
            return 0
        else:
            print("❌ Failed to send notifications.")
            return 1
    else:
        print("❌ Bot is offline and --force was not specified. No notification sent.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
