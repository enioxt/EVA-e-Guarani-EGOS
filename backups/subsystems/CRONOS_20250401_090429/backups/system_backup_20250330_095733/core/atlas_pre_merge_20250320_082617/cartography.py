#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ATLAS - Systemic Cartography Subsystem
Responsible for mapping connections and visualizing structures of the EVA & GUARANI system
Version: 8.0.0
Date: 19/03/2025
"""

import os
import sys
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple

# Logging configuration
logger = logging.getLogger("EVA_GUARANI.ATLAS")


class Atlas:
    """
    Main class of the ATLAS subsystem, responsible for systemic cartography.

    ATLAS maps the connections between different components of the system,
    creates visualizations of the structures, and facilitates understanding
    the relationships between modules, data, and functionalities.
    """

    def __init__(self, config: Dict[str, Any], system_root: Path):
        """
        Initializes the ATLAS subsystem

        Args:
            config: Configuration of the ATLAS subsystem
            system_root: Root path of the system
        """
        self.logger = logger
        self.logger.info("⭐ Initializing ATLAS subsystem v8.0.0 ⭐")

        self.config = config
        self.system_root = system_root
        self.enabled = config.get("enabled", True)
        self.visualization_engine = config.get("visualization_engine", "interactive")
        self.mapping_depth = config.get("mapping_depth", 3)
        self.connection_threshold = config.get("connection_threshold", 0.7)
        self.auto_refresh = config.get("auto_refresh", True)

        # System state
        self.is_running = False
        self.system_map = {}
        self.connections = []
        self.node_metadata = {}

        self.logger.info(
            f"ATLAS initialized with depth {self.mapping_depth} and threshold {self.connection_threshold}"
        )

    def start(self) -> bool:
        """
        Starts the ATLAS subsystem.

        Returns:
            bool: True if started successfully, False otherwise
        """
        if not self.enabled:
            self.logger.warning("ATLAS is disabled in the settings")
            return False

        if self.is_running:
            self.logger.warning("ATLAS is already running")
            return False

        self.logger.info("Starting ATLAS subsystem")

        # Initialize mapping
        self._initialize_mapping()

        self.is_running = True
        self.logger.info("ATLAS started successfully")
        return True

    def stop(self) -> bool:
        """
        Stops the ATLAS subsystem.

        Returns:
            bool: True if stopped successfully, False otherwise
        """
        if not self.is_running:
            self.logger.warning("ATLAS is not running")
            return False

        self.logger.info("Stopping ATLAS subsystem")

        # Save the current state if necessary
        self._save_current_state()

        self.is_running = False
        self.logger.info("ATLAS stopped successfully")
        return True

    def _initialize_mapping(self) -> None:
        """Initializes the system mapping"""
        self.logger.info("Initializing system mapping")

        # Here the initial analysis of the system structure would be done
        # For now, we just simulate with a basic structure

        self.system_map = {
            "nodes": {
                "core": {
                    "type": "category",
                    "children": ["egos", "atlas", "nexus", "cronos", "ethik"],
                },
                "modules": {"type": "category", "children": ["quantum", "analysis", "integration"]},
                "integrations": {"type": "category", "children": ["obsidian", "api", "bots"]},
                "tools": {
                    "type": "category",
                    "children": ["utilities", "visualization", "maintenance"],
                },
                "data": {"type": "category", "children": ["logs", "personas", "examples"]},
            }
        }

        # Create basic connections
        self._generate_connections()

        self.logger.info(
            f"Mapping initialized with {len(self.system_map['nodes'])} main categories"
        )

    def _generate_connections(self) -> None:
        """Generates connections between different nodes of the system"""
        self.logger.info("Generating connections between components")

        # We define some example connections
        self.connections = [
            {"source": "egos", "target": "atlas", "strength": 0.9, "type": "core"},
            {"source": "egos", "target": "nexus", "strength": 0.85, "type": "core"},
            {"source": "egos", "target": "cronos", "strength": 0.7, "type": "core"},
            {"source": "egos", "target": "ethik", "strength": 0.95, "type": "core"},
            {"source": "atlas", "target": "modules/quantum", "strength": 0.8, "type": "dependency"},
            {
                "source": "nexus",
                "target": "modules/analysis",
                "strength": 0.9,
                "type": "dependency",
            },
            {"source": "cronos", "target": "data/logs", "strength": 0.75, "type": "data_flow"},
            {
                "source": "ethik",
                "target": "modules/integration",
                "strength": 0.6,
                "type": "influence",
            },
            {
                "source": "integrations/obsidian",
                "target": "tools/visualization",
                "strength": 0.85,
                "type": "utilization",
            },
        ]

        self.logger.info(f"Generated {len(self.connections)} main connections")

    def _save_current_state(self) -> None:
        """Saves the current mapping state"""
        self.logger.info("Saving current mapping state")

        # Here the logic to save the state would be implemented
        # For now, we just log the action

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        state_path = self.system_root / "data" / "atlas" / f"map_state_{timestamp}.json"

        self.logger.info(f"Mapping state would be saved at: {state_path}")

    def generate_visualization(self, format: str = "mermaid") -> str:
        """
        Generates a visualization of the current mapping

        Args:
            format: Output format (mermaid, json, d3)

        Returns:
            str: Visualization in the requested format
        """
        self.logger.info(f"Generating visualization in {format} format")

        if format == "mermaid":
            return self._generate_mermaid()
        elif format == "json":
            return json.dumps(
                {"system_map": self.system_map, "connections": self.connections}, indent=2
            )
        else:
            self.logger.warning(f"Format {format} not supported, using mermaid as default")
            return self._generate_mermaid()

    def _generate_mermaid(self) -> str:
        """
        Generates a Mermaid format visualization

        Returns:
            str: Diagram in Mermaid format
        """
        mermaid = [
            "mermaid",
            "graph TD",
            "    %% Main nodes",
            "    EVA[EVA & GUARANI] --> CORE[Core]",
            "    EVA --> MODULES[Modules]",
            "    EVA --> INTEGRATIONS[Integrations]",
            "    EVA --> TOOLS[Tools]",
            "    EVA --> DATA[Data]",
            "",
            "    %% Core components",
            "    CORE --> EGOS[EGOS]",
            "    CORE --> ATLAS[ATLAS]",
            "    CORE --> NEXUS[NEXUS]",
            "    CORE --> CRONOS[CRONOS]",
            "    CORE --> ETHIK[ETHIK]",
            "",
            "    %% Modules",
            "    MODULES --> QUANTUM[Quantum]",
            "    MODULES --> ANALYSIS[Analysis]",
            "    MODULES --> INTEGRATION[Integration]",
            "",
            "    %% Integrations",
            "    INTEGRATIONS --> OBSIDIAN[Obsidian]",
            "    INTEGRATIONS --> API[API]",
            "    INTEGRATIONS --> BOTS[Bots]",
            "",
            "    %% Tools",
            "    TOOLS --> UTILITIES[Utilities]",
            "    TOOLS --> VISUALIZATION[Visualization]",
            "    TOOLS --> MAINTENANCE[Maintenance]",
            "",
            "    %% Data",
            "    DATA --> LOGS[Logs]",
            "    DATA --> PERSONAS[Personas]",
            "    DATA --> EXAMPLES[Examples]",
            "",
            "    %% Specific connections",
            "    EGOS -.-> ATLAS",
            "    EGOS -.-> NEXUS",
            "    EGOS -.-> CRONOS",
            "    EGOS -.-> ETHIK",
            "    ATLAS -.-> QUANTUM",
            "    NEXUS -.-> ANALYSIS",
            "    CRONOS -.-> LOGS",
            "    ETHIK -.-> INTEGRATION",
            "    OBSIDIAN -.-> VISUALIZATION",
            "",
        ]

        return "\n".join(mermaid)

    def analyze_component(self, component_path: str) -> Dict[str, Any]:
        """
        Analyzes a specific component and its connections

        Args:
            component_path: Path of the component to be analyzed

        Returns:
            Dict: Analysis of the component
        """
        self.logger.info(f"Analyzing component: {component_path}")

        # Here the detailed analysis of the component would be implemented
        # For now, we return simulated data

        analysis = {
            "component": component_path,
            "connections": [
                conn
                for conn in self.connections
                if conn["source"] == component_path or conn["target"] == component_path
            ],
            "strength": {
                "incoming": sum(
                    [c["strength"] for c in self.connections if c["target"] == component_path]
                ),
                "outgoing": sum(
                    [c["strength"] for c in self.connections if c["source"] == component_path]
                ),
            },
            "complexity": 0.75,
            "centrality": 0.65,
            "visualization": self._generate_component_visualization(component_path),
        }

        self.logger.info(f"Analysis of component {component_path} completed")
        return analysis

    def _generate_component_visualization(self, component_path: str) -> str:
        """
        Generates a specific visualization for a component

        Args:
            component_path: Path of the component

        Returns:
            str: Visualization of the component
        """
        # Simplification for the example
        mermaid = [
            "mermaid",
            "graph TD",
            f"    COMP[{component_path}]",
        ]

        # Add incoming connections
        for conn in [c for c in self.connections if c["target"] == component_path]:
            mermaid.append(
                f"    {conn['source'].replace('/', '_')}[{conn['source']}] -->|{conn['type']}| COMP"
            )

        # Add outgoing connections
        for conn in [c for c in self.connections if c["source"] == component_path]:
            mermaid.append(
                f"    COMP -->|{conn['type']}| {conn['target'].replace('/', '_')}[{conn['target']}]"
            )

        mermaid.append("")
        return "\n".join(mermaid)

    def export_map(self, format: str = "json", path: Optional[Path] = None) -> Path:
        """
        Exports the system map to a file

        Args:
            format: Export format
            path: Path to save the file (optional)

        Returns:
            Path: Path of the exported file
        """
        self.logger.info(f"Exporting system map in {format} format")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        if path is None:
            export_dir = self.system_root / "data" / "atlas" / "exports"
            export_dir.mkdir(parents=True, exist_ok=True)
            path = export_dir / f"system_map_{timestamp}.{format}"

        # Content of the export depends on the format
        content = ""
        if format == "json":
            content = json.dumps(
                {
                    "metadata": {"timestamp": timestamp, "version": "8.0.0", "generator": "ATLAS"},
                    "system_map": self.system_map,
                    "connections": self.connections,
                },
                indent=2,
            )
        elif format == "markdown":
            content = (
                f"# EVA & GUARANI System Map\n\n"
                f"Generated on: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
                f"## Visualization\n\n{self._generate_mermaid()}\n\n"
                f"## Connections\n\n"
                + "\n".join(
                    [
                        f"- {c['source']} → {c['target']} ({c['type']}, strength: {c['strength']})"
                        for c in sorted(self.connections, key=lambda x: x["source"])
                    ]
                )
            )
        else:
            self.logger.warning(f"Format {format} not fully supported, exporting as text")
            content = (
                f"EVA & GUARANI System - Map\n{self.system_map}\n\nConnections:\n{self.connections}"
            )

        # Write file
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        self.logger.info(f"Map exported to {path}")
        return path

    def refresh_map(self) -> None:
        """Updates the system map with the latest information"""
        self.logger.info("Updating system map")

        # Here the update logic would be implemented
        # For now, we just simulate

        self.logger.info("System map updated")


def create_atlas(config: Dict[str, Any], system_root: Path) -> Atlas:
    """
    Factory function to create an instance of ATLAS

    Args:
        config: Configuration of ATLAS
        system_root: Root path of the system

    Returns:
        Atlas: Instance of the ATLAS subsystem
    """
    return Atlas(config, system_root)


if __name__ == "__main__":
    """Test execution of the ATLAS subsystem"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Test configuration
    test_config = {
        "enabled": True,
        "visualization_engine": "interactive",
        "mapping_depth": 3,
        "connection_threshold": 0.7,
        "auto_refresh": True,
    }

    # Create ATLAS instance
    system_root = Path(__file__).parent.parent.parent
    atlas = create_atlas(test_config, system_root)

    # Start ATLAS
    atlas.start()

    # Generate and display visualization
    print(atlas.generate_visualization(format="mermaid"))

    # Analyze a component
    analysis = atlas.analyze_component("core/egos")
    print(f"\nAnalysis of component core/egos:")
    print(f"- Connections: {len(analysis['connections'])}")
    print(f"- Total strength: {analysis['strength']}")

    # Export map
    atlas.export_map(format="markdown")

    # Stop ATLAS
    atlas.stop()
