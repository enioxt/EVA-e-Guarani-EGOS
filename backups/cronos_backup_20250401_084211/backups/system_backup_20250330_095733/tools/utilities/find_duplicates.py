#!/usr/bin/env python3
python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Duplicate Detection System (ATLAS/CRONOS)
=========================================================

This script identifies duplicate or potentially redundant files
in the EVA & GUARANI system, allowing for consolidation and optimization
of the structure with ethical preservation of information.

Author: EVA & GUARANI
Version: 1.0
"""

import os
import sys
import hashlib
import json
import argparse
import datetime
import re
from collections import defaultdict
from pathlib import Path

class DuplicateDetector:
    """
    Duplicate detector with ethical awareness
    Implements methods to identify redundancies in the EVA & GUARANI system
    """
    
    def __init__(self, exclude_dirs=None, exclude_exts=None, report_dir='./reports'):
        """
        Initializes the detector with settings
        
        Args:
            exclude_dirs (list): Directories to exclude from analysis
            exclude_exts (list): Extensions to exclude from analysis
            report_dir (str): Directory for reports
        """
        self.exclude_dirs = exclude_dirs or [
            '.git', '.github', '.vscode', '.obsidian', '.cursor',
            'venv', '__pycache__', 'node_modules', 'backup', 'logs'
        ]
        
        self.exclude_exts = exclude_exts or [
            '.pyc', '.pyo', '.o', '.obj', '.exe', '.dll', '.so', '.dylib',
            '.zip', '.tar', '.gz', '.rar', '.7z', '.pdf'
        ]
        
        self.report_dir = report_dir
        os.makedirs(self.report_dir, exist_ok=True)
        
        # Structures for analysis
        self.files_by_name = defaultdict(list)
        self.files_by_size = defaultdict(list)
        self.files_by_hash = defaultdict(list)
        self.potential_duplicates = []
        self.exact_duplicates = []
        self.similar_files = []
    
    def log(self, message):
        """
        Logs message with timestamp
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def analyze_directory(self, root_path='.'):
        """
        Analyzes directory recursively identifying possible duplicates
        
        Args:
            root_path (str): Root path for analysis
        """
        self.log(f"Starting duplicate analysis in: {os.path.abspath(root_path)}")
        self.root_path = os.path.abspath(root_path)
        
        # Statistics
        total_files = 0
        processed_files = 0
        skipped_dirs = 0
        
        # Traverse file system
        for root, dirs, files in os.walk(root_path):
            # Filter excluded directories
            filtered_dirs = []
            for d in dirs:
                if d in self.exclude_dirs or d.startswith('.'):
                    skipped_dirs += 1
                else:
                    filtered_dirs.append(d)
            
            # Update directory list in-place
            dirs[:] = filtered_dirs
            
            for file in files:
                total_files += 1
                
                # Check extension
                _, ext = os.path.splitext(file)
                if ext.lower() in self.exclude_exts:
                    continue
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.root_path)
                
                try:
                    # Get file statistics
                    file_size = os.path.getsize(file_path)
                    
                    # Skip empty files
                    if file_size == 0:
                        continue
                    
                    # Register file by name (for potential duplicates)
                    self.files_by_name[file].append({
                        'path': rel_path,
                        'size': file_size,
                        'absolute_path': file_path
                    })
                    
                    # Register file by size (for in-depth analysis)
                    self.files_by_size[file_size].append({
                        'path': rel_path,
                        'name': file,
                        'absolute_path': file_path
                    })
                    
                    processed_files += 1
                    
                    # Progress feedback every 1000 files
                    if processed_files % 1000 == 0:
                        self.log(f"Processed {processed_files} files...")
                    
                except Exception as e:
                    self.log(f"Error processing '{rel_path}': {e}")
        
        self.log(f"Initial analysis completed: {processed_files} files processed, {skipped_dirs} directories skipped")
        
        # Identify potential duplicates based on name
        self._identify_name_duplicates()
        
        # Identify duplicates based on size
        self._identify_size_duplicates()
        
        # Identify exact duplicates using hash
        self._identify_exact_duplicates()
        
        # Identify similar files
        self._identify_similar_files()
        
        return {
            'total_files': total_files,
            'processed_files': processed_files,
            'skipped_dirs': skipped_dirs,
            'potential_duplicates': len(self.potential_duplicates),
            'exact_duplicates': len(self.exact_duplicates),
            'similar_files': len(self.similar_files)
        }
    
    def _identify_name_duplicates(self):
        """
        Identifies files with identical names
        """
        self.log("Identifying files with identical names...")
        
        for name, files in self.files_by_name.items():
            if len(files) > 1:
                self.potential_duplicates.append({
                    'name': name,
                    'count': len(files),
                    'files': files
                })
        
        # Sort by count (most duplicates first)
        self.potential_duplicates.sort(key=lambda x: x['count'], reverse=True)
        
        self.log(f"Identified {len(self.potential_duplicates)} groups of files with identical names")
    
    def _identify_size_duplicates(self):
        """
        Identifies files with identical sizes
        """
        self.log("Identifying files with identical sizes...")
        
        size_duplicates = []
        for size, files in self.files_by_size.items():
            if len(files) > 1:
                size_duplicates.append({
                    'size': size,
                    'count': len(files),
                    'files': files
                })
        
        self.log(f"Identified {len(size_duplicates)} groups of files with identical sizes")
        
        # We don't store all duplicates by size, just use them to
        # identify hash candidates
    
    def _calculate_file_hash(self, file_path, block_size=65536):
        """
        Calculates SHA-256 hash of a file
        
        Args:
            file_path (str): File path
            block_size (int): Block size for reading
            
        Returns:
            str: SHA-256 hash of the file
        """
        try:
            hasher = hashlib.sha256()
            
            with open(file_path, 'rb') as f:
                buf = f.read(block_size)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(block_size)
            
            return hasher.hexdigest()
        except Exception as e:
            self.log(f"Error calculating hash for '{file_path}': {e}")
            return None
    
    def _identify_exact_duplicates(self):
        """
        Identifies exactly duplicated files using SHA-256 hash
        """
        self.log("Identifying exact duplicates with SHA-256 hash...")
        
        # Only calculate hash for files with the same size
        hash_candidates = 0
        
        for size, files in self.files_by_size.items():
            if len(files) > 1:
                # Only need to calculate hash if there is more than one file with the same size
                for file_info in files:
                    file_hash = self._calculate_file_hash(file_info['absolute_path'])
                    
                    if file_hash:
                        # Add hash to record
                        file_info['hash'] = file_hash
                        
                        # Group by hash
                        self.files_by_hash[file_hash].append(file_info)
                        
                        hash_candidates += 1
                        
                        # Progress feedback every 100 hashes
                        if hash_candidates % 100 == 0:
                            self.log(f"Calculated {hash_candidates} hashes...")
        
        # Identify exact duplicates
        for hash_value, files in self.files_by_hash.items():
            if len(files) > 1:
                # Check if the first file has the 'size' key, otherwise use a default value
                file_size = files[0].get('size', 0)
                
                self.exact_duplicates.append({
                    'hash': hash_value,
                    'count': len(files),
                    'size': file_size,
                    'files': files
                })
        
        # Sort by size (largest files first)
        self.exact_duplicates.sort(key=lambda x: x['size'], reverse=True)
        
        self.log(f"Identified {len(self.exact_duplicates)} groups of exactly duplicated files")
    
    def _identify_similar_files(self):
        """
        Identifies potentially similar files by name patterns
        """
        self.log("Identifying similar files by name pattern...")
        
        # Common patterns in similar files
        patterns = {
            'backup': r'(backup|bkp|old|copy|copia|\.bak|\(\d+\)|_\d+)$',
            'version': r'(v\d+|version|versao|\d+\.\d+\.\d+)',
            'temp': r'(temp|tmp|temp_)',
            'draft': r'(draft|rascunho|_draft)',
            'auto': r'(auto\-save|autosave)',
            'untitled': r'(untitled|new|novo|sem_titulo)'
        }
        
        # Group files by name root
        name_roots = defaultdict(list)
        
        for name, files in self.files_by_name.items():
            # Remove extension
            file_base = os.path.splitext(name)[0]
            
            # Remove common suffixes
            clean_name = file_base
            for pattern_name, pattern in patterns.items():
                clean_name = re.sub(pattern, '', clean_name, flags=re.IGNORECASE)
            
            # If it has at least 5 characters and is not all numeric
            if len(clean_name) >= 5 and not clean_name.isdigit():
                # Use the first 5+ characters as "root"
                name_root = clean_name[:min(8, len(clean_name))]
                
                for file_info in files:
                    name_roots[name_root].append({
                        'original_name': name,
                        'root': name_root,
                        'path': file_info['path'],
                        'size': file_info['size']
                    })
        
        # Identify groups with similar names
        for root, files in name_roots.items():
            if len(files) > 1:
                # Check if there are really different names in the group
                unique_names = {f['original_name'] for f in files}
                
                if len(unique_names) > 1:
                    self.similar_files.append({
                        'root': root,
                        'count': len(files),
                        'files': files
                    })
        
        # Sort by count (most similar first)
        self.similar_files.sort(key=lambda x: x['count'], reverse=True)
        
        self.log(f"Identified {len(self.similar_files)} groups of potentially similar files")
    
    def generate_report(self):
        """
        Generates a complete analysis report
        
        Returns:
            str: Report file path
        """
        self.log("Generating duplicate report...")
        
        # Prepare report data
        report_data = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'root_path': self.root_path,
            'statistics': {
                'total_files_by_name': len(self.files_by_name),
                'total_files_by_size': len(self.files_by_size),
                'unique_sizes': len(self.files_by_size),
                'name_duplicates': len(self.potential_duplicates),
                'exact_duplicates': len(self.exact_duplicates),
                'similar_files': len(self.similar_files)
            },
            'potential_duplicates': self.potential_duplicates[:100],  # Limit to the first 100
            'exact_duplicates': self.exact_duplicates[:50],  # Limit to the first 50
            'similar_files': self.similar_files[:50]  # Limit to the first 50
        }
        
        # Calculate space statistics
        space_saved = 0
        for dup in self.exact_duplicates:
            # Each group has 'count' files with the same hash
            # We can save (count - 1) * size
            space_saved += (dup['count'] - 1) * dup['size']
        
        report_data['statistics']['potential_space_saved'] = space_saved
        report_data['statistics']['potential_space_saved_mb'] = round(space_saved / (1024 * 1024), 2)
        
        # Save JSON report
        report_file = os.path.join(
            self.report_dir, 
            f"duplicate_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # Generate Markdown report
        md_report = self._generate_markdown_report(report_data)
        md_report_file = os.path.join(
            self.report_dir, 
            f"duplicate_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        with open(md_report_file, 'w', encoding='utf-8') as f:
            f.write(md_report)
        
        self.log(f"JSON report saved in: {report_file}")
        self.log(f"Markdown report saved in: {md_report_file}")
        
        return md_report_file
    
    def _generate_markdown_report(self, report_data):
        """
        Generates report in Markdown format
        
        Args:
            report_data (dict): Report data
            
        Returns:
            str: Markdown report content
        """
        md = f"""# EVA & GUARANI Duplicate Analysis
*Generated on: {report_data['timestamp']}*

## 📊 General Statistics

- **Root Directory:** `{report_data['root_path']}`
- **Total Files Analyzed:** {report_data['statistics']['total_files_by_name']}
- **Groups of Files with Same Name:** {report_data['statistics']['name_duplicates']}
- **Groups of Exactly Duplicated Files:** {report_data['statistics']['exact_duplicates']}
- **Groups of Potentially Similar Files:** {report_data['statistics']['similar_files']}
- **Potential Space to Save:** {report_data['statistics']['potential_space_saved_mb']} MB

## 🧩 Exact Duplicates

Found {report_data['statistics']['exact_duplicates']} groups of exactly identical files.
These files have the same content (confirmed by SHA-256 hash).

| Hash (partial) | Quantity | Size | Redundant Space |
|----------------|----------|------|-----------------|
"""
        
        # Add exact duplicates
        for i, dup in enumerate(report_data['exact_duplicates'][:10]):  # Show only 10
            hash_partial = dup['hash'][:8] + "..."
            size_kb = round(dup['size'] / 1024, 2)
            redundant_mb = round((dup['count'] - 1) * dup['size'] / (1024 * 1024), 2)
            md += f"| {hash_partial} | {dup['count']} | {size_kb} KB | {redundant_mb} MB |\n"
        
        if len(report_data['exact_duplicates']) > 10:
            md += f"| ... | ... | ... | ... |\n"
        
        # Add files with identical names
        md += f"""
## 📄 Files with Identical Names

Found {report_data['statistics']['name_duplicates']} groups of files with identical names,
possibly in different directories.

| File Name | Occurrences |
|-----------|-------------|
"""
        
        for i, dup in enumerate(report_data['potential_duplicates'][:10]):  # Show only 10
            md += f"| `{dup['name']}` | {dup['count']} |\n"
        
        if len(report_data['potential_duplicates']) > 10:
            md += f"| ... | ... |\n"
        
        # Add similar files
        md += f"""
## 📋 Potentially Similar Files

Found {report_data['statistics']['similar_files']} groups of files with similar names,
which may have related contents or different versions of the same file.

| Name Root | Quantity | Examples |
|-----------|----------|----------|
"""
        
        for i, sim in enumerate(report_data['similar_files'][:10]):  # Show only 10
            example_files = [f"`{f['original_name']}`" for f in sim['files'][:2]]
            examples = ", ".join(example_files)
            if len(sim['files']) > 2:
                examples += ", ..."
            
            md += f"| {sim['root']} | {sim['count']} | {examples} |\n"
        
        if len(report_data['similar_files']) > 10:
            md += f"| ... | ... | ... |\n"
        
        # Recommendations
        md += """
## 🚀 Recommendations for Cleanup

1. **Consolidate exact duplicates:**
   - Keep only one copy of each exactly duplicated file
   - Consider moving other copies to quarantine before permanently removing them

2. **Review files with the same name:**
   - Files with the same name in different locations may indicate duplication of function
   - Check if they can be consolidated or if one is obsolete

3. **Analyze similar files:**
   - Files with similar names may be different versions of the same content
   - Identify the most recent version and consider archiving the previous ones

4. **Implement naming convention:**
   - Adopt consistent standards to avoid future duplications
   - Use version control for important files instead of multiple copies

## 📝 Next Steps

1. Review the groups of exact duplicates, starting with the largest files
2. Move redundant files to quarantine using the script `move_to_quarantine.py`
3. Consolidate similar files after manual analysis
4. Implement a strategy to prevent future duplications

---

*Analysis conducted with love and awareness by the EVA & GUARANI system 🌌*

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""
        
        return md


def parse_arguments():
    """
    Processes command line arguments
    
    Returns:
        argparse.Namespace: Processed arguments
    """
    parser = argparse.ArgumentParser(description='EVA & GUARANI - Duplicate Detection System')
    
    parser.add_argument('--dir', type=str, default='.',
                        help='Root directory for analysis (default: current directory)')
    
    parser.add_argument('--exclude-dirs', type=str, 
                        default='.git,.github,.vscode,__pycache__,node_modules,quarantine,backup,logs',
                        help='Comma-separated list of directories to ignore')
    
    parser.add_argument('--exclude-exts', type=str,
                        default='.pyc,.pyo,.exe,.dll,.obj,.o',
                        help