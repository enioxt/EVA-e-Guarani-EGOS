#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Sandbox Environment Setup Script
This script creates the directory structure and necessary files for the sandbox environment
"""

import os
import sys
import shutil
from pathlib import Path

# Directory structure for the sandbox
DIRECTORY_STRUCTURE = {
    "api": {
        "flask_api": {},
        "django_api": {
            "sandbox_project": {
                "sandbox_app": {}
            }
        }
    },
    "frontend": {
        "html_basic": {},
        "react_app": {
            "public": {},
            "src": {
                "components": {},
                "styles": {}
            }
        },
        "vue_app": {
            "public": {},
            "src": {
                "components": {},
                "assets": {}
            }
        }
    },
    "examples": {
        "api_usage": {},
        "frontend_examples": {},
        "integration": {}
    },
    "data": {
        "sample": {},
        "temp": {}
    },
    "docs": {
        "diagrams": {},
        "api": {},
        "tutorials": {}
    }
}

def create_directory_structure(base_path, structure, level=0):
    """
    Recursively creates the directory structure
    
    Args:
        base_path (Path): Base path where the structure will be created
        structure (dict): Dictionary representing the directory structure
        level (int): Current depth level (for output formatting)
    """
    for name, subdir in structure.items():
        dir_path = base_path / name
        
        # Create directory if it doesn't exist
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"{'  ' * level}✓ Created directory: {name}")
        else:
            print(f"{'  ' * level}• Directory already exists: {name}")
        
        # Create subdirectory structure
        if subdir:
            create_directory_structure(dir_path, subdir, level + 1)

def create_placeholder_files(base_path):
    """
    Creates placeholder files (README.md) in empty directories
    
    Args:
        base_path (Path): Base path where files will be created
    """
    for root, dirs, files in os.walk(base_path):
        # Convert path to Path object
        root_path = Path(root)
        
        # If directory is empty, create a README.md file
        if not files and root_path != base_path:
            rel_path = root_path.relative_to(base_path)
            readme_path = root_path / "README.md"
            
            # Only create if file doesn't exist
            if not readme_path.exists():
                with open(readme_path, "w", encoding="utf-8") as f:
                    # Get directory name for title
                    dir_name = root_path.name
                    
                    f.write(f"# {dir_name.capitalize()}\n\n")
                    f.write(f"This directory is part of the EVA & GUARANI Sandbox environment.\n\n")
                    f.write(f"Path: `{rel_path}`\n\n")
                    f.write("## Description\n\n")
                    f.write("Add a description about the files and purpose of this directory here.\n\n")
                    f.write("## Usage Examples\n\n")
                    f.write("Add examples of how to use the resources in this directory here.\n")
                
                print(f"✓ Created placeholder file: {rel_path}/README.md")

def check_existing_files(base_path):
    """
    Checks if important files have already been created
    
    Args:
        base_path (Path): Base path to check
        
    Returns:
        dict: Dictionary with status of each important file
    """
    files_to_check = {
        "README.md": base_path / "README.md",
        "requirements.txt": base_path / "requirements.txt",
        "run_sandbox.py": base_path / "run_sandbox.py",
        "run_sandbox.bat": base_path / "run_sandbox.bat",
        "app.py (Flask API)": base_path / "api" / "flask_api" / "app.py",
        "index.html": base_path / "frontend" / "html_basic" / "index.html",
        "basic_integration.py": base_path / "examples" / "basic_integration.py"
    }
    
    result = {}
    for name, path in files_to_check.items():
        result[name] = path.exists()
        status = "✓" if path.exists() else "✗"
        print(f"{status} {name}")
    
    return result

def main():
    """Main function for sandbox environment setup"""
    # Sandbox base path (current directory where script is executed)
    sandbox_path = Path(__file__).resolve().parent
    
    print("\n==== EVA & GUARANI - Sandbox Environment Setup ====\n")
    
    # Create directory structure
    print("Creating directory structure:")
    create_directory_structure(sandbox_path, DIRECTORY_STRUCTURE)
    
    # Check important files
    print("\nChecking important files:")
    existing_files = check_existing_files(sandbox_path)
    
    # Create placeholder files in empty directories
    print("\nCreating placeholder files in empty directories:")
    create_placeholder_files(sandbox_path)
    
    # Summary
    missing_files = [name for name, exists in existing_files.items() if not exists]
    
    print("\n==== Setup completed ====")
    
    if missing_files:
        print("\nImportant files not yet created:")
        for name in missing_files:
            print(f"- {name}")
        print("\nRun the appropriate scripts to create these files.")
    else:
        print("\nAll important files have been created.")
    
    print("\nTo start the sandbox environment, run:")
    print("  - On Windows: run_sandbox.bat")
    print("  - On Linux/Mac: python run_sandbox.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 