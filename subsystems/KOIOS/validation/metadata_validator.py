#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KOIOS Metadata Validator
========================

Scans project files (Python, Markdown) to ensure they contain required
metadata fields according to KOIOS standards.

TODO:
- Define the definitive metadata schema (load from STANDARDS.md or config?).
- Implement robust metadata extraction for Python files (AST, regex?).
- Implement metadata extraction for other relevant file types.
- Add more sophisticated validation logic (type checking, value constraints).
- Add command-line options (e.g., --schema-file, --exclude).
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# --- YAML Dependency ---
try:
    import yaml
except ImportError:
    print("ERROR: PyYAML library not found. Please install it:")
    print("pip install PyYAML>=6.0")
    sys.exit(1)

# --- Project Imports ---
# Assuming this script is in subsystems/KOIOS/validation/
try:
    from subsystems.KOIOS.core.logging import KoiosLogger

    # Reuse root finding and ignore list from naming validator for consistency
    from .naming_validator import IGNORE_CONTENTS_DIRS, find_project_root
except ImportError as e:
    print(f"Error importing validator components: {e}")
    print("Ensure the script is run correctly relative to the project root,")
    print("or adjust PYTHONPATH if necessary.")
    sys.exit(1)

# --- Globals & Constants ---
logger = KoiosLogger.get_logger(__name__)

# Placeholder Schema - Replace with actual schema definition later
# Example: Define required fields for different file types
PYTHON_REQUIRED_METADATA = {"description", "version", "author"}
MARKDOWN_REQUIRED_METADATA = {"description", "version", "status", "last_updated"}

# --- Core Functions ---


