"""
EVA & GUARANI - NEXUS Unification Script
Version: 1.0
Date: 2025-03-30
Description: Automated unification script for NEXUS subsystem with ML model preservation
"""

import json
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
import subprocess
import hashlib
import re

# Configuration
config = {
    "version": "1.0.0",
    "source_dirs": [
        "core/nexus",
        "web/atendimento/frontend_streamlit/pages",
        "web/atendimento/backend/app/integrations",
        "tools/integration",
        "core/config/modules"
    ],
    "target_dir": "QUANTUM_PROMPTS/NEXUS",
    "backup_dir": "quarantine/NEXUS_backup",
    "models_dir": "models_backup",
    "required_tools": [
        "python"
    ]
}

class NexusUnification:
    """Handles the unification process for the NEXUS subsystem."""

    def __init__(self):
        """Initialize the unification process."""
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = Path(f"{config['backup_dir']}_{self.timestamp}")
        self.models_backup_path = Path(f"{config['models_dir']}_{self.timestamp}")
        self.target_path = Path(config["target_dir"])
        
        # Metrics
        self.metrics = {
            "files_processed": 0,
            "directories_created": 0,
            "bytes_transferred": 0,
            "models_preserved": 0,
            "references_updated": 0
        }
        
        # Setup logging
        self.setup_logger()

    def setup_logger(self):
        """Configure logging for the unification process."""
        self.logger = logging.getLogger("NEXUS_UNIFICATION")
        self.logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # File handler
        log_file = log_dir / f"nexus_unification_{self.timestamp}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def check_environment(self):
        """Verify required tools are available."""
        self.logger.info("Checking environment requirements...")
        for tool in config["required_tools"]:
            try:
                subprocess.run([tool, "--version"], capture_output=True)
                self.logger.info(f"[OK] {tool} is available")
            except FileNotFoundError:
                self.logger.error(f"[✗] {tool} is not available")
                return False
        return True

    def backup_models(self):
        """Create a backup of ML models."""
        self.logger.info("Creating ML models backup...")
        models_source = Path("core/nexus/models")
        if models_source.exists():
            self.models_backup_path.mkdir(parents=True, exist_ok=True)
            for model_file in models_source.glob("**/*"):
                if model_file.is_file():
                    relative_path = model_file.relative_to(models_source)
                    target_path = self.models_backup_path / relative_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(model_file, target_path)
                    self.metrics["models_preserved"] += 1
            self.logger.info(f"Backed up {self.metrics['models_preserved']} models")

    def create_backup(self):
        """Create a backup of all NEXUS related files."""
        self.logger.info("Creating backup...")
        self.backup_path.mkdir(parents=True, exist_ok=True)
        
        files_backed_up = 0
        for source_dir in config["source_dirs"]:
            source_path = Path(source_dir)
            if source_path.exists():
                for file_path in source_path.glob("**/*"):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(source_path)
                        backup_file_path = self.backup_path / source_dir / relative_path
                        backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, backup_file_path)
                        files_backed_up += 1
        
        self.logger.info(f"Backed up {files_backed_up} files")
        return self.verify_backup_integrity()

    def verify_backup_integrity(self):
        """Verify the integrity of backed up files."""
        self.logger.info("Verifying backup integrity...")
        
        def calculate_hash(file_path):
            """Calculate SHA-256 hash of a file."""
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()

        for source_dir in config["source_dirs"]:
            source_path = Path(source_dir)
            if source_path.exists():
                for file_path in source_path.glob("**/*"):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(source_path)
                        backup_file_path = self.backup_path / source_dir / relative_path
                        
                        if not backup_file_path.exists():
                            self.logger.error(f"Backup file missing: {backup_file_path}")
                            return False
                        
                        source_hash = calculate_hash(file_path)
                        backup_hash = calculate_hash(backup_file_path)
                        
                        if source_hash != backup_hash:
                            self.logger.error(f"Hash mismatch for {file_path}")
                            return False

        self.logger.info("Backup integrity verified successfully")
        return True

    def create_directory_structure(self):
        """Create the target directory structure."""
        self.logger.info("Creating target directory structure...")
        directories = [
            "core/python",
            "core/analyzers",
            "core/optimizers",
            "web/frontend/components",
            "web/frontend/styles",
            "web/backend/api",
            "web/backend/services",
            "integrations",
            "config",
            "docs",
            "tests/unit",
            "tests/integration",
            "scripts"
        ]

        for dir_path in directories:
            full_path = self.target_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {full_path}")
            self.metrics["directories_created"] += 1

    def migrate_files(self):
        """Move files to their new locations."""
        self.logger.info("Starting file migration...")
        
        # File mapping
        file_mapping = {
            'core/nexus/__init__.py': 'core/python/__init__.py',
            'core/nexus/src/nexus_core.py': 'core/python/nexus_core.py',
            'web/atendimento/frontend_streamlit/pages/nexus.py': 'web/frontend/nexus.py',
            'web/atendimento/backend/app/integrations/egos_connector.py': 'web/backend/api/egos_connector.py',
            'tools/integration/nexus_bridge.py': 'integrations/nexus_bridge.py',
            'core/config/modules/nexus_config.json': 'config/nexus_config.json',
            'core/nexus/README.md': 'docs/README.md'
        }

        for source, target in file_mapping.items():
            source_path = Path(source)
            target_path = self.target_path / target
            
            if source_path.exists():
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, target_path)
                self.metrics["files_processed"] += 1
                self.metrics["bytes_transferred"] += source_path.stat().st_size
                self.logger.info(f"Migrated: {source} -> {target_path}")

        self.logger.info("File migration completed successfully")

    def update_references(self):
        """Update file references to match new structure."""
        self.logger.info("Updating file references...")
        
        patterns = [
            (r'from (core\.)?nexus\.', 'from QUANTUM_PROMPTS.NEXUS.'),
            (r'import (core\.)?nexus\.', 'import QUANTUM_PROMPTS.NEXUS.'),
            (r'from [\'"].*?/nexus/', 'from \'QUANTUM_PROMPTS/NEXUS/'),
            (r'require\([\'"].*?/nexus/', 'require(\'QUANTUM_PROMPTS/NEXUS/'),
            (r'"path":\s*".*?/nexus/', '"path": "QUANTUM_PROMPTS/NEXUS/')
        ]

        python_files = [
            'core/python/nexus_core.py',
            'web/frontend/nexus.py',
            'web/backend/api/egos_connector.py'
        ]

        for file_path in python_files:
            full_path = self.target_path / file_path
            if full_path.exists():
                content = full_path.read_text()
                original_content = content
                
                for pattern, replacement in patterns:
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    full_path.write_text(content)
                    self.metrics["references_updated"] += 1
                    self.logger.info(f"Updated references in {file_path}")

    def validate_migration(self):
        """Validate the migration process."""
        self.logger.info("Validating migration...")
        
        # Required files
        required_files = [
            'core/python/__init__.py',
            'core/python/nexus_core.py',
            'config/nexus_config.json',
            'docs/README.md'
        ]

        for file_path in required_files:
            full_path = self.target_path / file_path
            if not full_path.exists():
                self.logger.error(f"Required file missing: {file_path}")
                return False

        # Check ML models
        if self.metrics["models_preserved"] == 0:
            self.logger.warning("No ML models found")

        self.logger.info("Migration validation completed successfully")
        return True

    def generate_report(self):
        """Generate a detailed report of the unification process."""
        report = {
            "timestamp": self.timestamp,
            "version": config["version"],
            "metrics": self.metrics,
            "status": "success",
            "backup_location": str(self.backup_path),
            "models_backup": str(self.models_backup_path)
        }

        report_path = Path("logs") / f"nexus_unification_report_{self.timestamp}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        self.logger.info("Unification report generated successfully")

    def execute(self):
        """Execute the unification process."""
        try:
            self.logger.info("Starting NEXUS unification process...")
            
            if not self.check_environment():
                raise Exception("Environment check failed")

            if not self.create_backup():
                raise Exception("Backup creation failed")

            self.backup_models()
            self.create_directory_structure()
            self.migrate_files()
            self.update_references()

            if not self.validate_migration():
                raise Exception("Migration validation failed")

            self.generate_report()
            self.logger.info("NEXUS unification completed successfully")
            return True

        except Exception as e:
            self.logger.error(f"Unification failed: {str(e)}")
            return False

if __name__ == "__main__":
    unification = NexusUnification()
    success = unification.execute()
    sys.exit(0 if success else 1) 