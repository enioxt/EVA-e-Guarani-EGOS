"""
CRONOS File Unification System
=============================

This module provides systematic methods for unifying and organizing files across different
directories, handling duplicates, and managing file migrations with proper backup.

Key Features:
- File comparison and deduplication
- Reference updating
- Safe migration to quarantine
- Metadata preservation
- Mycelial integration for tracking changes

Author: EVA & GUARANI
Version: 1.0
"""

import os
import shutil
import hashlib
import json
import datetime
from typing import Dict, List, Tuple, Set
from pathlib import Path

class FileUnificationSystem:
    def __init__(self, base_path: str):
        """Initialize the file unification system.
        
        Args:
            base_path: Root path for all operations
        """
        self.base_path = Path(base_path)
        self.quarantine_path = self.base_path / "quarantine"
        self.metadata_path = self.base_path / "METADATA"
        self.mycelium_path = self.base_path / "QUANTUM_PROMPTS/CRONOS/mycelium"
        
        # Ensure required directories exist
        self.quarantine_path.mkdir(exist_ok=True)
        self.metadata_path.mkdir(exist_ok=True)
        self.mycelium_path.mkdir(exist_ok=True)

    def generate_file_signature(self, file_path: Path) -> Dict:
        """Generate a unique signature for a file including metadata.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dict containing file signature and metadata
        """
        if not file_path.exists():
            return None
            
        with open(file_path, 'rb') as f:
            content = f.read()
            
        return {
            'hash': hashlib.sha256(content).hexdigest(),
            'size': file_path.stat().st_size,
            'modified': datetime.datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            'path': str(file_path.relative_to(self.base_path))
        }

    def find_duplicates(self, source_dir: Path, target_dir: Path) -> Dict[str, List[Path]]:
        """Find duplicate files between source and target directories.
        
        Args:
            source_dir: Source directory path
            target_dir: Target directory path
            
        Returns:
            Dict mapping file signatures to lists of duplicate paths
        """
        duplicates = {}
        
        for dir_path in [source_dir, target_dir]:
            for file_path in dir_path.rglob('*'):
                if file_path.is_file():
                    signature = self.generate_file_signature(file_path)
                    if signature:
                        hash_key = signature['hash']
                        if hash_key not in duplicates:
                            duplicates[hash_key] = []
                        duplicates[hash_key].append(file_path)
                        
        return {k: v for k, v in duplicates.items() if len(v) > 1}

    def update_references(self, old_path: Path, new_path: Path, search_dirs: List[Path]) -> List[Tuple[Path, int]]:
        """Update references to old file paths in all relevant files.
        
        Args:
            old_path: Original file path
            new_path: New file path
            search_dirs: List of directories to search for references
            
        Returns:
            List of tuples containing (modified_file, number_of_replacements)
        """
        modified_files = []
        old_ref = str(old_path.relative_to(self.base_path))
        new_ref = str(new_path.relative_to(self.base_path))
        
        for search_dir in search_dirs:
            for file_path in search_dir.rglob('*'):
                if file_path.is_file() and file_path.suffix in ['.py', '.md', '.txt', '.json', '.toml', '.yml', '.yaml']:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        if old_ref in content:
                            new_content = content.replace(old_ref, new_ref)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            modified_files.append((file_path, content.count(old_ref)))
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
                        
        return modified_files

    def create_quarantine_backup(self, source_path: Path) -> Path:
        """Create a backup of files in quarantine with metadata preservation.
        
        Args:
            source_path: Path to be quarantined
            
        Returns:
            Path to quarantine location
        """
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        quarantine_name = f"{source_path.name}_backup_{timestamp}"
        quarantine_dir = self.quarantine_path / quarantine_name
        
        # Create quarantine directory
        quarantine_dir.mkdir(exist_ok=True)
        
        # Copy files with metadata
        shutil.copytree(source_path, quarantine_dir / source_path.name, dirs_exist_ok=True)
        
        # Save metadata
        metadata = {
            'original_path': str(source_path.relative_to(self.base_path)),
            'timestamp': timestamp,
            'reason': 'file_unification',
            'file_signatures': {}
        }
        
        for file_path in source_path.rglob('*'):
            if file_path.is_file():
                signature = self.generate_file_signature(file_path)
                if signature:
                    metadata['file_signatures'][str(file_path.relative_to(source_path))] = signature
                    
        metadata_file = self.metadata_path / f"{quarantine_name}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
            
        return quarantine_dir

    def unify_directories(self, source_dir: Path, target_dir: Path, search_dirs: List[Path] = None) -> Dict:
        """Unify two directories, handling duplicates and updating references.
        
        Args:
            source_dir: Source directory to be unified
            target_dir: Target directory to unify into
            search_dirs: Optional list of directories to search for references
            
        Returns:
            Dict containing unification results and statistics
        """
        if search_dirs is None:
            search_dirs = [self.base_path]
            
        results = {
            'duplicates_found': 0,
            'files_moved': 0,
            'references_updated': 0,
            'modified_files': [],
            'quarantine_path': None,
            'errors': []
        }
        
        try:
            # Find duplicates
            duplicates = self.find_duplicates(source_dir, target_dir)
            results['duplicates_found'] = sum(len(v) for v in duplicates.values())
            
            # Create quarantine backup
            quarantine_path = self.create_quarantine_backup(source_dir)
            results['quarantine_path'] = str(quarantine_path)
            
            # Process each file
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    signature = self.generate_file_signature(file_path)
                    if signature:
                        relative_path = file_path.relative_to(source_dir)
                        target_file = target_dir / relative_path
                        
                        # Create parent directories if needed
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Move unique files or newer versions
                        if not target_file.exists() or (
                            target_file.exists() and 
                            file_path.stat().st_mtime > target_file.stat().st_mtime
                        ):
                            shutil.copy2(file_path, target_file)
                            results['files_moved'] += 1
                            
                            # Update references
                            modified = self.update_references(file_path, target_file, search_dirs)
                            results['references_updated'] += len(modified)
                            results['modified_files'].extend([str(m[0]) for m in modified])
                            
            # Clean up source directory after successful migration
            shutil.rmtree(source_dir)
            
        except Exception as e:
            results['errors'].append(str(e))
            
        # Save operation metadata
        operation_metadata = {
            'timestamp': datetime.datetime.now().isoformat(),
            'source_dir': str(source_dir),
            'target_dir': str(target_dir),
            'results': results
        }
        
        metadata_file = self.metadata_path / f"unification_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(operation_metadata, f, indent=2)
            
        return results

    def verify_unification(self, results: Dict) -> bool:
        """Verify the success of a unification operation.
        
        Args:
            results: Results dictionary from unify_directories
            
        Returns:
            Boolean indicating verification success
        """
        if results['errors']:
            return False
            
        quarantine_path = Path(results['quarantine_path'])
        return (
            quarantine_path.exists() and
            results['files_moved'] > 0 and
            len(results['modified_files']) >= results['references_updated']
        )

def create_unification_system(base_path: str) -> FileUnificationSystem:
    """Factory function to create a FileUnificationSystem instance.
    
    Args:
        base_path: Base path for the system
        
    Returns:
        Configured FileUnificationSystem instance
    """
    return FileUnificationSystem(base_path) 