#!/usr/bin/env python3
"""
EVA & GUARANI - Reference Management Tool
This tool helps manage references to large directories without having them in the main project.
It creates symbolic links or moves folders to external locations.
"""

import os
import sys
import shutil
from pathlib import Path
import argparse
import platform
import subprocess

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        if platform.system() == 'Windows':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # For Unix-like systems, simplify to avoid OS-specific APIs
            # This is a simplification that works for most cases
            return os.access('/', os.W_OK)
    except:
        return False

def create_symlink(source, target):
    """Create a symbolic link from source to target."""
    source_path = Path(source).resolve()
    target_path = Path(target).resolve()
    
    if not target_path.exists():
        print(f"Error: Target directory '{target}' does not exist.")
        return False

    # Check if the source already exists as a directory
    if source_path.exists() and source_path.is_dir():
        # Back up the existing directory
        backup_name = f"{source_path}.backup_{os.path.basename(source)}"
        print(f"Backing up existing directory: {source} → {backup_name}")
        source_path.rename(backup_name)
    
    # Create the symbolic link
    try:
        if platform.system() == 'Windows':
            # Windows requires different commands and admin privileges for symlinks
            if is_admin():
                if target_path.is_dir():
                    cmd = f'mklink /D "{source_path}" "{target_path}"'
                else:
                    cmd = f'mklink "{source_path}" "{target_path}"'
                subprocess.run(cmd, shell=True, check=True)
            else:
                print("Error: Administrator privileges required to create symbolic links on Windows.")
                print("Please run this script as administrator.")
                return False
        else:
            # Unix-like systems
            os.symlink(target_path, source_path)
        
        print(f"✓ Symbolic link created: {source} → {target}")
        return True
    except Exception as e:
        print(f"Error creating symbolic link: {e}")
        return False

def move_directory(source, target, create_link=True):
    """Move a directory to another location and optionally create a symbolic link."""
    source_path = Path(source).resolve()
    target_parent = Path(target).resolve()
    
    if not source_path.exists():
        print(f"Error: Source directory '{source}' does not exist.")
        return False
    
    if not target_parent.exists():
        print(f"Creating target directory: {target_parent}")
        target_parent.mkdir(parents=True, exist_ok=True)
    
    # Determine the final target path
    final_target = target_parent / source_path.name
    
    # Move the directory
    try:
        print(f"Moving directory: {source} → {final_target}")
        if final_target.exists():
            print(f"Warning: Target already exists. Using unique name.")
            final_target = target_parent / f"{source_path.name}_{os.path.basename(source)}"
        
        shutil.move(str(source_path), str(final_target))
        print(f"✓ Directory moved: {final_target}")
        
        # Create symbolic link if requested
        if create_link:
            create_symlink(source, final_target)
        
        return True
    except Exception as e:
        print(f"Error moving directory: {e}")
        return False

def list_large_directories(root_dir="."):
    """List large directories in the project."""
    root_path = Path(root_dir)
    print("\nLarge directories in project:")
    print(f"{'Directory':<40} {'Size':<15}")
    print(f"{'-'*60}")
    
    for item in sorted(root_path.glob('*')):
        if item.is_dir() and not str(item).startswith('.'):
            try:
                size = sum(f.stat().st_size for f in item.glob('**/*') if f.is_file())
                size_mb = size / (1024*1024)
                
                if size_mb > 10:  # Only show directories larger than 10MB
                    print(f"{str(item):<40} {size_mb:.2f} MB")
            except Exception as e:
                print(f"{str(item):<40} Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Manage references to large directories in EVA & GUARANI project")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Link command
    link_parser = subparsers.add_parser("link", help="Create a symbolic link")
    link_parser.add_argument("source", help="Source directory in the project")
    link_parser.add_argument("target", help="Target directory outside the project")
    
    # Move command
    move_parser = subparsers.add_parser("move", help="Move a directory and create a link")
    move_parser.add_argument("source", help="Source directory in the project")
    move_parser.add_argument("target", help="Target directory outside the project")
    move_parser.add_argument("--no-link", action="store_true", help="Don't create a symbolic link after moving")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List large directories")
    
    # Setup command (setup reference directories)
    setup_parser = subparsers.add_parser("setup", help="Set up reference directories")
    setup_parser.add_argument("--refs-dir", default="../EVA_REFS", help="Directory to store references")
    
    args = parser.parse_args()
    
    if args.command == "link":
        create_symlink(args.source, args.target)
    
    elif args.command == "move":
        move_directory(args.source, args.target, not args.no_link)
    
    elif args.command == "list":
        list_large_directories()
    
    elif args.command == "setup":
        # Create reference directories structure
        refs_dir = Path(args.refs_dir)
        
        print(f"\n{'-'*80}")
        print(f"Setting up reference directories in: {refs_dir}")
        print(f"{'-'*80}\n")
        
        try:
            # Create main refs directory
            refs_dir.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories for different types of references
            (refs_dir / "docs").mkdir(exist_ok=True)
            (refs_dir / "apps").mkdir(exist_ok=True)
            (refs_dir / "archives").mkdir(exist_ok=True)
            
            print("✓ Reference directories created successfully")
            
            # Check for large directories to suggest moving
            large_dirs = ["docs", "eva-atendimento"]
            
            for dir_name in large_dirs:
                if Path(dir_name).exists():
                    dir_type = "docs" if dir_name == "docs" else "apps"
                    target = refs_dir / dir_type / dir_name
                    
                    print(f"\nLarge directory found: {dir_name}")
                    print(f"Suggested command to move it:")
                    print(f"python tools/manage_references.py move {dir_name} {refs_dir}/{dir_type}")
            
            print("\nAfter moving directories, they will still be accessible at their original location")
            print("but won't be indexed by VSCode/Cursor during development.")
            
        except Exception as e:
            print(f"Error setting up reference directories: {e}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 