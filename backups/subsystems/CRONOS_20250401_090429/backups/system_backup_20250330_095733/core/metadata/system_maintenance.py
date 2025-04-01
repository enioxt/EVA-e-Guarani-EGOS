"""EVA & GUARANI - System Maintenance Module
Version: 8.0

This module handles system maintenance operations including backups, cleanup, and quarantine.

Roadmap:
- Q2 2025: ML-based anomaly detection for outdated files
- Q2 2025: Automated backup scheduling
- Q3 2025: Cloud backup integration
- Q3 2025: Quantum state preservation
- Q4 2025: Advanced file analysis with NEXUS integration
- Q4 2025: ETHIK validation for file operations
"""

import os
import shutil
import datetime
import hashlib
import json
import logging
import tarfile
import base64
import sys
import platform
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from threading import Lock
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import re

# === Currently Implemented Features ===

class SystemMaintenance:
    def __init__(self, root_dir: str, quarantine_dir: str = "quarantine", max_backups: int = 10):
        self.root_dir = Path(root_dir)
        self.quarantine_dir = self.root_dir / quarantine_dir
        self.backup_dir = self.root_dir / "backups"
        self.metadata_dir = self.root_dir / "METADATA"
        self.quantum_dir = self.root_dir / "QUANTUM_PROMPTS"
        self.temp_dir = self.root_dir / "temp"
        self.logs_dir = self.root_dir / "logs"
        self.max_backups = max_backups
        self._backup_lock = Lock()
        
        # Directories and patterns to exclude from backups
        self.exclude_patterns = {
            '.git',
            '__pycache__',
            'node_modules',
            'venv',
            '.pytest_cache',
            '.coverage',
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '.DS_Store',
            'Thumbs.db'
        }
        
        # Ensure directories exist
        self.quarantine_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        self.metadata_dir.mkdir(exist_ok=True)
        self.quantum_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger("system_maintenance")
        self.logger.setLevel(logging.INFO)
        log_dir = self.root_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        handler = logging.FileHandler(log_dir / "maintenance.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def _should_exclude(self, path: Path) -> bool:
        """Check if a path should be excluded from backup."""
        # Check if any part of the path matches exclude patterns
        path_str = str(path)
        return any(
            pattern in path_str or 
            (pattern.startswith('*') and path_str.endswith(pattern[1:])) 
            for pattern in self.exclude_patterns
        )

    def create_backup(self, password: Optional[str] = None, compress: bool = True) -> str:
        """Create a timestamped backup of the entire system."""
        with self._backup_lock:  # Ensure only one backup operation runs at a time
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"system_backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            
            try:
                # Create backup directory
                backup_path.mkdir(exist_ok=True)
                
                # Create temporary directory for files
                temp_dir = backup_path / "temp"
                temp_dir.mkdir()
                
                # Copy core directories
                dirs_to_backup = ['core', 'web', 'QUANTUM_PROMPTS', 'METADATA']
                total_size = 0
                file_count = 0
                
                for dir_name in dirs_to_backup:
                    src = self.root_dir / dir_name
                    if src.exists():
                        dst = temp_dir / dir_name
                        # Copy directory excluding patterns
                        self._copy_directory(src, dst)
                        
                        # Calculate directory statistics
                        for file_path in dst.rglob('*'):
                            if file_path.is_file():
                                total_size += file_path.stat().st_size
                                file_count += 1
                
                # Create backup archive
                archive_path = backup_path / f"{backup_name}.tar"
                if compress:
                    archive_path = archive_path.with_suffix('.tar.gz')
                
                # Create archive
                mode = 'w:gz' if compress else 'w'
                with tarfile.open(archive_path, mode) as tar:
                    tar.add(temp_dir, arcname=backup_name)
                
                # Encrypt if password provided
                if password:
                    archive_path = self._encrypt_file(archive_path, password)
                    encrypted = True
                else:
                    encrypted = False
                
                # Calculate archive hash AFTER encryption
                archive_hash = self._calculate_file_hash(archive_path)
                
                # Create backup manifest
                manifest = {
                    'timestamp': timestamp,
                    'name': backup_name,
                    'version': '8.0',
                    'directories': dirs_to_backup,
                    'files_count': file_count,
                    'total_size': total_size,
                    'compressed': compress,
                    'encrypted': encrypted,
                    'archive_hash': archive_hash,
                    'archive_path': str(archive_path.relative_to(backup_path)),
                    'system_info': {
                        'python_version': sys.version,
                        'platform': platform.platform(),
                        'created_by': os.getenv('USERNAME', 'unknown')
                    }
                }
                
                # Save manifest
                manifest_path = backup_path / 'manifest.json'
                with open(manifest_path, 'w') as f:
                    json.dump(manifest, f, indent=2)
                
                # Clean up temporary directory
                shutil.rmtree(temp_dir)
                
                # Verify backup
                if not self._verify_backup(backup_path, manifest):
                    raise ValueError("Backup verification failed")
                
                # Rotate old backups
                self._rotate_backups()
                
                self.logger.info(f"Created backup: {backup_name}")
                return str(backup_path)
                
            except Exception as e:
                self.logger.error(f"Backup failed: {str(e)}")
                if backup_path.exists():
                    shutil.rmtree(backup_path)
                raise

    def _copy_directory(self, src: Path, dst: Path) -> None:
        """Copy directory excluding specified patterns."""
        dst.mkdir(parents=True, exist_ok=True)
        
        for item in src.iterdir():
            if self._should_exclude(item):
                continue
                
            if item.is_dir():
                self._copy_directory(item, dst / item.name)
            else:
                try:
                    shutil.copy2(item, dst / item.name)
                except (PermissionError, OSError) as e:
                    self.logger.warning(f"Failed to copy {item}: {str(e)}")

    def restore_backup(self, backup_name: str, password: Optional[str] = None) -> bool:
        """Restore system from a backup."""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            self.logger.error(f"Backup not found: {backup_name}")
            return False
        
        try:
            # Read manifest
            manifest_path = backup_path / 'manifest.json'
            with open(manifest_path) as f:
                manifest = json.load(f)
            
            # Verify backup before restoring
            if not self._verify_backup(backup_path, manifest):
                raise ValueError("Backup verification failed")
            
            # Create temporary backup of current state
            temp_backup_name = f"temp_before_restore_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            temp_backup = self.create_backup(
                password="temp123",  # Use a temporary password
                compress=True
            )
            
            # Get archive path
            archive_path = backup_path / manifest['archive_path']
            
            # Decrypt if necessary
            if manifest.get('encrypted', False):
                if not password:
                    raise ValueError("Password required for encrypted backup")
                archive_path = self._decrypt_file(archive_path, password)
            
            # Create temporary directory for extraction
            temp_dir = backup_path / "temp_restore"
            temp_dir.mkdir()
            
            try:
                # Extract archive
                with tarfile.open(archive_path) as tar:
                    tar.extractall(temp_dir)
                
                # Restore directories
                extracted_dir = temp_dir / backup_name
                for dir_name in manifest['directories']:
                    src_dir = extracted_dir / dir_name
                    dst_dir = self.root_dir / dir_name
                    
                    if src_dir.exists():
                        if dst_dir.exists():
                            shutil.rmtree(dst_dir)
                        shutil.copytree(src_dir, dst_dir)
                
                self.logger.info(f"Backup restored successfully: {backup_name}")
                return True
                
            finally:
                # Clean up
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
                if manifest.get('encrypted', False) and archive_path.exists():
                    archive_path.unlink()  # Remove decrypted archive
            
        except Exception as e:
            self.logger.error(f"Restore failed: {str(e)}")
            # Attempt to restore from temporary backup
            if 'temp_backup' in locals():
                self._restore_from_temp(temp_backup)
            return False

    def _verify_backup(self, backup_path: Path, manifest: Dict) -> bool:
        """Verify backup integrity using stored hash."""
        try:
            archive_path = backup_path / manifest['archive_path']
            if not archive_path.exists():
                self.logger.error("Archive file not found")
                return False
            
            # Verify archive hash
            current_hash = self._calculate_file_hash(archive_path)
            if current_hash != manifest['archive_hash']:
                self.logger.error("Archive hash mismatch")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Backup verification failed: {str(e)}")
            return False

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read the file in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _rotate_backups(self) -> None:
        """Remove old backups while keeping the specified maximum number."""
        try:
            backups = []
            for backup_dir in self.backup_dir.iterdir():
                if backup_dir.is_dir() and backup_dir.name.startswith('system_backup_'):
                    manifest_path = backup_dir / 'manifest.json'
                    if manifest_path.exists():
                        with open(manifest_path) as f:
                            manifest = json.load(f)
                        backups.append((manifest['timestamp'], backup_dir))
            
            # Sort by timestamp (oldest first)
            backups.sort()
            
            # Remove oldest backups if we exceed max_backups
            while len(backups) > self.max_backups:
                _, backup_dir = backups.pop(0)
                shutil.rmtree(backup_dir)
                self.logger.info(f"Removed old backup: {backup_dir.name}")
                
        except Exception as e:
            self.logger.error(f"Backup rotation failed: {str(e)}")

    def _encrypt_file(self, file_path: Path, password: str) -> Path:
        """Encrypt a file using Fernet symmetric encryption."""
        # Generate key from password
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        f = Fernet(key)
        
        # Encrypt file
        encrypted_path = file_path.with_suffix(file_path.suffix + '.enc')
        with open(file_path, 'rb') as src, open(encrypted_path, 'wb') as dst:
            # Write salt first
            dst.write(salt)
            # Then write encrypted data
            dst.write(f.encrypt(src.read()))
        
        # Remove original file
        file_path.unlink()
        
        return encrypted_path

    def _decrypt_file(self, file_path: Path, password: str) -> Path:
        """Decrypt a file using Fernet symmetric encryption."""
        # Read salt and encrypted data
        with open(file_path, 'rb') as f:
            salt = f.read(16)
            encrypted_data = f.read()
        
        # Generate key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        f = Fernet(key)
        
        # Decrypt to new file
        decrypted_path = file_path.with_suffix('').with_suffix('')
        with open(decrypted_path, 'wb') as dst:
            dst.write(f.decrypt(encrypted_data))
        
        return decrypted_path

    def _restore_from_temp(self, temp_backup_path: str) -> bool:
        """Restore system from a temporary backup in case of failure."""
        try:
            if not temp_backup_path or not Path(temp_backup_path).exists():
                self.logger.error("No temporary backup available for restoration")
                return False
                
            # Read manifest
            manifest_path = Path(temp_backup_path) / 'manifest.json'
            if not manifest_path.exists():
                self.logger.error("No manifest found in temporary backup")
                return False
                
            with open(manifest_path) as f:
                manifest = json.load(f)
            
            # Verify backup before restoring
            if not self._verify_backup(Path(temp_backup_path), manifest):
                self.logger.error("Temporary backup verification failed")
                return False
            
            # Get archive path
            archive_path = Path(temp_backup_path) / manifest['archive_path']
            
            # Create temporary directory for extraction
            temp_dir = Path(temp_backup_path) / "temp_restore"
            temp_dir.mkdir()
            
            try:
                # Extract archive
                with tarfile.open(archive_path) as tar:
                    tar.extractall(temp_dir)
                
                # Restore directories
                extracted_dir = temp_dir / manifest['name']
                for dir_name in manifest['directories']:
                    src_dir = extracted_dir / dir_name
                    dst_dir = self.root_dir / dir_name
                    
                    if src_dir.exists():
                        if dst_dir.exists():
                            shutil.rmtree(dst_dir)
                        shutil.copytree(src_dir, dst_dir)
                
                self.logger.info("Successfully restored from temporary backup")
                return True
                
            finally:
                # Clean up
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
                
        except Exception as e:
            self.logger.error(f"Failed to restore from temporary backup: {str(e)}")
            return False

    # === Core Cleanup Features ===

    def cleanup_system(self) -> Dict[str, List[str]]:
        """Clean up the system by identifying and quarantining outdated or duplicate files."""
        results = {
            'quarantined': [],
            'duplicates': [],
            'outdated': []
        }
        
        try:
            # Get file metadata
            metadata = self._collect_file_metadata()
            
            # Find duplicates
            duplicates = self._find_duplicate_files(metadata)
            results['duplicates'] = duplicates
            
            # Find outdated files
            outdated = self._find_outdated_files(metadata)
            results['outdated'] = outdated
            
            # Move files to quarantine
            for file_path in duplicates + outdated:
                if self._quarantine_file(file_path):
                    results['quarantined'].append(file_path)
            
            self.logger.info(f"Cleanup completed: {len(results['quarantined'])} files quarantined")
            return results
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")
            raise

    def _collect_file_metadata(self) -> List[Dict]:
        """Collect metadata for all files in the system."""
        data = []
        
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and not self._is_excluded(file_path):
                try:
                    stat = file_path.stat()
                    data.append({
                        'path': str(file_path),
                        'size': stat.st_size,
                        'modified': datetime.datetime.fromtimestamp(stat.st_mtime),
                        'hash': self._calculate_file_hash(file_path),
                        'extension': file_path.suffix.lower()
                    })
                except Exception as e:
                    self.logger.warning(f"Could not collect metadata for {file_path}: {str(e)}")
        
        return data

    def _find_duplicate_files(self, metadata: List[Dict]) -> List[str]:
        """Find duplicate files based on content hash."""
        duplicates = []
        hash_groups = {}
        
        # Group files by hash
        for file_data in metadata:
            file_hash = file_data['hash']
            if file_hash in hash_groups:
                hash_groups[file_hash].append(file_data)
            else:
                hash_groups[file_hash] = [file_data]
        
        # Find duplicates
        for files in hash_groups.values():
            if len(files) > 1:
                # Sort by modified time, newest first
                files.sort(key=lambda x: x['modified'], reverse=True)
                # Add all but the newest file to duplicates
                duplicates.extend(f['path'] for f in files[1:])
        
        return duplicates

    def _find_outdated_files(self, metadata: List[Dict]) -> List[str]:
        """Find outdated files based on modification time."""
        outdated = []
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=90)
        
        for file_data in metadata:
            if file_data['modified'] < cutoff_date:
                outdated.append(file_data['path'])
        
        return list(set(outdated))

    # === Core Quarantine Features ===

    def _quarantine_file(self, file_path: str) -> bool:
        """Move a file to quarantine directory while preserving its path structure."""
        try:
            src_path = Path(file_path)
            if not src_path.exists():
                return False
            
            # Create relative path for quarantine
            rel_path = src_path.relative_to(self.root_dir)
            dst_path = self.quarantine_dir / rel_path
            
            # Create parent directories
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file to quarantine
            shutil.move(str(src_path), str(dst_path))
            
            # Create metadata file
            metadata = {
                'original_path': str(file_path),
                'quarantine_date': datetime.datetime.now().isoformat(),
                'reason': 'automated_cleanup'
            }
            
            metadata_path = dst_path.with_suffix('.meta.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to quarantine {file_path}: {str(e)}")
            return False

    def _is_excluded(self, file_path: Path) -> bool:
        """Check if a file should be excluded from analysis."""
        excluded_dirs = {
            self.quarantine_dir,
            self.backup_dir,
            self.root_dir / 'logs',
            self.root_dir / '.git',
            self.root_dir / 'node_modules',
            self.root_dir / 'venv'
        }
        
        excluded_extensions = {'.pyc', '.pyo', '.pyd', '.git'}
        
        return (
            any(parent in excluded_dirs for parent in file_path.parents) or
            file_path.suffix in excluded_extensions
        )

    def list_quarantined_files(self) -> List[Dict]:
        """List all files in quarantine with their metadata."""
        quarantined = []
        
        for meta_file in self.quarantine_dir.rglob('*.meta.json'):
            try:
                with open(meta_file) as f:
                    metadata = json.load(f)
                    file_path = meta_file.with_suffix('').with_suffix('')  # Remove .meta.json
                    if file_path.exists():
                        metadata['path'] = str(file_path)
                        quarantined.append(metadata)
            except Exception as e:
                self.logger.warning(f"Could not read metadata for {meta_file}: {str(e)}")
        
        return quarantined

    def restore_from_quarantine(self, file_path: str) -> bool:
        """Restore a file from quarantine to its original location."""
        try:
            quarantine_path = Path(file_path)
            meta_path = quarantine_path.with_suffix('.meta.json')
            
            if not quarantine_path.exists() or not meta_path.exists():
                return False
            
            # Read metadata
            with open(meta_path) as f:
                metadata = json.load(f)
            
            # Get original path
            original_path = Path(metadata['original_path'])
            original_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file back
            shutil.move(str(quarantine_path), str(original_path))
            meta_path.unlink()
            
            self.logger.info(f"Restored file from quarantine: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore {file_path}: {str(e)}")
            return False

    def get_system_stats(self) -> Dict:
        """Get system statistics."""
        stats = {
            'total_files': 0,
            'total_size': 0,
            'recent_activity': {
                'modified_24h': 0,
                'modified_7d': 0,
                'modified_30d': 0
            },
            'file_types': {},
            'quarantine': {
                'total_files': 0,
                'total_size': 0
            },
            'backups': {
                'count': 0,
                'total_size': 0,
                'latest': None
            }
        }
        
        try:
            now = datetime.datetime.now()
            
            # Analyze main system files
            for file_path in self.root_dir.rglob('*'):
                if file_path.is_file() and not self._is_excluded(file_path):
                    stats['total_files'] += 1
                    size = file_path.stat().st_size
                    stats['total_size'] += size
                    
                    # Check modification time
                    mtime = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                    if (now - mtime).days < 1:
                        stats['recent_activity']['modified_24h'] += 1
                    if (now - mtime).days < 7:
                        stats['recent_activity']['modified_7d'] += 1
                    if (now - mtime).days < 30:
                        stats['recent_activity']['modified_30d'] += 1
                    
                    # Count file types
                    ext = file_path.suffix.lower() or 'no extension'
                    stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1
            
            # Count quarantined files
            for file_path in self.quarantine_dir.rglob('*'):
                if file_path.is_file() and not file_path.name.endswith('.meta.json'):
                    stats['quarantine']['total_files'] += 1
                    stats['quarantine']['total_size'] += file_path.stat().st_size
            
            # Count backups
            latest_backup = None
            for backup_dir in self.backup_dir.iterdir():
                if backup_dir.is_dir():
                    stats['backups']['count'] += 1
                    manifest_path = backup_dir / 'manifest.json'
                    if manifest_path.exists():
                        with open(manifest_path) as f:
                            manifest = json.load(f)
                            stats['backups']['total_size'] += manifest.get('total_size', 0)
                            if not latest_backup or manifest['timestamp'] > latest_backup:
                                latest_backup = manifest['timestamp']
            
            stats['backups']['latest'] = latest_backup
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get system stats: {str(e)}")
            raise

    # === Planned Features (Q2-Q4 2025) ===

    def schedule_backup(self, interval_hours: int = 24) -> None:
        """Schedule automatic backups at specified intervals.
        Planned for Q2 2025."""
        raise NotImplementedError("Scheduled for Q2 2025")

    def detect_anomalies(self) -> List[Dict]:
        """Use ML to detect anomalous files and patterns.
        Planned for Q2 2025."""
        raise NotImplementedError("Scheduled for Q2 2025")

    def backup_to_cloud(self, provider: str, credentials: Dict) -> str:
        """Upload backup to cloud storage.
        Planned for Q3 2025."""
        raise NotImplementedError("Scheduled for Q3 2025")

    def preserve_quantum_state(self) -> Dict:
        """Preserve system quantum state during operations.
        Planned for Q3 2025."""
        raise NotImplementedError("Scheduled for Q3 2025")

    def analyze_with_nexus(self) -> Dict:
        """Deep analysis of system state using NEXUS.
        Planned for Q4 2025."""
        raise NotImplementedError("Scheduled for Q4 2025")

    def validate_with_ethik(self, operation: str, target: str) -> bool:
        """Validate operations against ETHIK framework.
        Planned for Q4 2025."""
        raise NotImplementedError("Scheduled for Q4 2025")

    def reorganize_root_directory(self):
        """
        Reorganizes the root directory while preserving quantum subsystem connections
        and establishing mycelial networks between related files.
        """
        results = {
            'moved_files': [],
            'created_dirs': [],
            'mycelial_connections': [],
            'quantum_links': {},
            'errors': []
        }
        
        try:
            # Define quantum file mappings
            quantum_files = {
                'QUANTUM_PROMPTS/MASTER': [
                    'quantum_prompt_8.0.md',
                    'core_principles.md',
                    'cursor_ide_rules.md',
                    'VERSION_PERA.md'
                ],
                'QUANTUM_PROMPTS/ETHIK': [
                    'prompt_encoder.py',
                    'setup_session.txt'
                ],
                'QUANTUM_PROMPTS/ATLAS': [
                    'mycelium_monitor.js',
                    'update_roadmap.js'
                ],
                'QUANTUM_PROMPTS/CRONOS': [
                    'schedule_roadmap_update.js',
                    'start_monitor_simple.ps1',
                    'start_mycelium_monitor.ps1'
                ],
                'QUANTUM_PROMPTS/NEXUS': [
                    'create_postman_collection.ps1'
                ],
                'QUANTUM_PROMPTS/BIOS-Q': [
                    'start_server_simple.ps1'
                ]
            }
            
            # Create quantum directories and move files
            for dir_path, files in quantum_files.items():
                dir_path = Path(self.root_dir) / dir_path
                dir_path.mkdir(parents=True, exist_ok=True)
                results['created_dirs'].append(str(dir_path))
                
                for file_name in files:
                    source_file = Path(self.root_dir) / 'QUANTUM_PROMPTS' / file_name
                    if source_file.exists():
                        target_file = dir_path / file_name
                        try:
                            shutil.move(str(source_file), str(target_file))
                            results['moved_files'].append(f"Moved to subsystem: {source_file} -> {target_file}")
                            results['quantum_links'][str(target_file)] = dir_path.name
                        except Exception as e:
                            results['errors'].append(f"Error moving {file_name}: {str(e)}")
            
            # Move support files to appropriate directories
            support_mappings = {
                'web': ['web_client/*', 'RPG/*'],
                'tests': ['tests/*', 'pytest.ini'],
                'docs': ['README.md'],
                'config': ['package.json', 'package-lock.json', 'requirements.txt']
            }
            
            for target_dir, patterns in support_mappings.items():
                target_path = Path(self.root_dir) / target_dir
                target_path.mkdir(parents=True, exist_ok=True)
                
                for pattern in patterns:
                    source_dir = Path(self.root_dir) / 'QUANTUM_PROMPTS'
                    for source_file in source_dir.glob(pattern):
                        if source_file.is_file():
                            target_file = target_path / source_file.name
                            try:
                                if target_file.exists():
                                    quarantine_path = Path(self.root_dir) / 'quarantine' / source_file.name
                                    shutil.move(str(source_file), str(quarantine_path))
                                    results['moved_files'].append(f"Quarantined: {source_file} -> {quarantine_path}")
                                else:
                                    shutil.move(str(source_file), str(target_file))
                                    results['moved_files'].append(f"Moved: {source_file} -> {target_file}")
                            except Exception as e:
                                results['errors'].append(f"Error moving {source_file}: {str(e)}")
            
            # Clean up empty directories
            for empty_dir in Path(self.root_dir).glob('**/'):
                try:
                    if empty_dir.is_dir() and not any(empty_dir.iterdir()):
                        empty_dir.rmdir()
                        results['moved_files'].append(f"Removed empty directory: {empty_dir}")
                except Exception:
                    pass
            
            return results
            
        except Exception as e:
            results['errors'].append(str(e))
            return results

    def migrate_bios_q(self) -> Dict[str, Any]:
        """
        Migra o BIOS-Q para QUANTUM_PROMPTS/BIOS-Q com segurança.
        
        Returns:
            Dict com resultados da migração
        """
        results = {
            'success': False,
            'files_moved': [],
            'errors': [],
            'preserved_files': []
        }
        
        try:
            # 1. Criar diretório de backup temporário
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_backup = self.temp_dir / f"bios_q_backup_{timestamp}"
            temp_backup.mkdir(exist_ok=True)
            
            # 2. Preservar arquivos existentes em QUANTUM_PROMPTS/BIOS-Q
            bios_q_target = self.quantum_dir / "BIOS-Q"
            if bios_q_target.exists():
                for item in bios_q_target.glob('*'):
                    if item.is_file():
                        shutil.copy2(item, temp_backup)
                        results['preserved_files'].append(str(item.name))
            
            # 3. Mover arquivos do BIOS-Q original
            bios_q_source = self.root_dir / "BIOS-Q"
            if bios_q_source.exists():
                # Primeiro, copiar tudo
                if not bios_q_target.exists():
                    bios_q_target.mkdir(parents=True)
                for item in bios_q_source.glob('**/*'):
                    if item.is_file():
                        relative_path = item.relative_to(bios_q_source)
                        target_file = bios_q_target / relative_path
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, target_file)
                        results['files_moved'].append(str(relative_path))
                
                # 4. Atualizar caminhos nos arquivos
                self._update_bios_q_paths(bios_q_target)
                
                results['success'] = True
                
            else:
                results['errors'].append("BIOS-Q source directory not found")
                
        except Exception as e:
            results['errors'].append(f"Error during BIOS-Q migration: {str(e)}")
            
        return results
    
    def _update_bios_q_paths(self, bios_q_dir: Path):
        """
        Atualiza os caminhos nos arquivos do BIOS-Q para refletir a nova estrutura.
        """
        try:
            # Atualizar arquivos .bat
            for bat_file in bios_q_dir.glob('**/*.bat'):
                with open(bat_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Atualizar caminhos
                content = content.replace(
                    'cd "C:\\Eva Guarani EGOS\\BIOS-Q"',
                    'cd "C:\\Eva Guarani EGOS\\QUANTUM_PROMPTS\\BIOS-Q"'
                )
                
                with open(bat_file, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Atualizar arquivos .py
            for py_file in bios_q_dir.glob('**/*.py'):
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Atualizar caminhos
                content = content.replace(
                    'BIOS_Q_DIR = Path("BIOS-Q")',
                    'BIOS_Q_DIR = Path("QUANTUM_PROMPTS/BIOS-Q")'
                )
                
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            # Atualizar arquivos de configuração
            config_files = list(bios_q_dir.glob('**/*.cfg')) + list(bios_q_dir.glob('**/*.toml'))
            for config_file in config_files:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Atualizar caminhos
                content = content.replace(
                    'path = "BIOS-Q"',
                    'path = "QUANTUM_PROMPTS/BIOS-Q"'
                )
                
                with open(config_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
        except Exception as e:
            self.logger.error(f"Error updating BIOS-Q paths: {str(e)}")
            raise 