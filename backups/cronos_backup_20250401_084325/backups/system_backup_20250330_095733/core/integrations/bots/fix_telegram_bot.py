#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to fix settings for the Telegram bot EVA & GUARANI.
This script applies the following improvements:
1. Adds appropriate timeouts to avoid connection issues
2. Configures network error handling
3. Enables automatic reconnection mode
"""

import os
import sys
import re
import shutil
import logging
from datetime import datetime

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Files to be modified
TARGET_FILES = ["setup_telegram_bot.py", "bot/__main__.py", "bot/telegram_bot.py"]


def backup_file(file_path):
    """Creates a backup of the original file"""
    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return False

    backup_dir = os.path.join(".", "backups")
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(file_path)
    backup_path = os.path.join(backup_dir, f"{filename}_{timestamp}.bak")

    shutil.copy2(file_path, backup_path)
    logger.info(f"Backup created: {backup_path}")
    return True


def fix_updater_config(file_content):
    """Fixes the Updater configuration to add timeout parameters"""
    # Pattern to find the creation of the Updater
    updater_pattern = r"updater *= *Updater\(([^)]*)\)"

    # New code with optimized settings
    replacement = """request_kwargs = {
    'read_timeout': 30,
    'connect_timeout': 30,
    'pool_timeout': 30
}
updater = Updater(\\1, request_kwargs=request_kwargs)"""

    # Replace in the content
    new_content = re.sub(updater_pattern, replacement, file_content)

    return new_content


def fix_polling_config(file_content):
    """Fixes the polling configuration to add error handling and reconnection"""
    # Pattern to find the start of polling
    polling_pattern = r"updater\.start_polling\(([^)]*)\)"

    # New code with optimized settings
    replacement = """updater.start_polling(drop_pending_updates=True, timeout=30, allowed_updates=Update.ALL_TYPES)
logger.info("Bot started with optimized settings for network stability")"""

    # Replace in the content
    new_content = re.sub(polling_pattern, replacement, file_content)

    return new_content


def add_error_handler(file_content):
    """Adds a custom error handler to handle network errors"""
    # Check if an error handler already exists
    if "def error_handler" in file_content:
        return file_content

    # Find the point of handler registration
    handlers_pattern = r"(dispatcher\.add_handler\([^)]+\)[^\n]*\n+)"

    # Code for the error handler
    error_handler_code = """
# Function to handle network errors
def error_handler(update, context):
    logger.warning(f'Error during update processing: {context.error}')

    # Handle network errors
    if "ConnectionResetError" in str(context.error) or "NetworkError" in str(context.error):
        logger.error(f"Network error detected: {context.error}. Attempting to reconnect...")
        # The bot will attempt to reconnect automatically

# Register error handler
dispatcher.add_error_handler(error_handler)

"""

    # Find all occurrences of handler registration
    matches = list(re.finditer(handlers_pattern, file_content))
    if matches:
        # Add after the last registered handler
        last_match = matches[-1]
        insert_position = last_match.end()
        new_content = (
            file_content[:insert_position] + error_handler_code + file_content[insert_position:]
        )
        return new_content

    return file_content


def fix_file(file_path):
    """Applies all fixes to a file"""
    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return False

    # Create backup
    if not backup_file(file_path):
        return False

    # Read the content
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Apply fixes
    content = fix_updater_config(content)
    content = fix_polling_config(content)
    content = add_error_handler(content)

    # Save the modified content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"File fixed: {file_path}")
    return True


def main():
    """Main function"""
    logger.info("Starting fixes for the Telegram bot EVA & GUARANI...")

    success_count = 0
    for file_path in TARGET_FILES:
        if os.path.exists(file_path):
            if fix_file(file_path):
                success_count += 1
        else:
            logger.warning(f"File not found: {file_path}")

    logger.info(f"Process completed. {success_count} files fixed.")

    if success_count > 0:
        logger.info("You can now restart the bot with: ./setup_and_start.ps1")
    else:
        logger.warning("No files were fixed. Check the logs for more details.")


if __name__ == "__main__":
    main()
