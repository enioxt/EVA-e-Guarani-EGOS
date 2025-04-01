#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Quantum Memory Preservation Module
==================================

Responsible for preserving and retrieving memories from EVA & GUARANI.
"""

import logging
import json
import os
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("quantum_memory_preservation")

class MemoryPreservation:
    """Class for memory preservation and retrieval."""
    
    def __init__(self):
        self.logger = logging.getLogger("quantum_memory_preservation")
        self.logger.info("MemoryPreservation initialized")
        self.memory_dir = Path("data/memories")
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.memories = {}
        self.load_memories()
        
    def load_memories(self):
        """Loads all saved memories."""
        try:
            memory_files = list(self.memory_dir.glob("*.json"))
            for file in memory_files:
                with open(file, "r", encoding="utf-8") as f:
                    memory = json.load(f)
                    self.memories[file.stem] = memory
            self.logger.info(f"Loaded {len(self.memories)} memories")
        except Exception as e:
            self.logger.error(f"Error loading memories: {e}")
            
    def save_memory(self, key, data):
        """Saves a memory."""
        try:
            self.memories[key] = data
            filepath = self.memory_dir / f"{key}.json"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Memory '{key}' saved")
            return True
        except Exception as e:
            self.logger.error(f"Error saving memory '{key}': {e}")
            return False
            
    def get_memory(self, key):
        """Retrieves a memory."""
        if key in self.memories:
            self.logger.info(f"Memory '{key}' retrieved")
            return self.memories[key]
        else:
            self.logger.warning(f"Memory '{key}' not found")
            return None
            
    def list_memories(self):
        """Lists all available memories."""
        return list(self.memories.keys())

# Global instance
memory_preservation = MemoryPreservation()