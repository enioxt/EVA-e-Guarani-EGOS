#!/usr/bin/env python3
python
import os
import shutil
from datetime import datetime
import sys

# Root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Get timestamp for obsolete files folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OBSOLETE_DIR = os.path.join(ROOT_DIR, f"obsolete_files_{timestamp}")

# List of potentially obsolete folders
OBSOLETE_CANDIDATES = [
    "Old Bots",
    "New folder",
    "old_files_20250301_171050",
    "backup_20250301_171540",
    "quarantine",
    "quarantine",
    "unused_files",
    "archived_files",
    "[destination_directory]",
    "cache",
    "temp",
    "dockerfiles",
    "generated_images",
    "generated_videos",
    "processed_images",
    "infinity_ai.egg-info",
    "transfers",
    "downloads"
]

# Duplicate folders (when we have multiple folders with similar functions)
DUPLICATE_GROUPS = [
    ["backup", "backups", "backup_quantum"], 
    ["bot", "Old Bots"],
    ["quarantine", "quarantine"],
    ["docs", "examples", "static"]
]

def analyze_directory(dir_path):
    """Analyzes a directory and returns statistics about its usage"""
    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        return None
    
    total_files = 0
    total_size = 0
    file_extensions = {}
    last_modified = None
    
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_files += 1
            
            # Calculate size
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                total_size += size
            
            # Determine extension
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext:
                file_extensions[ext] = file_extensions.get(ext, 0) + 1
            
            # Check last modification
            if os.path.exists(file_path):
                mod_time = os.path.getmtime(file_path)
                if last_modified is None or mod_time > last_modified:
                    last_modified = mod_time
    
    if last_modified:
        last_modified_date = datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d %H:%M:%S')
    else:
        last_modified_date = "Unknown"
    
    # Sort extensions by quantity
    sorted_extensions = sorted(file_extensions.items(), key=lambda x: x[1], reverse=True)
    top_extensions = sorted_extensions[:5] if sorted_extensions else []
    
    return {
        "total_files": total_files,
        "total_size": total_size,
        "last_modified": last_modified_date,
        "top_extensions": top_extensions
    }

def move_to_obsolete(dir_path):
    """Moves a directory to the obsolete files folder"""
    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        return False
    
    # Create obsolete files folder if it doesn't exist
    if not os.path.exists(OBSOLETE_DIR):
        os.makedirs(OBSOLETE_DIR)
    
    # Move the directory
    dir_name = os.path.basename(dir_path)
    dest_path = os.path.join(OBSOLETE_DIR, dir_name)
    try:
        shutil.move(dir_path, dest_path)
        return True
    except Exception as e:
        print(f"Error moving {dir_path}: {e}")
        return False

