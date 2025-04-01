#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - ATLAS (Systemic Cartography)
Streamlit Interface for the ATLAS module.

Date: 2025-03-20
"""

import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os
from pathlib import Path

# Add parent directory to path to import common modules
sys.path.append(str(Path(__file__).parent.parent))
from utils import set_page_style, display_footer
from integrations import EVASystem

# Page configuration
st.set_page_config(
    page_title="EVA & GUARANI - ATLAS",
    page_icon="🌌",
    layout="wide"
)

# Apply page style
set_page_style()

def initialize_session():
    """Initialize session variables."""
    if "atlas_initialized" not in st.session_state:
        st.session_state.atlas_initialized = False
    if "eva_system" not in st.session_state:
        st.session_state.eva_system = None
    if "graph" not in st.session_state:
        st.session_state.graph = nx.Graph()
    if "nodes" not in st.session_state:
        st.session_state.nodes = []
    if "connections" not in st.session_state:
        st.session_state.connections = []

def initialize_system():
    """Initialize the EVA & GUARANI system."""
    with st.spinner("Initializing ATLAS system..."):
        core_path = "C:/Eva & Guarani - EGOS/core"
        
        if st.session_state.eva_system is None:
            try:
                eva_system = EVASystem(core_path)
                
                # Initialize interfaces
                initialization_success = eva_system.initialize()
                
                if initialization_success:
                    st.session_state.eva_system = eva_system
                    st.session_state.atlas_initialized = True
                    st.success("ATLAS system initialized successfully!")
                    return True
                else:
                    st.error("Failed to initialize the ATLAS system")
                    return False
            except Exception as e:
                st.error(f"Error initializing: {str(e)}")
                return False
        else:
            return True

def create_node_form():
    """Form to create a new node in the system."""
    with st.form("node_form"):
        st.subheader("Create New Node")
        
        name = st.text_input("Node Name")
        node_type = st.selectbox(
            "Node Type",
            options=["System", "Component", "Concept", "Entity", "Process"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            love_quotient = st.slider("Love Quotient", 0.0, 1.0, 0.95, 0.01)
        with col2:
            consciousness_level = st.slider("Consciousness Level", 0.0, 1.0, 0.90, 0.01)
        
        description = st.text_area("Description")
        
        submitted = st.form_submit_button("Create Node")
        
        if submitted and name:
            if st.session_state.atlas_initialized:
                try:
                    metadata = {
                        "description": description,
                        "created_by": "EVA_Frontend"
                    }
                    
                    # Create node using the ATLAS interface
                    node_id = st.session_state.eva_system.atlas.create_node(
                        name=name,
                        node_type=node_type,
                        metadata=metadata,
                        love_quotient=love_quotient,
                        consciousness_level=consciousness_level
                    )
                    
                    if node_id:
                        st.success(f"Node '{name}' created successfully!")
                        # Update the list of nodes
                        update_system_data()
                    else:
                        st.error("Failed to create node")
                except Exception as e:
                    st.error(f"Error creating node: {str(e)}")
            else:
                st.warning("ATLAS system not initialized")

def create_connection_form():
    """Form to create a new connection between nodes."""
    if len(st.session_state.nodes) < 2:
        st.warning("At least two nodes are required to create a connection")
        return
    
    with st.form("connection_form"):
        st.subheader("Create New Connection")
        
        # Extract list of available nodes
        node_options = {node["name"]: node["id"] for node in st.session_state.nodes}
        
        # Form fields
        source_name = st.selectbox("Source Node", options=list(node_options.keys()))
        target_name = st.selectbox("Target Node", options=list(node_options.keys()))
        
        conn_type = st.selectbox(
            "Connection Type",
            options=["Dependency", "Communication", "Contains", "Influences", "Transforms"]
        )
        
        strength = st.slider("Connection Strength", 0.0, 1.0, 0.8, 0.01)
        description = st.text_area("Connection Description")
        
        submitted = st.form_submit_button("Create Connection")
        
        if submitted and source_name != target_name:
            if st.session_state.atlas_initialized:
                try:
                    source_id = node_options[source_name]
                    target_id = node_options[target_name]
                    
                    metadata = {
                        "description": description,
                        "created_by": "EVA_Frontend"
                    }
                    
                    # Create connection using the ATLAS interface
                    conn_id = st.session_state.eva_system.atlas.create_connection(
                        source_id=source_id,
                        target_id=target_id,
                        conn_type=conn_type,
                        strength=strength,
                        metadata=metadata
                    )
                    
                    if conn_id:
                        st.success(f"Connection created successfully between '{source_name}' and '{target_name}'!")
                        # Update the list of connections
                        update_system_data()
                    else:
                        st.error("Failed to create connection")
                except Exception as e:
                    st.error(f"Error creating connection: {str(e)}")
            else:
                st.warning("ATLAS system not initialized")

def update_system_data():
    """Update system data by loading nodes and connections."""
    if st.session_state.atlas_initialized:
        try:
            # Get nodes and connections from core
            atlas_core = st.session_state.eva_system.atlas.atlas_core
            
            # Update nodes
            st.session_state.nodes = [
                {
                    "id": node.id,
                    "name": node.name,
                    "type": node.type,
                    "love_quotient": node.love_quotient,
                    "consciousness_level": node.consciousness_level,
                    "metadata": node.metadata
                }
                for node in atlas_core.nodes.values()
            ]
            
            # Update connections
            st.session_state.connections = [
                {
                    "id": conn.id,
                    "source_id": conn.source_id,
                    "target_id": conn.target_id,
                    "type": conn.type,
                    "strength": conn.strength,
                    "metadata": conn.metadata
                }
                for conn in atlas_core.connections.values()
            ]
            
            # Update graph
            G = nx.Graph()
            
            # Add nodes
            for node in st.session_state.nodes:
                G.add_node(
                    node["id"],
                    name=node["name"],
                    type=node["type"],
                    love_quotient=node["love_quotient"],
                    consciousness_level=node["consciousness_level"]
                )
            
            # Add connections
            for conn in st.session_state.connections:
                G.add_edge(
                    conn["source_id"],
                    conn["target_id"],
                    type=conn["type"],
                    strength=conn["strength"]
                )
            
            st.session_state.graph = G
            
        except Exception as e:
            st.error(f"Error updating system data: {str(e)}")

def create_network_graph():
    """Create a network graph visualization."""
    G = st.session_state.graph
    
    if len(G.nodes) == 0:
        st.info("No nodes available for visualization")
        return
    
    # Create graph layout
    pos = nx.spring_layout(G, seed=42)
    
    # Create traces for nodes
    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers+text',
        text=[G.nodes[node]['name'] for node in G.nodes()],
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=15,
            color=[G.nodes[node]['love_quotient'] * 100 for node in G.nodes()],
            colorscale='Viridis',
            colorbar=dict(title='Love Quotient'),
            line=dict(width=2)
        ),
        hovertext=[f"Name: {G.nodes[node]['name']}<br>"
                   f"Type: {G.nodes[node]['type']}<br>"
                   f"Love Quotient: {G.nodes[node]['love_quotient']:.2f}<br>"
                   f"Consciousness: {G.nodes[node]['consciousness_level']:.2f}"
                   for node in G.nodes()]
    )
    
    # Create traces for connections
    edge_x = []
    edge_y = []
    edge_text = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        source_name = G.nodes[edge[0]]['name']
        target_name = G.nodes[edge[1]]['name']
        edge_type = G.edges[edge].get('type', 'Default')
        strength = G.edges[edge].get('strength', 0.5)
        
        edge_text.append(f"Type: {edge_type}<br>"
                        f"Strength: {strength:.2f}<br>"
                        f"From: {source_name}<br>"
                        f"To: {target_name}")
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='text',
        mode='lines',
        hovertext=edge_text
    )
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                  layout=go.Layout(
                      title='System Map',
                      showlegend=False,
                      hovermode='closest',
                      margin=dict(b=20,l=5,r=5,t=40),
                      plot_bgcolor='rgba(240,240,240,0.8)',
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                  ))
    
    st.plotly_chart(fig, use_container_width=True)

def display_system_analysis():
    """Display the ATLAS system analysis."""
    if st.session_state.atlas_initialized:
        try:
            # Get system analysis
            analysis = st.session_state.eva_system.atlas.analyze_system()
            
            if not analysis:
                st.warning("Unable to obtain system analysis")
                return
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Nodes", analysis.get("node_count", 0))
            with col2:
                st.metric("Connections", analysis.get("connection_count", 0))
            with col3:
                love_quotient = analysis.get("average_love_quotient", 0)
                st.metric("Average Love Quotient", f"{love_quotient:.2f}")
            with col4:
                health = analysis.get("system_health", 0)
                st.metric("System Health", f"{health:.2f}")
            
            # Full details
            with st.expander("Analysis Details"):
                # Format timestamp
                timestamp = analysis.get("timestamp")
                if isinstance(timestamp, datetime):
                    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    formatted_time = str(timestamp)
                
                st.markdown(f"**Last analysis:** {formatted_time}")
                st.markdown(f"**Average Consciousness Level:** {analysis.get('average_consciousness_level', 0):.4f}")
                
                # Additional data if available
                for key, value in analysis.items():
                    if key not in ["node_count", "connection_count", "average_love_quotient", 
                                  "average_consciousness_level", "system_health", "timestamp"]:
                        st.markdown(f"**{key}:** {value}")
            
        except Exception as e:
            st.error(f"Error displaying system analysis: {str(e)}")
    else:
        st.warning("ATLAS system not initialized")

def display_node_table():
    """Display a table with the system nodes."""
    if len(st.session_state.nodes) == 0:
        st.info("No nodes registered in the system")
        return
    
    # Create dataframe
    nodes_df = pd.DataFrame(st.session_state.nodes)
    
    if not nodes_df.empty:
        # Select and rename columns for display
        display_columns = {
            "name": "Name",
            "type": "Type",
            "love_quotient": "Love Quotient",
            "consciousness_level": "Consciousness"
        }
        
        filtered_df = nodes_df[display_columns.keys()].rename(columns=display_columns)
        st.dataframe(filtered_df, use_container_width=True)

def display_connection_table():
    """Display a table with the system connections."""
    if len(st.session_state.connections) == 0:
        st.info("No connections registered in the system")
        return
    
    try:
        # Create dataframe
        connections_df = pd.DataFrame(st.session_state.connections)
        
        if not connections_df.empty:
            # Map IDs to names
            node_map = {node["id"]: node["name"] for node in st.session_state.nodes}
            
            # Add columns with names
            connections_df["source_name"] = connections_df["source_id"].map(node_map)
            connections_df["target_name"] = connections_df["target_id"].map(node_map)
            
            # Select and rename columns for display
            display_columns = {
                "source_name": "Source",
                "target_name": "Target",
                "type": "Type",
                "strength": "Strength"
            }
            
            filtered_df = connections_df[display_columns.keys()].rename(columns=display_columns)
            st.dataframe(filtered_df, use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying connection table: {str(e)}")

def main():
    """Main function of the application."""
    # Initialize session variables
    initialize_session()
    
    # Title and description
    st.title("🌌 ATLAS - Systemic Cartography")
    st.markdown("""
    The ATLAS module allows mapping and visualizing the topology of the EVA & GUARANI system,
    analyzing connections, recognizing patterns, and optimizing structures.
    """)
    
    # Initialize the system
    initialize_button = st.button("Initialize ATLAS")
    if initialize_button:
        initialize_system()
    
    # Check if the system is initialized
    if not st.session_state.atlas_initialized:
        st.warning("The ATLAS system needs to be initialized")
        # Demo image
        st.image("https://via.placeholder.com/800x400?text=ATLAS+Module")
    else:
        # Update system data
        update_button = st.button("Update Data")
        if update_button:
            update_system_data()
        
        # Create tabs to organize content
        tab1, tab2, tab3, tab4 = st.tabs(["Visualization", "Analysis", "Nodes", "Connections"])
        
        with tab1:
            # System visualization
            create_network_graph()
            
        with tab2:
            # System analysis
            display_system_analysis()
        
        with tab3:
            # Node management
            col1, col2 = st.columns([2, 1])
            
            with col1:
                display_node_table()
            
            with col2:
                create_node_form()
        
        with tab4:
            # Connection management
            col1, col2 = st.columns([2, 1])
            
            with col1:
                display_connection_table()
            
            with col2:
                create_connection_form()
    
    # Application footer
    display_footer()

if __name__ == "__main__":
    main()