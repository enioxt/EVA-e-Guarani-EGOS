#!/usr/bin/env python3
python
#!/usr/bin/env python
"""
Perplexity API Setup Script - EVA & GUARANI
-------------------------------------------
This script sets up the Perplexity API key for use in the EVA & GUARANI system.
"""

import sys
import os
from services.config import config_manager


def setup_perplexity_api():
    """Sets up the Perplexity API key for the system."""
    print("\n========== Perplexity API Setup ==========")
    print("This script will set up the Perplexity API key for the EVA & GUARANI system.")

    # Check if already configured
    if config_manager.is_configured("perplexity"):
        existing_key = config_manager.get_key("perplexity")
        masked_key = f"{existing_key[:8]}...{existing_key[-4:]}" if existing_key else ""
        print(f"\nA Perplexity API key is already configured: {masked_key}")

        choice = input("\nDo you want to replace it? (y/n): ").strip().lower()
        if choice != "y":
            print("Setup canceled. The existing API key will be retained.")
            return

    # Obtain the new API key
    print("\nYou can obtain a Perplexity API key at: https://www.perplexity.ai/settings/api")

    # Use the API key provided as an argument or prompt the user
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        print("\nAPI key provided via command line argument.")
    else:
        api_key = input("\nEnter your Perplexity API key: ").strip()

    if not api_key.startswith("pplx-"):
        print(
            "\nWARNING: The provided API key does not appear to be valid (must start with 'pplx-')."
        )
        confirm = input("Do you want to continue anyway? (y/n): ").strip().lower()
        if confirm != "y":
            print("Setup canceled.")
            return

    # Save the API key
    config_manager.set_key("perplexity", api_key)
    print("\nPerplexity API key successfully configured!")

    # Additional information
    print("\nThe API key is stored in:", config_manager.config_path)
    print("To use the API in a production environment, consider setting")
    print("the PERPLEXITY_API_KEY environment variable instead of storing it in the file.")

    # Test connection
    print("\nDo you want to test the connection to the API? (y/n): ", end="")
    test_choice = input().strip().lower()
    if test_choice == "y":
        test_perplexity_connection()


def test_perplexity_connection():
    """Tests the connection to the Perplexity API."""
    try:
        from services.perplexity_service import PerplexityService

        print("\nTesting connection to the Perplexity API...")
        perplexity = PerplexityService()

        test_query = "What is today's date?"
        print(f"\nTest query: '{test_query}'")

        results = perplexity.search(test_query)

        if results.get("status") == "success":
            print("\n✅ Connection successfully established!")
            print("\nExample of result:")
            if "results" in results:
                # Show only a preview of the result to avoid overloading the terminal
                result_preview = (
                    str(results["results"])[:200] + "..."
                    if len(str(results["results"])) > 200
                    else str(results["results"])
                )
                print(result_preview)

            if "sources" in results:
                print(f"\nSources: {len(results['sources'])} found")
        else:
            print("\n❌ Connection failed:")
            print(results.get("error_message", "Unknown error"))

    except ImportError:
        print("\n❌ Error: PerplexityService module not found.")
    except Exception as e:
        print(f"\n❌ Error during the test: {str(e)}")


if __name__ == "__main__":
    # Adjust PYTHONPATH to access modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    setup_perplexity_api()
