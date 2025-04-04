#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Bot Files Organizer
==================================

Script to organize and clean up the bot files, moving obsolete or duplicate files to quarantine.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0.0
"""

import os
import shutil
import datetime
import json
from pathlib import Path

# Get current time for organizing
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
quarantine_dir = os.path.join(project_root, "quarantine", "telegram_bot", timestamp)

# Create quarantine directory
os.makedirs(quarantine_dir, exist_ok=True)

# Files to keep
files_to_keep = [
    # Main bot implementations
    "simple_telegram_bot.py",
    "simple_bot.py",
    # Configuration files
    "telegram_config.json",
    # Startup scripts
    "start_bot.bat",
    "start_bot_with_payment.bat",
    # Utility scripts
    "check_bot.py",
    "open_telegram_web.py",
    "get_telegram_id.py",
    # Documentation
    "README.md",
    # Directories to keep
    "logs",
    "__pycache__",
]

# Files to move to quarantine
files_to_quarantine = [
    # Duplicate bot implementations
    "eva_guarani_telegram_bot.py",
    "unified_telegram_bot_utf8.py",
    "unified_telegram_bot_utf8_1.py",
    "unified_telegram_bot_utf8_2.py",
    "telegram_bot_with_knowledge.py",
    "minimal_bot.py",
    "run_bot.py",
    "run_bot_direct.py",
    "start_bot_direct.py",
    # Obsolete configuration files
    "telegram_bot.json",
    "bot_config.json",
    # Obsolete startup scripts
    "start_eva_bot.bat",
    "start_eva_guarani_bot.bat",
    "start_simple_bot.bat",
    "start_telegram_bot.bat",
    "start_telegram_eliza_bridge.bat",
    "check_bot_status.bat",
    "check_bot_health.bat",
    "start_bot_with_payment.sh",
    # Obsolete utility scripts
    "check_telegram.py",
    "check_bot_status.py",
    "fix_telegram_bot.py",
    "test_bot_config.py",
    "test_bot_modules.py",
    "test_telegram_bot.py",
    "start_telegram_bot.py",
    "start_telegram_eliza_bridge.py",
    # PowerShell scripts
    "run_telegram_bot_service.ps1",
    "check_bot_health.ps1",
    # Log files
    "telegram_bot.log",
    "bot_package.log",
    "telegram_eliza_bridge.log",
]

# Track results
moved_files = []
skipped_files = []
kept_files = []

# Process files in current directory
print(f"✧༺❀༻∞ EVA & GUARANI - Bot Files Organizer ∞༺❀༻✧")
print(f"Organizing files in: {current_dir}")
print(f"Quarantine directory: {quarantine_dir}")
print("=" * 60)

for item in os.listdir(current_dir):
    item_path = os.path.join(current_dir, item)

    # Skip if it's a directory in the keep list
    if os.path.isdir(item_path) and item in files_to_keep:
        kept_files.append(item)
        continue

    # Skip if it's a file to keep
    if item in files_to_keep:
        kept_files.append(item)
        continue

    # Move to quarantine if it's in the quarantine list
    if item in files_to_quarantine:
        try:
            destination = os.path.join(quarantine_dir, item)

            # Create subdirectories if it's a directory
            if os.path.isdir(item_path):
                shutil.copytree(item_path, destination)
                # We don't remove directories yet, just copy them
                print(f"Copied directory: {item} ➡️ quarantine")
            else:
                shutil.copy2(item_path, destination)
                # Handle edge case where the file might be in use
                try:
                    os.remove(item_path)
                    print(f"Moved file: {item} ➡️ quarantine")
                except:
                    print(f"Copied file (couldn't remove): {item} ➡️ quarantine")

            moved_files.append(item)
        except Exception as e:
            print(f"Error processing {item}: {e}")
            skipped_files.append(item)
    else:
        skipped_files.append(item)

# Create manifest.json in quarantine directory
manifest = {
    "timestamp": timestamp,
    "moved_files": moved_files,
    "skipped_files": skipped_files,
    "kept_files": kept_files,
    "description": "Automated cleanup of bot files to reduce redundancy and improve organization",
}

with open(os.path.join(quarantine_dir, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

# Print summary
print("\n" + "=" * 60)
print(f"Cleanup Summary:")
print(f"✅ Files kept: {len(kept_files)}")
print(f"🔄 Files moved to quarantine: {len(moved_files)}")
print(f"⏩ Files skipped: {len(skipped_files)}")
print("=" * 60)

print("\nCreated quarantine manifest: manifest.json")
print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

# If run directly
if __name__ == "__main__":
    print("\nDone! Files have been organized.")
    print("To restore files from quarantine, copy them back from:")
    print(f"{quarantine_dir}")
