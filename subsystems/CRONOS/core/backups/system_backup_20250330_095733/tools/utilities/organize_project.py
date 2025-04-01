#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI Project Organizer
This script organizes the project by moving old files to quarantine
and keeping only the active and necessary files.
"""

import os
import shutil
import json
import datetime
import logging
from typing import List, Dict, Any, Set

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/organize_project.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# Constants
QUARANTINE_DIR = "quarantine"
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Directories to keep in the root
ESSENTIAL_DIRS = {
    "modules", "config", "data", "logs", "EGOS", "quantum", 
    "prompts", "backups", "ethics", "quarantine"
}

# Essential files in the root
ESSENTIAL_FILES = {
    "unified_eva_guarani_bot.py", "payment_gateway.py", "dalle_integration.py",
    "setup_payment_system.py", "README.md", "requirements.txt",
    ".gitignore", "organize_project.py"
}

# Extensions to ignore
IGNORE_EXTENSIONS = {".pyc", ".pyo", ".pyd", ".git"}

def ensure_dir(directory: str) -> None:
    """Ensures that a directory exists."""
    os.makedirs(directory, exist_ok=True)
    logger.info(f"Directory ensured: {directory}")

def create_manifest(moved_files: List[Dict[str, Any]]) -> str:
    """Creates a manifest file with details of the moved files."""
    manifest_data = {
        "timestamp": TIMESTAMP,
        "moved_files_count": len(moved_files),
        "moved_files": moved_files
    }
    
    manifest_path = os.path.join(QUARANTINE_DIR, f"manifest_{TIMESTAMP}.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=4, ensure_ascii=False)
    
    logger.info(f"Manifest created: {manifest_path}")
    return manifest_path

def move_to_quarantine(source_path: str, target_dir: str) -> Dict[str, Any]:
    """
    Moves a file or directory to quarantine.
    
    Args:
        source_path: Path of the file or directory to be moved
        target_dir: Destination directory within quarantine
        
    Returns:
        Dict with information about the moved file
    """
    # Ensure that the destination directory exists
    ensure_dir(target_dir)
    
    # Get file information before moving
    file_info = {}
    file_info["original_path"] = source_path
    file_info["size_bytes"] = os.path.getsize(source_path) if os.path.isfile(source_path) else None
    file_info["timestamp"] = TIMESTAMP
    
    # Determine the destination path
    filename = os.path.basename(source_path)
    base, ext = os.path.splitext(filename)
    
    # Add timestamp to the file name to avoid conflicts
    new_filename = f"{base}_{TIMESTAMP}{ext}"
    target_path = os.path.join(target_dir, new_filename)
    
    # Move the file
    shutil.move(source_path, target_path)
    
    file_info["quarantine_path"] = target_path
    logger.info(f"Moved to quarantine: {source_path} -> {target_path}")
    
    return file_info

def identify_old_files(dir_path: str, essential_files: Set[str]) -> List[str]:
    """
    Identifies old files in a directory.
    
    Args:
        dir_path: Path of the directory to be analyzed
        essential_files: Set of essential file names to keep
        
    Returns:
        List of full paths of files to be moved to quarantine
    """
    files_to_move = []
    
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        
        # Ignore essential directories
        if os.path.isdir(item_path) and item in ESSENTIAL_DIRS:
            continue
            
        # Check files
        if os.path.isfile(item_path):
            # Ignore essential files
            if item in essential_files:
                continue
                
            # Ignore specific extensions
            _, ext = os.path.splitext(item)
            if ext.lower() in IGNORE_EXTENSIONS:
                continue
                
            # Add to the list of files to move
            files_to_move.append(item_path)
        
        # For non-essential directories in the root, move to quarantine
        elif os.path.isdir(item_path) and dir_path == ".":
            if item not in ESSENTIAL_DIRS and not item.startswith("."):
                files_to_move.append(item_path)
    
    return files_to_move

def organize_project() -> None:
    """Organizes the project by moving old files to quarantine."""
    # Ensure that the quarantine folder exists
    ensure_dir(QUARANTINE_DIR)
    ensure_dir(os.path.join(QUARANTINE_DIR, "root_files"))
    ensure_dir(os.path.join(QUARANTINE_DIR, "directories"))
    ensure_dir("logs")
    
    moved_files = []
    
    # Identify files in the root
    root_files_to_move = identify_old_files(".", ESSENTIAL_FILES)
    
    # Move files from the root
    for file_path in root_files_to_move:
        if os.path.isfile(file_path):
            file_info = move_to_quarantine(file_path, os.path.join(QUARANTINE_DIR, "root_files"))
        else:
            file_info = move_to_quarantine(file_path, os.path.join(QUARANTINE_DIR, "directories"))
        moved_files.append(file_info)
    
    # Create manifest of moved files
    manifest_path = create_manifest(moved_files)
    
    logger.info(f"Organization completed. Moved {len(moved_files)} files/directories to quarantine.")
    logger.info(f"Manifest: {manifest_path}")
    
    # Summary of operations
    print("\n" + "="*50)
    print(f"ORGANIZATION REPORT - {TIMESTAMP}")
    print("="*50)
    print(f"Total files/directories moved: {len(moved_files)}")
    print(f"Detailed manifest: {manifest_path}")
    print("="*50 + "\n")

if __name__ == "__main__":
    logger.info("Starting organization of EVA & GUARANI project")
    organize_project()