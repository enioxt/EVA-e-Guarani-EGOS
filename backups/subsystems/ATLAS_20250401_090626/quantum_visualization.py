#!/usr/bin/env python3
"""
Quantum Visualization Module for EVA & GUARANI
Handles advanced visualization of quantum connections between subsystems
"""

import json
from typing import Dict, List, Optional
import networkx as nx
from pathlib import Path
import plotly.graph_objects as go
from dataclasses import dataclass
import logging


@dataclass
class QuantumConnection:
    source: str
    target: str
    strength: float
    connection_type: str
    metadata: Dict


class QuantumVisualizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.graph = nx.Graph()
        self.connections = []
        self.subsystems = set()

    def add_connection(
        self,
        source: str,
        target: str,
        strength: float = 0.5,
        connection_type: str = "quantum",
        metadata: Optional[Dict] = None,
    ):
        """Add a quantum connection between subsystems"""
        if metadata is None:
            metadata = {}

        connection = QuantumConnection(
            source=source,
            target=target,
            strength=strength,
            connection_type=connection_type,
            metadata=metadata,
        )

        self.connections.append(connection)
        self.subsystems.add(source)
        self.subsystems.add(target)

        # Update network graph
        self.graph.add_edge(source, target, weight=strength, type=connection_type, **metadata)

    def generate_mermaid_diagram(self) -> str:
        """Generate a Mermaid.js compatible diagram"""
        mermaid = ["graph TD"]

        # Add nodes with styling
        for subsystem in self.subsystems:
            node_id = subsystem.replace(" ", "_")
            mermaid.append(f'    {node_id}["{subsystem}"]')

        # Add connections with strength indicators
        for conn in self.connections:
            source = conn.source.replace(" ", "_")
            target = conn.target.replace(" ", "_")
            # Represent connection strength in line thickness
            style = "==>" if conn.strength > 0.7 else "-->"
            mermaid.append(f"    {source} {style} {target}")

        return "\n".join(mermaid)

    def generate_interactive_visualization(self) -> go.Figure:
        """Generate an interactive visualization using Plotly"""
        # Create network layout
        pos = nx.spring_layout(self.graph)

        # Create edges (connections)
        edge_x = []
        edge_y = []
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y, line=dict(width=0.5, color="#888"), hoverinfo="none", mode="lines"
        )

        # Create nodes
        node_x = []
        node_y = []
        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            hoverinfo="text",
            text=list(self.graph.nodes()),
            textposition="top center",
            marker=dict(
                showscale=True,
                colorscale="YlGnBu",
                size=20,
                colorbar=dict(
                    thickness=15, title="Connection Strength", xanchor="left", titleside="right"
                ),
            ),
        )

        # Create the figure
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title="EVA & GUARANI Quantum Connections",
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        )

        return fig

    def export_visualization(self, output_path: str, format: str = "html"):
        """Export the visualization to a file"""
        if format == "html":
            fig = self.generate_interactive_visualization()
            fig.write_html(output_path)
        elif format == "mermaid":
            mermaid = self.generate_mermaid_diagram()
            with open(output_path, "w") as f:
                f.write(mermaid)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def analyze_connections(self) -> Dict:
        """Analyze the quantum connections and return metrics"""
        return {
            "total_connections": len(self.connections),
            "total_subsystems": len(self.subsystems),
            "average_strength": (
                sum(c.strength for c in self.connections) / len(self.connections)
                if self.connections
                else 0
            ),
            "connection_types": {c.connection_type for c in self.connections},
            "density": nx.density(self.graph),
            "clustering_coefficient": nx.average_clustering(self.graph),
        }


# Example usage
if __name__ == "__main__":
    visualizer = QuantumVisualizer()

    # Add some example connections
    visualizer.add_connection("CRONOS", "ATLAS", 0.8, "primary")
    visualizer.add_connection("ATLAS", "NEXUS", 0.9, "primary")
    visualizer.add_connection("NEXUS", "ETHIK", 0.7, "secondary")

    # Generate and save visualizations
    visualizer.export_visualization("quantum_connections.html", "html")
    visualizer.export_visualization("quantum_connections.md", "mermaid")

    # Analyze connections
    metrics = visualizer.analyze_connections()
    print(json.dumps(metrics, indent=2))
