"""EVA & GUARANI Metadata System
Version: 8.0
"""

from pathlib import Path

# Package paths
METADATA_DIR = Path(__file__).parent
CORE_DIR = METADATA_DIR.parent
ROOT_DIR = CORE_DIR.parent

# Version information
VERSION = '8.0'
BUILD = '2025.03.26'

# Initialize metadata components
def initialize():
    """Initialize metadata system components."""
    # Create necessary directories
    for directory in ['data', 'logs', 'cache']:
        (METADATA_DIR / directory).mkdir(exist_ok=True)
        
    return {
        'version': VERSION,
        'build': BUILD,
        'paths': {
            'metadata': str(METADATA_DIR),
            'core': str(CORE_DIR),
            'root': str(ROOT_DIR)
        }
    }

from .system_maintenance import SystemMaintenance

__all__ = ['SystemMaintenance'] 