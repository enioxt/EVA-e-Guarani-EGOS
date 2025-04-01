#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Portuguese to English Translation Tool
This script helps identify and translate Portuguese files to English.
"""

import os
import re
import sys
import json
import logging
import datetime  # Use datetime module directly
from pathlib import Path
from typing import List, Dict, Tuple, Set, Optional, Any, Union
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("translation_log.txt", encoding="utf-8")
    ]
)
logger = logging.getLogger("translate_to_english")

# Common Portuguese words to help identify files
PORTUGUESE_INDICATORS = [
    "file", "function", "module", "system", "class", "object", "method",
    "for", "as", "because", "then", "through", "while", "also",
    "no", "yes", "user", "implementation", "configuration", "code",
    "directory", "file", "test", "variable", "connection", "database", "data"
]

# Portuguese-specific characters
PORTUGUESE_CHARS = "áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ"

class TranslationTool:
    """Tool to identify and manage translation of Portuguese files to English"""
    
    def __init__(self, root_dir: Path, ignore_dirs: List[str] = [], ignore_files: List[str] = []):
        """
        Initialize the translation tool
        
        Args:
            root_dir: Root directory to scan
            ignore_dirs: Directories to ignore
            ignore_files: Files to ignore
        """
        self.root_dir = root_dir
        
        # Default directories to ignore (system and third-party folders)
        default_ignore_dirs = [
            ".git", "__pycache__", "venv", "env", "node_modules", 
            "cursor", "AppData", "OneDrive", "Windows", "Program Files", 
            "ProgramData", "Users", ".vscode", "bin", "lib", "include", 
            "Scripts", "site-packages"
        ]
        
        # Combine default and user-specified directories to ignore
        self.ignore_dirs = list(set(default_ignore_dirs + (ignore_dirs or [])))
        
        # Default files to ignore (system files, binaries, etc.)
        default_ignore_files = [
            ".gitignore", "LICENSE", ".DS_Store", "Thumbs.db", 
            "*.exe", "*.dll", "*.so", "*.dylib", "*.pyd", "*.pyc",
            "*.pyo", "*.pdb", "*.obj", "*.o", "*.a", "*.lib"
        ]
        
        # Combine default and user-specified files to ignore
        self.ignore_files = list(set(default_ignore_files + (ignore_files or [])))
        
        self.portuguese_files = []
        self.translated_count = 0
        self.skipped_count = 0
        self.total_files = 0
        
        # Translation log
        self.translation_log = {
            "translated": [],
            "skipped": [],
            "failed": []
        }
    
    def is_likely_portuguese(self, content: str) -> bool:
        """
        Check if content is likely in Portuguese
        
        Args:
            content: File content to check
            
        Returns:
            bool: True if likely Portuguese
        """
        # Check for Portuguese characters
        if any(char in content for char in PORTUGUESE_CHARS):
            return True
            
        # Check for common Portuguese words
        word_count = 0
        for word in PORTUGUESE_INDICATORS:
            if re.search(r'\b' + word + r'\b', content, re.IGNORECASE):
                word_count += 1
                
        # If multiple Portuguese words are found, it's likely Portuguese
        return word_count >= 3
    
    def should_ignore_path(self, path: str) -> bool:
        """
        Check if a path should be ignored based on ignore patterns
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if the path should be ignored
        """
        # Check if path contains any of the ignored directory names
        for ignore_dir in self.ignore_dirs:
            if f"/{ignore_dir}/" in path.replace("\\", "/") or path.replace("\\", "/").endswith(f"/{ignore_dir}"):
                return True
                
        # Check if filename matches any of the ignored file patterns
        filename = os.path.basename(path)
        for ignore_file in self.ignore_files:
            if re.match(f"^{ignore_file.replace('*', '.*')}$", filename):
                return True
                
        return False
    
    def is_project_file(self, path: str) -> bool:
        """
        Check if a file is likely part of the Eva & Guarani project
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if the file is likely part of the project
        """
        # Convert path separators to standard format for pattern matching
        norm_path = path.replace("\\", "/").lower()
        
        # Key project directories to include
        project_indicators = [
            "/eva & guarani", "/eva&guarani", "/egos", 
            "/core/", "/modules/", "/ethik/", "/atlas/", 
            "/nexus/", "/cronos/", "/ui/", "/docs/", 
            "/integrations/", "/api/", "/sandbox/"
        ]
        
        # If the path contains any of the project indicators, consider it a project file
        for indicator in project_indicators:
            if indicator in norm_path:
                return True
                
        return False
    
    def scan_directory(self) -> List[Path]:
        """
        Scan directory for files likely in Portuguese
        
        Returns:
            List[Path]: List of files likely in Portuguese
        """
        logger.info(f"Scanning directory: {self.root_dir}")
        
        portuguese_files = []
        
        for root, dirs, files in os.walk(self.root_dir):
            # Filter out directories to ignore
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs and not self.should_ignore_path(os.path.join(root, d))]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip if the file should be ignored
                if self.should_ignore_path(file_path):
                    continue
                
                # Skip if not likely part of the project
                if not self.is_project_file(file_path):
                    continue
                
                # Skip binary files and non-text files
                if not file.endswith(('.py', '.md', '.txt', '.json', '.js', '.html', '.css', '.yml', '.yaml', '.bat', '.ps1')):
                    continue
                
                self.total_files += 1
                
                try:
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check if file is likely Portuguese
                    if self.is_likely_portuguese(content):
                        portuguese_files.append(Path(file_path))
                        logger.info(f"Found Portuguese file: {Path(file_path).relative_to(self.root_dir)}")
                except Exception as e:
                    logger.warning(f"Error reading file {file_path}: {str(e)}")
        
        self.portuguese_files = portuguese_files
        logger.info(f"Found {len(portuguese_files)} files likely in Portuguese out of {self.total_files} total files")
        
        return portuguese_files
    
    def generate_translation_report(self, output_path: Optional[Path] = None) -> Path:
        """
        Generate a report of Portuguese files for translation
        
        Args:
            output_path: Path to save report (optional)
            
        Returns:
            Path: Path to saved report
        """
        if not output_path:
            output_path = self.root_dir / "translation_report.md"
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# EVA & GUARANI Translation Report\n\n")
            f.write("> Files identified as containing Portuguese content\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total files scanned**: {self.total_files}\n")
            f.write(f"- **Files likely in Portuguese**: {len(self.portuguese_files)}\n")
            f.write(f"- **Files already translated**: {self.translated_count}\n")
            f.write(f"- **Files skipped**: {self.skipped_count}\n\n")
            
            f.write("## Files to Translate\n\n")
            f.write("| File | Type | Size | Priority |\n")
            f.write("|------|------|------|----------|\n")
            
            for file_path in self.portuguese_files:
                rel_path = file_path.relative_to(self.root_dir)
                file_type = file_path.suffix.lstrip('.')
                file_size = file_path.stat().st_size / 1024  # KB
                
                # Determine priority based on file type and location
                priority = "Medium"
                
                # High priority items
                if any(s in str(file_path) for s in ["README", "core/", "ethik/", "atlas/", "nexus/", "cronos/", "config"]):
                    priority = "High"
                
                # Medium priority items (already set as default)
                
                # Low priority items
                if any(s in str(file_path) for s in ["tests", "examples", "sandbox/examples"]):
                    priority = "Low"
                
                f.write(f"| {rel_path} | {file_type} | {file_size:.1f} KB | {priority} |\n")
        
        logger.info(f"Translation report saved to {output_path}")
        return output_path
    
    def save_translation_log(self, output_path: Optional[Path] = None) -> Path:
        """
        Save translation log to JSON file
        
        Args:
            output_path: Path to save log (optional)
            
        Returns:
            Path: Path to saved log
        """
        if not output_path:
            output_path = self.root_dir / "translation_log.json"
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.translation_log, f, indent=2)
            
        logger.info(f"Translation log saved to {output_path}")
        return output_path

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="EVA & GUARANI Portuguese File Scanner")
    parser.add_argument("--root-dir", type=str, default="..", help="Root directory to scan")
    parser.add_argument("--output", type=str, default="translation_report.md", help="Output file for the report")
    parser.add_argument("--ignore-dirs", type=str, nargs="+", help="Additional directories to ignore")
    parser.add_argument("--sample-only", action="store_true", help="Limit scan to a small sample of files for quick testing")
    parser.add_argument("--verbose", action="store_true", help="Show more detailed output")
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("translation_scan.log", encoding="utf-8")
        ]
    )
    
    root_dir = os.path.abspath(args.root_dir)
    output_file = args.output
    ignore_dirs = args.ignore_dirs or []
    
    logging.info(f"Starting scan of {root_dir}")
    
    scanner = PortugueseFileScanner(
        root_dir=root_dir,
        additional_ignored_dirs=ignore_dirs,
        sample_only=args.sample_only
    )
    
    portuguese_files = scanner.scan()
    
    logging.info(f"Found {len(portuguese_files)} files with Portuguese content")
    
    # Generate report
    generate_report(portuguese_files, output_file, root_dir, sample_only=args.sample_only)
    
    logging.info(f"Report generated: {output_file}")

class PortugueseFileScanner:
    """Scanner to find files with Portuguese content"""
    
    def __init__(self, root_dir: str, additional_ignored_dirs: Optional[List[str]] = None, sample_only: bool = False):
        """Initialize the scanner"""
        self.root_dir = root_dir
        self.additional_ignored_dirs = additional_ignored_dirs or []
        self.sample_only = sample_only
        self.sample_limit = 50  # Increase sample size to catch more files
        self.files_checked = 0
        self.found_files = []
        
        # Default directories to ignore
        self.ignored_dirs = [
            ".git", "__pycache__", "venv", "env", "node_modules", 
            "cursor", "AppData", "OneDrive", "Windows", "Program Files", 
            "ProgramData", "Users", ".vscode", "bin", "lib", "include", 
            "Scripts", "site-packages"
        ]
        
        # Add additional ignored directories
        for d in self.additional_ignored_dirs:
            if d not in self.ignored_dirs:
                self.ignored_dirs.append(d)
                
        # Default files to ignore
        self.ignored_files = [
            ".gitignore", "LICENSE", ".DS_Store", "Thumbs.db",
            # Binary file extensions
            ".exe", ".dll", ".so", ".dylib", ".pyc", ".pyo", ".pyd", 
            ".obj", ".o", ".a", ".lib", ".jar", ".war", 
            # Image files
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".svg", 
            # Audio/video files
            ".mp3", ".mp4", ".wav", ".avi", ".mov", ".flv", 
            # Archive files
            ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar", 
            # Database files
            ".db", ".sqlite", ".sqlite3", ".mdb"
        ]
        
        # Portuguese words to look for (common words that distinguish Portuguese from other languages)
        self.portuguese_indicators = [
            "no", "is", "function", "code", "also", "configuration",
            "module", "file", "directory", "variable", "class", "method",
            "through", "connection", "user", "system", "version", "translation",
            "execution", "instance", "parameter", "value", "service", "usage",
            "implementation", "application", "import", "configure", "verify",
            "process", "use", "execute", "load", "download", "save",
            # Shorter but unique Portuguese words
            "by", "for", "to", "as", "more", "each", "been", "after",
            "between", "still", "all", "every", "each", "their", "its",
            # Common code comments in Portuguese
            "# Function", "# Configuration", "# File", "# Variable",
            "# Implementation", "# This", "# That", "# Method", 
            "# This", "# For", "# Checks", "# Returns",
            # Common docstrings in Portuguese
            '"""This', '"""That', '"""This',
            "'''This", "'''That", "'''This",
            # Common variable names in Portuguese
            "user", "password", "file", "message", "response",
            "connection", "configuration", "result", "value", "list"
        ]
    
    def _should_ignore_dir(self, path: str) -> bool:
        """Check if directory should be ignored"""
        path = path.replace("\\", "/")
        for ignore_dir in self.ignored_dirs:
            if f"/{ignore_dir}/" in path.replace("\\", "/") or path.replace("\\", "/").endswith(f"/{ignore_dir}"):
                return True
        return False
    
    def _should_ignore_file(self, path: str) -> bool:
        """Check if file should be ignored"""
        filename = os.path.basename(path)
        if filename in self.ignored_files:
            return True
            
        ext = os.path.splitext(filename)[1].lower()
        if ext in self.ignored_files:
            return True
            
        # Also check wildcards
        for ignore_file in self.ignored_files:
            if "*" in ignore_file and re.match(f"^{ignore_file.replace('*', '.*')}$", filename):
                return True
                
        return False
    
    def _is_project_file(self, path: str) -> bool:
        """Check if file is likely part of the EVA & GUARANI project"""
        # Simplified check - can be made more sophisticated
        norm_path = path.replace("\\", "/").lower()
        
        # Check if the file is a text file we can analyze
        if not self._is_text_file(path):
            return False
            
        # Include files within the EVA & GUARANI project directories
        project_indicators = [
            "eva", "guarani", "atlas", "nexus", "cronos", "ethik", 
            "sandbox", "modules", "core", "integration"
        ]
        
        for indicator in project_indicators:
            if indicator in norm_path:
                return True
                
        return False
    
    def _is_text_file(self, path: str) -> bool:
        """Check if file is a text file we can analyze"""
        # Common text file extensions
        text_extensions = [
            ".py", ".md", ".txt", ".js", ".html", ".css", ".json", 
            ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", 
            ".sh", ".bat", ".ps1", ".sql"
        ]
        
        ext = os.path.splitext(path)[1].lower()
        if ext in text_extensions:
            return True
            
        # Try to read as text
        try:
            with open(path, 'r', encoding='utf-8') as f:
                f.read(1024)  # Read first 1KB
            return True
        except:
            return False
    
    def _contains_portuguese(self, file_path: str) -> bool:
        """Check if file contains Portuguese content"""
        try:
            # Skip large files to avoid performance issues
            file_size = os.path.getsize(file_path)
            if file_size > 1024 * 1024:  # Skip files larger than 1 MB
                return False
                
            # Read file content
            with open(file_path, 'r', encoding='