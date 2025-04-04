"""EVA & GUARANI - System Maintenance CLI
Version: 8.0

Command-line interface for system maintenance operations.
"""

#!/usr/bin/env python3
import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Get the absolute path to the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)  # Change to project root directory

# Add project root to Python path
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from core.metadata.system_maintenance import SystemMaintenance
except ImportError as e:
    print(f"Error importing SystemMaintenance: {str(e)}")
    print("Make sure you have installed all required dependencies:")
    print("pip install -r core/metadata/requirements.txt")
    sys.exit(1)


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp in human-readable format."""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp


def create_backup(maintenance: SystemMaintenance) -> None:
    """Create a system backup."""
    try:
        backup_path = maintenance.create_backup()
        print(f"\n✅ Backup created successfully at: {backup_path}")

        # Print manifest contents
        manifest_path = Path(backup_path) / "manifest.json"
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)
                print("\nBackup manifest:")
                print(f"  📅 Timestamp: {manifest['timestamp']}")
                print(f"  📁 Directories: {', '.join(manifest['directories'])}")
                print(f"  📄 Files: {manifest['files_count']}")
                print(f"  💾 Total size: {format_size(manifest['total_size'])}")
    except Exception as e:
        print(f"\n❌ Failed to create backup: {str(e)}", file=sys.stderr)
        sys.exit(1)


def cleanup_system(maintenance: SystemMaintenance) -> None:
    """Clean up the system by identifying and quarantining files."""
    try:
        print("\n🔍 Analyzing system files...")
        results = maintenance.cleanup_system()

        # Print results
        print("\nCleanup results:")
        print(f"  🗑️  Total files quarantined: {len(results['quarantined'])}")

        if results["duplicates"]:
            print("\n📑 Duplicate files found:")
            for file in results["duplicates"]:
                print(f"  • {file}")

        if results["outdated"]:
            print("\n📅 Outdated files found:")
            for file in results["outdated"]:
                print(f"  • {file}")

        if results["quarantined"]:
            print("\n🔒 Files moved to quarantine:")
            for file in results["quarantined"]:
                print(f"  • {file}")

        print("\n✅ System cleanup completed successfully")
    except Exception as e:
        print(f"\n❌ Cleanup failed: {str(e)}", file=sys.stderr)
        sys.exit(1)


def list_quarantine(maintenance: SystemMaintenance) -> None:
    """List all files in quarantine."""
    try:
        files = maintenance.list_quarantined_files()

        if not files:
            print("\n📭 No files in quarantine")
            return

        print("\n🔒 Quarantined files:")
        for file in files:
            print(f"\n  📄 {file['path']}")
            print(f"    • Original path: {file['original_path']}")
            print(f"    • Quarantine date: {format_timestamp(file['quarantine_date'])}")
            print(f"    • Reason: {file['reason']}")
    except Exception as e:
        print(f"\n❌ Failed to list quarantine: {str(e)}", file=sys.stderr)
        sys.exit(1)


def restore_file(maintenance: SystemMaintenance, file_path: str) -> None:
    """Restore a file from quarantine."""
    try:
        if maintenance.restore_from_quarantine(file_path):
            print(f"\n✅ Successfully restored: {file_path}")
        else:
            print(f"\n❌ Failed to restore: {file_path}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Restore failed: {str(e)}", file=sys.stderr)
        sys.exit(1)


def show_stats(maintenance: SystemMaintenance) -> None:
    """Show system statistics."""
    try:
        stats = maintenance.get_system_stats()

        print("\n📊 System Statistics")
        print("\n📁 Files:")
        print(f"  • Total files: {stats['total_files']}")
        print(f"  • Total size: {format_size(stats['total_size'])}")

        print("\n📈 Recent Activity:")
        print(f"  • Last 24 hours: {stats['recent_activity']['modified_24h']} files modified")
        print(f"  • Last 7 days: {stats['recent_activity']['modified_7d']} files modified")
        print(f"  • Last 30 days: {stats['recent_activity']['modified_30d']} files modified")

        print("\n📝 File Types:")
        for ext, count in sorted(stats["file_types"].items(), key=lambda x: x[1], reverse=True):
            print(f"  • {ext or 'no extension'}: {count} files")

        print("\n🔒 Quarantine:")
        print(f"  • Files: {stats['quarantine']['total_files']}")
        print(f"  • Size: {format_size(stats['quarantine']['total_size'])}")

        print("\n💾 Backups:")
        print(f"  • Total backups: {stats['backups']['count']}")
        print(f"  • Total size: {format_size(stats['backups']['total_size'])}")
        if stats["backups"]["latest"]:
            print(f"  • Latest backup: {format_timestamp(stats['backups']['latest'])}")
    except Exception as e:
        print(f"\n❌ Failed to get stats: {str(e)}", file=sys.stderr)
        sys.exit(1)


def reorganize_root(maintenance: SystemMaintenance) -> None:
    """
    Reorganize the root directory while preserving quantum connections
    and establishing mycelial networks.
    """
    print("\n🌌 Iniciando reorganização quântica do sistema...")
    try:
        results = maintenance.reorganize_root_directory()

        if results["created_dirs"]:
            print("\n📁 Diretórios criados:")
            for dir_path in results["created_dirs"]:
                print(f"  ├── {dir_path}")

        if results["moved_files"]:
            print("\n📦 Arquivos movidos:")
            for move_info in results["moved_files"]:
                print(f"  ├── {move_info}")

        if results["mycelial_connections"]:
            print("\n🍄 Conexões miceliais estabelecidas:")
            for connection in results["mycelial_connections"]:
                print(f"  ├── {connection['source']}")
                for related in connection["connections"]:
                    print(f"  │   └── {related}")

        if results["quantum_links"]:
            print("\n⚛️ Links quânticos preservados:")
            for file_path, subsystem in results["quantum_links"].items():
                print(f"  ├── {file_path} -> {subsystem}")

        if results["errors"]:
            print("\n⚠️ Erros encontrados:")
            for error in results["errors"]:
                print(f"  ├── {error}")

        print("\n✨ Reorganização concluída com sucesso!")

    except Exception as e:
        print(f"\n❌ Erro durante a reorganização: {str(e)}")
        sys.exit(1)


def migrate_bios_q(maintenance: SystemMaintenance):
    """
    Migra o BIOS-Q para QUANTUM_PROMPTS/BIOS-Q.
    """
    print("\n🌌 Iniciando migração do BIOS-Q...")

    results = maintenance.migrate_bios_q()

    if results["success"]:
        print("\n✨ Migração do BIOS-Q concluída com sucesso!")

        if results["preserved_files"]:
            print("\n📦 Arquivos preservados em backup:")
            for file in results["preserved_files"]:
                print(f"  ├── {file}")

        print("\n📦 Arquivos migrados:")
        for file in results["files_moved"]:
            print(f"  ├── {file}")

    else:
        print("\n❌ Erro durante a migração do BIOS-Q:")
        for error in results["errors"]:
            print(f"  ├── {error}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="EVA & GUARANI System Maintenance CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s backup                     Create a system backup
  %(prog)s cleanup                    Clean up the system
  %(prog)s reorganize                Reorganize root directory
  %(prog)s quarantine list           List quarantined files
  %(prog)s quarantine restore FILE   Restore a file from quarantine
  %(prog)s stats                     Show system statistics
  %(prog)s migrate-bios-q            Migrate BIOS-Q to QUANTUM_PROMPTS
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add reorganize command
    subparsers.add_parser("reorganize", help="Reorganize root directory structure")

    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create system backup")
    backup_parser.add_argument("--compress", action="store_true", help="Enable backup compression")
    backup_parser.add_argument("--password", type=str, help="Password for backup encryption")
    backup_parser.add_argument(
        "--max-backups", type=int, default=10, help="Maximum number of backups to keep"
    )

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up the system")

    # Quarantine commands
    quarantine_parser = subparsers.add_parser("quarantine", help="Quarantine operations")
    quarantine_subparsers = quarantine_parser.add_subparsers(dest="quarantine_command")

    list_parser = quarantine_subparsers.add_parser("list", help="List quarantined files")
    restore_parser = quarantine_subparsers.add_parser(
        "restore", help="Restore file from quarantine"
    )
    restore_parser.add_argument("file", help="File to restore")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show system statistics")

    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore from backup")
    restore_parser.add_argument("backup_name", help="Name of backup to restore")
    restore_parser.add_argument("--password", type=str, help="Password for encrypted backup")

    # List backups command
    subparsers.add_parser("list-backups", help="List available backups")

    # Migrate BIOS-Q command
    migrate_parser = subparsers.add_parser(
        "migrate-bios-q", help="Migrate BIOS-Q to QUANTUM_PROMPTS"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        maintenance = SystemMaintenance(
            str(PROJECT_ROOT), max_backups=getattr(args, "max_backups", 10)
        )

        if args.command == "reorganize":
            reorganize_root(maintenance)
        elif args.command == "backup":
            backup_path = maintenance.create_backup(password=args.password, compress=args.compress)
            print(f"\n✅ Backup created successfully at: {backup_path}")

            # Print manifest details
            manifest_path = Path(backup_path) / "manifest.json"
            if manifest_path.exists():
                with open(manifest_path) as f:
                    manifest = json.load(f)
                print("\nBackup details:")
                print(f"  Timestamp: {manifest['timestamp']}")
                print(f"  Files: {manifest['files_count']}")
                print(f"  Size: {format_size(manifest['total_size'])}")
                print(f"  Compressed: {'Yes' if manifest.get('compressed', False) else 'No'}")
                print(f"  Encrypted: {'Yes' if manifest.get('encrypted', False) else 'No'}")
                print(f"  Version: {manifest.get('version', 'unknown')}")
        elif args.command == "cleanup":
            cleanup_system(maintenance)
        elif args.command == "quarantine":
            if args.quarantine_command == "list":
                list_quarantine(maintenance)
            elif args.quarantine_command == "restore":
                restore_file(maintenance, args.file)
            else:
                quarantine_parser.print_help()
                sys.exit(1)
        elif args.command == "stats":
            show_stats(maintenance)
        elif args.command == "restore":
            success = maintenance.restore_backup(args.backup_name, password=args.password)
            if success:
                print(f"\nSuccessfully restored from backup: {args.backup_name}")
            else:
                print(f"\nFailed to restore from backup: {args.backup_name}")
                sys.exit(1)
        elif args.command == "list-backups":
            backup_dir = PROJECT_ROOT / "backups"
            if not backup_dir.exists():
                print("\nNo backups found.")
                return

            print("\nAvailable backups:")
            for backup_path in backup_dir.iterdir():
                if backup_path.is_dir() and backup_path.name.startswith("system_backup_"):
                    manifest_path = backup_path / "manifest.json"
                    if manifest_path.exists():
                        with open(manifest_path) as f:
                            manifest = json.load(f)
                        print(f"\n{backup_path.name}:")
                        print(f"  Created: {manifest['timestamp']}")
                        print(f"  Files: {manifest['files_count']}")
                        print(f"  Size: {format_size(manifest['total_size'])}")
                        print(
                            f"  Compressed: {'Yes' if manifest.get('compressed', False) else 'No'}"
                        )
                        print(f"  Encrypted: {'Yes' if manifest.get('encrypted', False) else 'No'}")
                        print(f"  Version: {manifest.get('version', 'unknown')}")
                    else:
                        print(f"\n{backup_path.name}: (No manifest found)")
        elif args.command == "migrate-bios-q":
            migrate_bios_q(maintenance)

    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)
