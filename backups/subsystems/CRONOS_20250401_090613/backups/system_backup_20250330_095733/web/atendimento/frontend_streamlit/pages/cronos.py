#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - CRONOS (Evolutionary Preservation)
Streamlit Interface for the CRONOS module.

Date: 2025-03-20
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Add parent directory to path to import common modules
sys.path.append(str(Path(__file__).parent.parent))
from utils import set_page_style, display_footer
from integrations import EVASystem

# Page configuration
st.set_page_config(
    page_title="EVA & GUARANI - CRONOS",
    page_icon="⌛",
    layout="wide"
)

# Apply page style
set_page_style()

def initialize_session():
    """Initialize session variables."""
    if "cronos_initialized" not in st.session_state:
        st.session_state.cronos_initialized = False
    if "eva_system" not in st.session_state:
        st.session_state.eva_system = None
    if "system_states" not in st.session_state:
        st.session_state.system_states = []
    if "backups" not in st.session_state:
        st.session_state.backups = []
    if "evolution_metrics" not in st.session_state:
        st.session_state.evolution_metrics = {}

def initialize_system():
    """Initialize the EVA & GUARANI system."""
    with st.spinner("Initializing CRONOS system..."):
        core_path = "C:/Eva & Guarani - EGOS/core"
        
        if st.session_state.eva_system is None:
            try:
                eva_system = EVASystem(core_path)
                
                # Initialize interfaces
                initialization_success = eva_system.initialize()
                
                if initialization_success:
                    st.session_state.eva_system = eva_system
                    st.session_state.cronos_initialized = True
                    st.success("CRONOS system initialized successfully!")
                    return True
                else:
                    st.error("Failed to initialize the CRONOS system")
                    return False
            except Exception as e:
                st.error(f"Error during initialization: {str(e)}")
                return False
        else:
            return True

def create_backup_form():
    """Form to create a new system backup."""
    with st.form("backup_form"):
        st.subheader("Create New Backup")
        
        backup_name = st.text_input("Backup Name")
        backup_type = st.selectbox(
            "Backup Type",
            options=["Complete", "Incremental", "Differential"]
        )
        
        description = st.text_area("Description")
        include_data = st.checkbox("Include Data", value=True)
        compress = st.checkbox("Compress Backup", value=True)
        
        submitted = st.form_submit_button("Create Backup")
        
        if submitted and backup_name:
            if st.session_state.cronos_initialized:
                try:
                    metadata = {
                        "description": description,
                        "include_data": include_data,
                        "compress": compress,
                        "created_by": "EVA_Frontend"
                    }
                    
                    # Create backup using the CRONOS interface
                    backup_id = st.session_state.eva_system.cronos.create_backup(
                        name=backup_name,
                        backup_type=backup_type,
                        metadata=metadata
                    )
                    
                    if backup_id:
                        st.success(f"Backup '{backup_name}' created successfully!")
                        # Update the list of backups
                        update_system_data()
                    else:
                        st.error("Failed to create backup")
                except Exception as e:
                    st.error(f"Error creating backup: {str(e)}")
            else:
                st.warning("CRONOS system not initialized")

def restore_backup_form():
    """Form to restore a system backup."""
    if len(st.session_state.backups) == 0:
        st.info("No backups available for restoration")
        return
    
    with st.form("restore_form"):
        st.subheader("Restore Backup")
        
        # Extract list of available backups
        backup_options = {
            f"{backup['name']} ({backup['created_at']})": backup['id'] 
            for backup in st.session_state.backups
        }
        
        selected_backup = st.selectbox(
            "Select Backup",
            options=list(backup_options.keys())
        )
        
        verify_integrity = st.checkbox("Verify Integrity", value=True)
        create_restore_point = st.checkbox("Create Restore Point", value=True)
        
        submitted = st.form_submit_button("Restore System")
        
        if submitted and selected_backup:
            if st.session_state.cronos_initialized:
                try:
                    backup_id = backup_options[selected_backup]
                    
                    # Confirm restoration
                    if st.warning("⚠️ This operation will restore the system to a previous state. Do you want to continue?"):
                        # Restore backup using the CRONOS interface
                        success = st.session_state.eva_system.cronos.restore_backup(
                            backup_id=backup_id,
                            verify_integrity=verify_integrity,
                            create_restore_point=create_restore_point
                        )
                        
                        if success:
                            st.success("System restored successfully!")
                            # Update system data
                            update_system_data()
                        else:
                            st.error("Failed to restore system")
                except Exception as e:
                    st.error(f"Error restoring system: {str(e)}")
            else:
                st.warning("CRONOS system not initialized")

