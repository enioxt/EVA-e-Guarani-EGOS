#!/usr/bin/env python3
python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Duplicate Consolidation System (CRONOS/ATLAS)
===================================================================

This script moves identified duplicate files to quarantine
based on the previously generated analysis report, keeping only
one copy of each file to optimize the system structure.

Author: EVA & GUARANI
Version: 1.0
"""

import os
import sys
import json
import shutil
import datetime
import argparse
from pathlib import Path

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
    
    Returns:
        argparse.Namespace: Processed arguments
    """
    parser = argparse.ArgumentParser(description='EVA & GUARANI - Duplicate Consolidation')
    
    parser.add_argument('--report-file', type=str, required=True,
                        help='JSON report file with identified duplicates')
    
    parser.add_argument('--target-dir', type=str, default='./duplicate_quarantine',
                        help='Directory where duplicates will be moved (default: ./duplicate_quarantine)')
    
    parser.add_argument('--dry-run', action='store_true',
                        help='Run in simulation mode without moving files')
    
    parser.add_argument('--keep-newest', action='store_true',
                        help='Keep the most recent file and move others (default: keep the first listed)')
    
    parser.add_argument('--max-files', type=int, default=0,
                        help='Maximum number of files to move (0 = no limit)')
    
    parser.add_argument('--report-dir', type=str, default='./reports',
                        help='Directory to save operation report')
    
    return parser.parse_args()

def load_duplicate_report(report_file):
    """
    Loads the duplicate report
    
    Args:
        report_file (str): Path to the report file
        
    Returns:
        dict: Duplicate report data
    """
    log_event(f"Loading duplicate report: {report_file}")
    
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
            
        log_event(f"Report loaded successfully")
        return report_data
    except Exception as e:
        log_event(f"Error loading report: {e}", 'ERROR')
        sys.exit(1)

def move_duplicates_to_quarantine(report_data, target_dir, dry_run=True, keep_newest=False, max_files=0):
    """
    Moves duplicate files to quarantine
    
    Args:
        report_data (dict): Duplicate report data
        target_dir (str): Destination directory for quarantine
        dry_run (bool): If True, only simulates the operation without moving files
        keep_newest (bool): If True, keeps the most recent file and moves others
        max_files (int): Maximum number of files to move (0 = no limit)
        
    Returns:
        dict: Operation report
    """
    log_event(f"{'Simulating' if dry_run else 'Executing'} duplicate movement to: {target_dir}")
    
    # Create quarantine directory if it doesn't exist and not a dry-run
    if not dry_run:
        os.makedirs(target_dir, exist_ok=True)
    
    # Prepare operation report
    operation_report = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'mode': 'DRY-RUN' if dry_run else 'EXECUTION',
        'target_dir': target_dir,
        'keep_newest': keep_newest,
        'exact_duplicates_processed': 0,
        'files_moved': 0,
        'errors': 0,
        'groups': []
    }
    
    # Access exact duplicates
    exact_duplicates = report_data.get('exact_duplicates', [])
    
    if not exact_duplicates:
        log_event("No exact duplicate groups found in the report", 'WARNING')
        return operation_report
    
    log_event(f"Processing {len(exact_duplicates)} exact duplicate groups")
    
    # Counter for moved files
    files_moved = 0
    
    # Process each duplicate group
    for group_index, dup_group in enumerate(exact_duplicates):
        hash_value = dup_group.get('hash', f"group_{group_index}")
        files = dup_group.get('files', [])
        
        if len(files) <= 1:
            continue  # Skip if there are no duplicates
        
        group_report = {
            'hash': hash_value,
            'total_files': len(files),
            'files_kept': [],
            'files_moved': [],
            'errors': []
        }
        
        # Determine which file to keep
        if keep_newest:
            # Sort by modification date (most recent first)
            try:
                files.sort(key=lambda x: os.path.getmtime(x['absolute_path']), reverse=True)
            except Exception as e:
                log_event(f"Error sorting files by date: {e}", 'WARNING')
        
        # First file in the list is the one to be kept
        file_to_keep = files[0]
        group_report['files_kept'].append(file_to_keep['path'])
        
        # Move the remaining files
        for file_info in files[1:]:
            try:
                src_path = file_info.get('absolute_path')
                rel_path = file_info.get('path')
                
                if not src_path or not rel_path:
                    raise ValueError(f"Incomplete information for the file")
                
                # Check if the file exists
                if not os.path.exists(src_path):
                    raise FileNotFoundError(f"File not found: {src_path}")
                
                # Create destination directory preserving the structure
                dest_dir = os.path.join(target_dir, os.path.dirname(rel_path))
                dest_path = os.path.join(target_dir, rel_path)
                
                # Execute the move if not a dry-run
                if not dry_run:
                    # Create destination directories
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Move file
                    shutil.move(src_path, dest_path)
                
                # Log success
                group_report['files_moved'].append(rel_path)
                files_moved += 1
                
                # Log every 10 files
                if files_moved % 10 == 0:
                    log_event(f"{'[SIMULATION] ' if dry_run else ''}Moved {files_moved} duplicate files...")
                
                # Check maximum limit
                if max_files > 0 and files_moved >= max_files:
                    log_event(f"Maximum limit of {max_files} files reached")
                    break
                    
            except Exception as e:
                error_msg = f"Error moving {rel_path}: {e}"
                log_event(error_msg, 'ERROR')
                group_report['errors'].append(error_msg)
                operation_report['errors'] += 1
        
        # Add group report
        operation_report['groups'].append(group_report)
        operation_report['exact_duplicates_processed'] += 1
        
        # Check maximum limit (between groups)
        if max_files > 0 and files_moved >= max_files:
            break
    
    # Update final counters
    operation_report['files_moved'] = files_moved
    
    log_event(f"Operation completed: {files_moved} files {'simulated' if dry_run else 'moved'} to quarantine")
    return operation_report

