#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simplified Context Capture for MCP
Handles saving the current Cursor context
"""

import os
import json
import datetime
from pathlib import Path

# Paths
SAVE_DIR = Path(__file__).parent.parent / "saves"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

def generate_save_name():
    """Generate a unique name for the save file"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"context_{timestamp}.json"

def save_context(context_data=None):
    """Save the current context to a file"""
    try:
        # If no context data provided, create minimal structure
        if context_data is None:
            context_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "messages": [],
                "metadata": {
                    "source": "cursor",
                    "version": "1.0"
                }
            }
        
        # Generate save file path
        save_path = SAVE_DIR / generate_save_name()
        
        # Save context
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, indent=2)
            
        print(f"Context saved to: {save_path}")
        return str(save_path)
    except Exception as e:
        print(f"Error saving context: {e}")
        return None

def get_latest_save():
    """Get the path of the most recent save file"""
    try:
        saves = list(SAVE_DIR.glob("context_*.json"))
        if not saves:
            return None
        return str(max(saves, key=os.path.getctime))
    except Exception as e:
        print(f"Error getting latest save: {e}")
        return None

def get_save_list():
    """Get list of all save files"""
    try:
        saves = list(SAVE_DIR.glob("context_*.json"))
        return [
            {
                "path": str(save),
                "timestamp": datetime.datetime.fromtimestamp(save.stat().st_ctime).isoformat()
            }
            for save in saves
        ]
    except Exception as e:
        print(f"Error listing saves: {e}")
        return []

if __name__ == "__main__":
    # Test save
    test_context = {
        "timestamp": datetime.datetime.now().isoformat(),
        "messages": ["Test message"],
        "metadata": {"test": True}
    }
    
    save_path = save_context(test_context)
    if save_path:
        print(f"Test save successful: {save_path}")
        
    # List saves
    saves = get_save_list()
    print(f"\nFound {len(saves)} save files:") 