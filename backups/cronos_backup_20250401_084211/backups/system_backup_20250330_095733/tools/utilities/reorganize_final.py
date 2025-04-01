#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reorganize Workspace (Final) - Final script to reorganize the structure
This script moves all remaining folders in the root to the modular structure of EVA & GUARANI.

Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("data/logs/system/reorganization_final.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Current date and time for directory names
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Directories that should remain in the root
KEEP_IN_ROOT = [
    "core", "modules", "integrations", "tools", "docs", "tests", "ui", "data",
    "backup", "quarantine", "venv", "__pycache__",
    ".git", ".github", ".vscode", ".obsidian", ".bolt", ".cursor"
]

# Directories to move to appropriate structures
MOVE_MAPPING = {
    # Core
    "config": "core/config",
    "EGOS": "core/egos",
    "ethics": "core/ethik",
    "ethik-core": "core/ethik/legacy",
    "src": "core/src",
    
    # Modules
    "quantum": "modules/quantum",
    "eliza": "modules/eliza",
    "eliza_os": "modules/eliza/os",
    "blockchain": "modules/blockchain",
    "gamification": "modules/gamification",
    
    # Integrations
    "bot": "integrations/bots",
    "temp_bot": "integrations/bots/temp",
    "extensions": "integrations/extensions",
    "prompts": "integrations/prompts",
    "QUANTUM_PROMPTS": "integrations/prompts/quantum",
    
    # Tools
    "utils": "tools/utils",
    "system_analysis": "tools/analysis",
    
    # Data
    "personas": "data/personas",
    "logs": "data/logs",
    "story_elements": "data/story_elements",
    "examples": "data/examples"
}

# Backup directories to consolidate
BACKUP_DIRS = [
    "backup_20250301_171540",
    "backup_before_reorganization",
    "backup_pre_reorganization_20250319",
    "backup_quantum",
    "backups",
    "essential_backup_20250228_164242",
    "shared_egos_20250301_163205",
    "old_files_20250301_171050"
]

# Quarantine directories to consolidate
QUARANTINE_DIRS = [
    "quarantine",
    "quarantine_20250319",
    "quarantine_duplicates_20250319",
    "quarantine_folders_20250319"
]

def move_directory(source, destination):
    """Move a directory to the specified destination"""
    source_path = ROOT_DIR / source
    dest_path = ROOT_DIR / destination
    
    # Check if the source directory exists
    if not source_path.exists() or not source_path.is_dir():
        logging.warning(f"Source directory not found: {source}")
        return False
        
    logging.info(f"Processing directory: {source}")
    
    # Create destination directory if it doesn't exist
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if dest_path.exists():
            # If the destination already exists, create a folder to merge content
            merge_dir = dest_path / f"merged_from_{source}"
            merge_dir.mkdir(exist_ok=True)
            
            # Copy content to the merge folder
            for item in source_path.iterdir():
                target = merge_dir / item.name
                if item.is_dir():
                    if target.exists():
                        logging.warning(f"Subdirectory {item.name} already exists in destination, skipping")
                    else:
                        shutil.copytree(item, target)
                else:
                    if not target.exists():
                        shutil.copy2(item, target)
            
            # Remove original directory
            shutil.rmtree(source_path)
            logging.info(f"Content from {source} merged into {destination}/merged_from_{source}")
        else:
            # If the destination doesn't exist, move directly
            shutil.move(str(source_path), str(dest_path))
            logging.info(f"Directory {source} moved to {destination}")
        
        return True
        
    except Exception as e:
        logging.error(f"Error moving {source} to {destination}: {str(e)}")
        return False

def consolidate_backups():
    """Consolidate all backup directories into backup/history"""
    logging.info("Consolidating backup directories...")
    
    backup_dir = ROOT_DIR / "backup" / "history"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    for source in BACKUP_DIRS:
        move_directory(source, f"backup/history/{source}")
        
    logging.info("Backup consolidation completed")

def consolidate_quarantines():
    """Consolidate all quarantine directories into quarantine/"""
    logging.info("Consolidating quarantine directories...")
    
    quarantine_dir = ROOT_DIR / "quarantine"
    quarantine_dir.mkdir(exist_ok=True)
    
    for source in QUARANTINE_DIRS:
        if source != "quarantine":  # Do not move the quarantine folder itself
            move_directory(source, f"quarantine/{source}")
            
    logging.info("Quarantine consolidation completed")

def move_remaining_directories():
    """Move all remaining directories in the root to quarantine/misc"""
    logging.info("Processing remaining directories in the root...")
    
    misc_dir = ROOT_DIR / "quarantine" / "misc"
    misc_dir.mkdir(parents=True, exist_ok=True)
    
    moved_count = 0
    skipped_count = 0
    
    for item in ROOT_DIR.glob("*"):
        if not item.is_dir():
            continue
            
        dir_name = item.name
        
        # Ignore directories that should remain in the root
        if dir_name in KEEP_IN_ROOT:
            logging.debug(f"Keeping directory in root: {dir_name}")
            skipped_count += 1
            continue
            
        # Check if the directory has already been mapped
        if dir_name in MOVE_MAPPING or dir_name in BACKUP_DIRS or dir_name in QUARANTINE_DIRS:
            logging.debug(f"Directory already processed previously: {dir_name}")
            continue
            
        # Move to the misc folder in quarantine
        dest_path = misc_dir / dir_name
        
        if dest_path.exists():
            # If it already exists in quarantine, rename with timestamp
            new_dest = misc_dir / f"{dir_name}_{TIMESTAMP}"
            logging.info(f"Moving {dir_name} to quarantine/misc/{dir_name}_{TIMESTAMP}")
            try:
                shutil.move(str(item), str(new_dest))
                moved_count += 1
            except Exception as e:
                logging.error(f"Error moving {dir_name} to quarantine/misc: {str(e)}")
        else:
            # Move directly
            logging.info(f"Moving {dir_name} to quarantine/misc/{dir_name}")
            try:
                shutil.move(str(item), str(dest_path))
                moved_count += 1
            except Exception as e:
                logging.error(f"Error moving {dir_name} to quarantine/misc: {str(e)}")
    
    logging.info(f"Processing of remaining directories completed: {moved_count} moved, {skipped_count} kept in root")

def generate_report():
    """Generate a final reorganization report"""
    logging.info("Generating final reorganization report...")
    
    report_dir = ROOT_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"reorganization_final_report_{TIMESTAMP}.md"
    
    # Count directories in main structures
    structure_counts = {}
    for category in ["core", "modules", "integrations", "tools", "docs", "tests", "ui", "data"]:
        category_path = ROOT_DIR / category
        if category_path.exists():
            subdirs = [d for d in category_path.glob("*") if d.is_dir()]
            structure_counts[category] = len(subdirs)
    
    # Count backup and quarantine directories
    backup_path = ROOT_DIR / "backup"
    quarantine_path = ROOT_DIR / "quarantine"
    
    backup_count = len([d for d in backup_path.glob("**/*") if d.is_dir()]) if backup_path.exists() else 0
    quarantine_count = len([d for d in quarantine_path.glob("**/*") if d.is_dir()]) if quarantine_path.exists() else 0
    
    # Generate report
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# Final Reorganization Report - EVA & GUARANI\n\n")
            f.write(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            f.write("## System Structure\n\n")
            for category, count in structure_counts.items():
                f.write(f"- **{category}**: {count} subdirectories\n")
            
            f.write(f"\n- **backup**: {backup_count} directories\n")
            f.write(f"- **quarantine**: {quarantine_count} directories\n")
            
            f.write("\n## Directories in the Root\n\n")
            root_dirs = [d.name for d in ROOT_DIR.glob("*") if d.is_dir()]
            for d in sorted(root_dirs):
                f.write(f"- {d}\n")
            
            f.write("\n## Recommendations\n\n")
            f.write("1. Check if there are important directories in the quarantine/misc area\n")
            f.write("2. Update references to directories that were moved in the code\n")
            f.write("3. Run system integrity tests\n")
            f.write("4. Consider safe removal of old backups after validation\n")
            
            f.write("\n---\n\n")
            f.write("_Report generated by the final reorganization script_\n")
            f.write("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")
        
        logging.info(f"Report generated successfully: {report_path}")
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")

def main():
    """Main execution function"""
    logging.info("=== STARTING FINAL WORKSPACE REORGANIZATION ===")
    
    try:
        # First move specific directories to appropriate structures
        for source, destination in MOVE_MAPPING.items():
            move_directory(source, destination)
        
        # Consolidate backup directories
        consolidate_backups()
        
        # Consolidate quarantine directories
        consolidate_quarantines()
        
        # Move remaining directories to quarantine/misc
        move_remaining_directories()
        
        # Generate report
        generate_report()
        
        logging.info("=== FINAL REORGANIZATION SUCCESSFULLY COMPLETED ===")
        
    except Exception as e:
        logging.error(f"Error during final reorganization: {str(e)}")
        logging.info("=== FINAL REORGANIZATION INTERRUPTED WITH ERRORS ===")

if __name__ == "__main__":
    main()