#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Update Checker
This script checks if there are updates available for the bot and notifies the administrators.
"""

import os
import sys
import json
import logging
import argparse
import subprocess
from datetime import datetime, timedelta

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/update_checker.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("update_checker")

# Load configuration
CONFIG_PATH = os.path.join("config", "eva_guarani_config.json")

def load_config():
    """Loads the bot configuration."""
    try:
        if not os.path.exists(CONFIG_PATH):
            logger.error(f"Configuration file not found: {CONFIG_PATH}")
            return None
        
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
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
            check=False
        )
        return result.returncode == 0
    except Exception:
        return False

def check_for_updates():
    """Checks if there are updates available in the Git repository."""
    try:
        # Update remote references
        subprocess.run(
            ["git", "fetch"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        
        # Check if there are differences between the local and remote branches
        result = subprocess.run(
            ["git", "rev-list", "HEAD..origin/main", "--count"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        commit_count = int(result.stdout.strip())
        
        if commit_count > 0:
            # Get information about the available updates
            log_result = subprocess.run(
                ["git", "log", "HEAD..origin/main", "--pretty=format:%h %s"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            updates = log_result.stdout.strip().split('\n')
            return True, commit_count, updates
        else:
            return False, 0, []
    except Exception as e:
        logger.error(f"Error checking for updates: {e}")
        return False, 0, []

def get_last_check_time():
    """Gets the date and time of the last update check."""
    try:
        last_check_file = os.path.join("logs", "last_update_check.txt")
        
        if not os.path.exists(last_check_file):
            return None
        
        with open(last_check_file, 'r') as f:
            timestamp = f.read().strip()
            
        return datetime.fromisoformat(timestamp)
    except Exception as e:
        logger.error(f"Error getting last check date: {e}")
        return None

def save_check_time():
    """Saves the current date and time as the last update check."""
    try:
        last_check_file = os.path.join("logs", "last_update_check.txt")
        
        with open(last_check_file, 'w') as f:
            f.write(datetime.now().isoformat())
            
        return True
    except Exception as e:
        logger.error(f"Error saving check date: {e}")
        return False

def send_notification(message):
    """Sends a notification about available updates."""
    try:
        if os.path.exists("notify_status.py"):
            logger.info("Sending notification about available updates...")
            
            result = subprocess.run(
                [sys.executable, "notify_status.py", "--message", message, "--force"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
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
    parser = argparse.ArgumentParser(description='Check for updates for the EVA & GUARANI bot')
    parser.add_argument('--force', action='store_true', help='Force check even if it was recently checked')
    parser.add_argument('--interval', type=int, default=24, help='Minimum interval between checks in hours (default: 24)')
    parser.add_argument('--notify-always', action='store_true', help='Notify even if there are no updates')
    args = parser.parse_args()
    
    # Check if it is a Git repository
    if not is_git_repository():
        logger.error("This directory is not a Git repository.")
        logger.error("Update checking only works with Git-based installations.")
        return 1
    
    # Check if it was recently checked
    if not args.force:
        last_check = get_last_check_time()
        if last_check is not None:
            time_since_last_check = datetime.now() - last_check
            if time_since_last_check < timedelta(hours=args.interval):
                logger.info(f"Last check was {time_since_last_check.total_seconds() / 3600:.1f} hours ago.")
                logger.info(f"Waiting for minimum interval of {args.interval} hours.")
                return 0
    
    # Check for updates
    logger.info("Checking for updates...")
    has_updates, commit_count, updates = check_for_updates()
    
    # Save check time
    save_check_time()
    
    if has_updates:
        logger.info(f"{commit_count} updates available:")
        for update in updates:
            logger.info(f"   - {update}")
        
        # Prepare notification message
        notification_message = f"""
🔄 <b>UPDATES AVAILABLE</b> - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

<b>Available updates:</b> {commit_count}
<b>Details:</b>
"""
        for update in updates[:5]:  # Limit to 5 updates to avoid overloading the message
            notification_message += f"- {update}\n"
        
        if len(updates) > 5:
            notification_message += f"... and {len(updates) - 5} more updates.\n"
            
        notification_message += """
<b>To update:</b>
- Windows: Run update_bot.bat
- Linux/Mac: Run ./update_bot.sh
- Or run: python update_bot."""
        
        # Send notification
        send_notification(notification_message)
        return 0
    else:
        logger.info("No updates available.")
        
        if args.notify_always:
            notification_message = f"""
✅ <b>BOT UPDATED</b> - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

The bot is already at the latest version. No updates available.
"""
            send_notification(notification_message)
        
        return 0

if __name__ == "__main__":
    sys.exit(main())