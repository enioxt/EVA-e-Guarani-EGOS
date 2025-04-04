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
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [BIOS-Q] %(message)s",
    handlers=[logging.FileHandler("bios_q_init.log"), logging.StreamHandler(sys.stdout)],
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

            with open(readme_path, "r") as f:
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
            with open(readme_path, "w") as f:
                f.write(content)

            logger.info("Updated README with BIOS-Q initialization instructions")
            return True
        except Exception as e:
            logger.error(f"Error updating README: {e}")
            return False

    def initialize(self):
        """Run the full BIOS-Q initialization process"""
        logger.info("Starting BIOS-Q initialization...")

        # Record initialization
        init_time = datetime.datetime.now()
        init_record = {
            "timestamp": init_time.isoformat(),
            "version": "7.5",
            "system": "BIOS-Q",
            "initialized_by": os.environ.get("USERNAME", "unknown"),
            "base_path": str(self.base_path),
        }

        # Save initialization record
        os.makedirs(self.base_path / "logs", exist_ok=True)
        with open(self.base_path / "logs" / "bios_q_init.json", "w") as f:
            json.dump(init_record, f, indent=2)

        # Run steps
        steps = [
            ("Running context boot sequence", self.run_context_boot_sequence),
            ("Running BIOS-Q context integration", self.run_bios_q_context_integration),
            ("Updating dynamic context", self.update_dynamic_context),
            ("Creating BIOS-Q shortcut", self.create_bios_q_shortcut),
            ("Updating README", self.create_readme_pointer),
        ]

        results = {}
        for step_name, step_func in steps:
            logger.info(f"Step: {step_name}")
            success = step_func()
            results[step_name] = "Success" if success else "Failed"
            logger.info(f"Step result: {results[step_name]}")

        # Check overall result
        if all(r == "Success" for r in results.values()):
            logger.info("BIOS-Q initialization completed successfully")
            return True
        else:
            logger.warning("BIOS-Q initialization completed with warnings/errors")
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="BIOS-Q Initialization")
    parser.add_argument("--base-path", help="Base path for the EVA & GUARANI EGOS system")
    args = parser.parse_args()

    initializer = BiosQInitializer(args.base_path)
    success = initializer.initialize()

    if success:
        print("\nBIOS-Q initialization completed successfully.")
        print("Please refer to QUANTUM_PROMPTS/MASTER/CURSOR_INITIALIZATION.md for next steps.")
    else:
        print("\nBIOS-Q initialization completed with warnings/errors.")
        print("Please check the logs for details.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
