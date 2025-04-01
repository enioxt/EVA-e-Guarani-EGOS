#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fix Encoding - Script to fix encoding issues in documentation files
This script ensures all files are properly encoded in UTF-8.

Version: 1.0.0
Date: 2025-03-20
"""

import os
import sys
import chardet
from pathlib import Path
import logging
import shutil
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("fix_encoding.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Create timestamp for backups
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT_DIR / "backup" / "encoding_fix" / TIMESTAMP

def create_backup(file_path):
    """Create a backup of a file before modifying it"""
    rel_path = file_path.relative_to(ROOT_DIR)
    backup_path = BACKUP_DIR / rel_path
    
    # Create parent directories
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy the file
    shutil.copy2(file_path, backup_path)
    logging.info(f"Created backup of {rel_path}")

def fix_file_encoding(file_path):
    """Fix the encoding of a single file"""
    try:
        # Read the file in binary mode
        with open(file_path, 'rb') as f:
            raw_content = f.read()
        
        # Detect the encoding
        result = chardet.detect(raw_content)
        encoding = result['encoding']
        
        if not encoding:
            logging.warning(f"Could not detect encoding for {file_path}")
            return False
        
        # Try to decode with detected encoding
        try:
            content = raw_content.decode(encoding)
        except UnicodeDecodeError:
            logging.warning(f"Failed to decode {file_path} with detected encoding {encoding}")
            return False
        
        # Create backup
        create_backup(file_path)
        
        # Write back in UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logging.info(f"Successfully fixed encoding of {file_path} (was: {encoding})")
        return True
        
    except Exception as e:
        logging.error(f"Error processing {file_path}: {str(e)}")
        return False

def fix_directory_encoding(directory):
    """Fix encoding for all files in a directory and its subdirectories"""
    success_count = 0
    failed_files = []
    
    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in ['.md', '.txt', '.py']:
            if fix_file_encoding(file_path):
                success_count += 1
            else:
                failed_files.append(file_path)
    
    return success_count, failed_files

def generate_report(success_count, failed_files):
    """Generate a report of the encoding fix process"""
    report_dir = ROOT_DIR / "docs" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"encoding_fix_report_{TIMESTAMP}.md"
    
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Encoding Fix Report\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Successfully fixed**: {success_count}\n")
            f.write(f"- **Failed**: {len(failed_files)}\n")
            f.write(f"- **Backup location**: `{BACKUP_DIR}`\n\n")
            
            if failed_files:
                f.write("## Failed Files\n\n")
                for file_path in failed_files:
                    f.write(f"- `{file_path.relative_to(ROOT_DIR)}`\n")
                f.write("\n")
            
            f.write("## Next Steps\n\n")
            f.write("1. Verify that all fixed files are readable\n")
            f.write("2. Check failed files manually\n")
            f.write("3. Run the English migration script again\n\n")
            
            f.write("---\n\n")
            f.write("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")
        
        logging.info(f"Report generated at {report_path}")
        return report_path
    
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        return None

def main():
    """Main execution function"""
    logging.info("=== STARTING ENCODING FIX PROCESS ===")
    
    try:
        # Fix encoding in docs directory
        docs_dir = ROOT_DIR / "docs"
        success_count, failed_files = fix_directory_encoding(docs_dir)
        
        # Generate report
        report_path = generate_report(success_count, failed_files)
        
        logging.info("=== ENCODING FIX PROCESS COMPLETED ===")
        if report_path:
            logging.info(f"Report available at: {report_path}")
        
    except Exception as e:
        logging.error(f"Error during encoding fix: {str(e)}")
        logging.info("=== ENCODING FIX PROCESS FAILED ===")

if __name__ == "__main__":
    main() 