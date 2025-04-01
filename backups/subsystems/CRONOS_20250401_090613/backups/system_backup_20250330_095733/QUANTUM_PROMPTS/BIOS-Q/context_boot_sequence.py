#!/usr/bin/env python3
import os
import json
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any
import configparser
import datetime

class ContextBootSequence:
    """
    BIOS-Q Context Boot Sequence Manager
    
    Handles the correct loading sequence of contexts for EVA & GUARANI EGOS
    Acts as the first system loaded during initialization
    """
    
    def __init__(self, base_path: str = "C:/Eva & Guarani - EGOS"):
        self.base_path = Path(base_path)
        self.bootloader_path = self.base_path / "BIOS-Q/bootloader.cfg"
        self.contexts_path = self.base_path / "QUANTUM_PROMPTS/MASTER/context_boot.json"
        self.quantum_context_path = self.base_path / "QUANTUM_PROMPTS/MASTER/quantum_context.md"
        self.log_path = self.base_path / "logs/bios_boot.log"
        
        # Ensure logs directory exists
        os.makedirs(self.base_path / "logs", exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [BIOS-Q] %(message)s',
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger("BIOS-Q")
        self.boot_config = None
        self.context_sequence = None

    def load_boot_config(self) -> None:
        """Load the bootloader configuration"""
        self.logger.info("Loading BIOS-Q bootloader configuration...")
        
        if not self.bootloader_path.exists():
            self.logger.error(f"Bootloader configuration not found at {self.bootloader_path}")
            raise FileNotFoundError(f"Bootloader not found: {self.bootloader_path}")
            
        config = configparser.ConfigParser()
        config.read(self.bootloader_path)
        self.boot_config = config
        
        self.logger.info("Bootloader configuration loaded successfully.")
        return config

    def save_context_sequence(self, contexts: List[Dict[str, Any]]) -> None:
        """Save the context loading sequence"""
        self.context_sequence = contexts
        
        # Ensure parent directory exists
        os.makedirs(self.contexts_path.parent, exist_ok=True)
        
        # Create context boot sequence file
        context_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "7.5",
            "system": "EVA & GUARANI EGOS",
            "boot_sequence": contexts
        }
        
        with open(self.contexts_path, "w") as f:
            json.dump(context_data, f, indent=2)
            
        self.logger.info(f"Context boot sequence saved to {self.contexts_path}")

    def generate_context_sequence(self) -> List[Dict[str, Any]]:
        """Generate the recommended context loading sequence"""
        contexts = [
            {"path": "QUANTUM_PROMPTS/MASTER", "priority": 1, "required": True, 
             "description": "Master context containing core system definitions"},
            {"path": "QUANTUM_PROMPTS", "priority": 2, "required": True,
             "description": "Quantum prompts and system principles"},
            {"path": "core/atlas", "priority": 3, "required": True,
             "description": "Systemic cartography module"},
            {"path": "core/nexus", "priority": 4, "required": True,
             "description": "Modular analysis system"},
            {"path": "core/cronos", "priority": 5, "required": True,
             "description": "Evolutionary preservation system"},
            {"path": "core/ethik", "priority": 6, "required": True,
             "description": "Ethical framework integration"},
            {"path": "tools", "priority": 7, "required": True,
             "description": "System utilities and management tools"},
            {"path": "CHATS", "priority": 8, "required": True,
             "description": "Chat history and conversation context"}
        ]
        
        return contexts

    def verify_context_files(self) -> bool:
        """Verify that all required context files exist"""
        self.logger.info("Verifying context files...")
        
        missing_files = []
        
        # Check quantum context file
        if not self.quantum_context_path.exists():
            missing_files.append(str(self.quantum_context_path))
            
        # Check core directories
        for ctx in self.context_sequence:
            path = self.base_path / ctx["path"]
            if not path.exists():
                missing_files.append(str(path))
                
        if missing_files:
            self.logger.warning(f"Missing context files or directories: {', '.join(missing_files)}")
            return False
        
        self.logger.info("All context files verified successfully.")
        return True

    def generate_boot_instructions(self) -> str:
        """Generate human-readable boot instructions"""
        instructions = [
            "# EVA & GUARANI EGOS - Context Loading Instructions",
            "",
            "When starting a new Cursor chat, add these contexts in order:",
            ""
        ]
        
        for ctx in sorted(self.context_sequence, key=lambda x: x["priority"]):
            required = "REQUIRED" if ctx["required"] else "Optional"
            instructions.append(f"{ctx['priority']}. {ctx['path']} - {required}")
            
        instructions.extend([
            "",
            "Master Context File: QUANTUM_PROMPTS/MASTER/quantum_context.md",
            "",
            "## BIOS-Q Boot Sequence",
            "1. Load BIOS-Q context boot sequence",
            "2. Verify context files and directories",
            "3. Initialize quantum context",
            "4. Load contexts in priority order",
            "5. Verify system integrity",
            "",
            "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
        ])
        
        return "\n".join(instructions)

    def save_boot_instructions(self) -> None:
        """Save boot instructions to a file"""
        instructions = self.generate_boot_instructions()
        instructions_path = self.base_path / "BIOS-Q/CONTEXT_BOOT_INSTRUCTIONS.md"
        
        with open(instructions_path, "w") as f:
            f.write(instructions)
            
        self.logger.info(f"Boot instructions saved to {instructions_path}")

    def initialize(self) -> bool:
        """Initialize the boot sequence"""
        try:
            self.logger.info("Initializing BIOS-Q Context Boot Sequence...")
            
            # Load boot configuration
            self.load_boot_config()
            
            # Generate context sequence
            contexts = self.generate_context_sequence()
            self.save_context_sequence(contexts)
            
            # Verify context files
            self.verify_context_files()
            
            # Generate and save boot instructions
            self.save_boot_instructions()
            
            self.logger.info("BIOS-Q Context Boot Sequence initialized successfully.")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing BIOS-Q Context Boot Sequence: {e}")
            return False

    def display_boot_sequence(self) -> None:
        """Display the boot sequence to console"""
        self.logger.info("BIOS-Q Context Boot Sequence:")
        
        for ctx in sorted(self.context_sequence, key=lambda x: x["priority"]):
            status = "Available" if (self.base_path / ctx["path"]).exists() else "Missing"
            self.logger.info(f"{ctx['priority']}. {ctx['path']} - {status}")
            
        self.logger.info("Boot sequence displayed.")

if __name__ == "__main__":
    # Initialize boot sequence
    boot_seq = ContextBootSequence()
    if boot_seq.initialize():
        boot_seq.display_boot_sequence()
        print("\nBIOS-Q Context Boot Sequence initialized successfully.")
        print("Run with --help for more options.")
    else:
        print("\nError initializing BIOS-Q Context Boot Sequence.")
        print("Check logs for details.") 