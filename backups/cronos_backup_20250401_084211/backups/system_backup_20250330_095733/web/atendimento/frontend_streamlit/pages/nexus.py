#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - NEXUS (Modular Analysis)
Streamlit Interface for the NEXUS module.

Date: 2025-03-20
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
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
st.set_page_config(page_title="EVA & GUARANI - NEXUS", page_icon="🔮", layout="wide")

# Apply page style
set_page_style()


def initialize_session():
    """Initialize session variables."""
    if "nexus_initialized" not in st.session_state:
        st.session_state.nexus_initialized = False
    if "eva_system" not in st.session_state:
        st.session_state.eva_system = None
    if "components" not in st.session_state:
        st.session_state.components = []
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = {}
    if "optimization_history" not in st.session_state:
        st.session_state.optimization_history = []


def initialize_system():
    """Initialize the EVA & GUARANI system."""
    with st.spinner("Initializing NEXUS system..."):
        core_path = "C:/Eva & Guarani - EGOS/core"

        if st.session_state.eva_system is None:
            try:
                eva_system = EVASystem(core_path)

                # Initialize interfaces
                initialization_success = eva_system.initialize()

                if initialization_success:
                    st.session_state.eva_system = eva_system
                    st.session_state.nexus_initialized = True
                    st.success("NEXUS system initialized successfully!")
                    return True
                else:
                    st.error("Failed to initialize the NEXUS system")
                    return False
            except Exception as e:
                st.error(f"Error during initialization: {str(e)}")
                return False
        else:
            return True


def analyze_component_form():
    """Form to analyze a system component."""
    if len(st.session_state.components) == 0:
        st.info("No component available for analysis")
        return

    with st.form("analysis_form"):
        st.subheader("Analyze Component")

        # Extract list of available components
        component_options = {
            f"{comp['name']} ({comp['type']})": comp["id"] for comp in st.session_state.components
        }

        selected_component = st.selectbox(
            "Select Component", options=list(component_options.keys())
        )

        analysis_level = st.select_slider(
            "Analysis Level",
            options=["Superficial", "Intermediate", "Deep", "Quantum"],
            value="Intermediate",
        )

        include_metrics = st.checkbox("Include Metrics", value=True)
        include_dependencies = st.checkbox("Analyze Dependencies", value=True)

        submitted = st.form_submit_button("Analyze")

        if submitted and selected_component:
            if st.session_state.nexus_initialized:
                try:
                    component_id = component_options[selected_component]

                    # Perform analysis using the NEXUS interface
                    analysis = st.session_state.eva_system.nexus.analyze_component(
                        component_id=component_id,
                        analysis_level=analysis_level.lower(),
                        include_metrics=include_metrics,
                        include_dependencies=include_dependencies,
                    )

                    if analysis:
                        st.session_state.analysis_results[component_id] = analysis
                        st.success("Analysis completed successfully!")
                        # Update system data
                        update_system_data()
                    else:
                        st.error("Failed to perform analysis")
                except Exception as e:
                    st.error(f"Error analyzing component: {str(e)}")
            else:
                st.warning("NEXUS system not initialized")


def optimize_component_form():
    """Form to optimize a system component."""
    if len(st.session_state.components) == 0:
        st.info("No component available for optimization")
        return

    with st.form("optimization_form"):
        st.subheader("Optimize Component")

        # Extract list of available components
        component_options = {
            f"{comp['name']} ({comp['type']})": comp["id"] for comp in st.session_state.components
        }

        selected_component = st.selectbox(
            "Select Component", options=list(component_options.keys())
        )

        optimization_target = st.selectbox(
            "Optimization Target",
            options=["Performance", "Quality", "Integration", "Consciousness"],
        )

        col1, col2 = st.columns(2)
        with col1:
            love_threshold = st.slider("Love Quotient Threshold", 0.0, 1.0, 0.95, 0.01)
        with col2:
            consciousness_threshold = st.slider("Consciousness Threshold", 0.0, 1.0, 0.90, 0.01)

        create_backup = st.checkbox("Create Backup Before", value=True)

        submitted = st.form_submit_button("Optimize")

        if submitted and selected_component:
            if st.session_state.nexus_initialized:
                try:
                    component_id = component_options[selected_component]

                    # Perform optimization using the NEXUS interface
                    optimization = st.session_state.eva_system.nexus.optimize_component(
                        component_id=component_id,
                        target=optimization_target.lower(),
                        love_threshold=love_threshold,
                        consciousness_threshold=consciousness_threshold,
                        create_backup=create_backup,
                    )

                    if optimization:
                        st.success("Optimization completed successfully!")
                        # Update system data
                        update_system_data()
                    else:
                        st.error("Failed to optimize component")
                except Exception as e:
                    st.error(f"Error optimizing component: {str(e)}")
            else:
                st.warning("NEXUS system not initialized")


