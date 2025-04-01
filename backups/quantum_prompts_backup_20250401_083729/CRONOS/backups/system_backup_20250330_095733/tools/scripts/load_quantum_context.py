#!/usr/bin/env python3
import os
import json
import shutil
from pathlib import Path

def prepare_quantum_context():
    """Prepare and verify quantum context for Cursor"""
    base_path = Path("C:/Eva & Guarani - EGOS")
    cursor_context_path = base_path / "CHATS" / "cursor_context"
    
    # Ensure cursor_context directory exists
    cursor_context_path.mkdir(parents=True, exist_ok=True)
    
    # Define essential contexts
    essential_contexts = [
        {"path": "QUANTUM_PROMPTS/MASTER", "priority": 1},
        {"path": "QUANTUM_PROMPTS", "priority": 2},
        {"path": "core/atlas", "priority": 3},
        {"path": "core/nexus", "priority": 4},
        {"path": "core/cronos", "priority": 5},
        {"path": "core/ethik", "priority": 6},
        {"path": "tools", "priority": 7},
        {"path": "CHATS", "priority": 8}
    ]
    
    # Create context manifest
    context_manifest = {
        "system": "EVA & GUARANI EGOS",
        "version": "7.5",
        "contexts": essential_contexts,
        "master_file": "QUANTUM_PROMPTS/MASTER/quantum_context.md"
    }
    
    # Save manifest
    with open(cursor_context_path / "context_manifest.json", "w") as f:
        json.dump(context_manifest, f, indent=2)
    
    print("\nQuantum Context Loading Instructions:")
    print("=====================================")
    print("When starting a new Cursor chat, add these contexts in order:")
    for ctx in sorted(essential_contexts, key=lambda x: x["priority"]):
        print(f"{ctx['priority']}. {ctx['path']}")
    print("\nMaster Context File: QUANTUM_PROMPTS/MASTER/quantum_context.md")

if __name__ == "__main__":
    prepare_quantum_context() 