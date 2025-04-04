#!/usr/bin/env python3
"""
EVA & GUARANI - CRONOS Evolutionary Preservation
-----------------------------------------------
This module implements the CRONOS subsystem for evolutionary preservation
in the EVA & GUARANI BIOS-Q ecosystem.

Version: 7.5
Created: 2025-03-26
"""

import os
import sys
import logging
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from ..logging import get_logger

logger = get_logger(__name__)


class CRONOSManager:
    """Main manager for the CRONOS evolutionary preservation subsystem."""

    def __init__(self, config=None):
        """Initialize the CRONOS manager.

        Args:
            config: Optional system configuration
        """
        self.config = config
        self.state_preservation = None

        try:
            # Try to import state preservation module
            from .state_preservation import StatePreservationManager

            self.state_preservation = StatePreservationManager(config)
            logger.info("CRONOS state preservation system initialized")
        except Exception as e:
            logger.error(f"Error initializing state preservation system: {e}")

    def save_system_state(self, state_name: str, description: str = "") -> Optional[str]:
        """Save the current system state.

        Args:
            state_name: Name of the state
            description: Optional description of the state

        Returns:
            The ID of the saved state, or None if the operation fails
        """
        if not self.state_preservation:
            logger.error("State preservation system not available")
            return None

        try:
            return self.state_preservation.save_system_state(state_name, description)
        except Exception as e:
            logger.error(f"Error saving system state: {e}")
            return None

    def restore_system_state(self, state_id: str) -> bool:
        """Restore the system to a previous state.

        Args:
            state_id: The ID of the state to restore

        Returns:
            True if the state was restored successfully, False otherwise
        """
        if not self.state_preservation:
            logger.error("State preservation system not available")
            return False

        try:
            return self.state_preservation.restore_system_state(state_id)
        except Exception as e:
            logger.error(f"Error restoring system state: {e}")
            return False

    def list_states(self) -> List[Dict[str, Any]]:
        """Get a list of available system states.

        Returns:
            A list of system states
        """
        if not self.state_preservation:
            logger.error("State preservation system not available")
            return []

        try:
            return self.state_preservation.get_system_states()
        except Exception as e:
            logger.error(f"Error listing system states: {e}")
            return []

    def analyze_changes(self) -> Dict[str, Any]:
        """Analyze changes in critical files since the last state.

        Returns:
            A dictionary with information about changes
        """
        if not self.state_preservation:
            logger.error("State preservation system not available")
            return {"changes_detected": False, "message": "State preservation system not available"}

        try:
            return self.state_preservation.analyze_changes()
        except Exception as e:
            logger.error(f"Error analyzing changes: {e}")
            return {"changes_detected": False, "message": f"Error analyzing changes: {e}"}

    def create_snapshot(self, name: Optional[str] = None) -> Optional[str]:
        """Create a full system snapshot with optional name.

        Args:
            name: Optional name for the snapshot

        Returns:
            The ID of the snapshot, or None if the operation fails
        """
        if not self.state_preservation:
            logger.error("State preservation system not available")
            return None

        try:
            return self.state_preservation.create_system_snapshot(name)
        except Exception as e:
            logger.error(f"Error creating system snapshot: {e}")
            return None


# Convenience function to directly access state preservation
def save_system_state(state_name: str, description: str = "", config=None) -> Optional[str]:
    """Save the current system state.

    Args:
        state_name: Name of the state
        description: Optional description of the state
        config: Optional system configuration

    Returns:
        The ID of the saved state, or None if the operation fails
    """
    manager = CRONOSManager(config)
    return manager.save_system_state(state_name, description)


def restore_system_state(state_id: str, config=None) -> bool:
    """Restore the system to a previous state.

    Args:
        state_id: The ID of the state to restore
        config: Optional system configuration

    Returns:
        True if the state was restored successfully, False otherwise
    """
    manager = CRONOSManager(config)
    return manager.restore_system_state(state_id)


def create_snapshot(name: Optional[str] = None, config=None) -> Optional[str]:
    """Create a full system snapshot with optional name.

    Args:
        name: Optional name for the snapshot
        config: Optional system configuration

    Returns:
        The ID of the snapshot, or None if the operation fails
    """
    manager = CRONOSManager(config)
    return manager.create_snapshot(name)


