#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Organize Logs - Script to organize system logs into a proper structure
This script moves all logs from the root to data/logs with an organized structure.

Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Root directory of the project
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Create log directory before configuring logging
log_dir = ROOT_DIR / "data" / "logs" / "system"
log_dir.mkdir(parents=True, exist_ok=True)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(str(log_dir / "log_organization.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Directory structure for logs
LOG_STRUCTURE = {
    "system": [
        "reorganization_final.log",
        "system_reorganization.log",
        "system_integrity_check.log",
    ],
    "quarantine": ["quarantine_folders_log.txt"],
}


def setup_log_directories():
    """Sets up the directory structure for logs"""
    logs_base = ROOT_DIR / "data" / "logs"

    # Create directories for each category
    for category in LOG_STRUCTURE.keys():
        (logs_base / category).mkdir(parents=True, exist_ok=True)

    return logs_base


def move_logs():
    """Moves logs to their respective folders"""
    logs_base = setup_log_directories()
    moved_count = 0

    for category, log_files in LOG_STRUCTURE.items():
        category_dir = logs_base / category

        for log_file in log_files:
            source = ROOT_DIR / log_file
            if source.exists():
                # Add timestamp to the file name to preserve history
                timestamp = datetime.fromtimestamp(source.stat().st_mtime).strftime("%Y%m%d_%H%M%S")
                new_name = f"{log_file.rsplit('.', 1)[0]}_{timestamp}.{log_file.rsplit('.', 1)[1]}"
                destination = category_dir / new_name

                try:
                    shutil.move(str(source), str(destination))
                    logging.info(f"Moved: {log_file} -> {destination.relative_to(ROOT_DIR)}")
                    moved_count += 1
                except Exception as e:
                    logging.error(f"Error moving {log_file}: {str(e)}")

    return moved_count


def update_log_config():
    """Updates reorganization scripts to use the new log structure"""
    scripts_to_update = [
        "tools/utilities/reorganize_final.py",
        "tools/utilities/reorganize_simple.py",
        "tools/utilities/reorganize_workspace.py",
    ]

    for script_path in scripts_to_update:
        script = ROOT_DIR / script_path
        if not script.exists():
            continue

        try:
            with open(script, "r", encoding="utf-8") as f:
                content = f.read()

            # Update logging configuration
            content = content.replace(
                'logging.FileHandler("reorganization_final.log"',
                'logging.FileHandler("data/logs/system/reorganization_final.log"',
            )
            content = content.replace(
                'logging.FileHandler("system_reorganization.log"',
                'logging.FileHandler("data/logs/system/system_reorganization.log"',
            )

            with open(script, "w", encoding="utf-8") as f:
                f.write(content)

            logging.info(f"Updated script: {script_path}")

        except Exception as e:
            logging.error(f"Error updating {script_path}: {str(e)}")


def main():
    """Main function"""
    logging.info("=== STARTING LOG ORGANIZATION ===")

    try:
        # Move existing logs
        moved_count = move_logs()
        logging.info(f"Total of {moved_count} logs moved successfully")

        # Update configuration in scripts
        update_log_config()

        logging.info("=== LOG ORGANIZATION COMPLETED ===")

    except Exception as e:
        logging.error(f"Error during log organization: {str(e)}")
        logging.info("=== LOG ORGANIZATION INTERRUPTED WITH ERRORS ===")


if __name__ == "__main__":
    main()
