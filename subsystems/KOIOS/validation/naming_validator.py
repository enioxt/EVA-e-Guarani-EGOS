#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KOIOS Naming Convention Validator
================================

Scans project directories and files to ensure adherence to EGOS
naming conventions defined in KOIOS standards.

Version: 0.1 (Initial Structure)
"""

import argparse
import re
from pathlib import Path
from typing import List

# Adjust import based on project structure
from subsystems.KOIOS.core.logging import KoiosLogger

# Initialize logger for the validator script
logger = KoiosLogger.get_logger(__name__)

# --- Naming Convention Rules (Based on KOIOS STANDARDS.md Section 5) ---
# Refined regex patterns
PYTHON_FILE_PATTERN = r"^[a-z0-9_]+\.py$"  # Must be snake_case and end with .py
PYTHON_TEST_PATTERN = r"^test_[a-z0-9_]+\.py$"
MARKDOWN_GENERAL_PATTERN = r"^[a-z0-9_-]+\.md$"  # snake_case or kebab-case, must end with .md
MARKDOWN_SPECIFIC_PATTERN = r"^[A-Z_]+\.md$"  # UPPERCASE_SNAKE, must end with .md
CONFIG_PATTERN = r"^[a-z0-9_.-]+\.(json|yaml|yml|toml|ini)$"
SCRIPT_PATTERN = r"^[a-z0-9_-]+\.(sh|bat|ps1)$"  # Python scripts covered separately
DIR_SNAKE_KEBAB_PATTERN = r"^[a-z0-9_-]+$"
DIR_UPPERCASE_PATTERN = r"^[A-Z0-9_]+$"  # Primarily for top-level subsystems

# Special file names to allow (case-sensitive)
ALLOWED_SPECIFIC_FILES = {
    "README.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "LICENSE.md",
    "pyproject.toml",
    "requirements.txt",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    ".env",
    "go.mod",  # If Go is used
    "__init__.py",  # Allow init files
    # Add other specific allowed files
}

# Directories whose *contents* should be ignored entirely (case-sensitive)
IGNORE_CONTENTS_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    ".vscode",
    ".cursor",
    "htmlcov",
    # Add others if needed, e.g., build artifacts, node_modules
}

# NOTE: Removed ALLOWED_SPECIFIC_DIRS. Directory names themselves are validated by patterns below.
# We only need to ignore the *contents* of certain dirs like .git, __pycache__.

# Top-level directories expected to be UPPERCASE under subsystems/
EXPECTED_UPPERCASE_SUBDIRS = {
    "ATLAS",
    "CRONOS",
    "ETHIK",
    "KOIOS",
    "MASTER",
    "MYCELIUM",
    "NEXUS",
    # Add other subsystems as needed
}


def validate_name(name: str, item_path: Path, is_dir: bool) -> List[str]:
    """Validates a single file or directory name against conventions."""
    violations = []
    # Use relative path for context to match standards doc examples
    try:
        # Use Path.cwd() for now, as that's what tests mock
        relative_path = str(item_path.relative_to(Path.cwd()))  # Placeholder relative path
    except ValueError:
        relative_path = str(item_path)  # Fallback to full path if relative fails

    # --- Initial Skip Checks ---

    # 1. Skip universally ignored file names (case-sensitive match)
    if not is_dir and name in ALLOWED_SPECIFIC_FILES:
        logger.debug(f"Skipping specifically allowed file: '{relative_path}'")
        return []

    # 2. Skip if item is WITHIN an explicitly ignored directory (e.g., file inside .git)
    # Check parent parts for any directory in IGNORE_CONTENTS_DIRS
    parent_parts = item_path.parent.parts
    # Handle edge case: if item_path is root (e.g. '.'), parent_parts is empty.
    if parent_parts and any(part in IGNORE_CONTENTS_DIRS for part in parent_parts):
        logger.debug(f"Skipping item '{relative_path}' inside an ignored directory.")
        return []
    # Also skip the ignored directory itself
    if is_dir and name in IGNORE_CONTENTS_DIRS:
        logger.debug(f"Skipping ignored directory itself: '{relative_path}'")
        return []

    # --- Validation Logic ---
    if is_dir:
        # Check if it's a directory directly under subsystems/
        # Check needs to be robust against different CWDs or deeper paths
        # Using relative_path parts which are relative to mocked CWD ('.') in tests
        path_parts = Path(relative_path).parts
        is_subsystem_dir = len(path_parts) > 1 and path_parts[-2] == "subsystems"

        if is_subsystem_dir:
            # Directories directly under subsystems MUST be UPPERCASE_SNAKE
            if not re.fullmatch(DIR_UPPERCASE_PATTERN, name):
                violations.append(
                    f"Subsystem Directory '{relative_path}': "
                    f"Expected UPPERCASE_SNAKE, found '{name}'"
                )
            # Optionally, also check if it's in the known list?
            # elif name not in EXPECTED_UPPERCASE_SUBDIRS:
            #    violations.append(
            #        f"Subsystem Directory '{relative_path}': "
            #        f"Unknown subsystem name '{name}'"
            #    )
        # General directory check (snake_case or kebab-case)
        # Apply this if it's not a subsystem dir AND not an explicitly ignored dir name
        elif name not in IGNORE_CONTENTS_DIRS and not re.fullmatch(DIR_SNAKE_KEBAB_PATTERN, name):
            violations.append(
                f"Directory '{relative_path}': Expected snake_case or kebab-case, found '{name}'"
            )
    else:  # It's a file
        ext = item_path.suffix.lower()
        if ext == ".py":
            if name.startswith("test_"):
                if not re.fullmatch(PYTHON_TEST_PATTERN, name):
                    violations.append(
                        f"Python Test File '{relative_path}': "
                        f"Invalid format (expected test_snake_case.py)."
                    )
            # Don't flag __init__.py (already skipped) or test files here
            elif not name.startswith("test_") and not re.fullmatch(PYTHON_FILE_PATTERN, name):
                violations.append(
                    f"Python File '{relative_path}': "
                    f"Invalid format (expected snake_case.py). Found '{name}'"
                )
        elif ext == ".md":
            # Check against general pattern OR specific uppercase pattern
            is_general_md = re.fullmatch(MARKDOWN_GENERAL_PATTERN, name)
            is_specific_md = re.fullmatch(MARKDOWN_SPECIFIC_PATTERN, name)
            if not (is_general_md or is_specific_md):
                violations.append(
                    f"Markdown File '{relative_path}': "
                    f"Invalid format (expected snake_case/kebab-case.md or UPPERCASE_SNAKE.md). "
                    f"Found '{name}'"
                )
        elif ext in [".json", ".yaml", ".yml", ".toml", ".ini"]:
            if not re.fullmatch(CONFIG_PATTERN, name):
                violations.append(f"Config File '{relative_path}': Invalid format. Found '{name}'")
        elif ext in [".sh", ".bat", ".ps1"]:
            if not re.fullmatch(SCRIPT_PATTERN, name):
                violations.append(
                    f"Script File '{relative_path}': "
                    f"Invalid format (expected snake_case/kebab-case with extension). "
                    f"Found '{name}'"
                )
        else:
            # If the extension wasn't specifically handled above and the file wasn't skipped
            # Flag as a violation unless it's extensionless and allowed (like LICENSE)
            if ext:  # File has an extension that wasn't handled
                violations.append(
                    f"File '{relative_path}': "
                    f"Unrecognized/disallowed file type/extension ('{ext}'). Found '{name}'"
                )
            # Check needed for extensionless files NOT in the allowed list.
            elif not ext and name not in ALLOWED_SPECIFIC_FILES:
                violations.append(
                    f"File '{relative_path}': "
                    f"Files without extensions are generally disallowed "
                    f"(except specific ones like LICENSE). Found '{name}'"
                )

    # Log violations if any found
    if violations:
        logger.debug(f"Violations found for '{relative_path}': {violations}")

    return violations


def scan_directory(target_dir: Path, project_root: Path) -> List[str]:
    """Recursively scans a directory and validates names."""
    all_violations = []
    logger.info(f"Scanning directory: {target_dir}")

    # Ensure the main loop is wrapped for PermissionError
    try:
        for item in target_dir.iterdir():
            try:
                relative_item_path = item.relative_to(project_root)
            except ValueError:
                logger.warning(f"Item {item} seems outside project root {project_root}. Skipping.")
                continue  # Skip items outside the root

            item_name = item.name
            is_dir = item.is_dir()

            # Check if the item itself or its parent is in an ignored directory path
            should_skip = False
            parent_parts = item.parent.parts
            if parent_parts and any(part in IGNORE_CONTENTS_DIRS for part in parent_parts):
                # Content within an ignored directory
                # Log only once per ignored parent dir? Maybe too complex.
                # Log skipping the item itself for clarity.
                logger.debug(f"Skipping item '{relative_item_path}' inside an ignored directory.")
                should_skip = True
            elif is_dir and item_name in IGNORE_CONTENTS_DIRS:
                # The directory itself is ignored
                # Fixed: Moved logging here from validate_name
                logger.debug(f"Skipping ignored directory itself: '{relative_item_path}'")
                should_skip = True

            if should_skip:
                continue  # Move to the next item in target_dir

            # If not skipped, validate the item name
            violations = validate_name(item_name, relative_item_path, is_dir)
            all_violations.extend(violations)

            # Recursively scan subdirectories if it's a directory and not ignored
            if is_dir:
                # No need to check IGNORE_CONTENTS_DIRS again, handled by should_skip above
                all_violations.extend(scan_directory(item, project_root))

    except PermissionError:
        # Fixed: This block should now correctly catch PermissionError from iterdir
        logger.error(f"Permission denied accessing {target_dir}. Skipping.")
    except Exception as e:
        logger.exception(f"Error scanning directory {target_dir}: {e}")

    return all_violations


def find_project_root(start_path: Path) -> Path:
    """Find the project root by looking for a marker (e.g., .git or pyproject.toml)."""
    current_path = start_path.resolve()
    while True:
        if (current_path / ".git").exists() or (current_path / "pyproject.toml").exists():
            return current_path
        if current_path.parent == current_path:  # Reached the filesystem root
            logger.warning(
                "Could not find project root marker (.git/pyproject.toml). "
                "Using current dir as fallback."
            )
            return start_path.resolve()
        current_path = current_path.parent


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Validate EGOS naming conventions.")
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target directory or file to scan (defaults to current directory).",
    )
    # TODO: Add arguments for --exclude, --rules-file, etc.
    args = parser.parse_args()

    start_scan_path = Path(args.target).resolve()
    project_root = find_project_root(start_scan_path)
    logger.info(f"Determined project root: {project_root}")

    if not start_scan_path.exists():
        logger.critical(f"Target path does not exist: {start_scan_path}")
        return

    violations = []
    if start_scan_path.is_dir():
        logger.info(f"Starting naming convention validation for directory: {start_scan_path}")
        violations = scan_directory(start_scan_path, project_root)
    elif start_scan_path.is_file():
        logger.info(f"Starting naming convention validation for file: {start_scan_path}")
        try:
            relative_path = start_scan_path.relative_to(project_root)
            violations = validate_name(start_scan_path.name, relative_path, False)
        except ValueError:
            logger.error(
                f"Target file {start_scan_path} is outside determined project root {project_root}."
            )
    else:
        logger.error(f"Target path is neither a file nor a directory: {start_scan_path}")

    if violations:
        logger.warning("Naming convention violations found:")
        for violation in sorted(list(set(violations))):  # Sort and remove duplicates
            logger.warning(f"- {violation}")
        # Optionally exit with non-zero code
        # import sys
        # sys.exit(1)
    else:
        logger.info("No naming convention violations found.")


if __name__ == "__main__":
    main()
