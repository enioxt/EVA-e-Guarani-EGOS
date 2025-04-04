"""
BIOS-Q Core Module
Implements the core functionality of the BIOS-Q system.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from .errors import BiosQError
from .context_integration import BiosQContextIntegration


class BIOSQ:
    """Core BIOS-Q class implementing quantum-inspired system initialization."""

    def __init__(self):
        """Initialize BIOS-Q system."""
        self.context_manager = BiosQContextIntegration()
        self.mcp_connector = None
        self._initialize_logging()

    def _initialize_logging(self):
        """Set up logging configuration."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "bios_q.log"
        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def add_message(self, role: str, content: str) -> Dict[str, Any]:
        """Add a message to the context."""
        try:
            self.context_manager.add_message(
                {"role": role, "content": content, "timestamp": datetime.now().isoformat()}
            )
            return {"success": True}
        except Exception as e:
            logging.error(f"Error adding message: {e}")
            return {"success": False, "error": str(e)}

    def get_context(self) -> List[Dict[str, str]]:
        """Get current context."""
        return self.context_manager.messages

    def get_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return {
            "context_size": len(self.context_manager.messages),
            "context_limit": self.context_manager.context_limit,
            "mcp_available": self.mcp_connector is not None,
        }

    def save_to_mcp(self) -> Dict[str, Any]:
        """Save current state to MCP."""
        if not self.mcp_connector:
            return {"success": False, "error": "MCP not available"}

        try:
            state = {"context": self.get_context(), "status": self.get_status()}
            self.mcp_connector.save_state(state)
            return {"success": True}
        except Exception as e:
            logging.error(f"Error saving to MCP: {e}")
            return {"success": False, "error": str(e)}

    def load_from_mcp(self) -> Dict[str, Any]:
        """Load state from MCP."""
        if not self.mcp_connector:
            return {"success": False, "error": "MCP not available"}

        try:
            state = self.mcp_connector.load_state()
            if state and "context" in state:
                self.context_manager.messages = state["context"]
            return {"success": True}
        except Exception as e:
            logging.error(f"Error loading from MCP: {e}")
            return {"success": False, "error": str(e)}

    def create_backup(self) -> Optional[str]:
        """Create a backup of current state."""
        try:
            backup_dir = Path("backups")
            backup_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"bios_q_backup_{timestamp}.json"

            state = {
                "context": self.get_context(),
                "status": self.get_status(),
                "timestamp": timestamp,
            }

            with open(backup_file, "w") as f:
                json.dump(state, f, indent=2)

            return str(backup_file)
        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            return None
