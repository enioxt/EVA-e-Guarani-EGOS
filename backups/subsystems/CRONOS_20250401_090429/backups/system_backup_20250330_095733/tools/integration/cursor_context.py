#!/usr/bin/env python3
"""
Cursor Context Integration for Perplexity
Enriches Cursor's context with up-to-date information from Perplexity
"""

import os
import json
import asyncio
import logging
import argparse
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
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


class CursorContextEnricher:
    """
    Enriches Cursor's context with information from Perplexity
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the context enricher"""
        load_dotenv()
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        self.enabled = bool(self.api_key) and perplexity_enabled

        if not self.enabled:
            logger.warning(
                "Cursor context enrichment not enabled. Missing API key or Perplexity integration."
            )

        # Default context directory
        self.context_dir = Path(".cursor/context")
        self.context_dir.mkdir(parents=True, exist_ok=True)

    async def enrich_context(
        self, query: str, context_name: str, persona: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Enrich Cursor's context with information from Perplexity

        Args:
            query: The search query
            context_name: Name for the context file
            persona: Optional persona to use

        Returns:
            Status information
        """
        if not self.enabled:
            return {
                "status": "error",
                "error": "Context enrichment not enabled. Check API key and installation.",
            }

        try:
            # Initialize Perplexity integration
            integration = PerplexityIntegration(self.api_key)

            # Perform search
            result = await integration.enhance_knowledge(query, persona=persona)

            if result.get("status") != "success":
                return {
                    "status": "error",
                    "error": result.get("message", "Unknown error during search"),
                }

            # Format context data
            context_data = {
                "title": f"Perplexity Search: {query[:50]}{'...' if len(query) > 50 else ''}",
                "description": "Up-to-date information retrieved via Perplexity API",
                "query": query,
                "content": result.get("knowledge", {}).get("content", ""),
                "sources": result.get("knowledge", {}).get("sources", []),
                "timestamp": result.get("knowledge", {}).get("timestamp", ""),
                "reliability": result.get("knowledge", {}).get("reliability", 0),
            }

            if persona:
                context_data["persona"] = persona

            # Save to context file
            safe_name = "".join(c if c.isalnum() else "_" for c in context_name)
            context_file = self.context_dir / f"{safe_name}.json"

            with open(context_file, "w", encoding="utf-8") as f:
                json.dump(context_data, f, ensure_ascii=False, indent=2)

            logger.info(f"Context saved to {context_file}")

            return {
                "status": "success",
                "message": f"Context successfully enriched with Perplexity search results",
                "context_file": str(context_file),
            }

        except Exception as e:
            logger.error(f"Error enriching context: {str(e)}")
            return {"status": "error", "error": f"Exception during context enrichment: {str(e)}"}

    def list_contexts(self) -> List[Dict[str, Any]]:
        """
        List all available contexts

        Returns:
            List of context information
        """
        contexts = []

        try:
            for context_file in self.context_dir.glob("*.json"):
                try:
                    with open(context_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        contexts.append(
                            {
                                "name": context_file.stem,
                                "file": str(context_file),
                                "title": data.get("title", "Unknown"),
                                "timestamp": data.get("timestamp", "Unknown"),
                            }
                        )
                except Exception as e:
                    logger.error(f"Error reading context file {context_file}: {str(e)}")

            return contexts
        except Exception as e:
            logger.error(f"Error listing contexts: {str(e)}")
            return []

    def get_context(self, context_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific context by name

        Args:
            context_name: Name of the context

        Returns:
            Context data or None if not found
        """
        try:
            context_file = self.context_dir / f"{context_name}.json"

            if not context_file.exists():
                logger.error(f"Context file {context_file} not found")
                return None

            with open(context_file, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            logger.error(f"Error getting context {context_name}: {str(e)}")
            return None


async def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="Enrich Cursor's context with Perplexity search")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Enrich command
    enrich_parser = subparsers.add_parser("enrich", help="Enrich context with a search")
    enrich_parser.add_argument("query", help="Search query")
    enrich_parser.add_argument(
        "--name", "-n", help="Context name (defaults to 'perplexity_<timestamp>')"
    )
    enrich_parser.add_argument(
        "--persona", "-p", help="Persona to use (philosopher, scientist, etc.)"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List available contexts")

    # Get command
    get_parser = subparsers.add_parser("get", help="Get a specific context")
    get_parser.add_argument("name", help="Context name")

    args = parser.parse_args()

    enricher = CursorContextEnricher()

    if args.command == "enrich":
        # Generate default name if not provided
        if not args.name:
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            args.name = f"perplexity_{timestamp}"

        result = await enricher.enrich_context(args.query, args.name, args.persona)
        print(json.dumps(result, indent=2))

    elif args.command == "list":
        contexts = enricher.list_contexts()
        print(json.dumps(contexts, indent=2))

    elif args.command == "get":
        context = enricher.get_context(args.name)
        if context:
            print(json.dumps(context, indent=2))
        else:
            print(f"Context '{args.name}' not found")

    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
