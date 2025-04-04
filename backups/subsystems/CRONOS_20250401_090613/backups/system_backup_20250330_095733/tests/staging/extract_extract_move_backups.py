#!/usr/bin/env python3
# Important content extracted from staging\extract_move_backups.py
# Original file moved to quarantine
# Date: 2025-03-22 08:45:53

# Important content extracted from tools\utilities\move_backups.py
# Original file moved to quarantine
# Date: 2025-03-22 08:37:23

python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Move Backups - Script to move backup and quarantine folders
Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import shutil
import logging
from pathlib import Path

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Mapping of backup folders to reorganize
BACKUP_MAPPING = {
    "backup_20250301_171540": "backup/history/backup_20250301_171540",
    "backup_before_reorganization": "backup/history/backup_before_reorganization",
    "backup_pre_reorganization_20250319": "backup/history/backup_pre_reorganization_20250319",
    "backup_quantum": "backup/history/backup_quantum",
    "backups": "backup/history/backups",
    "essential_backup_20250228_164242": "backup/history/essential_backup_20250228_164242",
    "shared_egos_20250301_163205": "backup/history/shared_egos_20250301_163205",
    "old_files_20250301_171050": "backup/history/old_files_20250301_171050"
}

# Mapping of quarantine folders to reorganize
QUARANTINE_MAPPING = {
    "quarantine": "quarantine/quarantine",
    "quarantine_20250319": "quarantine/quarantine_20250319",
    "quarantine_duplicates_20250319": "quarantine/quarantine_duplicates_20250319",
    "quarantine_folders_20250319": "quarantine/quarantine_folders_20250319"
}

def ensure_dirs_exist():
    """Ensure that the destination directories exist"""
    (ROOT_DIR / "backup").mkdir(exist_ok=True)
    (ROOT_DIR / "backup" / "history").mkdir(parents=True, exist_ok=True)
    (ROOT_DIR / "quarantine").mkdir(exist_ok=True)

def move_directory(source, destination):
    """Move a directory to the specified destination"""
    source_path = ROOT_DIR / source
    dest_path = ROOT_DIR / destination

    # Check if the source directory exists
    if not source_path.exists() or not source_path.is_dir():
        logging.warning(f"Source directory not found: {source}")
        return False

    # Create parent directories of the destination
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Move directory directly
        shutil.move(str(source_path), str(dest_path))
        logging.info(f"Moved: {source} -> {destination}")
        return True
    except Exception as e:
        logging.error(f"Error moving {source}: {str(e)}")
        return False

def main():
    """Main execution function"""
    logging.info("=== STARTING BACKUP AND QUARANTINE MOVEMENT ===")

    # Ensure that the destination directories exist
    ensure_dirs_exist()

    # Move backup folders
    backup_count = 0
    for source, destination in BACKUP_MAPPING.items():
        if move_directory(source, destination):
            backup_count += 1

    logging.info(f"Moved {backup_count} of {len(BACKUP_MAPPING)} backup directories")

    # Move quarantine folders
    quarantine_count = 0
    for source, destination in QUARANTINE_MAPPING.items():
        if move_directory(source, destination):
            quarantine_count += 1

    logging.info(f"Moved {quarantine_count} of {len(QUARANTINE_MAPPING)} quarantine directories")

    logging.info("=== BACKUP AND QUARANTINE MOVEMENT COMPLETED ===")

if __name__ == "__main__":
    main()

# End of extracted content
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧


# End of extracted content
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
