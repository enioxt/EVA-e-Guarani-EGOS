#!/usr/bin/env python3
"""
Test suite for the Quantum Visualization module
"""

import pytest
import json
import os
from pathlib import Path
import networkx as nx
import plotly.graph_objects as go
from ..quantum_visualization import QuantumVisualizer, QuantumConnection

@pytest.fixture
def visualizer():
    """Create a fresh visualizer instance for each test"""
    return QuantumVisualizer()

@pytest.fixture
def sample_connections(visualizer):
    """Create a set of sample connections for testing"""
    connections = [
        ("CRONOS", "ATLAS", 0.8, "primary"),
        ("ATLAS", "NEXUS", 0.9, "primary"),
        ("NEXUS", "ETHIK", 0.7, "secondary"),
        ("ETHIK", "MASTER", 0.85, "primary"),
    ]
    
    for source, target, strength, conn_type in connections:
        visualizer.add_connection(source, target, strength, conn_type)
    
    return visualizer

def test_add_connection(visualizer):
    """Test adding a new connection"""
    visualizer.add_connection("CRONOS", "ATLAS", 0.8, "primary")
    
    assert len(visualizer.connections) == 1
    assert len(visualizer.subsystems) == 2
    assert visualizer.graph.number_of_edges() == 1
    
    conn = visualizer.connections[0]
    assert conn.source == "CRONOS"
    assert conn.target == "ATLAS"
    assert conn.strength == 0.8
    assert conn.connection_type == "primary"

def test_add_connection_with_metadata(visualizer):
    """Test adding a connection with metadata"""
    metadata = {"priority": "high", "description": "Critical path"}
    visualizer.add_connection("CRONOS", "ATLAS", 0.8, "primary", metadata)
    
    conn = visualizer.connections[0]
    assert conn.metadata == metadata
    assert visualizer.graph.edges[("CRONOS", "ATLAS")]["priority"] == "high"

def test_generate_mermaid_diagram(sample_connections):
    """Test Mermaid diagram generation"""
    diagram = sample_connections.generate_mermaid_diagram()
    
    # Check basic structure
    assert diagram.startswith("graph TD")
    
    # Check all nodes are present
    for subsystem in ["CRONOS", "ATLAS", "NEXUS", "ETHIK", "MASTER"]:
        assert f'["{subsystem}"]' in diagram
    
    # Check connections
    assert "CRONOS ==>" in diagram  # Strong connection (0.8)
    assert "NEXUS -->" in diagram   # Weaker connection (0.7)

def test_generate_interactive_visualization(sample_connections):
    """Test interactive visualization generation"""
    fig = sample_connections.generate_interactive_visualization()
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2  # Edge trace and node trace
    
    # Check figure layout
    assert fig.layout.title.text == "EVA & GUARANI Quantum Connections"
    assert fig.layout.showlegend == False
    assert fig.layout.hovermode == "closest"

def test_export_visualization(sample_connections, tmp_path):
    """Test visualization export functionality"""
    # Test HTML export
    html_path = tmp_path / "test_vis.html"
    sample_connections.export_visualization(str(html_path), "html")
    assert html_path.exists()
    assert html_path.stat().st_size > 0
    
    # Test Mermaid export
    mermaid_path = tmp_path / "test_vis.md"
    sample_connections.export_visualization(str(mermaid_path), "mermaid")
    assert mermaid_path.exists()
    assert mermaid_path.stat().st_size > 0
    
    # Test invalid format
    with pytest.raises(ValueError):
        sample_connections.export_visualization("invalid.txt", "invalid")

def test_analyze_connections(sample_connections):
    """Test connection analysis metrics"""
    metrics = sample_connections.analyze_connections()
    
    assert metrics["total_connections"] == 4
    assert metrics["total_subsystems"] == 5
    assert 0.8 <= metrics["average_strength"] <= 0.9  # Should be around 0.8125
    assert metrics["connection_types"] == {"primary", "secondary"}
    assert 0 < metrics["density"] < 1
    assert 0 <= metrics["clustering_coefficient"] <= 1

def test_empty_visualizer(visualizer):
    """Test behavior with no connections"""
    metrics = visualizer.analyze_connections()
    
    assert metrics["total_connections"] == 0
    assert metrics["total_subsystems"] == 0
    assert metrics["average_strength"] == 0
    assert metrics["connection_types"] == set()
    assert metrics["density"] == 0
    assert metrics["clustering_coefficient"] == 0

def test_duplicate_connections(visualizer):
    """Test handling of duplicate connections"""
    # Add same connection twice
    visualizer.add_connection("CRONOS", "ATLAS", 0.8, "primary")
    visualizer.add_connection("CRONOS", "ATLAS", 0.9, "primary")
    
    # Should update the existing connection rather than create duplicate
    assert len(visualizer.connections) == 2
    assert visualizer.graph.number_of_edges() == 1

def test_bidirectional_connections(visualizer):
    """Test bidirectional connections"""
    visualizer.add_connection("CRONOS", "ATLAS", 0.8, "primary")
    visualizer.add_connection("ATLAS", "CRONOS", 0.7, "secondary")
    
    # Should treat these as separate connections
    assert len(visualizer.connections) == 2
    assert visualizer.graph.number_of_edges() == 2

if __name__ == "__main__":
    pytest.main([__file__]) 