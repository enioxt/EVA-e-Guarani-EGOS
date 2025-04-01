#!/usr/bin/env python3
python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Structural Analysis and Optimization System (ATLAS/CRONOS)
=========================================================================

This script implements a deep analysis of the EVA & GUARANI system,
identifying obsolete components, analyzing usage, and suggesting organizational improvements
with evolutionary preservation.

Author: EVA & GUARANI
Version: 1.0
"""

import os
import sys
import time
import datetime
import shutil
import json
import re
from pathlib import Path
from collections import defaultdict, Counter

class SystemAnalyzer:
    """
    System Analyzer with ethical and evolutionary awareness
    Implements methods to analyze, preserve, and optimize the EVA & GUARANI system
    """
    
    def __init__(self, root_path='.', quarantine_path='./quarantine', report_path='./system_analysis'):
        """
        Initializes the analyzer with paths and settings
        
        Args:
            root_path (str): Root path of the EVA & GUARANI system
            quarantine_path (str): Path to quarantine directory
            report_path (str): Path to store analysis reports
        """
        self.root_path = os.path.abspath(root_path)
        self.quarantine_path = os.path.abspath(quarantine_path)
        self.report_path = os.path.abspath(report_path)
        
        # Analysis settings
        self.days_threshold = 90  # Files not modified for this period may be obsolete
        
        # Directories to be ignored in the analysis
        self.ignore_dirs = [
            '.git', '.github', '.obsidian', '.vscode', '.cursor', 'venv',
            '__pycache__', 'node_modules', 'quarantine', 'quarentena',
            'backup', 'backups', 'archived_files', 'logs'
        ]
        
        # Structure to store analysis results
        self.old_files = []
        self.duplicate_files = []
        self.system_structure = defaultdict(list)
        self.file_stats = defaultdict(int)
        self.subsystems = defaultdict(list)
        
        # Ensure output directories exist
        os.makedirs(self.quarantine_path, exist_ok=True)
        os.makedirs(self.report_path, exist_ok=True)
        
        # Execution log
        self.log = []
        self.log_event('System analyzer initialization with love and awareness')
    
    def log_event(self, message, level='INFO'):
        """
        Logs event with timestamp
        
        Args:
            message (str): Message to be logged
            level (str): Log level (INFO, WARNING, ERROR)
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}][{level}] {message}"
        print(log_entry)
        self.log.append(log_entry)
    
    def analyze_system(self):
        """
        Performs a complete system analysis
        """
        self.log_event("Starting systemic analysis of EVA & GUARANI")
        
        # Step 1: Map the system structure
        self._map_system_structure()
        
        # Step 2: Identify old files
        self._identify_old_files()
        
        # Step 3: Find duplicates
        self._identify_duplicate_files()
        
        # Step 4: Group by subsystems
        self._identify_subsystems()
        
        # Step 5: Generate statistics
        self._generate_statistics()
        
        # Step 6: Generate report
        self._generate_report()
        
        self.log_event("Systemic analysis completed with love and awareness")
        return True
    
    def _map_system_structure(self):
        """
        Maps the complete system structure
        """
        self.log_event("Mapping system structure")
        
        for root, dirs, files in os.walk(self.root_path):
            # Filter ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs and not d.startswith('.')]
            
            # Relative path
            rel_path = os.path.relpath(root, self.root_path)
            
            # Register files
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Register by extension
                self.system_structure[file_ext].append(file_path)
                
                # Statistics
                self.file_stats['total'] += 1
                self.file_stats[file_ext] += 1
        
        self.log_event(f"System structure mapped: {self.file_stats['total']} files found")
    
    def _identify_old_files(self):
        """
        Identifies files that have not been modified for a long period
        """
        self.log_event(f"Identifying files not modified for more than {self.days_threshold} days")
        threshold_date = time.time() - (self.days_threshold * 24 * 60 * 60)
        
        for ext, files in self.system_structure.items():
            for file_path in files:
                try:
                    # Check modification date
                    mod_time = os.path.getmtime(file_path)
                    if mod_time < threshold_date:
                        rel_path = os.path.relpath(file_path, self.root_path)
                        mod_date = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
                        self.old_files.append({
                            'path': rel_path,
                            'last_modified': mod_date,
                            'type': ext,
                            'age_days': int((time.time() - mod_time) / (24 * 60 * 60))
                        })
                except Exception as e:
                    self.log_event(f"Error checking {file_path}: {e}", 'ERROR')
        
        # Sort by date (oldest first)
        self.old_files.sort(key=lambda x: x['age_days'], reverse=True)
        self.log_event(f"Identified {len(self.old_files)} potentially obsolete files")
    
    def _identify_duplicate_files(self):
        """
        Identifies potential duplicate files by name
        """
        self.log_event("Identifying possible duplicate files")
        
        # Group by file name
        files_by_name = defaultdict(list)
        
        for ext, files in self.system_structure.items():
            for file_path in files:
                file_name = os.path.basename(file_path)
                files_by_name[file_name].append(file_path)
        
        # Identify duplicates
        for name, paths in files_by_name.items():
            if len(paths) > 1:
                self.duplicate_files.append({
                    'name': name,
                    'count': len(paths),
                    'paths': [os.path.relpath(p, self.root_path) for p in paths]
                })
        
        # Sort by number of duplicates
        self.duplicate_files.sort(key=lambda x: x['count'], reverse=True)
        self.log_event(f"Identified {len(self.duplicate_files)} groups of possible duplicate files")
    
    def _identify_subsystems(self):
        """
        Identifies and classifies subsystems of EVA & GUARANI
        """
        self.log_event("Classifying files by subsystems")
        
        # Patterns to identify subsystems
        subsystem_patterns = {
            'ATLAS': r'atlas|cartogra|map|visualiza|dependenc',
            'NEXUS': r'nexus|modular|analy[sz]|component',
            'CRONOS': r'cronos|backup|preserva|versio|histor',
            'EGOS': r'egos|core|essenc|unified',
            'BOT': r'bot|telegram|chat|messag',
            'QUANTUM': r'quantum|prompts?|knowledge|essence',
            'ETHIK': r'ethik|etic|ethic|moral',
            'ELIZA': r'eliza|conversation|dialog',
            'PAYMENT': r'pay|finance|monetiz|subscript',
            'BLOCKCHAIN': r'blockchain|smart.?contract|web3',
            'MEDIA': r'image|video|media|dalle|midjourney'
        }
        
        # Classify files
        for ext, files in self.system_structure.items():
            for file_path in files:
                rel_path = os.path.relpath(file_path, self.root_path)
                file_name = os.path.basename(file_path)
                
                # Check content of text files for more accurate classification
                content = ""
                if ext.lower() in ['.py', '.js', '.md', '.txt', '.json', '.html', '.bat', '.ps1', '.sh']:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read(5000)  # Read first 5000 characters
                    except Exception as e:
                        self.log_event(f"Could not read {file_path}: {e}", 'WARNING')
                
                # Combine name and content for analysis
                text_to_analyze = f"{rel_path} {file_name} {content}".lower()
                
                # Classify by subsystem
                classified = False
                for subsystem, pattern in subsystem_patterns.items():
                    if re.search(pattern, text_to_analyze, re.IGNORECASE):
                        self.subsystems[subsystem].append(rel_path)
                        classified = True
                        break
                
                # If not classified, add to "Others"
                if not classified:
                    self.subsystems['OTHERS'].append(rel_path)
        
        # Subsystem statistics
        subsystem_counts = {name: len(files) for name, files in self.subsystems.items()}
        self.log_event(f"Classification by subsystems completed: {subsystem_counts}")
    
    def _generate_statistics(self):
        """
        Generates additional system statistics
        """
        self.log_event("Generating system statistics")
        
        # Statistics by file type
        self.file_stats['by_extension'] = dict(self.file_stats)
        
        # Statistics by directory
        dir_counts = Counter()
        for ext, files in self.system_structure.items():
            for file_path in files:
                dir_path = os.path.dirname(os.path.relpath(file_path, self.root_path))
                if dir_path == '':
                    dir_path = '.'
                dir_counts[dir_path] += 1
        
        self.file_stats['by_directory'] = dir_counts
        
        # Subsystem statistics
        self.file_stats['by_subsystem'] = {name: len(files) for name, files in self.subsystems.items()}
        
        # Age statistics
        if self.old_files:
            age_counts = Counter()
            for file in self.old_files:
                age_range = f"{(file['age_days'] // 30) * 30}-{((file['age_days'] // 30) + 1) * 30} days"
                age_counts[age_range] += 1
            
            self.file_stats['by_age'] = dict(age_counts)
        
        self.log_event("System statistics generated successfully")
    
    def _generate_report(self):
        """
        Generates a complete system analysis report
        """
        self.log_event("Generating systemic analysis report")
        
        report = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'system_name': 'EVA & GUARANI',
            'analysis_version': '1.0',
            'root_path': self.root_path,
            'statistics': self.file_stats,
            'old_files': self.old_files[:100],  # Limit to the oldest 100
            'duplicate_files': self.duplicate_files[:50],  # Limit to the top 50 groups with most duplicates
            'subsystems': {name: len(files) for name, files in self.subsystems.items()},
            'recommendations': self._generate_recommendations()
        }
        
        # Save report as JSON
        report_file = os.path.join(self.report_path, f"system_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Generate text report
        text_report = self._generate_text_report(report)
        text_report_file = os.path.join(self.report_path, f"system_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write(text_report)
        
        self.log_event(f"Analysis report generated: {report_file}")
        self.log_event(f"Text report generated: {text_report_file}")
        
        return report_file, text_report_file
    
    def _generate_recommendations(self):
        """
        Generates recommendations based on system analysis
        """
        recommendations = []
        
        # Recommendations for old files
        if len(self.old_files) > 0:
            old_files_count = len(self.old_files)
            very_old_files = sum(1 for f in self.old_files if f['age_days'] > 180)
            
            recommendations.append({
                'type': 'quarantine',
                'title': f'Quarantine of {very_old_files} very old files',
                'description': f'There are {very_old_files} files not modified for more than 180 days. '
                              f'Consider moving them to quarantine to simplify the system.',
                'impact': 'Medium',
                'files_affected': very_old_files
            })
        
        # Recommendations for duplicates
        if len(self.duplicate_files) > 0:
            dup_count = sum(item['count'] for item in self.duplicate_files)
            
            recommendations.append({
                'type': 'consolidation',
                'title': f'Consolidation of up to {dup_count} possible duplicates',
                'description': f'There are {len(self.duplicate_files)} groups of files with identical names '
                              f'that may be duplicates. Consider reviewing and consolidating.',
                'impact': 'High',
                'files_affected': dup_count
            })
        
        # Recommendation for organization by subsystems
        if 'OTHERS' in self.subsystems and len(self.subsystems['OTHERS']) > 50:
            recommendations.append({
                'type': 'reorganization',
                'title': 'Structural reorganization by subsystems',
                'description': f'There are {len(self.subsystems["OTHERS"])} files not classified into subsystems. '
                              f'Consider reorganizing the structure into well-defined folders by subsystem.',
                'impact': 'High',
                'files_affected': len(self.subsystems['OTHERS'])
            })
        
        # Recommendations for documentation
        if '.md' in self.system_structure and len(self.system_structure['.md']) < 10:
            recommendations.append({
                'type': 'documentation',
                'title': 'Documentation improvement',
                'description': 'The system has few Markdown documentation files. '
                              'Consider improving documentation by subsystem.',
                'impact': 'Medium',
                'files_affected': 0
            })
        
        return recommendations
    
    def _generate_text_report(self, report_data):
        """
        Generates a report in Markdown format
        """
        text = f"""# EVA & GUARANI Systemic Analysis
*Generated on: {report_data['timestamp']}*

## 📊 General Statistics

- **Total Files:** {report_data['statistics']['total']}
- **Root Directory:** `{report_data['root_path']}`

## 🧩 Distribution by Subsystems

| Subsystem | Number of Files |
|-----------|-----------------|
"""
        
        # Add subsystems
        for subsystem, count in sorted(report_data['subsystems'].items(), key=lambda x: x[1], reverse=True):
            text += f"| {subsystem} | {count} |\n"
        
        # Obsolete files
        text += f"""
## ⏱️ Potentially Obsolete Files

Total: {len(self.old_files)} files not modified for more than {self.days_threshold} days.

| Path | Last Modified | Age (days) |
|------|---------------|------------|
"""
        
        for file in self.old_files[:20]:  # Show only the oldest 20
            text += f"| `{file['path']}` | {file['last_modified']} | {file['age_days']} |\n"
        
        # Duplicate files
        text += f"""
## 🔄 Possible Duplicates

Total: {len(self.duplicate_files)} groups of possible duplicates.

| File Name | Occurrences | 
|-----------|-------------|
"""
        
        for dup in self.duplicate_files[:10]:  # Show only the top 10 groups
            text += f"| `{dup['name']}` | {dup['count']} |\n"
        
        # Recommendations
        text += """
## 🚀 Recommendations

"""
        
        for i, rec in enumerate(report_data['recommendations'], 1):
            text += f"### {i}. {rec['title']}\n\n"
            text += f"{rec['description']}\n\n"
            text += f"**Impact:** {rec['impact']}\n"
            text += f"**Files affected:** {rec['files_affected']}\n\n"
        
        # Conclusion
        text += """
## 🔍 Recommended Next Steps

1. **Review obsolete files** - Review and move identified very old files to quarantine
2. **Consolidate duplicates** - Identify and resolve unnecessary duplications
3. **Reorganize by subsystems** - Apply a clearer structure based on identified subsystems
4. **Documentation** - Improve documentation, especially for key subsystems
5. **Standardization** - Implement consistent naming and organizational standards

---

*Analysis conducted with love and awareness by the EVA & GUARANI system 🌌*

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""
        
        return text
    
    def move_to_quarantine(self, file_list, dry_run=True):
        """
        Moves files to quarantine
        
        Args:
            file_list (list): List of relative paths of files to be moved
            dry_run (bool): If True, only simulates the operation without actually moving
        
        Returns:
            dict: Operation report
        """
        self.log_event(f"{'Simulating' if dry_run else 'Executing'} move to quarantine: {len(file_list)} files")
        
        results = {
            'success': [],
            'failed': [],
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        for rel_path in file_list:
            src_path = os.path.join(self.root_path, rel_path)
            
            # Create similar structure in quarantine
            dest_dir = os.path.join(self.quarantine_path, os.path.dirname(rel_path))
            dest_path = os.path.join(self.quarantine_path, rel_path)
            
            try:
                # Validate source
                if not os.path.exists(src_path):
                    raise FileNotFoundError(f"File not found: {src_path}")
                
                if not dry_run:
                    # Create destination directory if it doesn't exist
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Move file
                    shutil.move(src_path, dest_path)
                
                #