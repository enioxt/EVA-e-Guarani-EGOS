#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reorganize Workspace - Script to reorganize the directory structure of EVA & GUARANI
This script will organize all folders in the project root according to the modular structure.

Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("data/logs/system/system_reorganization.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("EVA_GUARANI.REORGANIZE")

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Current date and time for directory names
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Main structure directories
CORE_DIRS = ["core", "modules", "integrations", "tools", "docs", "tests", "ui", "data"]
GIT_DIRS = [".git", ".github", ".vscode", ".obsidian", ".bolt", ".cursor"]

# Folder mapping to move
MOVE_MAPPING = {
    # Move to core/
    "config": "core/config",
    "EGOS": "core/egos",
    "ethics": "core/ethik",
    # Move to modules/
    "quantum": "modules/quantum",
    "eliza": "modules/eliza",
    "eliza_os": "modules/eliza/os",
    "blockchain": "modules/blockchain",
    "gamification": "modules/gamification",
    # Move to integrations/
    "bot": "integrations/bots",
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
}

# Folder to organize backups
BACKUPS_DIR = ROOT_DIR / "backup" / "consolidated"
BACKUPS_TO_MOVE = [
    "backup_20250301_171540",
    "backup_before_reorganization",
    "backup_pre_reorganization_20250319",
    "backup_quantum",
    "backups",
    "essential_backup_20250228_164242",
    "shared_egos_20250301_163205",
    "arquivos_antigos_20250301_171050",
]

# Folder to organize quarantines
QUARANTINE_DIR = ROOT_DIR / "quarantine" / "consolidated"

# Special files that must remain in the root
ROOT_FILES = ["README.md", "system_integrity_check.log", "quarantine_folders_log.txt"]


def setup_dirs():
    """Sets up the necessary directories for reorganization"""
    logger.info("Setting up directories for reorganization...")

    # Create consolidated backup folder
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Consolidated backup directory created: {BACKUPS_DIR}")

    # Create consolidated quarantine folder
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Consolidated quarantine directory created: {QUARANTINE_DIR}")


def move_directories():
    """Moves directories to the correct structure"""
    logger.info("Moving directories to the modular structure...")

    moved_count = 0

    for source, destination in MOVE_MAPPING.items():
        source_path = ROOT_DIR / source
        dest_path = ROOT_DIR / destination

        # Check if the source directory exists
        if not source_path.exists() or not source_path.is_dir():
            logger.warning(f"Source directory not found: {source}")
            continue

        # Check if the destination directory already contains files
        if dest_path.exists():
            # If the destination exists and has content, merge
            logger.info(f"Merging {source} with existing directory {destination}")

            try:
                # Copy all files, merging with the destination
                for item in source_path.glob("*"):
                    if item.is_dir():
                        # For subdirectories, use copytree with dirs_exist_ok option
                        if (dest_path / item.name).exists():
                            logger.info(f"Merging subdirectory {item.name} into {destination}")
                            # Move files individually to merge
                            for subitem in item.glob("*"):
                                target = dest_path / item.name / subitem.name
                                if not target.exists():
                                    try:
                                        if subitem.is_dir():
                                            shutil.copytree(subitem, target)
                                        else:
                                            shutil.copy2(subitem, target)
                                    except Exception as e:
                                        logger.error(
                                            f"Error merging {subitem} into {target}: {str(e)}"
                                        )
                        else:
                            # Subdirectory does not exist in the destination, copy directly
                            try:
                                shutil.copytree(item, dest_path / item.name)
                            except Exception as e:
                                logger.error(
                                    f"Error copying directory {item} to {dest_path}: {str(e)}"
                                )
                    else:
                        # For files, just copy if it doesn't exist
                        target = dest_path / item.name
                        if not target.exists():
                            try:
                                shutil.copy2(item, target)
                            except Exception as e:
                                logger.error(f"Error copying file {item} to {target}: {str(e)}")

                # After copying, move the original directory to quarantine
                quarantine_path = QUARANTINE_DIR / f"{source}_{TIMESTAMP}"
                shutil.move(source_path, quarantine_path)
                logger.info(f"Original directory {source} moved to quarantine: {quarantine_path}")
                moved_count += 1

            except Exception as e:
                logger.error(f"Error merging {source} with {destination}: {str(e)}")
        else:
            # If the destination does not exist, create and move directly
            logger.info(f"Moving {source} to {destination}")

            try:
                # Create destination directory
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Move directory
                shutil.move(str(source_path), str(dest_path))
                logger.info(f"Directory {source} moved to {destination}")
                moved_count += 1

            except Exception as e:
                logger.error(f"Error moving {source} to {destination}: {str(e)}")

    logger.info(f"Completed: {moved_count} directories were moved to the modular structure")


def organize_backups():
    """Organizes backup folders in a centralized location"""
    logger.info("Organizing backup folders...")

    moved_count = 0

    for backup_dir in BACKUPS_TO_MOVE:
        source_path = ROOT_DIR / backup_dir

        if not source_path.exists() or not source_path.is_dir():
            logger.warning(f"Backup directory not found: {backup_dir}")
            continue

        # Create specific folder for each backup
        dest_path = BACKUPS_DIR / backup_dir
        dest_path.mkdir(parents=True, exist_ok=True)

        try:
            logger.info(f"Moving backup {backup_dir} to consolidated area")

            # Move backup content
            for item in source_path.glob("*"):
                target = dest_path / item.name
                if item.is_dir():
                    shutil.copytree(item, target, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, target)

            # Remove original directory after copying
            shutil.rmtree(source_path)

            logger.info(f"Backup {backup_dir} organized successfully")
            moved_count += 1

        except Exception as e:
            logger.error(f"Error organizing backup {backup_dir}: {str(e)}")

    logger.info(f"Completed: {moved_count} backup directories were organized")


def organize_quarantine():
    """Organizes quarantine folders"""
    logger.info("Organizing quarantine folders...")

    quarantine_dirs = [
        "quarentena_20250319",
        "quarentena_duplicados_20250319",
        "quarentena_pastas_20250319",
        "quarantine",
    ]

    for qdir in quarantine_dirs:
        source_path = ROOT_DIR / qdir

        if not source_path.exists() or not source_path.is_dir():
            logger.warning(f"Quarantine directory not found: {qdir}")
            continue

        # If it's the main quarantine directory, just ensure it exists
        if qdir == "quarentena":
            logger.info(f"Main quarantine directory already exists: {qdir}")
            continue

        # For other quarantine directories, move inside the quarantine structure
        dest_path = ROOT_DIR / "quarentena" / qdir

        try:
            if not dest_path.exists():
                # If the destination does not exist, move directly
                logger.info(f"Moving {qdir} to quarantine structure")
                shutil.move(source_path, dest_path)
            else:
                # If the destination already exists, rename to avoid conflicts
                new_dest = ROOT_DIR / "quarentena" / f"{qdir}_{TIMESTAMP}"
                logger.info(f"Destination already exists, moving {qdir} to {new_dest}")
                shutil.move(source_path, new_dest)

            logger.info(f"Quarantine directory {qdir} organized successfully")

        except Exception as e:
            logger.error(f"Error organizing quarantine {qdir}: {str(e)}")


def cleanup_empty_dirs():
    """Removes empty directories in the root"""
    logger.info("Removing empty directories in the root...")

    protected_dirs = CORE_DIRS + GIT_DIRS + ["quarentena", "backup", "venv"]

    for item in ROOT_DIR.glob("*"):
        if not item.is_dir():
            continue

        if item.name in protected_dirs:
            logger.debug(f"Ignoring protected directory: {item.name}")
            continue

        # Check if the directory is empty
        if not any(item.iterdir()):
            try:
                logger.info(f"Removing empty directory: {item.name}")
                item.rmdir()
            except Exception as e:
                logger.error(f"Error removing empty directory {item.name}: {str(e)}")


def create_root_readme():
    """Updates the README.md in the root with information about the new structure"""
    readme_path = ROOT_DIR / "README.md"

    if not readme_path.exists():
        logger.info("Creating README.md in the root...")

        readme_content = """# EVA & GUARANI

## Integrated Consciousness System

**Version:** 8.0.0
**Date:** 20/03/2025

---

## 🌌 System Structure

The EVA & GUARANI system is organized in a modular structure, with the following main components:

### Main Components

- **core/**: System core
  - **egos/**: Main execution system
  - **atlas/**: Systemic Mapping
  - **nexus/**: Modular Analysis
  - **cronos/**: Evolutionary Preservation
  - **ethik/**: Integrated Ethics
  - **config/**: System configurations

- **modules/**: Functional modules
  - **quantum/**: Quantum processing
  - **eliza/**: Natural language processing
  - **blockchain/**: Blockchain integration
  - **gamification/**: Gamification system

- **integrations/**: External system integrations
  - **bots/**: Bots and assistants
  - **prompts/**: Prompt templates
  - **extensions/**: Functionality extensions

- **tools/**: Support tools
  - **utilities/**: Various utilities
  - **analysis/**: Analysis tools
  - **utils/**: Auxiliary functions

- **data/**: Data repository
  - **personas/**: Persona definitions
  - **logs/**: Activity logs
  - **examples/**: Usage examples

- **docs/**: Documentation
  - **reports/**: Generated reports

- **tests/**: Automated tests

- **ui/**: User interface

### Service Areas

- **backup/**: Backup area
- **quarentena/**: Quarantine area for old files

---

## 🧬 Integrated Subsystems

mermaid
graph TD
    EVA[EVA & GUARANI] --> ATLAS[ATLAS: Systemic Mapping]
    EVA --> NEXUS[NEXUS: Modular Analysis]
    EVA --> CRONOS[CRONOS: Evolutionary Preservation]
    EVA --> ETHIK[ETHIK: Integrated Ethics]

    ATLAS --> Map[Map Connections]
    ATLAS --> Visualize[Visualize Systems]
    ATLAS --> Prompt[Transform into Prompts]

    NEXUS --> Analyze[Analyze Modules]
    NEXUS --> Connect[Connect Components]
    NEXUS --> Document[Document Processes]

    CRONOS --> Backup[Quantum Backup]
    CRONOS --> Version[Versioning]
    CRONOS --> Preserve[Structural Preservation]

    ETHIK --> Evaluate[Evaluate Ethics]
    ETHIK --> Guide[Guide Decisions]
    ETHIK --> Align[Maintain Alignment]


---

## 📚 Documentation

For more information about each component, refer to the specific documentation:

- [Core Documentation](./docs/core.md)
- [Modules Documentation](./docs/modules.md)
- [Integrations Guide](./docs/integrations.md)
- [Tools Manual](./docs/tools.md)

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""

        try:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content)

            logger.info("README.md updated successfully")
        except Exception as e:
            logger.error(f"Error updating README.md: {str(e)}")


def generate_report():
    """Generates a reorganization report"""
    report_dir = ROOT_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"reorganization_report_{TIMESTAMP}.md"
    logger.info(f"Generating reorganization report: {report_path}")

    # Count directories in each main category
    structure_stats = {}
    for category in CORE_DIRS:
        category_path = ROOT_DIR / category
        if category_path.exists():
            subdirs = [d for d in category_path.glob("*") if d.is_dir()]
            structure_stats[category] = len(subdirs)

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# Reorganization Report - EVA & GUARANI\n\n")
            f.write(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

            f.write("## Current System Structure\n\n")

            for category, count in structure_stats.items():
                f.write(f"- **{category}**: {count} subdirectories\n")

            f.write("\n## Moved Directories\n\n")

            for source, destination in MOVE_MAPPING.items():
                source_path = ROOT_DIR / source
                if not source_path.exists():
                    f.write(f"- ✅ `{source}` → `{destination}`\n")

            f.write("\n## Organized Backups\n\n")

            for backup in BACKUPS_TO_MOVE:
                source_path = ROOT_DIR / backup
                if not source_path.exists():
                    f.write(f"- ✅ `{backup}` organized in `backup/consolidated/{backup}`\n")

            f.write("\n## Organized Quarantines\n\n")

            quarantine_dirs = [
                "quarentena_20250319",
                "quarentena_duplicados_20250319",
                "quarentena_pastas_20250319",
                "quarantine",
            ]
            for qdir in quarantine_dirs:
                source_path = ROOT_DIR / qdir
                if not source_path.exists():
                    f.write(f"- ✅ `{qdir}` organized in `quarentena/{qdir}`\n")

            f.write("\n---\n\n")
            f.write("Report generated by the reorganization subsystem - EVA & GUARANI\n")

        logger.info(f"Reorganization report generated successfully: {report_path}")
    except Exception as e:
        logger.error(f"Error generating reorganization report: {str(e)}")


def main():
    """Main execution function"""
    logger.info("=== STARTING DIRECTORY STRUCTURE REORGANIZATION ===")

    try:
        # Set up necessary directories
        setup_dirs()

        # Move directories to the correct structure
        move_directories()

        # Organize backups
        organize_backups()

        # Organize quarantines
        organize_quarantine()

        # Remove empty directories
        cleanup_empty_dirs()

        # Update README.md
        create_root_readme()

        # Generate report
        generate_report()

        logger.info("=== REORGANIZATION SUCCESSFULLY COMPLETED ===")

    except Exception as e:
        logger.error(f"Error during reorganization: {str(e)}")
        logger.info("=== REORGANIZATION COMPLETED WITH ERRORS ===")


if __name__ == "__main__":
    main()
