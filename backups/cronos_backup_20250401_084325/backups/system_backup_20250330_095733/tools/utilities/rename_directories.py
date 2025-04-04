#!/usr/bin/env python3
"""
Directory Renaming Script - Standardize project structure to English

This script renames directories and files from Portuguese to English,
ensuring a consistent naming convention across the project.

Version: 1.0.0
Date: 2025-03-20
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("data/logs/system/rename_directories.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Mapping of directories to rename (old_name: new_name)
RENAME_MAPPING = {
    # Root level directories
    "quarentena": "quarantine",
    # Core directories
    "core/egos": "core/os",
    # Docs directories
    "docs/arquivados": "docs/archived",
    # Quarantine subdirectories
    "quarantine/bots_antigos": "quarantine/old_bots",
    "quarantine/outros": "quarantine/others",
    "quarantine/scripts_obsoletos": "quarantine/obsolete_scripts",
    "quarantine/quarentena_20250319": "quarantine/quarantine_20250319",
    "quarantine/quarentena_duplicados_20250319": "quarantine/duplicates_quarantine_20250319",
    "quarantine/quarentena_pastas_20250319": "quarantine/folders_quarantine_20250319",
    # Ensure these directories exist with English names
    "data/logs": "data/logs",
    "data/backups": "data/backups",
    "docs/reports": "docs/reports",
    "docs/api": "docs/api",
    "docs/user_guides": "docs/user_guides",
    "docs/developer_guides": "docs/developer_guides",
    "docs/architecture": "docs/architecture",
    "docs/tutorials": "docs/tutorials",
}

# Mapping of files to rename (old_name: new_name)
FILE_RENAME_MAPPING = {
    # Documentation files
    "docs/COMPLETE_TRANSITION.md": "docs/COMPLETE_TRANSITION.md",
    "docs/UNIFICATION_SUMMARY.md": "docs/UNIFICATION_SUMMARY.md",
    "docs/FAIR_EXCHANGE_PRINCIPLES.md": "docs/FAIR_EXCHANGE_PRINCIPLES.md",
    "docs/fundamental_principles.md": "docs/fundamental_principles.md",
    "docs/ethical_navigator.md": "docs/ethical_navigator.md",
    "docs/quantum_musician.md": "docs/quantum_musician.md",
    "docs/IMPLEMENTING_FAIR_EXCHANGE.md": "docs/IMPLEMENTING_FAIR_EXCHANGE.md",
    "docs/INSTALLATION_GUIDE_V7.4.md": "docs/INSTALLATION_GUIDE_V7.4.md",
    "docs/INSTALLATION_GUIDE.md": "docs/INSTALLATION_GUIDE.md",
    "docs/IMPLEMENTATION_GUIDE.md": "docs/IMPLEMENTATION_GUIDE.md",
    "docs/knowledge_guardian.md": "docs/knowledge_guardian.md",
    "docs/quantum_gamer.md": "docs/quantum_gamer.md",
    "docs/quantum_philosopher.md": "docs/quantum_philosopher.md",
    "docs/quantum_ethics.md": "docs/quantum_ethics.md",
    "docs/SYSTEM_STRUCTURE.md": "docs/SYSTEM_STRUCTURE.md",
    "docs/quantum_economist.md": "docs/quantum_economist.md",
    "docs/QUANTUM_KNOWLEDGE_DOCUMENTATION.md": "docs/QUANTUM_KNOWLEDGE_DOCUMENTATION.md",
    "docs/cientista_integrador.md": "docs/integration_scientist.md",
    "docs/artista_quantico.md": "docs/quantum_artist.md",
    "docs/FAIR_EXCHANGE_PROMPTS.md": "docs/FAIR_EXCHANGE_PROMPTS.md",
}


def create_backup(path: Path) -> Path:
    """
    Create a backup of the given path in the backup directory.

    Args:
        path: Path to create backup of

    Returns:
        Path: Path to the backup directory
    """
    backup_dir = Path(
        os.path.join(
            str(ROOT_DIR), "backup", "rename_backup", datetime.now().strftime("%Y%m%d_%H%M%S")
        )
    )
    backup_dir.mkdir(parents=True, exist_ok=True)

    try:
        if path.is_file():
            shutil.copy2(str(path), str(backup_dir / path.name))
        else:
            shutil.copytree(str(path), str(backup_dir / path.name))
        logging.info(f"Created backup at {backup_dir}")
    except Exception as e:
        logging.error(f"Failed to create backup: {str(e)}")

    return backup_dir


def rename_directory(old_path: Path, new_path: Path) -> bool:
    """
    Safely rename a directory with backup.

    Args:
        old_path: Current path of the directory
        new_path: New path for the directory

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not old_path.exists():
            logging.warning(f"Source directory not found: {old_path}")
            return False

        if new_path.exists():
            logging.warning(f"Target directory already exists: {new_path}")
            return False

        # Create backup
        backup_dir = create_backup(old_path)

        # Create parent directories if needed
        new_path.parent.mkdir(parents=True, exist_ok=True)

        # Rename directory
        old_path.rename(new_path)
        logging.info(f"Successfully renamed {old_path} to {new_path}")

        return True

    except Exception as e:
        logging.error(f"Error renaming {old_path} to {new_path}: {str(e)}")

        # Try to restore from backup
        if "backup_dir" in locals() and backup_dir.exists():
            try:
                if new_path.exists():
                    shutil.rmtree(new_path)
                backup_path = os.path.join(str(backup_dir), old_path.name)
                shutil.copytree(backup_path, old_path)
                logging.info(f"Restored {old_path} from backup")
            except Exception as restore_error:
                logging.error(f"Failed to restore from backup: {str(restore_error)}")

        return False


