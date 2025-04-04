#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Optimize Modules - Script to optimize and consolidate system modules
This script reorganizes and consolidates duplicated or overlapping modules.

Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Create logs directory
log_dir = ROOT_DIR / "data" / "logs" / "system"
log_dir.mkdir(parents=True, exist_ok=True)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(str(log_dir / "module_optimization.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Mapping of modules to move/consolidate
MODULE_MOVES = {
    # Move to core/
    "modules/atlas": "core/atlas",
    "modules/nexus": "core/nexus",
    "modules/cronos": "core/cronos",
    "modules/ethical": "core/ethik/modules",
    # Consolidate bots and APIs
    "modules/bot": "integrations/bots/modules",
    "modules/api": "integrations/apis/modules",
    # Consolidate Eliza
    "modules/eliza_legacy": "modules/eliza/legacy",
    # Reorganize special modules
    "modules/prometheus": "modules/monitoring",
    "modules/mycelium": "modules/nexus/connections",
    "modules/love": "modules/ai/emotional",
    "modules/memory": "modules/ai/memory",
}

# Modules to merge (source: destination)
MODULE_MERGES = {
    "modules/ai": "modules/quantum/intelligence",
    "modules/love": "modules/quantum/consciousness",
}


def move_module(source, destination):
    """Move a module to a new location, preserving history"""
    source_path = ROOT_DIR / source
    dest_path = ROOT_DIR / destination

    if not source_path.exists():
        logging.warning(f"Source module not found: {source}")
        return False

    try:
        # Create destination directory
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if dest_path.exists():
            # If destination exists, create subdirectory for old content
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = dest_path.parent / f"{dest_path.name}_pre_merge_{timestamp}"
            shutil.move(str(dest_path), str(backup_dir))
            logging.info(f"Backup created: {backup_dir.relative_to(ROOT_DIR)}")

        # Move module
        shutil.move(str(source_path), str(dest_path))
        logging.info(f"Module moved: {source} -> {destination}")
        return True

    except Exception as e:
        logging.error(f"Error moving module {source}: {str(e)}")
        return False


def merge_module(source, destination):
    """Merge a module with another, preserving content"""
    source_path = ROOT_DIR / source
    dest_path = ROOT_DIR / destination

    if not source_path.exists():
        logging.warning(f"Source module not found: {source}")
        return False

    try:
        # Create destination directory
        dest_path.mkdir(parents=True, exist_ok=True)

        # Copy content
        for item in source_path.glob("*"):
            target = dest_path / item.name
            if item.is_dir():
                if target.exists():
                    # If folder already exists, move content to subdirectory
                    merge_dir = target / f"merged_from_{item.name}"
                    merge_dir.mkdir(exist_ok=True)
                    for subitem in item.glob("*"):
                        shutil.move(str(subitem), str(merge_dir / subitem.name))
                else:
                    shutil.copytree(item, target)
            else:
                if not target.exists():
                    shutil.copy2(item, target)

        # Create merge log file
        merge_log = dest_path / "_MERGE_INFO.md"
        with open(merge_log, "a", encoding="utf-8") as f:
            f.write(f"\n## Merged from {source}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source: {source}\n")
            f.write("---\n")

        # Remove source directory after merging
        shutil.rmtree(source_path)
        logging.info(f"Module merged: {source} -> {destination}")
        return True

    except Exception as e:
        logging.error(f"Error merging module {source}: {str(e)}")
        return False


def update_imports():
    """Update imports in Python files to reflect new structure"""
    python_files = list(ROOT_DIR.rglob("*.py"))

    for file in python_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()

            # Update imports
            for old_path, new_path in MODULE_MOVES.items():
                old_import = old_path.replace("/", ".")
                new_import = new_path.replace("/", ".")
                content = content.replace(f"from {old_import}", f"from {new_import}")
                content = content.replace(f"import {old_import}", f"import {new_import}")

            with open(file, "w", encoding="utf-8") as f:
                f.write(content)

        except Exception as e:
            logging.error(f"Error updating imports in {file}: {str(e)}")


def main():
    """Main function"""
    logging.info("=== STARTING MODULE OPTIMIZATION ===")

    try:
        # Move modules
        for source, destination in MODULE_MOVES.items():
            move_module(source, destination)

        # Merge modules
        for source, destination in MODULE_MERGES.items():
            merge_module(source, destination)

        # Update imports
        update_imports()

        logging.info("=== MODULE OPTIMIZATION COMPLETED ===")

    except Exception as e:
        logging.error(f"Error during module optimization: {str(e)}")
        logging.info("=== MODULE OPTIMIZATION INTERRUPTED WITH ERRORS ===")


if __name__ == "__main__":
    main()
