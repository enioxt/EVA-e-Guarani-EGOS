#!/usr/bin/env python3
"""
EVA & GUARANI - State Preservation Module
-----------------------------------------
This module implements comprehensive state preservation functionality
for the EVA & GUARANI BIOS-Q system, allowing the system to save and
restore its state across multiple source files.

Version: 7.5
Created: 2025-03-26
"""

import os
import sys
import json
import time
import shutil
import logging
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple

from ..logging import get_logger
from ..config import Config
from ..utils import generate_id, ensure_directory, load_json, save_json, format_timestamp

logger = get_logger(__name__)

class StatePreservationManager:
    """Manager for state preservation operations in the CRONOS subsystem."""
    
    def __init__(self, config: Config):
        """Initialize the state preservation manager.
        
        Args:
            config: The system configuration
        """
        self.config = config
        
        # Set up paths
        self.project_root = Path(os.getcwd()).resolve()
        self.storage_dir = self.project_root / "storage" / "states"
        self.snapshot_dir = self.storage_dir / "snapshots"
        self.index_file = self.storage_dir / "state_index.json"
        
        # Create directories
        ensure_directory(self.storage_dir)
        ensure_directory(self.snapshot_dir)
        
        # Load state index
        self.state_index = self._load_state_index()
        
        # Critical files to track
        self.critical_files = [
            # Main documentation files
            "BIOS-Q/docs/platform_integration.md",
            "QUANTUM_PROMPTS/MASTER/quantum_context.md",
            "BIOS-Q/README.md",
            
            # Configuration files
            "BIOS-Q/system_flags.toml",
            "BIOS-Q/hardware_map.json",
            "BIOS-Q/bootloader.cfg",
            
            # Code files
            "BIOS-Q/dynamic_roadmap.py",
            "BIOS-Q/init_bios_q.py",
            "BIOS-Q/context_boot_sequence.py"
        ]
        
        # Subsystem directories
        self.subsystem_dirs = [
            "QUANTUM_PROMPTS/CRONOS",
            "QUANTUM_PROMPTS/ATLAS",
            "QUANTUM_PROMPTS/NEXUS", 
            "QUANTUM_PROMPTS/ETHIK"
        ]
        
        # Platform interface files
        self.platform_files = [
            "BIOS-Q/bios_q/interfaces/web_app.py",
            "BIOS-Q/bios_q/interfaces/telegram_bot.py",
            "BIOS-Q/bios_q/web/static/index.html"
        ]
    
    def _load_state_index(self) -> Dict[str, Any]:
        """Load the state index from disk.
        
        Returns:
            The state index
        """
        if not self.index_file.exists():
            return {
                "states": [],
                "last_updated": format_timestamp(),
                "version": "7.5"
            }
        
        try:
            return load_json(self.index_file)
        except Exception as e:
            logger.error(f"Error loading state index: {e}")
            return {
                "states": [],
                "last_updated": format_timestamp(),
                "version": "7.5"
            }
    
    def _save_state_index(self) -> None:
        """Save the state index to disk."""
        try:
            self.state_index["last_updated"] = format_timestamp()
            save_json(self.index_file, self.state_index)
        except Exception as e:
            logger.error(f"Error saving state index: {e}")
    
    def _create_file_hash(self, file_path: Path) -> Optional[str]:
        """Create a hash of a file to detect changes.
        
        Args:
            file_path: The path to the file
            
        Returns:
            The hash of the file, or None if the file doesn't exist
        """
        if not file_path.exists():
            return None
            
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error creating hash for {file_path}: {e}")
            return None
    
    def save_system_state(self, state_name: str, description: str = "") -> str:
        """Save the current system state.
        
        Args:
            state_name: Name of the state
            description: Optional description of the state
            
        Returns:
            The ID of the saved state
        """
        # Generate unique ID for this state
        state_id = generate_id("state-")
        timestamp = datetime.now().isoformat()
        
        # Create state directory
        state_dir = self.snapshot_dir / state_id
        ensure_directory(state_dir)
        
        # Track which files were preserved
        preserved_files = []
        preserved_stats = {
            "total_files": 0,
            "preserved_files": 0,
            "total_size": 0
        }
        
        # Preserve critical files
        for file_path in self.critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                # Create directory structure in snapshot
                rel_dir = os.path.dirname(file_path)
                target_dir = state_dir / rel_dir
                ensure_directory(target_dir)
                
                # Copy file
                target_path = state_dir / file_path
                try:
                    shutil.copy2(full_path, target_path)
                    preserved_files.append(file_path)
                    preserved_stats["preserved_files"] += 1
                    preserved_stats["total_size"] += os.path.getsize(full_path)
                except Exception as e:
                    logger.error(f"Error preserving {file_path}: {e}")
            
            preserved_stats["total_files"] += 1
        
        # Preserve platform interface files
        for file_path in self.platform_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                # Create directory structure in snapshot
                rel_dir = os.path.dirname(file_path)
                target_dir = state_dir / rel_dir
                ensure_directory(target_dir)
                
                # Copy file
                target_path = state_dir / file_path
                try:
                    shutil.copy2(full_path, target_path)
                    preserved_files.append(file_path)
                    preserved_stats["preserved_files"] += 1
                    preserved_stats["total_size"] += os.path.getsize(full_path)
                except Exception as e:
                    logger.error(f"Error preserving {file_path}: {e}")
            
            preserved_stats["total_files"] += 1
        
        # Create state metadata
        state_metadata = {
            "id": state_id,
            "name": state_name,
            "description": description,
            "timestamp": timestamp,
            "version": "7.5",
            "preserved_files": preserved_files,
            "stats": preserved_stats
        }
        
        # Save state metadata
        state_metadata_file = state_dir / "metadata.json"
        save_json(state_metadata_file, state_metadata)
        
        # Update state index
        self.state_index["states"].append({
            "id": state_id,
            "name": state_name,
            "description": description,
            "timestamp": timestamp,
            "file_count": preserved_stats["preserved_files"],
            "size": preserved_stats["total_size"]
        })
        
        # Sort states by timestamp
        self.state_index["states"].sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Save state index
        self._save_state_index()
        
        logger.info(f"Saved system state '{state_name}' with ID {state_id}")
        return state_id
    
    def restore_system_state(self, state_id: str) -> bool:
        """Restore the system to a previous state.
        
        Args:
            state_id: The ID of the state to restore
            
        Returns:
            True if the state was restored successfully, False otherwise
        """
        # Find state in index
        state_info = next((s for s in self.state_index["states"] if s["id"] == state_id), None)
        if not state_info:
            logger.error(f"State with ID {state_id} not found")
            return False
        
        # Check if state directory exists
        state_dir = self.snapshot_dir / state_id
        if not state_dir.exists():
            logger.error(f"State directory {state_dir} does not exist")
            return False
        
        # Load state metadata
        metadata_file = state_dir / "metadata.json"
        if not metadata_file.exists():
            logger.error(f"State metadata file {metadata_file} does not exist")
            return False
        
        try:
            metadata = load_json(metadata_file)
        except Exception as e:
            logger.error(f"Error loading state metadata: {e}")
            return False
        
        # Restore files
        restored_files = 0
        for file_path in metadata["preserved_files"]:
            source_path = state_dir / file_path
            target_path = self.project_root / file_path
            
            if not source_path.exists():
                logger.warning(f"Source file {source_path} does not exist in state snapshot")
                continue
            
            # Create directory if it doesn't exist
            target_dir = os.path.dirname(target_path)
            ensure_directory(Path(target_dir))
            
            # Copy file
            try:
                shutil.copy2(source_path, target_path)
                restored_files += 1
            except Exception as e:
                logger.error(f"Error restoring {file_path}: {e}")
        
        logger.info(f"Restored {restored_files} files from state '{state_info['name']}' ({state_id})")
        return True
    
    def get_system_states(self) -> List[Dict[str, Any]]:
        """Get a list of available system states.
        
        Returns:
            A list of system states
        """
        return self.state_index["states"]
    
    def get_state_info(self, state_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific system state.
        
        Args:
            state_id: The ID of the state
            
        Returns:
            The state information, or None if the state doesn't exist
        """
        # Find state in index
        state_info = next((s for s in self.state_index["states"] if s["id"] == state_id), None)
        if not state_info:
            logger.error(f"State with ID {state_id} not found")
            return None
        
        # Load state metadata
        metadata_file = self.snapshot_dir / state_id / "metadata.json"
        if not metadata_file.exists():
            logger.error(f"State metadata file {metadata_file} does not exist")
            return None
        
        try:
            return load_json(metadata_file)
        except Exception as e:
            logger.error(f"Error loading state metadata: {e}")
            return None
    
    def delete_system_state(self, state_id: str) -> bool:
        """Delete a system state.
        
        Args:
            state_id: The ID of the state to delete
            
        Returns:
            True if the state was deleted successfully, False otherwise
        """
        # Find state in index
        state_index = next((i for i, s in enumerate(self.state_index["states"]) if s["id"] == state_id), -1)
        if state_index == -1:
            logger.error(f"State with ID {state_id} not found")
            return False
        
        # Remove state from index
        self.state_index["states"].pop(state_index)
        
        # Delete state directory
        state_dir = self.snapshot_dir / state_id
        if state_dir.exists():
            try:
                shutil.rmtree(state_dir)
            except Exception as e:
                logger.error(f"Error deleting state directory {state_dir}: {e}")
                return False
        
        # Save state index
        self._save_state_index()
        
        logger.info(f"Deleted system state with ID {state_id}")
        return True
    
    def analyze_changes(self) -> Dict[str, Any]:
        """Analyze changes in critical files since the last state.
        
        Returns:
            A dictionary with information about changes
        """
        # Get the most recent state
        if not self.state_index["states"]:
            return {
                "changes_detected": False,
                "message": "No previous states found to compare with"
            }
        
        most_recent_state = self.state_index["states"][0]
        state_id = most_recent_state["id"]
        state_dir = self.snapshot_dir / state_id
        
        if not state_dir.exists():
            return {
                "changes_detected": False,
                "message": f"State directory {state_dir} does not exist"
            }
        
        # Load state metadata
        metadata_file = state_dir / "metadata.json"
        if not metadata_file.exists():
            return {
                "changes_detected": False,
                "message": f"State metadata file {metadata_file} does not exist"
            }
        
        try:
            metadata = load_json(metadata_file)
        except Exception as e:
            logger.error(f"Error loading state metadata: {e}")
            return {
                "changes_detected": False,
                "message": f"Error loading state metadata: {e}"
            }
        
        # Check for changes in critical files
        changes = []
        for file_path in self.critical_files + self.platform_files:
            if file_path in metadata["preserved_files"]:
                # Calculate current hash
                current_file = self.project_root / file_path
                current_hash = self._create_file_hash(current_file)
                
                # Calculate preserved hash
                preserved_file = state_dir / file_path
                preserved_hash = self._create_file_hash(preserved_file)
                
                if current_hash and preserved_hash and current_hash != preserved_hash:
                    changes.append({
                        "file": file_path,
                        "change_type": "modified"
                    })
            else:
                # Check if file exists now
                current_file = self.project_root / file_path
                if current_file.exists():
                    changes.append({
                        "file": file_path,
                        "change_type": "added"
                    })
        
        # Check for deleted files
        for file_path in metadata["preserved_files"]:
            current_file = self.project_root / file_path
            if not current_file.exists():
                changes.append({
                    "file": file_path,
                    "change_type": "deleted"
                })
        
        return {
            "changes_detected": len(changes) > 0,
            "changes": changes,
            "compared_with": {
                "state_id": state_id,
                "state_name": most_recent_state["name"],
                "timestamp": most_recent_state["timestamp"]
            }
        }
    
    def create_system_snapshot(self, name: str = None) -> str:
        """Create a full system snapshot with optional name.
        
        Args:
            name: Optional name for the snapshot
            
        Returns:
            The ID of the snapshot
        """
        if not name:
            name = f"System Snapshot {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
        description = "Full system snapshot created by CRONOS preservation system"
        return self.save_system_state(name, description)
    
    def get_cross_references(self) -> Dict[str, List[str]]:
        """Get cross-references between critical files.
        
        Returns:
            A dictionary mapping each file to a list of files it references
        """
        references = {}
        
        # Check each critical file
        for file_path in self.critical_files + self.platform_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                continue
                
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
            except Exception as e:
                logger.error(f"Error reading {file_path}: {e}")
                continue
                
            file_references = []
            # Check for references to other critical files
            for other_file in self.critical_files + self.platform_files:
                if other_file == file_path:
                    continue
                    
                # Simple check for filename in content
                if os.path.basename(other_file) in content:
                    file_references.append(other_file)
            
            references[file_path] = file_references
        
        return references

# Create CLI command functions to interact with the state preservation manager

def save_state(config: Config, name: str, description: str = "") -> None:
    """CLI command to save the current system state.
    
    Args:
        config: The system configuration
        name: Name of the state
        description: Optional description of the state
    """
    manager = StatePreservationManager(config)
    state_id = manager.save_system_state(name, description)
    print(f"✅ System state saved with ID: {state_id}")
    print(f"Name: {name}")
    if description:
        print(f"Description: {description}")

def restore_state(config: Config, state_id: str) -> None:
    """CLI command to restore a system state.
    
    Args:
        config: The system configuration
        state_id: The ID of the state to restore
    """
    manager = StatePreservationManager(config)
    success = manager.restore_system_state(state_id)
    
    if success:
        print(f"✅ System state {state_id} restored successfully")
    else:
        print(f"❌ Failed to restore system state {state_id}")

def list_states(config: Config) -> None:
    """CLI command to list available system states.
    
    Args:
        config: The system configuration
    """
    manager = StatePreservationManager(config)
    states = manager.get_system_states()
    
    if not states:
        print("No system states found.")
        return
    
    print(f"📋 Available System States ({len(states)}):")
    print("-" * 80)
    
    for i, state in enumerate(states):
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

def show_state(config: Config, state_id: str) -> None:
    """CLI command to show details of a system state.
    
    Args:
        config: The system configuration
        state_id: The ID of the state to show
    """
    manager = StatePreservationManager(config)
    state_info = manager.get_state_info(state_id)
    
    if not state_info:
        print(f"❌ State with ID {state_id} not found")
        return
    
    # Parse timestamp for display
    try:
        timestamp = datetime.fromisoformat(state_info["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    except:
        timestamp = state_info["timestamp"]
    
    print(f"📊 State Information: {state_info['name']} ({state_id})")
    print("-" * 80)
    print(f"Created: {timestamp}")
    print(f"Version: {state_info.get('version', 'N/A')}")
    
    if state_info.get("description"):
        print(f"Description: {state_info['description']}")
    
    # Show stats
    stats = state_info.get("stats", {})
    if stats:
        print("\n📈 Statistics:")
        print(f"Total Files: {stats.get('total_files', 'N/A')}")
        print(f"Preserved Files: {stats.get('preserved_files', 'N/A')}")
        print(f"Total Size: {stats.get('total_size', 0) / 1024:.1f} KB")
    
    # Show preserved files
    preserved_files = state_info.get("preserved_files", [])
    if preserved_files:
        print(f"\n📂 Preserved Files ({len(preserved_files)}):")
        for file in preserved_files:
            print(f"  - {file}")

def analyze_changes_cmd(config: Config) -> None:
    """CLI command to analyze changes since the last state.
    
    Args:
        config: The system configuration
    """
    manager = StatePreservationManager(config)
    analysis = manager.analyze_changes()
    
    if not analysis["changes_detected"]:
        print(f"✅ No changes detected since last state.")
        print(analysis.get("message", ""))
        return
    
    # Show comparison state
    compared_with = analysis.get("compared_with", {})
    if compared_with:
        print(f"📊 Changes since state: {compared_with.get('state_name')} ({compared_with.get('state_id')})")
        try:
            timestamp = datetime.fromisoformat(compared_with.get("timestamp")).strftime("%Y-%m-%d %H:%M:%S")
            print(f"Last State Created: {timestamp}")
        except:
            pass
    
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

def show_cross_references(config: Config) -> None:
    """CLI command to show cross-references between files.
    
    Args:
        config: The system configuration
    """
    manager = StatePreservationManager(config)
    references = manager.get_cross_references()
    
    if not references:
        print("No cross-references found.")
        return
    
    print("📊 File Cross-References:")
    print("-" * 80)
    
    for file, refs in references.items():
        if refs:
            print(f"\n📄 {file} references:")
            for ref in refs:
                print(f"  - {ref}")

def create_snapshot(config: Config, name: str = None) -> None:
    """CLI command to create a full system snapshot.
    
    Args:
        config: The system configuration
        name: Optional name for the snapshot
    """
    manager = StatePreservationManager(config)
    snapshot_id = manager.create_system_snapshot(name)
    
    print(f"✅ System snapshot created with ID: {snapshot_id}")
    if name:
        print(f"Name: {name}")

# Main function for direct execution
def main():
    """Run the state preservation module as a standalone script."""
    import argparse
    from ..config import Config
    
    parser = argparse.ArgumentParser(description="EVA & GUARANI State Preservation")
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
    
    # Show state command
    show_parser = subparsers.add_parser("show", help="Show details of a system state")
    show_parser.add_argument("state_id", help="ID of the state to show")
    
    # Analyze changes command
    subparsers.add_parser("analyze", help="Analyze changes since the last state")
    
    # Show cross-references command
    subparsers.add_parser("refs", help="Show cross-references between files")
    
    # Create snapshot command
    snapshot_parser = subparsers.add_parser("snapshot", help="Create a full system snapshot")
    snapshot_parser.add_argument("--name", "-n", help="Name of the snapshot")
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config()
    config.load_config()
    
    # Execute appropriate command
    if args.command == "save":
        save_state(config, args.name, args.description or "")
    elif args.command == "restore":
        restore_state(config, args.state_id)
    elif args.command == "list":
        list_states(config)
    elif args.command == "show":
        show_state(config, args.state_id)
    elif args.command == "analyze":
        analyze_changes_cmd(config)
    elif args.command == "refs":
        show_cross_references(config)
    elif args.command == "snapshot":
        create_snapshot(config, args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 