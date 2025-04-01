#!/usr/bin/env python3
python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Quarantine System by Date (CRONOS)
==================================================

This script identifies files not updated until a specific date
and moves them to the quarantine folder, preserving the original structure
and generating detailed logs of the process with ethical awareness.

Author: EVA & GUARANI
Version: 1.0
"""

import os
import sys
import time
import datetime
import shutil
import json
import argparse
from pathlib import Path
from collections import defaultdict

def log_event(message, level='INFO'):
    """
    Logs event to the console with timestamp
    
    Args:
        message (str): Message to be logged
        level (str): Log level (INFO, WARNING, ERROR)
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}][{level}] {message}"
    print(log_entry)

def parse_arguments():
    """
    Parses command line arguments
    """
    parser = argparse.ArgumentParser(description="EVA & GUARANI - Quarantine System by Date")
    parser.add_argument("--cutoff-date", type=str, default=None, 
                        help="Cutoff date to consider files obsolete (format: YYYY-MM-DD)")
    parser.add_argument("--exclude-dirs", type=str, default="node_modules,.git,.vscode,venv",
                        help="List of directories to exclude, separated by commas")
    parser.add_argument("--exclude-exts", type=str, default="",
                        help="List of extensions to exclude, separated by commas")
    parser.add_argument("--quarantine-dir", type=str, default="quarantine",
                        help="Directory where files will be quarantined")
    parser.add_argument("--dry-run", action="store_true", 
                        help="Runs in simulation mode without moving files")
    parser.add_argument("--report-dir", type=str, default="./reports",
                        help="Directory to save the report")
    parser.add_argument("--min-size", type=int, default=0,
                        help="Minimum file size in bytes to be considered")
    parser.add_argument("--only-extensions", type=str, default="",
                        help="List of extensions to process only, separated by commas")
    parser.add_argument("--analyze-extensions", action="store_true",
                        help="Analyzes and shows the distribution of obsolete file extensions")
    
    return parser.parse_args()

def find_old_files_by_date(root_path, cutoff_date, exclude_dirs=None, exclude_exts=None, only_exts=None, min_size=0):
    """
    Finds files not modified until the cutoff date
    
    :param root_path: Root path to start the search
    :param cutoff_date: Cutoff date (datetime.date)
    :param exclude_dirs: List of directories to exclude
    :param exclude_exts: List of extensions to exclude
    :param only_exts: List of extensions to include only
    :param min_size: Minimum file size in bytes
    :return: List of file paths
    """
    old_files = []
    total_files = 0
    
    # Convert date to timestamp
    cutoff_timestamp = datetime.datetime.combine(cutoff_date, datetime.time()).timestamp()
    
    exclude_dirs = exclude_dirs or []
    exclude_exts = exclude_exts or []
    only_exts = only_exts or []
    
    log_event(f"Starting search for files not modified until {cutoff_date.strftime('%d/%m/%Y')}", "INFO")
    
    # Counters
    old_file_count = 0
    errors = 0
    
    # Traverse file system
    for root, dirs, files in os.walk(root_path):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            total_files += 1
            
            # Check extension
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            
            # Skip excluded extensions
            if ext in exclude_exts:
                continue
                
            # If only_extensions specified, check if extension is included
            if only_exts and ext not in only_exts:
                continue
            
            file_path = os.path.join(root, file)
            
            try:
                # Check size
                file_size = os.path.getsize(file_path)
                if file_size < min_size:
                    continue
                
                # Check modification date
                mod_time = os.path.getmtime(file_path)
                
                # If modified after the cutoff date, skip
                if mod_time > cutoff_timestamp:
                    continue
                
                # Old file, include in list
                mod_date = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
                rel_path = os.path.relpath(file_path, root_path)
                
                old_files.append({
                    'path': rel_path,
                    'absolute_path': file_path,
                    'size_bytes': file_size,
                    'last_modified': mod_date,
                    'extension': ext
                })
                
                old_file_count += 1
                
                # Log every 100 old files found
                if old_file_count % 100 == 0:
                    log_event(f"Found {old_file_count} files not updated until {cutoff_date.strftime('%d/%m/%Y')}...")
                        
            except Exception as e:
                errors += 1
                if errors < 10:  # Limit number of errors in log
                    log_event(f"Error analyzing '{file_path}': {e}", 'ERROR')
                elif errors == 10:
                    log_event("Many errors found, suppressing additional messages...", 'WARNING')
    
    # Sort by date (oldest first)
    old_files.sort(key=lambda x: x['last_modified'])
    
    log_event(f"Search completed. Analyzed {total_files} files, found {len(old_files)} files to be moved, {errors} errors")
    return old_files

