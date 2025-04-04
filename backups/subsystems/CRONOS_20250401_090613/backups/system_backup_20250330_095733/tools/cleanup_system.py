import os
import shutil
import json
from datetime import datetime
import sys
from pathlib import Path

# Add core to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core.metadata.scanner import MetadataScanner
from core.metadata.tracker import UsageTracker
from core.metadata.organizer import FileOrganizer
from core.metadata.ml.analyzer import MetadataAnalyzer


class SystemCleanup:
    def __init__(self):
        self.scanner = MetadataScanner()
        self.tracker = UsageTracker(self.scanner)
        self.organizer = FileOrganizer(self.scanner)
        self.analyzer = MetadataAnalyzer(self.scanner, self.tracker, self.organizer)

        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.quarantine_dir = os.path.join(self.root_dir, "quarantine")

        # Ensure quarantine directory exists
        os.makedirs(self.quarantine_dir, exist_ok=True)

    def analyze_duplicates(self):
        """Find duplicate files in the system."""
        print("Analyzing duplicates...")
        duplicates = self.analyzer.find_duplicates()

        # Save analysis results
        with open(os.path.join(self.root_dir, "cleanup_analysis.json"), "w") as f:
            json.dump(
                {"timestamp": datetime.now().isoformat(), "duplicates": duplicates}, f, indent=2
            )

        return duplicates

    def organize_files(self):
        """Organize files based on metadata analysis."""
        print("Organizing files...")

        # Get organization suggestions
        suggestions = self.organizer.suggest_locations()

        # Apply suggestions
        for suggestion in suggestions:
            if suggestion["confidence"] > 0.8:  # Only apply high-confidence suggestions
                src = suggestion["current_path"]
                dst = suggestion["suggested_path"]

                if os.path.exists(src):
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.move(src, dst)
                    print(f"Moved: {src} -> {dst}")

    def clean_directories(self):
        """Clean up empty directories and temporary files."""
        print("Cleaning directories...")

        # Extensions to clean
        temp_extensions = {".tmp", ".temp", ".log", ".bak", ".cache"}

        for root, dirs, files in os.walk(self.root_dir, topdown=False):
            # Remove temporary files
            for file in files:
                if any(file.endswith(ext) for ext in temp_extensions):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Removed temporary file: {file_path}")

            # Remove empty directories
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                    print(f"Removed empty directory: {dir_path}")
                except OSError:
                    pass  # Directory not empty

    def quarantine_outdated(self):
        """Move outdated files to quarantine."""
        print("Identifying outdated files...")

        # Get outdated files from analyzer
        outdated = self.analyzer.find_outdated_files()

        # Move to quarantine
        for file in outdated:
            if os.path.exists(file["path"]):
                rel_path = os.path.relpath(file["path"], self.root_dir)
                dst = os.path.join(self.quarantine_dir, rel_path)

                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(file["path"], dst)
                print(f"Quarantined outdated file: {rel_path}")

    def optimize_structure(self):
        """Optimize the directory structure based on ML analysis."""
        print("Optimizing directory structure...")

        # Get optimization suggestions
        optimizations = self.analyzer.suggest_optimizations()

        # Apply structural optimizations
        for opt in optimizations:
            if opt["type"] == "structure_optimization" and opt["confidence"] > 0.8:
                if os.path.exists(opt["source"]):
                    os.makedirs(os.path.dirname(opt["target"]), exist_ok=True)
                    shutil.move(opt["source"], opt["target"])
                    print(f"Optimized structure: {opt['source']} -> {opt['target']}")

    def run(self):
        """Run the cleanup process."""
        print("Starting system cleanup process...")

        # Scan system first
        self.scanner.scan_system(self.root_dir)

        # Run cleanup steps
        self.analyze_duplicates()
        self.organize_files()
        self.clean_directories()
        self.quarantine_outdated()
        self.optimize_structure()

        print("Cleanup process completed!")


if __name__ == "__main__":
    cleanup = SystemCleanup()
    cleanup.run()
