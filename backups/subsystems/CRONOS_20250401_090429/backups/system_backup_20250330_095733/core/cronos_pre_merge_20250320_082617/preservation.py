#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CRONOS - Evolutionary Preservation Subsystem
Responsible for backup, versioning, and preservation of the EVA & GUARANI system
Version: 8.0.0
Date: 19/03/2025
"""

import os
import sys
import json
import logging
import datetime
import shutil
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple, Set

# Logging configuration
logger = logging.getLogger("EVA_GUARANI.CRONOS")

class Cronos:
    """
    Main class of the CRONOS subsystem, responsible for evolutionary preservation.

    CRONOS manages the backup, versioning, and preservation of the system,
    ensuring that the essence is maintained through transformations and
    allowing recovery and access to previous states when needed.
    """

    def __init__(self, config: Dict[str, Any], system_root: Path):
        """
        Initializes the CRONOS subsystem

        Args:
            config: Configuration of the CRONOS subsystem
            system_root: Root path of the system
        """
        self.logger = logger
        self.logger.info("⏳ Initializing CRONOS subsystem v8.0.0 ⏳")

        self.config = config
        self.system_root = system_root
        self.enabled = config.get("enabled", True)
        self.backup_interval_hours = config.get("backup_interval_hours", 12)
        self.versions_to_keep = config.get("versions_to_keep", 5)
        self.compression_level = config.get("compression_level", 6)
        self.include_logs = config.get("include_logs", False)

        # Configure paths
        self.backup_dir = system_root / "backup"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.version_history_file = self.backup_dir / "version_history.json"

        # System state
        self.is_running = False
        self.last_backup_time = None
        self.version_history = self._load_version_history()
        self.scheduled_backups = []

        # Metrics
        self.metrics = {
            "total_backups": len(self.version_history.get("versions", [])),
            "total_preserved_size_bytes": self._calculate_total_preserved_size(),
            "last_backup_duration_seconds": 0,
            "average_backup_size_bytes": 0,
            "compression_ratio": 0.0
        }

        # Check if metrics should be updated
        if self.metrics["total_backups"] > 0:
            self._update_metrics()

        self.logger.info(f"CRONOS initialized with interval of {self.backup_interval_hours}h and {self.versions_to_keep} versions to keep")

    def start(self) -> bool:
        """
        Starts the CRONOS subsystem.

        Returns:
            bool: True if started successfully, False otherwise
        """
        if not self.enabled:
            self.logger.warning("CRONOS is disabled in the settings")
            return False

        if self.is_running:
            self.logger.warning("CRONOS is already running")
            return False

        self.logger.info("Starting CRONOS subsystem")

        # Check need for initial backup
        self._check_initial_backup()

        # Configure schedules (simulated for this example)
        self._schedule_backups()

        self.is_running = True
        self.logger.info("CRONOS started successfully")
        return True

    def stop(self) -> bool:
        """
        Stops the CRONOS subsystem.

        Returns:
            bool: True if stopped successfully, False otherwise
        """
        if not self.is_running:
            self.logger.warning("CRONOS is not running")
            return False

        self.logger.info("Stopping CRONOS subsystem")

        # Cancel pending schedules
        self._cancel_scheduled_backups()

        # Save version history
        self._save_version_history()

        self.is_running = False
        self.logger.info("CRONOS stopped successfully")
        return True

    def _load_version_history(self) -> Dict[str, Any]:
        """
        Loads the version history from the file

        Returns:
            Dict: Version history
        """
        if not self.version_history_file.exists():
            return {
                "last_updated": datetime.datetime.now().isoformat(),
                "versions": []
            }

        try:
            with open(self.version_history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            self.logger.info(f"Version history loaded: {len(history.get('versions', []))} versions found")
            return history
        except Exception as e:
            self.logger.error(f"Error loading version history: {str(e)}")
            return {
                "last_updated": datetime.datetime.now().isoformat(),
                "versions": []
            }

    def _save_version_history(self) -> None:
        """Saves the version history to a file"""
        try:
            self.version_history["last_updated"] = datetime.datetime.now().isoformat()

            with open(self.version_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.version_history, f, indent=2, default=str)

            self.logger.info("Version history saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving version history: {str(e)}")

    def _calculate_total_preserved_size(self) -> int:
        """
        Calculates the total size of stored backups

        Returns:
            int: Total size in bytes
        """
        total_size = 0
        for version in self.version_history.get("versions", []):
            backup_path = self.backup_dir / version.get("filename", "")
            if backup_path.exists():
                total_size += backup_path.stat().st_size

        return total_size

    def _update_metrics(self) -> None:
        """Updates the subsystem metrics"""
        versions = self.version_history.get("versions", [])
        total_backups = len(versions)

        if total_backups > 0:
            # Calculate total preserved size
            total_size = self._calculate_total_preserved_size()

            # Calculate average size
            average_size = total_size / total_backups

            # Get last backup duration
            if versions:
                last_backup = versions[0]  # Assuming the list is ordered by most recent
                last_duration = last_backup.get("duration_seconds", 0)
            else:
                last_duration = 0

            # Calculate compression ratio (if available)
            compression_ratio = 0.0
            compressed_versions = [v for v in versions if v.get("original_size_bytes") and v.get("compressed_size_bytes")]
            if compressed_versions:
                total_original = sum(v.get("original_size_bytes", 0) for v in compressed_versions)
                total_compressed = sum(v.get("compressed_size_bytes", 0) for v in compressed_versions)
                if total_original > 0:
                    compression_ratio = 1 - (total_compressed / total_original)

            # Update metrics
            self.metrics = {
                "total_backups": total_backups,
                "total_preserved_size_bytes": total_size,
                "last_backup_duration_seconds": last_duration,
                "average_backup_size_bytes": average_size,
                "compression_ratio": compression_ratio
            }

            self.logger.info(f"Metrics updated: {total_backups} backups, {total_size / (1024*1024):.2f} MB total")

    def _check_initial_backup(self) -> None:
        """Checks if an initial backup is necessary"""
        versions = self.version_history.get("versions", [])

        if not versions:
            self.logger.info("No backup found. Performing initial system backup.")
            self.create_backup("Initial system backup")
        else:
            last_backup_time = None
            try:
                last_backup_time = datetime.datetime.fromisoformat(versions[0].get("timestamp", ""))
            except (ValueError, TypeError):
                last_backup_time = None

            if last_backup_time:
                now = datetime.datetime.now()
                hours_since_last_backup = (now - last_backup_time).total_seconds() / 3600

                if hours_since_last_backup > self.backup_interval_hours:
                    self.logger.info(f"Last backup was {hours_since_last_backup:.1f} hours ago. Performing automatic backup.")
                    self.create_backup("Automatic backup after interval")
                else:
                    self.logger.info(f"Recent backup found ({hours_since_last_backup:.1f}h ago). No initial backup needed.")
            else:
                self.logger.warning("Could not determine when the last backup was. Performing backup as a precaution.")
                self.create_backup("Precautionary backup - invalid timestamp")

    def _schedule_backups(self) -> None:
        """
        Schedules automatic backups based on the configured interval

        Note: In a real implementation, this would use a scheduler like APScheduler.
        For this example, we only simulate scheduling.
        """
        self.logger.info(f"Scheduling automatic backups every {self.backup_interval_hours} hours")

        # In a real system, a job would be configured in the scheduler here
        # For now, we only register the intention
        next_backup_time = datetime.datetime.now() + datetime.timedelta(hours=self.backup_interval_hours)
        self.scheduled_backups.append({
            "description": "Scheduled automatic backup",
            "scheduled_time": next_backup_time
        })

        self.logger.info(f"Next automatic backup scheduled for: {next_backup_time}")

    def _cancel_scheduled_backups(self) -> None:
        """Cancels all scheduled backups"""
        count = len(self.scheduled_backups)
        self.scheduled_backups = []
        self.logger.info(f"{count} scheduled backups have been canceled")

    def create_backup(self, description: str = "", include_modules: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Creates a backup of the system or specific modules

        Args:
            description: Description of the backup
            include_modules: List of modules to include (None for all)

        Returns:
            Dict: Information about the created backup
        """
        start_time = time.time()
        self.logger.info(f"Starting backup process: {description}")

        # Generate unique name for the backup
        timestamp = datetime.datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp_str}"

        # In a real implementation, the physical backup of files would be done here
        # For this example, we simulate the process

        # 1. Determine what will be included in the backup
        backup_modules = include_modules or ["core", "modules", "integrations", "tools", "data"]
        if not self.include_logs and "data/logs" not in backup_modules:
            backup_modules = [m for m in backup_modules if m != "data/logs"]

        self.logger.info(f"Backup will include: {', '.join(backup_modules)}")

        # 2. Simulate file collection for backup
        collected_files = self._simulate_file_collection(backup_modules)
        file_count = len(collected_files)
        total_size = sum(f.get("size", 0) for f in collected_files)

        self.logger.info(f"Collected {file_count} files totaling {total_size / (1024*1024):.2f} MB")

        # 3. Simulate compression
        compressed_size = int(total_size * (0.9 - (self.compression_level * 0.05)))  # Compression simulation

        self.logger.info(f"Compression applied: {total_size / (1024*1024):.2f} MB → {compressed_size / (1024*1024):.2f} MB")

        # 4. Simulate backup
        backup_path = self.backup_dir / f"{backup_name}.zip"  # In practice, this would be a real file

        # Simulate a delay due to the backup process
        # time.sleep(2)  # Uncomment in production would cause a real delay

        # 5. Register the backup in the history
        end_time = time.time()
        duration = end_time - start_time

        backup_info = {
            "version": self.config.get("version", "8.0.0"),
            "timestamp": timestamp.isoformat(),
            "description": description,
            "filename": f"{backup_name}.zip",
            "file_count": file_count,
            "original_size_bytes": total_size,
            "compressed_size_bytes": compressed_size,
            "modules_included": backup_modules,
            "duration_seconds": duration,
            "compression_level": self.compression_level
        }

        # Add to history (at the beginning of the list to keep ordered by most recent)
        versions = self.version_history.get("versions", [])
        versions.insert(0, backup_info)

        # Limit number of versions kept
        if len(versions) > self.versions_to_keep:
            removed_versions = versions[self.versions_to_keep:]
            versions = versions[:self.versions_to_keep]

            # In production, here would remove physical files of old backups
            for version in removed_versions:
                old_file = self.backup_dir / version.get("filename", "")
                self.logger.info(f"Removing old backup: {old_file}")
                # old_file.unlink(missing_ok=True)  # Uncomment in production

        self.version_history["versions"] = versions
        self._save_version_history()

        # Update metrics
        self._update_metrics()

        self.logger.info(f"Backup '{backup_name}' completed in {duration:.2f} seconds")

        return backup_info

    def _simulate_file_collection(self, modules: List[str]) -> List[Dict[str, Any]]:
        """
        Simulates file collection for backup

        Args:
            modules: List of modules to include

        Returns:
            List: List of dictionaries with file information
        """
        # This is a simulation - in production, a real file scan would be done
        simulated_files = []

        # Simulate files for each module
        for module in modules:
            # Simulated number of files per module
            file_count = {
                "core": 50,
                "modules": 100,
                "integrations": 200,
                "tools": 30,
                "data": 500,
                "data/logs": 300
            }.get(module, 20)

            # Simulated average size per file (in bytes)
            avg_size = {
                "core": 20_000,
                "modules": 15_000,
                "integrations": 30_000,
                "tools": 25_000,
                "data": 100_000,
                "data/logs": 500_000
            }.get(module, 10_000)

            # Create simulated files
            for i in range(file_count):
                # Vary size to be more realistic
                import random
                size_variation = random.uniform(0.5, 2.0)
                file_size = int(avg_size * size_variation)

                file_info = {
                    "path": f"{module}/file_{i}.py",
                    "size": file_size,
                    "last_modified": datetime.datetime.now().isoformat()
                }
                simulated_files.append(file_info)

        return simulated_files

    def restore_backup(self, version_id: Optional[str] = None,
                      target_modules: Optional[List[str]] = None,
                      target_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Restores a specific backup

        Args:
            version_id: ID of the version to restore (None to use the most recent)
            target_modules: List of modules to restore (None for all)
            target_dir: Target directory for restoration (None to use the original directory)

        Returns:
            Dict: Result of the restoration operation
        """
        self.logger.info(f"Starting backup restoration process")

        # Get the backup version
        versions = self.version_history.get("versions", [])

        if not versions:
            self.logger.error("No backup available for restoration")
            return {"success": False, "error": "No backup available"}

        target_version = None
        if version_id:
            # Search for the specific version
            target_version = next((v for v in versions
                                if v.get("filename", "").split(".")[0] == version_id
                                or v.get("timestamp") == version_id), None)

            if not target_version:
                self.logger.error(f"Version '{version_id}' not found")
                return {"success": False, "error": f"Version '{version_id}' not found"}
        else:
            # Use the most recent version
            target_version = versions[0]

        backup_file = self.backup_dir / target_version.get("filename", "")
        if not os.path.exists(backup_file):
            self.logger.error(f"Backup file not found: {backup_file}")
            return {"success": False, "error": f"Backup file not found: {backup_file}"}

        # Define target modules
        modules_to_restore = target_modules or target_version.get("modules_included", [])

        self.logger.info(f"Restoring backup {target_version.get('filename')} from {target_version.get('timestamp')}")
        self.logger.info(f"Modules to restore: {', '.join(modules_to_restore)}")

        # Define target directory
        restore_dir = target_dir or self.system_root

        # In production, the real restoration of files would be done here
        # For this example, we only simulate

        # Simulate restoration process
        start_time = time.time()

        # Simulate decompression
        # time.sleep(1)  # Uncomment in production would cause a real delay

        # Simulate file restoration
        file_count = target_version.get("file_count", 0)
        restored_modules = []
        for module in modules_to_restore:
            # time.sleep(0.5)  # Uncomment in production
            restored_modules.append(module)
            self.logger.info(f"Restored module: {module}")

        end_time = time.time()
        duration = end_time - start_time

        self.logger.info(f"Restoration completed in {duration:.2f} seconds. {file_count} files restored.")

        result = {
            "success": True,
            "version": target_version.get("version"),
            "backup_timestamp": target_version.get("timestamp"),
            "restored_modules": restored_modules,
            "file_count": file_count,
            "duration_seconds": duration,
            "target_directory": str(restore_dir)
        }

        return result

    def list_backups(self) -> List[Dict[str, Any]]:
        """
        Lists all available backups
