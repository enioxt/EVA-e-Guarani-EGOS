#!/usr/bin/env python3
python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✧༺❀༻∞ ATLAS - Systemic Cartography Demo ∞༺❀༻✧
====================================================

This script demonstrates the capabilities of the EGOS ATLAS subsystem,
allowing you to map and visualize the structure of a project.

Usage:
    python atlas_demo.py --project /path/to/project [--output format] [--export directory]

Author: EGOS Community
Version: 1.0.0
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path

# Add root directory to path to import modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("ATLAS.Demo")


# Terminal colors
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_colored(message, color=Colors.CYAN, bold=False):
    """Prints a colored message to the terminal."""
    prefix = Colors.BOLD if bold else ""
    print(f"{prefix}{color}{message}{Colors.ENDC}")


def print_banner():
    """Displays the ATLAS banner."""
    banner = f"""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║                       ✧༺❀༻∞ ATLAS ∞༺❀༻✧                          ║
║                      Systemic Cartography                          ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """
    print_colored(banner, Colors.CYAN, bold=True)
    print_colored("Demonstration of the EGOS cartography subsystem\n", Colors.BLUE)


def parse_arguments():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="ATLAS - Systemic Cartography")
    parser.add_argument(
        "--project", type=str, required=True, help="Path to the project to be mapped"
    )
    parser.add_argument(
        "--output", type=str, default="json", choices=["json", "md", "html"], help="Output format"
    )
    parser.add_argument("--export", type=str, help="Directory to export visualization for Obsidian")
    parser.add_argument("--config", type=str, help="Path to custom configuration file")
    return parser.parse_args()


def main():
    """Main function."""
    # Display banner
    print_banner()

    # Parse arguments
    args = parse_arguments()

    # Check if the project exists
    if not os.path.exists(args.project):
        print_colored(f"Error: The project path '{args.project}' does not exist", Colors.RED)
        return 1

    print_colored(f"Mapping project: {args.project}", Colors.BLUE)
    print_colored(f"Output format: {args.output}", Colors.BLUE)

    try:
        # Import the ATLAS module
        from core.atlas import AtlasModule

        # Configuration
        config_path = args.config
        if not config_path:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "config",
                "modules",
                "atlas_config.json",
            )

        # Initialize ATLAS
        print_colored("Initializing ATLAS...", Colors.BLUE)
        atlas = AtlasModule(config_path)

        # Map the project
        print_colored("Mapping project structure...", Colors.BLUE)
        mapping = atlas.map_project(args.project, args.output)

        # Display statistics
        print_colored("\nMapping statistics:", Colors.GREEN, bold=True)
        print(f"  Project: {mapping['project']}")
        print(f"  Path: {mapping['path']}")
        print(f"  Timestamp: {mapping['timestamp']}")
        print(f"  Nodes: {len(mapping['nodes'])}")
        print(f"  Connections: {len(mapping['edges'])}")
        print(f"  Metrics:")
        print(f"    - Files: {mapping['metrics']['files']}")
        print(f"    - Directories: {mapping['metrics']['directories']}")
        print(f"    - Connections: {mapping['metrics']['connections']}")
        print(f"    - Complexity: {mapping['metrics']['complexity']}")

        # Generate visualization
        print_colored("\nGenerating visualization...", Colors.BLUE)
        visualization_path = atlas.visualize_mapping(mapping)
        print_colored(f"Visualization generated at: {visualization_path}", Colors.GREEN)

        # Export to Obsidian if requested
        if args.export:
            print_colored(f"\nExporting to Obsidian at: {args.export}", Colors.BLUE)
            files = atlas.export_to_obsidian(mapping, args.export)
            print_colored(f"Export completed: {len(files)} files generated", Colors.GREEN)
            for file in files:
                print(f"  - {file}")

        print_colored("\n⊹⊱∞⊰⊹ ATLAS: Mapping with Love ⊹⊰∞⊱⊹\n", Colors.CYAN, bold=True)
        return 0

    except ImportError as e:
        print_colored(f"Error importing ATLAS: {str(e)}", Colors.RED)
        return 1
    except Exception as e:
        print_colored(f"Error during execution: {str(e)}", Colors.RED)
        logger.error(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
