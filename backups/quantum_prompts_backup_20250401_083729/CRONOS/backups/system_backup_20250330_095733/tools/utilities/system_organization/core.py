#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Core System Organization Module
This module provides a unified interface for system organization and maintenance.

Version: 1.0.0
Date: 2025-03-20
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("system_organization.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


class SystemOrganizer:
    """Core system organization class that handles all structural operations."""

    def __init__(self, root_dir: Optional[Path] = None):
        """Initialize the system organizer with root directory."""
        self.root_dir = root_dir or Path().resolve()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Standard directory structure
        self.CORE_DIRS = {
            "atlas": "core/atlas",
            "config": "core/config",
            "cronos": "core/cronos",
            "ethik": "core/ethik",
            "nexus": "core/nexus",
            "os": "core/os",
        }

        self.MODULE_DIRS = {
            "analysis": "modules/analysis",
            "blockchain": "modules/blockchain",
            "quantum": "modules/quantum",
            "visualization": "modules/visualization",
        }

        self.INTEGRATION_DIRS = {
            "apis": "integrations/apis",
            "bots": "integrations/bots",
            "platforms": "integrations/platforms",
            "services": "integrations/services",
        }

        self.TOOL_DIRS = {
            "deployment": "tools/deployment",
            "maintenance": "tools/maintenance",
            "scripts": "tools/scripts",
            "utilities": "tools/utilities",
        }

        # Backup and quarantine directories
        self.backup_dir = self.root_dir / "backup" / f"system_backup_{self.timestamp}"
        self.quarantine_dir = self.root_dir / "quarantine" / f"quarantine_{self.timestamp}"

    def create_backup(self, target_path: Path) -> bool:
        """Create a backup of the specified path."""
        try:
            rel_path = target_path.relative_to(self.root_dir)
            backup_path = self.backup_dir / rel_path

            # Create parent directories
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            if target_path.is_dir():
                shutil.copytree(target_path, backup_path, dirs_exist_ok=True)
            else:
                shutil.copy2(target_path, backup_path)

            logging.info(f"Created backup: {rel_path}")
            return True

        except Exception as e:
            logging.error(f"Backup failed for {target_path}: {str(e)}")
            return False

    def organize_directory(
        self, directory_map: Dict[str, str]
    ) -> Tuple[int, List[Tuple[str, str]]]:
        """Organize directories according to the provided mapping."""
        success_count = 0
        failed_items = []

        for source, destination in directory_map.items():
            source_path = self.root_dir / source
            dest_path = self.root_dir / destination

            if not source_path.exists():
                continue

            try:
                # Create backup
                self.create_backup(source_path)

                # Create parent directories
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                if dest_path.exists():
                    # Move to quarantine if destination exists
                    quarantine_path = self.quarantine_dir / source
                    quarantine_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source_path), str(quarantine_path))
                    logging.info(f"Moved to quarantine: {source} -> {quarantine_path}")
                else:
                    # Move to new location
                    shutil.move(str(source_path), str(dest_path))
                    logging.info(f"Organized: {source} -> {destination}")
                    success_count += 1

            except Exception as e:
                logging.error(f"Failed to organize {source}: {str(e)}")
                failed_items.append((source, str(e)))

        return success_count, failed_items

    def organize_system(self) -> bool:
        """Organize the entire system structure."""
        try:
            # Create essential directories
            for directory_map in [
                self.CORE_DIRS,
                self.MODULE_DIRS,
                self.INTEGRATION_DIRS,
                self.TOOL_DIRS,
            ]:
                success, failed = self.organize_directory(directory_map)
                logging.info(f"Organized {success} directories, {len(failed)} failures")

            # Create backup and quarantine directories if they don't exist
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            self.quarantine_dir.mkdir(parents=True, exist_ok=True)

            return True

        except Exception as e:
            logging.error(f"System organization failed: {str(e)}")
            return False

    def generate_report(self) -> Optional[Path]:
        """Generate a system organization report."""
        report_dir = self.root_dir / "docs" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        report_path = report_dir / f"system_organization_report_{self.timestamp}.md"

        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("# System Organization Report\n\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                f.write("## Directory Structure\n\n")
                f.write("### Core Directories\n")
                for name, path in self.CORE_DIRS.items():
                    f.write(f"- `{name}`: {path}\n")

                f.write("\n### Module Directories\n")
                for name, path in self.MODULE_DIRS.items():
                    f.write(f"- `{name}`: {path}\n")

                f.write("\n### Integration Directories\n")
                for name, path in self.INTEGRATION_DIRS.items():
                    f.write(f"- `{name}`: {path}\n")

                f.write("\n### Tool Directories\n")
                for name, path in self.TOOL_DIRS.items():
                    f.write(f"- `{name}`: {path}\n")

                f.write("\n## Backup Information\n")
                f.write(f"- Backup location: `{self.backup_dir}`\n")
                f.write(f"- Quarantine location: `{self.quarantine_dir}`\n\n")

                f.write("## Next Steps\n\n")
                f.write("1. Review quarantined items\n")
                f.write("2. Verify all systems are functioning correctly\n")
                f.write("3. Update documentation to reflect new structure\n")
                f.write("4. Clean up any temporary files\n\n")

                f.write("---\n\n")
                f.write("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

            logging.info(f"Report generated at {report_path}")
            return report_path

        except Exception as e:
            logging.error(f"Error generating report: {str(e)}")
            return None


def main():
    """Main execution function."""
    logging.info("=== STARTING SYSTEM ORGANIZATION ===")

    try:
        organizer = SystemOrganizer()
        if organizer.organize_system():
            report_path = organizer.generate_report()
            if report_path:
                logging.info(f"Organization complete. Report available at: {report_path}")
        else:
            logging.error("System organization failed")

    except Exception as e:
        logging.error(f"Error during system organization: {str(e)}")

    logging.info("=== SYSTEM ORGANIZATION PROCESS COMPLETED ===")


if __name__ == "__main__":
    main()
