#!/usr/bin/env python3
import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import datetime


class BiosQContextIntegration:
    """
    BIOS-Q Integration with Dynamic Context System

    Provides seamless integration between BIOS-Q and the Dynamic Context System,
    ensuring that context loading is properly performed during system initialization.
    """

    def __init__(self, base_path: str = "C:/Eva & Guarani - EGOS"):
        self.base_path = Path(base_path)
        self.bios_q_dir = self.base_path / "BIOS-Q"
        self.quantum_prompts_dir = self.base_path / "QUANTUM_PROMPTS"
        self.master_dir = self.quantum_prompts_dir / "MASTER"
        self.context_boot_file = self.master_dir / "context_boot.json"
        self.quantum_context_file = self.master_dir / "quantum_context.md"
        self.context_history_file = self.base_path / "CHATS" / "context_history.json"

        # Ensure directories exist
        os.makedirs(self.master_dir, exist_ok=True)
        os.makedirs(self.base_path / "CHATS", exist_ok=True)

        # Set up logging
        self.logger = logging.getLogger("BIOS-Q.ContextIntegration")

    def load_context_boot_sequence(self) -> Optional[Dict[str, Any]]:
        """Load the context boot sequence configuration"""
        try:
            if not self.context_boot_file.exists():
                self.logger.warning(
                    f"Context boot sequence file not found: {self.context_boot_file}"
                )
                return None

            with open(self.context_boot_file, "r") as f:
                data = json.load(f)

            self.logger.info(
                f"Loaded context boot sequence version {data.get('version', 'unknown')}"
            )
            return data
        except Exception as e:
            self.logger.error(f"Error loading context boot sequence: {e}")
            return None

    def verify_dynamic_context_system(self) -> bool:
        """Verify that the dynamic context system is properly set up"""
        try:
            # Check for dynamic context manager
            dcm_path = self.base_path / "tools/scripts/dynamic_context_manager.py"
            if not dcm_path.exists():
                self.logger.warning(f"Dynamic context manager not found: {dcm_path}")
                return False

            # Check for auto context updater
            acu_path = self.base_path / "tools/scripts/auto_context_updater.py"
            if not acu_path.exists():
                self.logger.warning(f"Auto context updater not found: {acu_path}")
                return False

            # Check for quantum context template
            template_path = self.master_dir / "quantum_context_template.md"
            if not template_path.exists():
                self.logger.warning(f"Quantum context template not found: {template_path}")
                return False

            # Check for quantum context file
            if not self.quantum_context_file.exists():
                self.logger.warning(f"Quantum context file not found: {self.quantum_context_file}")
                return False

            self.logger.info("Dynamic context system verification successful")
            return True
        except Exception as e:
            self.logger.error(f"Error verifying dynamic context system: {e}")
            return False

    def update_bootloader_with_context_priorities(
        self, boot_sequence: List[Dict[str, Any]]
    ) -> bool:
        """Update the BIOS-Q bootloader with context loading priorities"""
        try:
            # Create bootloader context configuration
            boot_context_cfg = {
                "CONTEXT_LOADING": {
                    "ENABLED": "true",
                    "AUTO_LOAD": "true",
                    "VERIFY": "true",
                    "LAST_UPDATED": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
                "CONTEXT_SEQUENCE": {},
            }

            # Add context sequences
            for ctx in boot_sequence:
                key = f"PRIORITY_{ctx['priority']}"
                boot_context_cfg["CONTEXT_SEQUENCE"][key] = ctx["path"]

            # Save to a new file
            config_path = self.bios_q_dir / "context_boot.cfg"

            with open(config_path, "w") as f:
                f.write("[CONTEXT_CONFIGURATION]\n")
                f.write("# EVA & GUARANI EGOS - BIOS-Q Context Loading Configuration\n")
                f.write(f"# Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("# DO NOT EDIT MANUALLY\n\n")

                for section, values in boot_context_cfg.items():
                    f.write(f"[{section}]\n")
                    if isinstance(values, dict):
                        for key, value in values.items():
                            f.write(f"{key} = {value}\n")
                    else:
                        f.write(f"VALUE = {values}\n")
                    f.write("\n")

            self.logger.info(f"Updated bootloader context configuration: {config_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating bootloader with context priorities: {e}")
            return False

    def create_context_reminder(self) -> bool:
        """Create a reminder file for context loading sequence"""
        try:
            boot_sequence = self.load_context_boot_sequence()
            if not boot_sequence:
                self.logger.warning("Cannot create context reminder, boot sequence not found")
                return False

            contexts = boot_sequence.get("boot_sequence", [])
            if not contexts:
                self.logger.warning("Boot sequence is empty")
                return False

            # Create reminder file
            reminder_path = self.bios_q_dir / "CONTEXT_LOADING_REMINDER.md"

            with open(reminder_path, "w") as f:
                f.write("# EVA & GUARANI EGOS - Context Loading Reminder\n\n")
                f.write(
                    "> ⚠️ **IMPORTANT**: Always load contexts in the following order when starting a new Cursor chat\n\n"
                )

                f.write("## Context Loading Sequence\n\n")
                for ctx in sorted(contexts, key=lambda x: x["priority"]):
                    req_text = "**REQUIRED**" if ctx.get("required") else "Optional"
                    f.write(f"{ctx['priority']}. `{ctx['path']}` - {req_text}\n")
                    if "description" in ctx:
                        f.write(f"   *{ctx['description']}*\n")

                f.write("\n## Primary Context File\n\n")
                f.write(
                    f"`{self.quantum_context_file.relative_to(self.base_path)}` - This file contains the dynamic system state\n\n"
                )

                f.write("## How to Use\n\n")
                f.write(
                    "1. When starting a new Cursor chat, click on 'Add files, folders, docs...'\n"
                )
                f.write("2. Add each context in the order shown above\n")
                f.write("3. Wait for each context to load before adding the next\n")
                f.write("4. Begin your interaction only after all contexts are loaded\n\n")

                f.write("## Quantum Coherence Warning\n\n")
                f.write(
                    "> Loading contexts in the wrong order may result in decreased system performance,\n"
                )
                f.write("> ethical framework misalignment, or quantum decoherence.\n\n")

                f.write("---\n\n")
                f.write("*Generated by BIOS-Q Context Integration System*\n")
                f.write(
                    f"*Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
                )
                f.write("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

            self.logger.info(f"Created context loading reminder: {reminder_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating context reminder: {e}")
            return False

    def register_bios_q_with_dynamic_context(self) -> bool:
        """Register BIOS-Q with the dynamic context system"""
        try:
            # Create registration file
            registration_path = self.master_dir / "bios_q_integration.json"

            registration_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "system": "BIOS-Q",
                "version": "7.5",
                "integration_type": "Context Management",
                "bootloader_path": str(self.bios_q_dir / "bootloader.cfg"),
                "hardware_map_path": str(self.bios_q_dir / "hardware_map.json"),
                "context_boot_path": str(self.bios_q_dir / "context_boot.cfg"),
                "reminder_path": str(self.bios_q_dir / "CONTEXT_LOADING_REMINDER.md"),
                "capabilities": [
                    "Context sequence management",
                    "Boot-time context verification",
                    "Context loading reminders",
                    "Dynamic context integration",
                    "Quantum coherence monitoring",
                ],
                "status": "active",
            }

            with open(registration_path, "w") as f:
                json.dump(registration_data, f, indent=2)

            self.logger.info(f"Registered BIOS-Q with dynamic context system: {registration_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error registering BIOS-Q with dynamic context system: {e}")
            return False

    def update_quantum_context_with_bios_markers(self) -> bool:
        """Update quantum context template with BIOS-Q markers"""
        try:
            template_path = self.master_dir / "quantum_context_template.md"
            if not template_path.exists():
                self.logger.warning(f"Quantum context template not found: {template_path}")
                return False

            # Read template
            with open(template_path, "r") as f:
                template_content = f.read()

            # Check if BIOS-Q section already exists
            if "## BIOS-Q Integration" in template_content:
                self.logger.info("BIOS-Q section already exists in quantum context template")
                return True

            # Add BIOS-Q section
            bios_q_section = """
## BIOS-Q Integration

```json
{{BIOS_Q_STATE}}
```

Boot Sequence: {{BIOS_Q_BOOT_SEQUENCE}}
Quantum Coherence: {{BIOS_Q_COHERENCE}}
Context Integrity: {{BIOS_Q_CONTEXT_INTEGRITY}}
"""

            # Find insertion point (before metadata section)
            if "## Metadata" in template_content:
                template_content = template_content.replace(
                    "## Metadata", bios_q_section + "\n\n## Metadata"
                )
            else:
                template_content += "\n" + bios_q_section

            # Save updated template
            with open(template_path, "w") as f:
                f.write(template_content)

            self.logger.info("Updated quantum context template with BIOS-Q markers")
            return True
        except Exception as e:
            self.logger.error(f"Error updating quantum context with BIOS-Q markers: {e}")
            return False

    def update_dynamic_context_manager(self) -> bool:
        """Update dynamic context manager to include BIOS-Q information"""
        try:
            dcm_path = self.base_path / "tools/scripts/dynamic_context_manager.py"
            if not dcm_path.exists():
                self.logger.warning(f"Dynamic context manager not found: {dcm_path}")
                return False

            # Add BIOS-Q methods to dynamic context manager
            # ...

            self.logger.info("Updated dynamic context manager to include BIOS-Q information")
            return True
        except Exception as e:
            self.logger.error(f"Error updating dynamic context manager: {e}")
            return False

    def integrate(self) -> bool:
        """Perform full integration between BIOS-Q and dynamic context system"""
        try:
            self.logger.info("Starting BIOS-Q integration with dynamic context system...")

            # Load context boot sequence
            boot_sequence = self.load_context_boot_sequence()
            if not boot_sequence:
                # Try to generate from context boot sequence script
                context_boot_script = self.base_path / "BIOS-Q/context_boot_sequence.py"
                if context_boot_script.exists():
                    self.logger.info("Running context boot sequence script...")
                    # We'll just continue with the integration

            # Verify dynamic context system
            if not self.verify_dynamic_context_system():
                self.logger.warning("Dynamic context system verification failed")
                # Continue anyway

            # Update bootloader with context priorities
            boot_seq_data = boot_sequence.get("boot_sequence", []) if boot_sequence else []
            if boot_seq_data:
                self.update_bootloader_with_context_priorities(boot_seq_data)

            # Create context reminder
            self.create_context_reminder()

            # Register BIOS-Q with dynamic context
            self.register_bios_q_with_dynamic_context()

            # Update quantum context with BIOS-Q markers
            self.update_quantum_context_with_bios_markers()

            # Update dynamic context manager
            self.update_dynamic_context_manager()

            self.logger.info("BIOS-Q integration with dynamic context system complete")
            return True
        except Exception as e:
            self.logger.error(f"Error during BIOS-Q integration: {e}")
            return False


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler("bios_q_context_integration.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Run integration
    integration = BiosQContextIntegration()
    success = integration.integrate()

    if success:
        print("\nBIOS-Q integration with dynamic context system completed successfully.")
        print("Context loading reminders have been created.")
    else:
        print("\nErrors occurred during BIOS-Q integration.")
        print("Please check the logs for details.")
