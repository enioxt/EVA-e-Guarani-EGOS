#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to verify the integrity of the EVA & GUARANI system after reorganization.

Author: EVA & GUARANI
Date: 19/03/2025
Version: 1.0
"""

import os
import json
import argparse
import logging
import time
from pathlib import Path
import sys
from typing import Dict, List, Set, Tuple, Any

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("system_integrity_check.log"), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("SystemIntegrityCheck")

# Main categories that must exist
MAIN_CATEGORIES = ["core", "modules", "integrations", "tools", "docs", "tests", "ui", "data"]

# Critical subcategories that must exist
CRITICAL_SUBCATEGORIES = {
    "core": ["egos", "ethik", "config"],
    "modules": ["quantum", "analysis"],
    "integrations": ["bots"],
    "tools": ["utilities"],
    "data": ["logs", "personas", "examples"],
    "docs": [],
}

# Folders that were moved to the new structure
MOVED_FOLDERS = {
    "bot": "integrations/bots",
    "config": "core/config",
    "EGOS": "core/egos",
    "ethics": "core/ethik",
    "examples": "data/examples",
    "logs": "data/logs",
    "personas": "data/personas",
    "quantum": "modules/quantum",
    "QUANTUM_PROMPTS": "modules/quantum/prompts",
    "system_analysis": "modules/analysis",
    "utils": "tools/utilities",
}

# Critical files that must exist
CRITICAL_FILES = [
    "README.md",
    "docs/CHANGELOG.md",
    "docs/VERSIONING.md",
    "docs/REORGANIZATION_SUMMARY.md",
    "docs/NEXT_STEPS.md",
    "docs/STATUS_VISUALIZATION.md",
]


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Verify the integrity of the EVA & GUARANI system after reorganization."
    )
    parser.add_argument(
        "--report",
        type=str,
        default="./reports/system_integrity_report.md",
        help="Path to save the integrity report.",
    )
    parser.add_argument(
        "--json_report",
        type=str,
        default="./reports/system_integrity_report.json",
        help="Path to save the report in JSON format.",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Perform a deep check, including file counting and content validation.",
    )
    return parser.parse_args()


def check_main_categories() -> Tuple[bool, List[str], List[str]]:
    """Check if all main categories exist."""
    missing_categories = []
    existing_categories = []

    for category in MAIN_CATEGORIES:
        if os.path.isdir(category):
            existing_categories.append(category)
            logger.info(f"✅ Main category '{category}' exists.")
        else:
            missing_categories.append(category)
            logger.error(f"❌ Main category '{category}' not found.")

    return len(missing_categories) == 0, existing_categories, missing_categories


def check_subcategories(
    existing_main_categories: List[str],
) -> Tuple[bool, Dict[str, List[str]], Dict[str, List[str]]]:
    """Check if critical subcategories exist."""
    all_ok = True
    existing_subcategories = {}
    missing_subcategories = {}

    for category in existing_main_categories:
        if category in CRITICAL_SUBCATEGORIES:
            existing_subcategories[category] = []
            missing_subcategories[category] = []

            for subcategory in CRITICAL_SUBCATEGORIES[category]:
                full_path = os.path.join(category, subcategory)
                if os.path.isdir(full_path):
                    existing_subcategories[category].append(subcategory)
                    logger.info(f"✅ Subcategory '{full_path}' exists.")
                else:
                    missing_subcategories[category].append(subcategory)
                    logger.error(f"❌ Subcategory '{full_path}' not found.")
                    all_ok = False

    return all_ok, existing_subcategories, missing_subcategories


def check_moved_folders() -> Tuple[bool, Dict[str, bool]]:
    """Check if folders were moved correctly to the new structure."""
    all_moved = True
    moved_status = {}

    for source, destination in MOVED_FOLDERS.items():
        # If the original folder still exists, it may not have been moved correctly
        original_exists = os.path.isdir(source)

        # Check if the destination exists
        destination_exists = os.path.isdir(destination)

        moved_status[source] = {
            "destination": destination,
            "destination_exists": destination_exists,
            "original_exists": original_exists,
            "status": "OK" if destination_exists else "FAIL",
        }

        if destination_exists:
            logger.info(f"✅ Folder '{source}' moved correctly to '{destination}'.")
        else:
            logger.error(
                f"❌ Folder '{destination}' not found. The folder '{source}' may not have been moved correctly."
            )
            all_moved = False

    return all_moved, moved_status


def check_critical_files() -> Tuple[bool, List[str], List[str]]:
    """Check if all critical files exist."""
    missing_files = []
    existing_files = []

    for file_path in CRITICAL_FILES:
        if os.path.isfile(file_path):
            existing_files.append(file_path)
            logger.info(f"✅ Critical file '{file_path}' exists.")
        else:
            missing_files.append(file_path)
            logger.error(f"❌ Critical file '{file_path}' not found.")

    return len(missing_files) == 0, existing_files, missing_files


def count_files_by_category() -> Dict[str, int]:
    """Count the number of files in each main category."""
    file_counts = {}

    for category in MAIN_CATEGORIES:
        if os.path.isdir(category):
            count = 0
            for root, _, files in os.walk(category):
                count += len(files)
            file_counts[category] = count
            logger.info(f"📊 Category '{category}' contains {count} files.")

    return file_counts


def check_quarantine_folders() -> Dict[str, int]:
    """Check quarantine folders."""
    quarantine_info = {}
    quarantine_folders = [
        "quarantine",
        "quarantine_20250319",
        "quarantine_duplicates_20250319",
        "quarantine_folders_20250319",
    ]

    for folder in quarantine_folders:
        if os.path.isdir(folder):
            # Count files in quarantine
            file_count = 0
            folder_count = 0
            for root, dirs, files in os.walk(folder):
                file_count += len(files)
                folder_count += len(dirs)

            quarantine_info[folder] = {
                "exists": True,
                "file_count": file_count,
                "folder_count": folder_count,
            }
            logger.info(
                f"✅ Quarantine folder '{folder}' exists with {file_count} files and {folder_count} subfolders."
            )
        else:
            quarantine_info[folder] = {"exists": False, "file_count": 0, "folder_count": 0}
            logger.warning(f"⚠️ Quarantine folder '{folder}' not found.")

    return quarantine_info


def deep_check() -> Dict[str, Any]:
    """Perform a deep system check."""
    results = {}

    # Check configuration files
    config_files = ["core/config/config.json", "core/config/settings.py"]
    configs_ok = True
    for file in config_files:
        if os.path.isfile(file):
            logger.info(f"✅ Configuration file '{file}' exists.")
        else:
            logger.warning(f"⚠️ Configuration file '{file}' not found.")
            configs_ok = False

    results["config_files_ok"] = configs_ok

    # Check READMEs in each main category
    readmes_ok = True
    readme_status = {}
    for category in MAIN_CATEGORIES:
        readme_path = os.path.join(category, "README.md")
        readme_exists = os.path.isfile(readme_path)
        readme_status[category] = readme_exists
        if readme_exists:
            logger.info(f"✅ README found in '{category}'.")
        else:
            logger.warning(f"⚠️ README not found in '{category}'.")
            readmes_ok = False

    results["readmes_ok"] = readmes_ok
    results["readme_status"] = readme_status

    # Check presence of Python files in code categories
    code_categories = ["core", "modules", "integrations", "tools"]
    python_files_ok = True
    python_files_count = {}

    for category in code_categories:
        if os.path.isdir(category):
            count = 0
            for root, _, files in os.walk(category):
                count += sum(1 for f in files if f.endswith(".py"))
            python_files_count[category] = count
            if count > 0:
                logger.info(f"✅ Category '{category}' contains {count} Python files.")
            else:
                logger.warning(f"⚠️ Category '{category}' does not contain Python files.")
                python_files_ok = False

    results["python_files_ok"] = python_files_ok
    results["python_files_count"] = python_files_count

    return results


def generate_report(args: argparse.Namespace, results: Dict[str, Any]) -> None:
    """Generate system integrity report."""
    # Create report directory if it does not exist
    os.makedirs(os.path.dirname(args.report), exist_ok=True)

    # Save JSON report
    with open(args.json_report, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    # Calculate global status
    status_ok = (
        results["main_categories_ok"]
        and results["subcategories_ok"]
        and results["moved_folders_ok"]
        and results["critical_files_ok"]
    )

    # Save Markdown report
    with open(args.report, "w", encoding="utf-8") as f:
        f.write("# EVA & GUARANI System Integrity Report\n\n")
        f.write(f"*Date: {time.strftime('%d/%m/%Y %H:%M')}*\n\n")

        # General Status
        f.write("## General Status\n\n")
        if status_ok:
            f.write(
                "✅ **SYSTEM INTACT** - All critical components have been verified and are as expected.\n\n"
            )
        else:
            f.write(
                "⚠️ **ATTENTION NEEDED** - Some critical components were not found or have issues.\n\n"
            )

        # Summary
        f.write("## Summary\n\n")
        f.write(
            f"- Main Categories: {'✅ All OK' if results['main_categories_ok'] else '❌ Missing some'}\n"
        )
        f.write(
            f"- Critical Subcategories: {'✅ All OK' if results['subcategories_ok'] else '❌ Missing some'}\n"
        )
        f.write(
            f"- Moved Folders: {'✅ All OK' if results['moved_folders_ok'] else '❌ Problems detected'}\n"
        )
        f.write(
            f"- Critical Files: {'✅ All OK' if results['critical_files_ok'] else '❌ Missing some'}\n\n"
        )

        # Main Categories
        f.write("## Main Categories\n\n")
        for category in MAIN_CATEGORIES:
            if category in results["existing_categories"]:
                f.write(f"- ✅ `/{category}`\n")
            else:
                f.write(f"- ❌ `/{category}` (NOT FOUND)\n")
        f.write("\n")

        # Critical Subcategories
        f.write("## Critical Subcategories\n\n")
        for main_category, subcategories in CRITICAL_SUBCATEGORIES.items():
            if not subcategories:
                continue

            f.write(f"### /{main_category}\n\n")
            if main_category in results["existing_subcategories"]:
                for subcategory in subcategories:
                    if subcategory in results["existing_subcategories"][main_category]:
                        f.write(f"- ✅ `{subcategory}`\n")
                    else:
                        f.write(f"- ❌ `{subcategory}` (NOT FOUND)\n")
            else:
                f.write("*Main category not found*\n")
            f.write("\n")

        # Moved Folders
        f.write("## Moved Folders\n\n")
        for source, info in results["moved_status"].items():
            if info["destination_exists"]:
                f.write(f"- ✅ `{source}` → `{info['destination']}`\n")
            else:
                status = " (The original folder still exists)" if info["original_exists"] else ""
                f.write(f"- ❌ `{source}` → `{info['destination']}` (NOT FOUND){status}\n")
        f.write("\n")

        # Critical Files
        f.write("## Critical Files\n\n")
        for file_path in CRITICAL_FILES:
            if file_path in results["existing_files"]:
                f.write(f"- ✅ `{file_path}`\n")
            else:
                f.write(f"- ❌ `{file_path}` (NOT FOUND)\n")
        f.write("\n")

        # File Count
        f.write("## File Count by Category\n\n")
        for category, count in results["file_counts"].items():
            f.write(f"- `/{category}`: {count} files\n")
        f.write("\n")

        # Quarantine Information
        f.write("## Quarantine Folders\n\n")
        for folder, info in results["quarantine_info"].items():
            if info["exists"]:
                f.write(
                    f"- ✅ `{folder}`: {info['file_count']} files, {info['folder_count']} subfolders\n"
                )
            else:
                f.write(f"- ⚠️ `{folder}` (NOT FOUND)\n")
        f.write("\n")

        # Deep Check (if applicable)
        if args.deep:
            f.write("## Deep Check\n\n")

            f.write("### Configuration Files\n\n")
            if results["deep_check"]["config_files_ok"]:
                f.write("✅ All critical configuration files are present.\n\n")
            else:
                f.write("⚠️ Some critical configuration files were not found.\n\n")

            f.write("### READMEs in Main Categories\n\n")
            for category, exists in results["deep_check"]["readme_status"].items():
                if exists:
                    f.write(f"- ✅ `/{category}/README.md`\n")
                else:
                    f.write(f"- ⚠️ `/{category}/README.md` (NOT FOUND)\n")
            f.write("\n")

            f.write("### Python Files in Code Categories\n\n")
            for category, count in results["deep_check"]["python_files_count"].items():
                if count > 0:
                    f.write(f"- ✅ `/{category}`: {count} Python files\n")
                else:
                    f.write(f"- ⚠️ `/{category}`: No Python files found\n")
            f.write("\n")

        # Recommendations
        f.write("## Recommendations\n\n")
        if not status_ok:
            f.write("### Recommended Corrective Actions\n\n")

            if not results["main_categories_ok"]:
                f.write("1. **Create missing main categories**:\n")
                for category in results["missing_categories"]:
                    f.write(f"   - Create the folder `/{category}`\n")
                f.write("\n")

            missing_subcats = False
            for main_category, subcats in results.get("missing_subcategories", {}).items():
                if subcats:
                    missing_subcats = True
                    break

            if missing_subcats:
                f.write("2. **Create missing critical subcategories**:\n")
                for main_category, subcats in results.get("missing_subcategories", {}).items():
                    for subcat in subcats:
                        f.write(f"   - Create the folder `/{main_category}/{subcat}`\n")
                f.write("\n")

            if not results["moved_folders_ok"]:
                f.write("3. **Check folders that were not moved correctly**:\n")
                for source, info in results["moved_status"].items():
                    if not info["destination_exists"]:
                        f.write(f"   - Move `{source}` to `{info['destination']}`\n")
                f.write("\n")

            if not results["critical_files_ok"]:
                f.write("4. **Recover or recreate missing critical files**:\n")
                for file_path in results["missing_files"]:
                    f.write(f"   - Recover or recreate `{file_path}`\n")
                f.write("\n")
        else:
            f.write("### Continuous Maintenance\n\n")
            f.write(
                "1. **Update references** in code files to reflect the new directory structure\n"
            )
            f.write(
                "2. **Perform integration tests** to verify that all functionalities remain operational\n"
            )
            f.write(
                "3. **Expand documentation** for components that are not yet fully documented\n"
            )
            f.write("4. **Implement a CI/CD system** to ensure continuous system integrity\n\n")

        f.write("---\n\n")
        f.write("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

    logger.info(f"Integrity report generated: {args.report}")
    logger.info(f"JSON report generated: {args.json_report}")


def main() -> None:
    """Main function."""
    args = parse_arguments()

    logger.info("Starting integrity check of the EVA & GUARANI system")

    results = {}

    # Check main categories
    main_categories_ok, existing_categories, missing_categories = check_main_categories()
    results["main_categories_ok"] = main_categories_ok
    results["existing_categories"] = existing_categories
    results["missing_categories"] = missing_categories

    # Check critical subcategories
    subcategories_ok, existing_subcategories, missing_subcategories = check_subcategories(
        existing_categories
    )
    results["subcategories_ok"] = subcategories_ok
    results["existing_subcategories"] = existing_subcategories
    results["missing_subcategories"] = missing_subcategories

    # Check moved folders
    moved_folders_ok, moved_status = check_moved_folders()
    results["moved_folders_ok"] = moved_folders_ok
    results["moved_status"] = moved_status

    # Check critical files
    critical_files_ok, existing_files, missing_files = check_critical_files()
    results["critical_files_ok"] = critical
