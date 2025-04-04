#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Status Checker
This script checks if the bot is running and displays information about the process.
"""

import os
import sys
import psutil
import time
from datetime import datetime, timedelta


def format_time(seconds):
    """Formats time in seconds to a readable format."""
    return str(timedelta(seconds=seconds))


def check_bot_running():
    """Checks if the bot is running."""
    try:
        for proc in psutil.process_iter(["pid", "name", "cmdline", "create_time"]):
            cmdline = proc.info.get("cmdline", [])
            if cmdline and any("unified_telegram_bot" in cmd for cmd in cmdline if cmd):
                # Bot found
                pid = proc.info["pid"]
                create_time = proc.info["create_time"]
                running_time = time.time() - create_time
                memory_info = proc.memory_info()
                cpu_percent = proc.cpu_percent(interval=0.1)

                print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")
                print("BOT STATUS: ONLINE")
                print(f"PID: {pid}")
                print(
                    f"Started at: {datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')}"
                )
                print(f"Running time: {format_time(running_time)}")
                print(f"Memory usage: {memory_info.rss / (1024 * 1024):.2f} MB")
                print(f"CPU usage: {cpu_percent:.1f}%")
                print("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")
                return True, pid

        # Bot not found
        print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")
        print("BOT STATUS: OFFLINE")
        print("The bot is not running.")
        print("To start the bot, run: . tart_bot.bat")
        print("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")
        return False, None

    except Exception as e:
        print(f"Error checking bot status: {e}")
        return False, None


if __name__ == "__main__":
    check_bot_running()
