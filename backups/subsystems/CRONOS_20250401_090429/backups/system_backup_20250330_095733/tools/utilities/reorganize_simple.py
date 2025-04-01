#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reorganize Workspace (Simple) - Simplified script to reorganize the structure
This script moves unorganized folders to the modular structure of EVA & GUARANI.

Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import shutil
import logging
from pathlib import Path

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Mapping of folders to move
MOVE_MAPPING = {
    # Move to core/
    "config": "core/config",
    "EGOS": "core/egos",
    "ethics": "core/ethik",
    "ethik-core": "core/ethik/legacy",
    
    # Move to modules/
    "quantum": "modules/quantum",
    "eliza": "modules/eliza",
    "eliza_os": "modules/eliza/os",
    "blockchain": "modules/blockchain",
    "gamification": "modules/gamification",
    
    # Move to integrations/
    "bot": "integrations/bots",
    "temp_bot": "integrations/bots/temp",
    "extensions": "integrations/extensions",
    "prompts": "integrations/prompts",
    "QUANTUM_PROMPTS": "integrations/prompts/quantum",
    
    # Move to tools/
    "utils": "tools/utils",
    "system_analysis": "tools/analysis",
    
    # Move to data/
    "personas": "data/personas",
    "logs": "data/logs",
    "story_elements": "data/story_elements",
    "examples": "data/examples",
    
    # Move to docs/
    "reports": "docs/reports",
    
    # Move to backup/
    "backup_20250301_171540": "backup/history/backup_20250301_171540",
    "backup_before_reorganization": "backup/history/backup_before_reorganization",
    "backup_pre_reorganization_20250319": "backup/history/backup_pre_reorganization_20250319",
    "backup_quantum": "backup/history/backup_quantum",
    "backups": "backup/history/backups",
    "essential_backup_20250228_164242": "backup/history/essential_backup_20250228_164242",
    "shared_egos_20250301_163205": "backup/history/shared_egos_20250301_163205",
    "arquivos_antigos_20250301_171050": "backup/history/arquivos_antigos_20250301_171050",
    
    # Move to quarantine/
    "quarantine": "quarentena/quarantine",
    "quarentena_20250319": "quarentena/quarentena_20250319",
    "quarentena_duplicados_20250319": "quarentena/quarentena_duplicados_20250319",
    "quarentena_pastas_20250319": "quarentena/quarentena_pastas_20250319"
}

def move_directory(source, destination):
    """Move a directory to the destination"""
    source_path = ROOT_DIR / source
    dest_path = ROOT_DIR / destination
    
    # Check if the source directory exists
    if not source_path.exists():
        logging.warning(f"Directory not found: {source}")
        return False
        
    # Check if the destination directory already exists
    if dest_path.exists():
        logging.info(f"Destination directory already exists: {destination}")
        
        # If the destination exists, create a subdirectory to merge
        merge_dir = dest_path / f"merged_from_{source}"
        merge_dir.mkdir(exist_ok=True)
        
        # Move files to the subdirectory
        try:
            for item in source_path.iterdir():
                target = merge_dir / item.name
                if item.is_dir():
                    if target.exists():
                        # If the subdirectory already exists, skip
                        logging.warning(f"Subdirectory already exists at destination, skipping: {item.name}")
                    else:
                        shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)
                    
            # Remove original directory after copying
            shutil.rmtree(source_path)
            logging.info(f"Content from {source} merged into {destination}/merged_from_{source}")
            return True
        except Exception as e:
            logging.error(f"Error merging {source} into {destination}: {str(e)}")
            return False
    else:
        # If the destination does not exist, create the parent directory
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Move the directory
            shutil.move(str(source_path), str(dest_path))
            logging.info(f"Successfully moved: {source} -> {destination}")
            return True
        except Exception as e:
            logging.error(f"Error moving {source} to {destination}: {str(e)}")
            return False

def main():
    """Main execution function"""
    logging.info("Starting simplified directory reorganization")
    
    # Count successfully moved directories
    success_count = 0
    
    # Move each mapped directory
    for source, destination in MOVE_MAPPING.items():
        if move_directory(source, destination):
            success_count += 1
    
    # Final result
    logging.info(f"Reorganization complete: {success_count} of {len(MOVE_MAPPING)} directories moved successfully")
    
    # Create backup and quarantine directories if they don't exist
    (ROOT_DIR / "backup").mkdir(exist_ok=True)
    (ROOT_DIR / "quarentena").mkdir(exist_ok=True)

if __name__ == "__main__":
    main()