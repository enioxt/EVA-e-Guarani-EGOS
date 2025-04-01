"""
EVA & GUARANI - ETHIK Unification Script
Version: 1.0
Date: 2025-03-29
Description: Automated unification script for ETHIK subsystem with blockchain support
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
        "ETHIK",
        "core/ethik"
    ],
    "target_dir": "QUANTUM_PROMPTS/ETHIK",
    "backup_dir": "quarantine/ETHIK_backup",
    "blockchain_dir": "blockchain_backup",
    "required_tools": [
        "node",
        "npm",
        "truffle",
        "hardhat"
    ]
}

class EthikUnification:
    def __init__(self):
        self.logger = self._setup_logger()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = f"{CONFIG['backup_dir']}_{self.timestamp}"
        self.blockchain_backup = f"{CONFIG['blockchain_dir']}_{self.timestamp}"
        self.metrics = {
            "files_processed": 0,
            "directories_created": 0,
            "contracts_migrated": 0,
            "rules_validated": 0,
            "bytes_transferred": 0,
            "errors_encountered": 0
        }

    def _setup_logger(self) -> logging.Logger:
        """Configure logging for the unification process."""
        logger = logging.getLogger("ETHIK_UNIFICATION")
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
            f"logs/ethik_unification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
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

    def create_blockchain_backup(self) -> bool:
        """Create a backup of blockchain contracts and configurations."""
        try:
            self.logger.info("Creating blockchain snapshot...")
            
            # Create backup directories if they don't exist
            os.makedirs(self.blockchain_backup, exist_ok=True)
            
            # List of potential blockchain directories to backup
            blockchain_dirs = [
                "ETHIK/contracts",
                "core/ethik/contracts",
                "QUANTUM_PROMPTS/ETHIK/core/contracts"
            ]
            
            files_backed_up = 0
            for dir_path in blockchain_dirs:
                if os.path.exists(dir_path):
                    target_dir = os.path.join(self.blockchain_backup, os.path.basename(dir_path))
                    shutil.copytree(dir_path, target_dir, dirs_exist_ok=True)
                    files_backed_up += sum(len(files) for _, _, files in os.walk(dir_path))
            
            if files_backed_up == 0:
                self.logger.warning("No blockchain files found to backup")
                return True
            
            self.logger.info(f"Backed up {files_backed_up} blockchain files")
            return True
            
        except Exception as e:
            self.logger.error(f"Blockchain backup failed: {str(e)}")
            return False

    def create_backup(self) -> bool:
        """Create a backup of all ETHIK related files."""
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
            
            # Verify blockchain backup
            if not self._verify_blockchain_backup():
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

    def _verify_blockchain_backup(self) -> bool:
        """Verify the integrity of blockchain backup."""
        try:
            # Check contract state export
            state_file = Path(self.blockchain_backup) / "contracts_state.json"
            if not state_file.exists():
                self.logger.error("Contract state export not found")
                return False
            
            # Validate JSON format
            with open(state_file) as f:
                try:
                    json.load(f)
                except json.JSONDecodeError:
                    self.logger.error("Contract state file is not valid JSON")
                    return False
            
            # Check contract builds
            builds_dir = Path(self.blockchain_backup) / "contract_builds"
            if not builds_dir.exists():
                self.logger.error("Contract builds backup not found")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Blockchain backup verification failed: {str(e)}")
            return False

    def create_target_structure(self) -> bool:
        """Create the target directory structure."""
        try:
            self.logger.info("Creating target directory structure...")
            
            # Define directory structure
            directories = [
                'core',
                'core/contracts',
                'core/web3',
                'core/js',
                'core/python',
                'tests/contracts',
                'tests/web3',
                'tests/unit',
                'config',
                'docs',
                'scripts',
                'backups',
                'sanitizers',
                'validators'
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
                'core/ethik/ethik_core.py': 'core/python/ethik_core.py',
                'core/ethik/ethik_core.js': 'core/js/ethik_core.js',
                'core/ethik/ethics.py': 'core/python/ethics.py',
                'core/ethik/ethik_config.json': 'config/ethik_config.json',
                'core/ethik/ETHIK_CHAIN_TECHNOLOGY.md': 'docs/ETHIK_CHAIN_TECHNOLOGY.md',
                'core/ethik/README.md': 'docs/README.md',
                'core/ethik/requirements.txt': 'config/requirements.txt'
            }
            
            # Move files from core/ethik directory
            for source, target in file_mappings.items():
                if os.path.exists(source):
                    target_path = os.path.join(CONFIG['target_dir'], target)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(source, target_path)
                    self.logger.info(f"Migrated: {source} -> {target_path}")
                    self.metrics['files_processed'] += 1
                    self.metrics['bytes_transferred'] += os.path.getsize(source)
            
            # Move sanitizers
            sanitizers_dir = 'core/ethik/sanitizers'
            if os.path.exists(sanitizers_dir):
                target_dir = os.path.join(CONFIG['target_dir'], 'sanitizers')
                for file in os.listdir(sanitizers_dir):
                    if file.endswith('.py'):
                        source = os.path.join(sanitizers_dir, file)
                        target = os.path.join(target_dir, file)
                        shutil.copy2(source, target)
                        self.logger.info(f"Migrated sanitizer: {file}")
                        self.metrics['files_processed'] += 1
                        self.metrics['bytes_transferred'] += os.path.getsize(source)
            
            # Move validators
            validators_dir = 'core/ethik/validators'
            if os.path.exists(validators_dir):
                target_dir = os.path.join(CONFIG['target_dir'], 'validators')
                for file in os.listdir(validators_dir):
                    if file.endswith('.py'):
                        source = os.path.join(validators_dir, file)
                        target = os.path.join(target_dir, file)
                        shutil.copy2(source, target)
                        self.logger.info(f"Migrated validator: {file}")
                        self.metrics['files_processed'] += 1
                        self.metrics['bytes_transferred'] += os.path.getsize(source)
            
            # Move tests
            tests_dir = 'core/ethik/tests'
            if os.path.exists(tests_dir):
                for file in os.listdir(tests_dir):
                    if file.startswith('test_') and file.endswith('.py'):
                        source = os.path.join(tests_dir, file)
                        if 'contract' in file.lower():
                            target = os.path.join(CONFIG['target_dir'], 'tests/contracts', file)
                        elif 'web3' in file.lower():
                            target = os.path.join(CONFIG['target_dir'], 'tests/web3', file)
                        else:
                            target = os.path.join(CONFIG['target_dir'], 'tests/unit', file)
                        os.makedirs(os.path.dirname(target), exist_ok=True)
                        shutil.copy2(source, target)
                        self.logger.info(f"Migrated test: {file}")
                        self.metrics['files_processed'] += 1
                        self.metrics['bytes_transferred'] += os.path.getsize(source)
            
            # Move documentation
            docs_dir = 'core/ethik/docs'
            if os.path.exists(docs_dir):
                target_dir = os.path.join(CONFIG['target_dir'], 'docs')
                for file in os.listdir(docs_dir):
                    if file.endswith(('.md', '.rst', '.txt')):
                        source = os.path.join(docs_dir, file)
                        target = os.path.join(target_dir, file)
                        shutil.copy2(source, target)
                        self.logger.info(f"Migrated documentation: {file}")
                        self.metrics['files_processed'] += 1
                        self.metrics['bytes_transferred'] += os.path.getsize(source)
            
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
                'env'
            }
            
            files_updated = 0
            for root, dirs, files in os.walk(CONFIG['target_dir']):
                # Remove ignored directories
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                
                for file in files:
                    if file.endswith(('.py', '.js', '.json', '.md', '.yml', '.yaml')):
                        file_path = os.path.join(root, file)
                        try:
                            # Try UTF-8 first
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Update imports and references
                            updated_content = self._update_file_content(content)
                            
                            if updated_content != content:
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(updated_content)
                                files_updated += 1
                                self.logger.info(f"Updated references in {file_path}")
                                
                        except UnicodeDecodeError:
                            # Try with a different encoding if UTF-8 fails
                            try:
                                with open(file_path, 'r', encoding='latin-1') as f:
                                    content = f.read()
                                
                                updated_content = self._update_file_content(content)
                                
                                if updated_content != content:
                                    with open(file_path, 'w', encoding='latin-1') as f:
                                        f.write(updated_content)
                                    files_updated += 1
                                    self.logger.info(f"Updated references in {file_path} (latin-1 encoding)")
                            except Exception as e:
                                self.logger.warning(f"Skipping {file_path} due to encoding issues: {str(e)}")
                        except PermissionError:
                            self.logger.warning(f"Skipping {file_path} due to permission denied")
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
        content = self._update_python_imports(content)
        
        # Update JavaScript imports
        content = self._update_javascript_imports(content)
        
        # Update JSON references
        content = self._update_json_references(content)
        
        # Update Markdown links
        content = self._update_markdown_links(content)
        
        return content

    def _update_python_imports(self, content: str) -> str:
        """Update Python import statements."""
        import_patterns = [
            (r'from ETHIK\.', r'from QUANTUM_PROMPTS.ETHIK.'),
            (r'from core\.ethik\.', r'from QUANTUM_PROMPTS.ETHIK.'),
            (r'import ETHIK\.', r'import QUANTUM_PROMPTS.ETHIK.'),
            (r'import core\.ethik\.', r'import QUANTUM_PROMPTS.ETHIK.')
        ]
        
        for old_pattern, new_pattern in import_patterns:
            content = re.sub(old_pattern, new_pattern, content)
        
        return content

    def _update_javascript_imports(self, content: str) -> str:
        """Update JavaScript import/require statements."""
        import_patterns = [
            (r'require\([\'"]ETHIK/', r'require(\'QUANTUM_PROMPTS/ETHIK/'),
            (r'require\([\'"]\.\.?/ETHIK/', r'require(\'QUANTUM_PROMPTS/ETHIK/'),
            (r'from [\'"]ETHIK/', r'from \'QUANTUM_PROMPTS/ETHIK/'),
            (r'from [\'"]\.\.?/ETHIK/', r'from \'QUANTUM_PROMPTS/ETHIK/')
        ]
        
        for old_pattern, new_pattern in import_patterns:
            content = re.sub(old_pattern, new_pattern, content)
        
        return content

    def _update_json_references(self, content: str) -> str:
        """Update paths in JSON files."""
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                data = self._update_json_dict(data)
                return json.dumps(data, indent=2)
        except json.JSONDecodeError:
            pass
        return content

    def _update_json_dict(self, data: Dict) -> Dict:
        """Recursively update paths in JSON dictionary."""
        updated = {}
        for key, value in data.items():
            if isinstance(value, str):
                if 'ETHIK/' in value or 'core/ethik/' in value:
                    value = value.replace('ETHIK/', 'QUANTUM_PROMPTS/ETHIK/')
                    value = value.replace('core/ethik/', 'QUANTUM_PROMPTS/ETHIK/')
            elif isinstance(value, dict):
                value = self._update_json_dict(value)
            elif isinstance(value, list):
                value = [
                    self._update_json_dict(item) if isinstance(item, dict)
                    else item
                    for item in value
                ]
            updated[key] = value
        return updated

    def _update_markdown_links(self, content: str) -> str:
        """Update links in Markdown files."""
        link_patterns = [
            (r'\[([^\]]+)\]\(ETHIK/', r'[\1](QUANTUM_PROMPTS/ETHIK/'),
            (r'\[([^\]]+)\]\(\.\.?/ETHIK/', r'[\1](QUANTUM_PROMPTS/ETHIK/'),
            (r'\[([^\]]+)\]\(core/ethik/', r'[\1](QUANTUM_PROMPTS/ETHIK/')
        ]
        
        for old_pattern, new_pattern in link_patterns:
            content = re.sub(old_pattern, new_pattern, content)
        
        return content

    def validate_migration(self) -> bool:
        """Validate the migration process."""
        try:
            self.logger.info("Validating migration...")
            
            # Validate directory structure
            required_dirs = [
                'core/python',
                'core/js',
                'core/contracts',
                'tests',
                'config',
                'scripts',
                'backups',
                'sanitizers',
                'validators'
            ]
            
            for dir_path in required_dirs:
                full_path = os.path.join(CONFIG['target_dir'], dir_path)
                if not os.path.exists(full_path):
                    self.logger.error(f"Required directory missing: {full_path}")
                    return False
            
            # Validate core files
            required_files = [
                'core/python/ethik_core.py',
                'core/python/ethics.py',
                'core/js/ethik_core.js',
                'config/ethik_config.json'
            ]
            
            for file_path in required_files:
                full_path = os.path.join(CONFIG['target_dir'], file_path)
                if not os.path.exists(full_path):
                    self.logger.error(f"Required file missing: {full_path}")
                    return False
            
            # Validate blockchain files if they exist
            blockchain_files = [
                'core/contracts/package.json',
                'core/contracts/truffle-config.js',
                'core/contracts/hardhat.config.js'
            ]
            
            blockchain_files_found = False
            for file_path in blockchain_files:
                full_path = os.path.join(CONFIG['target_dir'], file_path)
                if os.path.exists(full_path):
                    blockchain_files_found = True
                    break
            
            if not blockchain_files_found:
                self.logger.warning("No blockchain configuration files found")
            
            # Validate smart contracts if they exist
            contracts_dir = os.path.join(CONFIG['target_dir'], 'core/contracts/contracts')
            if os.path.exists(contracts_dir):
                contract_files = [f for f in os.listdir(contracts_dir) if f.endswith('.sol')]
                if not contract_files:
                    self.logger.warning("No smart contracts found in contracts directory")
                else:
                    self.logger.info(f"Found {len(contract_files)} smart contracts")
            else:
                self.logger.warning("Contracts directory not found")
            
            # Validate test files
            test_dirs = [
                'tests/contracts',
                'tests/web3',
                'tests/unit'
            ]
            
            tests_found = False
            for dir_path in test_dirs:
                full_path = os.path.join(CONFIG['target_dir'], dir_path)
                if os.path.exists(full_path):
                    test_files = [
                        f for f in os.listdir(full_path)
                        if f.startswith('test_') and f.endswith(('.py', '.js'))
                    ]
                    if test_files:
                        tests_found = True
                        self.logger.info(f"Found {len(test_files)} test files in {dir_path}")
            
            if not tests_found:
                self.logger.warning("No test files found")
            
            # Validate sanitizers and validators
            sanitizers_dir = os.path.join(CONFIG['target_dir'], 'sanitizers')
            validators_dir = os.path.join(CONFIG['target_dir'], 'validators')
            
            sanitizers = [f for f in os.listdir(sanitizers_dir) if f.endswith('.py')] if os.path.exists(sanitizers_dir) else []
            validators = [f for f in os.listdir(validators_dir) if f.endswith('.py')] if os.path.exists(validators_dir) else []
            
            if not sanitizers:
                self.logger.warning("No sanitizer modules found")
            else:
                self.logger.info(f"Found {len(sanitizers)} sanitizer modules")
                
            if not validators:
                self.logger.warning("No validator modules found")
            else:
                self.logger.info(f"Found {len(validators)} validator modules")
            
            # Generate validation report
            report = {
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'metrics': self.metrics,
                'warnings': [],
                'validation': {
                    'directory_structure': True,
                    'core_files': True,
                    'blockchain_files': blockchain_files_found,
                    'contracts_found': bool(contract_files) if 'contract_files' in locals() else False,
                    'tests_found': tests_found,
                    'sanitizers_found': bool(sanitizers),
                    'validators_found': bool(validators)
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
                'blockchain_backup': self.blockchain_backup,
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
            self.logger.info("Starting ETHIK unification process...")
            
            # Check environment
            if not self.check_environment():
                return False
            
            # Create backups
            if not self.create_backup():
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
            
            self.logger.info("ETHIK unification completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Unification failed: {str(e)}")
            return False

def main():
    """Main execution function."""
    unification = EthikUnification()
    success = unification.execute()
    
    if success:
        print("\n✅ ETHIK unification completed successfully")
        sys.exit(0)
    else:
        print("\n❌ ETHIK unification failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 