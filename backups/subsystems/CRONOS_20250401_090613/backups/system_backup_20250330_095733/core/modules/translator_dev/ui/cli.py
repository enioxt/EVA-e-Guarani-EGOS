#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command Line Interface for EVA & GUARANI Translator.

This module provides CLI functions for the translator, including progress display,
statistics, and logging setup.
"""

import os
import sys
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    from rich.console import Console
    from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
    from rich.table import Table

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class Session:
    """Manages translation sessions, tracking progress and files."""

    def __init__(self, session_dir: Optional[str] = None):
        """Initialize a new session or load an existing one."""
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = session_dir or os.path.join("data", "sessions")
        os.makedirs(self.session_dir, exist_ok=True)

        self.session_file = os.path.join(self.session_dir, f"session_{self.session_id}.json")
        self.status = {
            "start_time": time.time(),
            "end_time": None,
            "files_total": 0,
            "files_processed": 0,
            "files_skipped": 0,
            "files_pending": [],
            "files_completed": [],
            "files_failed": [],
        }

    def add_files(self, file_list: List[str]) -> None:
        """Add files to the session."""
        self.status["files_total"] += len(file_list)
        self.status["files_pending"].extend(file_list)
        self._save_session()

    def mark_file_completed(self, file_path: str) -> None:
        """Mark a file as successfully processed."""
        if file_path in self.status["files_pending"]:
            self.status["files_pending"].remove(file_path)
        self.status["files_completed"].append(file_path)
        self.status["files_processed"] += 1
        self._save_session()

    def mark_file_failed(self, file_path: str) -> None:
        """Mark a file as failed during processing."""
        if file_path in self.status["files_pending"]:
            self.status["files_pending"].remove(file_path)
        self.status["files_failed"].append(file_path)
        self.status["files_processed"] += 1
        self._save_session()

    def mark_file_skipped(self, file_path: str) -> None:
        """Mark a file as skipped during processing."""
        if file_path in self.status["files_pending"]:
            self.status["files_pending"].remove(file_path)
        self.status["files_skipped"] += 1
        self._save_session()

    def complete_session(self) -> None:
        """Mark the session as completed."""
        self.status["end_time"] = time.time()
        self._save_session()

    def _save_session(self) -> None:
        """Save the session status to disk."""
        import json

        with open(self.session_file, "w", encoding="utf-8") as f:
            json.dump(self.status, f, indent=2)

    @classmethod
    def load_most_recent(cls) -> "Session":
        """Load the most recent session if available."""
        session_dir = os.path.join("data", "sessions")
        if not os.path.exists(session_dir):
            return cls()

        session_files = [
            f for f in os.listdir(session_dir) if f.startswith("session_") and f.endswith(".json")
        ]
        if not session_files:
            return cls()

        # Sort by modification time
        session_files.sort(
            key=lambda x: os.path.getmtime(os.path.join(session_dir, x)), reverse=True
        )
        most_recent = session_files[0]

        # Load the session
        session = cls()
        import json

        with open(os.path.join(session_dir, most_recent), "r", encoding="utf-8") as f:
            session.status = json.load(f)
        session.session_file = os.path.join(session_dir, most_recent)
        session.session_id = most_recent.replace("session_", "").replace(".json", "")

        return session


def setup_logging(level: int = logging.INFO) -> None:
    """Setup logging configuration."""
    log_dir = os.path.join("data", "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"translator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8", mode="w"),
        ],
    )


def display_progress(title: str, total: int, completed: int) -> None:
    """Display progress bar for translation."""
    if RICH_AVAILABLE:
        console = Console()
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(title, total=total)
            progress.update(task, completed=completed)
    else:
        # Fallback to simple progress display
        percentage = (completed / total) * 100 if total > 0 else 0
        bar_length = 30
        filled_length = int(bar_length * completed // total)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        print(f"\r{title}: [{bar}] {percentage:.1f}% ({completed}/{total})", end="")
        if completed == total:
            print()


def display_stats(config: Any) -> None:
    """Display translation statistics."""
    # Load cache to get stats
    cache_dir = os.path.join("data", "cache")
    if not os.path.exists(cache_dir):
        print("No statistics available (cache directory not found).")
        return

    cache_files = [f for f in os.listdir(cache_dir) if f.endswith(".json")]
    if not cache_files:
        print("No statistics available (no cache files found).")
        return

    # Basic stats
    total_files = len(cache_files)
    total_chars = 0
    total_translations = 0

    # Load each cache file to get more detailed stats
    import json

    for cache_file in cache_files:
        try:
            with open(os.path.join(cache_dir, cache_file), "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                total_translations += len(cache_data)
                for key, value in cache_data.items():
                    total_chars += len(key)
        except Exception as e:
            logging.error(f"Error loading cache file {cache_file}: {e}")

    # Display stats
    if RICH_AVAILABLE:
        console = Console()
        table = Table(title="EVA & GUARANI Translator Statistics")

        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Cached Files", str(total_files))
        table.add_row("Total Translations", str(total_translations))
        table.add_row("Total Characters", str(total_chars))

        console.print(table)
    else:
        print("\nEVA & GUARANI Translator Statistics")
        print("================================")
        print(f"Total Cached Files: {total_files}")
        print(f"Total Translations: {total_translations}")
        print(f"Total Characters: {total_chars}")