def format_size(size_bytes):
    """Formats the size in bytes to a readable representation"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def main():
    # Check command line arguments
    interactive_mode = True
    auto_cleanup = False
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        interactive_mode = False
        auto_cleanup = True
    
    # Analyze existing directories
    dir_stats = {}
    for dir_name in os.listdir(ROOT_DIR):
        dir_path = os.path.join(ROOT_DIR, dir_name)
        if os.path.isdir(dir_path) and not dir_name.startswith('.'):
            stats = analyze_directory(dir_path)
            if stats:
                dir_stats[dir_name] = stats
    
    # Identify candidates for removal
    obsolete_dirs = []
    for dir_name in OBSOLETE_CANDIDATES:
        dir_path = os.path.join(ROOT_DIR, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            obsolete_dirs.append(dir_name)
    
    # Identify duplicates
    duplicate_dirs = []
    for group in DUPLICATE_GROUPS:
        existing_in_group = []
        for dir_name in group:
            dir_path = os.path.join(ROOT_DIR, dir_name)
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                existing_in_group.append(dir_name)
        
        if len(existing_in_group) > 1:
            duplicate_dirs.append(existing_in_group)
    
    # Display results
    print("\n=== Directory Analysis ===")
    
    print("\nPotentially obsolete directories:")
    for dir_name in obsolete_dirs:
        stats = dir_stats.get(dir_name, {})
        files = stats.get("total_files", 0)
        size = format_size(stats.get("total_size", 0))
        last_mod = stats.get("last_modified", "Unknown")
        print(f"- {dir_name}: {files} files, {size}, last modification: {last_mod}")
    
    print("\nGroups of duplicate directories:")
    for i, group in enumerate(duplicate_dirs, 1):
        print(f"Group {i}:")
        for dir_name in group:
            stats = dir_stats.get(dir_name, {})
            files = stats.get("total_files", 0)
            size = format_size(stats.get("total_size", 0))
            print(f"  - {dir_name}: {files} files, {size}")
    
    # Processing
    if interactive_mode:
        print("\n=== Directory Cleanup ===")
        print("\nWhat would you like to do?")
        print("1. Move all obsolete directories to the archive")
        print("2. Select specific directories to move")
        print("3. Handle groups of duplicate directories")
        print("4. Exit without making changes")
        
        choice = input("\nChoose an option (1-4): ")
        
        if choice == "1":
            # Move all obsolete
            for dir_name in obsolete_dirs:
                dir_path = os.path.join(ROOT_DIR, dir_name)
                if move_to_obsolete(dir_path):
                    print(f"Moved: {dir_name} → obsolete_files_{timestamp}")
        
        elif choice == "2":
            # Select specific ones
            print("\nSelect directories to move (separated by comma):")
            for i, dir_name in enumerate(obsolete_dirs, 1):
                print(f"{i}. {dir_name}")
            
            selection = input("\nDirectory numbers (e.g., 1,3,5): ")
            selected_indices = [int(idx.strip()) - 1 for idx in selection.split(",") if idx.strip().isdigit()]
            
            for idx in selected_indices:
                if 0 <= idx < len(obsolete_dirs):
                    dir_name = obsolete_dirs[idx]
                    dir_path = os.path.join(ROOT_DIR, dir_name)
                    if move_to_obsolete(dir_path):
                        print(f"Moved: {dir_name} → obsolete_files_{timestamp}")
        
        elif choice == "3":
            # Handle duplicates
            for i, group in enumerate(duplicate_dirs, 1):
                print(f"\nGroup {i}: {', '.join(group)}")
                print("Which directory would you like to keep? The others will be moved to the archive.")
                for j, dir_name in enumerate(group, 1):
                    print(f"{j}. {dir_name}")
                
                keep_choice = input(f"Directory to keep (1-{len(group)}): ")
                if keep_choice.isdigit() and 1 <= int(keep_choice) <= len(group):
                    keep_idx = int(keep_choice) - 1
                    for j, dir_name in enumerate(group):
                        if j != keep_idx:
                            dir_path = os.path.join(ROOT_DIR, dir_name)
                            if move_to_obsolete(dir_path):
                                print(f"Moved: {dir_name} → obsolete_files_{timestamp}")
    
    elif auto_cleanup:
        # Automatic mode: move all obsolete
        for dir_name in obsolete_dirs:
            dir_path = os.path.join(ROOT_DIR, dir_name)
            if move_to_obsolete(dir_path):
                print(f"Moved: {dir_name} → obsolete_files_{timestamp}")
        
        # Handle duplicates (keep the first of each group)
        for group in duplicate_dirs:
            for j, dir_name in enumerate(group):
                if j > 0:  # Keep the first, move the others
                    dir_path = os.path.join(ROOT_DIR, dir_name)
                    if move_to_obsolete(dir_path):
                        print(f"Moved (duplicate): {dir_name} → obsolete_files_{timestamp}")
    
    print("\n=== Cleanup Completed ===")
    if os.path.exists(OBSOLETE_DIR):
        print(f"\nObsolete directories have been moved to: {OBSOLETE_DIR}")
        print("If the system continues to function correctly, you can delete this directory later.")
    else:
        print("\nNo directories were moved.")
    
    print("\nNext steps:")
    print("1. Check if the system works correctly with the new structure")
    print("2. Update the documentation to reflect the changes")
    print("3. If everything is working, you can delete the obsolete files directory")

if __name__ == "__main__":
    main()