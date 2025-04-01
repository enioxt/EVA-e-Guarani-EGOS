#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simplified Context Monitor for MCP
Provides adaptive context monitoring and auto-save functionality
"""

import os
import time
import json
import threading
import datetime
from pathlib import Path

# Configuration
DEFAULT_CONTEXT_LIMIT = 100000  # Initial conservative limit
SAFE_MARGIN = 0.90  # Use 90% of real limit for safety
CHECK_INTERVAL = 60  # Check every 60 seconds
AUTO_SAVE_INTERVAL = 30 * 60  # Auto-save every 30 minutes

# Paths
CONFIG_DIR = Path(__file__).parent.parent / "config"
CONTEXT_LIMITS_FILE = CONFIG_DIR / "context_limits.json"
MONITOR_DATA_FILE = CONFIG_DIR / "monitor_data.json"

# Ensure config directory exists
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# Global state
monitor_state = {
    "running": False,
    "current_size": 0,
    "message_count": 0,
    "capacity_used": 0.0,
    "last_check_time": time.time(),
    "last_save_time": time.time(),
    "threshold_reached": False,
    "context_limit": DEFAULT_CONTEXT_LIMIT,
    "context_source": "default"
}

# Thread safety
state_lock = threading.RLock()

def load_context_limits():
    """Load context limits from config"""
    try:
        if CONTEXT_LIMITS_FILE.exists():
            with open(CONTEXT_LIMITS_FILE, 'r', encoding='utf-8') as f:
                limits = json.load(f)
                with state_lock:
                    if "cursor" in limits and limits["cursor"].get("measured", False):
                        monitor_state["context_limit"] = limits["cursor"]["safe_limit"]
                        monitor_state["context_source"] = "empirical"
                        return True
        return False
    except Exception as e:
        print(f"Error loading context limits: {e}")
        return False

def save_context_limits(limit, measured=True):
    """Save context limits to config"""
    try:
        limits = {}
        if CONTEXT_LIMITS_FILE.exists():
            with open(CONTEXT_LIMITS_FILE, 'r', encoding='utf-8') as f:
                limits = json.load(f)
        
        limits["cursor"] = {
            "limit": limit,
            "measured": measured,
            "last_updated": datetime.datetime.now().isoformat(),
            "safe_limit": int(limit * SAFE_MARGIN)
        }
        
        with open(CONTEXT_LIMITS_FILE, 'w', encoding='utf-8') as f:
            json.dump(limits, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving context limits: {e}")
        return False

def save_monitor_state():
    """Save monitor state to file"""
    try:
        with open(MONITOR_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(monitor_state, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving monitor state: {e}")
        return False

def check_context_size():
    """Check current context size and trigger auto-save if needed"""
    with state_lock:
        current_time = time.time()
        
        # Auto-save on interval
        if current_time - monitor_state["last_save_time"] >= AUTO_SAVE_INTERVAL:
            from . import mcp_capture  # Import here to avoid circular dependency
            mcp_capture.save_context()
            monitor_state["last_save_time"] = current_time
        
        # Update state
        monitor_state["last_check_time"] = current_time
        save_monitor_state()

def start_monitoring():
    """Start the monitoring thread"""
    def monitor_loop():
        while monitor_state["running"]:
            check_context_size()
            time.sleep(CHECK_INTERVAL)
    
    with state_lock:
        if not monitor_state["running"]:
            monitor_state["running"] = True
            thread = threading.Thread(target=monitor_loop, daemon=True)
            thread.start()
            return thread
    return None

def stop_monitoring():
    """Stop the monitoring thread"""
    with state_lock:
        monitor_state["running"] = False
        save_monitor_state()

def update_context_size(size):
    """Update the current context size"""
    with state_lock:
        monitor_state["current_size"] = size
        monitor_state["capacity_used"] = size / monitor_state["context_limit"]
        monitor_state["threshold_reached"] = (monitor_state["capacity_used"] >= 0.8)
        save_monitor_state()

def get_monitor_status():
    """Get current monitor status"""
    with state_lock:
        return {
            "running": monitor_state["running"],
            "current_size": monitor_state["current_size"],
            "capacity_used": f"{monitor_state['capacity_used']*100:.1f}%",
            "context_limit": monitor_state["context_limit"],
            "source": monitor_state["context_source"],
            "last_check": datetime.datetime.fromtimestamp(monitor_state["last_check_time"]).isoformat(),
            "last_save": datetime.datetime.fromtimestamp(monitor_state["last_save_time"]).isoformat()
        }

if __name__ == "__main__":
    print("Starting context monitor...")
    
    if load_context_limits():
        print(f"Loaded empirical limit: {monitor_state['context_limit']} chars")
    else:
        print(f"Using default limit: {monitor_state['context_limit']} chars")
    
    monitor_thread = start_monitoring()
    
    try:
        while True:
            time.sleep(10)
            with state_lock:
                if not monitor_state["running"]:
                    break
    except KeyboardInterrupt:
        print("\nStopping monitor...")
    finally:
        stop_monitoring()
        
    print("Context monitor stopped.") 