def update_system_data():
    """Update system data by loading states and backups."""
    if st.session_state.cronos_initialized:
        try:
            # Get data from core
            cronos_core = st.session_state.eva_system.cronos.cronos_core
            
            # Update system states
            st.session_state.system_states = cronos_core.get_system_states()
            
            # Update backups
            st.session_state.backups = cronos_core.get_backups()
            
            # Update evolution metrics
            st.session_state.evolution_metrics = cronos_core.get_evolution_metrics()
            
        except Exception as e:
            st.error(f"Error updating system data: {str(e)}")

def create_evolution_timeline():
    """Create a visualization of the system's evolution timeline."""
    if not st.session_state.system_states:
        st.info("No system states recorded")
        return
    
    # Create dataframe with system states
    df = pd.DataFrame(st.session_state.system_states)
    
    # Create figure
    fig = px.timeline(
        df,
        x_start="created_at",
        x_end="updated_at",
        y="state_type",
        color="health_score",
        hover_name="name",
        title="Evolution Timeline"
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="State Type",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_evolution_metrics():
    """Display system evolution metrics."""
    if not st.session_state.evolution_metrics:
        st.info("No evolution metrics available")
        return
    
    metrics = st.session_state.evolution_metrics
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Evolution Rate",
            f"{metrics.get('evolution_rate', 0):.2f}",
            f"{metrics.get('evolution_rate_delta', 0):.2f}%"
        )
    
    with col2:
        st.metric(
            "System Health",
            f"{metrics.get('system_health', 0):.2f}",
            f"{metrics.get('health_delta', 0):.2f}%"
        )
    
    with col3:
        st.metric(
            "Integrity",
            f"{metrics.get('integrity_score', 0):.2f}",
            f"{metrics.get('integrity_delta', 0):.2f}%"
        )
    
    with col4:
        st.metric(
            "Temporal Consciousness",
            f"{metrics.get('temporal_consciousness', 0):.2f}",
            f"{metrics.get('consciousness_delta', 0):.2f}%"
        )
    
    # Temporal evolution chart
    if metrics.get('historical_data'):
        historical_df = pd.DataFrame(metrics['historical_data'])
        
        fig = go.Figure()
        
        # Add lines for different metrics
        for column in ['evolution_rate', 'system_health', 'integrity_score']:
            if column in historical_df.columns:
                fig.add_trace(go.Scatter(
                    x=historical_df['timestamp'],
                    y=historical_df[column],
                    name=column.replace('_', ' ').title(),
                    mode='lines+markers'
                ))
        
        fig.update_layout(
            title="System Temporal Evolution",
            xaxis_title="Date",
            yaxis_title="Value",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_backup_table():
    """Display a table with system backups."""
    if len(st.session_state.backups) == 0:
        st.info("No backups recorded")
        return
    
    # Create dataframe
    backups_df = pd.DataFrame(st.session_state.backups)
    
    if not backups_df.empty:
        # Select and rename columns for display
        display_columns = {
            "name": "Name",
            "type": "Type",
            "created_at": "Creation Date",
            "size": "Size",
            "status": "Status"
        }
        
        filtered_df = backups_df[display_columns.keys()].rename(columns=display_columns)
        st.dataframe(filtered_df, use_container_width=True)

def main():
    """Main function of the application."""
    # Initialize session variables
    initialize_session()
    
    # Title and description
    st.title("⌛ CRONOS - Evolutionary Preservation")
    st.markdown("""
    The CRONOS module is responsible for the evolutionary preservation of the EVA & GUARANI system,
    managing backups, system states, and temporal evolution metrics.
    """)
    
    # Initialize the system
    initialize_button = st.button("Initialize CRONOS")
    if initialize_button:
        initialize_system()
    
    # Check if the system is initialized
    if not st.session_state.cronos_initialized:
        st.warning("The CRONOS system needs to be initialized")
        # Demonstration image
        st.image("https://via.placeholder.com/800x400?text=CRONOS+Module")
    else:
        # Update system data
        update_button = st.button("Update Data")
        if update_button:
            update_system_data()
        
        # Create tabs to organize content
        tab1, tab2, tab3 = st.tabs(["Evolution", "Backups", "States"])
        
        with tab1:
            # System evolution visualization
            display_evolution_metrics()
            create_evolution_timeline()
        
        with tab2:
            # Backup management
            col1, col2 = st.columns([2, 1])
            
            with col1:
                display_backup_table()
            
            with col2:
                create_backup_form()
                st.markdown("---")
                restore_backup_form()
        
        with tab3:
            # System states
            if st.session_state.system_states:
                for state in st.session_state.system_states:
                    with st.expander(f"State: {state['name']} ({state['created_at']})"):
                        st.json(state)
            else:
                st.info("No system states recorded")
    
    # Application footer
    display_footer()

if __name__ == "__main__":
    main()