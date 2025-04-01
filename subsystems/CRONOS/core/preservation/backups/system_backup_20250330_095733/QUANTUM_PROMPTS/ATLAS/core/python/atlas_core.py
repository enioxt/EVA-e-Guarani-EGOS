#!/usr/bin/env python3
python
#!/usr/bin/env python3
"""
EGOS - ATLAS Subsystem
======================

ATLAS (Advanced Topological Linking and Systemic Mapping) is the subsystem 
responsible for systemic mapping in EGOS. It maps connections between 
components, visualizes complex systems, and identifies latent relationships.

Version: 1.0.0
"""

import os
import sys
import json
import logging
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple

# Directory configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
ATLAS_DATA_DIR = os.path.join(DATA_DIR, "atlas")

# Ensure directories exist
os.makedirs(ATLAS_DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(LOGS_DIR, "modules", "atlas"), exist_ok=True)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, "modules", "atlas", "atlas.log")),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("EGOS.ATLAS")

class ATLASCore:
    """Core of the ATLAS subsystem for systemic mapping."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initializes the ATLAS core.
        
        Args:
            config_path: Path to the custom configuration file.
        """
        self.version = "1.0.0"
        self.startup_time = datetime.now().isoformat()
        
        # Load configuration
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            default_config_path = os.path.join(CONFIG_DIR, "modules", "atlas_config.json")
            if os.path.exists(default_config_path):
                with open(default_config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self._create_default_config()
                
        # Initialize graph for mapping
        self.graph = nx.DiGraph()
        
        # Log initialization
        self._log_operation("INITIALIZATION", "Completed", 
                           f"ATLAS Core v{self.version} initialized",
                           "System ready for mapping")
        
        logger.info(f"ATLAS Core initialized - Version {self.version}")

    def _create_default_config(self) -> Dict[str, Any]:
        """Creates a default configuration for ATLAS."""
        config = {
            "version": self.version,
            "visualization": {
                "node_size": 800,
                "edge_width": 1.5,
                "font_size": 10,
                "arrow_size": 15,
                "layout": "spring",
                "colormap": "viridis"
            },
            "analysis": {
                "detect_communities": True,
                "identify_central_nodes": True,
                "find_shortest_paths": True
            },
            "export": {
                "formats": ["png", "svg", "graphml", "json"],
                "obsidian_integration": True,
                "obsidian_template": "atlas_map.md"
            }
        }
        
        # Save default configuration
        os.makedirs(os.path.join(CONFIG_DIR, "modules"), exist_ok=True)
        with open(os.path.join(CONFIG_DIR, "modules", "atlas_config.json"), 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        return config
    
    def _log_operation(self, operation: str, status: str, details: str, 
                      recommendations: Optional[str] = None, 
                      ethical_reflection: Optional[str] = None) -> None:
        """
        Logs an operation in the universal log.
        
        Args:
            operation: Name of the operation
            status: Status of the operation (Started/In Progress/Completed/Failed)
            details: Details of the operation
            recommendations: Recommendations for next steps
            ethical_reflection: Relevant ethical reflection
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}][ATLAS][{operation}]\n"
        log_entry += f"STATUS: {status}\n"
        log_entry += f"CONTEXT: Systemic Mapping\n"
        log_entry += f"DETAILS: {details}\n"
        
        if recommendations:
            log_entry += f"RECOMMENDATIONS: {recommendations}\n"
        
        if ethical_reflection:
            log_entry += f"ETHICAL REFLECTION: {ethical_reflection}\n"
        
        # Log to universal log file
        universal_log_path = os.path.join(LOGS_DIR, "universal_log.txt")
        with open(universal_log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
        
        # Log to logger
        logger.info(f"{operation} - {status}: {details}")
    
    def map_system(self, system_data: Dict[str, Any], name: str) -> bool:
        """
        Maps a system from structured data.
        
        Args:
            system_data: Data of the system to be mapped
            name: Name of the mapping
            
        Returns:
            bool: True if the mapping was successful
        """
        self._log_operation("MAP_SYSTEM", "Started", 
                           f"Starting system mapping: {name}",
                           "Preparing graph structure")
        
        try:
            # Clear existing graph
            self.graph.clear()
            
            # Add nodes
            if "nodes" in system_data:
                for node_id, node_data in system_data["nodes"].items():
                    self.graph.add_node(node_id, **node_data)
            
            # Add edges
            if "edges" in system_data:
                for edge in system_data["edges"]:
                    source = edge["source"]
                    target = edge["target"]
                    # Remove source and target from dictionary to use the rest as attributes
                    edge_attrs = {k: v for k, v in edge.items() if k not in ["source", "target"]}
                    self.graph.add_edge(source, target, **edge_attrs)
            
            # Save the mapping
            self._save_mapping(name)
            
            self._log_operation("MAP_SYSTEM", "Completed", 
                               f"Mapping completed: {name}",
                               f"Graph created with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} connections",
                               "System mapping is an ethical responsibility that requires precision and respect for complexity")
            
            return True
        
        except Exception as e:
            self._log_operation("MAP_SYSTEM", "Failed", 
                               f"Error mapping system: {str(e)}",
                               "Check the structure of the input data")
            logger.error(f"Error mapping system: {str(e)}")
            return False
    
    def visualize(self, output_path: Optional[str] = None, 
                 title: Optional[str] = None,
                 layout: Optional[str] = None) -> str:
        """
        Visualizes the current graph and saves the image.
        
        Args:
            output_path: Path to save the visualization
            title: Title of the visualization
            layout: Layout algorithm to be used
            
        Returns:
            str: Path of the generated visualization file
        """
        self._log_operation("VISUALIZE", "Started", 
                           "Generating visualization of the mapped system")
        
        if self.graph.number_of_nodes() == 0:
            self._log_operation("VISUALIZE", "Failed", 
                               "No mapped system to visualize",
                               "Run map_system before visualizing")
            return ""
        
        try:
            # Visualization settings
            vis_config = self.config["visualization"]
            node_size = vis_config["node_size"]
            edge_width = vis_config["edge_width"]
            font_size = vis_config["font_size"]
            layout_algo = layout or vis_config["layout"]
            
            # Create figure
            plt.figure(figsize=(12, 10))
            
            # Set layout
            if layout_algo == "spring":
                pos = nx.spring_layout(self.graph)
            elif layout_algo == "circular":
                pos = nx.circular_layout(self.graph)
            elif layout_algo == "kamada_kawai":
                pos = nx.kamada_kawai_layout(self.graph)
            elif layout_algo == "spectral":
                pos = nx.spectral_layout(self.graph)
            else:
                pos = nx.spring_layout(self.graph)
            
            # Draw nodes
            nx.draw_networkx_nodes(self.graph, pos, 
                                  node_size=node_size,
                                  node_color="skyblue",
                                  alpha=0.8)
            
            # Draw edges
            nx.draw_networkx_edges(self.graph, pos, 
                                  width=edge_width,
                                  alpha=0.5,
                                  arrows=True,
                                  arrowsize=vis_config["arrow_size"])
            
            # Draw labels
            nx.draw_networkx_labels(self.graph, pos, 
                                   font_size=font_size,
                                   font_family="sans-serif")
            
            # Add title
            if title:
                plt.title(title, fontsize=16)
            else:
                plt.title("ATLAS - Systemic Mapping", fontsize=16)
            
            # Remove axes
            plt.axis("off")
            
            # Set output path
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(ATLAS_DATA_DIR, f"atlas_map_{timestamp}.png")
            
            # Save figure
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close()
            
            self._log_operation("VISUALIZE", "Completed", 
                               f"Visualization saved at: {output_path}",
                               "The visualization can be integrated with Obsidian for additional analysis",
                               "Ethical visualization of complex systems should balance clarity and precision")
            
            return output_path
        
        except Exception as e:
            self._log_operation("VISUALIZE", "Failed", 
                               f"Error generating visualization: {str(e)}")
            logger.error(f"Error generating visualization: {str(e)}")
            return ""
    
    def export_to_obsidian(self, vault_path: str, 
                          template_name: Optional[str] = None) -> str:
        """
        Exports the current mapping to Obsidian.
        
        Args:
            vault_path: Path to the Obsidian vault
            template_name: Name of the template to be used
            
        Returns:
            str: Path of the generated markdown file
        """
        self._log_operation("EXPORT_OBSIDIAN", "Started", 
                           "Exporting mapping to Obsidian")
        
        if self.graph.number_of_nodes() == 0:
            self._log_operation("EXPORT_OBSIDIAN", "Failed", 
                               "No mapped system to export",
                               "Run map_system before exporting")
            return ""
        
        try:
            # Check if the vault exists
            if not os.path.exists(vault_path):
                os.makedirs(vault_path, exist_ok=True)
            
            # Generate visualization to include in markdown
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"atlas_map_{timestamp}.png"
            image_path = os.path.join(vault_path, "attachments", image_filename)
            os.makedirs(os.path.join(vault_path, "attachments"), exist_ok=True)
            
            # Create visualization
            self.visualize(output_path=image_path)
            
            # Create markdown content
            template = template_name or self.config["export"]["obsidian_template"]
            markdown_content = self._generate_markdown(image_filename)
            
            # Set output path
            note_filename = f"ATLAS - Systemic Mapping {timestamp}.md"
            note_path = os.path.join(vault_path, note_filename)
            
            # Save markdown file
            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            self._log_operation("EXPORT_OBSIDIAN", "Completed", 
                               f"Mapping exported to: {note_path}",
                               "The mapping can be explored in Obsidian",
                               "Integration with connected thinking tools enhances our capacity for ethical understanding")
            
            return note_path
        
        except Exception as e:
            self._log_operation("EXPORT_OBSIDIAN", "Failed", 
                               f"Error exporting to Obsidian: {str(e)}")
            logger.error(f"Error exporting to Obsidian: {str(e)}")
            return ""
    
    def _generate_markdown(self, image_filename: str) -> str:
        """
        Generates markdown content for export.
        
        Args:
            image_filename: Name of the image file
            
        Returns:
            str: Markdown content
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Graph statistics
        num_nodes = self.graph.number_of_nodes()
        num_edges = self.graph.number_of_edges()
        
        # Identify central nodes
        if num_nodes > 0:
            centrality = nx.degree_centrality(self.graph)
            central_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
            central_nodes_str = "\n".join([f"- **{node}**: {round(score * 100, 2)}%" for node, score in central_nodes])
        else:
            central_nodes_str = "No nodes found"
        
        # Generate markdown
        markdown = f"""# ATLAS - Systemic Mapping

> "In the cartography of complex systems, we reveal not only visible connections but also latent potentials that transcend the apparent structure."

## Overview

This mapping was generated by the ATLAS subsystem of EGOS (Eva & Guarani OS) on {timestamp}.

## Visualization

![[attachments/{image_filename}]]

## Statistics

- **Nodes**: {num_nodes}
- **Connections**: {num_edges}
- **Density**: {nx.density(self.graph) if num_nodes > 1 else 0}

## Central Nodes

{central_nodes_str}

## Analysis

The mapping reveals the interconnected structure of the system, highlighting the central components and their relationships. The visualization above allows identifying emerging patterns and potential areas for optimization or expansion.

## Next Steps

1. Explore the central nodes to understand their role in the system
2. Identify possible bottlenecks or points of fragility
3. Consider potential connections that could enrich the system
4. Analyze the system's evolution over time

---

✧༺❀༻∞ Generated by ATLAS - EGOS ∞༺❀༻✧
"""
        return markdown
    
    def _save_mapping(self, name: str) -> None:
        """
        Saves the current mapping in JSON format.
        
        Args:
            name: Name of the mapping
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name.lower().replace(' ', '_')}_{timestamp}.json"
        filepath = os.path.join(ATLAS_DATA_DIR, filename)
        
        # Convert graph to dictionary
        data = {
            "metadata": {
                "name": name,
                "timestamp": timestamp,
                "version": self.version
            },
            "nodes": {},
            "edges": []
        }
        
        # Add nodes
        for node, attrs in self.graph.nodes(data=True):
            data["nodes"][node] = attrs
        
        # Add edges
        for source, target, attrs in self.graph.edges(data=True):
            edge_data = {"source": source, "target": target}
            edge_data.update(attrs)
            data["edges"].append(edge_data)
        
        # Save file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Mapping saved at: {filepath}")

    def analyze_system(self) -> Dict[str, Any]:
        """
        Analyzes the mapped system and returns metrics.
        
        Returns:
            Dict[str, Any]: System metrics and analysis
        """
        self._log_operation("ANALYZE", "Started", 
                           "Analyzing mapped system")
        
        if self.graph.number_of_nodes() == 0:
            self._log_operation("ANALYZE", "Failed", 
                               "No mapped system to analyze",
                               "Run map_system before analyzing")
            return {"error": "No mapped system"}
        
        try:
            logger.info(f"Analyzing system with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
            
            # Calculate average degree
            total_degree = sum(d for _, d in self.graph.degree())
            avg_degree = total_degree / self.graph.number_of_nodes() if self.graph.number_of_nodes() > 0 else 0
            
            # Basic analysis
            analysis = {
                "basic_metrics": {
                    "num_nodes": self.graph.number_of_nodes(),
                    "num_edges": self.graph.number_of_edges(),
                    "density": nx.density(self.graph) if self.graph.number_of_nodes() > 1 else 0,
                    "is_connected": nx.is_connected(self.graph) if self.graph.number_of_nodes() > 0 else False,
                    "avg_degree": avg_degree
                },
                "centrality": {
                    "degree": {},
                    "betweenness": {},
                    "closeness": {}
                },
                "communities": {
                    "num_communities": 0,
                    "partition": {}
                },
                "node_types": {}
            }
            
            # Centrality analysis
            if self.graph.number_of_nodes() > 1:
                # Degree
                degree_centrality = nx.degree_centrality(self.graph)
                analysis["centrality"]["degree"] = degree_centrality
                
                # Betweenness
                betweenness_centrality = nx.betweenness_centrality(self.graph)
                analysis["centrality"]["betweenness"] = betweenness_centrality
                
                # Closeness (only for connected graphs)
                if analysis["basic_metrics"]["is_connected"]:
                    closeness_centrality = nx.closeness_centrality(self.graph)
                    analysis["centrality"]["closeness"] = closeness_centrality
            
            # Community detection
            if self.config["analysis"]["detect_communities"] and analysis["basic_metrics"]["num_nodes"] > 2:
                try:
                    # Import community-detection module 
                    # (can be installed via: pip install python-louvain)
                    community_detection_available = False
                    
                    try:
                        #