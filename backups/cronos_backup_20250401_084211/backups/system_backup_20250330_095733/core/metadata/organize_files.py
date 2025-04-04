import os
import argparse
from datetime import datetime
from scanner import MetadataScanner
from organizer import FileOrganizer
from tracker import UsageTracker


def main():
    parser = argparse.ArgumentParser(description="Organize files using the metadata system")
    parser.add_argument("--root-dir", type=str, default=".", help="Root directory to scan")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show proposed changes without executing them"
    )
    parser.add_argument("--track-usage", action="store_true", help="Start tracking file usage")
    parser.add_argument(
        "--days", type=int, default=30, help="Number of days to look back for usage stats"
    )
    args = parser.parse_args()

    # Initialize the metadata system
    print(f"\n=== Initializing Metadata System ===")
    scanner = MetadataScanner()
    organizer = FileOrganizer(scanner)
    tracker = UsageTracker(scanner)

    # Scan the system
    print(f"\n=== Scanning System ===")
    print(f"Root directory: {args.root_dir}")
    scanner.scan_system(args.root_dir)

    # Get organization suggestions
    print(f"\n=== File Organization Analysis ===")
    moves = organizer.organize_files(dry_run=True)

    if moves:
        print(f"\nSuggested file moves ({len(moves)}):")
        for move in moves:
            print(f"\n- Move: {move['file']}")
            print(f"  To: {move['destination']}")
            print(f"  Reason: {move['reason']}")
    else:
        print("\nNo file moves suggested.")

    # Get inactive files
    inactive = scanner.get_inactive_files(days=args.days)
    if inactive:
        print(f"\nInactive files ({len(inactive)}):")
        for item in inactive:
            print(f"\n- File: {item['file']}")
            print(f"  Last accessed: {item['last_accessed']}")
            print(f"  Days inactive: {item['days_inactive']}")
            print(f"  Suggested action: {item['suggested_action']}")
    else:
        print("\nNo inactive files found.")

    # Get replacement candidates
    replacements = scanner.get_replacement_candidates()
    if replacements:
        print(f"\nReplacement candidates ({len(replacements)}):")
        for item in replacements:
            print(f"\n- Old file: {item['old_file']}")
            print(f"  New file: {item['new_file']}")
            print(f"  Reason: {item['reason']}")
    else:
        print("\nNo replacement candidates found.")

    # Generate organization report
    print(f"\n=== Organization Report ===")
    report = organizer.get_organization_report()

    print(f"\nOverview:")
    print(f"- Total files: {report['total_files']}")
    print(f"- Misplaced files: {report['misplaced_files']}")
    print(f"- Inactive files: {report['inactive_files']}")
    print(f"- Replacement candidates: {report['replacement_candidates']}")

    print(f"\nSubsystem Statistics:")
    for subsystem, stats in report["subsystem_stats"].items():
        print(f"\n{subsystem}:")
        print(f"- Total files: {stats['total_files']}")
        print(f"- Active files: {stats['active_files']}")
        print(f"- Quantum metrics:")
        for metric, value in stats["quantum_metrics"].items():
            print(f"  - {metric}: {value:.2f}")

    # Execute moves if not in dry run mode
    if not args.dry_run and moves:
        print(f"\n=== Executing File Moves ===")
        organizer.organize_files(dry_run=False)
        print("\nFile moves completed.")
        organizer.save_move_history()

    # Start usage tracking if requested
    if args.track_usage:
        print(f"\n=== Starting Usage Tracking ===")
        print("Press Ctrl+C to stop tracking")
        tracker.start_tracking(args.root_dir)


if __name__ == "__main__":
    main()
