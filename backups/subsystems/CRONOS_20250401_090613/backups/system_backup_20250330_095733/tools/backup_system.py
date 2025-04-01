"""EVA & GUARANI - System Backup Module
Version: 8.0
"""

import os
import shutil
import json
import hashlib
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional
import time

class SystemBackup:
    """Handles system backup operations with versioning and integrity checks."""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.backup_dir = self.root_dir / "backups"
        self.quantum_dir = self.root_dir / "QUANTUM_PROMPTS"
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger("system_backup")
        self.logger.setLevel(logging.INFO)
        log_dir = self.root_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        handler = logging.FileHandler(log_dir / "backup.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        
        # Directories to backup
        self.backup_dirs = [
            'core',
            'web',
            'tools',
            'QUANTUM_PROMPTS',
            'METADATA',
            'ETHIK',
            'ATLAS',
            'NEXUS',
            'CRONOS'
        ]
        
        # Files to exclude
        self.exclude_patterns = {
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '*.so',
            '*.dll',
            '__pycache__',
            '.git',
            'node_modules',
            'backups',
            'logs'
        }
    
    def create_backup(self, name: Optional[str] = None) -> str:
        """Create a new backup with versioning."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = name or f"system_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        try:
            # Create backup directory
            backup_path.mkdir(exist_ok=True)
            
            # Initialize manifest
            manifest = {
                'timestamp': timestamp,
                'name': backup_name,
                'version': '8.0',
                'directories': {},
                'files': {},
                'quantum_state': self._get_quantum_state()
            }
            
            # Copy directories
            total_size = 0
            total_files = 0
            
            for dir_name in self.backup_dirs:
                src_dir = self.root_dir / dir_name
                if src_dir.exists():
                    dst_dir = backup_path / dir_name
                    dir_stats = self._backup_directory(src_dir, dst_dir)
                    
                    manifest['directories'][dir_name] = {
                        'size': dir_stats['size'],
                        'files': dir_stats['files'],
                        'hash': dir_stats['hash']
                    }
                    
                    total_size += dir_stats['size']
                    total_files += dir_stats['files']
            
            # Update manifest with totals
            manifest.update({
                'total_size': total_size,
                'total_files': total_files,
                'integrity_check': self._calculate_integrity_hash(backup_path)
            })
            
            # Save manifest
            manifest_path = backup_path / 'manifest.json'
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            self.logger.info(f"Backup created successfully: {backup_name}")
            return str(backup_path)
            
        except Exception as e:
            self.logger.error(f"Backup creation failed: {str(e)}")
            if backup_path.exists():
                shutil.rmtree(backup_path)
            raise
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore system from a backup."""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            self.logger.error(f"Backup not found: {backup_name}")
            return False
        
        try:
            # Verify backup integrity
            if not self._verify_backup_integrity(backup_path):
                self.logger.error(f"Backup integrity check failed: {backup_name}")
                return False
            
            # Create temporary backup of current state
            temp_backup = self.create_backup("temp_before_restore")
            
            # Restore directories
            for dir_name in self.backup_dirs:
                src_dir = backup_path / dir_name
                dst_dir = self.root_dir / dir_name
                
                if src_dir.exists():
                    if dst_dir.exists():
                        shutil.rmtree(dst_dir)
                    shutil.copytree(src_dir, dst_dir)
            
            self.logger.info(f"Backup restored successfully: {backup_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Restore failed: {str(e)}")
            # Attempt to restore from temporary backup
            self._restore_from_temp(temp_backup)
            return False
    
    def list_backups(self) -> List[Dict]:
        """List all available backups with their details."""
        backups = []
        
        for backup_dir in self.backup_dir.glob('system_backup_*'):
            manifest_path = backup_dir / 'manifest.json'
            if manifest_path.exists():
                try:
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                    backups.append({
                        'name': manifest['name'],
                        'timestamp': manifest['timestamp'],
                        'total_size': manifest['total_size'],
                        'total_files': manifest['total_files'],
                        'version': manifest.get('version', 'unknown'),
                        'integrity': self._verify_backup_integrity(backup_dir)
                    })
                except Exception as e:
                    self.logger.warning(f"Error reading backup manifest {backup_dir}: {str(e)}")
        
        return sorted(backups, key=lambda x: x['timestamp'], reverse=True)
    
    def _backup_directory(self, src_dir: Path, dst_dir: Path) -> Dict:
        """Backup a directory and return statistics."""
        stats = {'size': 0, 'files': 0, 'hash': ''}
        hasher = hashlib.sha256()
        
        # Copy directory
        shutil.copytree(src_dir, dst_dir, ignore=self._ignore_patterns)
        
        # Calculate statistics
        for file_path in dst_dir.rglob('*'):
            if file_path.is_file():
                size = file_path.stat().st_size
                stats['size'] += size
                stats['files'] += 1
                
                # Update directory hash
                with open(file_path, 'rb') as f:
                    hasher.update(f.read())
        
        stats['hash'] = hasher.hexdigest()
        return stats
    
    def _ignore_patterns(self, directory: str, contents: List[str]) -> List[str]:
        """Determine which files to exclude from backup."""
        ignored = []
        for pattern in self.exclude_patterns:
            for item in contents:
                if Path(item).match(pattern):
                    ignored.append(item)
        return ignored
    
    def _calculate_integrity_hash(self, backup_path: Path) -> str:
        """Calculate integrity hash for the entire backup."""
        hasher = hashlib.sha256()
        
        for file_path in sorted(backup_path.rglob('*')):
            if file_path.is_file() and file_path.name != 'manifest.json':
                hasher.update(file_path.name.encode())
                with open(file_path, 'rb') as f:
                    hasher.update(f.read())
        
        return hasher.hexdigest()
    
    def _verify_backup_integrity(self, backup_path: Path) -> bool:
        """Verify backup integrity using stored hash."""
        manifest_path = backup_path / 'manifest.json'
        if not manifest_path.exists():
            return False
        
        try:
            with open(manifest_path) as f:
                manifest = json.load(f)
            
            stored_hash = manifest.get('integrity_check')
            if not stored_hash:
                return False
            
            current_hash = self._calculate_integrity_hash(backup_path)
            return stored_hash == current_hash
            
        except Exception as e:
            self.logger.error(f"Integrity check failed: {str(e)}")
            return False
    
    def _get_quantum_state(self) -> Dict:
        """Get current quantum state from QUANTUM_PROMPTS."""
        state_file = self.quantum_dir / "quantum_state.json"
        if state_file.exists():
            try:
                with open(state_file) as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not read quantum state: {str(e)}")
        return {}
    
    def _restore_from_temp(self, temp_backup: str) -> None:
        """Attempt to restore from temporary backup in case of failure."""
        try:
            self.restore_backup(Path(temp_backup).name)
            self.logger.info("Successfully restored from temporary backup")
        except Exception as e:
            self.logger.error(f"Failed to restore from temporary backup: {str(e)}")
        finally:
            # Clean up temporary backup
            temp_path = Path(temp_backup)
            if temp_path.exists():
                shutil.rmtree(temp_path)
    
    def cleanup_old_backups(self, max_age_days: int = 30, min_keep: int = 5) -> None:
        """Clean up old backups while keeping a minimum number."""
        try:
            backups = self.list_backups()
            if len(backups) <= min_keep:
                return
            
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=max_age_days)
            
            # Sort backups by timestamp
            backups.sort(key=lambda x: x['timestamp'])
            
            # Keep the most recent backups
            to_keep = set(b['name'] for b in backups[-min_keep:])
            
            # Remove old backups
            for backup in backups[:-min_keep]:
                backup_time = datetime.datetime.strptime(backup['timestamp'], "%Y%m%d_%H%M%S")
                if backup_time < cutoff_date and backup['name'] not in to_keep:
                    backup_path = self.backup_dir / backup['name']
                    shutil.rmtree(backup_path)
                    self.logger.info(f"Removed old backup: {backup['name']}")
            
        except Exception as e:
            self.logger.error(f"Cleanup of old backups failed: {str(e)}") 