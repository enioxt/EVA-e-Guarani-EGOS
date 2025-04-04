"""
Test suite for BIOS-Q initialization and core functionality.
"""

import unittest
import os
import json
from pathlib import Path
from BIOS_Q.bios_core import BIOSQ


class TestBIOSQ(unittest.TestCase):
    """Test cases for BIOS-Q functionality."""

    def setUp(self):
        """Set up test environment."""
        self.bios = BIOSQ()

    def test_initialization(self):
        """Test basic initialization."""
        self.assertIsNotNone(self.bios)
        self.assertTrue(hasattr(self.bios, "context_manager"))

    def test_add_message(self):
        """Test message addition."""
        result = self.bios.add_message("user", "Test message")
        self.assertTrue(result["success"])
        self.assertEqual(len(self.bios.context_manager.messages), 1)

    def test_context_limit(self):
        """Test context size management."""
        # Add messages up to limit
        for i in range(10):
            self.bios.add_message("user", f"Message {i}")

        status = self.bios.get_status()
        self.assertLess(status["context_size"], status["context_limit"])

    def test_mcp_integration(self):
        """Test MCP connector functionality."""
        if self.bios.mcp_connector:
            result = self.bios.save_to_mcp()
            self.assertTrue(result["success"])

            result = self.bios.load_from_mcp()
            self.assertTrue(result["success"])

    def test_status(self):
        """Test status reporting."""
        status = self.bios.get_status()
        self.assertIsInstance(status, dict)
        self.assertIn("context_size", status)
        self.assertIn("context_limit", status)
        self.assertIn("mcp_available", status)


if __name__ == "__main__":
    unittest.main()
