#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reorganize Folders - Final script to reorganize unorganized folders
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
    handlers=[logging.StreamHandler()],
)

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Folders that are part of the main structure and should be kept
CORE_DIRS = [
    "core",
    "modules",
    "integrations",
    "tools",
    "docs",
    "tests",
    "ui",
    "data",
    "backup",
    "quarantine",
]

# Version control and editor folders that should be kept
SYSTEM_DIRS = [".git", ".github", ".vscode", ".obsidian", ".bolt", ".cursor", "__pycache__", "venv"]

# Mapping of remaining folders to reorganize
MOVE_MAPPING = {
    # Move to core/
    "config": "core/config",
    "EGOS": "core/egos",
    "ethics": "core/ethik",
    "ethik-core": "core/ethik/legacy",
    # Move to modules/
    "quantum": "modules/quantum",
    "eliza": "modules/eliza",
    "eliza_os": "modules/eliza/os",
    "blockchain": "modules/blockchain",
    "gamification": "modules/gamification",
    "src": "modules/legacy_src",
    # Move to integrations/
    "bot": "integrations/bots/bot_legacy",
    "temp_bot": "integrations/bots/temp",
    "extensions": "integrations/extensions",
    "prompts": "integrations/prompts",
    "QUANTUM_PROMPTS": "integrations/prompts/quantum",
    # Move to tools/
    "utils": "tools/utils",
    "system_analysis": "tools/analysis",
    # Move to data/
    "personas": "data/personas",
    "logs": "data/logs",
    "story_elements": "data/story_elements",
    "examples": "data/examples",
    # Move to docs/
    "reports": "docs/reports",
    # Move to backup/history/
    "backup_20250301_171540": "backup/history/backup_20250301_171540",
    "backup_before_reorganization": "backup/history/backup_before_reorganization",
    "backup_pre_reorganization_20250319": "backup/history/backup_pre_reorganization_20250319",
    "backup_quantum": "backup/history/backup_quantum",
    "backups": "backup/history/backups",
    "essential_backup_20250228_164242": "backup/history/essential_backup_20250228_164242",
    "shared_egos_20250301_163205": "backup/history/shared_egos_20250301_163205",
    "arquivos_antigos_20250301_171050": "backup/history/arquivos_antigos_20250301_171050",
    # Move to quarantine/
    "quarantine": "quarantine/quarantine",
    "quarentena_20250319": "quarantine/quarentena_20250319",
    "quarentena_duplicados_20250319": "quarantine/quarentena_duplicados_20250319",
    "quarentena_pastas_20250319": "quarantine/quarentena_pastas_20250319",
}


def ensure_dirs_exist():
    """Ensure that the main directories exist"""
    for dir_name in CORE_DIRS:
        (ROOT_DIR / dir_name).mkdir(exist_ok=True)

    (ROOT_DIR / "backup" / "history").mkdir(parents=True, exist_ok=True)


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

    # If the destination already exists, use merge strategy
    if dest_path.exists():
        try:
            # Create subdirectory for merged content
            merge_dir = dest_path / f"merged_from_{source}"
            merge_dir.mkdir(exist_ok=True)

            # Copy content to subdirectory
            for item in source_path.iterdir():
                target = merge_dir / item.name
                if item.is_dir():
                    if target.exists():
                        logging.warning(f"Subdirectory already exists, skipping: {item.name}")
                    else:
                        shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)

            # Remove original directory
            shutil.rmtree(source_path)
            logging.info(f"Merged: {source} -> {destination}/merged_from_{source}")
            return True
        except Exception as e:
            logging.error(f"Error merging {source}: {str(e)}")
            return False
    else:
        try:
            # Move directory directly
            shutil.move(str(source_path), str(dest_path))
            logging.info(f"Moved: {source} -> {destination}")
            return True
        except Exception as e:
            logging.error(f"Error moving {source}: {str(e)}")
            return False


def scan_and_move_unmapped():
    """Scan and move unmapped folders to quarantine"""
    unmapped_dirs = []

    # Find unmapped directories
    for item in ROOT_DIR.iterdir():
        if not item.is_dir():
            continue

        dir_name = item.name

        # Ignore directories that are part of the main structure
        if dir_name in CORE_DIRS or dir_name in SYSTEM_DIRS:
            continue

        # Ignore directories already in the mapping
        if dir_name in MOVE_MAPPING:
            continue

        unmapped_dirs.append(dir_name)

    # Move unmapped directories to quarantine
    if unmapped_dirs:
        logging.info(f"Found {len(unmapped_dirs)} unmapped directories")

        # Create others directory in quarantine
        others_dir = ROOT_DIR / "quarantine" / "others"
        others_dir.mkdir(parents=True, exist_ok=True)

        # Move each unmapped directory
        for dir_name in unmapped_dirs:
            source_path = ROOT_DIR / dir_name
            dest_path = others_dir / dir_name

            try:
                shutil.move(str(source_path), str(dest_path))
                logging.info(f"Moved to quarantine: {dir_name}")
            except Exception as e:
                logging.error(f"Error moving {dir_name} to quarantine: {str(e)}")


def main():
    """Main execution function"""
    logging.info("=== STARTING FINAL DIRECTORY REORGANIZATION ===")

    # Ensure that the main directories exist
    ensure_dirs_exist()

    # Count of moved directories
    success_count = 0

    # Move mapped directories
    for source, destination in MOVE_MAPPING.items():
        if move_directory(source, destination):
            success_count += 1

    logging.info(f"Moved {success_count} of {len(MOVE_MAPPING)} mapped directories")

    # Move unmapped directories to quarantine/others
    scan_and_move_unmapped()

    logging.info("=== FINAL REORGANIZATION COMPLETED ===")


if __name__ == "__main__":
    main()
