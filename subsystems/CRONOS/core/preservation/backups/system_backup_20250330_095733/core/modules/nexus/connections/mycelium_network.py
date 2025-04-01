#!/usr/bin/env python3
"""
# ========================================================================
# MYCELIUM NETWORK - Connection Analysis for EVA & GUARANI
# ========================================================================
#
# VISION: 1.0.0 "Quantum Integration" - Mycelial Connection Network
#
# This module provides the MyceliumNetwork class that complements the
# functionality of quantum_mycelium.py by:
# 
# 1. Providing a network-based approach to analyzing code connections
# 2. Identifying valuable integration points between components
# 3. Offering visualization of system connections
# 4. Suggesting potential optimizations for network structure
#
# The MyceliumNetwork acts as a bridge between NEXUS (modular analysis) 
# and ATLAS (systemic cartography) components.
# ========================================================================
"""

import os
import sys
import json
import re
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict

# Ensure we can import from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from core.quantum_mycelium import QuantumMycelium

# ========================================================================
# CONFIGURATION
# ========================================================================

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
VISUALIZATIONS_DIR = os.path.join(PROJECT_ROOT, "staging", "visualizations")
NETWORK_FILE = os.path.join(VISUALIZATIONS_DIR, "mycelium_network.json")
NETWORK_IMAGE = os.path.join(VISUALIZATIONS_DIR, "mycelium_network.png")

# ========================================================================
# MAIN CLASS: MYCELIUM NETWORK
# ========================================================================

