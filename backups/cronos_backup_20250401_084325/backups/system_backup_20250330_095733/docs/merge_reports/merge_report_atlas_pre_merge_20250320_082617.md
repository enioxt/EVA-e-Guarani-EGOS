---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: docs
  changelog: []
  dependencies:
  - ATLAS
  - QUANTUM_PROMPTS
  - BIOS-Q
  description: Component of the EVA & GUARANI Quantum Unified System
  documentation_quality: 0.95
  encoding: utf-8
  ethical_validation: true
  last_updated: '2025-03-29'
  related_files: []
  required: true
  review_status: approved
  security_level: 0.95
  simulation_capable: false
  status: active
  subsystem: ATLAS
  test_coverage: 0.9
  translation_status: completed
  type: documentation
  version: '8.0'
  windows_compatibility: true
---
```yaml
METADATA:
  type: documentation
  category: module
  subsystem: MASTER
  status: active
  required: false
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
  principles: []
  security_level: standard
  test_coverage: 0.0
  documentation_quality: 0.0
  ethical_validation: true
  windows_compatibility: true
  encoding: utf-8
  backup_required: false
  translation_status: pending
  api_endpoints: []
  related_files: []
  changelog: ''
  review_status: pending
```

```yaml
METADATA:
  type: documentation
  category: module
  subsystem: MASTER
  status: active
  required: false
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
```

markdown
# Backup Analysis Report - atlas_pre_merge_20250320_082617

Date: 2025-03-20 08:30:39

## Unique Files in Backup

- `atlas_analyzer.js`

- `cartography.py`

- `README.md`

- `ROADMAP_EXECUTIVE.md`

## Unique Files in Current Version

- `__init__.py`

- `__pycache__\__init__.cpython-313.pyc`

- `atlas_core.py`

## Difference Analysis

### Differences in `atlas_demo.py`

diff
--- C:\Eva & Guarani - EGOS\core\atlas_pre_merge_20250320_082617\atlas_demo.py

+++ C:\Eva & Guarani - EGOS\core\atlas\atlas_demo.py

@@ -1,11 +1,16 @@

 #!/usr/bin/env python3

+# -*- coding: utf-8 -*-

 """

-EGOS - ATLAS Demo

-================

+✧༺❀༻∞ ATLAS - Systemic Cartography Demo ∞༺❀༻✧

+====================================================

 

-This script demonstrates how to use the ATLAS subsystem to map

-the structure of a project and visualize it.

+This script demonstrates the capabilities of the EGOS ATLAS subsystem,

+allowing you to map and visualize the structure of a project.

 

+Usage:

+    python atlas_demo.py --project /path/to/project [--output format] [--export directory]

+

+Author: EGOS Community

 Version: 1.0.0

 """

 

@@ -13,216 +18,132 @@

 import sys

 import json

 import argparse

+import logging

 from pathlib import Path

 

-# Add root directory to path to import EGOS modules

-sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

+# Add root directory to path to import modules

+sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

 

-try:

-    from core.atlas.atlas_core import ATLASCore

-except ImportError:

-    print("Error: Could not import the ATLAS module.")

-    print("Ensure that EGOS is installed correctly.")

-    sys.exit(1)

+# Logging configuration

+logging.basicConfig(

+    level=logging.INFO,

+    format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s",

+    handlers=[

+        logging.StreamHandler(sys.stdout)

+    ]

+)

 

-def scan_project_structure(project_path):

+logger = logging.getLogger("ATLAS.Demo")

+

+# Terminal colors

+class Colors:

+    HEADER = '\033[95m'

+    BLUE = '\033[94m'

+    CYAN = '\033[96m'

+    GREEN = '\033[92m'

+    YELLOW = '\033[93m'

+    RED = '\033[91m'

+    ENDC = '\033[0m'

+    BOLD = '\033[1m'

+    UNDERLINE = '\033[4m'

+

+def print_colored(message, color=Colors.CYAN, bold=False):

+    """Prints a colored message in the terminal."""

+    prefix = Colors.BOLD if bold else ""

