"""Metadata scanner module for analyzing and tracking file metadata."""

import os
import ast
import json
import hashlib
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, asdict
import pandas as pd

@dataclass
class FileMetadata:
    path: str
    name: str
    extension: str
    size: int
    created: datetime
    modified: datetime
    last_accessed: datetime
    md5_hash: str
    imports: List[str]
    dependencies: List[str]
    subsystem: Optional[str]
    purpose: Optional[str]
    quantum_metrics: Dict[str, float]
    usage_count: int
    is_active: bool

class MetadataScanner:
    """Scanner for collecting and analyzing file metadata."""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.logger = logging.getLogger("metadata_scanner")
        self.logger.setLevel(logging.INFO)
        
        # Setup logging
        log_dir = self.root_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        handler = logging.FileHandler(log_dir / "metadata_scanner.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        
        # Excluded paths
        self.excluded_dirs = {
            self.root_dir / "backups",
            self.root_dir / "quarantine",
            self.root_dir / "node_modules",
            self.root_dir / ".git",
            self.root_dir / "logs"
        }
        
        self.excluded_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.log'}
        
        self.metadata_db: Dict[str, FileMetadata] = {}
        self.dependency_graph: Dict[str, Set[str]] = {}
        self.subsystem_rules = {
            'core': {
                'patterns': ['core/*'],
                'allowed_types': ['.py', '.js', '.ts'],
                'purpose': ['system', 'service', 'model']
            },
            'web': {
                'patterns': ['web/*'],
                'allowed_types': ['.html', '.css', '.js'],
                'purpose': ['interface', 'client', 'style']
            },
            'quantum_prompts': {
                'patterns': ['QUANTUM_PROMPTS/*'],
                'allowed_types': ['.md', '.txt'],
                'purpose': ['documentation', 'configuration']
            }
        }
        
    def scan_system(self, root_dir: str) -> None:
        """Scan the entire system and build metadata database."""
        print(f"Starting system scan from {root_dir}")
        
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    metadata = self._extract_file_metadata(filepath)
                    if metadata:
                        self.metadata_db[filepath] = metadata
                        self._update_dependency_graph(metadata)
                except Exception as e:
                    print(f"Error processing {filepath}: {str(e)}")
        
        self._analyze_relationships()
        self._calculate_quantum_metrics()
        self._save_metadata()
    
    def scan_directory(self, directory: Optional[str] = None) -> pd.DataFrame:
        """Scan a directory and collect metadata for all files."""
        scan_path = Path(directory) if directory else self.root_dir
        data = []
        
        try:
            for file_path in scan_path.rglob('*'):
                if self._should_process_file(file_path):
                    try:
                        metadata = self._collect_file_metadata(file_path)
                        data.append(metadata)
                    except Exception as e:
                        self.logger.warning(f"Failed to process {file_path}: {str(e)}")
            
            return pd.DataFrame(data)
            
        except Exception as e:
            self.logger.error(f"Scan failed for {scan_path}: {str(e)}")
            raise
    
    def _should_process_file(self, file_path: Path) -> bool:
        """Check if a file should be processed."""
        if not file_path.is_file():
            return False
            
        if any(parent in self.excluded_dirs for parent in file_path.parents):
            return False
            
        if file_path.suffix.lower() in self.excluded_extensions:
            return False
            
        if file_path.name.startswith('.'):
            return False
            
        return True
    
    def _collect_file_metadata(self, file_path: Path) -> Dict:
        """Collect metadata for a single file."""
        stat = file_path.stat()
        
        return {
            'path': str(file_path),
            'name': file_path.name,
            'extension': file_path.suffix.lower(),
            'size': stat.st_size,
            'created': datetime.datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.datetime.fromtimestamp(stat.st_mtime),
            'accessed': datetime.datetime.fromtimestamp(stat.st_atime),
            'hash': self._calculate_file_hash(file_path),
            'is_symlink': file_path.is_symlink(),
            'relative_path': str(file_path.relative_to(self.root_dir))
        }
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        hasher = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            self.logger.warning(f"Failed to calculate hash for {file_path}: {str(e)}")
            return ''
    
    def _extract_file_metadata(self, filepath: str) -> Optional[FileMetadata]:
        """Extract metadata from a file."""
        if not os.path.exists(filepath):
            return None
            
        stat = os.stat(filepath)
        name = os.path.basename(filepath)
        ext = os.path.splitext(name)[1]
        
        with open(filepath, 'rb') as f:
            content = f.read()
            md5 = hashlib.md5(content).hexdigest()
        
        imports = []
        if ext in ['.py', '.js', '.ts']:
            imports = self._extract_imports(filepath)
        
        subsystem = self._detect_subsystem(filepath)
        purpose = self._detect_purpose(filepath)
        
        return FileMetadata(
            path=filepath,
            name=name,
            extension=ext,
            size=stat.st_size,
            created=datetime.datetime.fromtimestamp(stat.st_ctime),
            modified=datetime.datetime.fromtimestamp(stat.st_mtime),
            last_accessed=datetime.datetime.fromtimestamp(stat.st_atime),
            md5_hash=md5,
            imports=imports,
            dependencies=[],  # Will be populated later
            subsystem=subsystem,
            purpose=purpose,
            quantum_metrics={
                'consciousness': 0.0,
                'harmony': 0.0,
                'evolution': 0.0
            },
            usage_count=0,
            is_active=True
        )
    
    def _extract_imports(self, filepath: str) -> List[str]:
        """Extract import statements from a file."""
        imports = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if filepath.endswith('.py'):
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            imports.append(name.name)
                    elif isinstance(node, ast.ImportFrom):
                        imports.append(node.module)
            elif filepath.endswith('.js') or filepath.endswith('.ts'):
                # Simple regex for JS/TS imports (can be enhanced)
                import re
                import_patterns = [
                    r'import\s+.*\s+from\s+[\'"](.+)[\'"]',
                    r'require\([\'"](.+)[\'"]\)'
                ]
                for pattern in import_patterns:
                    matches = re.findall(pattern, content)
                    imports.extend(matches)
        except Exception as e:
            print(f"Error extracting imports from {filepath}: {str(e)}")
        
        return imports
    
    def _detect_subsystem(self, filepath: str) -> Optional[str]:
        """Detect which subsystem a file belongs to."""
        for subsystem, rules in self.subsystem_rules.items():
            for pattern in rules['patterns']:
                if self._matches_pattern(filepath, pattern):
                    if os.path.splitext(filepath)[1] in rules['allowed_types']:
                        return subsystem
        return None
    
    def _detect_purpose(self, filepath: str) -> Optional[str]:
        """Detect the purpose of a file based on its location and content."""
        filename = os.path.basename(filepath)
        if 'test' in filename.lower():
            return 'test'
        elif filepath.endswith('.md'):
            return 'documentation'
        elif '/core/' in filepath:
            return 'system'
        elif '/web/' in filepath:
            return 'interface'
        return None
    
    def _matches_pattern(self, filepath: str, pattern: str) -> bool:
        """Check if a filepath matches a pattern."""
        from fnmatch import fnmatch
        return fnmatch(filepath, pattern)
    
    def _update_dependency_graph(self, metadata: FileMetadata) -> None:
        """Update the dependency graph with file relationships."""
        self.dependency_graph[metadata.path] = set()
        for imp in metadata.imports:
            # Find corresponding file for import
            for path in self.metadata_db:
                if path.endswith(f"{imp.replace('.', '/')}.py") or \
                   path.endswith(f"{imp.replace('.', '/')}.js") or \
                   path.endswith(f"{imp.replace('.', '/')}.ts"):
                    self.dependency_graph[metadata.path].add(path)
    
    def _analyze_relationships(self) -> None:
        """Analyze relationships between files."""
        for filepath, metadata in self.metadata_db.items():
            # Update dependencies list
            metadata.dependencies = list(self.dependency_graph.get(filepath, set()))
            
            # Calculate usage count
            usage_count = 0
            for deps in self.dependency_graph.values():
                if filepath in deps:
                    usage_count += 1
            metadata.usage_count = usage_count
    
    def _calculate_quantum_metrics(self) -> None:
        """Calculate quantum metrics for each file."""
        for metadata in self.metadata_db.values():
            # Calculate consciousness based on relationships and purpose
            consciousness = min(1.0, (len(metadata.dependencies) + metadata.usage_count) / 20)
            
            # Calculate harmony based on proper placement and organization
            harmony = 1.0 if metadata.subsystem and metadata.purpose else 0.5
            
            # Calculate evolution based on modifications and usage
            age = (datetime.datetime.now() - metadata.created).days
            recent_mods = (datetime.datetime.now() - metadata.modified).days < 30
            evolution = min(1.0, (metadata.usage_count / 10) + (0.3 if recent_mods else 0))
            
            metadata.quantum_metrics = {
                'consciousness': consciousness,
                'harmony': harmony,
                'evolution': evolution
            }
    
    def _save_metadata(self) -> None:
        """Save metadata to a JSON file."""
        output = {
            'last_scan': datetime.datetime.now().isoformat(),
            'files': {
                path: asdict(metadata)
                for path, metadata in self.metadata_db.items()
            }
        }
        
        with open('metadata_scan.json', 'w') as f:
            json.dump(output, f, indent=2, default=str)
    
    def get_misplaced_files(self) -> List[Dict[str, str]]:
        """Get list of files that should be in different locations."""
        misplaced = []
        for filepath, metadata in self.metadata_db.items():
            correct_subsystem = self._detect_subsystem(filepath)
            if metadata.subsystem != correct_subsystem:
                misplaced.append({
                    'file': filepath,
                    'current_subsystem': metadata.subsystem,
                    'suggested_subsystem': correct_subsystem,
                    'reason': 'File type and purpose better match another subsystem'
                })
        return misplaced
    
    def get_inactive_files(self, days_threshold: int = 30) -> List[Dict[str, str]]:
        """Get list of potentially inactive files."""
        inactive = []
        now = datetime.datetime.now()
        for filepath, metadata in self.metadata_db.items():
            days_since_access = (now - metadata.last_accessed).days
            if days_since_access > days_threshold and metadata.usage_count == 0:
                inactive.append({
                    'file': filepath,
                    'last_accessed': metadata.last_accessed.isoformat(),
                    'days_inactive': days_since_access,
                    'suggested_action': 'Review for removal or archival'
                })
        return inactive
    
    def get_replacement_candidates(self) -> List[Dict[str, str]]:
        """Get list of files that might have been replaced by newer versions."""
        candidates = []
        for filepath, metadata in self.metadata_db.items():
            # Look for files with similar names or purposes
            name_base = os.path.splitext(metadata.name)[0]
            for other_path, other_meta in self.metadata_db.items():
                if filepath != other_path and \
                   name_base in other_meta.name and \
                   metadata.purpose == other_meta.purpose and \
                   metadata.modified < other_meta.modified:
                    candidates.append({
                        'old_file': filepath,
                        'new_file': other_path,
                        'reason': 'Newer file with similar name and purpose exists'
                    })
        return candidates
    
    def find_duplicates(self, scan_result: Optional[pd.DataFrame] = None) -> Dict[str, List[str]]:
        """Find duplicate files based on content hash."""
        if scan_result is None:
            scan_result = self.scan_directory()
        
        duplicates = {}
        hash_groups = scan_result.groupby('hash')
        
        for file_hash, group in hash_groups:
            if len(group) > 1 and file_hash:  # Skip empty hashes
                duplicates[file_hash] = group['path'].tolist()
        
        return duplicates
    
    def find_large_files(self, min_size_mb: float = 100.0, scan_result: Optional[pd.DataFrame] = None) -> List[Dict]:
        """Find files larger than the specified size."""
        if scan_result is None:
            scan_result = self.scan_directory()
        
        min_size_bytes = min_size_mb * 1024 * 1024
        large_files = scan_result[scan_result['size'] >= min_size_bytes]
        
        return large_files.to_dict('records')
    
    def find_old_files(self, days: int = 90, scan_result: Optional[pd.DataFrame] = None) -> List[Dict]:
        """Find files not modified in the specified number of days."""
        if scan_result is None:
            scan_result = self.scan_directory()
        
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        old_files = scan_result[scan_result['modified'] < cutoff_date]
        
        return old_files.to_dict('records')
    
    def get_extension_stats(self, scan_result: Optional[pd.DataFrame] = None) -> Dict[str, Dict]:
        """Get statistics about file extensions."""
        if scan_result is None:
            scan_result = self.scan_directory()
        
        stats = {}
        for ext, group in scan_result.groupby('extension'):
            stats[ext or 'no_extension'] = {
                'count': len(group),
                'total_size': group['size'].sum(),
                'avg_size': group['size'].mean(),
                'newest': group['modified'].max().isoformat(),
                'oldest': group['modified'].min().isoformat()
            }
        
        return stats
    
    def get_activity_timeline(self, days: int = 30, scan_result: Optional[pd.DataFrame] = None) -> Dict[str, int]:
        """Get file modification activity timeline."""
        if scan_result is None:
            scan_result = self.scan_directory()
        
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        # Create date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        timeline = {d.strftime('%Y-%m-%d'): 0 for d in date_range}
        
        # Count modifications per day
        for date, group in scan_result.groupby(scan_result['modified'].dt.strftime('%Y-%m-%d')):
            if date in timeline:
                timeline[date] = len(group)
        
        return timeline 