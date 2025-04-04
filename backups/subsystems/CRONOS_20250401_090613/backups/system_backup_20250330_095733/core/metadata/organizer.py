import os
import shutil
from typing import Dict, List, Optional
from datetime import datetime
from .scanner import MetadataScanner, FileMetadata


class FileOrganizer:
    def __init__(self, scanner: MetadataScanner):
        self.scanner = scanner
        self.move_history: List[Dict[str, str]] = []
        self.location_rules = {
            "core": {
                "base_path": "core/",
                "subdirs": {
                    "system": "system/",
                    "service": "services/",
                    "model": "models/",
                    "test": "tests/",
                },
            },
            "web": {
                "base_path": "web/",
                "subdirs": {
                    "interface": "components/",
                    "client": "js/",
                    "style": "css/",
                    "test": "tests/",
                },
            },
            "quantum_prompts": {
                "base_path": "QUANTUM_PROMPTS/",
                "subdirs": {"documentation": "docs/", "configuration": "config/"},
            },
        }

    def organize_files(self, dry_run: bool = True) -> List[Dict[str, str]]:
        """Organize files based on metadata analysis."""
        moves = []

        # Get misplaced files
        misplaced = self.scanner.get_misplaced_files()
        for item in misplaced:
            new_location = self._get_suggested_location(item["file"], item["suggested_subsystem"])
            if new_location:
                moves.append(
                    {"file": item["file"], "destination": new_location, "reason": item["reason"]}
                )

        # Handle inactive files
        inactive = self.scanner.get_inactive_files()
        for item in inactive:
            archive_location = self._get_archive_location(item["file"])
            if archive_location:
                moves.append(
                    {
                        "file": item["file"],
                        "destination": archive_location,
                        "reason": f"File inactive for {item['days_inactive']} days",
                    }
                )

        # Handle replacement candidates
        replacements = self.scanner.get_replacement_candidates()
        for item in replacements:
            archive_location = self._get_archive_location(item["old_file"])
            if archive_location:
                moves.append(
                    {
                        "file": item["old_file"],
                        "destination": archive_location,
                        "reason": item["reason"],
                    }
                )

        if not dry_run:
            self._execute_moves(moves)

        return moves

    def _get_suggested_location(self, filepath: str, subsystem: str) -> Optional[str]:
        """Get suggested location for a file based on its metadata."""
        if subsystem not in self.location_rules:
            return None

        metadata = self.scanner.metadata_db.get(filepath)
        if not metadata:
            return None

        rules = self.location_rules[subsystem]
        base_path = rules["base_path"]

        # Determine appropriate subdirectory
        subdir = ""
        if metadata.purpose in rules["subdirs"]:
            subdir = rules["subdirs"][metadata.purpose]

        # Construct new path
        new_location = os.path.join(base_path, subdir, metadata.name)

        # Ensure we don't overwrite existing files
        if os.path.exists(new_location):
            base, ext = os.path.splitext(new_location)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_location = f"{base}_{timestamp}{ext}"

        return new_location

    def _get_archive_location(self, filepath: str) -> Optional[str]:
        """Get archive location for an inactive or replaced file."""
        metadata = self.scanner.metadata_db.get(filepath)
        if not metadata:
            return None

        archive_base = "archive"
        if not os.path.exists(archive_base):
            os.makedirs(archive_base)

        # Create archive structure by year/month
        timestamp = metadata.last_accessed
        year_month = timestamp.strftime("%Y/%m")
        archive_path = os.path.join(archive_base, year_month)

        if not os.path.exists(archive_path):
            os.makedirs(archive_path)

        # Add timestamp to filename to prevent conflicts
        base, ext = os.path.splitext(metadata.name)
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        archive_name = f"{base}_{timestamp_str}{ext}"

        return os.path.join(archive_path, archive_name)

    def _execute_moves(self, moves: List[Dict[str, str]]) -> None:
        """Execute the file moves."""
        for move in moves:
            src = move["file"]
            dst = move["destination"]

            try:
                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dst), exist_ok=True)

                # Move the file
                shutil.move(src, dst)

                # Record the move
                self.move_history.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "source": src,
                        "destination": dst,
                        "reason": move["reason"],
                    }
                )

                print(f"Moved {src} to {dst}")

            except Exception as e:
                print(f"Error moving {src} to {dst}: {str(e)}")

    def save_move_history(self) -> None:
        """Save move history to a JSON file."""
        import json

        output = {"last_organization": datetime.now().isoformat(), "moves": self.move_history}

        with open("move_history.json", "w") as f:
            json.dump(output, f, indent=2)

    def restore_file(self, archived_path: str) -> Optional[str]:
        """Restore a file from the archive to its original location."""
        if not os.path.exists(archived_path):
            return None

        # Extract original filename without timestamp
        filename = os.path.basename(archived_path)
        base, ext = os.path.splitext(filename)
        original_name = base.split("_")[0] + ext

        # Find the last known location from move history
        original_location = None
        for move in reversed(self.move_history):
            if os.path.basename(move["source"]) == original_name:
                original_location = move["source"]
                break

        if not original_location:
            return None

        try:
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(original_location), exist_ok=True)

            # Move file back to original location
            shutil.move(archived_path, original_location)

            # Record the restoration
            self.move_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "source": archived_path,
                    "destination": original_location,
                    "reason": "File restored from archive",
                }
            )

            print(f"Restored {archived_path} to {original_location}")
            return original_location

        except Exception as e:
            print(f"Error restoring {archived_path}: {str(e)}")
            return None

    def get_organization_report(self) -> Dict[str, any]:
        """Generate a report of the current file organization state."""
        total_files = len(self.scanner.metadata_db)
        misplaced = len(self.scanner.get_misplaced_files())
        inactive = len(self.scanner.get_inactive_files())
        replacements = len(self.scanner.get_replacement_candidates())

        subsystem_stats = {}
        for filepath, metadata in self.scanner.metadata_db.items():
            if metadata.subsystem:
                if metadata.subsystem not in subsystem_stats:
                    subsystem_stats[metadata.subsystem] = {
                        "total_files": 0,
                        "active_files": 0,
                        "quantum_metrics": {"consciousness": 0.0, "harmony": 0.0, "evolution": 0.0},
                    }

                stats = subsystem_stats[metadata.subsystem]
                stats["total_files"] += 1
                if metadata.is_active:
                    stats["active_files"] += 1

                # Update quantum metrics
                for metric, value in metadata.quantum_metrics.items():
                    stats["quantum_metrics"][metric] += value

        # Calculate averages for quantum metrics
        for stats in subsystem_stats.values():
            if stats["total_files"] > 0:
                for metric in stats["quantum_metrics"]:
                    stats["quantum_metrics"][metric] /= stats["total_files"]

        return {
            "timestamp": datetime.now().isoformat(),
            "total_files": total_files,
            "misplaced_files": misplaced,
            "inactive_files": inactive,
            "replacement_candidates": replacements,
            "subsystem_stats": subsystem_stats,
            "recent_moves": self.move_history[-10:] if self.move_history else [],
        }
