#!/usr/bin/env python3
python
#!/usr/bin/env python3
"""
Demonstration Script - Integration of Perplexity API with EVA & GUARANI
-----------------------------------------------------------------------

This script demonstrates the use of the EVA & GUARANI system to perform
internet searches using the Perplexity API. It includes examples of
queries, ethical validation, and result handling.

Prerequisite: Perplexity API key configured via setup_perplexity."""

import os
import sys
import json
import time
from datetime import datetime

# Add the root directory to PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import the Perplexity integration module
try:
    from modules.perplexity_integration import PerplexityIntegration
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("\nEnsure you are running this script from the project's root directory.")
    sys.exit(1)


def print_header(title):
    """Prints a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_section(title):
    """Prints a formatted section title."""
    print(f"\n{'>'*3} {title} {'<'*3}")


def wait_for_user():
    """Waits for the user to press Enter to continue."""
    input("\n[Press Enter to continue]")


def print_quantum_box(content):
    """Prints content in a quantum-style formatted box."""
    width = 76
    print("\n╭" + "─" * width + "╮")

    for line in content.split("\n"):
        while line:
            print("│ " + line[: width - 2].ljust(width - 2) + " │")
            line = line[width - 2 :]

    print("╰" + "─" * width + "╯")


def run_demo():
    """Runs the demonstration of integration with the Perplexity API."""
    print_header("Demonstration of EVA & GUARANI Integration with Perplexity API")

    print(
        """
This demo shows how the EVA & GUARANI system uses the Perplexity API
to perform internet searches with ethical validation and quantum
processing of results.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
    """
    )

    # Check if the API is configured
    try:
        print_section("Initializing Quantum Integration")
        print("Checking Perplexity API configuration...")

        perplexity = PerplexityIntegration()
        print("✅ Perplexity API configured successfully!")

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease run the setup_perplexity.py script to configure the API.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

    # Example 1: Basic query
    print_section("Example 1: Basic News Query")
    print("Demonstration of a simple query about recent news.")
    wait_for_user()

    query = "What are the main technological news of the last week?"
    print(f"\nQuery: '{query}'")
    print("Processing...")

    try:
        results = perplexity.search(query)

        if results["status"] == "success":
            print("\n✅ Query successfully performed!")

            # Show result
            print_quantum_box(str(results["content"]))

            # Show metadata
            print_section("Query Metadata")
            print(f"Timestamp: {results['metadata']['timestamp']}")
            print(f"Validation level: {results['metadata']['validation_level']}")
            print(f"Confidence score: {results['metadata']['confidence_score']:.2f}")

            # Show sources
            print_section("Consulted Sources")
            for i, source in enumerate(results["sources"], 1):
                print(f"{i}. {source['title']}")
                print(f"   URL: {source['url']}")
                print(f"   Estimated reliability: {source['reliability']:.2f}")
                print()
        else:
            print(f"\n❌ Query failed: {results.get('reason', 'Unknown error')}")

    except Exception as e:
        print(f"\n❌ Error during query: {e}")

    # Example 2: Query with ethical analysis (rejected)
    wait_for_user()
    print_section("Example 2: Query with Ethical Verification")
    print("Demonstration of how the system handles potentially problematic queries.")
    wait_for_user()

    problematic_query = "How to hack someone's email account"
    problematic_context = "I am trying to access someone's account without permission"

    print(f"\nQuery: '{problematic_query}'")
    print(f"Context: '{problematic_context}'")
    print("Processing with contextual ethical analysis...")

    try:
        results = perplexity.search(
            problematic_query,
            ethical_filter=True,
            validation_level="strict",
            context=problematic_context,
        )

        if results["status"] == "rejected":
            print("\n🛑 Query rejected for ethical reasons")
            print(f"Reason: {results['reason']}")
            print(f"Ethical analysis: {results['ethical_analysis']}")

            if "alternative_suggestion" in results:
                print(f"Alternative suggestion: {results['alternative_suggestion']}")
        else:
            print("\n⚠️ The ethical query was not rejected as expected.")

    except Exception as e:
        print(f"\n❌ Error during query: {e}")

    # Example 3: Technical query with strict validation
    wait_for_user()
    print_section("Example 3: Technical Query with Strict Validation")
    print("Demonstration of a technical query with the highest level of validation.")
    wait_for_user()

    technical_query = "What are the best security practices for REST APIs in 2024?"
    print(f"\nQuery: '{technical_query}'")
    print("Processing with strict validation...")

    try:
        results = perplexity.search(technical_query, ethical_filter=True, validation_level="strict")

        if results["status"] == "success":
            print("\n✅ Technical query successfully performed!")

            # Show result
            content = str(results["content"])
            preview = content[:500] + "..." if len(content) > 500 else content
            print_quantum_box(preview)

            # Show technical sources
            print_section("Technical Sources")
            for i, source in enumerate(results["sources"], 1):
                if source["reliability"] >= 0.8:  # Filter only highly reliable sources
                    print(f"{i}. {source['title']} ({source['reliability']:.2f})")
                    print(f"   {source['url']}")
                    print()

            # Display validation note if it exists
            if results.get("validation_note"):
                print_section("Validation Note")
                print(results["validation_note"])
        else:
            print(f"\n❌ Query failed: {results.get('reason', 'Unknown error')}")

    except Exception as e:
        print(f"\n❌ Error during technical query: {e}")

    # Example 4: Query history
    wait_for_user()
    print_section("Example 4: Query History")
    print("Demonstration of the logging of performed query history.")

    history = perplexity.get_query_history()

    print(f"\nQuery History: {len(history)} query(ies) performed")
    for i, entry in enumerate(history, 1):
        print(f"\n{i}. Query: '{entry['query']}'")
        print(f"   Timestamp: {entry['timestamp']}")
        if entry.get("context"):
            print(f"   Context: '{entry['context']}'")

    # Conclusion of the demonstration
    wait_for_user()
    print_header("Conclusion of the Demonstration")

    print(
        """
The integration of the Perplexity API with the EVA & GUARANI system
enables internet searches with:

1. Strict ethical validation of queries
2. Reliability assessment of sources
3. Detection of potential biases
4. Quantum formatting of results
5. Detailed operation logging
6. Historical query logging

This implementation follows the fundamental principles of the EVA & GUARANI system:
- Integrated ethics
- Unconditional love
- Systemic cartography
- Modular analysis
- Evolutionary preservation

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
    """
    )


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by the user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error during demonstration: {e}")
        sys.exit(1)
