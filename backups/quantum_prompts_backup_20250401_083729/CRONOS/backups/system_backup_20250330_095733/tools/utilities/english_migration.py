#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
English Migration - Optimized batch script to standardize project to English
This script efficiently renames files and directories from Portuguese to English in a single pass.

Version: 1.0.0
Date: 2025-03-20
"""

import os
import sys
import shutil
import logging
import time
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("english_migration.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Root directory of the project
ROOT_DIR = Path().resolve()

# Create timestamp for backups
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT_DIR / "backup" / "english_migration" / TIMESTAMP

# Directories to ignore when updating references
IGNORE_DIRS = [".git", "venv", "__pycache__", "backup", "quarantine", "eliza", "node_modules"]

# Comprehensive mapping of files and directories to rename
RENAME_MAPPING = {
    # Directories
    "docs/arquivados": "docs/archived",
    # Portuguese documentation files
    "docs/TRANSIÇÃO_COMPLETA.md": "docs/COMPLETE_TRANSITION.md",
    "docs/RESUMO_UNIFICAÇÃO.md": "docs/UNIFICATION_SUMMARY.md",
    "docs/PRINCÍPIOS_TROCAS_JUSTAS.md": "docs/FAIR_EXCHANGE_PRINCIPLES.md",
    "docs/principios_fundamentais.md": "docs/fundamental_principles.md",
    "docs/navegador_etico.md": "docs/ethical_navigator.md",
    "docs/musico_quantico.md": "docs/quantum_musician.md",
    "docs/IMPLEMENTANDO_TROCAS_JUSTAS.md": "docs/IMPLEMENTING_FAIR_EXCHANGE.md",
    "docs/GUIA_INSTALACAO_V7.4.md": "docs/INSTALLATION_GUIDE_V7.4.md",
    "docs/GUIA_INSTALACAO.md": "docs/INSTALLATION_GUIDE.md",
    "docs/GUIA_IMPLEMENTACAO.md": "docs/IMPLEMENTATION_GUIDE.md",
    "docs/guardiaoConhecimento.md": "docs/knowledge_guardian.md",
    "docs/gamer_quantico.md": "docs/quantum_gamer.md",
    "docs/filosofo_quantico.md": "docs/quantum_philosopher.md",
    "docs/etica_quantum.md": "docs/quantum_ethics.md",
    "docs/ESTRUTURA_SISTEMA.md": "docs/SYSTEM_STRUCTURE.md",
    "docs/economista_quantico.md": "docs/quantum_economist.md",
    "docs/DOCUMENTACAO_CONHECIMENTO_QUANTICO.md": "docs/QUANTUM_KNOWLEDGE_DOCUMENTATION.md",
    "docs/cientista_integrador.md": "docs/integration_scientist.md",
    "docs/artista_quantico.md": "docs/quantum_artist.md",
    "docs/TROCAS_JUSTAS_PROMPTS.md": "docs/FAIR_EXCHANGE_PROMPTS.md",
    "docs/archived/README_SIMPLIFICAÇÃO.md": "docs/archived/README_SIMPLIFICATION.md",
}


def create_backup():
    """Create a backup of all files that will be renamed"""
    logging.info(f"Creating backup in {BACKUP_DIR}")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Back up each file that will be renamed
    for old_path in RENAME_MAPPING.keys():
        old_path = ROOT_DIR / old_path
        if old_path.exists():
            rel_path = old_path.relative_to(ROOT_DIR)
            backup_path = BACKUP_DIR / rel_path

            # Create parent directories
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            if old_path.is_dir():
                shutil.copytree(old_path, backup_path)
                logging.info(f"Backed up directory: {rel_path}")
            else:
                shutil.copy2(old_path, backup_path)
                logging.info(f"Backed up file: {rel_path}")

    logging.info(f"Backup completed at {BACKUP_DIR}")


def update_references_batch(rename_map):
    """
    Update references to renamed files and directories in all relevant files

    Args:
        rename_map: Dictionary mapping old paths to new paths
    """
    logging.info("Updating references in batch mode...")

    # Collect all files that need to be processed
    python_files = []
    markdown_files = []

    for file_path in ROOT_DIR.rglob("*"):
        # Skip files in ignored directories
        if any(ignore in str(file_path) for ignore in IGNORE_DIRS):
            continue

        if file_path.suffix == ".py":
            python_files.append(file_path)
        elif file_path.suffix == ".md":
            markdown_files.append(file_path)

    # Process Python files (import statements and strings)
    for py_file in python_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            modified = False

            for old_path, new_path in rename_map.items():
                # Convert to Path objects
                old = Path(old_path)
                new = Path(new_path)

                # Replace full paths
                content = content.replace(str(old), str(new))

                # Replace directory/module names in imports
                if old.is_dir() or old.suffix == ".py":
                    old_module = str(old).replace("/", ".").replace("\\", ".")
                    if old.suffix == ".py":
                        old_module = old_module[:-3]  # Remove .
                    new_module = str(new).replace("/", ".").replace("\\", ".")
                    if new.suffix == ".py":
                        new_module = new_module[:-3]  # Remove .py

                    content = content.replace(f"import {old_module}", f"import {new_module}")
                    content = content.replace(f"from {old_module}", f"from {new_module}")

            if content != original_content:
                with open(py_file, "w", encoding="utf-8") as f:
                    f.write(content)
                logging.info(f"Updated references in {py_file}")
                modified = True

        except Exception as e:
            logging.error(f"Error updating references in {py_file}: {str(e)}")

    # Process Markdown files (links and text)
    for md_file in markdown_files:
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            modified = False

            for old_path, new_path in rename_map.items():
                # Replace markdown links [text](path)
                old_name = Path(old_path).name
                new_name = Path(new_path).name

                # Replace full paths in links
                content = content.replace(f"]({old_path})", f"]({new_path})")
                content = content.replace(f"](./{old_path})", f"](./{new_path})")

                # Replace just the filenames in links
                content = content.replace(f"]({old_name})", f"]({new_name})")

                # Replace mentions of filenames in text
                content = content.replace(f" {old_name} ", f" {new_name} ")
                content = content.replace(f"`{old_name}`", f"`{new_name}`")

            if content != original_content:
                with open(md_file, "w", encoding="utf-8") as f:
                    f.write(content)
                logging.info(f"Updated references in {md_file}")
                modified = True

        except Exception as e:
            logging.error(f"Error updating references in {md_file}: {str(e)}")

    logging.info("Batch reference update completed")


def rename_all_items():
    """Rename all files and directories in a single pass"""
    logging.info("Starting batch renaming process...")

    # Track success and failures
    success_count = 0
    failed_items = []

    # Organize items by type and depth for proper processing order
    dirs_to_rename = {}
    files_to_rename = {}

    for old_path, new_path in RENAME_MAPPING.items():
        old_full = ROOT_DIR / old_path
        if old_full.exists():
            if old_full.is_dir():
                depth = len(Path(old_path).parts)
                if depth not in dirs_to_rename:
                    dirs_to_rename[depth] = []
                dirs_to_rename[depth].append((old_path, new_path))
            else:
                files_to_rename[old_path] = new_path

    # First rename files (to avoid path conflicts)
    for old_path, new_path in files_to_rename.items():
        old_full = ROOT_DIR / old_path
        new_full = ROOT_DIR / new_path

        try:
            # Create parent directory if it doesn't exist
            new_full.parent.mkdir(parents=True, exist_ok=True)

            # Rename the file
            old_full.rename(new_full)
            logging.info(f"Successfully renamed {old_path} to {new_path}")
            success_count += 1

        except Exception as e:
            logging.error(f"Failed to rename {old_path}: {str(e)}")
            failed_items.append((old_path, str(e)))

    # Then rename directories (starting from deepest)
    sorted_depths = sorted(dirs_to_rename.keys(), reverse=True)
    for depth in sorted_depths:
        for old_path, new_path in dirs_to_rename[depth]:
            old_full = ROOT_DIR / old_path
            new_full = ROOT_DIR / new_path

            try:
                # Only rename if old directory exists and new doesn't
                if old_full.exists() and not new_full.exists():
                    # Create parent directory if it doesn't exist
                    new_full.parent.mkdir(parents=True, exist_ok=True)

                    # Rename the directory
                    old_full.rename(new_full)
                    logging.info(f"Successfully renamed {old_path} to {new_path}")
                    success_count += 1
                elif new_full.exists():
                    logging.warning(f"Target directory already exists: {new_path}")
                    failed_items.append((old_path, "Target already exists"))
                else:
                    logging.warning(f"Source directory not found: {old_path}")
                    failed_items.append((old_path, "Source not found"))

            except Exception as e:
                logging.error(f"Failed to rename {old_path}: {str(e)}")
                failed_items.append((old_path, str(e)))

    # Report results
    logging.info(f"Rename process completed: {success_count} items renamed successfully")
    if failed_items:
        logging.warning(f"{len(failed_items)} items could not be renamed:")
        for item, reason in failed_items:
            logging.warning(f"  - {item}: {reason}")

    return success_count, failed_items


def generate_report(success_count, failed_items):
    """Generate a report of the English migration process"""
    report_dir = ROOT_DIR / "docs" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"english_migration_report_{TIMESTAMP}.md"

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# English Migration Report\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Total items processed**: {len(RENAME_MAPPING)}\n")
            f.write(f"- **Successfully renamed**: {success_count}\n")
            f.write(f"- **Failed**: {len(failed_items)}\n")
            f.write(f"- **Backup location**: `{BACKUP_DIR}`\n\n")

            if failed_items:
                f.write("## Failed Items\n\n")
                for item, reason in failed_items:
                    f.write(f"- `{item}`: {reason}\n")
                f.write("\n")

            f.write("## Next Steps\n\n")
            f.write("1. Verify that all renamed items are working correctly\n")
            f.write("2. Update any references that might have been missed\n")
            f.write("3. Consider manual renaming for any failed items\n")
            f.write("4. Update READMEs and documentation to reflect changes\n\n")

            f.write("---\n\n")
            f.write("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

        logging.info(f"Report generated at {report_path}")
        return report_path

    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        return None


def main():
    """Main execution function"""
    start_time = time.time()
    logging.info("=== STARTING ENGLISH MIGRATION PROCESS ===")

    try:
        # Step 1: Create backup
        create_backup()

        # Step 2: Rename all files and directories
        success_count, failed_items = rename_all_items()

        # Step 3: Update references in batch mode
        update_references_batch(RENAME_MAPPING)

        # Step 4: Generate report
        report_path = generate_report(success_count, failed_items)

        # Calculate execution time
        execution_time = time.time() - start_time
        logging.info(f"=== ENGLISH MIGRATION COMPLETED IN {execution_time:.2f} SECONDS ===")
        if report_path:
            logging.info(f"Report available at: {report_path}")

    except Exception as e:
        logging.error(f"Error during English migration: {str(e)}")
        logging.info("=== ENGLISH MIGRATION PROCESS FAILED ===")


if __name__ == "__main__":
    main()
