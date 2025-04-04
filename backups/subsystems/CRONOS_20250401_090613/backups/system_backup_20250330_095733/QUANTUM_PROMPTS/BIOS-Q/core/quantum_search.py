#!/usr/bin/env python3
"""
Quantum Search - EVA & GUARANI Core Module
----------------------------------------
This module implements the Quantum Search system that provides
intelligent search capabilities across all subsystems.

Version: 7.5
Created: 2025-03-26
"""

import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
import asyncio

# Import Mycelium Network
from .mycelium_network import mycelium

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("quantum-search")


class QuantumSearchIndex:
    """Manages the quantum search index."""

    def __init__(self):
        self.index: Dict[str, Dict[str, Any]] = {}
        self.last_update = datetime.now()

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any]) -> None:
        """Add a document to the index."""
        self.index[doc_id] = {
            "content": content,
            "metadata": metadata,
            "indexed_at": datetime.now(),
        }
        self.last_update = datetime.now()

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document from the index."""
        if doc_id in self.index:
            del self.index[doc_id]
            self.last_update = datetime.now()
            return True
        return False

    def search(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search the index using quantum-inspired algorithms.
        This is a simplified version - in production, we would use
        more sophisticated quantum-inspired search algorithms.
        """
        results = []

        for doc_id, doc in self.index.items():
            # Simple relevance calculation (to be replaced with quantum algorithm)
            relevance = self._calculate_relevance(query, doc["content"])

            # Apply filters if any
            if filters and not self._matches_filters(doc["metadata"], filters):
                continue

            results.append(
                {
                    "doc_id": doc_id,
                    "relevance": relevance,
                    "metadata": doc["metadata"],
                    "indexed_at": doc["indexed_at"],
                }
            )

        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results

    def _calculate_relevance(self, query: str, content: str) -> float:
        """Calculate relevance score between query and content."""
        # This is a simplified implementation
        # In production, we would use quantum-inspired algorithms
        query_terms = query.lower().split()
        content_terms = content.lower().split()

        matches = sum(1 for term in query_terms if term in content_terms)
        return matches / len(query_terms) if query_terms else 0.0

    def _matches_filters(self, metadata: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if document metadata matches the filters."""
        return all(metadata.get(key) == value for key, value in filters.items())


class QuantumSearch:
    """
    The Quantum Search system that provides intelligent search
    capabilities across all EVA & GUARANI subsystems.
    """

    def __init__(self):
        self.index = QuantumSearchIndex()
        self.node = mycelium.get_node("QUANTUM_SEARCH")
        if not self.node:
            self.node = mycelium.register_node("QUANTUM_SEARCH", "search")

    async def index_directory(self, directory: str, recursive: bool = True) -> None:
        """Index all files in a directory."""
        path = Path(directory)
        if not path.exists():
            logger.error(f"Directory not found: {directory}")
            return

        async def _process_file(file_path: Path) -> None:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                metadata = {
                    "filename": file_path.name,
                    "extension": file_path.suffix,
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
                }

                self.index.add_document(str(file_path), content, metadata)
                logger.info(f"Indexed: {file_path}")

            except Exception as e:
                logger.error(f"Error indexing {file_path}: {str(e)}")

        # Process files concurrently
        tasks = []
        pattern = "**/*" if recursive else "*"

        for file_path in path.glob(pattern):
            if file_path.is_file():
                tasks.append(_process_file(file_path))

        if tasks:
            await asyncio.gather(*tasks)

    async def search(
        self, query: str, filters: Optional[Dict[str, Any]] = None, propagate: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Perform a quantum search across all indexed content.

        Args:
            query: The search query
            filters: Optional filters to apply
            propagate: Whether to propagate the search through the Mycelium network
        """
        results = self.index.search(query, filters)

        if propagate:
            # Propagate search through the Mycelium network
            search_data = {
                "type": "search",
                "query": query,
                "filters": filters,
                "timestamp": datetime.now().isoformat(),
            }

            await mycelium.propagate_update("QUANTUM_SEARCH", search_data)

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get search system statistics."""
        return {
            "total_documents": len(self.index.index),
            "last_update": self.index.last_update.isoformat(),
            "connected_nodes": len(self.node.connections) if self.node else 0,
        }


# Initialize the global quantum search system
quantum_search = QuantumSearch()

if __name__ == "__main__":
    # Test the search system
    async def test_search():
        print("\n✧༺❀༻∞ EVA & GUARANI - Quantum Search Test ∞༺❀༻✧\n")

        # Index the current directory
        print("Indexing files...")
        await quantum_search.index_directory(".")

        # Perform a test search
        query = "quantum mycelium network"
        print(f"\nSearching for: {query}")

        results = await quantum_search.search(query)

        print("\nSearch Results:")
        for result in results[:5]:  # Show top 5 results
            print(f"\n- Document: {result['doc_id']}")
            print(f"  Relevance: {result['relevance']:.2f}")
            print(f"  Indexed: {result['metadata']['indexed_at']}")

        # Print stats
        stats = quantum_search.get_stats()
        print(f"\nSystem Stats:")
        print(f"Total Documents: {stats['total_documents']}")
        print(f"Last Update: {stats['last_update']}")
        print(f"Connected Nodes: {stats['connected_nodes']}")

        print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

    # Run the test
    asyncio.run(test_search())
