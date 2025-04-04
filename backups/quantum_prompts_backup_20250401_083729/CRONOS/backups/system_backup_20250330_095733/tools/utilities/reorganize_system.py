#!/usr/bin/env python3
python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Structural Reorganization System (ATLAS)
==========================================================

This script implements the reorganization of the directory structure of the
EVA & GUARANI system, following best practices for organization and modularity,
preserving system integrity while optimizing its architecture.

Author: EVA & GUARANI
Version: 1.0
"""

import os
import sys
import shutil
import datetime
import argparse
import json
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
    parser = argparse.ArgumentParser(description='EVA & GUARANI - Structural Reorganization')

    parser.add_argument('--dry-run', action='store_true',
                        help='Runs in simulation mode without moving files')

    parser.add_argument('--backup-dir', type=str, default='./backup_before_reorganization',
                        help='Directory for backup before reorganization')

    parser.add_argument('--report-dir', type=str, default='./reports',
                        help='Directory to save reports')

    parser.add_argument('--category', type=str, default='all',
                        help='Specific category to reorganize (all, core, integrations, etc)')

    return parser.parse_args()

def create_directory_structure(root_path, dry_run=True):
    """
    Creates the optimized directory structure

    Args:
        root_path (str): System root path
        dry_run (bool): If True, only simulates the operation

    Returns:
        list: List of created directories
    """
    log_event(f"{'[SIMULATION] ' if dry_run else ''}Creating optimized directory structure")

    # Define the new directory structure
    directory_structure = {
        'core': [
            'egos',
            'atlas',
            'nexus',
            'cronos',
            'ethik'
        ],
        'integrations': [
            'bots',
            'apis',
            'platforms',
            'services'
        ],
        'modules': [
            'quantum',
            'visualization',
            'analysis',
            'preservation',
            'customization'
        ],
        'tools': [
            'scripts',
            'utilities',
            'maintenance',
            'deployment'
        ],
        'docs': [
            'architecture',
            'user_guides',
            'developer_guides',
            'api_references',
            'tutorials'
        ],
        'tests': [
            'unit',
            'integration',
            'performance',
            'security'
        ],
        'ui': [
            'components',
            'assets',
            'themes',
            'layouts'
        ],
        'data': [
            'samples',
            'models',
            'schemas',
            'exports'
        ]
    }

    created_dirs = []

    # Create each directory in the structure
    for category, subdirs in directory_structure.items():
        # Create main category directory
        category_path = os.path.join(root_path, category)

        if not dry_run:
            os.makedirs(category_path, exist_ok=True)

        created_dirs.append(category_path)

        # Create subdirectories
        for subdir in subdirs:
            subdir_path = os.path.join(category_path, subdir)

            if not dry_run:
                os.makedirs(subdir_path, exist_ok=True)

            created_dirs.append(subdir_path)

            # Add README.md file in each subdirectory
            readme_path = os.path.join(subdir_path, 'README.md')
            if not dry_run:
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(f"# EVA & GUARANI - {category.capitalize()}/{subdir.capitalize()}\n\n")
                    f.write(f"This directory contains the {subdir} components of the {category} subsystem.\n\n")
                    f.write("## Purpose\n\n")
                    f.write(f"Implement {subdir} functionalities in a modular and well-documented manner.\n\n")
                    f.write("## Components\n\n")
                    f.write("*Add specific components of this module here*\n\n")
                    f.write("---\n\n")
                    f.write("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

    log_event(f"{'[SIMULATION] ' if dry_run else ''}Created {len(created_dirs)} directories in the new structure")
    return created_dirs

def backup_current_structure(root_path, backup_dir, dry_run=True):
    """
    Performs backup of the current structure before reorganization

    Args:
        root_path (str): System root path
        backup_dir (str): Backup directory
        dry_run (bool): If True, only simulates the operation

    Returns:
        bool: True if the backup was successful
    """
    log_event(f"{'[SIMULATION] ' if dry_run else ''}Starting backup of the current structure in: {backup_dir}")

    # Directories to be ignored in the backup
    ignore_dirs = [
        '.git', '.github', '.vscode', '.obsidian', '.cursor',
        'venv', '__pycache__', 'node_modules',
        'quarantine', 'quarantine_duplicates', 'backup',
        os.path.basename(backup_dir)
    ]

    # Add any folder that starts with quarantine or backup
    for d in os.listdir(root_path):
        dir_path = os.path.join(root_path, d)
        if os.path.isdir(dir_path) and (d.startswith('quarantine') or d.startswith('backup')):
            ignore_dirs.append(d)

    # Create backup directory
    if not dry_run:
        os.makedirs(backup_dir, exist_ok=True)

    # Helper function to ignore directories
    def ignore_function(dir, files):
        return [f for f in files if f in ignore_dirs or os.path.basename(dir) in ignore_dirs]

    # Perform backup
    try:
        if not dry_run:
            # Create backup metadata file
            metadata = {
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'root_path': root_path,
                'backup_path': backup_dir,
                'description': 'Backup before structural reorganization of the EVA & GUARANI system'
            }

            metadata_file = os.path.join(backup_dir, 'backup_metadata.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            # Copy files (except ignored ones)
            for item in os.listdir(root_path):
                src_path = os.path.join(root_path, item)
                dst_path = os.path.join(backup_dir, item)

                if os.path.isdir(src_path):
                    if item not in ignore_dirs:
                        shutil.copytree(src_path, dst_path, ignore=ignore_function)
                else:
                    shutil.copy2(src_path, dst_path)

        log_event(f"{'[SIMULATION] ' if dry_run else ''}Backup completed successfully")
        return True
    except Exception as e:
        log_event(f"Error performing backup: {e}", 'ERROR')
        return False

def identify_file_category(file_path, file_name):
    """
    Identifies the appropriate category for a file based on its name and path

    Args:
        file_path (str): File path
        file_name (str): File name

    Returns:
        dict: Category and subcategory information
    """
    # Define patterns for classification
    patterns = {
        'core/egos': ['egos_', 'core_', 'main_', 'system_'],
        'core/atlas': ['atlas_', 'map_', 'visual_', 'cartogra'],
        'core/nexus': ['nexus_', 'module_', 'component_', 'analyser_'],
        'core/cronos': ['cronos_', 'backup_', 'version_', 'history_'],
        'core/ethik': ['ethik_', 'ethics_', 'moral_', 'ethical_'],

        'integrations/bots': ['bot_', 'telegram_', 'discord_', 'chat_'],
        'integrations/apis': ['api_', 'rest_', 'graphql_', 'endpoint_'],
        'integrations/platforms': ['platform_', 'integrate_', 'connect_'],
        'integrations/services': ['service_', 'cloud_', 'saas_', 'online_'],

        'modules/quantum': ['quantum_', 'prompt_', 'gpt_', 'llm_', 'ai_'],
        'modules/visualization': ['vis_', 'chart_', 'graph_', 'plot_', 'diagram_'],
        'modules/analysis': ['analys_', 'statistic_', 'data_', 'metric_'],
        'modules/preservation': ['preserv_', 'save_', 'archiv_', 'storage_'],
        'modules/customization': ['custom_', 'config_', 'setting_', 'prefer_'],

        'tools/scripts': ['script_', 'run_', 'auto_', 'batch_'],
        'tools/utilities': ['util_', 'helper_', 'tool_', 'assist_'],
        'tools/maintenance': ['maint_', 'clean_', 'fix_', 'repair_'],
        'tools/deployment': ['deploy_', 'release_', 'publish_', 'distrib_'],

        'docs': ['README', 'document', 'guide', 'manual', '.md', '.rst', '.txt'],
        'tests': ['test_', 'spec_', 'benchmark_', '.test.', '.spec.', 'pytest'],
        'ui': ['.html', '.css', '.scss', '.jsx', '.tsx', 'component', 'layout', 'theme'],
        'data': ['.json', '.csv', '.xml', '.yaml', '.yml', 'data_', 'model_']
    }

    # Check extension
    _, ext = os.path.splitext(file_name.lower())

    # Initial match based on extension
    initial_category = None

    if ext in ['.py', '.js', '.ts']:
        # Code files - need deeper analysis
        pass
    elif ext in ['.md', '.rst', '.txt']:
        initial_category = 'docs'
    elif ext in ['.html', '.css', '.scss', '.less', '.jsx', '.tsx']:
        initial_category = 'ui'
    elif ext in ['.json', '.csv', '.xml', '.yaml', '.yml', '.db', '.sqlite']:
        initial_category = 'data'
    elif file_name.startswith('test_') or '.test.' in file_name:
        initial_category = 'tests'

    # Check specific patterns
    for category, pattern_list in patterns.items():
        file_name_lower = file_name.lower()
        for pattern in pattern_list:
            if pattern.lower() in file_name_lower:
                # If we already have an initial match, check which is more specific
                if initial_category and '/' not in initial_category:
                    # Specific pattern takes precedence
                    parts = category.split('/')
                    return {
                        'main_category': parts[0],
                        'subcategory': parts[1] if len(parts) > 1 else None
                    }
                else:
                    parts = category.split('/')
                    return {
                        'main_category': parts[0],
                        'subcategory': parts[1] if len(parts) > 1 else None
                    }

    # If no specific pattern found but has initial match
    if initial_category:
        if '/' in initial_category:
            parts = initial_category.split('/')
            return {
                'main_category': parts[0],
                'subcategory': parts[1]
            }
        else:
            # For main categories, use default subcategories
            defaults = {
                'docs': 'developer_guides',
                'tests': 'unit',
                'ui': 'components',
                'data': 'samples'
            }
            return {
                'main_category': initial_category,
                'subcategory': defaults.get(initial_category)
            }

    # If unable to classify, place in "tools/utilities"
    return {
        'main_category': 'tools',
        'subcategory': 'utilities'
    }

def reorganize_files(root_path, dry_run=True, category_filter='all'):
    """
    Reorganizes the system files into the new directory structure

    Args:
        root_path (str): System root path
        dry_run (bool): If True, only simulates the operation
        category_filter (str): Specific category to reorganize

    Returns:
        dict: Reorganization statistics
    """
    log_event(f"{'[SIMULATION] ' if dry_run else ''}Starting file reorganization")

    # Directories to ignore
    ignore_dirs = [
        '.git', '.github', '.vscode', '.obsidian', '.cursor',
        'venv', '__pycache__', 'node_modules',
        'quarantine', 'backup', 'reports'
    ]

    # Add any folder that starts with quarantine or backup
    for d in os.listdir(root_path):
        dir_path = os.path.join(root_path, d)
        if os.path.isdir(dir_path) and (d.startswith('quarantine') or d.startswith('backup')):
            ignore_dirs.append(d)

    # Add the new structure folders
    new_structure = ['core', 'integrations', 'modules', 'tools', 'docs', 'tests', 'ui', 'data']
    ignore_dirs.extend(new_structure)

    # Statistics
    stats = {
        'total_files': 0,
        'moved_files': 0,
        'skipped_files': 0,
        'errors': 0,
        'by_category': {}
    }

    # Mapping of moved files for logging
    moved_files = []

    # Traverse all files
    for root, dirs, files in os.walk(root_path):
        # Filter ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not any(root.startswith(os.path.join(root_path, ign)) for ign in ignore_dirs)]

        for file in files:
            stats['total_files'] += 1
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_path)

            # Identify appropriate category
            category_info = identify_file_category(file_path, file)
            main_category = category_info['main_category']
            subcategory = category_info['subcategory']

            # Check category filter
            if category_filter != 'all' and main_category != category_filter:
                stats['skipped_files'] += 1
                continue

            # Update statistics by category
            category_key = f"{main_category}/{subcategory}" if subcategory else main_category
            stats['by_category'][category_key] = stats['by_category'].get(category_key, 0) + 1

            # Define destination path
            if subcategory:
                dest_dir = os.path.join(root_path, main_category, subcategory)
            else:
                dest_dir = os.path.join(root_path, main_category)

            dest_path = os.path.join(dest_dir, file)

            # If destination path is the same as source, skip
            if os.path.abspath(file_path) == os.path.abspath(dest_path):
                stats['skipped_files'] += 1
                continue

            try:
                # Create directory if it doesn't exist
                if not dry_run:
                    os.makedirs(dest_dir, exist_ok=True)

                # Check if file already exists at destination
                if os.path.exists(dest_path):
                    # Add numeric suffix
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(os.path.join(dest_dir, f"{base}_{counter}{ext}")):
                        counter += 1

                    dest_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")

                # Move file
                if not dry_run:
                    shutil.move(file_path, dest_path)

                # Log movement
                moved_files.append({
                    'source': rel_path,
                    'destination': os.path.relpath(dest_path, root_path),
                    'category': main_category,
                    'subcategory': subcategory
                })

                stats['moved_files'] += 1

                # Progress log every 50 files
                if stats['moved_files'] % 50 == 0:
                    log_event(f"{'[SIMULATION] ' if dry_run else ''}Moved {stats['moved_files']} files...")

            except Exception as e:
                error_msg = f"Error moving {rel_path}: {e}"
                log_event(error_msg, 'ERROR')
                stats['errors'] += 1

    log_event(f"{'[SIMULATION] ' if dry_run else ''}Reorganization completed: {stats['moved_files']} files moved, {stats['skipped_files']} skipped, {stats['errors']} errors")

    return stats, moved_files

def generate_report(stats, moved_files, report_dir, dry_run=True):
    """
    Generates a detailed reorganization report

    Args:
        stats (dict): Reorganization statistics
        moved_files (list): List of moved files
        report_dir (str): Directory to save reports
        dry_run (bool): If it was a simulation run

    Returns:
        tuple: Paths of the report files (json, md)
    """
    log_event(f"Generating {'simulation ' if dry_run else ''}reorganization report")

    # Create report directory if it doesn't exist
    os.makedirs(report_dir, exist_ok=True)

    # Prepare full report
    report_data = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'mode': 'DRY-RUN' if dry_run else 'EXECUTION',
        'statistics': stats,
        'moved_files': moved_files
    }

    # Report file names
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    json_report = os.path.join(report_dir, f"reorganization_report_{timestamp}.json")
    md_report = os.path.join(report_dir, f"reorganization_report_{timestamp}.md")

    # Save JSON report
    with open(json_report, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    # Create Markdown report
    md_content = f"""# Structural Reorganization Report
*Generated on: {report_data['timestamp']}*

## 📊 Operation Statistics

- **Execution Mode:** {report_data['mode']}
- **Total Files Analyzed
