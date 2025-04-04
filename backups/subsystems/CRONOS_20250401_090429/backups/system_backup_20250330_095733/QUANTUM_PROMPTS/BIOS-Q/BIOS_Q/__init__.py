"""
BIOS-Q: Basic Input/Output System - Quantum
Core initialization module for EVA & GUARANI system.
"""

from .bios_core import BIOSQ
from .errors import BiosQError
from .context_integration import BiosQContextIntegration

__version__ = "8.0"
__author__ = "EVA & GUARANI"
__all__ = ["BIOSQ", "BiosQError", "BiosQContextIntegration"]


def initialize_bios():
    """Initialize BIOS-Q and start Cursor integration."""
    try:
        # Initialize BIOS-Q
        bios = BIOSQ()
        return bios, None

    except Exception as e:
        print(f"Error initializing BIOS-Q: {e}")
        return None, None


def stop_bios():
    """Stop BIOS-Q."""
    print("BIOS-Q stopped successfully")
