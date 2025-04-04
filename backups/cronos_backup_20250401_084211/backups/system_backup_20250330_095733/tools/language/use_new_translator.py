#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Translator Redirect
This script redirects users to the new translator implementation.
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """Redirect to new translator implementation"""
    print("\n" + "=" * 80)
    print(" EVA & GUARANI - TRANSLATOR MIGRATION NOTICE ".center(80, "="))
    print("=" * 80 + "\n")

    print("The translator has been migrated to a new location with enhanced features:\n")
    print("  OLD LOCATION: /tools/language/")
    print("  NEW LOCATION: /modules/translator_dev/\n")

    print("The new translator includes:")
    print("  • Multiple translation engines (HuggingFace, OpenAI)")
    print("  • Smart caching system")
    print("  • Format-specific handlers for different file types")
    print("  • Technical terminology management")
    print("  • Cost monitoring and budget controls")
    print("  • Concurrent batch processing")
    print("  • Enhanced user interface\n")

    # Determine root directory
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    root_dir = current_dir.parent.parent  # Move up from /tools/language to root

    # Path to new translator
    new_translator = root_dir / "modules" / "translator_dev" / "translator.py"

    # Check if new translator exists
    if not new_translator.exists():
        print(f"ERROR: New translator not found at {new_translator}")
        print("Please check the installation or contact the administrator.")
        return 1

    print(f"To use the new translator, run:")
    print(f"  python {new_translator.relative_to(root_dir)} [OPTIONS]")
    print("\nExample commands:")
    print(f"  python {new_translator.relative_to(root_dir)} --scan path/to/directory")
    print(f"  python {new_translator.relative_to(root_dir)} --file path/to/file.md")
    print(f"  python {new_translator.relative_to(root_dir)} --translate path/to/directory")
    print(
        f"  python {new_translator.relative_to(root_dir)} --translate path/to/directory --engine huggingface\n"
    )

    # Ask if user wants to run the new translator
    while True:
        choice = input("Would you like to run the new translator now? (y/n): ").strip().lower()
        if choice in ["y", "yes"]:
            # Pass all command line arguments to the new translator
            args = [sys.executable, str(new_translator)] + sys.argv[1:]
            print(f"\nLaunching: {' '.join(args)}\n")
            return subprocess.call(args)
        elif choice in ["n", "no"]:
            print("\nExiting. Please use the new translator for future translations.")
            return 0
        else:
            print("Please enter 'y' or 'n'")


if __name__ == "__main__":
    sys.exit(main())
