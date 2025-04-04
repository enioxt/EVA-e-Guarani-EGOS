#!/usr/bin/env python3
python
#!/usr/bin/env python3
"""
Script to test integration with the Perplexity API using the OpenAI library.

This script checks if communication with the Perplexity API is working
correctly using our updated implementation.
"""

import os
import sys
import json
import datetime
from typing import Dict, Any, Optional, List
import traceback
import logging
import pytest

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("TestPerplexity")

# Add root directory to path to help with imports
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)


def print_separator(title=None):
    """
    Prints a visual separator to improve output readability.

    Args:
        title: Optional title to be displayed on the separator.
    """
    width = 80
    if title:
        print("\n" + "=" * width)
        print(f"{title.center(width)}")
        print("=" * width + "\n")
    else:
        print("\n" + "-" * width + "\n")


def print_quantum_box(content):
    """
    Prints content in a stylized quantum box.

    Args:
        content: Content to be displayed.
    """
    width = 80
    border_top = "╭" + "─" * (width - 2) + "╮"
    border_bottom = "╰" + "─" * (width - 2) + "╯"

    print(border_top)

    for line in content.split("\n"):
        chunks = [line[i : i + width - 4] for i in range(0, len(line), width - 4)]
        for chunk in chunks:
            print(f"│ {chunk.ljust(width-4)} │")

    print(border_bottom)


def print_source(index, source):
    """
    Prints information about a source in a formatted way.

    Args:
        index: Index of the source.
        source: Dictionary with source information.
    """
    title = source.get("title", "Title not available")
    url = source.get("url", "URL not available")
    reliability = source.get("reliability", "N/A")

    print(f"  [{index+1}] {title}")
    print(f"      URL: {url}")
    print(f"      Reliability: {reliability}")


def test_perplexity_setup():
    """
    Checks if the Perplexity module configuration is correct.
    """
    print_separator("CHECKING DEPENDENCIES")

    # Check OpenAI library
    try:
        import openai

        print("✓ 'openai' library installed correctly.")
    except ImportError:
        print("✗ 'openai' library is not installed!")
        print("  Run 'pip install openai' to install.")
        pytest.fail("OpenAI library is not installed")

    # Check API key
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        # Try to load from configuration files
        try:
            # Try absolute imports first
            config_manager = None
            try:
                sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
                from EGOS.services.config import config_manager

                print("✓ Configuration module imported from EGOS.services.config")
            except ImportError:
                print(
                    "ℹ️ Configuration module EGOS.services.config not found, using environment values"
                )

                # Define a mock ConfigManager for testing
                class ConfigManagerMock:
                    def get_key(self, service_name):
                        if service_name == "perplexity" and os.environ.get("PERPLEXITY_API_KEY"):
                            return os.environ.get("PERPLEXITY_API_KEY")
                        return None

                    def is_configured(self, service_name):
                        return self.get_key(service_name) is not None

                config_manager = ConfigManagerMock()

            # Try to get the API key
            if config_manager:
                api_key = config_manager.get_key("perplexity")
        except Exception as e:
            print(f"ℹ️ Error loading configuration: {str(e)}")
            print("  Trying to use environment variables...")

    # Check if the key was found
    if api_key:
        masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "****"
        print(f"✓ Perplexity API configured with key: {masked_key}")
    else:
        print("✗ Perplexity API key not found!")
        print("  Set the environment variable PERPLEXITY_API_KEY")
        pytest.skip("Perplexity API key not found")


def test_perplexity_search():
    """
    Tests the search functionality of the Perplexity API.
    """
    perplexity_service = None

    # Get the API key
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        try:
            # Try absolute imports first
            try:
                sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
                from EGOS.services.config import config_manager

                api_key = config_manager.get_key("perplexity")
            except ImportError:
                print("ℹ️ Configuration module not found, trying environment variables")
        except Exception as e:
            logger.error(f"Error getting API key: {str(e)}")

    if not api_key:
        logger.error("Perplexity API key not found!")
        pytest.skip("Perplexity API key not found")

    # Initialize the service
    try:
        # Try absolute imports first
        try:
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
            from EGOS.services.perplexity_service import PerplexityService
        except ImportError:
            logger.error("Could not import PerplexityService module!")
            pytest.skip("PerplexityService module not found")

        perplexity_service = PerplexityService(api_key=api_key)
        logger.info("Perplexity service initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing service: {str(e)}")
        traceback.print_exc()
        pytest.fail(f"Error initializing service: {str(e)}")

    # Perform test search
    try:
        query = "What are the latest advancements in artificial intelligence in 2024?"
        logger.info(f"Performing search: {query}")

        # Use the "sonar" model (one of the officially supported models)
        result = perplexity_service.search(query, validate_level="normal", model="sonar")

        assert result is not None, "Search returned an empty result"
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "content" in result, "Result should contain 'content' field"
        assert "metadata" in result, "Result should contain 'metadata' field"

        # Check basic metadata
        metadata = result["metadata"]
        assert "timestamp" in metadata, "Metadata should include timestamp"
        assert "validation_level" in metadata, "Metadata should include validation level"
        assert "validation_status" in metadata, "Metadata should include validation status"

        return result
    except Exception as e:
        logger.error(f"Error during search: {str(e)}")
        traceback.print_exc()
        pytest.fail(f"Error during search: {str(e)}")


def main():
    """
    Main function for executing the test.
    """
    print_separator("INTEGRATION TEST WITH PERPLEXITY API")
    print(f"Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check configuration
    if not test_perplexity_setup():
        print_separator("CONCLUSION")
        print("✗ Test failed in configuration check")
        return

    # Perform search
    print_separator("PERFORMING TEST SEARCH")
    result = test_perplexity_search()

    if not result:
        print_separator("CONCLUSION")
        print("✗ Test failed during search")
        print("  Check the errors above for more details.")
        return

    # Show results
    print_separator("SEARCH RESULTS")
    print_quantum_box(result["content"])

    # Show metadata
    print_separator("METADATA")
    metadata = result["metadata"]
    print(f"Timestamp: {metadata.get('timestamp', 'N/A')}")
    print(f"Validation Level: {metadata.get('validation_level', 'N/A')}")
    print(f"Validation Status: {metadata.get('validation_status', 'N/A')}")
    print(f"Confidence Score: {metadata.get('confidence_score', 'N/A')}")

    # Show sensitivity warnings
    warnings = metadata.get("warnings", [])
    if warnings:
        print_separator("WARNINGS")
        for warning in warnings:
            print(f"  - {warning}")

    # Show sources
    sources = metadata.get("sources", [])
    if sources:
        print_separator("CONSULTED SOURCES")

        # Limit display to 5 sources to avoid overwhelming the output
        for i, source in enumerate(sources[:5]):
            print_source(i, source)

        if len(sources) > 5:
            print(f"\n  ... and {len(sources) - 5} more sources")

    # Show potential biases
    biases = metadata.get("potential_biases", [])
    if biases:
        print_separator("POTENTIAL BIASES")
        for bias in biases:
            print(f"  - {bias}")

    print_separator("SEARCH HISTORY")
    history = metadata.get("search_history", {})
    print(f"Timestamp: {history.get('timestamp', 'N/A')}")
    print(f"Query: {history.get('query', 'N/A')}")
    print(f"Model: {history.get('model', 'N/A')}")

    print_separator("CONCLUSION")
    print("✓ Test completed successfully!")
    print("  Integration with the Perplexity API is working correctly.")


if __name__ == "__main__":
    main()
