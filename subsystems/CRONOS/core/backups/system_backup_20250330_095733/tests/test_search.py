#!/usr/bin/env python3
python
#!/usr/bin/env python3
"""
Web Search Test with EVA & GUARANI
----------------------------------
This script performs a test web query using the integration
with the Perplexity API implemented in the EVA & GUARANI system.
"""

import os
import sys
import json
from datetime import datetime

# Add the current directory to PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


def print_separator(title=None):
    """Prints a separator line with an optional title."""
    width = 80
    print("\n" + "=" * width)
    if title:
        print(f" {title} ".center(width))
        print("=" * width)


def print_quantum_box(content):
    """Prints content in a formatted quantum-style box."""
    lines = content.split("\n")
    max_length = max(len(line) for line in lines)
    width = min(max_length + 4, 100)

    print("\n╭" + "─" * width + "╮")

    for line in lines:
        while line:
            chunk = line[: width - 4]
            print("│ " + chunk.ljust(width - 4) + " │")
            line = line[width - 4 :]

    print("╰" + "─" * width + "╯")


def print_source(index, source):
    """Prints information about a source in a structured format."""
    reliability = source.get("reliability", 0)
    reliability_color = "green" if reliability >= 0.8 else "yellow" if reliability >= 0.6 else "red"

    print(f"\n[Source {index}]")
    print(f"  Title: {source.get('title', 'Not specified')}")
    print(f"  URL: {source.get('url', 'Not available')}")
    print(f"  Reliability: {reliability:.2f} ({reliability_color})")


# Main test
if __name__ == "__main__":
    print_separator("WEB SEARCH TEST WITH EVA & GUARANI")
    print("Performing a test query on the internet using integration with the Perplexity API...")

    try:
        # Import the QuantumTools module
        from EGOS.modules.quantum_tools import QuantumTools

        # Initialize quantum tools
        tools = QuantumTools()

        if not tools.perplexity:
            print("\n❌ Error: PERPLEXITY module is not available.")
            print("Check if the Perplexity API is configured correctly.")
            sys.exit(1)

        # Define the test query
        query = "What are the latest advancements in artificial intelligence in 2024?"

        print(f"\n🔍 Performing query: '{query}'")
        print("Please wait while we process your query...")

        # Perform the search
        results = tools.search_web(
            query=query, validation_level="strict"  # Use the maximum validation level
        )

        # Check the result
        if results.get("status") == "success":
            print("\n✅ Query performed successfully!")

            # Display the response content
            print("\n📝 Search result:")
            print_quantum_box(str(results["content"]))

            # Display metadata
            print("\n📊 Query metadata:")
            print(f"  Timestamp: {results['metadata']['timestamp']}")
            print(f"  Validation level: {results['metadata']['validation_level']}")
            print(f"  Confidence score: {results['metadata']['confidence_score']:.2f}")

            if results["metadata"].get("sensitivity_warning"):
                print(f"  ⚠️ Sensitivity warning: {results['metadata']['sensitivity_warning']}")

            # Display sources
            print(f"\n📚 Consulted sources ({len(results['sources'])} total):")
            for i, source in enumerate(results["sources"][:5], 1):
                print_source(i, source)

            if len(results["sources"]) > 5:
                print(f"\n... and {len(results['sources']) - 5} more sources not displayed")

            # Display potential biases
            if results.get("potential_biases"):
                print("\n⚖️ Potential biases detected:")
                for bias in results["potential_biases"]:
                    print(f"  - {bias}")

            # Display history
            history = tools.get_web_search_history()
            print(f"\n📜 Query history: {len(history)} query(ies) recorded")

        else:
            print(f"\n❌ Query failure: {results.get('error_message', 'Unknown error')}")

        # Display logs
        print("\n📋 Logs generated during the operation:")
        for log in tools.get_logs()[-5:]:  # Display only the last 5 logs
            print(f"  [{log['timestamp']}] {log['operation']}: {log['details']}")

    except ImportError as e:
        print(f"\n❌ Error importing necessary modules: {e}")
        print("Check if the directory structure is correct.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")
