#!/usr/bin/env python3
"""
EVA & GUARANI - Project Structure Optimization Tool
This script helps identify unused modules, large directories, and provides
recommendations for organization to improve performance.
"""

import os
import sys
import json
from pathlib import Path
import shutil
from datetime import datetime

# Configuration
EXCLUDE_DIRS = [
    "__pycache__",
    ".git", 
    ".vscode", 
    ".pytest_cache", 
    "venv",
    ".obsidian",
    ".cursor"
]

ARCHIVE_CANDIDATES = [
    "backup",
    "quarantine",
    "docs/archived",
    "docs/BACKUPS",
]

WORKING_MODULES = [
    "core/atlas",
    "core/nexus",
    "core/cronos",
    "core/ethik",
    "tools",
    "modules",
    "ui",
    "integrations"
]

def get_dir_size(path):
    """Calculate directory size recursively."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def human_size(size_bytes):
    """Convert bytes to human-readable format."""
    if size_bytes == 0:
        return "0B"
    size_names = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def analyze_project_structure(root_dir):
    """Analyze project structure and identify optimization opportunities."""
    print(f"\n{'-'*80}")
    print(f"EVA & GUARANI - Project Structure Analysis")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'-'*80}\n")
    
    root_path = Path(root_dir)
    
    # Analyze directory sizes
    print("Directory Size Analysis:")
    print(f"{'Directory':<40} {'Size':<15} {'Files':<10}")
    print(f"{'-'*70}")
    
    dir_sizes = []
    for item in sorted(root_path.glob('*')):
        if item.is_dir() and item.name not in EXCLUDE_DIRS:
            size = get_dir_size(item)
            file_count = sum(1 for _ in item.glob('**/*') if _.is_file())
            dir_sizes.append((item.name, size, file_count))
            print(f"{item.name:<40} {human_size(size):<15} {file_count:<10}")
    
    # Archive candidates
    print("\nArchive Candidates (Consider moving to external storage):")
    for dir_name in ARCHIVE_CANDIDATES:
        dir_path = root_path / dir_name
        if dir_path.exists():
            size = get_dir_size(dir_path)
            print(f"- {dir_name:<40} {human_size(size):<15}")
    
    # Working modules
    print("\nActive Development Modules:")
    for module in WORKING_MODULES:
        module_path = root_path / module
        if module_path.exists():
            size = get_dir_size(module_path)
            print(f"- {module:<40} {human_size(size):<15}")
    
    # Find duplicate files (by name only, not content)
    print("\nPotential Duplicate Files (by name):")
    all_files = {}
    for path in root_path.glob('**/*'):
        if path.is_file() and path.name != ".DS_Store" and not any(exclude in str(path) for exclude in EXCLUDE_DIRS):
            if path.name in all_files:
                all_files[path.name].append(str(path))
            else:
                all_files[path.name] = [str(path)]
    
    duplicates = {name: paths for name, paths in all_files.items() if len(paths) > 1}
    if duplicates:
        for name, paths in list(duplicates.items())[:10]:  # Show only first 10
            print(f"- {name}: {len(paths)} occurrences")
    else:
        print("- No potential duplicates found")
    
    # Optimization recommendations
    print("\nOptimization Recommendations:")
    print("1. Archive unused directories like 'backup' and 'quarantine'")
    print("2. Consider moving docs to a separate repository or external storage")
    print("3. Implement workspace settings to exclude large directories from indexing")
    print("4. Focus on specific modules during development rather than entire codebase")
    print("5. Use Git sparse-checkout to work with specific directories")
    
    # Create VSCode workspace file
    create_workspace_file(root_path, dir_sizes)
    
    print(f"\n{'-'*80}")
    print("Analysis complete. A VSCode workspace file has been created to help you")
    print("focus on specific modules during development.")
    print(f"{'-'*80}\n")

def create_workspace_file(root_path, dir_sizes):
    """Create a VSCode workspace file to help focus on specific modules."""
    workspace = {
        "folders": [],
        "settings": {
            "files.exclude": {
                "**/__pycache__": True,
                "**/.pytest_cache": True,
                "**/*.pyc": True,
                ".git": True,
                ".vscode": True,
                ".coverage": True,
                "venv": True
            },
            "search.exclude": {
                "venv/**": True,
                "**/__pycache__/**": True,
                "**/.pytest_cache/**": True,
                "docs/**": True,
                "backup/**": True,
                "quarantine/**": True
            }
        }
    }
    
    # Add main workspace folder
    workspace["folders"].append({
        "name": "EVA & GUARANI",
        "path": "."
    })
    
    # Add separate entries for core modules
    for module in ["core/atlas", "core/nexus", "core/cronos", "core/ethik"]:
        module_path = root_path / module
        if module_path.exists():
            workspace["folders"].append({
                "name": module.split('/')[-1].upper(),
                "path": module
            })
    
    # Add other important directories
    for dir_name in ["tools", "ui", "modules", "integrations"]:
        dir_path = root_path / dir_name
        if dir_path.exists():
            workspace["folders"].append({
                "name": dir_name.upper(),
                "path": dir_name
            })
    
    # Write workspace file
    with open(root_path / "eva_guarani.code-workspace", "w") as f:
        json.dump(workspace, f, indent=4)
    
    print("\nCreated VSCode workspace file: eva_guarani.code-workspace")

if __name__ == "__main__":
    # Use current directory if no argument is provided
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    analyze_project_structure(root_dir) 