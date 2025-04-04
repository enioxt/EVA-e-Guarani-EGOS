#!/usr/bin/env python3
python
"""
Perplexity Integration Module with EVA & GUARANI
------------------------------------------------
This module establishes the connection between the EVA & GUARANI quantum system
and the Perplexity API, allowing internet searches with ethical information
handling and source validation.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

# Add the root directory to PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
egos_dir = os.path.dirname(current_dir)
if egos_dir not in sys.path:
    sys.path.append(egos_dir)

# Import services and configurations
from services.perplexity_service import PerplexityService
from services.config import config_manager


class PerplexityIntegration:
    """
    Integration between the EVA & GUARANI system and the Perplexity API.
    Provides methods for internet search with ethical validation.
    """

    def __init__(self):
        """Initializes the integration with the Perplexity API."""
        self._ensure_api_configured()
        self.perplexity = PerplexityService()
        self.last_search_results = None
        self.query_history = []

    def _ensure_api_configured(self) -> None:
        """Checks if the Perplexity API is configured."""
        if not config_manager.is_configured("perplexity"):
            raise ValueError(
                "Perplexity API not configured. Run the setup_perplexity.py script "
                "or set the PERPLEXITY_API_KEY environment variable."
            )

    def search(
        self,
        query: str,
        ethical_filter: bool = True,
        validation_level: str = "standard",
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Performs an internet search using the Perplexity API.

        Args:
            query: Search query
            ethical_filter: Whether to apply ethical filters (default: True)
            validation_level: Validation level ("basic", "standard", "strict")
            context: Additional query context for ethical analysis

        Returns:
            Processed results with validation metadata
        """
        # Quantum log in EVA & GUARANI format
        self._log_quantum_operation("INTERNET_SEARCH", query, context)

        # Additional ethics check based on context
        if context:
            ethics_assessment = self._assess_query_ethics(query, context)
            if not ethics_assessment["is_appropriate"]:
                return {
                    "status": "rejected",
                    "reason": ethics_assessment["reason"],
                    "timestamp": datetime.now().isoformat(),
                    "ethical_analysis": ethics_assessment["analysis"],
                    "alternative_suggestion": ethics_assessment.get("alternative"),
                }

        # Register history
        self.query_history.append(
            {"timestamp": datetime.now().isoformat(), "query": query, "context": context}
        )

        # Perform search via PerplexityService
        results = self.perplexity.search(
            query, ethical_filter=ethical_filter, validation_level=validation_level
        )

        # Store results for reference
        self.last_search_results = results

        # Process results in EVA & GUARANI format
        processed_results = self._process_for_quantum_system(results)

        # Completion log
        if results.get("status") == "success":
            self._log_quantum_operation(
                "SEARCH_COMPLETED",
                f"Query: {query[:30]}...",
                f"Sources: {len(results.get('sources', []))}",
            )
        else:
            self._log_quantum_operation(
                "SEARCH_FAILED",
                f"Query: {query[:30]}...",
                results.get("error_message", "Unknown error"),
            )

        return processed_results

    def _assess_query_ethics(self, query: str, context: str) -> Dict[str, Any]:
        """
        Performs a deeper ethical assessment of the query based on context.

        Args:
            query: Query to be evaluated
            context: Query context (e.g., previous conversation)

        Returns:
            Detailed ethical assessment
        """
        # This is a simplified version. In production, a more sophisticated AI model
        # would be used for contextual ethical analysis.

        query_lower = query.lower()
        context_lower = context.lower()

        # Detect malicious intents based on context
        malicious_patterns = [
            ("hack", "breach", "access account"),
            ("bypass", "deceive", "fraud"),
            ("pornography", "illegal material"),
            ("bypass security", "bypass"),
        ]

        for pattern_set in malicious_patterns:
            query_matches = any(pattern in query_lower for pattern in pattern_set)
            context_matches = any(pattern in context_lower for pattern in pattern_set)

            if query_matches and context_matches:
                return {
                    "is_appropriate": False,
                    "reason": "The query, when analyzed in context, appears to request information on potentially unethical or illegal activities.",
                    "analysis": f"Patterns detected in both the query and context: {pattern_set}",
                    "alternative": "Consider rephrasing your query to focus on educational or defensive security aspects.",
                }

        # If no issues
        return {
            "is_appropriate": True,
            "reason": "Query approved in contextual ethical check",
            "analysis": "No problematic patterns detected in the query context.",
        }

    def _process_for_quantum_system(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes search results for the EVA & GUARANI system format.

        Args:
            results: Raw search results

        Returns:
            Results formatted for the quantum system
        """
        if results.get("status") != "success":
            return results

        # Prepare the result for the EVA & GUARANI format
        quantum_results = {
            "status": results["status"],
            "query": results["query"],
            "content": results["results"],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "validation_level": results.get("validation_metadata", {}).get("validation_level"),
                "confidence_score": results.get("validation_metadata", {}).get(
                    "confidence_score", 0.7
                ),
                "sensitive_topic_warning": results.get("sensitive_topic_warning", None),
            },
            "sources": [
                {
                    "title": source.get("title", "Not specified"),
                    "url": source.get("url", ""),
                    "reliability": self._estimate_source_reliability(source),
                }
                for source in results.get("sources", [])
            ],
            "potential_biases": results.get("potential_biases", []),
            "validation_note": results.get("validation_note", ""),
        }

        return quantum_results

    def _estimate_source_reliability(self, source: Dict[str, Any]) -> float:
        """
        Estimates the reliability of a source based on heuristics.

        Args:
            source: Information about the source

        Returns:
            Reliability score between 0.0 and 1.0
        """
        # Simplified implementation
        # In production, it would be based on lists of reliable sources,
        # domain verification, etc.

        # Base score
        reliability = 0.7

        # Academic and governmental domains have higher reliability
        url = source.get("url", "").lower()
        if url:
            if url.endswith((".edu", ".gov", ".org")):
                reliability += 0.1
            elif "wikipedia.org" in url:
                reliability += 0.05
            elif any(domain in url for domain in ["news", "blog", "forum"]):
                reliability -= 0.1

        # Very sensationalist titles may indicate lower reliability
        title = source.get("title", "").lower()
        sensational_terms = [
            "unbelievable",
            "shocking",
            "you won't believe",
            "revealed",
            "secret",
            "exclusive",
            "surprising",
        ]
        if any(term in title for term in sensational_terms):
            reliability -= 0.15

        return max(min(reliability, 1.0), 0.1)  # Limit between 0.1 and 1.0

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
        log_entry = f"[{timestamp}][ATLAS][PERPLEXITY][{operation}]"

        if context:
            log_entry += f"\nCONTEXT: {context}"

        log_entry += f"\nDETAILS: {details}"

        # Recommendations for better results
        if operation == "SEARCH":
            log_entry += (
                "\nRECOMMENDATIONS: For better results, use specific queries and avoid ambiguities."
            )

        # Ethical reflection for searches
        log_entry += "\nETHICAL REFLECTION: Internet information should be verified across multiple reliable sources."

        # In production, this log would be directed to an appropriate logging system
        print(log_entry)

    def get_query_history(self) -> List[Dict[str, str]]:
        """
        Returns the history of performed queries.

        Returns:
            List of queries with timestamp and context
        """
        return self.query_history

    def clear_history(self) -> None:
        """Clears the query history."""
        self.query_history = []
        self.last_search_results = None


# Example of use:
if __name__ == "__main__":
    try:
        perplexity_integration = PerplexityIntegration()

        test_query = "What are the main technological innovations of 2024?"
        print(f"\nPerforming query: '{test_query}'")

        results = perplexity_integration.search(test_query)

        if results["status"] == "success":
            print("\n✅ Query performed successfully!")
            print(f"\nResult (preview):")

            content_preview = (
                str(results["content"])[:300] + "..."
                if len(str(results["content"])) > 300
                else str(results["content"])
            )
            print(content_preview)

            print(f"\nSources found: {len(results['sources'])}")
            for i, source in enumerate(results["sources"][:3], 1):
                print(f"  {i}. {source['title']} (Reliability: {source['reliability']:.2f})")

            if len(results["sources"]) > 3:
                print(f"  ... and {len(results['sources']) - 3} more sources")

            print(f"\nValidation level: {results['metadata']['validation_level']}")
            print(f"Confidence score: {results['metadata']['confidence_score']:.2f}")

            if results["potential_biases"]:
                print("\nPotential biases detected:")
                for bias in results["potential_biases"]:
                    print(f"  - {bias}")
        else:
            print("\n❌ Query failed:")
            print(results.get("reason", "Unknown error"))

    except ValueError as e:
        print(f"\n❌ Configuration error: {str(e)}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
