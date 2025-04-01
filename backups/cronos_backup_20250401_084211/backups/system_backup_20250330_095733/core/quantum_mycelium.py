#!/usr/bin/env python3
"""
# ========================================================================
# QUANTUM MYCELIUM - EVA & GUARANI CONNECTION ANALYSIS SYSTEM
# ========================================================================
#
# VERSION: 1.0.0 "Pear" - Mycelial Analysis and Systemic Integrity
#
# WHAT IS THIS SYSTEM?
# ---------------------
# This system performs a deep analysis of the EVA & GUARANI project,
# identifying:
# - Duplicate or obsolete files (to move to quarantine)
# - Loose ends that need to be interconnected
# - Important content in obsolete files (to preserve)
# - Missing mycelial connections between system components
#
# BASED ON THE MYCELIUM PRINCIPLE:
# ---------------------------------
# Just as fungal networks in nature connect different parts
# of an ecosystem, this system seeks to ensure that all components
# of EVA & GUARANI are properly interconnected.
#
# ========================================================================
"""

import os
import sys
import json
import re
import hashlib
import shutil
import datetime
import difflib
from pathlib import Path
from collections import defaultdict, Counter

# Import the Quantum Changelog system for integration
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.quantum_changelog import QuantumChangelog, QUANTUM_SIGNATURE

# ========================================================================
# CONFIGURATION
# ========================================================================

# Main directories
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUARANTINE_DIR = os.path.join(PROJECT_ROOT, "quarantine")
STAGING_DIR = os.path.join(PROJECT_ROOT, "staging")
MYCELIUM_REPORT_FILE = os.path.join(STAGING_DIR, "mycelium_analysis.md")
MYCELIUM_JSON_FILE = os.path.join(STAGING_DIR, "mycelium_data.json")

# Analysis configurations
MIN_DUPLICATE_SIMILARITY = 0.85  # Minimum similarity to consider duplication
MIN_CONNECTION_SCORE = 0.6  # Minimum score to consider connection
MAX_FILES_TO_ANALYZE = 1000  # Limit of files for deep analysis
IGNORE_DIRS = ['.git', '.vscode', '__pycache__', 'venv', 'node_modules', 'quarantine']
IGNORE_FILES = ['.gitignore', '.DS_Store', 'Thumbs.db']
IMPORTANT_EXTENSIONS = ['.py', '.md', '.js', '.html', '.json', '.yaml', '.yml', '.txt']

# Patterns to identify references to other files
FILE_REFERENCE_PATTERNS = [
    r'import\s+(\w+(?:\.\w+)*)',  # Python imports
    r'from\s+(\w+(?:\.\w+)*)\s+import',  # Python from imports
    r'require\([\'"](.+?)[\'"]\)',  # JS requires
    r'import\s+.+?from\s+[\'"](.+?)[\'"]',  # JS imports
    r'include\([\'"](.+?)[\'"]\)',  # PHP includes
    r'\[.*?\]\((.*?)\)',  # Markdown links
    r'<a\s+href=[\'"](.+?)[\'"]',  # HTML links
    r'src=[\'"](.+?)[\'"]',  # HTML/JS src
    r'href=[\'"](.+?)[\'"]',  # HTML href
    r'EVA & GUARANI',  # Project name references
    r'BIOS-Q',  # References to BIOS-Q
    r'QUANTUM_PROMPTS',  # References to quantum prompts
    r'Quantum',  # General quantum references
    r'EGOS'  # References to EGOS
]

# ========================================================================
# MAIN CLASS: QUANTUM MYCELIUM
# ========================================================================

