#!/usr/bin/env python3
python
"""
Quantum Tools - EVA & GUARANI
-------------------------------------
This module provides high-level tools that integrate the various
subsystems of EVA & GUARANI, including systemic cartography (ATLAS),
modular analysis (NEXUS), evolutionary preservation (CRONOS), and internet
research (PERPLEXITY).
"""

import os
import sys
from typing import Dict, Any, List, Union, Optional
from datetime import datetime
import json

# Add the root directory to PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
egos_dir = os.path.dirname(current_dir)
if egos_dir not in sys.path:
    sys.path.append(egos_dir)

# Subsystem imports
try:
    from .perplexity_integration import PerplexityIntegration
except ImportError:
    # Fallback for development
    PerplexityIntegration = None
    print("[WARNING] Web search module (PERPLEXITY) not available")


class QuantumTools:
    """
    Integrated quantum tools of the EVA & GUARANI system.
    Provides a unified interface to access the subsystems
    ATLAS, NEXUS, CRONOS, and PERPLEXITY.
    """

    def __init__(self):
        """Initializes the quantum tools."""
        self.initialized_at = datetime.now()
        self.log_entries = []

        # Initialize the web search subsystem if available
        self.perplexity = None
        if PerplexityIntegration:
            try:
                self.perplexity = PerplexityIntegration()
                self._log_quantum_operation(
                    "INITIALIZATION", "PERPLEXITY module initialized successfully"
                )
            except Exception as e:
                self._log_quantum_operation(
                    "ERROR", f"Failed to initialize PERPLEXITY module: {str(e)}"
                )

    def search_web(
        self,
        query: str,
        ethical_filter: bool = True,
        validation_level: str = "standard",
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Performs a web search using the PERPLEXITY subsystem.

        Args:
            query: Search query
            ethical_filter: Whether to apply ethical filters
            validation_level: Validation level ("basic", "standard", "strict")
            context: Additional query context

        Returns:
            Search results with quantum metadata
        """
        if not self.perplexity:
            return {
                "status": "error",
                "error_message": "PERPLEXITY module not available",
                "timestamp": datetime.now().isoformat(),
            }

        self._log_quantum_operation(
            "WEB_SEARCH", f"Starting query: '{query}'", f"Validation: {validation_level}"
        )

        try:
            results = self.perplexity.search(
                query=query,
                ethical_filter=ethical_filter,
                validation_level=validation_level,
                context=context,
            )

            if results.get("status") == "success":
                self._log_quantum_operation(
                    "SEARCH_COMPLETED",
                    f"Successful query: '{query}'",
                    f"Sources: {len(results.get('sources', []))}",
                )
            else:
                self._log_quantum_operation(
                    "SEARCH_FAILED",
                    f"Query failed: '{query}'",
                    results.get("reason", "Unknown reason"),
                )

            return results

        except Exception as e:
            error_message = f"Error during search: {str(e)}"
            self._log_quantum_operation("ERROR", error_message)

            return {
                "status": "error",
                "error_message": error_message,
                "timestamp": datetime.now().isoformat(),
                "query": query,
            }

    def get_web_search_history(self) -> List[Dict[str, str]]:
        """
        Returns the web search history.

        Returns:
            List of search history entries
        """
        if not self.perplexity:
            return []

        return self.perplexity.get_query_history()

    def clear_web_search_history(self) -> None:
        """Clears the web search history."""
        if self.perplexity:
            self.perplexity.clear_history()
            self._log_quantum_operation("HISTORY_CLEARED", "Web search history cleared")

    def get_logs(self) -> List[Dict[str, str]]:
        """
        Returns the logs of quantum operations.

        Returns:
            List of log entries
        """
        return self.log_entries

    def clear_logs(self) -> None:
        """Clears the logs of quantum operations."""
        self.log_entries = []

    def _log_quantum_operation(
        self, operation: str, details: str, context: Optional[str] = None
    ) -> None:
        """
        Generates a log in the standard EVA & GUARANI format.

        Args:
            operation: Type of operation being performed
            details: Details of the operation
            context: Additional context (optional)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {"timestamp": timestamp, "operation": operation, "details": details}

        if context:
            log_entry["context"] = context

        self.log_entries.append(log_entry)

        # Formatting for display
        log_text = f"[{timestamp}][QUANTUM_TOOLS][{operation}]"
        if context:
            log_text += f"\nCONTEXT: {context}"
        log_text += f"\nDETAILS: {details}"

        # In production, this log would be directed to an appropriate logging system
        print(log_text)


# Example of use:
if __name__ == "__main__":
    # Initialize the quantum tools
    tools = QuantumTools()

    # Check if the PERPLEXITY module is available
    if tools.perplexity:
        print("\nPERPLEXITY available. Performing test search...")

        # Perform a test search
        results = tools.search_web(
            "What is the current state of nuclear fusion technology in 2024?",
            validation_level="strict",
        )

        if results["status"] == "success":
            print("\n✅ Search performed successfully!")
            print("\nResult (preview):")
            content = str(results["content"])
            preview = content[:200] + "..." if len(content) > 200 else content
            print(preview)

            print("\nMain sources:")
            for source in results["sources"][:3]:
                print(f"- {source['title']} ({source['reliability']:.2f})")
        else:
            print(f"\n❌ Search failed: {results.get('error_message', 'Unknown error')}")

        # Display search history
        history = tools.get_web_search_history()
        print(f"\nHistory: {len(history)} search(es) performed")
    else:
        print("\nThe PERPLEXITY module is not available.")
        print("Run the setup_perplexity.py script to configure.")

    # Display logs
    print("\nOperation logs:")
    for log in tools.get_logs():
        print(f"[{log['timestamp']}] {log['operation']}: {log['details']}")

    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")