def update_system_data():
    """Update system data by loading components and analyses."""
    if st.session_state.nexus_initialized:
        try:
            # Get data from core
            nexus_core = st.session_state.eva_system.nexus.nexus_core

            # Update components
            st.session_state.components = nexus_core.get_components()

            # Update optimization history
            st.session_state.optimization_history = nexus_core.get_optimization_history()

        except Exception as e:
            st.error(f"Error updating system data: {str(e)}")


def display_component_metrics():
    """Display metrics of the system components."""
    if not st.session_state.components:
        st.info("No registered component")
        return

    # Create dataframe with component metrics
    metrics_data = []
    for comp in st.session_state.components:
        metrics = comp.get("metrics", {})
        metrics_data.append(
            {
                "name": comp["name"],
                "type": comp["type"],
                "love_quotient": metrics.get("love_quotient", 0),
                "consciousness_level": metrics.get("consciousness_level", 0),
                "quality_score": metrics.get("quality_score", 0),
                "integration_score": metrics.get("integration_score", 0),
            }
        )

    df = pd.DataFrame(metrics_data)

    # Create radar chart for each component
    for _, row in df.iterrows():
        metrics = {
            "Love Quotient": row["love_quotient"],
            "Consciousness": row["consciousness_level"],
            "Quality": row["quality_score"],
            "Integration": row["integration_score"],
        }

        categories = list(metrics.keys())
        values = list(metrics.values())

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill="toself", name=row["name"]))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title=f"Metrics: {row['name']} ({row['type']})",
        )

        st.plotly_chart(fig, use_container_width=True)


def display_optimization_history():
    """Display the optimization history of the system."""
    if not st.session_state.optimization_history:
        st.info("No optimization history available")
        return

    # Create dataframe with history
    df = pd.DataFrame(st.session_state.optimization_history)

    # Create timeline chart
    fig = px.line(
        df,
        x="timestamp",
        y=["performance_gain", "quality_improvement", "consciousness_increase"],
        title="Optimization History",
        labels={"timestamp": "Date", "value": "Gain", "variable": "Metric"},
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display table with details
    st.dataframe(df, use_container_width=True)


def display_component_dependencies():
    """Display the dependencies between system components."""
    if not st.session_state.components:
        st.info("No dependencies to display")
        return

    # Create dependency matrix
    component_names = [comp["name"] for comp in st.session_state.components]
    n_components = len(component_names)

    # Create example random matrix (replace with real data)
    dependency_matrix = np.random.rand(n_components, n_components)
    np.fill_diagonal(dependency_matrix, 0)  # No self-dependency

    # Create heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=dependency_matrix, x=component_names, y=component_names, colorscale="Viridis"
        )
    )

    fig.update_layout(title="Dependency Matrix", xaxis_title="Component", yaxis_title="Depends on")

    st.plotly_chart(fig, use_container_width=True)


def main():
    """Main function of the application."""
    # Initialize session variables
    initialize_session()

    # Title and description
    st.title("🔮 NEXUS - Modular Analysis")
    st.markdown(
        """
    The NEXUS module is responsible for analyzing and optimizing the components of the EVA & GUARANI system,
    ensuring quality, integration, and conscious evolution.
    """
    )

    # Initialize the system
    initialize_button = st.button("Initialize NEXUS")
    if initialize_button:
        initialize_system()

    # Check if the system is initialized
    if not st.session_state.nexus_initialized:
        st.warning("The NEXUS system needs to be initialized")
        # Demonstration image
        st.image("https://via.placeholder.com/800x400?text=NEXUS+Module")
    else:
        # Update system data
        update_button = st.button("Update Data")
        if update_button:
            update_system_data()

        # Create tabs to organize content
        tab1, tab2, tab3, tab4 = st.tabs(["Metrics", "Analysis", "Optimization", "Dependencies"])

        with tab1:
            # Metrics visualization
            display_component_metrics()

        with tab2:
            # Component analysis
            col1, col2 = st.columns([2, 1])

            with col1:
                if st.session_state.analysis_results:
                    for comp_id, analysis in st.session_state.analysis_results.items():
                        with st.expander(f"Analysis: {analysis.get('name', comp_id)}"):
                            st.json(analysis)

            with col2:
                analyze_component_form()

        with tab3:
            # Component optimization
            col1, col2 = st.columns([2, 1])

            with col1:
                display_optimization_history()

            with col2:
                optimize_component_form()

        with tab4:
            # Dependencies visualization
            display_component_dependencies()

    # Application footer
    display_footer()


if __name__ == "__main__":
    main()
