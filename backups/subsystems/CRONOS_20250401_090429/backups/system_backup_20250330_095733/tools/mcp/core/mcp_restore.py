#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simplified Context Restore for MCP
Handles loading saved Cursor contexts
"""

import json
from pathlib import Path
from . import mcp_capture

def load_context(save_path=None):
    """Load context from a save file"""
    try:
        # If no path provided, try to get latest save
        if save_path is None:
            save_path = mcp_capture.get_latest_save()
            if save_path is None:
                print("No save files found")
                return None
        
        # Convert to Path object
        save_path = Path(save_path)
        
        # Verify file exists
        if not save_path.exists():
            print(f"Save file not found: {save_path}")
            return None
        
        # Load context
        with open(save_path, 'r', encoding='utf-8') as f:
            context = json.load(f)
            
        print(f"Context loaded from: {save_path}")
        return context
    except Exception as e:
        print(f"Error loading context: {e}")
        return None

def verify_context(context):
    """Verify that a context has the required structure"""
    try:
        required_fields = ["timestamp", "messages", "metadata"]
        return all(field in context for field in required_fields)
    except Exception:
        return False

if __name__ == "__main__":
    # Try to load latest context
    context = load_context()
    if context and verify_context(context):
        print("\nContext structure:")
        print(f"- Timestamp: {context['timestamp']}")
        print(f"- Messages: {len(context['messages'])}")
        print(f"- Metadata: {context['metadata']}") 