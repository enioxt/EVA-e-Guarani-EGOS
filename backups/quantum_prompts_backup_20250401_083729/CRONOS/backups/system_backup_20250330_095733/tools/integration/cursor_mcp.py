#!/usr/bin/env python3
"""
Cursor Model Context Protocol (MCP) for Perplexity Integration
Allows EVA & GUARANI to use Perplexity search directly from Cursor
"""

import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Perplexity integration
try:
    from tools.integration.perplexity_integration import PerplexityIntegration

    perplexity_enabled = True
except ImportError:
    logger.error(
        "Failed to import PerplexityIntegration. Make sure the module is properly installed."
    )
    perplexity_enabled = False


def perplexity_search(query: str, persona: Optional[str] = None) -> Dict[str, Any]:
    """
    Search the web with Perplexity AI from Cursor MCP

    Args:
        query: The search query
        persona: Optional persona to use (philosopher, scientist, etc.)

    Returns:
        Dictionary with search results
    """
    if not perplexity_enabled:
        return {
            "error": "Perplexity integration not available. Please check installation.",
            "status": "error",
        }

    # Run the async search in a synchronous wrapper
    result = asyncio.run(_async_perplexity_search(query, persona))
    return result


async def _async_perplexity_search(query: str, persona: Optional[str] = None) -> Dict[str, Any]:
    """Async implementation of the Perplexity search"""
    try:
        # Load environment variables
        load_dotenv()

        # Get API key from environment
        api_key = os.getenv("PERPLEXITY_API_KEY")

        if not api_key:
            return {
                "error": "PERPLEXITY_API_KEY not found in environment variables.",
                "status": "error",
            }

        # Initialize the Perplexity integration
        integration = PerplexityIntegration(api_key)

        # Perform the search
        result = await integration.enhance_knowledge(query, persona=persona)

        # Format output for Cursor display
        if result.get("status") == "success":
            # Get content and sources
            content = result.get("knowledge", {}).get("content", "No results found.")
            sources = result.get("knowledge", {}).get("sources", [])

            # Format sources as markdown list
            sources_md = []
            if sources:
                for i, source in enumerate(sources, 1):
                    if "title" in source and "url" in source:
                        sources_md.append(f"{i}. [{source['title']}]({source['url']})")
                    elif "url" in source:
                        sources_md.append(f"{i}. {source['url']}")

            # Check for ethical warnings
            warning = None
            if "ethical_warning" in result.get("knowledge", {}):
                warning = result["knowledge"]["ethical_warning"]

            # Format for Cursor display
            cursor_result = {
                "status": "success",
                "query": query,
                "content": content,
                "sources": sources_md,
                "warning": warning,
                "reliability": result.get("knowledge", {}).get("reliability", 0.0),
                "timestamp": result.get("knowledge", {}).get("timestamp", ""),
                "persona": persona,
            }

            # Also save to JSON file for reference
            with open("perplexity_result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            return cursor_result
        else:
            # Return error details
            return {
                "status": "error",
                "error": result.get("message", "Unknown error during search"),
                "query": query,
            }

    except Exception as e:
        logger.error(f"Error during Perplexity search: {str(e)}")
        return {"status": "error", "error": f"Exception during search: {str(e)}", "query": query}


if __name__ == "__main__":
    # Simple test when run directly
    result = perplexity_search("What is quantum computing?", "scientist")
    print(json.dumps(result, indent=2))
