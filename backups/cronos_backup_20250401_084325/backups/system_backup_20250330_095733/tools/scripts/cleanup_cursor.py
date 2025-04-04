#!/usr/bin/env python3
import os
import shutil
import json
from pathlib import Path
import datetime


def cleanup_cursor_cache():
    """Clean up Cursor cache directories"""
    cursor_cache_paths = [
        Path.home() / ".cursor" / "cache",
        Path.home() / ".cursor" / "tmp",
        Path.home() / "AppData" / "Local" / "Cursor" / "Cache",
        Path.home() / "AppData" / "Local" / "Cursor" / "Code Cache",
        Path.home() / "AppData" / "Local" / "Cursor" / "GPUCache",
    ]

    for cache_path in cursor_cache_paths:
        if cache_path.exists():
            try:
                if cache_path.is_dir():
                    shutil.rmtree(cache_path)
                else:
                    os.remove(cache_path)
                print(f"Cleaned: {cache_path}")
            except Exception as e:
                print(f"Error cleaning {cache_path}: {e}")


def quick_context_backup():
    """Create a quick backup of important files"""
    base_path = Path("C:/Eva & Guarani - EGOS")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = base_path / "CHATS" / f"backup_context_{timestamp}"

    try:
        # Create backup directory
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Files to backup
        important_paths = [
            base_path / "CHATS" / "current_chat.md",
            base_path / "CHATS" / "chat_index.json",
            base_path / "QUANTUM_PROMPTS" / "VERSION_PERA.md",
            base_path / "QUANTUM_PROMPTS" / "core_principles.md",
        ]

        # Copy files
        for path in important_paths:
            if path.exists():
                shutil.copy2(path, backup_dir / path.name)
                print(f"Backed up: {path.name}")

        # Save current state
        state = {
            "timestamp": timestamp,
            "type": "emergency_backup",
            "files": [str(p) for p in important_paths if p.exists()],
            "metadata": {"reason": "cursor_performance", "backup_type": "emergency"},
        }

        with open(backup_dir / "emergency_state.json", "w") as f:
            json.dump(state, f, indent=2)

        print(f"\nBackup created at: {backup_dir}")
        return True

    except Exception as e:
        print(f"Error during backup: {e}")
        return False


if __name__ == "__main__":
    print("Starting emergency backup and cleanup...")
    if quick_context_backup():
        print("\nStarting Cursor cache cleanup...")
        cleanup_cursor_cache()
        print("\nOperation completed. You can now restart Cursor safely.")