def extract_metadata_from_py(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Extracts metadata from a Python file.
    Placeholder implementation - needs robust parsing (e.g., AST, regex).
    """
    logger.debug(f"Attempting metadata extraction from Python file: {file_path}")
    # TODO: Implement robust Python metadata extraction
    # Example: Look for specific variables like __version__, __author__
    # Example: Parse module-level docstring for structured metadata
    metadata = {}
    try:
        # Very basic example: Look for simple assignments near top
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[:20]:  # Check first 20 lines
                if line.startswith("__version__"):
                    metadata["version"] = line.split("=")[1].strip().strip("'\"")
                elif line.startswith("__author__"):
                    metadata["author"] = line.split("=")[1].strip().strip("'\"")
                # Add more basic checks or implement AST parsing
        # Assume description might be in module docstring (needs parsing)
        if not metadata:
            logger.warning(
                f"No simple metadata found in Python file: {file_path}. Needs proper parsing."
            )
            return None  # Indicate no metadata found with this basic method
        return metadata
    except Exception as e:
        logger.error(f"Error extracting metadata from {file_path}: {e}", exc_info=True)
        return None


def extract_metadata_from_md(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Extracts metadata from YAML frontmatter in a Markdown file.
    """
    logger.debug(f"Attempting metadata extraction from Markdown file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    metadata = yaml.safe_load(frontmatter)
                    # Often frontmatter has a top-level 'metadata:' key
                    if isinstance(metadata, dict) and "metadata" in metadata:
                        return metadata.get("metadata")
                    elif isinstance(metadata, dict):  # Assume top-level keys are metadata
                        return metadata
                    else:
                        logger.warning(
                            f"Could not parse YAML frontmatter dictionary in {file_path}"
                        )
                        return None
            logger.debug(f"No YAML frontmatter found in {file_path}")
            return None  # No frontmatter found
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML frontmatter in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error reading or processing {file_path}: {e}", exc_info=True)
        return None


def validate_metadata(metadata: Optional[Dict[str, Any]], file_path: Path) -> List[str]:
    """
    Validates extracted metadata against the required schema for the file type.
    Returns a list of violation messages.
    """
    violations = []
    relative_path_str = str(file_path)  # Use relative path if possible later

    if metadata is None:
        # This means extraction failed or wasn't attempted/successful
        # Depending on policy, this could be a violation itself
        # violations.append(
        #     f"Metadata Missing/Unparseable: "
        #     f"Could not extract metadata from '{relative_path_str}'."
        # )
        logger.debug(
            f"No metadata to validate for {relative_path_str} (extraction failed or not found)."
        )
        return violations  # Cannot validate if no metadata was extracted

    if not isinstance(metadata, dict):
        violations.append(
            f"Invalid Format: Expected metadata dictionary, "
            f"found {type(metadata)} in '{relative_path_str}'."
        )
        return violations

    required_fields = set()
    file_ext = file_path.suffix.lower()

    if file_ext == ".py":
        required_fields = PYTHON_REQUIRED_METADATA
    elif file_ext == ".md":
        required_fields = MARKDOWN_REQUIRED_METADATA
    # Add other file types here
    else:
        logger.debug(f"Skipping metadata validation for unhandled file type: {relative_path_str}")
        return violations  # Don't validate types we don't have rules for yet

    # Check for missing required fields
    missing_fields = required_fields - metadata.keys()
    if missing_fields:
        for field in sorted(list(missing_fields)):
            violations.append(
                f"Metadata Missing: Required field '{field}' missing in '{relative_path_str}'."
            )

    # TODO: Add further validation (type checks, value constraints, etc.)
    # Example: Check if 'version' follows semantic versioning
    # Example: Check if 'status' is one of ['active', 'deprecated', 'planning']

    return violations


def scan_directory_metadata(target_dir: Path, project_root: Path) -> List[str]:
    """
    Recursively scans a directory, extracts metadata from relevant files,
    and validates it.
    """
    all_violations = []
    logger.info(f"Scanning directory for metadata: {target_dir}")

    try:
        for item in target_dir.iterdir():
            try:
                relative_item_path = item.relative_to(project_root)
            except ValueError:
                logger.warning(f"Item {item} seems outside project root {project_root}. Skipping.")
                continue

            item_name = item.name
            is_dir = item.is_dir()

            # --- Skipping Logic (mirrors naming_validator) ---
            should_skip = False
            parent_parts = item.parent.parts
            if parent_parts and any(part in IGNORE_CONTENTS_DIRS for part in parent_parts):
                logger.debug(
                    f"[Metadata Scan] Skipping item '{relative_item_path}' "
                    f"inside an ignored directory."
                )
                should_skip = True
            elif is_dir and item_name in IGNORE_CONTENTS_DIRS:
                logger.debug(
                    f"[Metadata Scan] Skipping ignored directory itself: '{relative_item_path}'"
                )
                should_skip = True

            if should_skip:
                continue
            # --- End Skipping Logic ---

            if is_dir:
                # Recursively scan subdirectories
                all_violations.extend(scan_directory_metadata(item, project_root))
            else:
                # Process files: Extract and Validate Metadata
                file_ext = item.suffix.lower()
                metadata: Optional[Dict[str, Any]] = None

                if file_ext == ".py":
                    metadata = extract_metadata_from_py(item)
                elif file_ext == ".md":
                    metadata = extract_metadata_from_md(item)
                # Add other supported file types here

                # Only validate if metadata *could* be extracted for this file type
                if file_ext in [".py", ".md"]:  # Check against handled types
                    # Validate even if metadata is None (extraction failed) for handled types
                    # Policy Decision: Should failure to extract be a violation?
                    # Yes, if required fields exist.
                    # Let validate_metadata handle the None case based on required fields.
                    file_violations = validate_metadata(
                        metadata, item
                    )  # Use absolute path 'item' for now
                    if file_violations:
                        logger.debug(f"Metadata violations found in {item}: {file_violations}")
                        all_violations.extend(file_violations)

    except PermissionError:
        logger.error(f"[Metadata Scan] Permission denied accessing {target_dir}. Skipping.")
    except Exception as e:
        logger.exception(f"[Metadata Scan] Error scanning directory {target_dir}: {e}")

    return all_violations


# --- Main Execution ---


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="KOIOS Metadata Validator.")
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help=(
            "Target directory or file to scan for metadata validation "
            "(defaults to current directory)."
        ),
    )
    # TODO: Add arguments for --schema-file, --exclude, etc.
    args = parser.parse_args()

    start_scan_path = Path(args.target).resolve()
    project_root = find_project_root(start_scan_path)
    logger.info(f"Determined project root: {project_root}")

    if not start_scan_path.exists():
        logger.critical(f"Target path does not exist: {start_scan_path}")
        return

    all_violations = []

    try:
        if start_scan_path.is_dir():
            logger.info(f"Starting metadata validation for directory: {start_scan_path}")
            all_violations = scan_directory_metadata(start_scan_path, project_root)
        elif start_scan_path.is_file():
            logger.info(f"Starting metadata validation for file: {start_scan_path}")
            file_ext = start_scan_path.suffix.lower()
            metadata = None
            if file_ext == ".py":
                metadata = extract_metadata_from_py(start_scan_path)
            elif file_ext == ".md":
                metadata = extract_metadata_from_md(start_scan_path)
            # Add other supported file types here

            if file_ext in [".py", ".md"]:
                all_violations = validate_metadata(metadata, start_scan_path)
            else:
                logger.info(
                    f"Skipping metadata validation for unsupported file type: {start_scan_path}"
                )

        else:
            logger.error(f"Target path is neither a file nor a directory: {start_scan_path}")

        # --- Report Results ---
        logger.info("Metadata validation scan complete.")  # Report even if no violations
        if all_violations:
            logger.warning("Metadata violations found:")
            # Sort and unique violations before printing
            unique_sorted_violations = sorted(list(set(all_violations)))
            for violation in unique_sorted_violations:
                logger.warning(f"- {violation}")
            logger.info(f"Found {len(unique_sorted_violations)} unique metadata violation(s).")
            # Optionally exit with non-zero code
            # sys.exit(1)
        else:
            logger.info("No metadata violations found.")

    except Exception as e:
        logger.critical(
            f"An unexpected error occurred during metadata validation: {e}", exc_info=True
        )
        # sys.exit(2)


if __name__ == "__main__":
    main()
