#!/usr/bin/env python3
python
import os
import shutil
from datetime import datetime

# Root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Get timestamp for obsolete files folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OBSOLETE_DIR = os.path.join(ROOT_DIR, f"obsolete_files_{timestamp}")

# Directory structure to be created
STRUCTURE = {
    "EGOS": {
        "core": {},
        "modules": {
            "atlas": {},
            "nexus": {},
            "cronos": {},
        },
        "config": {},
        "data": {
            "atlas": {},
            "nexus": {},
            "cronos": {},
        },
        "logs": {},
        "scripts": {},
        "quantum_prompts": {},
    },
    "docs": {},
    "tools": {},
    "bot": {},
    "backups": {},
}

# Essential files to be moved (source -> destination)
ESSENTIAL_FILES = {
    # Core
    "egos_core.py": "EGOS/core/",
    "ethik_core.js": "EGOS/core/",
    "quantum_core_essence.py": "EGOS/core/",
    
    # Quantum Prompts
    "EVA_GUARANI_v7.0.md": "EGOS/quantum_prompts/",
    
    # Configurations
    ".env": "EGOS/config/",
    
    # Startup scripts
    "start_egos.bat": "",  # Keep in root
    "start_egos.sh": "",  # Keep in root
    
    # Main documentation
    "README.md": "",  # Keep in root
    "SUBSYSTEMS.md": "docs/",
    "ARCHITECTURE.md": "docs/",
    "USAGE.md": "docs/",
    "CODE_OF_CONDUCT.md": "docs/",
    "LICENSE": "",  # Keep in root
    
    # Tools
    "backup_quantum_prompts.py": "tools/",
    "setup_egos.py": "tools/",
    "quantum_backup_system.py": "tools/",
    "create_egos_structure.py": "tools/",
    
    # Bots
    "unified_telegram_bot.py": "bot/",
    "start_bot.bat": "bot/",
    "start_unified_bot.bat": "bot/",
    
    # Others
    "requirements.txt": "",  # Keep in root
}

# Directories to be preserved (with their content)
PRESERVE_DIRS = [
    ".git",
    ".github",
    ".obsidian",
    "config",
    "logs",
    "quantum_prompts",
]

# List of potentially obsolete directories
POTENTIAL_OBSOLETE_DIRS = [
    "Old Bots",
    "New Folder",
    "old_files_20250301_171050",
    "backups",
    "backup_20250301_171540",
    "quarantine",
    "quarantine",
    "unused_files",
    "archived_files",
]

def create_directory_structure(base_dir, structure):
    """Creates the directory structure recursively"""
    for dir_name, sub_dirs in structure.items():
        dir_path = os.path.join(base_dir, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")
        
        if sub_dirs:
            create_directory_structure(dir_path, sub_dirs)

def move_essential_files():
    """Moves the essential files to their new locations"""
    for source, destination in ESSENTIAL_FILES.items():
        source_path = os.path.join(ROOT_DIR, source)
        
        # If the file does not exist, continue
        if not os.path.exists(source_path):
            print(f"File not found: {source_path}")
            continue
        
        # If the destination is empty, keep in root
        if destination == "":
            print(f"File kept in root: {source}")
            continue
        
        # Create the destination directory if it does not exist
        dest_dir = os.path.join(ROOT_DIR, destination)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        # Full destination path
        dest_path = os.path.join(dest_dir, os.path.basename(source_path))
        
        # Copy the file (instead of moving) to keep a copy in the original location
        shutil.copy2(source_path, dest_path)
        print(f"Copied: {source} → {destination}")

def identify_obsolete_dirs():
    """Identifies potentially obsolete directories"""
    obsolete = []
    for dir_name in POTENTIAL_OBSOLETE_DIRS:
        dir_path = os.path.join(ROOT_DIR, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            obsolete.append(dir_name)
    
    return obsolete

def main():
    # Create the directory structure
    create_directory_structure(ROOT_DIR, STRUCTURE)
    
    # Move essential files
    move_essential_files()
    
    # Identify obsolete directories
    obsolete_dirs = identify_obsolete_dirs()
    
    print("\n=== Reorganization Completed ===")
    print("\nPotentially obsolete directories:")
    for dir_name in obsolete_dirs:
        print(f"- {dir_name}")
    
    print("\nNext steps:")
    print("1. Verify that all essential files were copied correctly")
    print("2. Update the startup scripts to reflect the new structure")
    print("3. Review the potentially obsolete directories and decide which can be removed")
    print("4. Run tests to ensure the system works with the new structure")

if __name__ == "__main__":
    main()