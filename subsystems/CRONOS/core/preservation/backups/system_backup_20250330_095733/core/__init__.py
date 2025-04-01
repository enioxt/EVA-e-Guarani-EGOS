"""EVA & GUARANI Core Package
Version: 8.0

This package contains the core functionality of the EVA & GUARANI system.
"""

from pathlib import Path

# Core system paths
CORE_DIR = Path(__file__).parent
ROOT_DIR = CORE_DIR.parent
METADATA_DIR = CORE_DIR / 'metadata'
QUANTUM_DIR = ROOT_DIR / 'QUANTUM_PROMPTS'

# Version information
VERSION = '8.0'
BUILD = '2025.03.26'

# Initialize core components
def initialize():
    """Initialize core system components."""
    for directory in [CORE_DIR, METADATA_DIR, QUANTUM_DIR]:
        directory.mkdir(exist_ok=True)
        
    return {
        'version': VERSION,
        'build': BUILD,
        'paths': {
            'core': str(CORE_DIR),
            'root': str(ROOT_DIR),
            'metadata': str(METADATA_DIR),
            'quantum': str(QUANTUM_DIR)
        }
    }