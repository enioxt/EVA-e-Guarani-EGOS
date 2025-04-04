#!/usr/bin/env python3
import json
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class QuantumPromptManager:
    def __init__(self):
        # Get the script's directory
        self.script_path = Path(__file__).resolve()
        self.base_path = self.script_path.parent.parent
        self.config_path = self.base_path / "config" / "quantum_prompts.json"
        logging.info(f"Script path: {self.script_path}")
        logging.info(f"Base path: {self.base_path}")
        logging.info(f"Config path: {self.config_path}")
        self.config = self._load_config()
        self.prompts = {}

    def _load_config(self):
        """Load the quantum prompts configuration."""
        try:
            logging.info(f"Loading configuration from {self.config_path}")
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                logging.info("Configuration loaded successfully")
                return config
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            return None

    def _load_prompt(self, path):
        """Load a quantum prompt from file."""
        try:
            # Convert path to absolute path
            if path.startswith("../"):
                abs_path = (self.base_path.parent / path.lstrip("../")).resolve()
            else:
                abs_path = (self.base_path / path).resolve()

            logging.info(f"Loading prompt from {abs_path}")

            if not abs_path.exists():
                # Try alternative paths
                alt_paths = [
                    self.base_path.parent / path.lstrip("../"),  # Try parent directory
                    self.base_path / path,  # Try base directory
                    self.base_path / path.lstrip("/"),  # Try without leading slash
                    Path(path),  # Try absolute path
                ]

                for alt_path in alt_paths:
                    logging.info(f"Trying alternative path: {alt_path}")
                    if alt_path.exists():
                        abs_path = alt_path
                        break
                else:
                    logging.error(f"File not found: {abs_path}")
                    logging.error(f"Current working directory: {os.getcwd()}")
                    logging.error(f"Base path: {self.base_path}")
                    logging.error(f"Relative path: {path}")
                    logging.error("Tried alternative paths:")
                    for alt_path in alt_paths:
                        logging.error(f"- {alt_path}")
                    return None

            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
                logging.info(f"Successfully loaded prompt from {abs_path}")
                return content
        except Exception as e:
            logging.error(f"Error loading prompt {path}: {e}")
            logging.error(f"Current working directory: {os.getcwd()}")
            logging.error(f"Base path: {self.base_path}")
            logging.error(f"Relative path: {path}")
            return None

    def _update_cursor_prompt(self):
        """Update the Cursor's quantum prompt."""
        cursor_config = Path.home() / ".cursor" / "quantum_prompt.md"
        try:
            # Ensure the .cursor directory exists
            cursor_config.parent.mkdir(parents=True, exist_ok=True)
            logging.info(f"Updating Cursor prompt at {cursor_config}")

            # Write the master prompt to Cursor's config
            if self.prompts.get("master"):
                with open(cursor_config, "w", encoding="utf-8") as f:
                    f.write(self.prompts["master"])
                logging.info(f"Successfully updated Cursor prompt")
                print(f"✓ Prompt do Cursor atualizado em: {cursor_config}")
            else:
                logging.error("Master prompt not found")
                print("✗ Master prompt not found")
        except Exception as e:
            logging.error(f"Error updating Cursor prompt: {e}")
            print(f"Error updating Cursor prompt: {e}")

    def synchronize(self):
        """Synchronize all quantum prompts."""
        if not self.config:
            logging.error("No configuration loaded")
            print("✗ No configuration loaded")
            return False

        success = True

        # Load master prompt
        master_path = self.config["master_prompt"]["path"]
        logging.info(f"Loading master prompt from {master_path}")
        self.prompts["master"] = self._load_prompt(master_path)
        if not self.prompts["master"]:
            success = False
            logging.error(f"Failed to load master prompt from {master_path}")

        # Load subsystem prompts
        for subsystem in self.config["subsystems"]:
            name = subsystem["name"].lower()
            path = subsystem["path"]
            logging.info(f"Loading {name} prompt from {path}")
            self.prompts[name] = self._load_prompt(path)
            if not self.prompts[name]:
                success = False
                logging.error(f"Failed to load {name} prompt from {path}")

        # Update Cursor's prompt
        self._update_cursor_prompt()

        if success:
            print("✓ Todos os prompts foram sincronizados com sucesso")
        else:
            print("✗ Alguns prompts não puderam ser carregados")

        return success


def main():
    print("EVA & GUARANI - Quantum Prompt Manager")
    print("======================================")
    logging.info("Starting Quantum Prompt Manager")

    # Get the script's directory and change to it
    script_dir = Path(__file__).resolve().parent.parent
    os.chdir(script_dir)
    logging.info(f"Changed working directory to: {script_dir}")

    # Create the QUANTUM_PROMPTS directory if it doesn't exist
    quantum_prompts_dir = script_dir / "QUANTUM_PROMPTS"
    quantum_prompts_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories for each subsystem
    subsystems = ["MASTER", "CRONOS", "ATLAS", "NEXUS", "ETHIK"]
    for subsystem in subsystems:
        subsystem_dir = quantum_prompts_dir / subsystem
        subsystem_dir.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {subsystem_dir}")

    # Create symbolic links to existing prompts if they exist
    for subsystem in subsystems:
        source_path = Path(f"../QUANTUM_PROMPTS/{subsystem}/quantum_prompt.md")
        target_path = quantum_prompts_dir / subsystem / "quantum_prompt.md"

        if source_path.exists() and not target_path.exists():
            try:
                os.symlink(source_path, target_path)
                logging.info(f"Created symbolic link: {target_path} -> {source_path}")
            except Exception as e:
                logging.error(f"Error creating symbolic link: {e}")

    manager = QuantumPromptManager()
    if manager.synchronize():
        logging.info("All prompts synchronized successfully")
    else:
        logging.error("Failed to synchronize some prompts")


if __name__ == "__main__":
    main()
