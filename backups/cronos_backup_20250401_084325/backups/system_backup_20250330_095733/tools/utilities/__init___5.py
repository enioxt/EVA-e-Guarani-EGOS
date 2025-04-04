#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Quantum Package EVA & GUARANI
=============================

This package contains the quantum modules of EVA & GUARANI.
"""

from pathlib import Path
import logging
import sys
import os

# Configure logging
logger = logging.getLogger("quantum")
logger.setLevel(logging.INFO)

# Import quantum modules
try:
    from .quantum_master import quantum_master
    from .quantum_consciousness_backup import consciousness_backup
    from .quantum_memory_preservation import memory_preservation
    from .quantum_optimizer import quantum_optimizer

    logger.info("Quantum modules imported successfully")
except ImportError as e:
    logger.warning(f"Error importing quantum modules: {e}")
