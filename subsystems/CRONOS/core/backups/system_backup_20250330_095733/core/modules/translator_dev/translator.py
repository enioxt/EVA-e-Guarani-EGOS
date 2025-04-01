#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EVA & GUARANI Translator - Advanced Translation Utility

The translator is a powerful utility for batch translation of files
from Portuguese to English. It supports multiple translation engines,
smart caching, and technical terminology management.
"""

import os
import sys
import argparse
import logging
import time
from typing import List, Optional, Dict, Any
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner

# Add parent directory to path to allow importing modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from modules.translator_dev.core.scanner import Scanner, ScanResult
from modules.translator_dev.core.processor import TranslationProcessor
from modules.translator_dev.core.cache import TranslationCache
from modules.translator_dev.utils.logger import setup_logger

logger = logging.getLogger(__name__)

class Translator:
    """Main translator class that orchestrates the translation process"""
    
    def __init__(self, cache_dir: Optional[str] = None, verbose: bool = False):
        """
        Initialize the translator
        
        Args:
            cache_dir: Directory to store translation cache
            verbose: Enable verbose logging
        """
        # Setup logging
        log_level = logging.DEBUG if verbose else logging.INFO
        setup_logger(log_level)
        
        # Initialize console
        self.console = Console()
        
        # Initialize scanner
        self.scanner = Scanner()
        
        # Initialize cache
        self.cache = TranslationCache(cache_dir)
        
        # Initialize processor
        self.processor = TranslationProcessor(self.cache)
        
    def scan_directory(self, input_dir: str, target_lang: str = "pt") -> ScanResult:
        """
        Scan a directory for files to translate
        
        Args:
            input_dir: Directory to scan
            target_lang: Target language to scan for
            
        Returns:
            ScanResult object containing files to translate
        """
        self.console.print(f"[bold]Scanning directory:[/bold] {input_dir}")
        
        # Show a spinner while scanning
        with self.console.status("[bold green]Scanning for Portuguese files...[/bold green]") as status:
            scan_result = self.scanner.scan_directory(input_dir, target_lang)
        
        # Print scan results
        if scan_result.files:
            self.console.print(f"[green]Found {len(scan_result.files)} Portuguese files to translate[/green]")
        else:
            self.console.print("[yellow]No Portuguese files found[/yellow]")
            
        return scan_result
        
    def translate(self, scan_result: ScanResult, output_dir: str, 
                  engine_name: str = "huggingface", workers: int = 2) -> Dict[str, Any]:
        """
        Translate files based on scan results
        
        Args:
            scan_result: ScanResult object containing files to translate
            output_dir: Directory to save translated files
            engine_name: Translation engine to use
            workers: Number of worker threads
            
        Returns:
            Dictionary with translation statistics
        """
        if not scan_result.files:
            self.console.print("[yellow]No files to translate[/yellow]")
            return {}
            
        self.console.print(f"[bold]Translating {len(scan_result.files)} files to:[/bold] {output_dir}")
        self.console.print(f"[bold]Using engine:[/bold] {engine_name}")
        
        # Create progress bar
        with Progress(
            TextColumn("[bold blue]{task.description}[/bold blue]"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn()
        ) as progress:
            # Create a task for overall progress
            task = progress.add_task(f"Translating files", total=len(scan_result.files))
            
            # Define progress callback
            def update_progress(file_index: int):
                progress.update(task, advance=1)
            
            # Translate files
            stats = self.processor.translate_files(
                scan_result.files, 
                output_dir=output_dir,
                engine_name=engine_name,
                workers=workers,
                progress_callback=update_progress
            )
        
        # Show translation stats
        if stats:
            table = Table(title="Translation Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Files Processed", str(stats.get("files_processed", 0)))
            table.add_row("Total Characters", str(stats.get("total_chars", 0)))
            table.add_row("Cache Hits", str(stats.get("cache_hits", 0)))
            table.add_row("API Calls", str(stats.get("api_calls", 0)))
            table.add_row("Engine Used", stats.get("engine", engine_name))
            table.add_row("Total Time", f"{stats.get('total_time', 0):.2f} seconds")
            
            self.console.print(Panel(table, title="Translation Complete"))
        
        return stats

def main():
    """Main entry point for the translator"""
    parser = argparse.ArgumentParser(description="EVA & GUARANI Translator")
    
    # Add arguments
    parser.add_argument("--scan", metavar="DIR", help="Scan directory for Portuguese files")
    parser.add_argument("--translate", metavar="DIR", help="Translate Portuguese files in directory")
    parser.add_argument("--output", metavar="DIR", help="Output directory for translated files")
    parser.add_argument("--engine", choices=["huggingface", "openai"], default="huggingface", 
                        help="Translation engine to use (default: huggingface)")
    parser.add_argument("--workers", type=int, default=2, 
                        help="Number of worker threads (default: 2)")
    parser.add_argument("--cache-dir", metavar="DIR", 
                        help="Cache directory (default: data/cache/translations)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Create translator
    translator = Translator(cache_dir=args.cache_dir, verbose=args.verbose)
    
    # Scan directory
    if args.scan and not args.translate:
        translator.scan_directory(args.scan)
        return
        
    # Translate directory
    if args.translate:
        # If output directory not specified, use default
        output_dir = args.output or "data/translated"
        
        # Scan directory
        scan_result = translator.scan_directory(args.translate)
        
        # Translate files
        if scan_result.files:
            translator.translate(
                scan_result,
                output_dir=output_dir,
                engine_name=args.engine,
                workers=args.workers
            )
        return
        
    # If no action specified, show help
    parser.print_help()

if __name__ == "__main__":
    main() 