class MyceliumNetwork:
    """
    Provides network analysis and visualization for project connections.
    
    This class builds on the QuantumMycelium analysis, converting the connection
    data into a proper network graph that can be analyzed using graph theory
    algorithms and visualized for better understanding.
    """
    
    def __init__(self, quantum_mycelium=None):
        """Initialize the MyceliumNetwork with optional QuantumMycelium instance"""
        self.project_root = PROJECT_ROOT
        
        # Create visualization directory
        os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)
        
        # Initialize network graph
        self.graph = nx.DiGraph()
        
        # If quantum_mycelium was provided, use it
        self.quantum_mycelium = quantum_mycelium
        
        # Store analysis results
        self.centrality = {}
        self.communities = {}
        self.recommendations = []
    
    def load_from_quantum_mycelium(self):
        """Load data from a QuantumMycelium analysis"""
        if not self.quantum_mycelium:
            self.quantum_mycelium = QuantumMycelium()
            self.quantum_mycelium.scan_project()
            self.quantum_mycelium.analyze_connections()
        
        # Create nodes for all files
        for file_path in self.quantum_mycelium.files:
            self.graph.add_node(file_path, 
                                type=os.path.splitext(file_path)[1],
                                size=self.quantum_mycelium.file_metadata.get(file_path, {}).get('size', 0),
                                lines=self.quantum_mycelium.file_metadata.get(file_path, {}).get('lines', 0))
        
        # Add edges for file references
        for source, references in self.quantum_mycelium.file_references.items():
            for ref_data in references:
                # ref_data is a tuple of (reference, pattern)
                reference, pattern = ref_data
                
                # Try to match reference to actual files
                potential_matches = [f for f in self.quantum_mycelium.files if reference in f]
                for target in potential_matches:
                    self.graph.add_edge(source, target, type=pattern)
        
        print(f"✅ Created network with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
    
    def analyze_network(self):
        """Run network analysis algorithms on the graph"""
        if self.graph.number_of_nodes() == 0:
            print("⚠️ Network is empty. Please load data first.")
            return
        
        print("🔍 Analyzing network structure...")
        
        # Calculate centrality measures
        self.centrality = {
            'degree': nx.degree_centrality(self.graph),
            'betweenness': nx.betweenness_centrality(self.graph),
            'closeness': nx.closeness_centrality(self.graph)
        }
        
        # Detect communities - made optional since python-louvain might not be available
        self.communities = {}
        try:
            # Try using NetworkX's community detection first
            from networkx.algorithms import community
            communities_generator = community.girvan_newman(nx.Graph(self.graph))
            # Take the first level of communities
            top_level_communities = next(communities_generator)
            # Convert to a format similar to python-louvain's output
            for i, com in enumerate(top_level_communities):
                for node in com:
                    self.communities[node] = i
            print("✅ Community detection completed using NetworkX algorithms")
        except (ImportError, AttributeError) as e:
            print(f"⚠️ Community detection using NetworkX failed: {str(e)}")
            try:
                # Try using python-louvain as fallback (if available)
                from community import best_partition
                self.communities = best_partition(nx.Graph(self.graph))
                print("✅ Community detection completed using python-louvain")
            except ImportError:
                print("⚠️ Community detection requires either NetworkX community algorithms or python-louvain package.")
                print("⚠️ Community detection will be skipped. Visualization will use file types for coloring instead.")
        
        # Generate recommendations
        self._generate_recommendations()
        
        print("✅ Network analysis complete")
    
    def _generate_recommendations(self):
        """Generate recommendations based on network analysis"""
        self.recommendations = []
        
        # Find structural holes (high betweenness nodes that bridge communities)
        betweenness = self.centrality['betweenness']
        if betweenness:
            high_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
            for file, score in high_betweenness:
                if score > 0.1:  # Threshold for consideration
                    self.recommendations.append({
                        'type': 'structural_bridge',
                        'file': file,
                        'score': score,
                        'action': f"Review and enhance {file} as it serves as a critical bridge between components"
                    })
        
        # Find isolated components that should be connected
        for component in nx.weakly_connected_components(self.graph):
            if 1 < len(component) < 5:  # Small isolated components
                self.recommendations.append({
                    'type': 'isolated_component',
                    'files': list(component),
                    'action': f"Connect isolated component with main system: {', '.join(list(component)[:3])}"
                })
        
        # Find potential refactoring opportunities (high out-degree nodes)
        out_degree = {node: self.graph.out_degree(node) for node in self.graph.nodes()}
        high_outdegree = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[:5]
        for file, degree in high_outdegree:
            if degree > 10:  # Threshold for consideration
                self.recommendations.append({
                    'type': 'high_coupling',
                    'file': file,
                    'degree': degree,
                    'action': f"Consider refactoring {file} as it has high outward coupling ({degree} dependencies)"
                })
    
    def visualize_network(self, max_nodes=150):
        """Create a visualization of the network"""
        if self.graph.number_of_nodes() == 0:
            print("⚠️ Network is empty. Please load data first.")
            return
        
        print(f"📊 Generating network visualization...")
        
        # Create a simplified graph if too large
        if self.graph.number_of_nodes() > max_nodes:
            print(f"⚠️ Network is large ({self.graph.number_of_nodes()} nodes). Creating simplified view.")
            # Keep most central nodes
            betweenness = nx.betweenness_centrality(self.graph)
            important_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
            important_node_names = [n[0] for n in important_nodes]
            subgraph = self.graph.subgraph(important_node_names)
            vis_graph = subgraph
        else:
            vis_graph = self.graph
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        # Set up node colors based on file type or community
        if self.communities:
            node_colors = [self.communities.get(node, 0) for node in vis_graph.nodes()]
        else:
            # Color by file extension
            ext_colors = {
                '.py': 'blue',
                '.js': 'yellow',
                '.html': 'red',
                '.md': 'green',
                '.json': 'purple',
                '.css': 'orange',
                '.txt': 'gray'
            }
            node_colors = [ext_colors.get(os.path.splitext(node)[1], 'black') for node in vis_graph.nodes()]
        
        # Set node size based on centrality or file size
        if hasattr(self, 'centrality') and self.centrality.get('betweenness'):
            node_sizes = [5000 * self.centrality['betweenness'].get(node, 0.1) + 50 for node in vis_graph.nodes()]
        else:
            node_sizes = [100 for _ in vis_graph.nodes()]
        
        # Generate layout
        pos = nx.spring_layout(vis_graph)
        
        # Draw the graph
        nx.draw_networkx(
            vis_graph, pos, 
            with_labels=False,
            node_color=node_colors,
            node_size=node_sizes,
            alpha=0.7,
            edge_color='gray',
            arrows=True,
            width=0.5
        )
        
        # Add labels for important nodes only
        if vis_graph.number_of_nodes() > 30:
            # Label only the most central nodes
            centrality = nx.degree_centrality(vis_graph)
            important_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:15]
            important_node_dict = {n[0]: os.path.basename(n[0]) for n in important_nodes}
            nx.draw_networkx_labels(vis_graph, pos, labels=important_node_dict, font_size=8)
        else:
            # Use basename to shorten labels
            labels = {node: os.path.basename(node) for node in vis_graph.nodes()}
            nx.draw_networkx_labels(vis_graph, pos, labels=labels, font_size=8)
        
        plt.title("EVA & GUARANI - Mycelium Network Analysis")
        plt.axis('off')
        
        # Save the visualization
        plt.savefig(NETWORK_IMAGE, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Save network data for interactive visualization
        self._export_network_data()
        
        print(f"✅ Visualization saved to {NETWORK_IMAGE}")
        
    def _export_network_data(self):
        """Export network data in JSON format for interactive visualization"""
        # Format data for visualization libraries
        nodes = []
        for node in self.graph.nodes():
            node_data = {
                "id": node,
                "label": os.path.basename(node),
                "group": self.communities.get(node, 0) if self.communities else 1,
                "type": os.path.splitext(node)[1],
                "size": self.graph.nodes[node].get('size', 0),
                "lines": self.graph.nodes[node].get('lines', 0)
            }
            
            # Add centrality measures if available
            if hasattr(self, 'centrality'):
                for measure, values in self.centrality.items():
                    if node in values:
                        node_data[measure] = values[node]
            
            nodes.append(node_data)
        
        edges = []
        for source, target in self.graph.edges():
            edges.append({
                "source": source,
                "target": target,
                "type": self.graph.edges[source, target].get('type', 'unknown')
            })
        
        network_data = {
            "nodes": nodes,
            "links": edges,
            "metadata": {
                "timestamp": str(Path(NETWORK_FILE).stat().st_mtime) if os.path.exists(NETWORK_FILE) else None,
                "node_count": self.graph.number_of_nodes(),
                "edge_count": self.graph.number_of_edges()
            }
        }
        
        with open(NETWORK_FILE, 'w', encoding='utf-8') as f:
            json.dump(network_data, f, indent=2)
    
    def generate_report(self):
        """Generate a report with network analysis and recommendations"""
        report_file = os.path.join(VISUALIZATIONS_DIR, "mycelium_network_report.md")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("""# Mycelium Network Analysis Report

## Overview

This report provides insights from the network analysis of code connections in the EVA & GUARANI project.

""")
            
            # Add network statistics
            f.write("## Network Statistics\n\n")
            f.write(f"- **Total Files**: {self.graph.number_of_nodes()}\n")
            f.write(f"- **Total Connections**: {self.graph.number_of_edges()}\n")
            
            # Calculate network density
            density = nx.density(self.graph)
            f.write(f"- **Network Density**: {density:.4f}\n")
            
            # Count connected components
            weak_components = list(nx.weakly_connected_components(self.graph))
            f.write(f"- **Connected Components**: {len(weak_components)}\n")
            
            # Add information about largest component
            if weak_components:
                largest_component = max(weak_components, key=len)
                f.write(f"- **Largest Component Size**: {len(largest_component)} files ({len(largest_component)/self.graph.number_of_nodes()*100:.1f}% of total)\n\n")
            else:
                f.write("- **Largest Component Size**: 0 (empty graph)\n\n")
            
            # Add most central files
            f.write("## Most Central Files\n\n")
            f.write("Files that serve as important connection points in the system:\n\n")
            
            if hasattr(self, 'centrality') and self.centrality.get('betweenness'):
                top_central = sorted(self.centrality['betweenness'].items(), key=lambda x: x[1], reverse=True)[:10]
                for file, score in top_central:
                    f.write(f"- **{file}** (centrality score: {score:.4f})\n")
            else:
                f.write("*Centrality analysis not available*\n")
            
            f.write("\n")
            
            # Add recommendations
            f.write("## Recommendations\n\n")
            
            if self.recommendations:
                for i, rec in enumerate(self.recommendations):
                    f.write(f"### {i+1}. {rec['action']}\n\n")
                    
                    if rec['type'] == 'structural_bridge':
                        f.write(f"**File**: {rec['file']}\n")
                        f.write(f"**Centrality Score**: {rec['score']:.4f}\n")
                        f.write("\nThis file serves as a critical bridge between different parts of the system. "
                                "Consider enhancing its documentation and ensuring it has proper tests.\n\n")
                    
                    elif rec['type'] == 'isolated_component':
                        f.write(f"**Files**: {', '.join(rec['files'][:3])}" + 
                                (f" and {len(rec['files'])-3} more" if len(rec['files']) > 3 else "") + "\n\n")
                        f.write("This group of files forms an isolated component that isn't well connected to the rest "
                                "of the system. Consider integrating it more tightly or evaluating if it should be a separate module.\n\n")
                    
                    elif rec['type'] == 'high_coupling':
                        f.write(f"**File**: {rec['file']}\n")
                        f.write(f"**Outgoing Dependencies**: {rec['degree']}\n\n")
                        f.write("This file has an unusually high number of outgoing dependencies, which may indicate "
                                "it's doing too much. Consider refactoring to reduce coupling.\n\n")
            else:
                f.write("*No recommendations available*\n")
            
            # Add visualization reference
            f.write("\n## Visualization\n\n")
            f.write(f"A network visualization has been saved to: `{os.path.relpath(NETWORK_IMAGE, PROJECT_ROOT)}`\n\n")
            
            # Add JSON data reference
            f.write(f"Interactive visualization data available at: `{os.path.relpath(NETWORK_FILE, PROJECT_ROOT)}`\n\n")
            
            # Add signature
            f.write("\n\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")
        
        print(f"✅ Network analysis report generated at {report_file}")
    
    def run_analysis(self):
        """Run the complete network analysis pipeline"""
        if not self.quantum_mycelium:
            print("Loading data from quantum mycelium analysis...")
            self.load_from_quantum_mycelium()
        
        self.analyze_network()
        self.visualize_network()
        self.generate_report()
        
        return self.recommendations

# ========================================================================
# MAIN FUNCTIONS
# ========================================================================

def run_mycelium_network_analysis():
    """Run the mycelium network analysis"""
    # Create and run the network analysis
    network = MyceliumNetwork()
    network.load_from_quantum_mycelium()
    recommendations = network.run_analysis()
    
    print(f"\n✧༺❀༻∞ EVA & GUARANI - Mycelium Network Analysis ∞༺❀༻✧\n")
    print(f"Generated {len(recommendations)} recommendations")
    
    return network

if __name__ == "__main__":
    run_mycelium_network_analysis() 