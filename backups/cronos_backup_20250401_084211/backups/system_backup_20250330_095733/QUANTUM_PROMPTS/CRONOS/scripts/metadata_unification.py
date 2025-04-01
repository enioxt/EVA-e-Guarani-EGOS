"""
EVA & GUARANI - METADATA Unification Script
Version: 1.0
"""

import json
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('metadata_unification.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class MetadataUnification:
    """Handles the unification process of the METADATA directory."""
    
    def __init__(self):
        """Initialize the unification process."""
        self.root_dir = Path("C:/Eva Guarani EGOS")
        self.source_dir = self.root_dir / "METADATA"
        self.target_dir = self.root_dir / "QUANTUM_PROMPTS/METADATA"
        self.backup_dir = None
        self.metrics = {
            "files_processed": 0,
            "directories_created": 0,
            "bytes_transferred": 0,
            "errors_encountered": 0
        }
        
    def create_backup(self) -> bool:
        """Create a backup of the METADATA directory.
        
        Returns:
            bool: True if backup was successful
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.backup_dir = self.root_dir / f"quarantine/METADATA_backup_{timestamp}"
            
            logger.info(f"Creating backup at {self.backup_dir}")
            shutil.copytree(self.source_dir, self.backup_dir)
            
            # Verify backup
            source_files = set(p.relative_to(self.source_dir) for p in self.source_dir.rglob("*"))
            backup_files = set(p.relative_to(self.backup_dir) for p in self.backup_dir.rglob("*"))
            
            if source_files == backup_files:
                logger.info("Backup verification successful")
                return True
            else:
                logger.error("Backup verification failed")
                return False
                
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            return False
            
    def create_target_structure(self) -> bool:
        """Create the target directory structure.
        
        Returns:
            bool: True if structure creation was successful
        """
        try:
            directories = [
                "core",
                "config",
                "scripts",
                "tests",
                "docs",
                "backups",
                "metrics"
            ]
            
            for dir_name in directories:
                dir_path = self.target_dir / dir_name
                dir_path.mkdir(parents=True, exist_ok=True)
                self.metrics["directories_created"] += 1
                logger.info(f"Created directory: {dir_path}")
                
            return True
            
        except Exception as e:
            logger.error(f"Error creating target structure: {str(e)}")
            return False
            
    def move_files(self) -> bool:
        """Move files to their new locations.
        
        Returns:
            bool: True if file movement was successful
        """
        try:
            # Move core files
            core_files = {
                "core/metadata_manager.py": "core/metadata_manager.py",
                "core/filesystem_monitor.py": "core/filesystem_monitor.py"
            }
            
            for src, dst in core_files.items():
                src_path = self.source_dir / src
                dst_path = self.target_dir / dst
                if src_path.exists():
                    shutil.copy2(src_path, dst_path)
                    self.metrics["files_processed"] += 1
                    self.metrics["bytes_transferred"] += src_path.stat().st_size
                    logger.info(f"Moved {src} to {dst}")
                    
            # Move test files
            test_files = [
                "tests/test_metadata_manager.py",
                "tests/test_filesystem_monitor.py"
            ]
            
            for test_file in test_files:
                src_path = self.source_dir / test_file
                dst_path = self.target_dir / test_file
                if src_path.exists():
                    shutil.copy2(src_path, dst_path)
                    self.metrics["files_processed"] += 1
                    self.metrics["bytes_transferred"] += src_path.stat().st_size
                    logger.info(f"Moved {test_file}")
                    
            # Move metrics
            metrics_file = "metrics/metrics-2025-03-29.json"
            src_path = self.source_dir / metrics_file
            dst_path = self.target_dir / metrics_file
            if src_path.exists():
                shutil.copy2(src_path, dst_path)
                self.metrics["files_processed"] += 1
                self.metrics["bytes_transferred"] += src_path.stat().st_size
                logger.info(f"Moved {metrics_file}")
                
            # Move configuration and documentation
            config_files = {
                "requirements.txt": "requirements.txt",
                "README.md": "docs/README.md"
            }
            
            for src, dst in config_files.items():
                src_path = self.source_dir / src
                dst_path = self.target_dir / dst
                if src_path.exists():
                    shutil.copy2(src_path, dst_path)
                    self.metrics["files_processed"] += 1
                    self.metrics["bytes_transferred"] += src_path.stat().st_size
                    logger.info(f"Moved {src} to {dst}")
                    
            # Move backup files to backups directory
            backup_files = [f for f in self.source_dir.glob("*.json") if "backup" in f.name.lower()]
            for backup_file in backup_files:
                dst_path = self.target_dir / "backups" / backup_file.name
                shutil.copy2(backup_file, dst_path)
                self.metrics["files_processed"] += 1
                self.metrics["bytes_transferred"] += backup_file.stat().st_size
                logger.info(f"Moved backup file: {backup_file.name}")
                
            return True
            
        except Exception as e:
            logger.error(f"Error moving files: {str(e)}")
            self.metrics["errors_encountered"] += 1
            return False
            
    def update_references(self) -> bool:
        """Update file references and imports.
        
        Returns:
            bool: True if reference updates were successful
        """
        try:
            files_to_update = [
                self.target_dir / "core/metadata_manager.py",
                self.target_dir / "core/filesystem_monitor.py",
                self.target_dir / "tests/test_metadata_manager.py",
                self.target_dir / "tests/test_filesystem_monitor.py"
            ]
            
            for file_path in files_to_update:
                if not file_path.exists():
                    continue
                    
                content = file_path.read_text(encoding='utf-8')
                
                # Update relative imports
                content = content.replace(
                    "from .metadata_manager",
                    "from QUANTUM_PROMPTS.METADATA.core.metadata_manager"
                )
                
                # Update other references
                content = content.replace(
                    "METADATA/",
                    "QUANTUM_PROMPTS/METADATA/"
                )
                
                file_path.write_text(content, encoding='utf-8')
                logger.info(f"Updated references in {file_path}")
                
            return True
            
        except Exception as e:
            logger.error(f"Error updating references: {str(e)}")
            self.metrics["errors_encountered"] += 1
            return False
            
    def generate_report(self) -> Dict:
        """Generate a report of the unification process.
        
        Returns:
            Dict: Report data
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "status": "success" if self.metrics["errors_encountered"] == 0 else "failed",
            "metrics": self.metrics,
            "backup_location": str(self.backup_dir) if self.backup_dir else None,
            "source_directory": str(self.source_dir),
            "target_directory": str(self.target_dir)
        }
        
        # Save report
        report_path = self.target_dir / "docs/unification_report.json"
        report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
        logger.info(f"Generated unification report at {report_path}")
        
        return report
        
    def execute(self) -> bool:
        """Execute the unification process.
        
        Returns:
            bool: True if the entire process was successful
        """
        logger.info("Starting METADATA unification process")
        
        # Create backup
        if not self.create_backup():
            logger.error("Backup creation failed. Aborting.")
            return False
            
        # Create target structure
        if not self.create_target_structure():
            logger.error("Target structure creation failed. Aborting.")
            return False
            
        # Move files
        if not self.move_files():
            logger.error("File movement failed. Aborting.")
            return False
            
        # Update references
        if not self.update_references():
            logger.error("Reference updates failed. Aborting.")
            return False
            
        # Generate report
        report = self.generate_report()
        
        success = report["status"] == "success"
        if success:
            logger.info("METADATA unification completed successfully")
        else:
            logger.error("METADATA unification completed with errors")
            
        return success

def main():
    """Main entry point for the unification script."""
    unification = MetadataUnification()
    success = unification.execute()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 