def generate_report(operation_report, report_dir):
    """
    Generates detailed operation report
    
    Args:
        operation_report (dict): Operation data
        report_dir (str): Directory to save the report
    
    Returns:
        tuple: Paths of the report files (json, md)
    """
    # Create report directory if it doesn't exist
    os.makedirs(report_dir, exist_ok=True)
    
    # Base name for report files
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = f"duplicate_consolidation_{timestamp}"
    
    # Save JSON report
    json_path = os.path.join(report_dir, f"{base_name}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(operation_report, f, indent=2, ensure_ascii=False)
    
    # Generate Markdown report
    md_content = f"""# Duplicate Consolidation Report
*Generated on: {operation_report['timestamp']}*

## 📊 Operation Statistics

- **Execution Mode:** {operation_report['mode']}
- **Quarantine Directory:** `{operation_report['target_dir']}`
- **Preservation Criterion:** {"Most recent file" if operation_report['keep_newest'] else "First listed file"}
- **Duplicate Groups Processed:** {operation_report['exact_duplicates_processed']}
- **Total Files Moved:** {operation_report['files_moved']}
- **Errors Found:** {operation_report['errors']}

## 🔍 Processed Group Details

"""

    # Add information of up to 10 most significant groups
    significant_groups = sorted(operation_report['groups'], key=lambda g: len(g['files_moved']), reverse=True)[:10]
    
    for i, group in enumerate(significant_groups, 1):
        md_content += f"### Group {i}: {group['hash'][:8]}...\n\n"
        md_content += f"- **Total Files:** {group['total_files']}\n"
        md_content += f"- **Files Kept ({len(group['files_kept'])}):**\n"
        
        for file in group['files_kept'][:3]:  # Show up to 3 kept files
            md_content += f"  - `{file}`\n"
            
        if len(group['files_kept']) > 3:
            md_content += f"  - ... plus {len(group['files_kept']) - 3} more file(s)\n"
        
        md_content += f"- **Files Moved to Quarantine ({len(group['files_moved'])}):**\n"
        
        for file in group['files_moved'][:5]:  # Show up to 5 moved files
            md_content += f"  - `{file}`\n"
            
        if len(group['files_moved']) > 5:
            md_content += f"  - ... plus {len(group['files_moved']) - 5} more file(s)\n"
        
        if group['errors']:
            md_content += f"- **Errors ({len(group['errors'])}):**\n"
            for error in group['errors'][:3]:
                md_content += f"  - {error}\n"
            
            if len(group['errors']) > 3:
                md_content += f"  - ... plus {len(group['errors']) - 3} more error(s)\n"
        
        md_content += "\n"
    
    # Add recommendations
    md_content += """
## 🚀 Recommended Next Steps

1. **Verify Integrity** - Confirm the system continues to function correctly after the move
2. **Manual Review** - Examine the quarantine content to ensure no important files were removed
3. **Implement Structure** - Organize the system according to the proposed new structure
4. **Documentation** - Update the documentation to reflect the changes made

---

*Process carried out with love and awareness by the EVA & GUARANI system 🌌*

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""
    
    # Save Markdown report
    md_path = os.path.join(report_dir, f"{base_name}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    log_event(f"JSON report saved at: {json_path}")
    log_event(f"Markdown report saved at: {md_path}")
    
    return json_path, md_path

def main():
    """
    Main function
    """
    print("✧༺❀༻∞ EVA & GUARANI - Duplicate Consolidation System ∞༺❀༻✧")
    print("Starting duplicate consolidation with love and awareness...\n")
    
    # Process arguments
    args = parse_arguments()
    
    # Load duplicate report
    report_data = load_duplicate_report(args.report_file)
    
    # Confirmation if not a simulation
    if not args.dry_run:
        print(f"\nATTENTION: You are about to move duplicate files to quarantine.")
        print(f"This operation will keep only one copy of each duplicate file group.")
        confirmation = input(f"Do you wish to proceed? (y/n): ")
        
        if confirmation.lower() != 'y':
            print("Operation canceled by the user.")
            sys.exit(0)
    
    # Move duplicates to quarantine
    operation_report = move_duplicates_to_quarantine(
        report_data,
        args.target_dir,
        args.dry_run,
        args.keep_newest,
        args.max_files
    )
    
    # Generate report
    json_report, md_report = generate_report(operation_report, args.report_dir)
    
    print("\nProcess completed with love and awareness!")
    print(f"Groups processed: {operation_report['exact_duplicates_processed']}")
    print(f"Files moved: {operation_report['files_moved']}")
    print(f"Errors: {operation_report['errors']}")
    print(f"Mode: {'SIMULATION' if args.dry_run else 'REAL EXECUTION'}")
    print(f"Report: {md_report}")
    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

if __name__ == "__main__":
    main()