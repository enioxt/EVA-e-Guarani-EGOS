#!/usr/bin/env python3
python
import os
import sys
import subprocess
from datetime import datetime


def run_script(script_name):
    """Runs a Python script and returns the exit code"""
    print(f"\n=== Running {script_name} ===\n")
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    return result.returncode


def create_backup():
    """Creates a backup of the current state before reorganization"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"pre_reorganization_backup_{timestamp}"
    print(f"\n=== Creating backup in {backup_dir} ===\n")

    # Use the existing backup script if available
    if os.path.exists("quantum_backup_system.py"):
        subprocess.run([sys.executable, "quantum_backup_system.py", "--output", backup_dir])
        return True

    # Simplified manual backup if the script is not available
    import shutil

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # List important files for backup
    important_files = [
        "egos_core.py",
        "ethik_core.js",
        "quantum_core_essence.py",
        "EVA_GUARANI_v7.0.md",
        "start_egos.bat",
        "start_egos.sh",
        "README.md",
        "SUBSYSTEMS.md",
        "requirements.txt",
        ".env",
    ]

    # Copy important files
    for file_name in important_files:
        if os.path.exists(file_name):
            shutil.copy2(file_name, os.path.join(backup_dir, file_name))

    return True


def main():
    """Main function that coordinates the reorganization process"""
    print("====================================================")
    print("  EVA & GUARANI SYSTEM REORGANIZATION - EGOS")
    print("====================================================")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis script will reorganize the system's file structure.")
    print("The process includes the following steps:")
    print("1. Create a backup of the current state")
    print("2. Create new directory structure")
    print("3. Update paths in files")
    print("4. Update documentation")
    print("5. Identify and move obsolete directories")

    proceed = input("\nDo you want to proceed with the reorganization? (y/n): ")
    if proceed.lower() != "y":
        print("Reorganization canceled.")
        return

    # Create backup
    if not create_backup():
        print("Failed to create backup. Aborting reorganization.")
        return

    # Sequence of scripts to be executed
    scripts = [
        "organize_egos.py",  # Creates new structure
        "update_paths.py",  # Updates paths
        "update_docs.py",  # Updates documentation
        "cleanup_obsolete.py",  # Cleans up obsolete directories (interactive mode)
    ]

    # Execute scripts in sequence
    success = True
    for script in scripts:
        if not os.path.exists(script):
            print(f"Error: Script {script} not found.")
            success = False
            break

        exit_code = run_script(script)
        if exit_code != 0:
            print(f"Error: Script {script} failed with code {exit_code}.")
            success = False
            break

    # Final result
    print("\n====================================================")
    if success:
        print("✅ Reorganization completed successfully!")
        print("\nNext steps:")
        print("1. Verify that the system works correctly with the new structure")
        print(
            "2. Run './start_egos.bat' (Windows) or './start_egos.sh' (Linux/Mac) to start the system"
        )
        print("3. If you encounter issues, a backup was created and can be restored")
    else:
        print("❌ Reorganization encountered errors during the process.")
        print("Refer to the messages above to identify the issue.")
        print(
            "A backup was created before the reorganization and can be used to restore the previous state."
        )

    print("====================================================")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")


if __name__ == "__main__":
    main()
