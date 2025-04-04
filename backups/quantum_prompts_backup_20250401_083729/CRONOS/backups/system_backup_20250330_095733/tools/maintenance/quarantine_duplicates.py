#!/usr/bin/env python
"""
EVA & GUARANI EGOS - Duplicate File Quarantine Tool

This script identifies and quarantines duplicate or legacy files, keeping
the system organized and free of redundancies.
"""

import os
import sys
import json
import shutil
import datetime
import hashlib
from pathlib import Path
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [QUARANTINE] %(message)s",
    handlers=[logging.FileHandler("quarantine.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("QUARANTINE")


class DuplicateQuarantineManager:
    """Manages the quarantine of duplicate or legacy files"""

    def __init__(self, base_path=None, dry_run=False):
        """Initialize the quarantine manager"""
        # Determine base path
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path(os.getcwd())
            # If we're not in the project root, try to find it
            if not (self.base_path / "core").exists():
                if (self.base_path.parent / "core").exists():
                    self.base_path = self.base_path.parent

        self.quarantine_dir = self.base_path / "quarantine"
        self.dry_run = dry_run

        # Known duplicate patterns
        self.duplicate_patterns = [
            {
                "primary": "core/ethik/ethik_core.py",
                "duplicates": ["core/ethik/ethik_core_1.py", "core/ethik/ethics.py"],
            },
            {
                "primary": "modules/quantum/quantum_integration.py",
                "duplicates": [
                    "modules/quantum/quantum_integration_1.py",
                    "modules/quantum/quantum_integration_guarantee.py",
                ],
            },
            {
                "primary": "tools/scripts/cursor_integration.py",
                "duplicates": ["BIOS-Q/BIOS_Q/cursor_integration.py"],
            },
            {
                "primary": "tools/scripts/context_manager.py",
                "duplicates": ["BIOS-Q/BIOS_Q/context_manager.py"],
            },
            {
                "primary": "tools/integration/cursor_atlas_bridge.py",
                "duplicates": ["integrations/platforms/integrate_quantum_knowledge.py"],
            },
            {"primary": "start_bios_q.bat", "duplicates": ["BIOS-Q/start_cursor_bios.bat"]},
        ]

        # Known legacy files
        self.legacy_files = ["conversa anterior.txt"]

    def calculate_file_hash(self, file_path):
        """Calculate the MD5 hash of a file"""
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.md5()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
                return file_hash.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return None

    def find_content_duplicates(self):
        """Find files with duplicate content based on hash"""
        hash_map = {}
        duplicates = []

        for root, _, files in os.walk(self.base_path):
            # Skip quarantine directory and .git
            if "quarantine" in Path(root).parts or ".git" in Path(root).parts:
                continue

            for filename in files:
                file_path = Path(root) / filename
                try:
                    # Skip large files
                    if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB
                        continue

                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash:
                        rel_path = file_path.relative_to(self.base_path)
                        if file_hash in hash_map:
                            duplicates.append(
                                {
                                    "hash": file_hash,
                                    "primary": hash_map[file_hash],
                                    "duplicate": str(rel_path),
                                }
                            )
                        else:
                            hash_map[file_hash] = str(rel_path)
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")

        return duplicates

    def quarantine_file(self, file_path, reason):
        """Move a file to quarantine"""
        try:
            relative_path = Path(file_path)
            if not relative_path.is_absolute():
                absolute_path = self.base_path / relative_path
            else:
                absolute_path = relative_path
                relative_path = relative_path.relative_to(self.base_path)

            if not absolute_path.exists():
                logger.warning(f"File not found: {absolute_path}")
                return False

            # Create quarantine directory structure
            quarantine_path = self.quarantine_dir / relative_path.parent
            os.makedirs(quarantine_path, exist_ok=True)

            # Create metadata
            metadata = {
                "original_path": str(relative_path),
                "quarantine_date": datetime.datetime.now().isoformat(),
                "reason": reason,
                "size": absolute_path.stat().st_size,
                "hash": self.calculate_file_hash(absolute_path),
            }

            metadata_path = quarantine_path / f"{relative_path.name}.meta.json"

            if self.dry_run:
                logger.info(f"[DRY RUN] Would quarantine: {relative_path}")
                return True

            # Copy file to quarantine
            shutil.copy2(absolute_path, quarantine_path / relative_path.name)

            # Save metadata
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

            # Rename original file to .quarantined
            # absolute_path.rename(absolute_path.with_suffix(absolute_path.suffix + ".quarantined"))

            logger.info(f"Quarantined: {relative_path} → {quarantine_path / relative_path.name}")
            return True

        except Exception as e:
            logger.error(f"Error quarantining {file_path}: {e}")
            return False

    def quarantine_known_duplicates(self):
        """Quarantine known duplicate files"""
        quarantined = []

        for pattern in self.duplicate_patterns:
            primary = pattern["primary"]
            for duplicate in pattern["duplicates"]:
                logger.info(f"Processing duplicate: {duplicate} (primary: {primary})")
                if self.quarantine_file(duplicate, f"Duplicate of {primary}"):
                    quarantined.append(duplicate)

        return quarantined

    def quarantine_legacy_files(self):
        """Quarantine known legacy files"""
        quarantined = []

        for legacy_file in self.legacy_files:
            logger.info(f"Processing legacy file: {legacy_file}")
            if self.quarantine_file(legacy_file, "Legacy file"):
                quarantined.append(legacy_file)

        return quarantined

    def report_content_duplicates(self):
        """Report but don't quarantine content-based duplicates"""
        content_duplicates = self.find_content_duplicates()

        if content_duplicates:
            logger.info(f"Found {len(content_duplicates)} content-based duplicates:")
            for dup in content_duplicates:
                logger.info(f"  {dup['duplicate']} is identical to {dup['primary']}")
        else:
            logger.info("No content-based duplicates found")

        return content_duplicates

    def run(self):
        """Run the quarantine process"""
        logger.info(f"Starting duplicate quarantine process from {self.base_path}")

        # Create quarantine directory
        os.makedirs(self.quarantine_dir, exist_ok=True)

        # Quarantine known duplicates
        logger.info("Quarantining known duplicates...")
        quarantined_duplicates = self.quarantine_known_duplicates()

        # Quarantine legacy files
        logger.info("Quarantining legacy files...")
        quarantined_legacy = self.quarantine_legacy_files()

        # Report content duplicates
        logger.info("Scanning for content-based duplicates...")
        content_duplicates = self.report_content_duplicates()

        # Summary
        logger.info("Quarantine process completed")
        logger.info(f"  - Known duplicates quarantined: {len(quarantined_duplicates)}")
        logger.info(f"  - Legacy files quarantined: {len(quarantined_legacy)}")
        logger.info(f"  - Content duplicates found: {len(content_duplicates)}")

        return {
            "known_duplicates": quarantined_duplicates,
            "legacy_files": quarantined_legacy,
            "content_duplicates": content_duplicates,
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="EVA & GUARANI EGOS - Duplicate File Quarantine Tool"
    )
    parser.add_argument("--base-path", help="Base path for the EVA & GUARANI EGOS system")
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate actions without making changes"
    )
    args = parser.parse_args()

    quarantine = DuplicateQuarantineManager(args.base_path, args.dry_run)
    results = quarantine.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
