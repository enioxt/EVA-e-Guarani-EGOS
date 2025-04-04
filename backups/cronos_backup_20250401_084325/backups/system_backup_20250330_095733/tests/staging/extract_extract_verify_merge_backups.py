#!/usr/bin/env python3
# Important content extracted from staging\extract_verify_merge_backups.py
# Original file moved to quarantine
# Date: 2025-03-22 08:45:53

# Important content extracted from tools\utilities\verify_merge_backups.py
# Original file moved to quarantine
# Date: 2025-03-22 08:37:23

python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verify Merge Backups - Script to verify merge backups
This script analyzes the backups created during reorganization to ensure no functionality was lost.

Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import shutil
import logging
import difflib
from pathlib import Path
from datetime import datetime

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Logging configuration
log_dir = ROOT_DIR / "data" / "logs" / "system"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(str(log_dir / "merge_verification.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def find_merge_backups():
    """Finds all merge backups in the system"""
    backups = []
    for path in ROOT_DIR.rglob("*_pre_merge_*"):
        if path.is_dir():
            backups.append(path)
    return backups

def analyze_backup(backup_path):
    """Analyzes a specific backup and compares it with the current version"""
    logging.info(f"\nAnalyzing backup: {backup_path.relative_to(ROOT_DIR)}")

    # Find corresponding current directory
    current_dir = backup_path.parent / backup_path.name.split("_pre_merge_")[0]

    if not current_dir.exists():
        logging.warning(f"Current directory not found: {current_dir}")
        return

    # Create report for this backup
    report_dir = ROOT_DIR / "docs" / "merge_reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / f"merge_report_{backup_path.name}.md"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# Backup Analysis Report - {backup_path.name}\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Compare file structure
        backup_files = set(p.relative_to(backup_path) for p in backup_path.rglob("*") if p.is_file())
        current_files = set(p.relative_to(current_dir) for p in current_dir.rglob("*") if p.is_file())

        # Unique files in each version
        only_in_backup = backup_files - current_files
        only_in_current = current_files - backup_files
        common_files = backup_files & current_files

        # Write results
        f.write("## Unique Files in Backup\n\n")
        for file in sorted(only_in_backup):
            f.write(f"- `{file}`\n")

        f.write("\n## Unique Files in Current Version\n\n")
        for file in sorted(only_in_current):
            f.write(f"- `{file}`\n")

        f.write("\n## Difference Analysis\n\n")
        for file in sorted(common_files):
            backup_file = backup_path / file
            current_file = current_dir / file

            if backup_file.suffix in ['.py', '.md', '.txt', '.json', '.yaml', '.yml']:
                with open(backup_file, 'r', encoding='utf-8') as bf, \
                     open(current_file, 'r', encoding='utf-8') as cf:
                    backup_content = bf.readlines()
                    current_content = cf.readlines()

                diff = list(difflib.unified_diff(
                    backup_content,
                    current_content,
                    fromfile=str(backup_file),
                    tofile=str(current_file)
                ))

                if diff:
                    f.write(f"\n### Differences in `{file}`\n\n")
                    f.write("diff\n")
                    f.writelines(diff)
                    f.write("\n")

        # Add recommendations
        f.write("\n## Recommendations\n\n")
        if only_in_backup:
            f.write("### Potentially Lost Files\n")
            f.write("The following files exist only in the backup and may need to be restored:\n\n")
            for file in sorted(only_in_backup):
                f.write(f"- [ ] Review and possibly restore: `{file}`\n")

        if only_in_current:
            f.write("\n### New Files\n")
            f.write("The following files are new and should be checked:\n\n")
            for file in sorted(only_in_current):
                f.write(f"- [ ] Check new file: `{file}`\n")

    logging.info(f"Report generated: {report_file}")
    return report_file

def create_summary_report(analyzed_backups):
    """Creates a summary report of all analyzed backups"""
    summary_file = ROOT_DIR / "docs" / "merge_reports" / "00_SUMMARY.md"

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("# Backup Analysis Summary\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Analyzed Backups\n\n")
        for backup in analyzed_backups:
            f.write(f"- [{backup.name}](merge_report_{backup.name}.md)\n")

        f.write("\n## Next Steps\n\n")
        f.write("1. Review each individual report\n")
        f.write("2. Restore important files that were lost\n")
        f.write("3. Verify functionality of merged modules\n")
        f.write("4. Update documentation as needed\n")

        f.write("\n## Verification Checklist\n\n")
        f.write("- [ ] All reports have been reviewed\n")
        f.write("- [ ] Important files have been restored\n")
        f.write("- [ ] Tests have been run on affected modules\n")
        f.write("- [ ] Documentation has been updated\n")

def main():
    """Main function"""
    logging.info("=== STARTING MERGE BACKUP VERIFICATION ===")

    try:
        # Find all backups
        backups = find_merge_backups()
        logging.info(f"Found {len(backups)} backups for analysis")

        # Analyze each backup
        analyzed = []
        for backup in backups:
            report = analyze_backup(backup)
            if report:
                analyzed.append(backup)

        # Create summary report
        if analyzed:
            create_summary_report(analyzed)
            logging.info(f"Analysis complete. {len(analyzed)} backups processed")
        else:
            logging.warning("No backup was successfully analyzed")

        logging.info("=== MERGE BACKUP VERIFICATION COMPLETED ===")

    except Exception as e:
        logging.error(f"Error during backup verification: {str(e)}")
        logging.info("=== MERGE BACKUP VERIFICATION INTERRUPTED WITH ERRORS ===")

if __name__ == "__main__":
    main()

# End of extracted content
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧


# End of extracted content
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
