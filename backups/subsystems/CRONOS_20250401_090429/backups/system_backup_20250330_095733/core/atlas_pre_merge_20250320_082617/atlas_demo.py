#!/usr/bin/env python3
python
#!/usr/bin/env python3
"""
EGOS - ATLAS Demo
================

This script demonstrates how to use the ATLAS subsystem to map
the structure of a project and visualize it.

Version: 1.0.0
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add the root directory to the path to import EGOS modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.atlas.atlas_core import ATLASCore
except ImportError:
    print("Error: Could not import the ATLAS module.")
    print("Ensure that EGOS is installed correctly.")
    sys.exit(1)


def scan_project_structure(project_path):
    """
    Scans the structure of a project and creates a mapping for ATLAS.

    Args:
        project_path: Path to the project directory

    Returns:
        dict: Project structure in a format compatible with ATLAS
    """
    project_path = Path(project_path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print(f"Error: The path {project_path} does not exist or is not a directory.")
        sys.exit(1)

    # Structure for ATLAS
    system_data = {"nodes": {}, "edges": []}

    # Map directories and files
    for root, dirs, files in os.walk(project_path):
        root_path = Path(root)
        rel_path = root_path.relative_to(project_path)
        node_id = str(rel_path)

        if node_id == ".":
            node_id = project_path.name
            node_type = "project"
        else:
            node_type = "directory"

        # Add node for the directory
        system_data["nodes"][node_id] = {
            "type": node_type,
            "path": str(rel_path),
            "description": f"Directory: {node_id}",
        }

        # Add nodes for files
        for file in files:
            file_path = root_path / file
            file_rel_path = file_path.relative_to(project_path)
            file_id = str(file_rel_path)

            # Determine file type
            file_type = "file"
            if file.endswith((".py", ".pyw")):
                file_type = "python"
            elif file.endswith((".js", ".jsx", ".ts", ".tsx")):
                file_type = "javascript"
            elif file.endswith((".html", ".htm")):
                file_type = "html"
            elif file.endswith((".css", ".scss", ".sass")):
                file_type = "css"
            elif file.endswith((".md", ".markdown")):
                file_type = "markdown"
            elif file.endswith((".json", ".yaml", ".yml", ".toml")):
                file_type = "config"

            # Add node for the file
            system_data["nodes"][file_id] = {
                "type": file_type,
                "path": str(file_rel_path),
                "description": f"File: {file}",
            }

            # Add edge from directory to file
            system_data["edges"].append(
                {"source": node_id, "target": file_id, "type": "contains", "strength": 0.8}
            )

    # Add edges between directories (hierarchical structure)
    for node_id in system_data["nodes"]:
        if system_data["nodes"][node_id]["type"] in ["directory", "project"]:
            parent_path = Path(node_id).parent
            parent_id = str(parent_path)

            if parent_id != "." and parent_id in system_data["nodes"]:
                system_data["edges"].append(
                    {"source": parent_id, "target": node_id, "type": "parent", "strength": 0.9}
                )

    # Analyze imports in Python files to create additional connections
    for node_id, node_data in system_data["nodes"].items():
        if node_data["type"] == "python":
            file_path = project_path / node_data["path"]
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Simple analysis of imports
                lines = content.split("\n")
                for line in lines:
                    line = line.strip()
                    if line.startswith(("import ", "from ")):
                        # Simplification: just detect that there is an import
                        # A more sophisticated analysis would be needed to map correctly
                        for other_id, other_data in system_data["nodes"].items():
                            if other_data["type"] == "python" and other_id != node_id:
                                # Check if the imported file is in the path
                                imported_module = line.split()[1].split(".")[0]
                                if imported_module in other_id:
                                    system_data["edges"].append(
                                        {
                                            "source": node_id,
                                            "target": other_id,
                                            "type": "imports",
                                            "strength": 0.7,
                                        }
                                    )
                                    break
            except Exception as e:
                print(f"Warning: Could not analyze the file {file_path}: {str(e)}")

    return system_data


def main():
    """Main function."""
    # Banner
    print(
        """
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║                       ✧༺❀༻∞ ATLAS ∞༺❀༻✧                          ║
    ║                  Cartography Demonstration                        ║
    ║                                                                    ║
    ║         "Mapping project structures with awareness                 ║
    ║          to reveal latent connections and potentials."             ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """
    )

    # Command line arguments
    parser = argparse.ArgumentParser(description="ATLAS - Systemic Cartography Demonstration")
    parser.add_argument(
        "--project", "-p", required=True, help="Path to the project directory to be mapped"
    )
    parser.add_argument("--output", "-o", help="Path to save the visualization (optional)")
    parser.add_argument("--obsidian", help="Path to the Obsidian vault for export (optional)")

    args = parser.parse_args()

    # Initialize ATLAS
    print("\n[*] Initializing ATLAS subsystem...")
    atlas = ATLASCore()

    # Scan project
    print(f"\n[*] Scanning project structure: {args.project}")
    project_data = scan_project_structure(args.project)

    # Basic statistics
    num_files = sum(
        1
        for node in project_data["nodes"].values()
        if node["type"] != "directory" and node["type"] != "project"
    )
    num_dirs = sum(
        1
        for node in project_data["nodes"].values()
        if node["type"] == "directory" or node["type"] == "project"
    )

    print(f"\n[*] Scanned structure:")
    print(f"    - Directories: {num_dirs}")
    print(f"    - Files: {num_files}")
    print(f"    - Total nodes: {len(project_data['nodes'])}")
    print(f"    - Total connections: {len(project_data['edges'])}")

    # Map system
    print("\n[*] Mapping system in ATLAS...")
    project_name = Path(args.project).name
    atlas.map_system(project_data, f"Project: {project_name}")

    # Visualize
    print("\n[*] Generating visualization...")
    output_path = args.output if args.output else None
    vis_path = atlas.visualize(output_path=output_path, title=f"Project Structure: {project_name}")
    print(f"[✓] Visualization saved at: {vis_path}")

    # Analyze
    print("\n[*] Analyzing project structure...")
    analysis = atlas.analyze_system()

    print("\n[*] Basic metrics:")
    print(f"    - Nodes: {analysis['basic_metrics']['num_nodes']}")
    print(f"    - Connections: {analysis['basic_metrics']['num_edges']}")
    print(f"    - Density: {analysis['basic_metrics']['density']:.4f}")

    # Most central nodes
    if "centrality" in analysis and "degree" in analysis["centrality"]:
        central_nodes = sorted(
            analysis["centrality"]["degree"].items(), key=lambda x: x[1], reverse=True
        )[:5]
        print("\n[*] Most central files/directories:")
        for node, score in central_nodes:
            print(f"    - {node}: {score:.4f}")

    # Export to Obsidian
    if args.obsidian:
        print(f"\n[*] Exporting mapping to Obsidian: {args.obsidian}")
        note_path = atlas.export_to_obsidian(args.obsidian)
        print(f"[✓] Mapping exported to: {note_path}")

    print("\n⊹⊱∞⊰⊹ ATLAS: Transcending Through Cartography ⊹⊰∞⊱⊹")


if __name__ == "__main__":
    main()
