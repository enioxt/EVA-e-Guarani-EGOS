#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Automatic Updater
This script automatically checks and updates the Telegram bot.
"""

import os
import sys
import json
import time
import shutil
import logging
import argparse
import subprocess
from datetime import datetime

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/updater.log"), logging.StreamHandler()],
)
logger = logging.getLogger("updater")

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


def is_git_repository():
    """Checks if the current directory is a Git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False


def check_for_updates():
    """Checks if there are updates available in the Git repository."""
    try:
        # Update remote references
        subprocess.run(["git", "fetch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # Check if there are differences between the local and remote branch
        result = subprocess.run(
            ["git", "rev-list", "HEAD..origin/main", "--count"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        commit_count = int(result.stdout.strip())

        if commit_count > 0:
            # Get information about the available updates
            log_result = subprocess.run(
                ["git", "log", "HEAD..origin/main", "--pretty=format:%h %s"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )

            updates = log_result.stdout.strip().split("\n")
            return True, commit_count, updates
        else:
            return False, 0, []
    except Exception as e:
        logger.error(f"Error checking updates: {e}")
        return False, 0, []


def backup_config():
    """Backs up the configuration file."""
    try:
        if not os.path.exists(CONFIG_PATH):
            logger.warning("Configuration file not found for backup.")
            return False

        backup_dir = os.path.join("backup", "config")
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"eva_guarani_config_{timestamp}.json")

        shutil.copy2(CONFIG_PATH, backup_path)
        logger.info(f"Configuration backup created at: {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Error backing up configuration: {e}")
        return False


def backup_bot_files():
    """Backs up the bot's main files."""
    try:
        backup_dir = os.path.join("backup", "bot", datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(backup_dir, exist_ok=True)

        # Files and directories to backup
        items_to_backup = [
            os.path.join("bot", "unified_telegram_bot_utf8.py"),
            os.path.join("bot", "unified_telegram_bot.py"),
            "start_eva_guarani.py",
            "check_bot_status.py",
            "monitor_bot.py",
            "notify_status.py",
        ]

        for item in items_to_backup:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.copytree(item, os.path.join(backup_dir, os.path.basename(item)))
                else:
                    shutil.copy2(item, os.path.join(backup_dir, os.path.basename(item)))

        logger.info(f"Bot files backup created at: {backup_dir}")
        return True
    except Exception as e:
        logger.error(f"Error backing up bot files: {e}")
        return False


def update_repository():
    """Updates the Git repository."""
    try:
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        logger.info(f"Update completed: {result.stdout.strip()}")
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Error updating repository: {e.stderr}")
        return False, e.stderr
    except Exception as e:
        logger.error(f"Error updating repository: {e}")
        return False, str(e)


def restart_bot():
    """Restarts the bot."""
    try:
        if os.path.exists("start_eva_guarani.py"):
            logger.info("Restarting the bot...")

            result = subprocess.run(
                [sys.executable, "start_eva_guarani.py", "--restart"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                logger.info("Bot restarted successfully.")
                return True
            else:
                logger.error(f"Error restarting the bot: {result.stderr}")
                return False
        else:
            logger.error("Startup script not found.")
            return False
    except Exception as e:
        logger.error(f"Error restarting the bot: {e}")
        return False


def send_notification(message):
    """Sends a notification about the update."""
    try:
        if os.path.exists("notify_status.py"):
            logger.info("Sending notification about the update...")

            result = subprocess.run(
                [sys.executable, "notify_status.py", "--message", message, "--force"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                logger.info("Notification sent successfully.")
                return True
            else:
                logger.error(f"Error sending notification: {result.stderr}")
                return False
        else:
            logger.warning("Notification script not found.")
            return False
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Update the EVA & GUARANI bot")
    parser.add_argument(
        "--check-only", action="store_true", help="Only check for updates, do not apply them"
    )
    parser.add_argument(
        "--force", action="store_true", help="Force update even if no changes are detected"
    )
    parser.add_argument(
        "--no-restart", action="store_true", help="Do not restart the bot after updating"
    )
    parser.add_argument("--no-backup", action="store_true", help="Do not backup before updating")
    args = parser.parse_args()

    print("=" * 50)
    print("EVA & GUARANI - Automatic Updater")
    print("=" * 50)

    # Check if it is a Git repository
    if not is_git_repository():
        print("❌ This directory is not a Git repository.")
        print("Automatic updating only works with Git-based installations.")
        return 1

    # Check for updates
    print("\nChecking for updates...")
    has_updates, commit_count, updates = check_for_updates()

    if has_updates:
        print(f"✅ {commit_count} updates available:")
        for update in updates:
            print(f"   - {update}")
    else:
        print("✅ The bot is already up to date.")

        if not args.force:
            if args.check_only:
                return 0
            else:
                print("\nNo update necessary.")
                return 0
        else:
            print("\nForcing update even with no changes detected...")

    if args.check_only:
        return 0

    # Backup before updating
    if not args.no_backup:
        print("\nCreating backups before updating...")
        config_backup = backup_config()
        files_backup = backup_bot_files()

        if config_backup and files_backup:
            print("✅ Backups created successfully.")
        else:
            print("⚠️ There were problems creating the backups.")

            if not args.force:
                print("Update canceled. Use --force to continue anyway.")
                return 1

    # Update the repository
    print("\nUpdating the repository...")
    success, message = update_repository()

    if success:
        print("✅ Repository updated successfully.")

        # Prepare notification message
        if has_updates:
            notification_message = f"""
🔄 <b>BOT UPDATED</b> - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

<b>Updates installed:</b> {commit_count}
<b>Details:</b>
"""
            for update in updates[:5]:  # Limit to 5 updates to avoid overloading the message
                notification_message += f"- {update}\n"

            if len(updates) > 5:
                notification_message += f"... and {len(updates) - 5} more updates.\n"
        else:
            notification_message = f"""
🔄 <b>BOT UPDATED</b> - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

<b>Details:</b> Forced update with no changes detected.
"""

        # Restart the bot
        if not args.no_restart:
            print("\nRestarting the bot...")
            if restart_bot():
                print("✅ Bot restarted successfully.")
                notification_message += "\n<b>Status:</b> Bot restarted successfully."
            else:
                print("❌ Failed to restart the bot.")
                notification_message += (
                    "\n<b>Status:</b> Failed to restart the bot. Restart manually."
                )
        else:
            print("\nAutomatic restart disabled.")
            notification_message += "\n<b>Status:</b> Automatic restart disabled. Restart manually."

        # Send notification
        print("\nSending notification about the update...")
        if send_notification(notification_message):
            print("✅ Notification sent successfully.")
        else:
            print("⚠️ Failed to send notification.")

        print("\n" + "=" * 50)
        print("Update completed successfully!")
        if not args.no_restart:
            print("The bot has been restarted and is running.")
        else:
            print("Remember to restart the bot manually: python start_eva_guarani.py --restart")
        print("=" * 50)

        return 0
    else:
        print(f"❌ Failed to update the repository: {message}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