def analyze_changes(config=None) -> Dict[str, Any]:
    """Analyze changes in critical files since the last state.

    Args:
        config: Optional system configuration

    Returns:
        A dictionary with information about changes
    """
    manager = CRONOSManager(config)
    return manager.analyze_changes()


# Create a simple CLI for testing the module directly
def main():
    """Run the CRONOS module as a standalone script."""
    import argparse

    try:
        # Try to import the Config class dynamically
        from ..config import Config

        config = Config()
        config.load_config()
    except Exception:
        config = None

    parser = argparse.ArgumentParser(description="EVA & GUARANI CRONOS Preservation System")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Save state command
    save_parser = subparsers.add_parser("save", help="Save the current system state")
    save_parser.add_argument("name", help="Name of the state")
    save_parser.add_argument("--description", "-d", help="Description of the state")

    # Restore state command
    restore_parser = subparsers.add_parser("restore", help="Restore a system state")
    restore_parser.add_argument("state_id", help="ID of the state to restore")

    # List states command
    subparsers.add_parser("list", help="List available system states")

    # Analyze changes command
    subparsers.add_parser("analyze", help="Analyze changes since the last state")

    # Create snapshot command
    snapshot_parser = subparsers.add_parser("snapshot", help="Create a full system snapshot")
    snapshot_parser.add_argument("--name", "-n", help="Name of the snapshot")

    args = parser.parse_args()

    # Create manager
    manager = CRONOSManager(config)

    # Execute appropriate command
    if args.command == "save":
        state_id = manager.save_system_state(args.name, args.description or "")
        if state_id:
            print(f"✅ System state saved with ID: {state_id}")
            print(f"Name: {args.name}")
            if args.description:
                print(f"Description: {args.description}")
        else:
            print("❌ Failed to save system state")

    elif args.command == "restore":
        success = manager.restore_system_state(args.state_id)
        if success:
            print(f"✅ System state {args.state_id} restored successfully")
        else:
            print(f"❌ Failed to restore system state {args.state_id}")

    elif args.command == "list":
        states = manager.list_states()
        if not states:
            print("No system states found.")
            return

        print(f"📋 Available System States ({len(states)}):")
        print("-" * 80)

        for i, state in enumerate(states):
            from datetime import datetime

            # Parse timestamp for display
            try:
                timestamp = datetime.fromisoformat(state["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            except:
                timestamp = state["timestamp"]

            print(f"{i+1}. {state['name']} ({state['id']})")
            print(f"   Created: {timestamp}")
            print(f"   Files: {state.get('file_count', 'N/A')}")
            if state.get("description"):
                print(f"   Description: {state['description']}")
            print()

    elif args.command == "analyze":
        analysis = manager.analyze_changes()

        if not analysis["changes_detected"]:
            print(f"✅ No changes detected since last state.")
            print(analysis.get("message", ""))
            return

        # Show comparison state
        compared_with = analysis.get("compared_with", {})
        if compared_with:
            print(
                f"📊 Changes since state: {compared_with.get('state_name')} ({compared_with.get('state_id')})"
            )

        # Show changes
        changes = analysis.get("changes", [])
        if changes:
            print(f"\n🔄 Changes Detected ({len(changes)}):")

            modified = [c for c in changes if c["change_type"] == "modified"]
            added = [c for c in changes if c["change_type"] == "added"]
            deleted = [c for c in changes if c["change_type"] == "deleted"]

            if modified:
                print(f"\n✏️  Modified Files ({len(modified)}):")
                for change in modified:
                    print(f"  - {change['file']}")

            if added:
                print(f"\n➕ Added Files ({len(added)}):")
                for change in added:
                    print(f"  - {change['file']}")

            if deleted:
                print(f"\n❌ Deleted Files ({len(deleted)}):")
                for change in deleted:
                    print(f"  - {change['file']}")

    elif args.command == "snapshot":
        snapshot_id = manager.create_snapshot(args.name)
        if snapshot_id:
            print(f"✅ System snapshot created with ID: {snapshot_id}")
            if args.name:
                print(f"Name: {args.name}")
        else:
            print("❌ Failed to create system snapshot")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
