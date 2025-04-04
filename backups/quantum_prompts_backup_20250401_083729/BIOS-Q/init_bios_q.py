#!/usr/bin/env python
"""
EVA & GUARANI EGOS - BIOS-Q Initialization Script

This script serves as the primary initialization for BIOS-Q, which manages
the loading of contexts and ensures proper system startup.
"""

import os
import sys
import logging
import importlib.util
import subprocess
from pathlib import Path
import datetime
import argparse
import json

# Configure logging
log_dir = Path("BIOS-Q/logs")
os.makedirs(log_dir, exist_ok=True)
log_file = log_dir / "bios_q_init.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [BIOS-Q] %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("BIOS-Q.Init")


class BiosQInitializer:
    """BIOS-Q Initialization Manager"""

    def __init__(self, base_path=None):
        # Determine base path
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path(os.getcwd())
            # If we're not in the project root, try to find it
            if not (self.base_path / "BIOS-Q").exists():
                if (self.base_path.parent / "BIOS-Q").exists():
                    self.base_path = self.base_path.parent

        self.bios_q_dir = self.base_path / "BIOS-Q"
        self.quantum_dir = self.base_path / "QUANTUM_PROMPTS"
        self.master_dir = self.quantum_dir / "MASTER"

        # Ensure master directory exists
        os.makedirs(self.master_dir, exist_ok=True)

        # Add quantum state path
        self.quantum_state_path = self.quantum_dir / "BIOS-Q" / "quantum_state.json"
        self.quantum_state = None

        logger.info(f"BIOS-Q initializing from: {self.base_path}")

    def run_context_boot_sequence(self):
        """Run the context boot sequence script"""
        try:
            context_boot_script = self.bios_q_dir / "context_boot_sequence.py"
            if not context_boot_script.exists():
                logger.error(f"Context boot sequence script not found: {context_boot_script}")
                return False

            logger.info("Running context boot sequence...")

            # Try to import and run
            try:
                spec = importlib.util.spec_from_file_location(
                    "context_boot_sequence", context_boot_script
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                logger.info("Context boot sequence module loaded successfully")
                return True
            except ImportError:
                # Fall back to subprocess if import fails
                result = subprocess.run(
                    [sys.executable, str(context_boot_script)], capture_output=True, text=True
                )
                if result.returncode == 0:
                    logger.info("Context boot sequence completed successfully")
                    return True
                else:
                    logger.error(f"Context boot sequence failed: {result.stderr}")
                    return False

        except Exception as e:
            logger.error(f"Error running context boot sequence: {e}")
            return False

    def run_bios_q_context_integration(self):
        """Run the BIOS-Q context integration"""
        try:
            integration_script = self.bios_q_dir / "BIOS_Q" / "context_integration.py"
            if not integration_script.exists():
                logger.warning(f"Context integration script not found: {integration_script}")
                return False

            logger.info("Running BIOS-Q context integration...")

            # Try to import and run
            try:
                spec = importlib.util.spec_from_file_location(
                    "context_integration", integration_script
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Initialize integration
                integration = module.BiosQContextIntegration(str(self.base_path))
                success = integration.integrate()

                if success:
                    logger.info("BIOS-Q context integration completed successfully")
                    return True
                else:
                    logger.warning("BIOS-Q context integration completed with warnings")
                    return False

            except ImportError:
                # Fall back to subprocess
                result = subprocess.run(
                    [sys.executable, str(integration_script)], capture_output=True, text=True
                )
                if result.returncode == 0:
                    logger.info("BIOS-Q context integration completed successfully")
                    return True
                else:
                    logger.error(f"BIOS-Q context integration failed: {result.stderr}")
                    return False

        except Exception as e:
            logger.error(f"Error running BIOS-Q context integration: {e}")
            return False

    def update_dynamic_context(self):
        """Update the dynamic context"""
        try:
            dcm_script = self.base_path / "tools/scripts/dynamic_context_manager.py"
            if not dcm_script.exists():
                logger.warning(f"Dynamic context manager not found: {dcm_script}")
                return False

            logger.info("Updating dynamic context...")

            # Run the dynamic context manager
            result = subprocess.run(
                [sys.executable, str(dcm_script)], capture_output=True, text=True
            )
            if result.returncode == 0:
                logger.info("Dynamic context updated successfully")
                return True
            else:
                logger.error(f"Dynamic context update failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error updating dynamic context: {e}")
            return False

    def create_bios_q_shortcut(self):
        """Create a shortcut file for BIOS-Q initialization"""
        try:
            shortcut_path = self.base_path / "start_bios_q.bat"

            with open(shortcut_path, "w") as f:
                f.write("@echo off\n")
                f.write("echo EVA & GUARANI EGOS - BIOS-Q Initialization\n")
                f.write("echo =======================================\n")
                f.write("echo.\n")
                f.write("cd /d %~dp0\n")
                f.write("python BIOS-Q\\init_bios_q.py\n")
                f.write("echo.\n")
                f.write("echo BIOS-Q initialization complete.\n")
                f.write(
                    "echo Please refer to QUANTUM_PROMPTS/MASTER/CURSOR_INITIALIZATION.md for next steps.\n"
                )
                f.write("echo.\n")
                f.write("pause\n")

            logger.info(f"Created BIOS-Q shortcut: {shortcut_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating BIOS-Q shortcut: {e}")
            return False

    def create_readme_pointer(self):
        """Create or update a pointer in the README to BIOS-Q initialization"""
        try:
            readme_path = self.base_path / "README.md"
            if not readme_path.exists():
                logger.warning(f"README not found: {readme_path}")
                return False

            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check if BIOS-Q section exists
            if "## BIOS-Q Initialization" in content:
                logger.info("BIOS-Q section already exists in README")
                return True

            # Add BIOS-Q section
            bios_q_section = """
## BIOS-Q Initialization

To initialize the BIOS-Q system and ensure proper context loading:

1. Run `start_bios_q.bat` or `python BIOS-Q/init_bios_q.py`
2. Follow the instructions in `QUANTUM_PROMPTS/MASTER/CURSOR_INITIALIZATION.md`
3. Always load contexts in the correct order when starting a new chat

> ⚠️ **CRITICAL**: Always follow the context loading sequence to ensure system integrity.

"""

            # Find insertion point (before ## License or at the end)
            if "## License" in content:
                content = content.replace("## License", bios_q_section + "\n## License")
            else:
                content += "\n" + bios_q_section

            # Save updated README
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info("Updated README with BIOS-Q initialization instructions")
            return True
        except Exception as e:
            logger.error(f"Error updating README: {e}")
            return False

    def load_quantum_state(self):
        """Load the quantum state from file"""
        try:
            if self.quantum_state_path.exists():
                with open(self.quantum_state_path, "r") as f:
                    self.quantum_state = json.load(f)
                logger.info("Quantum state loaded successfully")
                return True
            else:
                logger.warning("Quantum state file not found, initializing new state")
                self.quantum_state = {
                    "version": "8.0.0",
                    "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "system_state": {
                        "status": "initializing",
                        "phase": "development",
                        "stage": "Phase 2",
                        "progress": 0.0,
                    },
                }
                return self.save_quantum_state()
        except Exception as e:
            logger.error(f"Error loading quantum state: {e}")
            return False

    def save_quantum_state(self):
        """Save the current quantum state to file"""
        try:
            # Ensure parent directory exists
            os.makedirs(self.quantum_state_path.parent, exist_ok=True)

            # Update last_updated timestamp
            if self.quantum_state:
                self.quantum_state["last_updated"] = datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

            with open(self.quantum_state_path, "w") as f:
                json.dump(self.quantum_state, f, indent=4)
            logger.info("Quantum state saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving quantum state: {e}")
            return False

    def update_quantum_state(self, updates):
        """Update specific fields in the quantum state"""
        try:
            if not self.quantum_state:
                if not self.load_quantum_state():
                    return False

            # Recursively update nested dictionaries
            def update_dict(current, updates):
                for key, value in updates.items():
                    if (
                        isinstance(value, dict)
                        and key in current
                        and isinstance(current[key], dict)
                    ):
                        update_dict(current[key], value)
                    else:
                        current[key] = value

            update_dict(self.quantum_state, updates)
            return self.save_quantum_state()
        except Exception as e:
            logger.error(f"Error updating quantum state: {e}")
            return False

    def initialize(self):
        """Initialize BIOS-Q"""
        logger.info("Starting BIOS-Q initialization...")

        # Load quantum state first
        if not self.load_quantum_state():
            logger.error("Failed to load quantum state")
            return False

        # Run initialization sequence
        success = True
        success &= self.run_context_boot_sequence()
        success &= self.run_bios_q_context_integration()
        success &= self.update_dynamic_context()
        success &= self.create_bios_q_shortcut()
        success &= self.create_readme_pointer()

        if success:
            # Update quantum state to operational
            self.update_quantum_state({"system_state": {"status": "operational"}})
            logger.info("BIOS-Q initialization completed successfully")
        else:
            logger.error("BIOS-Q initialization failed")

        return success


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="BIOS-Q Initialization")
    parser.add_argument("--base-path", help="Base path for BIOS-Q initialization")
    args = parser.parse_args()

    initializer = BiosQInitializer(args.base_path)
    success = initializer.initialize()

    if success:
        logger.info("BIOS-Q initialization completed successfully")
        logger.info(
            "Please refer to QUANTUM_PROMPTS/MASTER/CURSOR_INITIALIZATION.md for next steps"
        )
    else:
        logger.error("BIOS-Q initialization completed with warnings/errors")
        logger.error("Please check the logs for details")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
