#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fix Problematic Files - Script to handle files with complex encoding issues
This script tries multiple approaches to fix encoding issues in specific files.

Version: 1.0.0
Date: 2025-03-20
"""

import os
import sys
from pathlib import Path
import logging
import shutil
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("fix_problematic_files.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Create timestamp for backups
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT_DIR / "backup" / "problematic_files_fix" / TIMESTAMP

# List of problematic files
PROBLEMATIC_FILES = [
    "docs/readme_2.md",
    "docs/ROADMAP.md",
    "docs/STATUS_VISUALIZATION.md",
    "docs/UNIFIED_DOCUMENTATION.md",
    "docs/archived/README_FREEMIUM.md",
]

# List of encodings to try
ENCODINGS = [
    "utf-8",
    "utf-8-sig",
    "utf-16",
    "utf-16le",
    "utf-16be",
    "cp1252",
    "iso-8859-1",
    "latin1",
    "ascii",
    "windows-1254",
    "windows-1252",
    "macroman",
]


def create_backup(file_path):
    """Create a backup of a file before modifying it"""
    rel_path = file_path.relative_to(ROOT_DIR)
    backup_path = BACKUP_DIR / rel_path

    # Create parent directories
    backup_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy the file
    shutil.copy2(file_path, backup_path)
    logging.info(f"Created backup of {rel_path}")


def fix_file_encoding(file_path):
    """Fix the encoding of a problematic file by trying multiple encodings"""
    try:
        # Read the file in binary mode
        with open(file_path, "rb") as f:
            raw_content = f.read()

        # Try each encoding
        for encoding in ENCODINGS:
            try:
                content = raw_content.decode(encoding)

                # If we get here, the encoding worked
                # Create backup
                create_backup(file_path)

                # Write back in UTF-8
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                logging.info(f"Successfully fixed encoding of {file_path} using {encoding}")
                return True

            except UnicodeDecodeError:
                continue

        logging.error(f"Failed to fix {file_path} - no working encoding found")
        return False

    except Exception as e:
        logging.error(f"Error processing {file_path}: {str(e)}")
        return False


def main():
    """Main execution function"""
    logging.info("=== STARTING PROBLEMATIC FILES FIX PROCESS ===")

    success_count = 0
    failed_files = []

    try:
        for file_path in PROBLEMATIC_FILES:
            full_path = ROOT_DIR / file_path
            if fix_file_encoding(full_path):
                success_count += 1
            else:
                failed_files.append(file_path)

        # Log results
        logging.info(f"Successfully fixed {success_count} files")
        if failed_files:
            logging.warning(f"Failed to fix {len(failed_files)} files:")
            for file in failed_files:
                logging.warning(f"  - {file}")

        logging.info("=== PROBLEMATIC FILES FIX PROCESS COMPLETED ===")

    except Exception as e:
        logging.error(f"Error during problematic files fix: {str(e)}")
        logging.info("=== PROBLEMATIC FILES FIX PROCESS FAILED ===")


if __name__ == "__main__":
    main()