class QuantumMycelium:
    """
    Deep analysis system of the EVA & GUARANI project's mycelial structure.
    
    This system maps connections between files, identifies duplicates,
    obsolescence and loose ends, suggesting improvements and corrections.
    """
    
    def __init__(self):
        """Initializes the Quantum Mycelium system"""
        self.project_root = PROJECT_ROOT
        self.files = []
        self.file_hashes = {}  # {hash: path}
        self.file_contents = {}  # {path: content}
        self.file_metadata = {}  # {path: metadata}
        self.file_references = defaultdict(set)  # {path: {referenced files}}
        self.reference_graph = defaultdict(set)  # {path: {files referencing it}}
        self.disconnected_files = []  # Files without connections
        self.potentially_obsolete = []  # Potentially obsolete files
        self.duplicates = []  # Groups of duplicate files
        self.orphans = []  # Files that exist but are not referenced
        
        # Initialize directories
        os.makedirs(QUARANTINE_DIR, exist_ok=True)
        os.makedirs(STAGING_DIR, exist_ok=True)
        
        # Initialize changelog for action recording
        self.changelog = QuantumChangelog()
        
        print(f"\n{QUANTUM_SIGNATURE}")
        print("QUANTUM MYCELIUM - Mycelial Analysis and Systemic Integrity")
        print(f"Started on: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Project directory: {self.project_root}")
        print(f"Quarantine: {QUARANTINE_DIR}")
        print(f"Staging: {STAGING_DIR}\n")
    
    def scan_project(self):
        """Scans the entire project to gather information about the files"""
        print("🔍 Scanning the project for files...")
        
        for root, dirs, files in os.walk(self.project_root):
            # Ignore specific directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file in IGNORE_FILES:
                    continue
                    
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.project_root)
                
                # Check if it's a binary file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        is_binary = False
                except UnicodeDecodeError:
                    is_binary = True
                    content = ""
                except Exception as e:
                    print(f"⚠️ Error reading file {rel_path}: {str(e)}")
                    continue
                
                # Skip binary files for detailed analysis
                if is_binary:
                    self.file_metadata[rel_path] = {
                        'size': os.path.getsize(file_path),
                        'modified': os.path.getmtime(file_path),
                        'is_binary': True,
                        'extension': os.path.splitext(file)[1].lower(),
                    }
                    self.files.append(rel_path)
                    continue
                
                # Calculate file hash
                file_hash = hashlib.md5(content.encode()).hexdigest()
                
                # Store file information
                self.files.append(rel_path)
                self.file_hashes[file_hash] = rel_path
                self.file_contents[rel_path] = content
                self.file_metadata[rel_path] = {
                    'size': os.path.getsize(file_path),
                    'modified': os.path.getmtime(file_path),
                    'is_binary': False,
                    'hash': file_hash,
                    'extension': os.path.splitext(file)[1].lower(),
                    'lines': len(content.split('\n')),
                }
        
        print(f"✅ Found {len(self.files)} files for analysis.")
        
        # Limit deep analysis to avoid overload
        if len(self.files) > MAX_FILES_TO_ANALYZE:
            print(f"⚠️ Limiting deep analysis to {MAX_FILES_TO_ANALYZE} files to avoid overload.")
            
            # Prioritize important files
            self.files.sort(key=lambda f: 
                           (self.file_metadata[f]['extension'] in IMPORTANT_EXTENSIONS, 
                            not self.file_metadata[f]['is_binary'],
                            self.file_metadata[f]['size']), 
                           reverse=True)
            self.files = self.files[:MAX_FILES_TO_ANALYZE]
    
    def analyze_connections(self):
        """Analyzes connections between files in the project"""
        print("\n🔄 Analyzing connections between files...")
        
        # Analyze each file in search of references to other files
        for file_path in self.files:
            if self.file_metadata[file_path]['is_binary']:
                continue
                
            content = self.file_contents[file_path]
            
            # Search for references to other files
            for pattern in FILE_REFERENCE_PATTERNS:
                matches = re.finditer(pattern, content)
                for match in matches:
                    reference = match.group(1) if '(' in pattern else match.group(0)
                    reference_clean = reference.strip().replace('./', '').replace('../', '')
                    
                    # Add found references
                    self.file_references[file_path].add((reference_clean, pattern))
                    
                    # Try to find the referenced file
                    potential_matches = [f for f in self.files if reference_clean in f]
                    for potential in potential_matches:
                        self.reference_graph[potential].add(file_path)
        
        # Find disconnected files
        self.disconnected_files = [f for f in self.files 
                                if len(self.file_references[f]) == 0 and 
                                len(self.reference_graph[f]) == 0]
        
        # Find orphan files (not referenced)
        self.orphans = [f for f in self.files if len(self.reference_graph[f]) == 0]
        
        print(f"✅ Connection analysis completed.")
        print(f"📊 Statistics:")
        print(f"   - {len(self.disconnected_files)} files without connections")
        print(f"   - {len(self.orphans)} orphan files (not referenced)")
    
    def find_duplicates(self):
        """Identifies duplicate files in the project"""
        print("\n🔍 Searching for duplicate files...")
        
        # Group files by hash to find exact duplicates
        hash_groups = defaultdict(list)
        for file_path in self.files:
            if not self.file_metadata[file_path]['is_binary']:
                file_hash = self.file_metadata[file_path]['hash']
                hash_groups[file_hash].append(file_path)
        
        exact_duplicates = [files for files in hash_groups.values() if len(files) > 1]
        
        # Check similarity to find almost identical duplicates
        similar_duplicates = []
        already_checked = set()
        
        files_to_check = [f for f in self.files 
                        if not self.file_metadata[f]['is_binary'] and 
                        self.file_metadata[f]['extension'] in IMPORTANT_EXTENSIONS]
        
        # Limit check to avoid excessive processing
        if len(files_to_check) > 100:
            files_to_check = sorted(files_to_check, 
                                  key=lambda f: self.file_metadata[f]['size'])[:100]
        
        for i, file1 in enumerate(files_to_check):
            for file2 in files_to_check[i+1:]:
                if (file1, file2) in already_checked:
                    continue
                    
                # Check similar size
                size1 = self.file_metadata[file1]['size']
                size2 = self.file_metadata[file2]['size']
                
                # Prevent division by zero if both files are empty
                if size1 == 0 and size2 == 0:
                    # Both files are empty, consider them similar
                    similarity = 1.0
                elif max(size1, size2) == 0:
                    # One file is empty, the other isn't - they're different
                    continue
                elif abs(size1 - size2) / max(size1, size2) > 0.3:  # Size difference > 30%
                    continue
                else:
                    # Calculate similarity
                    content1 = self.file_contents[file1]
                    content2 = self.file_contents[file2]
                    similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
                
                if similarity >= MIN_DUPLICATE_SIMILARITY:
                    # Check if already part of an existing group
                    found_group = False
                    for group in similar_duplicates:
                        if file1 in group or file2 in group:
                            if file1 not in group:
                                group.append(file1)
                            if file2 not in group:
                                group.append(file2)
                            found_group = True
                            break
                    
                    if not found_group:
                        similar_duplicates.append([file1, file2])
                
                already_checked.add((file1, file2))
                already_checked.add((file2, file1))
        
        # Combine results
        self.duplicates = exact_duplicates + similar_duplicates
        
        print(f"✅ Duplicate analysis completed.")
        print(f"📊 Found {len(self.duplicates)} groups of duplicate or similar files.")
    
    def identify_obsolete(self):
        """Identifies potentially obsolete files"""
        print("\n🔍 Identifying obsolete files...")
        
        # Obsolete criteria
        for file_path in self.files:
            metadata = self.file_metadata[file_path]
            
            # Skip binary files
            if metadata['is_binary']:
                continue
            
            is_obsolete = False
            reasons = []
            
            # Check files with "_old", "backup", "deprecated" in name
            if any(term in file_path.lower() for term in ['_old', 'backup', 'deprecated', '.bak']):
                is_obsolete = True
                reasons.append(f"Name suggests obsolete file ({file_path})")
            
            # Check duplicate files and choose the oldest as obsolete
            for dup_group in self.duplicates:
                if file_path in dup_group:
                    # Sort group by modification date
                    sorted_group = sorted(dup_group, key=lambda f: self.file_metadata[f]['modified'])
                    if file_path != sorted_group[-1]:  # Not the most recent
                        is_obsolete = True
                        reasons.append(f"Older version of duplicated file ({sorted_group[-1]})")
            
            # Check orphan files (not referenced)
            if file_path in self.orphans and file_path not in self.disconnected_files:
                is_obsolete = True
                reasons.append("File not referenced by any other")
            
            # If obsolete, add to list
            if is_obsolete:
                self.potentially_obsolete.append((file_path, reasons))
        
        print(f"✅ Obsolete analysis completed.")
        print(f"📊 Found {len(self.potentially_obsolete)} potentially obsolete files.")
    
    def recommend_actions(self):
        """Recommends actions to improve the project structure"""
        print("\n🔄 Generating recommendations...")
        
        recommendations = []
        
        # 1. Move obsolete files to quarantine
        for file_path, reasons in self.potentially_obsolete:
            # Check if file has important content
            content = self.file_contents[file_path]
            is_important = self._has_important_content(file_path, content)
            
            if is_important:
                recommendations.append({
                    "type": "extract_and_quarantine",
                    "file": file_path,
                    "reasons": reasons,
                    "action": "Extract important content and move to quarantine"
                })
            else:
                recommendations.append({
                    "type": "quarantine",
                    "file": file_path,
                    "reasons": reasons,
                    "action": "Move to quarantine"
                })
        
        # 2. Connect disconnected files
        for file_path in self.disconnected_files:
            # Ignore certain types of files that can legitimately be disconnected
            if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico')):
                continue
                
            # Find similar files that could be connected
            similar_files = self._find_similar_files(file_path)
            if similar_files:
                recommendations.append({
                    "type": "connect",
                    "file": file_path,
                    "similar_files": similar_files,
                    "action": f"Connect with related files: {', '.join(similar_files[:3])}"
                })
        
        # 3. Combine similar files
        for dup_group in self.duplicates:
            if len(dup_group) > 1:
                # Sort by modification date (most recent first)
                sorted_group = sorted(dup_group, 
                                    key=lambda f: self.file_metadata[f]['modified'],
                                    reverse=True)
                
                recommendations.append({
                    "type": "combine",
                    "files": sorted_group,
                    "keep": sorted_group[0],
                    "action": f"Combine duplicate files, keep {sorted_group[0]}"
                })
        
        print(f"✅ Recommendation generation completed.")
        print(f"📊 Generated {len(recommendations)} recommendations.")
        
        return recommendations
    
    def _has_important_content(self, file_path, content):
        """Checks if a file has important content that should be preserved"""
        # Check extension
        extension = os.path.splitext(file_path)[1].lower()
        if extension not in IMPORTANT_EXTENSIONS:
            return False
        
        # Check size
        if len(content) < 100:
            return False
        
        # Check number of important references
        important_terms = ['EVA & GUARANI', 'BIOS-Q', 'Quantum', 'EGOS', 'def ', 'class ', 'function']
        important_refs = sum(1 for term in important_terms if term.lower() in content.lower())
        
        return important_refs >= 2
    
    def _find_similar_files(self, file_path):
        """Finds similar files for potential connection"""
        file_terms = set(re.findall(r'\w+', file_path.lower()))
        
        # Remove stopwords
        stopwords = {'a', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
        file_terms = file_terms - stopwords
        
        similar_files = []
        for other_file in self.files:
            if other_file == file_path:
                continue
                
            other_terms = set(re.findall(r'\w+', other_file.lower()))
            other_terms = other_terms - stopwords
            
            # Calculate similarity
            common_terms = file_terms.intersection(other_terms)
            if len(common_terms) >= 2:
                similar_files.append(other_file)
        
        return similar_files[:5]  # Return up to 5 similar files
    
    def execute_recommendations(self, recommendations, auto_apply=False):
        """Executes recommendations, with option for manual approval"""
        print("\n🔄 Executing recommendations...")
        
        for i, rec in enumerate(recommendations):
            print(f"\n[{i+1}/{len(recommendations)}] {rec['action']}")
            
            # Decide whether to apply automatically or ask for confirmation
            apply = auto_apply
            if not apply:
                choice = input("Apply this recommendation? (s/n/always): ").lower()
                if choice == 'always':
                    auto_apply = True
                    apply = True
                elif choice == 's':
                    apply = True
            
            if apply:
                self._apply_recommendation(rec)
    
    def _apply_recommendation(self, recommendation):
        """Applies a specific recommendation"""
        try:
            rec_type = recommendation['type']
            
            if rec_type == 'quarantine':
                file_path = os.path.join(self.project_root, recommendation['file'])
                quarantine_path = os.path.join(QUARANTINE_DIR, recommendation['file'])
                
                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(quarantine_path), exist_ok=True)
                
                # Move file to quarantine
                shutil.move(file_path, quarantine_path)
                
                # Register action in changelog
                self.changelog.add_entry(
                    content=f"File moved to quarantine: {recommendation['file']}",
                    source="quantum_mycelium.py",
                    category="maintenance",
                    importance=0.7
                )
                print(f"✅ File moved to quarantine: {recommendation['file']}")
            
            elif rec_type == 'extract_and_quarantine':
                file_path = os.path.join(self.project_root, recommendation['file'])
                quarantine_path = os.path.join(QUARANTINE_DIR, recommendation['file'])
                content = self.file_contents[recommendation['file']]
                
                # Create extraction file with important content
                extract_file = os.path.join(STAGING_DIR, f"extract_{os.path.basename(recommendation['file'])}")
                with open(extract_file, 'w', encoding='utf-8') as f:
                    f.write(f"""# Important content extracted from {recommendation['file']}
# Original file moved to quarantine
# Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{content}

# End of extracted content
{QUANTUM_SIGNATURE}
""")
                
                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(quarantine_path), exist_ok=True)
                
                # Move file to quarantine
                shutil.move(file_path, quarantine_path)
                
                # Register action in changelog
                self.changelog.add_entry(
                    content=f"Important content extracted and file moved to quarantine: {recommendation['file']}",
                    source="quantum_mycelium.py",
                    category="maintenance",
                    importance=0.8
                )
                print(f"✅ Important content extracted to {extract_file}")
                print(f"✅ File moved to quarantine: {recommendation['file']}")
            
            elif rec_type == 'combine':
                files = recommendation['files']
                keep_file = recommendation['keep']
                
                # Read content of file to keep
                keep_path = os.path.join(self.project_root, keep_file)
                keep_content = self.file_contents[keep_file]
                
                # Add comment about combination
                new_content = f"""
# ==================================================================
# COMBINED FILE FROM MULTIPLE SIMILAR FILES
# Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Combined files:
# - {keep_file} (kept)
"""
                # Add combined files list
                for f in files:
                    if f != keep_file:
                        new_content += f"# - {f} (moved to quarantine)\n"
                
                new_content += "# ==================================================================\n\n"
                new_content += keep_content
                
                # Add unique content from other files
                for f in files:
                    if f != keep_file:
                        f_content = self.file_contents[f]
                        
                        # Find unique content
                        s = difflib.SequenceMatcher(None, keep_content, f_content)
                        unique_content = ""
                        for opcode in s.get_opcodes():
                            tag, i1, i2, j1, j2 = opcode
                            if tag in ('insert', 'replace'):
                                unique_content += f_content[j1:j2] + "\n"
                        
                        if unique_content.strip():
                            new_content += f"\n\n# ==================================================================\n"
                            new_content += f"# UNIQUE CONTENT FROM {f}\n"
                            new_content += f"# ==================================================================\n\n"
                            new_content += unique_content
                
                # Update main file
                with open(keep_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                # Move other files to quarantine
                for f in files:
                    if f != keep_file:
                        file_path = os.path.join(self.project_root, f)
                        quarantine_path = os.path.join(QUARANTINE_DIR, f)
                        
                        # Create destination directory if it doesn't exist
                        os.makedirs(os.path.dirname(quarantine_path), exist_ok=True)
                        
                        # Move file to quarantine
                        shutil.move(file_path, quarantine_path)
                
                # Register action in changelog
                self.changelog.add_entry(
                    content=f"Duplicate files combined in {keep_file}",
                    source="quantum_mycelium.py",
                    category="optimization",
                    importance=0.9
                )
                print(f"✅ Files combined in {keep_file}")
            
            # Connections are only recommendations, we don't implement automatically
            elif rec_type == 'connect':
                print(f"ℹ️ Recommendation to connect files (manual implementation required)")
                print(f"  File: {recommendation['file']}")
                print(f"  Connect with: {', '.join(recommendation['similar_files'][:3])}")
        
        except Exception as e:
            print(f"⚠️ Error applying recommendation: {str(e)}")
    
    def generate_report(self, recommendations):
        """Generates a detailed report of the analysis and recommendations"""
        print("\n📝 Generating mycelial analysis report...")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(MYCELIUM_REPORT_FILE), exist_ok=True)
        
        with open(MYCELIUM_REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(f"""# Mycelial Analysis Report - EVA & GUARANI

{QUANTUM_SIGNATURE}

## Analysis Summary

**Analysis date**: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

**General statistics**:
- Total analyzed files: {len(self.files)}
- Files without connections: {len(self.disconnected_files)}
- Files not referenced by others: {len(self.orphans)}
- Duplicate file groups: {len(self.duplicates)}
- Potentially obsolete files: {len(self.potentially_obsolete)}
- Generated recommendations: {len(recommendations)}

## Main Recommendations

""")
            
            # Group recommendations by type
            rec_by_type = defaultdict(list)
            for rec in recommendations:
                rec_by_type[rec['type']].append(rec)
            
            # Add recommendations by type
            if 'quarantine' in rec_by_type:
                f.write("### Files for Quarantine\n\n")
                for rec in rec_by_type['quarantine']:
                    f.write(f"- **{rec['file']}**\n")
                    for reason in rec['reasons']:
                        f.write(f"  - {reason}\n")
                f.write("\n")
            
            if 'extract_and_quarantine' in rec_by_type:
                f.write("### Files with Important Content to Extract\n\n")
                for rec in rec_by_type['extract_and_quarantine']:
                    f.write(f"- **{rec['file']}**\n")
                    for reason in rec['reasons']:
                        f.write(f"  - {reason}\n")
                f.write("\n")
            
            if 'combine' in rec_by_type:
                f.write("### Duplicate Files to Combine\n\n")
                for rec in rec_by_type['combine']:
                    f.write(f"- Keep: **{rec['keep']}**\n")
                    f.write("  - Combine with:\n")
                    for file in rec['files']:
                        if file != rec['keep']:
                            f.write(f"    - {file}\n")
                f.write("\n")
            
            if 'connect' in rec_by_type:
                f.write("### Connection Suggestions\n\n")
                for rec in rec_by_type['connect']:
                    f.write(f"- File: **{rec['file']}**\n")
                    f.write("  - Connect with:\n")
                    for file in rec['similar_files'][:3]:
                        f.write(f"    - {file}\n")
                f.write("\n")
            
            # Add analysis details
            f.write("""## Analysis Details

### Methodology

Mycelial analysis follows these principles:

1. **Connection Identification**: Just as fungal networks in nature connect different parts of an ecosystem, we seek to identify and strengthen connections between system components.

2. **Redundancy Detection**: We identify duplicates and redundancies that can be optimized to make the system more efficient.

3. **Preservation of Valuable Content**: Before removing any component, we extract and preserve important content.

4. **Quarantine Instead of Exclusion**: We move obsolete files to quarantine, allowing recovery if necessary.

### Quantum Principles Applied

- **Conscious Modularity**: Deep understanding of parts and the whole
- **Systematic Mapping**: Precise mapping of connections and potentialities
- **Evolutive Preservation**: Maintaining essence during transformations

""")
            
            # Finalize report
            f.write(f"\n\n{QUANTUM_SIGNATURE}\n")
        
        # Save data in JSON for future use
        with open(MYCELIUM_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.datetime.now().isoformat(),
                'disconnected_files': self.disconnected_files,
                'orphans': self.orphans,
                'duplicates': self.duplicates,
                'potentially_obsolete': [(file, reasons) for file, reasons in self.potentially_obsolete],
                'recommendations': recommendations
            }, f, indent=4)
        
        print(f"✅ Report generated in {MYCELIUM_REPORT_FILE}")
        print(f"✅ Raw data saved in {MYCELIUM_JSON_FILE}")
    
    def run_analysis(self, auto_apply=False):
        """Executes the complete mycelial analysis process"""
        self.scan_project()
        self.analyze_connections()
        self.find_duplicates()
        self.identify_obsolete()
        recommendations = self.recommend_actions()
        self.generate_report(recommendations)
        
        # Ask if you want to execute recommendations
        if not auto_apply:
            choice = input("\nDo you want to execute recommendations? (s/n/auto): ").lower()
            if choice in ('s', 'auto'):
                self.execute_recommendations(recommendations, auto_apply=(choice == 'auto'))
        else:
            self.execute_recommendations(recommendations, auto_apply=True)
        
        print(f"\n✧༺❀༻∞ EVA & GUARANI - Mycelial Analysis Completed ∞༺❀༻✧\n")
        print(f"Report available in: {MYCELIUM_REPORT_FILE}")

