#!/usr/bin/env python3
# Important content extracted from staging\extract_move_old_files_to_quarantine.py
# Original file moved to quarantine
# Date: 2025-03-22 08:45:53

# Important content extracted from tools\utilities\move_old_files_to_quarantine.py
# Original file moved to quarantine
# Date: 2025-03-22 08:37:23

python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Identification and Quarantine System (CRONOS)
=============================================================

This script identifies files that have not been used for a long time and moves them to
the quarantine folder, preserving the original structure and generating detailed logs
of the process with ethical awareness.

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
    Processes command line arguments

    Returns:
        argparse.Namespace: Processed arguments
    """
    parser = argparse.ArgumentParser(description='EVA & GUARANI - Identification and Quarantine System')

    parser.add_argument('--days', type=int, default=180,
                        help='Number of days without modification to consider a file obsolete (default: 180)')

    parser.add_argument('--exclude-dirs', type=str, default='.git,.github,.vscode,__pycache__,node_modules,quarantine,backup,logs',
                        help='List of directories to ignore, separated by commas')

    parser.add_argument('--exclude-exts', type=str, default='.git,.pyc,.pyo,.exe,.dll,.obj,.o',
                        help='List of extensions to ignore, separated by commas')

    parser.add_argument('--quarantine-dir', type=str, default='./quarantine',
                        help='Quarantine directory (default: ./quarantine)')

    parser.add_argument('--dry-run', action='store_true',
                        help='Performs a simulation without moving files')

    parser.add_argument('--report-file', type=str, default='quarantine_report.json',
                        help='File to save the report of moved files')

    parser.add_argument('--min-size', type=int, default=0,
                        help='Minimum size in bytes to consider for quarantine (default: 0)')

    parser.add_argument('--only-extensions', type=str, default='',
                        help='Only process these file types (extensions separated by commas)')

    return parser.parse_args()

def find_old_files(root_path, days_threshold, exclude_dirs, exclude_exts, min_size, only_extensions):
    """
    Finds files that have not been modified for more than N days

    Args:
        root_path (str): Root directory to be analyzed
        days_threshold (int): Number of days to consider a file obsolete
        exclude_dirs (list): List of directories to ignore
        exclude_exts (list): List of extensions to ignore
        min_size (int): Minimum size in bytes to consider
        only_extensions (list): List of extensions to process (empty = all)

    Returns:
        list: List of dictionaries with information about old files
    """
    log_event(f"Starting search for files not modified for more than {days_threshold} days")

    threshold_date = time.time() - (days_threshold * 24 * 60 * 60)
    old_files = []

    # Convert extensions for processing
    only_exts_set = set()
    if only_extensions:
        only_exts_set = {ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in only_extensions}

    # Counters
    total_files = 0
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
            if only_exts_set and ext not in only_exts_set:
                continue

            file_path = os.path.join(root, file)

            try:
                # Check size
                file_size = os.path.getsize(file_path)
                if file_size < min_size:
                    continue

                # Check modification date
                mod_time = os.path.getmtime(file_path)
                if mod_time < threshold_date:
                    # Old file, calculate age in days
                    age_days = int((time.time() - mod_time) / (24 * 60 * 60))

                    # Age calculation in months (approximate)
                    age_months = age_days // 30

                    # Register old file
                    rel_path = os.path.relpath(file_path, root_path)
                    old_files.append({
                        'path': rel_path,
                        'absolute_path': file_path,
                        'size_bytes': file_size,
                        'last_modified': datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d'),
                        'extension': ext,
                        'age_days': age_days,
                        'age_months': age_months
                    })

                    old_file_count += 1

                    # Log every 100 old files found
                    if old_file_count % 100 == 0:
                        log_event(f"Found {old_file_count} old files so far...")

            except Exception as e:
                errors += 1
                if errors < 10:  # Limit number of errors in log
                    log_event(f"Error analyzing '{file_path}': {e}", 'ERROR')
                elif errors == 10:
                    log_event("Many errors found, suppressing additional messages...", 'WARNING')

    # Sort by age (oldest first)
    old_files.sort(key=lambda x: x['age_days'], reverse=True)

    log_event(f"Search completed. Analyzed {total_files} files, found {len(old_files)} old files, {errors} errors")
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
    log_event(f"{'Simulating' if dry_run else 'Executing'} moving {len(old_files)} files to quarantine")

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
                'age_days': file_info['age_days'],
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

    # Update counters in report
    report['success_count'] = success_count
    report['failed_count'] = failed_count

    log_event(f"Process completed: {success_count} files {'simulated' if dry_run else 'moved'}, {failed_count} failures")
    return report

def save_report(report, report_file):
    """
    Saves report in JSON format

    Args:
        report (dict): Report to be saved
        report_file (str): Path of the report file
    """
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        log_event(f"Report saved in: {report_file}")
    except Exception as e:
        log_event(f"Error saving report: {e}", 'ERROR')

def main():
    """
    Main function
    """
    print("✧༺❀༻∞ EVA & GUARANI - Identification and Quarantine System ∞༺❀༻✧")
    print("File analysis and quarantine with love and awareness...\n")

    args = parse_arguments()

    # Process exclusion lists
    exclude_dirs = args.exclude_dirs.split(',')
    exclude_exts = args.exclude_exts.split(',')
    only_extensions = args.only_extensions.split(',') if args.only_extensions else []

    # Find old files
    old_files = find_old_files(
        '.',  # Current directory
        args.days,
        exclude_dirs,
        exclude_exts,
        args.min_size,
        only_extensions
    )

    if not old_files:
        log_event("No old files found that meet the criteria.")
        return

    # Show preview of oldest files
    print("\n🕰️ Preview of the 10 oldest files:")
    for i, file in enumerate(old_files[:10], 1):
        print(f"{i}. '{file['path']}' - {file['age_days']} days ({file['last_modified']})")

    # Confirm action if not dry-run
    if not args.dry_run:
        confirmation = input(f"\nMoving {len(old_files)} files to quarantine. Confirm? (y/n): ")
        if confirmation.lower() != 'y':
            print("Operation canceled by user.")
            return

    # Move files to quarantine
    report = move_files_to_quarantine(old_files, args.quarantine_dir, args.dry_run)

    # Save report
    save_report(report, args.report_file)

    print("\nProcess completed with love and awareness!")
    print(f"Total files: {len(old_files)}")
    print(f"Success: {report['success_count']}")
    print(f"Failures: {report['failed_count']}")
    print(f"Mode: {'SIMULATION' if args.dry_run else 'REAL EXECUTION'}")
    print(f"Report: {args.report_file}")
    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

if __name__ == "__main__":
    main()

# End of extracted content
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧


# End of extracted content
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
