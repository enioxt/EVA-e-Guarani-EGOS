#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EVA & GUARANI Translator - Command Line Interface
This module provides a CLI for the translator tools.
"""

import os
import sys
import time
import logging
import argparse
import json
import shutil
import datetime
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, SpinnerColumn, TimeElapsedColumn, TaskProgressColumn
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm
from rich import print as rprint
from rich.logging import RichHandler
from rich.style import Style
from rich.theme import Theme

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.translator_dev.core.processor import TranslationProcessor
from modules.translator_dev.config.config import ConfigManager
from modules.translator_dev.core.scanner import FileScanner, ScanResult

# Custom theme for a cleaner and more professional look
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "progress.bar.finished": "green",
    "progress.bar.pulse": "cyan",
})

# Setup console for rich output
console = Console(theme=custom_theme, highlight=False)

# Configure logging - significantly reduce verbosity for cleaner output
logging.basicConfig(
    level=logging.WARNING,  # Changed from INFO to WARNING to reduce noise
    format="%(message)s",
    handlers=[
        logging.FileHandler("translator.log", mode="a", encoding="utf-8"),
    ]
)

# Create a separate logger for CLI that won't show in console
cli_logger = logging.getLogger("cli")
cli_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("translator.log", mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
cli_logger.addHandler(file_handler)

# Additional config for core loggers to reduce output
for logger_name in ["translator", "processor", "scanner", "cache", "huggingface", "openai"]:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.WARNING)  # Only show warnings and errors

class TranslatorCLI:
    """Command-line interface for the EVA & GUARANI Translator"""
    
    def __init__(self):
        """Initialize the CLI"""
        self.processor = None
        self.config_manager = ConfigManager()
        self.config = self.config_manager.config
        self.session_file = Path(self.config.cache.directory) / "session.pickle"
        self.session_data = {
            "pending_files": [],
            "completed_files": [],
            "skipped_files": [],
            "safe_files": [],  # Files marked as safe (sensitive content)
            "start_time": None,
            "last_updated": None,
            "paused": False
        }
        self._load_session()
    
    def _load_session(self):
        """Load session data if exists"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'rb') as f:
                    loaded_data = pickle.load(f)
                    # Update session data with loaded values, but maintain structure
                    for key in loaded_data:
                        if key in self.session_data:
                            self.session_data[key] = loaded_data[key]
                cli_logger.info(f"Loaded session with {len(self.session_data['pending_files'])} pending files")
            except Exception as e:
                cli_logger.error(f"Error loading session: {str(e)}")
    
    def _save_session(self):
        """Save current session data"""
        try:
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            self.session_data["last_updated"] = datetime.datetime.now()
            with open(self.session_file, 'wb') as f:
                pickle.dump(self.session_data, f)
            cli_logger.info("Session saved")
        except Exception as e:
            cli_logger.error(f"Error saving session: {str(e)}")
    
    def _init_processor(self):
        """Initialize the translation processor"""
        if not self.processor:
            self.processor = TranslationProcessor()
    
    def _display_header(self):
        """Display EVA & GUARANI header"""
        console.print("\n[bold cyan]✧༺❀༻∞ EVA & GUARANI TRANSLATOR ∞༺❀༻✧[/bold cyan]", justify="center")
        console.print("[italic]Translating with precision, ethics, and unconditional love[/italic]\n", justify="center")
    
    def _display_stats(self, stats: Dict[str, Any], elapsed_time: Optional[float] = None):
        """Display translation statistics in a clean table"""
        table = Table(title="Translation Statistics", show_header=True, header_style="bold magenta", expand=False, width=60)
        
        table.add_column("Metric", style="dim")
        table.add_column("Value", style="cyan")
        
        # Add stats to table
        table.add_row("Files Processed", str(stats.get("files_processed", 0)))
        table.add_row("Files Skipped", str(stats.get("files_skipped", 0)))
        table.add_row("Safe Files (Not Modified)", str(len(self.session_data.get("safe_files", []))))
        table.add_row("Cache Hits", str(stats.get("cache_hits", 0)))
        
        # Process bytes
        bytes_processed = stats.get("bytes_processed", 0)
        if bytes_processed > 1048576:  # 1MB
            table.add_row("Data Processed", f"{bytes_processed / 1048576:.2f} MB")
        else:
            table.add_row("Data Processed", f"{bytes_processed / 1024:.2f} KB")
        
        # Calculate and add time stats
        actual_elapsed_time = elapsed_time if elapsed_time is not None else stats.get("elapsed_time", 0)
        
        if actual_elapsed_time > 60:
            table.add_row("Elapsed Time", f"{actual_elapsed_time / 60:.2f} minutes")
        else:
            table.add_row("Elapsed Time", f"{actual_elapsed_time:.2f} seconds")
        
        # Add speed stats
        if actual_elapsed_time > 0 and stats.get("files_processed", 0) > 0:
            files_per_second = stats.get("files_processed", 0) / actual_elapsed_time
            if files_per_second < 0.1:
                table.add_row("Speed", f"{files_per_second * 60:.2f} files/minute")
            else:
                table.add_row("Speed", f"{files_per_second:.2f} files/second")
        
        console.print(Panel(table, border_style="cyan"))
    
    def scan_directory(self, directory: Union[str, Path], output: Optional[str] = None):
        """Scan a directory for Portuguese files
        
        Args:
            directory: Directory to scan
            output: Output file for scan results (optional)
        """
        self._display_header()
        
        directory = Path(directory)
        
        if not directory.exists() or not directory.is_dir():
            console.print(f"[error]Directory not found: {directory}[/error]")
            return
        
        console.print(Panel(f"Scanning directory: {directory}", title="File Scanner", border_style="blue"))
        scanner = FileScanner(self.config.scanner)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(complete_style="progress.bar.finished"),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            scan_task = progress.add_task("Scanning files...", total=None)
            
            # Need to adapt scanner to provide progress updates
            results = scanner.scan_directory(directory)
            
            progress.update(scan_task, total=1, completed=1)
        
        if not results:
            console.print(Panel("[warning]No Portuguese files found in the directory.[/warning]", border_style="yellow"))
            return
        
        # Display results summary
        console.print(Panel(f"Found [bold]{len(results)}[/bold] files with Portuguese content", title="Scan Results", border_style="green"))
        
        # Show confidence distribution table
        confidence_levels = {
            "High (>0.8)": 0,
            "Medium (0.5-0.8)": 0,
            "Low (<0.5)": 0
        }
        
        for result in results:
            if result.confidence > 0.8:
                confidence_levels["High (>0.8)"] += 1
            elif result.confidence >= 0.5:
                confidence_levels["Medium (0.5-0.8)"] += 1
            else:
                confidence_levels["Low (<0.5)"] += 1
        
        table = Table(title="Confidence Distribution", show_header=True, expand=False)
        table.add_column("Confidence Level", style="dim")
        table.add_column("Files", style="cyan", justify="right")
        
        for level, count in confidence_levels.items():
            table.add_row(level, str(count))
        
        console.print(Panel(table, border_style="cyan"))
        
        # Generate report if requested
        if output:
            report_path = scanner.generate_report(output)
            console.print(f"[success]Report generated: [bold]{report_path}[/bold][/success]")
            
            # Ask if user wants to translate these files
            if Confirm.ask("Do you want to translate these files now?", console=console):
                self.translate_files_from_scan(directory)
        else:
            # Save pending files to session for later use
            self.session_data["pending_files"] = [str(result.file_path) for result in results]
            self._save_session()
            
            console.print(Panel("Files added to translation queue", title="Session Updated", border_style="green"))
            console.print("Run 'translator translate --resume' to translate these files")
    
    def translate_file(self, file_path: Union[str, Path]):
        """Translate a single file
        
        Args:
            file_path: Path to the file to translate
        """
        self._display_header()
        self._init_processor()
        
        file_path = Path(file_path)
        
        if not file_path.exists() or not file_path.is_file():
            console.print(f"[error]File not found: {file_path}[/error]")
            return
        
        # Check if file is marked as safe
        if str(file_path) in self.session_data.get("safe_files", []):
            console.print(Panel(f"File is marked as safe (contains sensitive content): {file_path.name}", 
                              title="Safety Check", border_style="yellow"))
            if not Confirm.ask("Do you want to translate this file anyway?", console=console):
                console.print("[warning]Translation skipped.[/warning]")
                return
            # Remove from safe files if confirmed
            self.session_data["safe_files"].remove(str(file_path))
            self._save_session()
        
        with console.status(f"[bold blue]Translating: {file_path.name}[/bold blue]"):
            success, output_path = self.processor.translate_file(file_path)
        
        if success:
            console.print(Panel(f"Successfully translated to: {output_path}", title="Translation Complete", border_style="green"))
            
            # Add to completed files
            self.session_data["completed_files"].append(str(file_path))
            self._save_session()
        else:
            console.print(Panel(f"Translation failed for: {file_path}", title="Translation Failed", border_style="red"))
            
            # Add to skipped files
            self.session_data["skipped_files"].append(str(file_path))
            self._save_session()
    
    def translate_files_from_list(self, file_paths: List[Union[str, Path]]):
        """Translate files from a list
        
        Args:
            file_paths: List of file paths to translate
        """
        self._display_header()
        self._init_processor()
        
        if not file_paths:
            console.print("[warning]No files to translate.[/warning]")
            return
        
        # Convert all paths to Path objects
        paths = [Path(p) for p in file_paths]
        
        # Verify files exist
        valid_paths = []
        for path in paths:
            if path.exists() and path.is_file():
                valid_paths.append(path)
            else:
                console.print(f"[warning]File not found, skipping: {path}[/warning]")
        
        if not valid_paths:
            console.print("[error]No valid files to translate.[/error]")
            return
        
        # Filter out safe files
        paths_to_translate = []
        for path in valid_paths:
            if str(path) in self.session_data.get("safe_files", []):
                console.print(f"[warning]Skipping safe file: {path.name}[/warning]")
            else:
                paths_to_translate.append(path)
        
        if not paths_to_translate:
            console.print("[warning]All files are marked as safe. No files to translate.[/warning]")
            return
        
        # Update session
        self.session_data["pending_files"] = [str(p) for p in paths_to_translate]
        if not self.session_data["start_time"]:
            self.session_data["start_time"] = datetime.datetime.now()
        self.session_data["paused"] = False
        self._save_session()
        
        console.print(Panel(f"Translating {len(paths_to_translate)} files", title="Translation Queue", border_style="blue"))
        
        # Hint about pause functionality
        console.print("[info]Press P to pause translation at any time[/info]")
        
        # Set up progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(complete_style="progress.bar.finished"),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            overall_task = progress.add_task("Overall Progress", total=len(paths_to_translate))
            file_task = progress.add_task("Current File", total=1.0, visible=False)
            
            translated_files = []
            skipped_files = []
            
            try:
                for i, file_path in enumerate(paths_to_translate):
                    # Update task description with current file (shortened path)
                    file_name = file_path.name
                    progress.update(overall_task, description=f"File {i+1}/{len(paths_to_translate)}")
                    progress.update(file_task, description=f"Translating: {file_name}", completed=0, visible=True)
                    
                    # Translate file
                    success, output_path = self.processor.translate_file(file_path)
                    
                    # Update file progress
                    progress.update(file_task, completed=1.0)
                    
                    if success:
                        translated_files.append(str(file_path))
                    else:
                        skipped_files.append(str(file_path))
                    
                    # Update overall progress
                    progress.update(overall_task, advance=1)
                    
                    # Check for pause request every file
                    if sys.stdin.isatty():  # Only check if running in a terminal
                        try:
                            # Non-blocking check for keyboard input
                            import msvcrt
                            if msvcrt.kbhit():
                                key = msvcrt.getch().lower()
                                if key == b'p':  # 'p' for pause
                                    progress.stop()
                                    if Confirm.ask("\nPause translation?", console=console):
                                        # Save remaining files to session
                                        self.session_data["pending_files"] = [str(p) for p in paths_to_translate[i+1:]]
                                        self.session_data["completed_files"].extend(translated_files)
                                        self.session_data["skipped_files"].extend(skipped_files)
                                        self.session_data["paused"] = True
                                        self._save_session()
                                        
                                        console.print(Panel("Translation paused. Run 'translator resume' to continue.", 
                                                         title="Paused", border_style="yellow"))
                                        return
                                    progress.start()
                        except (ImportError, AttributeError):
                            # Fallback for non-Windows systems or environments without msvcrt
                            pass
            except KeyboardInterrupt:
                # Handle manual interruption
                progress.stop()
                console.print(Panel("Translation interrupted", title="Paused", border_style="yellow"))
                
                # Save progress
                self.session_data["pending_files"] = [str(p) for p in paths_to_translate[i+1:]]
                self.session_data["completed_files"].extend(translated_files)
                self.session_data["skipped_files"].extend(skipped_files)
                self.session_data["paused"] = True
                self._save_session()
                
                console.print("Progress saved. Run 'translator resume' to continue.")
                return
        
        # Hide file progress after completion
        progress.update(file_task, visible=False)
        
        # Update session with completed files
        self.session_data["completed_files"].extend(translated_files)
        self.session_data["skipped_files"].extend(skipped_files)
        self.session_data["pending_files"] = []
        self.session_data["paused"] = False
        self._save_session()
        
        # Display statistics at the end
        console.print(Panel("Translation completed!", title="Success", border_style="green"))
        stats = self.processor.get_stats()
        
        # Calculate elapsed time if available
        elapsed_time = None
        if self.session_data["start_time"]:
            elapsed_time = (datetime.datetime.now() - self.session_data["start_time"]).total_seconds()
        
        self._display_stats(stats, elapsed_time)
    
    def translate_files_from_scan(self, directory: Union[str, Path], priority: Optional[str] = None):
        """Translate files based on a directory scan
        
        Args:
            directory: Directory to scan and translate
            priority: Priority level to filter by (high, medium, low)
        """
        self._display_header()
        self._init_processor()
        
        directory = Path(directory)
        
        if not directory.exists() or not directory.is_dir():
            console.print(f"[error]Directory not found: {directory}[/error]")
            return
        
        console.print(Panel(f"Scanning directory: {directory}", title="File Scanner", border_style="blue"))
        
        with console.status("[bold blue]Scanning files...[/bold blue]"):
            scan_results = self.processor.scanner.scan_directory(directory)
        
        if not scan_results:
            console.print(Panel("No Portuguese files found in the directory.", border_style="yellow"))
            return
        
        # Filter by priority if specified
        if priority:
            priority = priority.lower()
            filtered_results = []
            
            for result in scan_results:
                file_priority = "medium"  # Default
                
                # Determine priority based on confidence
                if result.confidence > 0.8:
                    file_priority = "high"
                elif result.confidence < 0.5:
                    file_priority = "low"
                
                # Increase priority for important file types
                if result.file_type in ["md", "py", "js", "html", "json"]:
                    if file_priority == "medium":
                        file_priority = "high"
                
                if file_priority == priority:
                    filtered_results.append(result)
            
            scan_results = filtered_results
            console.print(Panel(f"Found [bold]{len(scan_results)}[/bold] {priority} priority files to translate", 
                              title="Filtered Results", border_style="blue"))
        else:
            console.print(Panel(f"Found [bold]{len(scan_results)}[/bold] files to translate", 
                              title="Scan Results", border_style="blue"))
        
        if not scan_results:
            console.print(Panel(f"No files with {priority} priority found.", border_style="yellow"))
            return
        
        # Allow user to view the file list before proceeding
        if Confirm.ask("Do you want to see the list of files before translating?", console=console):
            table = Table(title="Files to Translate", show_header=True)
            table.add_column("File", style="cyan")
            table.add_column("Type", style="magenta")
            table.add_column("Confidence", style="green")
            
            for result in scan_results[:20]:  # Show first 20 files only
                file_name = str(result.file_path.relative_to(directory) if result.file_path.is_relative_to(directory) else result.file_path)
                table.add_row(file_name, result.file_type, f"{result.confidence:.2f}")
            
            if len(scan_results) > 20:
                table.add_row(f"...and {len(scan_results) - 20} more files", "", "")
            
            console.print(Panel(table, border_style="cyan"))
        
        # Convert scan results to paths
        file_paths = [result.file_path for result in scan_results]
        
        if Confirm.ask("Do you want to translate these files now?", console=console):
            # Translate the files
            self.translate_files_from_list(file_paths)
        else:
            # Save to session for later
            self.session_data["pending_files"] = [str(p) for p in file_paths]
            self._save_session()
            console.print(Panel("Files added to session. Run 'translator resume' to translate later.", 
                              title="Session Updated", border_style="green"))
    
    def resume_translation(self):
        """Resume a previously paused translation session"""
        self._display_header()
        self._init_processor()
        
        if not self.session_data["pending_files"]:
            console.print(Panel("No pending translation session found.", border_style="yellow"))
            return
        
        pending_count = len(self.session_data["pending_files"])
        completed_count = len(self.session_data["completed_files"])
        skipped_count = len(self.session_data["skipped_files"])
        
        status = "paused" if self.session_data.get("paused", False) else "pending"
        
        console.print(Panel(
            f"Found {status} translation session:\n"
            f"[green]{completed_count} files translated[/green]\n"
            f"[yellow]{skipped_count} files skipped[/yellow]\n"
            f"[blue]{pending_count} files remaining[/blue]",
            title="Session Status", border_style="cyan"
        ))
        
        if not Confirm.ask("Continue translation?", console=console):
            return
        
        # Translate the pending files
        self.translate_files_from_list(self.session_data["pending_files"])
    
    def clear_session(self):
        """Clear the current translation session"""
        self._display_header()
        
        if not self.session_file.exists():
            console.print(Panel("No session file found.", border_style="yellow"))
            return
        
        if Confirm.ask("Are you sure you want to clear the current session?", console=console):
            try:
                os.remove(self.session_file)
                self.session_data = {
                    "pending_files": [],
                    "completed_files": [],
                    "skipped_files": [],
                    "safe_files": [],
                    "start_time": None,
                    "last_updated": None,
                    "paused": False
                }
                console.print(Panel("Session cleared successfully.", title="Success", border_style="green"))
            except Exception as e:
                console.print(Panel(f"Error clearing session: {str(e)}", title="Error", border_style="red"))
    
    def mark_file_safe(self, file_path: Union[str, Path]):
        """Mark a file as safe (containing sensitive content)
        
        Args:
            file_path: Path to the file to mark as safe
        """
        self._display_header()
        
        file_path = Path(file_path)
        
        if not file_path.exists() or not file_path.is_file():
            console.print(f"[error]File not found: {file_path}[/error]")
            return
        
        str_path = str(file_path)
        
        if str_path in self.session_data.get("safe_files", []):
            console.print(Panel(f"File is already marked as safe: {file_path.name}", border_style="yellow"))
            
            if Confirm.ask("Do you want to remove this file from the safe list?", console=console):
                self.session_data["safe_files"].remove(str_path)
                self._save_session()
                console.print(Panel(f"File removed from safe list: {file_path.name}", title="Success", border_style="green"))
            return
        
        if "safe_files" not in self.session_data:
            self.session_data["safe_files"] = []
            
        self.session_data["safe_files"].append(str_path)
        self._save_session()
        
        console.print(Panel(
            f"File marked as safe: {file_path.name}\n"
            "This file will be skipped during translation unless explicitly selected.",
            title="File Protected", border_style="green"
        ))
    
    def show_session_info(self):
        """Show information about the current session"""
        self._display_header()
        
        if not self.session_data["pending_files"] and not self.session_data["completed_files"] and not self.session_data["safe_files"]:
            console.print(Panel("No active session found.", border_style="yellow"))
            return
        
        table = Table(title="Session Information", show_header=True, header_style="bold magenta", expand=False, width=60)
        
        table.add_column("Item", style="dim")
        table.add_column("Count", style="cyan", justify="right")
        
        table.add_row("Pending Files", str(len(self.session_data["pending_files"])))
        table.add_row("Completed Files", str(len(self.session_data["completed_files"])))
        table.add_row("Skipped Files", str(len(self.session_data["skipped_files"])))
        table.add_row("Protected Files", str(len(self.session_data.get("safe_files", []))))
        
        status = "Paused" if self.session_data.get("paused", False) else "Active" if self.session_data["pending_files"] else "Complete"
        table.add_row("Status", status)
        
        if self.session_data["start_time"]:
            start_time = self.session_data["start_time"].strftime("%Y-%m-%d %H:%M:%S")
            table.add_row("Session Start", start_time)
        
        if self.session_data["last_updated"]:
            last_updated = self.session_data["last_updated"].strftime("%Y-%m-%d %H:%M:%S")
            table.add_row("Last Updated", last_updated)
        
        console.print(Panel(table, border_style="cyan"))
        
        # Show options based on session state
        if self.session_data["pending_files"]:
            if Confirm.ask("Resume translation?", console=console):
                self.resume_translation()
        elif self.session_data.get("safe_files", []):
            console.print("\n[info]Your session contains protected files that won't be translated.[/info]")
            if Confirm.ask("View protected files?", console=console):
                self._show_protected_files()
    
    def _show_protected_files(self):
        """Display a list of protected (safe) files"""
        if not self.session_data.get("safe_files", []):
            console.print("[warning]No protected files found.[/warning]")
            return
            
        table = Table(title="Protected Files", show_header=True)
        table.add_column("File", style="cyan")
        
        for i, file_path in enumerate(self.session_data["safe_files"][:20]):  # Show first 20 only
            file_name = Path(file_path).name
            table.add_row(file_name)
            
        if len(self.session_data["safe_files"]) > 20:
            table.add_row(f"...and {len(self.session_data['safe_files']) - 20} more files")
            
        console.print(Panel(table, border_style="cyan"))
    
    def main(self):
        """Main entry point for the CLI"""
        parser = argparse.ArgumentParser(description="EVA & GUARANI Translator")
        subparsers = parser.add_subparsers(dest="command", help="Command to execute")
        
        # Scan command
        scan_parser = subparsers.add_parser("scan", help="Scan a directory for Portuguese files")
        scan_parser.add_argument("directory", help="Directory to scan")
        scan_parser.add_argument("--output", "-o", help="Output file for scan results")
        
        # Translate file command
        file_parser = subparsers.add_parser("file", help="Translate a single file")
        file_parser.add_argument("file_path", help="Path to the file to translate")
        
        # Translate directory command
        dir_parser = subparsers.add_parser("directory", help="Translate Portuguese files in a directory")
        dir_parser.add_argument("directory", help="Directory containing files to translate")
        dir_parser.add_argument("--scan", "-s", action="store_true", help="Scan directory first")
        dir_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"], help="Filter by priority")
        
        # Translate batch command
        batch_parser = subparsers.add_parser("batch", help="Translate files from a batch file")
        batch_parser.add_argument("batch_file", help="File containing a list of files to translate")
        
        # Resume translation command
        subparsers.add_parser("resume", help="Resume a previously paused translation")
        
        # Session management commands
        session_parser = subparsers.add_parser("session", help="Manage translation sessions")
        session_parser.add_argument("action", choices=["info", "clear"], help="Session action to perform")
        
        # Safe file command
        safe_parser = subparsers.add_parser("safe", help="Mark file as safe (protected from translation)")
        safe_parser.add_argument("file_path", help="Path to the file to mark as safe")
        
        # Version command
        subparsers.add_parser("version", help="Show version information")
        
        # Parse arguments
        args = parser.parse_args()
        
        # Execute command
        if args.command == "scan":
            self.scan_directory(args.directory, args.output)
        elif args.command == "file":
            self.translate_file(args.file_path)
        elif args.command == "directory":
            if args.scan:
                self.translate_files_from_scan(args.directory, args.priority)
            else:
                # Get all files in directory
                directory = Path(args.directory)
                file_paths = list(directory.glob("**/*"))
                file_paths = [p for p in file_paths if p.is_file()]
                self.translate_files_from_list(file_paths)
        elif args.command == "batch":
            # Read batch file
            batch_file = Path(args.batch_file)
            if not batch_file.exists():
                console.print(f"[error]Batch file not found: {batch_file}[/error]")
                return
            
            # Determine file type and read accordingly
            if batch_file.suffix.lower() == ".json":
                with open(batch_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        file_paths = data
                    elif isinstance(data, dict) and "files" in data:
                        file_paths = data["files"]
                    else:
                        console.print("[error]Invalid JSON batch file format.[/error]")
                        return
            else:
                # Assume text file with one path per line
                with open(batch_file, 'r', encoding='utf-8') as f:
                    file_paths = [line.strip() for line in f if line.strip()]
            
            self.translate_files_from_list(file_paths)
        elif args.command == "resume":
            self.resume_translation()
        elif args.command == "session":
            if args.action == "info":
                self.show_session_info()
            elif args.action == "clear":
                self.clear_session()
        elif args.command == "safe":
            self.mark_file_safe(args.file_path)
        elif args.command == "version":
            self._display_header()
            console.print(Panel(
                "EVA & GUARANI Translator v1.2.0\n"
                "Phase 1: Stabilization and Foundation\n\n"
                "[cyan]Modular and efficient tool for automatic file translation[/cyan]",
                title="Version Information", border_style="cyan"
            ))
        else:
            # Display help if no command provided
            self._display_header()
            
            # If we have an active session, show session info
            if self.session_data["pending_files"] or self.session_data["completed_files"]:
                status = "paused" if self.session_data.get("paused", False) else "active"
                console.print(Panel(
                    f"You have a {status} translation session\n"
                    f"[green]{len(self.session_data['completed_files'])} files completed[/green]  "
                    f"[blue]{len(self.session_data['pending_files'])} files pending[/blue]",
                    title="Session Status", border_style="cyan"
                ))
                console.print("[info]Run 'translator resume' to continue translation[/info]")
                console.print("[info]Run 'translator session info' for detailed session information[/info]")
            
            # Show common commands
            table = Table(title="Common Commands", show_header=True, header_style="bold magenta", expand=False)
            table.add_column("Command", style="cyan")
            table.add_column("Description", style="dim")
            
            table.add_row("translator scan <directory>", "Scan directory for Portuguese files")
            table.add_row("translator file <file>", "Translate a single file")
            table.add_row("translator directory <dir> --scan", "Scan and translate files in directory")
            table.add_row("translator resume", "Resume a paused translation session")
            table.add_row("translator safe <file>", "Mark a file as protected from translation")
            table.add_row("translator session info", "View session information")
            
            console.print(Panel(table, border_style="blue"))

def main():
    """Entry point for the command-line interface"""
    cli = TranslatorCLI()
    try:
        cli.main()
    except KeyboardInterrupt:
        console.print(Panel("Operation interrupted", title="Exited", border_style="yellow"))
        sys.exit(1)
    except Exception as e:
        console.print(Panel(f"Error: {str(e)}", title="Error", border_style="red"))
        cli_logger.exception("Unhandled exception in CLI")
        sys.exit(1)

if __name__ == "__main__":
    main() 