+    print(f"{prefix}{color}{message}{Colors.ENDC}")

+

+def print_banner():

+    """Displays the ATLAS banner."""

+    banner = f"""

+╔════════════════════════════════════════════════════════════════════╗

+║                                                                    ║

+║                       ✧༺❀༻∞ ATLAS ∞༺❀༻✧                          ║

+║                      Systemic Cartography                          ║

+║                                                                    ║

+╚════════════════════════════════════════════════════════════════════╝

     """

-    Scans the structure of a project and creates a mapping for ATLAS.

-    

-    Args:

-        project_path: Path to the project directory

-        

-    Returns:

-        dict: Project structure in a format compatible with ATLAS

-    """

-    project_path = Path(project_path).resolve()

-    

-    if not project_path.exists() or not project_path.is_dir():

-        print(f"Error: The path {project_path} does not exist or is not a directory.")

-        sys.exit(1)

-    

-    # Structure for ATLAS

-    system_data = {

-        "nodes": {},

-        "edges": []

-    }

-    

-    # Map directories and files

-    for root, dirs, files in os.walk(project_path):

-        root_path = Path(root)

-        rel_path = root_path.relative_to(project_path)

-        node_id = str(rel_path)

-        

-        if node_id == ".":

-            node_id = project_path.name

-            node_type = "project"

-        else:

-            node_type = "directory"

-        

-        # Add node for directory

-        system_data["nodes"][node_id] = {

-            "type": node_type,

-            "path": str(rel_path),

-            "description": f"Directory: {node_id}"

-        }

-        

-        # Add nodes for files

-        for file in files:

-            file_path = root_path / file

-            file_rel_path = file_path.relative_to(project_path)

-            file_id = str(file_rel_path)

-            

-            # Determine file type

-            file_type = "file"

-            if file.endswith((".py", ".pyw")):

-                file_type = "python"

-            elif file.endswith((".js", ".jsx", ".ts", ".tsx")):

-                file_type = "javascript"

-            elif file.endswith((".html", ".htm")):

-                file_type = "html"

-            elif file.endswith((".css", ".scss", ".sass")):

-                file_type = "css"

-            elif file.endswith((".md", ".markdown")):

-                file_type = "markdown"

-            elif file.endswith((".json", ".yaml", ".yml", ".toml")):

-                file_type = "config"

-            

-            # Add node for file

-            system_data["nodes"][file_id] = {

-                "type": file_type,

-                "path": str(file_rel_path),

-                "description": f"File: {file}"

-            }

-            

-            # Add edge from directory to file

-            system_data["edges"].append({

-                "source": node_id,

-                "target": file_id,

-                "type": "contains",

-                "strength": 0.8

-            })

-    

-    # Add edges between directories (hierarchical structure)

-    for node_id in system_data["nodes"]:

-        if system_data["nodes"][node_id]["type"] in ["directory", "project"]:

-            parent_path = Path(node_id).parent

-            parent_id = str(parent_path)

-            

-            if parent_id != "." and parent_id in system_data["nodes"]:

-                system_data["edges"].append({

-                    "source": parent_id,

-                    "target": node_id,

-                    "type": "parent",

-                    "strength": 0.9

-                })

-    

-    # Analyze imports in Python files to create additional connections

-    for node_id, node_data in system_data["nodes"].items():

-        if node_data["type"] == "python":

-            file_path = project_path / node_data["path"]

-            try:

-                with open(file_path, 'r', encoding='utf-8') as f:

-                    content = f.read()

-                

-                # Simple import analysis

-                lines = content.split('\n')

-                for line in lines:

-                    line = line.strip()

-                    if line.startswith(("import ", "from ")):

-                        # Simplification: only detect that there is an import

-                        # A more sophisticated analysis would be needed to map correctly

-                        for other_id, other_data in system_data["nodes"].items():

-                            if other_data["type"] == "python" and other_id != node_id:

-                                # Check if the imported file is in the path

-                                imported_module = line.split()[1].split('.')[0]

-                                if imported_module in other_id:

-                                    system_data["edges"].append({

-                                        "source": node_id,

-                                        "target": other_id,

-                                        "type": "imports",

-                                        "strength": 0.7

-                                    })

-                                    break

-            except Exception as e:

-                print(f"Warning: Could not analyze the file {file_path}: {str(e)}")

-    

-    return system_data

+    print_colored(banner, Colors.CYAN, bold=True)

+    print_colored("Demonstration of the EGOS cartography subsystem\n", Colors.BLUE)

+

+def parse_arguments():

+    """Parses command line arguments."""

+    parser = argparse.ArgumentParser(description="ATLAS - Systemic Cartography")

+    parser.add_argument("--project", type=str, required=True, help="Path to the project to be mapped")

+    parser.add_argument("--output", type=str, default="json", choices=["json", "md", "html"], help="Output format")

+    parser.add_argument("--export", type=str, help="Directory to export visualization for Obsidian")

+    parser.add_argument("--config", type=str, help="Path to custom configuration file")

+    return parser.parse_args()

 

 def main():

     """Main function."""

-    # Banner

-    print("""

