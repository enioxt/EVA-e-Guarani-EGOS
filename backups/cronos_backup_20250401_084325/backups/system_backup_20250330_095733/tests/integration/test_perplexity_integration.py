#!/usr/bin/env python3
python
#!/usr/bin/env python3
"""
Script to test the integration with the Perplexity API using the OpenAI library.

This script checks if the communication with the Perplexity API is working
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
from pathlib import Path

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("TestPerplexity")

# Add root directory to path to help with imports
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


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


@pytest.mark.integration
def test_perplexity_setup():
    """
    Checks if the Perplexity module setup is correct.
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

    # Check the API key
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        # Try to load from configuration files
        try:
            # Try absolute imports first
            config_manager = None
            try:
                from core.config import config_manager

                print("✓ Configuration module imported from core.config")
            except ImportError:
                print("ℹ️ Configuration module core.config not found, using environment values")

                # Define a mock ConfigManager for tests
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


@pytest.mark.integration
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
                from core.config import config_manager

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
            from core.services.perplexity_service import PerplexityService
        except ImportError:
            logger.error("Could not import the PerplexityService module!")
            pytest.skip("PerplexityService module not found")

        perplexity_service = PerplexityService(api_key=api_key)
        logger.info("Perplexity service initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing the service: {str(e)}")
        traceback.print_exc()
        pytest.fail(f"Error initializing the service: {str(e)}")

    # Perform test search
    try:
        query = "What are the latest advancements in artificial intelligence in 2024?"
        logger.info(f"Performing search: {query}")

        # Use the "sonar" model (one of the officially supported models)
        result = perplexity_service.search(query, validate_level="normal", model="sonar")

        assert result is not None, "The search returned an empty result"
        assert isinstance(result, dict), "The result should be a dictionary"
        assert "content" in result, "The result should contain the 'content' field"
        assert "metadata" in result, "The result should contain the 'metadata' field"

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


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--capture=no", "-m", "integration"])
