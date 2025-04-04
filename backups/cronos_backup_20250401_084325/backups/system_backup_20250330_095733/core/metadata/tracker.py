import os
import time
from typing import Dict, List, Set, Optional
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .scanner import MetadataScanner, FileMetadata
import logging


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, tracker):
        self.tracker = tracker

    def on_modified(self, event):
        if not event.is_directory:
            self.tracker._record_access(event.src_path, "modified")

    def on_accessed(self, event):
        if not event.is_directory:
            self.tracker._record_access(event.src_path, "accessed")


class UsageTracker:
    def __init__(self, scanner: MetadataScanner):
        self.scanner = scanner
        self.access_log: List[Dict[str, any]] = []
        self.dependency_cache: Dict[str, Set[str]] = {}
        self.observer = Observer()
        self.event_handler = FileEventHandler(self)
        self.active_watchers: Dict[str, Observer] = {}
        self.event_callbacks: List[callable] = []

    def register_event_callback(self, callback: callable) -> None:
        """Register a callback for file events."""
        self.event_callbacks.append(callback)

    def _notify_callbacks(
        self, event_type: str, file_path: str, event_data: Dict[str, Any]
    ) -> None:
        """Notify all registered callbacks of an event."""
        for callback in self.event_callbacks:
            try:
                callback(event_type, file_path, event_data)
            except Exception as e:
                logging.error(f"Error in event callback: {str(e)}")

    def start_tracking(self, root_dir: str) -> None:
        """Start tracking file usage in the specified directory."""
        print(f"Starting file usage tracking in {root_dir}")

        # Start watchdog observer
        self.observer.schedule(self.event_handler, root_dir, recursive=True)
        self.observer.start()

        try:
            while True:
                # Update dependency cache periodically
                self._update_dependency_cache()
                # Sleep for a while before next update
                time.sleep(300)  # 5 minutes
        except KeyboardInterrupt:
            self.stop_tracking()

    def stop_tracking(self) -> None:
        """Stop tracking file usage."""
        self.observer.stop()
        self.observer.join()
        self._save_access_log()

    def _record_access(self, filepath: str, access_type: str) -> None:
        """Record a file access event."""
        if filepath not in self.scanner.metadata_db:
            return

        metadata = self.scanner.metadata_db[filepath]

        # Update last accessed time in metadata
        if access_type == "accessed":
            metadata.last_accessed = datetime.now()
        elif access_type == "modified":
            metadata.modified = datetime.now()

        # Create event data
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "file": filepath,
            "type": access_type,
            "subsystem": metadata.subsystem,
            "purpose": metadata.purpose,
        }

        # Record access event
        self.access_log.append(event_data)

        # Notify callbacks
        self._notify_callbacks(access_type, filepath, event_data)

        # Update dependency cache if file was modified
        if access_type == "modified":
            self._update_file_dependencies(filepath)

    def _update_dependency_cache(self) -> None:
        """Update the dependency cache for all files."""
        for filepath in self.scanner.metadata_db:
            self._update_file_dependencies(filepath)

    def _update_file_dependencies(self, filepath: str) -> None:
        """Update dependency information for a specific file."""
        metadata = self.scanner.metadata_db.get(filepath)
        if not metadata:
            return

        # Get current dependencies
        current_deps = set(metadata.dependencies)

        # Get new dependencies from scanner
        new_deps = self.scanner._extract_imports(filepath)
        resolved_deps = set()

        # Resolve import paths to actual files
        for imp in new_deps:
            for path in self.scanner.metadata_db:
                if (
                    path.endswith(f"{imp.replace('.', '/')}.py")
                    or path.endswith(f"{imp.replace('.', '/')}.js")
                    or path.endswith(f"{imp.replace('.', '/')}.ts")
                ):
                    resolved_deps.add(path)

        # Update dependency cache
        self.dependency_cache[filepath] = resolved_deps

        # Check for changes in dependencies
        added_deps = resolved_deps - current_deps
        removed_deps = current_deps - resolved_deps

        if added_deps or removed_deps:
            # Record dependency changes
            self.access_log.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "file": filepath,
                    "type": "dependency_change",
                    "added_dependencies": list(added_deps),
                    "removed_dependencies": list(removed_deps),
                }
            )

            # Update metadata
            metadata.dependencies = list(resolved_deps)

    def get_usage_stats(self, days: int = 30) -> Dict[str, any]:
        """Get usage statistics for the specified time period."""
        cutoff = datetime.now() - timedelta(days=days)
        recent_logs = [
            log for log in self.access_log if datetime.fromisoformat(log["timestamp"]) > cutoff
        ]

        stats = {
            "total_accesses": len(recent_logs),
            "files_accessed": set(),
            "files_modified": set(),
            "subsystem_activity": {},
            "purpose_activity": {},
            "dependency_changes": 0,
        }

        for log in recent_logs:
            if log["type"] == "accessed":
                stats["files_accessed"].add(log["file"])
            elif log["type"] == "modified":
                stats["files_modified"].add(log["file"])
            elif log["type"] == "dependency_change":
                stats["dependency_changes"] += 1

            # Track subsystem activity
            if log["subsystem"]:
                if log["subsystem"] not in stats["subsystem_activity"]:
                    stats["subsystem_activity"][log["subsystem"]] = 0
                stats["subsystem_activity"][log["subsystem"]] += 1

            # Track purpose activity
            if log["purpose"]:
                if log["purpose"] not in stats["purpose_activity"]:
                    stats["purpose_activity"][log["purpose"]] = 0
                stats["purpose_activity"][log["purpose"]] += 1

        # Convert sets to counts
        stats["unique_files_accessed"] = len(stats["files_accessed"])
        stats["unique_files_modified"] = len(stats["files_modified"])
        del stats["files_accessed"]
        del stats["files_modified"]

        return stats

    def get_file_usage_history(self, filepath: str) -> List[Dict[str, any]]:
        """Get usage history for a specific file."""
        return [log for log in self.access_log if log["file"] == filepath]

    def get_active_files(self, days: int = 30) -> List[Dict[str, any]]:
        """Get list of recently active files."""
        cutoff = datetime.now() - timedelta(days=days)
        active_files = {}

        for log in self.access_log:
            if datetime.fromisoformat(log["timestamp"]) > cutoff:
                filepath = log["file"]
                if filepath not in active_files:
                    active_files[filepath] = {
                        "file": filepath,
                        "access_count": 0,
                        "modification_count": 0,
                        "dependency_changes": 0,
                        "last_activity": None,
                    }

                stats = active_files[filepath]
                timestamp = datetime.fromisoformat(log["timestamp"])

                if not stats["last_activity"] or timestamp > stats["last_activity"]:
                    stats["last_activity"] = timestamp

                if log["type"] == "accessed":
                    stats["access_count"] += 1
                elif log["type"] == "modified":
                    stats["modification_count"] += 1
                elif log["type"] == "dependency_change":
                    stats["dependency_changes"] += 1

        return list(active_files.values())

    def get_dependency_changes(self, days: int = 30) -> List[Dict[str, any]]:
        """Get list of recent dependency changes."""
        cutoff = datetime.now() - timedelta(days=days)
        return [
            log
            for log in self.access_log
            if log["type"] == "dependency_change"
            and datetime.fromisoformat(log["timestamp"]) > cutoff
        ]

    def _save_access_log(self) -> None:
        """Save access log to a JSON file."""
        import json

        output = {"last_update": datetime.now().isoformat(), "access_log": self.access_log}

        with open("access_log.json", "w") as f:
            json.dump(output, f, indent=2)

    def get_replacement_suggestions(self) -> List[Dict[str, any]]:
        """Get suggestions for file replacements based on usage patterns."""
        suggestions = []

        # Get files with similar names
        for filepath, metadata in self.scanner.metadata_db.items():
            name_base = os.path.splitext(metadata.name)[0]
            similar_files = [
                other_path
                for other_path, other_meta in self.scanner.metadata_db.items()
                if filepath != other_path and name_base in other_meta.name
            ]

            if similar_files:
                # Get usage stats for each file
                file_stats = {}
                for path in [filepath] + similar_files:
                    history = self.get_file_usage_history(path)
                    recent_history = [
                        log
                        for log in history
                        if datetime.fromisoformat(log["timestamp"])
                        > (datetime.now() - timedelta(days=30))
                    ]

                    file_stats[path] = {
                        "access_count": len(
                            [log for log in recent_history if log["type"] == "accessed"]
                        ),
                        "modification_count": len(
                            [log for log in recent_history if log["type"] == "modified"]
                        ),
                        "last_activity": (
                            max(
                                [datetime.fromisoformat(log["timestamp"]) for log in recent_history]
                            )
                            if recent_history
                            else None
                        ),
                    }

                # Compare usage patterns
                main_stats = file_stats[filepath]
                for similar_path in similar_files:
                    similar_stats = file_stats[similar_path]

                    # If similar file is more active
                    if (
                        similar_stats["access_count"] > main_stats["access_count"] * 2
                        or similar_stats["modification_count"]
                        > main_stats["modification_count"] * 2
                    ):
                        suggestions.append(
                            {
                                "old_file": filepath,
                                "new_file": similar_path,
                                "reason": "Similar file with higher usage detected",
                                "stats": {"old_file": main_stats, "new_file": similar_stats},
                            }
                        )

        return suggestions
