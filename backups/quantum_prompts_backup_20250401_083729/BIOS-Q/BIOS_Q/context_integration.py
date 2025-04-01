#!/usr/bin/env python
"""
EVA & GUARANI EGOS - BIOS-Q Context Integration
This script handles the integration of contexts and ensures proper system initialization.
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [CONTEXT-INTEGRATION] %(message)s',
    handlers=[
        logging.FileHandler("context_integration.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("CONTEXT-INTEGRATION")

class BiosQContextIntegration:
    """Manages context integration for EVA & GUARANI EGOS"""
    
    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else Path(os.getcwd())
        self.quantum_prompts_dir = self.base_path / "QUANTUM_PROMPTS"
        self.bios_q_dir = self.base_path / "BIOS-Q"
        
    def verify_integration_paths(self):
        """Verify that all required paths exist"""
        required_paths = [
            self.quantum_prompts_dir,
            self.bios_q_dir,
            self.quantum_prompts_dir / "MASTER",
            self.quantum_prompts_dir / "BIOS-Q"
        ]
        
        missing_paths = []
        for path in required_paths:
            if not path.exists():
                missing_paths.append(path)
                logger.warning(f"Missing required path: {path}")
                
        return len(missing_paths) == 0
        
    def create_missing_paths(self):
        """Create any missing required paths"""
        required_paths = [
            self.quantum_prompts_dir,
            self.bios_q_dir,
            self.quantum_prompts_dir / "MASTER",
            self.quantum_prompts_dir / "BIOS-Q"
        ]
        
        for path in required_paths:
            if not path.exists():
                os.makedirs(path)
                logger.info(f"Created directory: {path}")
                
    def integrate(self):
        """Execute the context integration process"""
        logger.info("Starting BIOS-Q context integration...")
        
        # Step 1: Verify required paths
        if not self.verify_integration_paths():
            logger.info("Creating missing paths...")
            self.create_missing_paths()
            
        # Step 2: Create initialization markers
        self.create_initialization_markers()
        
        logger.info("BIOS-Q context integration completed successfully")
                return True
                
    def create_initialization_markers(self):
        """Create initialization marker files"""
        # Create BIOS-Q initialization marker
        bios_q_init = self.bios_q_dir / ".initialized"
        if not bios_q_init.exists():
            with open(bios_q_init, "w") as f:
                f.write("BIOS-Q initialization completed\n")
            logger.info("Created BIOS-Q initialization marker")
            
        # Create QUANTUM_PROMPTS initialization marker
        quantum_init = self.quantum_prompts_dir / ".initialized"
        if not quantum_init.exists():
            with open(quantum_init, "w") as f:
                f.write("QUANTUM_PROMPTS initialization completed\n")
            logger.info("Created QUANTUM_PROMPTS initialization marker")

def main():
    """Main entry point"""
    try:
        integration = BiosQContextIntegration()
        success = integration.integrate()
        return 0 if success else 1
        except Exception as e:
        logger.error(f"Error during context integration: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 