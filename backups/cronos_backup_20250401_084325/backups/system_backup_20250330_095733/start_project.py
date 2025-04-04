#!/usr/bin/env python3
"""
EVA & GUARANI - Project Launcher
This script sets up the optimal environment for working with the EVA & GUARANI project
by ensuring large directories are properly handled and launching the IDE with the right settings.
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


def clean_cache_files():
    """Remove __pycache__ directories to improve performance."""
    print("Cleaning up temporary files...")

    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                print(f"- Removed {pycache_path}")
            except Exception as e:
                print(f"  Error removing {pycache_path}: {e}")


def is_symlink(path):
    """Check if a path is a symbolic link."""
    return os.path.islink(path)


def check_directory_status(dir_name):
    """Check if a directory is optimized (symlink or excluded)."""
    if not os.path.exists(dir_name):
        print(f"- {dir_name}: Not found (excluded)")
        return True

    if is_symlink(dir_name):
        target = os.readlink(dir_name)
        print(f"- {dir_name}: OK (symbolic link → {target})")
        return True

    print(f"- {dir_name}: Found (regular directory)")
    return False


def find_ide():
    """Find the IDE (Cursor or VSCode) executable."""
    system = platform.system()

    if system == "Windows":
        # Check for Cursor
        cursor_paths = [
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "cursor", "Cursor.exe"),
            os.path.join(
                os.environ.get("APPDATA", ""), "Local", "Programs", "cursor", "Cursor.exe"
            ),
            r"C:\Program Files\cursor\Cursor.exe",
            r"C:\Program Files (x86)\cursor\Cursor.exe",
        ]

        for path in cursor_paths:
            if os.path.exists(path):
                return ("Cursor", path)

        # Check for VSCode
        vscode_paths = [
            os.path.join(
                os.environ.get("LOCALAPPDATA", ""), "Programs", "Microsoft VS Code", "Code.exe"
            ),
            os.path.join(
                os.environ.get("APPDATA", ""), "Local", "Programs", "Microsoft VS Code", "Code.exe"
            ),
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
        ]

        for path in vscode_paths:
            if os.path.exists(path):
                return ("VSCode", path)

    elif system == "Darwin":  # macOS
        # Check for Cursor
        cursor_paths = [
            "/Applications/Cursor.app/Contents/MacOS/Cursor",
            os.path.expanduser("~/Applications/Cursor.app/Contents/MacOS/Cursor"),
        ]

        for path in cursor_paths:
            if os.path.exists(path):
                return ("Cursor", path)

        # Check for VSCode
        vscode_paths = [
            "/Applications/Visual Studio Code.app/Contents/MacOS/Electron",
            os.path.expanduser("~/Applications/Visual Studio Code.app/Contents/MacOS/Electron"),
        ]

        for path in vscode_paths:
            if os.path.exists(path):
                return ("VSCode", path)

    elif system == "Linux":
        # Try to find in PATH
        try:
            cursor_path = subprocess.check_output(["which", "cursor"]).decode().strip()
            if cursor_path:
                return ("Cursor", cursor_path)
        except:
            pass

        try:
            code_path = subprocess.check_output(["which", "code"]).decode().strip()
            if code_path:
                return ("VSCode", code_path)
        except:
            pass

    return (None, None)


def launch_ide(ide_name, ide_path, workspace_file):
    """Launch the IDE with the workspace file."""
    try:
        if platform.system() == "Windows":
            subprocess.Popen([ide_path, workspace_file])
        else:
            subprocess.Popen([ide_path, workspace_file])

        print(f"Opening with {ide_name}...")
        return True
    except Exception as e:
        print(f"Error launching {ide_name}: {e}")
        return False


def main():
    """Main function to set up the environment and launch the project."""
    print("\n" + "=" * 80)
    print("EVA & GUARANI - Project Launcher")
    print("=" * 80 + "\n")

    # Check if workspace file exists
    workspace_file = "eva_guarani.code-workspace"
    if not os.path.exists(workspace_file):
        print("ERROR: Workspace file not found.")
        print("Please run setup first or make sure you're in the correct directory.")
        return False

    # Check if large directories are properly handled
    print("Checking project structure...")

    docs_handled = check_directory_status("docs")
    eva_handled = check_directory_status("eva-atendimento")

    if not docs_handled:
        print("\nWARNING: The docs directory is not optimized.")
        print("It's recommended to move it outside the project for better performance.")
        if platform.system() == "Windows":
            print("Run 'tools\\setup_references.ps1' as Administrator.")
        else:
            print("Run 'python tools/manage_references.py setup' and follow the instructions.")

    if not eva_handled:
        print("\nWARNING: The eva-atendimento directory is not optimized.")
        print("It's recommended to move it outside the project for better performance.")
        if platform.system() == "Windows":
            print("Run 'tools\\setup_references.ps1' as Administrator.")
        else:
            print("Run 'python tools/manage_references.py setup' and follow the instructions.")

    # Clean up cache files
    clean_cache_files()

    # Launch IDE
    print("\nLaunching project...")

    ide_name, ide_path = find_ide()
    if ide_name and ide_path:
        launch_ide(ide_name, ide_path, workspace_file)
    else:
        print("\nCould not find Cursor or VSCode automatically.")
        print(f'Please open "{workspace_file}" manually.')

    print("\n" + "=" * 80)
    print("EVA & GUARANI project is ready.")
    print("")
    print("If you need to work with large directories:")
    print("- Open them directly as separate workspaces")
    print("- Or temporarily modify the exclude settings in the workspace file")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = main()

    if platform.system() == "Windows":
        input("\nPress Enter to continue...")

    sys.exit(0 if success else 1)
