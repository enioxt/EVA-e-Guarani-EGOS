#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Bot Monitor
This script monitors the Telegram bot and automatically restarts it if it stops.
"""

import os
import sys
import time
import json
import logging
import subprocess
import argparse
from datetime import datetime, timedelta

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("monitor")

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

def is_bot_running():
    """Checks if the bot is already running."""
    try:
        import psutil
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and any('unified_telegram_bot' in cmd for cmd in cmdline if cmd):
                    return True, proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return False, None
    except ImportError:
        logger.warning("Module psutil not found. Cannot check processes.")
        return False, None
    except Exception as e:
        logger.error(f"Error checking processes: {e}")
        return False, None

def check_bot_status(bot_token):
    """Checks if the bot is online using the Telegram API."""
    try:
        import requests
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                return True, data.get("result", {})
            else:
                return False, data.get("description", "Unknown error")
        else:
            return False, f"Telegram API error: {response.status_code}"
    except Exception as e:
        return False, f"Error checking bot status: {e}"

def restart_bot():
    """Restarts the Telegram bot."""
    try:
        logger.info("Restarting the bot...")
        
        # Use the start_eva_guarani.py script to restart the bot
        start_script = "start_eva_guarani.py"
        
        if os.path.exists(start_script):
            subprocess.call([sys.executable, start_script, "--restart"])
            logger.info("Restart command sent successfully.")
            return True
        else:
            logger.error(f"Start script not found: {start_script}")
            
            # Try to start the bot script directly
            bot_script = os.path.join("bot", "unified_telegram_bot_utf8.py")
            
            if os.path.exists(bot_script):
                if sys.platform == 'win32':
                    subprocess.Popen(
                        f'start "EVA & GUARANI Bot" /min {sys.executable} {bot_script}',
                        shell=True
                    )
                else:
                    log_file = os.path.join("logs", "bot_output.log")
                    subprocess.Popen(
                        f'nohup {sys.executable} {bot_script} > {log_file} 2>&1 &',
                        shell=True,
                        preexec_fn=os.setpgrp
                    )
                logger.info("Bot started directly.")
                return True
            else:
                logger.error(f"Bot script not found: {bot_script}")
                return False
    except Exception as e:
        logger.error(f"Error restarting the bot: {e}")
        return False

def send_notification(message):
    """Sends a notification about the bot status."""
    try:
        # Log the notification
        logger.info(f"Notification: {message}")
        
        # Try to send via Telegram if possible
        config = load_config()
        if config:
            bot_token = config.get("telegram", {}).get("bot_token") or config.get("bot_token")
            admin_users = config.get("telegram", {}).get("admin_users", [])
            
            if bot_token and admin_users:
                try:
                    import requests
                    for admin_id in admin_users:
                        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                        data = {
                            "chat_id": admin_id,
                            "text": f"🤖 MONITOR: {message}",
                            "parse_mode": "HTML"
                        }
                        requests.post(url, json=data, timeout=10)
                    logger.info("Notification sent via Telegram.")
                except Exception as e:
                    logger.error(f"Error sending notification via Telegram: {e}")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")

def check_log_errors():
    """Checks log files for recent errors."""
    try:
        log_files = [
            "logs/unified_bot.log",
            "logs/eva_guarani.log",
            "logs/startup.log"
        ]
        
        recent_errors = []
        
        for log_file in log_files:
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    # Read the last 50 lines
                    lines = f.readlines()[-50:]
                    
                    # Look for errors
                    for line in lines:
                        if "ERROR" in line or "CRITICAL" in line:
                            recent_errors.append(f"{log_file}: {line.strip()}")
        
        return recent_errors
    except Exception as e:
        logger.error(f"Error checking logs: {e}")
        return [f"Error checking logs: {e}"]

def monitor_bot(check_interval=60, max_failures=3, restart_delay=5):
    """
    Monitors the bot and restarts it if necessary.
    
    Args:
        check_interval: Interval in seconds between checks
        max_failures: Maximum number of consecutive failures before restarting
        restart_delay: Time in seconds to wait after restarting
    """
    logger.info(f"Starting bot monitoring (interval: {check_interval}s)")
    
    config = load_config()
    if not config:
        logger.error("Could not load configuration. Monitoring stopped.")
        return
    
    bot_token = config.get("telegram", {}).get("bot_token") or config.get("bot_token")
    if not bot_token:
        logger.error("Bot token not found in configuration. Monitoring stopped.")
        return
    
    consecutive_failures = 0
    last_restart_time = datetime.now() - timedelta(hours=1)  # Initialize to allow immediate restart if needed
    
    while True:
        try:
            current_time = datetime.now()
            logger.info(f"Checking bot status at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Check if the process is running
            process_running, pid = is_bot_running()
            
            # Check if the bot is responding on the Telegram API
            api_running, info = check_bot_status(bot_token)
            
            if process_running and api_running:
                # Bot is working correctly
                logger.info(f"Bot is working correctly (PID: {pid}, Username: @{info.get('username')})")
                consecutive_failures = 0
            else:
                # Bot is not working correctly
                consecutive_failures += 1
                
                if not process_running:
                    logger.warning(f"Bot process not found. Failure {consecutive_failures}/{max_failures}")
                
                if not api_running:
                    logger.warning(f"Bot not responding on Telegram API: {info}. Failure {consecutive_failures}/{max_failures}")
                
                # Check logs for recent errors
                errors = check_log_errors()
                if errors:
                    logger.warning(f"Found {len(errors)} recent errors in logs")
                    for error in errors[:3]:  # Show only the first 3 errors
                        logger.warning(f"Log error: {error}")
                
                # Restart the bot if it reaches the maximum number of failures and enough time has passed since the last restart
                if consecutive_failures >= max_failures and (current_time - last_restart_time).total_seconds() > 300:  # 5 minutes
                    logger.warning(f"Reached limit of {max_failures} consecutive failures. Restarting the bot...")
                    
                    # Send notification
                    send_notification(f"Bot not responding after {consecutive_failures} checks. Automatically restarting.")
                    
                    # Restart the bot
                    if restart_bot():
                        last_restart_time = datetime.now()
                        logger.info(f"Bot restarted at {last_restart_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        consecutive_failures = 0
                        
                        # Wait for the bot to initialize
                        logger.info(f"Waiting {restart_delay} seconds for the bot to initialize...")
                        time.sleep(restart_delay)
                    else:
                        logger.error("Failed to restart the bot.")
            
            # Wait until the next check
            logger.info(f"Next check in {check_interval} seconds.")
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            logger.info("Monitoring interrupted by user.")
            break
        except Exception as e:
            logger.error(f"Error during monitoring: {e}")
            time.sleep(check_interval)  # Continue monitoring even after error

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Monitor the EVA & GUARANI bot')
    parser.add_argument('--interval', type=int, default=60, help='Interval in seconds between checks (default: 60)')
    parser.add_argument('--max-failures', type=int, default=3, help='Maximum number of consecutive failures before restarting (default: 3)')
    parser.add_argument('--restart-delay', type=int, default=5, help='Time in seconds to wait after restarting (default: 5)')
    args = parser.parse_args()
    
    print("=" * 50)
    print("EVA & GUARANI - Bot Monitor")
    print("=" * 50)
    print(f"Check interval: {args.interval} seconds")
    print(f"Maximum consecutive failures: {args.max_failures}")
    print(f"Delay after restart: {args.restart_delay} seconds")
    print("=" * 50)
    print("Press Ctrl+C to stop monitoring.")
    print("=" * 50)
    
    # Start monitoring
    monitor_bot(
        check_interval=args.interval,
        max_failures=args.max_failures,
        restart_delay=args.restart_delay
    )

if __name__ == "__main__":
    main()