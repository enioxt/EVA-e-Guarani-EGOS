#!/usr/bin/env python3
"""
EVA & GUARANI - Project Archive Utility
This script helps archive unused folders to improve performance.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import argparse


def archive_directory(source_dir, archive_dir=None, delete=False):
    """Archive a directory to improve performance."""
    source_path = Path(source_dir)

    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return False

    if not archive_dir:
        # Create archive directory in parent folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{source_path.name}_archived_{timestamp}"
        archive_path = source_path.parent / archive_name
    else:
        archive_path = Path(archive_dir) / source_path.name

    try:
        if delete:
            print(f"Deleting directory: {source_dir}")
            shutil.rmtree(str(source_path))
            print(f"✓ Directory deleted: {source_dir}")
        else:
            print(f"Archiving: {source_dir} → {archive_path}")
            # Create parent directories if they don't exist
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(archive_path))
            print(f"✓ Directory archived: {archive_path}")
        return True
    except Exception as e:
        print(f"Error during archiving: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Archive unused directories in EVA & GUARANI project"
    )
    parser.add_argument("--archive-dir", help="Directory where to archive files")
    parser.add_argument(
        "--delete", action="store_true", help="Delete directories instead of archiving"
    )
    parser.add_argument(
        "--list", action="store_true", help="List recommended directories to archive"
    )
    args = parser.parse_args()

    # Directories that are recommended to archive
    recommended_archive_dirs = [
        "backup",
        "quarantine",
        "docs/archived",
        "docs/BACKUPS",
        "docs/AVA_TECH_ART",
        "docs/AVA",
        "core/atlas_pre_merge_20250320_082617",
        "core/nexus_pre_merge_20250320_082617",
        "core/cronos_pre_merge_20250320_082617",
    ]

    if args.list:
        print("\nRecommended directories to archive:")
        for directory in recommended_archive_dirs:
            path = Path(directory)
            if path.exists():
                size = sum(f.stat().st_size for f in path.glob("**/*") if f.is_file())
                print(f"- {directory:<40} {size / (1024*1024):.2f} MB")
        return

    print(f"\n{'-'*80}")
    print(f"EVA & GUARANI - Project Archive Utility")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'-'*80}\n")

    # Ask for confirmation if no specific arguments provided
    if not args.list and not any([args.delete, args.archive_dir]):
        print("This utility will help you archive unused directories to improve performance.")
        print("Recommended directories to archive:")
        for directory in recommended_archive_dirs:
            path = Path(directory)
            if path.exists():
                print(f"- {directory}")

        confirm = input("\nWould you like to archive these directories? (y/n): ")
        if confirm.lower() != "y":
            print("Operation cancelled.")
            return

    # Process each recommended directory
    archived_count = 0
    for directory in recommended_archive_dirs:
        path = Path(directory)
        if path.exists():
            if archive_directory(directory, args.archive_dir, args.delete):
                archived_count += 1

    if archived_count > 0:
        print(f"\nSuccessfully processed {archived_count} directories.")
        print("This should improve indexing performance significantly.")
    else:
        print("\nNo directories were processed. They may already be archived or do not exist.")

    print(f"\n{'-'*80}")


if __name__ == "__main__":
    main()