def move_files_to_quarantine(old_files, quarantine_dir, dry_run=True):
    """
    Moves files to quarantine, preserving directory structure
    
    Args:
        old_files (list): List of old files to be moved
        quarantine_dir (str): Quarantine directory
        dry_run (bool): If True, only simulates the operation
        
    Returns:
        dict: Process report
    """
    log_event(f"{'Simulating' if dry_run else 'Executing'} movement of {len(old_files)} files to quarantine")
    
    # Create quarantine directory if it doesn't exist
    if not dry_run:
        os.makedirs(quarantine_dir, exist_ok=True)
    
    # Prepare report
    report = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'mode': 'DRY-RUN' if dry_run else 'EXECUTION',
        'total_files': len(old_files),
        'success': [],
        'failed': []
    }
    
    # Counters for feedback
    success_count = 0
    failed_count = 0
    
    # Process each file
    for file_info in old_files:
        src_path = file_info['absolute_path']
        rel_path = file_info['path']
        
        # Create destination directory preserving structure
        dest_dir = os.path.join(quarantine_dir, os.path.dirname(rel_path))
        dest_path = os.path.join(quarantine_dir, rel_path)
        
        try:
            # Check if file exists
            if not os.path.exists(src_path):
                raise FileNotFoundError(f"File not found: {src_path}")
            
            # In real execution mode, move the file
            if not dry_run:
                # Create destination directories if they don't exist
                os.makedirs(dest_dir, exist_ok=True)
                
                # Move file
                shutil.move(src_path, dest_path)
            
            # Register success
            success_count += 1
            report['success'].append({
                'source': rel_path,
                'destination': os.path.join('quarantine', rel_path),
                'last_modified': file_info['last_modified'],
                'size_bytes': file_info['size_bytes']
            })
            
            # Log every 50 files moved
            if success_count % 50 == 0:
                log_event(f"{'[SIMULATION] ' if dry_run else ''}Processed {success_count} files...")
                
        except Exception as e:
            failed_count += 1
            report['failed'].append({
                'source': rel_path,
                'error': str(e)
            })
            
            if failed_count < 10:  # Limit number of errors in log
                log_event(f"Error moving to quarantine: {rel_path} - {e}", 'ERROR')
            elif failed_count == 10:
                log_event("Many errors found, suppressing additional messages...", 'WARNING')
    
    # Update counters in the report
    report['success_count'] = success_count
    report['failed_count'] = failed_count
    
    log_event(f"Process completed: {success_count} files {'simulated' if dry_run else 'moved'}, {failed_count} failures")
    return report

