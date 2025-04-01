"""
EVA & GUARANI - ATLAS Unification Script
Version: 1.0
Date: 2025-03-30
Description: Automated unification script for ATLAS subsystem with visualization support
"""

import json
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import hashlib
import re

# Configuration
CONFIG = {
    "version": "1.0.0",
    "source_dirs": [
        "core/atlas",
        "web/atendimento/frontend_streamlit/pages",
        "web/atendimento/backend/data/telegram_bot/personas",
        "tools/integration"
    ],
    "target_dir": "QUANTUM_PROMPTS/ATLAS",
    "backup_dir": "quarantine/ATLAS_backup",
    "visualization_dir": "visualization_backup",
    "required_tools": [
        "node",
        "npm",
        "python"
    ]
}

class AtlasUnification:
    def __init__(self):
        self.logger = self._setup_logger()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = f"{CONFIG['backup_dir']}_{self.timestamp}"
        self.visualization_backup = f"{CONFIG['visualization_dir']}_{self.timestamp}"
        self.metrics = {
            "files_processed": 0,
            "directories_created": 0,
            "visualizations_migrated": 0,
            "components_validated": 0,
            "bytes_transferred": 0,
            "errors_encountered": 0
        }

    def _setup_logger(self) -> logging.Logger:
        """Configure logging for the unification process."""
        logger = logging.getLogger("ATLAS_UNIFICATION")
        logger.setLevel(logging.INFO)
        
        # Console handler with UTF-8 encoding
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # File handler with UTF-8 encoding
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler(
            f"logs/atlas_unification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(funcName)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        return logger

    def check_environment(self) -> bool:
        """Verify that all required tools are available."""
        self.logger.info("Checking environment requirements...")
        
        for tool in CONFIG["required_tools"]:
            try:
                # Use 'where' command on Windows to find executables
                if sys.platform == "win32":
                    result = subprocess.run(
                        ["where", tool],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    if result.returncode == 0:
                        self.logger.info(f"[OK] {tool} is available")
                    else:
                        self.logger.error(f"[ERROR] {tool} is not available")
                        return False
                else:
                    # For non-Windows systems, use 'which'
                    result = subprocess.run(
                        ["which", tool],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    if result.returncode == 0:
                        self.logger.info(f"[OK] {tool} is available")
                    else:
                        self.logger.error(f"[ERROR] {tool} is not available")
                        return False
                        
            except subprocess.CalledProcessError:
                self.logger.error(f"[ERROR] {tool} is not available")
                return False
            except Exception as e:
                self.logger.error(f"[ERROR] Failed to check {tool}: {str(e)}")
                return False
        
        return True

    def create_visualization_backup(self) -> bool:
        """Create a backup of visualization components and configurations."""
        try:
            self.logger.info("Creating visualization snapshot...")
            
            # Create backup directories if they don't exist
            os.makedirs(self.visualization_backup, exist_ok=True)
            
            # List of potential visualization directories to backup
            viz_dirs = [
                "core/atlas/visualization",
                "web/atendimento/frontend_streamlit/pages",
                "tools/integration/visualizations"
            ]
            
            files_backed_up = 0
            for dir_path in viz_dirs:
                if os.path.exists(dir_path):
                    target_dir = os.path.join(self.visualization_backup, os.path.basename(dir_path))
                    shutil.copytree(dir_path, target_dir, dirs_exist_ok=True)
                    files_backed_up += sum(len(files) for _, _, files in os.walk(dir_path))
            
            if files_backed_up == 0:
                self.logger.warning("No visualization files found to backup")
                return True
            
            self.logger.info(f"Backed up {files_backed_up} visualization files")
            return True
            
        except Exception as e:
            self.logger.error(f"Visualization backup failed: {str(e)}")
            return False

    def create_backup(self) -> bool:
        """Create a backup of all ATLAS related files."""
        try:
            self.logger.info("Creating backup...")
            
            # Create backup directory
            os.makedirs(self.backup_path, exist_ok=True)
            
            files_backed_up = 0
            for source_dir in CONFIG["source_dirs"]:
                if os.path.exists(source_dir):
                    target_dir = os.path.join(self.backup_path, os.path.basename(source_dir))
                    shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
                    files_backed_up += sum(len(files) for _, _, files in os.walk(source_dir))
            
            if files_backed_up == 0:
                self.logger.warning("No files found to backup")
                return True
                
            self.logger.info(f"Backed up {files_backed_up} files")
            return True
            
        except Exception as e:
            self.logger.error(f"Backup failed: {str(e)}")
            return False

    def _verify_backup_integrity(self) -> bool:
        """Verify the integrity of created backups."""
        try:
            self.logger.info("Verifying backup integrity...")
            
            # Check source directories backup
            for source_dir in CONFIG["source_dirs"]:
                source_path = Path(source_dir)
                backup_path = Path(self.backup_path) / source_dir
                
                if source_path.exists() and backup_path.exists():
                    source_files = set(f.relative_to(source_path) for f in source_path.rglob("*") if f.is_file())
                    backup_files = set(f.relative_to(backup_path) for f in backup_path.rglob("*") if f.is_file())
                    
                    if source_files != backup_files:
                        self.logger.error(f"Backup mismatch in {source_dir}")
                        return False
                        
                    for file in source_files:
                        source_hash = self._calculate_file_hash(source_path / file)
                        backup_hash = self._calculate_file_hash(backup_path / file)
                        
                        if source_hash != backup_hash:
                            self.logger.error(f"Hash mismatch for {file}")
                            return False
            
            # Verify visualization backup
            if not self._verify_visualization_backup():
                return False
            
            self.logger.info("Backup integrity verified successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Backup verification failed: {str(e)}")
            return False

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _verify_visualization_backup(self) -> bool:
        """Verify the integrity of visualization backup."""
        try:
            # Check visualization components
            viz_dirs = [
                "visualization",
                "pages",
                "visualizations"
            ]
            
            for dir_name in viz_dirs:
                backup_dir = Path(self.visualization_backup) / dir_name
                if backup_dir.exists():
                    # Verify key files
                    key_files = [
                        "package.json",
                        "webpack.config.js",
                        "tsconfig.json"
                    ]
                    for file in key_files:
                        if (backup_dir / file).exists():
                            self.logger.info(f"Found {file} in {dir_name}")
                        else:
                            self.logger.warning(f"Missing {file} in {dir_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Visualization backup verification failed: {str(e)}")
            return False

    def create_target_structure(self) -> bool:
        """Create the target directory structure."""
        try:
            self.logger.info("Creating target directory structure...")
            
            # Define directory structure
            directories = [
                'core/python',
                'core/visualization',
                'core/visualization/src',
                'core/visualization/dist',
                'web/frontend',
                'web/backend',
                'web/backend/personas',
                'integrations/cursor_bridge',
                'config',
                'docs',
                'tests/visualization',
                'tests/integration',
                'tests/unit',
                'scripts',
                'backups'
            ]
            
            # Create directories
            for dir_path in directories:
                full_path = os.path.join(CONFIG['target_dir'], dir_path)
                os.makedirs(full_path, exist_ok=True)
                self.logger.info(f"Created directory: {full_path}")
                self.metrics['directories_created'] += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create directory structure: {str(e)}")
            return False

    def move_files(self) -> bool:
        """Move files to their new locations."""
        try:
            self.logger.info("Starting file migration...")
            
            # Define file mappings
            file_mappings = {
                'core/atlas/atlas_core.py': 'core/python/atlas_core.py',
                'core/atlas/atlas_demo.py': 'core/python/atlas_demo.py',
                'core/atlas/src/atlas_core.py': 'core/python/atlas_core_src.py',
                'web/atendimento/frontend_streamlit/pages/atlas.py': 'web/frontend/atlas.py',
                'web/atendimento/backend/data/telegram_bot/personas/atlas.json': 'web/backend/personas/atlas.json',
                'tools/integration/cursor_atlas_bridge.py': 'integrations/cursor_bridge/cursor_atlas_bridge.py',
                'core/config/modules/atlas_config.json': 'config/atlas_config.json'
            }
            
            # Move files
            for source, target in file_mappings.items():
                if os.path.exists(source):
                    target_path = os.path.join(CONFIG['target_dir'], target)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(source, target_path)
                    self.logger.info(f"Migrated: {source} -> {target_path}")
                    self.metrics['files_processed'] += 1
                    self.metrics['bytes_transferred'] += os.path.getsize(source)
            
            # Move visualization files
            viz_source = 'core/atlas/visualization'
            if os.path.exists(viz_source):
                viz_target = os.path.join(CONFIG['target_dir'], 'core/visualization')
                for root, _, files in os.walk(viz_source):
                    for file in files:
                        source_file = os.path.join(root, file)
                        relative_path = os.path.relpath(source_file, viz_source)
                        target_file = os.path.join(viz_target, relative_path)
                        os.makedirs(os.path.dirname(target_file), exist_ok=True)
                        shutil.copy2(source_file, target_file)
                        self.logger.info(f"Migrated visualization: {relative_path}")
                        self.metrics['files_processed'] += 1
                        self.metrics['visualizations_migrated'] += 1
                        self.metrics['bytes_transferred'] += os.path.getsize(source_file)
            
            # Move tests
            test_patterns = {
                'test_visualization': 'tests/visualization',
                'test_integration': 'tests/integration',
                'test_unit': 'tests/unit'
            }
            
            for root, _, files in os.walk('tests'):
                for file in files:
                    if file.startswith('test_') and file.endswith(('.py', '.js')):
                        source_file = os.path.join(root, file)
                        target_dir = None
                        
                        # Determine target directory based on test type
                        for pattern, dir_path in test_patterns.items():
                            if pattern in file.lower():
                                target_dir = dir_path
                                break
                        
                        if target_dir:
                            target_file = os.path.join(CONFIG['target_dir'], target_dir, file)
                            os.makedirs(os.path.dirname(target_file), exist_ok=True)
                            shutil.copy2(source_file, target_file)
                            self.logger.info(f"Migrated test: {file}")
                            self.metrics['files_processed'] += 1
                            self.metrics['bytes_transferred'] += os.path.getsize(source_file)
            
            self.logger.info("File migration completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"File migration failed: {str(e)}")
            return False

    def update_references(self) -> bool:
        """Update file references to match new structure."""
        try:
            self.logger.info("Updating file references...")
            
            # Directories to ignore during reference updates
            ignore_dirs = {
                'node_modules',
                '__pycache__',
                '.git',
                'venv',
                'env',
                'dist'
            }
            
            files_updated = 0
            for root, dirs, files in os.walk(CONFIG['target_dir']):
                # Remove ignored directories
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                
                for file in files:
                    if file.endswith(('.py', '.js', '.json', '.md', '.yml', '.yaml', '.tsx', '.ts')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Update imports and references
                            updated_content = self._update_file_content(content)
                            
                            if updated_content != content:
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(updated_content)
                                files_updated += 1
                                self.logger.info(f"Updated references in {file_path}")
                                
                        except Exception as e:
                            self.logger.error(f"Failed to update references in {file_path}: {str(e)}")
            
            self.logger.info(f"Updated references in {files_updated} files")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update references: {str(e)}")
            return False

    def _update_file_content(self, content: str) -> str:
        """Update imports and references in file content."""
        # Update Python imports
        content = re.sub(
            r'from (core\.)?atlas\.',
            'from QUANTUM_PROMPTS.ATLAS.',
            content
        )
        content = re.sub(
            r'import (core\.)?atlas\.',
            'import QUANTUM_PROMPTS.ATLAS.',
            content
        )
        
        # Update JavaScript/TypeScript imports
        content = re.sub(
            r'from [\'"].*?/atlas/',
            'from \'QUANTUM_PROMPTS/ATLAS/',
            content
        )
        content = re.sub(
            r'require\([\'"].*?/atlas/',
            'require(\'QUANTUM_PROMPTS/ATLAS/',
            content
        )
        
        # Update relative paths in JSON
        content = re.sub(
            r'"path":\s*".*?/atlas/',
            '"path": "QUANTUM_PROMPTS/ATLAS/',
            content
        )
        
        # Update visualization imports
        content = re.sub(
            r'from [\'"].*?/visualization/',
            'from \'QUANTUM_PROMPTS/ATLAS/core/visualization/',
            content
        )
        
        return content

    def validate_migration(self) -> bool:
        """Validate the migration process."""
        try:
            self.logger.info("Validating migration...")
            
            # Validate directory structure
            required_dirs = [
                'core/python',
                'core/visualization',
                'web/frontend',
                'web/backend',
                'integrations/cursor_bridge',
                'config',
                'tests'
            ]
            
            for dir_path in required_dirs:
                full_path = os.path.join(CONFIG['target_dir'], dir_path)
                if not os.path.exists(full_path):
                    self.logger.error(f"Required directory missing: {full_path}")
                    return False
            
            # Validate core files
            required_files = [
                'core/python/atlas_core.py',
                'core/python/atlas_demo.py',
                'config/atlas_config.json',
                'integrations/cursor_bridge/cursor_atlas_bridge.py'
            ]
            
            for file_path in required_files:
                full_path = os.path.join(CONFIG['target_dir'], file_path)
                if not os.path.exists(full_path):
                    self.logger.error(f"Required file missing: {full_path}")
                    return False
            
            # Validate visualization setup
            viz_files = [
                'core/visualization/package.json',
                'core/visualization/webpack.config.js',
                'core/visualization/tsconfig.json'
            ]
            
            viz_files_found = False
            for file_path in viz_files:
                full_path = os.path.join(CONFIG['target_dir'], file_path)
                if os.path.exists(full_path):
                    viz_files_found = True
                    break
            
            if not viz_files_found:
                self.logger.warning("No visualization configuration files found")
            
            # Generate validation report
            report = {
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'metrics': self.metrics,
                'validation': {
                    'directory_structure': True,
                    'core_files': True,
                    'visualization_files': viz_files_found,
                    'web_components': os.path.exists(os.path.join(CONFIG['target_dir'], 'web')),
                    'integration_components': os.path.exists(os.path.join(CONFIG['target_dir'], 'integrations'))
                }
            }
            
            # Save validation report
            report_dir = os.path.join(CONFIG['target_dir'], 'docs')
            os.makedirs(report_dir, exist_ok=True)
            report_path = os.path.join(report_dir, 'validation_report.json')
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            
            self.logger.info("Migration validation completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Validation failed: {str(e)}")
            return False

    def generate_report(self) -> bool:
        """Generate a detailed report of the unification process."""
        try:
            self.logger.info("Generating unification report...")
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'metrics': self.metrics,
                'backup_location': self.backup_path,
                'visualization_backup': self.visualization_backup,
                'source_directories': CONFIG['source_dirs'],
                'target_directory': CONFIG['target_dir'],
                'files_processed': [],
                'directories_created': [],
                'warnings': [],
                'errors': []
            }
            
            # Add processed files
            for root, _, files in os.walk(CONFIG['target_dir']):
                for file in files:
                    file_path = os.path.join(root, file)
                    report['files_processed'].append({
                        'path': file_path,
                        'size': os.path.getsize(file_path),
                        'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                    })
            
            # Save report
            report_dir = os.path.join(CONFIG['target_dir'], 'docs')
            os.makedirs(report_dir, exist_ok=True)
            report_path = os.path.join(report_dir, 'unification_report.json')
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            
            self.logger.info("Unification report generated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate report: {str(e)}")
            return False

    def execute(self) -> bool:
        """Execute the complete unification process."""
        try:
            self.logger.info("Starting ATLAS unification process...")
            
            # Check environment
            if not self.check_environment():
                return False
            
            # Create backups
            if not self.create_backup():
                return False
                
            if not self.create_visualization_backup():
                return False
            
            # Create target structure
            if not self.create_target_structure():
                return False
            
            # Migrate files
            if not self.move_files():
                return False
            
            # Update references
            if not self.update_references():
                return False
            
            # Validate migration
            if not self.validate_migration():
                return False
            
            # Generate report
            if not self.generate_report():
                return False
            
            self.logger.info("ATLAS unification completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Unification failed: {str(e)}")
            return False

def main():
    """Main execution function."""
    unification = AtlasUnification()
    success = unification.execute()
    
    if success:
        print("\n✅ ATLAS unification completed successfully")
        sys.exit(0)
    else:
        print("\n❌ ATLAS unification failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 