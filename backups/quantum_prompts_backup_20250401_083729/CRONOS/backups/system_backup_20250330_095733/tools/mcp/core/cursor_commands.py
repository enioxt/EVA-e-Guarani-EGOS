#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simplified Command Interface for MCP
Provides commands for interacting with the MCP system
"""

import sys
import json
from pathlib import Path
from . import mcp_capture
from . import mcp_restore
from . import context_monitor


def save_mcp():
    """Save current context"""
    save_path = mcp_capture.save_context()
    if save_path:
        print(f"Context saved successfully to: {save_path}")
        return True
    return False


def load_mcp(path=None):
    """Load saved context"""
    context = mcp_restore.load_context(path)
    if context and mcp_restore.verify_context(context):
        print("Context loaded successfully")
        return True
    return False


def list_saves():
    """List all saved contexts"""
    saves = mcp_capture.get_save_list()
    if not saves:
        print("No saved contexts found")
        return False

    print(f"\nFound {len(saves)} saved contexts:")
    for save in saves:
        print(f"- {save['timestamp']}: {save['path']}")
    return True


def show_status():
    """Show current monitor status"""
    status = context_monitor.get_monitor_status()
    print("\nMCP Monitor Status:")
    print(f"- Running: {status['running']}")
    print(f"- Current Size: {status['current_size']} chars")
    print(f"- Capacity Used: {status['capacity_used']}")
    print(f"- Context Limit: {status['context_limit']} chars ({status['source']})")
    print(f"- Last Check: {status['last_check']}")
    print(f"- Last Save: {status['last_save']}")
    return True


def update_limit(size=None):
    """Update context limit based on current size"""
    if size is None:
        # In a real implementation, we would get this from Cursor
        size = 100000  # Example size

    success = context_monitor.save_context_limits(size)
    if success:
        print(f"Context limit updated to {size} chars")
        return True
    return False


def main():
    """Main command handler"""
    if len(sys.argv) < 2:
        print("Usage: cursor_commands.py <command> [args...]")
        return 1

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "save_mcp": save_mcp,
        "load_mcp": lambda: load_mcp(args[0] if args else None),
        "list_saves": list_saves,
        "show_status": show_status,
        "update_limit": lambda: update_limit(int(args[0]) if args else None),
    }

    if command not in commands:
        print(f"Unknown command: {command}")
        return 1

    success = commands[command]()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