def update_imports(file_path: Path, old_name: str, new_name: str) -> None:
    """
    Update import statements in Python files.

    Args:
        file_path: Path to the Python file
        old_name: Old import path
        new_name: New import path
    """
    if not file_path.suffix == ".py":
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace import statements
        old_import = f"from {old_name}"
        new_import = f"from {new_name}"
        content = content.replace(old_import, new_import)

        old_import = f"import {old_name}"
        new_import = f"import {new_name}"
        content = content.replace(old_import, new_import)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        logging.info(f"Updated imports in {file_path}")

    except Exception as e:
        logging.error(f"Error updating imports in {file_path}: {str(e)}")


def update_references(old_name: str, new_name: str) -> None:
    """
    Update references to renamed directories in all Python files.

    Args:
        old_name: Old directory name
        new_name: New directory name
    """
    # Directories to ignore
    IGNORE_DIRS = [".git", "venv", "__pycache__", "backup", "quarentena", "quarantine", "eliza"]

    for py_file in ROOT_DIR.rglob("*.py"):
        if not any(ignore in str(py_file) for ignore in IGNORE_DIRS):
            update_imports(py_file, old_name, new_name)


def rename_file(old_path: Path, new_path: Path) -> bool:
    """
    Safely rename a file with backup.

    Args:
        old_path: Current path of the file
        new_path: New path for the file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not old_path.exists():
            logging.warning(f"Source file not found: {old_path}")
            return False

        if new_path.exists():
            logging.warning(f"Target file already exists: {new_path}")
            return False

        # Create backup
        backup_dir = create_backup(old_path.parent)

        # Create parent directories if needed
        new_path.parent.mkdir(parents=True, exist_ok=True)

        # Rename file
        old_path.rename(new_path)
        logging.info(f"Successfully renamed {old_path} to {new_path}")

        return True

    except Exception as e:
        logging.error(f"Error renaming {old_path} to {new_path}: {str(e)}")

        # Try to restore from backup
        if "backup_dir" in locals() and backup_dir.exists():
            try:
                if new_path.exists():
                    new_path.rename(old_path)
                backup_path = os.path.join(str(backup_dir), old_path.name)
                shutil.copy2(backup_path, old_path)
                logging.info(f"Restored {old_path} from backup")
            except Exception as restore_error:
                logging.error(f"Failed to restore from backup: {str(restore_error)}")

        return False


def update_file_references(old_path: Path, new_path: Path) -> None:
    """
    Update references to renamed files in all markdown and Python files.

    Args:
        old_path: Old file path
        new_path: New file path
    """
    # Directories to ignore
    IGNORE_DIRS = [".git", "venv", "__pycache__", "backup", "quarentena", "quarantine", "eliza"]

    old_name = old_path.stem
    new_name = new_path.stem

    for file_path in ROOT_DIR.rglob("*"):
        if file_path.suffix in [".md", ".py"] and not any(
            ignore in str(file_path) for ignore in IGNORE_DIRS
        ):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Update references in content
                content = content.replace(str(old_path), str(new_path))
                content = content.replace(old_name, new_name)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                logging.info(f"Updated references in {file_path}")

            except Exception as e:
                logging.error(f"Error updating references in {file_path}: {str(e)}")


def main():
    """Main execution function"""
    logging.info("=== Starting Directory and File Renaming Process ===")

    # Create necessary directories
    backup_path = Path(os.path.join(str(ROOT_DIR), "backup", "rename_backup"))
    backup_path.mkdir(parents=True, exist_ok=True)

    dir_success_count = 0
    dir_total_count = len(RENAME_MAPPING)

    file_success_count = 0
    file_total_count = len(FILE_RENAME_MAPPING)

    # Process directories
    for old_name, new_name in RENAME_MAPPING.items():
        old_path = Path(os.path.join(str(ROOT_DIR), old_name))
        new_path = Path(os.path.join(str(ROOT_DIR), new_name))

        if old_path.exists() and old_path != new_path:
            logging.info(f"Processing directory: {old_name} -> {new_name}")

            if rename_directory(old_path, new_path):
                dir_success_count += 1
                # Update import statements and references
                update_references(old_name.replace("/", "."), new_name.replace("/", "."))

    # Process files
    for old_name, new_name in FILE_RENAME_MAPPING.items():
        old_path = Path(os.path.join(str(ROOT_DIR), old_name))
        new_path = Path(os.path.join(str(ROOT_DIR), new_name))

        if old_path.exists() and old_path != new_path:
            logging.info(f"Processing file: {old_name} -> {new_name}")

            if rename_file(old_path, new_path):
                file_success_count += 1
                # Update references to the file
                update_file_references(old_path, new_path)

    # Generate report
    logging.info("=== Directory and File Renaming Complete ===")
    logging.info(f"Successfully renamed {dir_success_count} of {dir_total_count} directories")
    logging.info(f"Successfully renamed {file_success_count} of {file_total_count} files")

    if dir_success_count < dir_total_count or file_success_count < file_total_count:
        logging.warning("Some items could not be renamed. Check the log for details.")

    # Create a report file
    report_path = Path(os.path.join(str(ROOT_DIR), "docs", "reports", "rename_report.md"))
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Directory and File Renaming Report\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Directory Changes\n\n")
        for old_name, new_name in RENAME_MAPPING.items():
            old_path = Path(os.path.join(str(ROOT_DIR), old_name))
            new_path = Path(os.path.join(str(ROOT_DIR), new_name))
            status = "✓" if new_path.exists() else "✗"
            f.write(f"- [{status}] {old_name} → {new_name}\n")

        f.write(
            f"\nTotal: {dir_success_count}/{dir_total_count} directories renamed successfully\n\n"
        )

        f.write("## File Changes\n\n")
        for old_name, new_name in FILE_RENAME_MAPPING.items():
            old_path = Path(os.path.join(str(ROOT_DIR), old_name))
            new_path = Path(os.path.join(str(ROOT_DIR), new_name))
            status = "✓" if new_path.exists() else "✗"
            f.write(f"- [{status}] {old_name} → {new_name}\n")

        f.write(f"\nTotal: {file_success_count}/{file_total_count} files renamed successfully\n")

    logging.info(f"Report generated at {report_path}")


if __name__ == "__main__":
    main()