def generate_report(report, old_files, cutoff_date, report_dir, report_file=None):
    """
    Generates a detailed quarantine report
    
    Args:
        report (dict): Process report
        old_files (list): List of files to be moved
        cutoff_date (datetime.datetime): Cutoff date
        report_dir (str): Directory for reports
        report_file (str): Report file name
    """
    # Create report directory if it doesn't exist
    os.makedirs(report_dir, exist_ok=True)
    
    # Report file name
    if not report_file:
        report_file = os.path.join(
            report_dir, 
            f"quarantine_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
    else:
        report_file = os.path.join(report_dir, report_file)
    
    # Add information to the report
    full_report = {
        **report,
        'cutoff_date': cutoff_date.strftime('%Y-%m-%d'),
        'total_size_bytes': sum(f['size_bytes'] for f in old_files),
        'extensions': {}
    }
    
    # Statistics by extension
    extension_stats = defaultdict(int)
    for file in old_files:
        ext = file['extension'] or 'no_extension'
        extension_stats[ext] += 1
    
    full_report['extensions'] = dict(extension_stats)
    
    # Save JSON report
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(full_report, f, indent=2, ensure_ascii=False)
    
    # Generate Markdown report
    md_report = f"""# EVA & GUARANI Quarantine Report
*Generated on: {full_report['timestamp']}*

## 📊 General Statistics

- **Cutoff Date:** {cutoff_date.strftime('%d/%m/%Y')}
- **Total Files:** {full_report['total_files']}
- **Execution Mode:** {'SIMULATION' if report['mode'] == 'DRY-RUN' else 'REAL EXECUTION'}
- **Total Size:** {full_report['total_size_bytes'] / (1024*1024):.2f} MB

## 📄 Distribution by Extension

| Extension | Quantity |
|-----------|----------|
"""
    
    # Add statistics by extension
    for ext, count in sorted(extension_stats.items(), key=lambda x: x[1], reverse=True):
        md_report += f"| {ext} | {count} |\n"
    
    # Add success/failure statistics
    md_report += f"""
## 🔄 Process Results

- **Files Successfully Processed:** {full_report['success_count']}
- **Failures:** {full_report['failed_count']}

## 🚀 Recommended Next Steps

1. **Verify Integrity** - Confirm that the files were moved correctly
2. **Review Functionality** - Check if the system functionality remains intact
3. **Duplicate Analysis** - Perform duplicate analysis for additional optimization
4. **Documentation** - Update documentation to reflect the changes made

---

*Report generated with love and awareness by the EVA & GUARANI system 🌌*

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""
    
    # Save Markdown report
    md_report_file = report_file.replace('.json', '.md')
    with open(md_report_file, 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    log_event(f"JSON report saved at: {report_file}")
    log_event(f"Markdown report saved at: {md_report_file}")
    
    return report_file, md_report_file

def analyze_extensions(old_files):
    """
    Analyzes the distribution of obsolete file extensions
    
    :param old_files: List of dictionaries with obsolete file information
    :return: None
    """
    log_event("Analyzing distribution of obsolete file extensions", "INFO")
    extension_count = {}
    no_extension = 0
    
    for file_info in old_files:
        file_path = file_info['path']
        file_name = os.path.basename(file_path)
        if '.' in file_name:
            extension = file_name.split('.')[-1].lower()
            extension_count[extension] = extension_count.get(extension, 0) + 1
        else:
            no_extension += 1
    
    log_event(f"Found {len(extension_count)} different types of extensions", "INFO")
    
    # Sort by quantity, from largest to smallest
    sorted_extensions = sorted(extension_count.items(), key=lambda x: x[1], reverse=True)
    
    # Show the 20 most common extensions
    print("\n📊 Extension Distribution (Top 20):")
    print("=" * 50)
    print(f"{'Extension':<15} | {'Quantity':<10} | {'Percentage':<12}")
    print("-" * 50)
    
    total_files = len(old_files)
    for i, (ext, count) in enumerate(sorted_extensions[:20]):
        percentage = (count / total_files) * 100
        print(f"{ext:<15} | {count:<10} | {percentage:.2f}%")
    
    if no_extension > 0:
        percentage = (no_extension / total_files) * 100
        print(f"{'<no extension>':<15} | {no_extension:<10} | {percentage:.2f}%")
    
    print("=" * 50)
    
    # Group by categories
    categories = {
        "Code": ["py", "js", "ts", "jsx", "tsx", "java", "c", "cpp", "cs", "go", "rb", "php", "html", "css", "sh", "bat", "ps1"],
        "Data": ["json", "csv", "xml", "yaml", "yml", "sql", "db", "sqlite"],
        "Documents": ["md", "txt", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods"],
        "Images": ["jpg", "jpeg", "png", "gif", "svg", "bmp", "tiff", "webp", "ico"],
        "Audio/Video": ["mp3", "wav", "ogg", "mp4", "avi", "mov", "flv", "webm"],
        "Compressed": ["zip", "rar", "7z", "tar", "gz", "bz2"],
        "Config": ["ini", "cfg", "conf", "env", "config"],
        "Binaries": ["exe", "dll", "so", "dylib", "bin"]
    }
    
    category_count = {category: 0 for category in categories}
    others = 0
    
    for ext, count in extension_count.items():
        categorized = False
        for category, extensions in categories.items():
            if ext in extensions:
                category_count[category] += count
                categorized = True
                break
        
        if not categorized:
            others += count
    
    # Add no extension and others
    if no_extension > 0:
        category_count["No Extension"] = no_extension
    
    if others > 0:
        category_count["Others"] = others
    
    # Show categories
    print("\n📊 Distribution by Categories:")
    print("=" * 50)
    print(f"{'Category':<15} | {'Quantity':<10} | {'Percentage':<12}")
    print("-" * 50)
    
    sorted_categories = sorted(category_count.items(), key=lambda x: x[1], reverse=True)
    for category, count in sorted_categories:
        if count > 0:
            percentage = (count / total_files) * 100
            print(f"{category:<15} | {count:<10} | {percentage:.2f}%")
    
    print("=" * 50)
    
    return extension_count

def main():
    """
    Main function
    """
    print("✧༺❀༻∞ EVA & GUARANI - Quarantine System by Date ∞༺❀༻✧")
    print("File analysis and quarantine with love and awareness...\n")
    
    args = parse_arguments()
    
    # Define the cutoff date
    cutoff_date = None
    if args.cutoff_date:
        try:
            cutoff_date = datetime.datetime.strptime(args.cutoff_date, "%Y-%m-%d").date()
        except ValueError:
            log_event(f"Invalid date format: {args.cutoff_date}. Use the format YYYY-MM-DD", "ERROR")
            sys.exit(1)
    else:
        days_ago = 365  # Default: 1 year
        cutoff_date = datetime.datetime.now().date() - datetime.timedelta(days=days_ago)
        log_event(f"Cutoff date not specified. Using default: {cutoff_date}", "INFO")
    
    # Prepare exclusion lists
    exclude_dirs = [d.strip() for d in args.exclude_dirs.split(",") if d.strip()]
    exclude_exts = [e.strip().lower() for e in args.exclude_exts.split(",") if e.strip()]
    only_extensions = [e.strip().lower() for e in args.only_extensions.split(",") if e.strip()]
    
    # Search for old files
    old_files = find_old_files_by_date(".", cutoff_date, exclude_dirs, exclude_exts, only_extensions, args.min_size)
    
    # If no old files, exit
    if not old_files:
        log_event("No obsolete files found", "INFO")
        return
    
    # If extension analysis requested, just show distribution and exit
    if args.analyze_extensions:
        analyze_extensions(old_files)
        return
    
    # Show preview of the oldest files
    print(f"\n🕰️ Preview of the {min(10, len(old_files))} files to be moved:")
    for i, file in enumerate(old_files[:10], 1):
        print(f"{i