-    ╔════════════════════════════════════════════════════════════════════╗

-    ║                                                                    ║

-    ║                       ✧༺❀༻∞ ATLAS ∞༺❀༻✧                          ║

-    ║                  Demonstration of Cartography                       ║

-    ║                                                                    ║

-    ║         "Mapping the structure of projects with awareness          ║

-    ║          to reveal latent connections and potentials."             ║

-    ║                                                                    ║

-    ╚════════════════════════════════════════════════════════════════════╝

-    """)

+    # Display banner

+    print_banner()

     

-    # Command line arguments

-    parser = argparse.ArgumentParser(description="ATLAS - Systemic Cartography Demonstration")

-    parser.add_argument("--project", "-p", required=True, help="Path to the project directory to be mapped")

-    parser.add_argument("--output", "-o", help="Path to save the visualization (optional)")

-    parser.add_argument("--obsidian", help="Path to the Obsidian vault for export (optional)")

+    # Parse arguments

+    args = parse_arguments()

     

-    args = parser.parse_args()

+    # Check if the project exists

+    if not os.path.exists(args.project):

+        print_colored(f"Error: The project path '{args.project}' does not exist", Colors.RED)

+        return 1

     

-    # Initialize ATLAS

-    print("\n[*] Initializing ATLAS subsystem...")

-    atlas = ATLASCore()

+    print_colored(f"Mapping project: {args.project}", Colors.BLUE)

+    print_colored(f"Output format: {args.output}", Colors.BLUE)

     

-    # Scan project

-    print(f"\n[*] Scanning project structure: {args.project}")

-    project_data = scan_project_structure(args.project)

-    

-    # Basic statistics

-    num_files = sum(1 for node in project_data["nodes"].values() if node["type"] != "directory" and node["type"] != "project")

-    num_dirs = sum(1 for node in project_data["nodes"].values() if node["type"] == "directory" or node["type"] == "project")

-    

-    print(f"\n[*] Scanned structure:")

-    print(f"    - Directories: {num_dirs}")

-    print(f"    - Files: {num_files}")

-    print(f"    - Total nodes: {len(project_data['nodes'])}")

-    print(f"    - Total connections: {len(project_data['edges'])}")

-    

-    # Map system

-    print("\n[*] Mapping system in ATLAS...")

-    project_name = Path(args.project).name

-    atlas.map_system(project_data, f"Project: {project_name}")

-    

-    # Visualize

-    print("\n[*] Generating visualization...")

-    output_path = args.output if args.output else None

-    vis_path = atlas.visualize(output_path=output_path, title=f"Project Structure: {project_name}")

-    print(f"[✓] Visualization saved at: {vis_path}")

-    

-    # Analyze

-    print("\n[*] Analyzing project structure...")

-    analysis = atlas.analyze_system()

-    

-    print("\n[*] Basic metrics:")

-    print(f"    - Nodes: {analysis['basic_metrics']['num_nodes']}")

-    print(f"    - Connections: {analysis['basic_metrics']['num_edges']}")

-    print(f"    - Density: {analysis['basic_metrics']['density']:.4f}")

-    

-    # Most central nodes

-    if "centrality" in analysis and "degree" in analysis["centrality"]:

-        central_nodes = sorted(analysis["centrality"]["degree"].items(), key=lambda x: x[1], reverse=True)[:5]

-        print("\n[*] Most central files/directories:")

-        for node, score in central_nodes:

-            print(f"    - {node}: {score:.4f}")

-    

-    # Export to Obsidian

-    if args.obsidian:

-        print(f"\n[*] Exporting mapping to Obsidian: {args.obsidian}")

-        note_path = atlas.export_to_obsidian(args.obsidian)

-        print(f"[✓] Mapping exported to: {note_path}")

-    

-    print("\n⊹⊱∞⊰⊹ ATLAS: Transcending Through Cartography ⊹⊰∞⊱⊹")

+    try:

+        # Import the ATLAS module

+        from core.atlas import AtlasModule

+        

+        # Configuration

+        config_path = args.config

+        if not config_path:

+            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 

+                                      "config", "modules", "atlas_config.json")

+        

+        # Initialize ATLAS

+        print_colored("Initializing ATLAS...", Colors.BLUE)

+        atlas = AtlasModule(config_path)

+        

+        # Map the project

+        print_colored("Mapping project structure...", Colors.BLUE)

+        mapping = atlas.map_project(args.project, args.output)

+        

+        # Display statistics

+        print_colored("\nMapping statistics:", Colors.GREEN, bold=True)

+        print(f"  Project: {mapping['project']}")

+        print(f"  Path: {mapping['path']}")

+        print(f"  Timestamp: {mapping['timestamp']}")

+        print(f"  Nodes: {len(mapping['nodes'])}")

+        print(f"  Connections: {len(mapping['edges'])}")

+        print(f"  Metrics:")

+        print(f"    - Files: {mapping['metrics']['files']}")

+        print(f"    - Directories: {mapping['metrics']['directories']}")

+        print(f"    - Connections: {mapping['metrics']['connections']}")

+        print(f"    - Complexity: {mapping['metrics']['complexity']}")

+        

+        # Generate visualization

+        print_colored("\nGenerating visualization...", Colors.BLUE)

+        visualization_path = atlas.visualize_mapping(mapping)

+        print_colored(f"Visualization generated at: {visualization_path}", Colors.GREEN)

+        

+        # Export to Obsidian if requested

+        if args.export:

+            print_colored(f"\nExporting to Obsidian at: {args.export}", Colors.BLUE)

+            files = atlas.export_to_obsidian(mapping, args.export)

+            print_colored(f"Export completed: {len(files)} files generated", Colors.GREEN)

+            for file in files:

+                print(f"  - {file}")

+        

+        print_colored("\n⊹⊱∞⊰⊹ ATLAS: Mapping with Love ⊹⊰∞⊱⊹\n", Colors.CYAN, bold=True)

+        return 0

+        

+    except ImportError as e:

+        print_colored(f"Error importing ATLAS: {str(e)}", Colors.RED)

+        return 1

+    except Exception as e:

+        print_colored(f"Error during execution: {str(e)}", Colors.RED)

+        logger.error(f"Error: {str(e)}")

+        return 1

 

 if __name__ == "__main__":

-    main()

+    sys.exit(main())



## Recommendations

### Potentially Lost Files

The following files exist only in the backup and may need to be restored:

- [ ] Review and possibly restore: `atlas_analyzer.js`

- [ ] Review and possibly restore: `cartography.py`

- [ ] Review and possibly restore: `README.md`

- [ ] Review and possibly restore: `ROADMAP_EXECUTIVE.md`

### New Files

The following files are new and should be verified:

- [ ] Verify new file: `__init__.py`

- [ ] Verify new file: `__pycache__\__init__.cpython-313.pyc`

- [ ] Verify new file: `atlas_core.py`