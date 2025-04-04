#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compatibility module for old imports
"""

import sys
import os
import importlib

# Add root directory to path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import quantum modules
try:
    import quantum

    # Create aliases for compatibility
    sys.modules["quantum_master"] = importlib.import_module("quantum.quantum_master")
    sys.modules["quantum_consciousness_backup"] = importlib.import_module(
        "quantum.quantum_consciousness_backup"
    )
    sys.modules["quantum_memory_preservation"] = importlib.import_module(
        "quantum.quantum_memory_preservation"
    )
    sys.modules["quantum_optimizer"] = importlib.import_module("quantum.quantum_optimizer")
except ImportError as e:
    print(f"Error importing quantum modules: {e}")