# ========================================================================
# MAIN FUNCTIONS
# ========================================================================

def run_mycelium_analysis(auto_apply=False):
    """Executes mycelial analysis with option for automatic application"""
    mycelium = QuantumMycelium()
    mycelium.run_analysis(auto_apply=auto_apply)

def main():
    """Main function"""
    print("\n✧༺❀༻∞ EVA & GUARANI - Quantum Mycelium ∞༺❀༻✧\n")
    print("Mycelial Analysis and Systemic Integrity System")
    print("Version: 1.0.0 'Pear'\n")
    
    print("MENU OF OPTIONS:")
    print("1. Analyze project and generate recommendations")
    print("2. Analyze and apply recommendations with manual approval")
    print("3. Analyze and apply recommendations automatically")
    print("4. Exit")
    
    choice = input("\nChoose an option (1-4): ")
    
    if choice == "1":
        mycelium = QuantumMycelium()
        mycelium.scan_project()
        mycelium.analyze_connections()
        mycelium.find_duplicates()
        mycelium.identify_obsolete()
        recommendations = mycelium.recommend_actions()
        mycelium.generate_report(recommendations)
    elif choice == "2":
        run_mycelium_analysis(auto_apply=False)
    elif choice == "3":
        run_mycelium_analysis(auto_apply=True)
    
    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

if __name__ == "__main__":
    main() 