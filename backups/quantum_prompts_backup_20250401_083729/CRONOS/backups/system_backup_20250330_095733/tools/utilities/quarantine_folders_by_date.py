#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to quarantine folders that have not been modified since a specific date.

Author: EVA & GUARANI
Date: 19/03/2025
Version: 1.0
"""

import os
import shutil
import datetime
import argparse
import json
import logging
import time
from pathlib import Path
import sys
from typing import Dict, List, Tuple, Optional, Any, Set

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("quarantine_folders_log.txt"), logging.StreamHandler()],
)
logger = logging.getLogger("QuarantineFolders")

# Directories that should NEVER be quarantined
CRITICAL_FOLDERS = {
    ".git",
    "core",
    "modules",
    "integrations",
    "tools",
    "docs",
    "tests",
    "ui",
    "data",
    "quarantine",
    "quarantine",
    "quarantine_20250319",
    "quarantine_duplicates_20250319",
    "reports",
    "backup_before_reorganization",
    "backup_pre_reorganization_20250319",
    ".cursor",  # Editor
    ".vscode",  # Editor
    ".obsidian",  # Editor
}

# Directories that should be moved to the new structure and not quarantined
MOVE_TO_NEW_STRUCTURE = {
    "bot": "integrations/bots",
    "EGOS": "core/egos",
    "ethics": "core/ethik",
    "quantum": "modules/quantum",
    "QUANTUM_PROMPTS": "modules/quantum/prompts",
    "system_analysis": "modules/analysis",
    "config": "core/config",
    "utils": "tools/utilities",
    "logs": "data/logs",
    "personas": "data/personas",
    "examples": "data/examples",
}


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Move outdated folders to quarantine.")
    parser.add_argument(
        "--date_limit",
        type=str,
        default="2025-03-02",
        help="Date limit in YYYY-MM-DD format. Folders not modified after this date will be moved to quarantine.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["simulation", "execution"],
        default="simulation",
        help="Operation mode: 'simulation' only shows what would be done; 'execution' performs the movements.",
    )
    parser.add_argument(
        "--quarantine_dir",
        type=str,
        default="./quarantine_folders_20250319",
        help="Quarantine directory where folders will be moved.",
    )
    parser.add_argument(
        "--report",
        type=str,
        default="./reports/quarantine_folders_report.json",
        help="Path to save the JSON report.",
    )
    parser.add_argument(
        "--report_md",
        type=str,
        default="./reports/quarantine_folders_report.md",
        help="Path to save the Markdown report.",
    )
    return parser.parse_args()


def is_folder_modified_after_date(folder_path: str, date_limit: datetime.datetime) -> bool:
    """Check if the folder was modified after the date limit."""
    try:
        modification_time = os.path.getmtime(folder_path)
        modification_date = datetime.datetime.fromtimestamp(modification_time)
        return modification_date > date_limit
    except Exception as e:
        logger.error(f"Error checking modification date of folder {folder_path}: {e}")
        return True  # For safety, consider it was modified recently


def create_quarantine_directory(quarantine_dir: str) -> bool:
    """Create the quarantine directory if it does not exist."""
    try:
        if not os.path.exists(quarantine_dir):
            os.makedirs(quarantine_dir)
            logger.info(f"Quarantine directory created: {quarantine_dir}")
        return True
    except Exception as e:
        logger.error(f"Error creating quarantine directory {quarantine_dir}: {e}")
        return False


def move_folder_to_quarantine(folder_path: str, quarantine_dir: str) -> bool:
    """Move the folder to the quarantine directory."""
    try:
        folder_name = os.path.basename(folder_path)
        destination = os.path.join(quarantine_dir, folder_name)

        # If the destination already exists, add a timestamp
        if os.path.exists(destination):
            timestamp = int(time.time())
            destination = f"{destination}_{timestamp}"

        shutil.move(folder_path, destination)
        logger.info(f"Folder moved to quarantine: {folder_path} -> {destination}")
        return True
    except Exception as e:
        logger.error(f"Error moving folder {folder_path} to quarantine: {e}")
        return False


def move_folder_to_new_structure(folder_path: str, destination_path: str) -> bool:
    """Move the folder to the new directory structure."""
    try:
        source = Path(folder_path)
        destination = Path(destination_path)

        # Create destination directory if it does not exist
        destination.parent.mkdir(parents=True, exist_ok=True)

        # If the destination exists, we merge the content
        if destination.exists():
            # Transfer files and folders to the destination
            for item in source.glob("*"):
                if item.is_file():
                    dest_file = destination / item.name
                    if dest_file.exists():
                        # If it already exists, add a timestamp to avoid loss
                        timestamp = int(time.time())
                        shutil.copy2(item, destination / f"{item.name}_{timestamp}")
                    else:
                        shutil.copy2(item, destination / item.name)
                elif item.is_dir():
                    merge_dir = destination / item.name
                    merge_dir.mkdir(parents=True, exist_ok=True)
                    for subitem in item.glob("**/*"):
                        if subitem.is_file():
                            rel_path = subitem.relative_to(item)
                            dest_subfile = merge_dir / rel_path
                            dest_subfile.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(subitem, dest_subfile)

            # We do not delete the original folder, we leave it for quarantine
            logger.info(f"Folder content merged: {folder_path} -> {destination_path}")
        else:
            # If it does not exist, we just move it
            shutil.copytree(source, destination)
            logger.info(f"Folder copied to the new structure: {folder_path} -> {destination_path}")

        return True
    except Exception as e:
        logger.error(f"Error moving folder {folder_path} to new structure: {e}")
        return False


def should_quarantine_folder(folder_path: str) -> bool:
    """Check if the folder should be quarantined based on specific criteria."""
    folder_name = os.path.basename(folder_path)

    # Critical folders that should never be quarantined
    if folder_name in CRITICAL_FOLDERS:
        return False

    # System or hidden directories (starting with a dot, except critical ones)
    if folder_name.startswith(".") and folder_name not in CRITICAL_FOLDERS:
        return False

    # Backup, quarantine, or date-named folders
    if any(
        keyword in folder_name.lower() for keyword in ["backup", "quarent", "20250", "essential"]
    ):
        return False

    return True


def generate_report(results: Dict, args: argparse.Namespace) -> None:
    """Generate reports in JSON and Markdown format."""
    # Ensure the report directory exists
    os.makedirs(os.path.dirname(args.report), exist_ok=True)

    # Save JSON report
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    # Save Markdown report
    with open(args.report_md, "w", encoding="utf-8") as f:
        f.write("# Folder Quarantine Report\n\n")
        f.write(f"*Date: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}*\n\n")
        f.write(f"## Operation Mode: {args.mode.upper()}\n\n")
        f.write(f"## Date Limit: {args.date_limit}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Total folders analyzed: {results['total_folders']}\n")
        f.write(f"- Folders moved to quarantine: {results['quarantined_count']}\n")
        f.write(f"- Folders moved to new structure: {results['moved_to_structure_count']}\n")
        f.write(f"- Folders preserved: {results['preserved_count']}\n")
        f.write(f"- Errors encountered: {results['errors_count']}\n\n")

        f.write("## Folders Moved to Quarantine\n\n")
        if results["quarantined"]:
            for folder in results["quarantined"]:
                f.write(f"- `{folder}`\n")
        else:
            f.write("*No folder was moved to quarantine.*\n")
        f.write("\n")

        f.write("## Folders Moved to New Structure\n\n")
        if results["moved_to_structure"]:
            for src, dest in results["moved_to_structure"].items():
                f.write(f"- `{src}` → `{dest}`\n")
        else:
            f.write("*No folder was moved to the new structure.*\n")
        f.write("\n")

        f.write("## Folders Preserved\n\n")
        if results["preserved"]:
            for folder in results["preserved"]:
                f.write(f"- `{folder}`\n")
        else:
            f.write("*No folder was preserved.*\n")
        f.write("\n")

        f.write("## Errors\n\n")
        if results["errors"]:
            for error in results["errors"]:
                f.write(f"- **{error['folder']}**: {error['message']}\n")
        else:
            f.write("*No errors were found during the process.*\n")
        f.write("\n")

        f.write("## Recommended Next Steps\n\n")
        f.write("1. Verify the integrity of folders in the new structure\n")
        f.write("2. Update references in code files to the new paths\n")
        f.write("3. Validate that the main functionalities remain operational\n")
        f.write("4. Consider deleting the quarantine after an observation period\n\n")

        f.write("---\n\n")
        f.write("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

    logger.info(f"Reports generated: {args.report} and {args.report_md}")


def main() -> None:
    """Main function of the script."""
    args = parse_arguments()

    # Additional logging configuration to avoid output overlap
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.handlers = [logging.FileHandler("quarantine_folders_log.txt"), console_handler]

    # Convert date limit to datetime object
    try:
        date_limit = datetime.datetime.strptime(args.date_limit, "%Y-%m-%d")
    except ValueError:
        logger.error(f"Invalid date format. Use YYYY-MM-DD. Received: {args.date_limit}")
        sys.exit(1)

    logger.info(f"Starting folder quarantine process in mode: {args.mode}")
    logger.info(f"Date limit: {args.date_limit}")

    # Create quarantine directory
    if args.mode == "execution":
        if not create_quarantine_directory(args.quarantine_dir):
            logger.error("Failed to create quarantine directory. Aborting.")
            sys.exit(1)

    # Results
    results = {
        "total_folders": 0,
        "quarantined": [],
        "moved_to_structure": {},
        "preserved": [],
        "errors": [],
        "quarantined_count": 0,
        "moved_to_structure_count": 0,
        "preserved_count": 0,
        "errors_count": 0,
        "execution_time": "",
        "mode": args.mode,
        "date_limit": args.date_limit,
    }

    start_time = time.time()

    # List all folders in the current directory (project root)
    try:
        all_folders = [f for f in os.listdir(".") if os.path.isdir(f)]
        results["total_folders"] = len(all_folders)

        for folder in all_folders:
            # Check if the folder should be moved to the new structure
            if folder in MOVE_TO_NEW_STRUCTURE:
                dest_path = MOVE_TO_NEW_STRUCTURE[folder]
                logger.info(f"Folder will be moved to new structure: {folder} -> {dest_path}")

                if args.mode == "execution":
                    if move_folder_to_new_structure(folder, dest_path):
                        results["moved_to_structure"][folder] = dest_path
                        results["moved_to_structure_count"] += 1
                    else:
                        results["errors"].append(
                            {
                                "folder": folder,
                                "message": f"Failed to move to new structure: {dest_path}",
                            }
                        )
                        results["errors_count"] += 1
                else:
                    # In simulation mode, just record
                    results["moved_to_structure"][folder] = dest_path
                    results["moved_to_structure_count"] += 1

            # Check if the folder should be quarantined
            elif should_quarantine_folder(folder):
                # Check if the folder was modified after the date limit
                if not is_folder_modified_after_date(folder, date_limit):
                    logger.info(f"Outdated folder: {folder}")

                    if args.mode == "execution":
                        if move_folder_to_quarantine(folder, args.quarantine_dir):
                            results["quarantined"].append(folder)
                            results["quarantined_count"] += 1
                        else:
                            results["errors"].append(
                                {"folder": folder, "message": "Failed to move to quarantine"}
                            )
                            results["errors_count"] += 1
                    else:
                        # In simulation mode, just record
                        results["quarantined"].append(folder)
                        results["quarantined_count"] += 1
                else:
                    logger.info(f"Updated folder (preserved): {folder}")
                    results["preserved"].append(folder)
                    results["preserved_count"] += 1
            else:
                logger.info(f"Critical or special folder (preserved): {folder}")
                results["preserved"].append(folder)
                results["preserved_count"] += 1

    except Exception as e:
        logger.error(f"Error processing folders: {e}")
        sys.exit(1)

    # Record execution time
    end_time = time.time()
    execution_time = end_time - start_time
    results["execution_time"] = f"{execution_time:.2f} seconds"

    # Generate reports
    generate_report(results, args)

    # Final message
    logger.info(f"Process completed in {results['execution_time']}")
    logger.info(f"Total folders: {results['total_folders']}")
    logger.info(f"Folders quarantined: {results['quarantined_count']}")
    logger.info(f"Folders moved to new structure: {results['moved_to_structure_count']}")
    logger.info(f"Folders preserved: {results['preserved_count']}")
    logger.info(f"Errors: {results['errors_count']}")

    print("\n✧༺❀༻∞ Process completed with love and consciousness ∞༺❀༻✧")


if __name__ == "__main__":
    main()
