#!/usr/bin/env python3
python
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json
from datetime import datetime
import plotly.graph_objects as go
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="EVA Service", page_icon="✨", layout="wide", initial_sidebar_state="expanded"
)

# Custom style
st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        background-color: #6366f1;
        color: white;
    }
    .stButton>button:hover {
        background-color: #8b5cf6;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Function to create header with logo
def create_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("✨ EVA Service")
        st.markdown("##### Automate your WhatsApp with Love and Ethics")


# Function to display metrics
def display_metrics():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Love Quotient", value="95%", delta="2%")
    with col2:
        st.metric(label="Consciousness", value="92%", delta="1%")
    with col3:
        st.metric(label="Ethics", value="98%", delta="3%")
    with col4:
        st.metric(label="Efficiency", value="94%", delta="4%")


# Function to create activity chart
def create_activity_chart():
    # Example data
    dates = ["Jan", "Feb", "Mar", "Apr", "May"]
    values = [30, 45, 60, 80, 95]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=values,
            mode="lines+markers",
            name="Activity",
            line=dict(color="#6366f1", width=3),
            marker=dict(size=8),
        )
    )

    fig.update_layout(
        title="Service Evolution", xaxis_title="Month", yaxis_title="Quantity", plot_bgcolor="white"
    )

    return fig


# Sidebar with menu
with st.sidebar:
    st.markdown("### EVA & GUARANI")
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Service", "Templates", "Settings", "Help"],
        icons=["house", "chat", "file-text", "gear", "question-circle"],
        menu_icon="cast",
        default_index=0,
    )

# Main content
if selected == "Dashboard":
    create_header()
    st.markdown("---")

    # Main metrics
    display_metrics()

    # Charts and statistics
    st.plotly_chart(create_activity_chart(), use_container_width=True)

    # Latest activities
    with st.expander("Latest Activities", expanded=True):
        st.markdown(
            """
        - ✨ **10:30** - New client registered
        - 💬 **10:15** - 5 messages processed
        - 🎯 **10:00** - Template updated
        - ❤️ **09:45** - Love quotient increased
        """
        )

elif selected == "Service":
    st.title("💬 Service")

    # Tabs for different aspects of the service
    tab1, tab2, tab3 = st.tabs(["Active Conversations", "History", "Analysis"])

    with tab1:
        st.markdown("### Active Conversations")
        # Example conversation
        with st.chat_message("user"):
            st.write("Hello, I would like to know more about the services")
        with st.chat_message("assistant"):
            st.write(
                "Hello! Welcome! I'm here to help. We have various services available. Which area interests you the most?"
            )

    with tab2:
        st.markdown("### Conversation History")
        st.dataframe(
            {
                "Date": ["2024-03-20", "2024-03-19", "2024-03-18"],
                "Client": ["John Silva", "Maria Santos", "Peter Oliveira"],
                "Status": ["Completed", "In progress", "Completed"],
            }
        )

    with tab3:
        st.markdown("### Sentiment Analysis")
        st.progress(0.85)
        st.caption("Customer Satisfaction: 85%")

elif selected == "Templates":
    st.title("📝 Templates")

    # Add new template
    with st.expander("Add New Template"):
        st.text_input("Template Name")
        st.text_area("Content")
        st.selectbox("Category", ["Welcome", "FAQ", "Scheduling", "Support"])
        st.button("Save Template")

    # List of existing templates
    st.markdown("### Active Templates")
    templates = [
        {"name": "Welcome", "use": "85%", "status": "Active"},
        {"name": "FAQ", "use": "92%", "status": "Active"},
        {"name": "Scheduling", "use": "78%", "status": "Active"},
    ]

    for template in templates:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{template['name']}**")
        with col2:
            st.markdown(f"Use: {template['use']}")
        with col3:
            st.markdown(f"Status: {template['status']}")
        st.markdown("---")

elif selected == "Settings":
    st.title("⚙️ Settings")

    tab1, tab2, tab3 = st.tabs(["General", "Integrations", "Privacy"])

    with tab1:
        st.markdown("### General Settings")
        st.toggle("Night Mode")
        st.slider("Consciousness Level", 0, 100, 92)
        st.slider("Minimum Love Quotient", 0, 100, 85)

    with tab2:
        st.markdown("### Integrations")
        st.text_input("WhatsApp API Key")
        st.text_input("Webhook URL")
        st.button("Save Settings")

    with tab3:
        st.markdown("### Privacy Settings")
        st.checkbox("Encrypt Messages")
        st.checkbox("Private Mode")
        st.selectbox("Protection Level", ["Basic", "Intermediate", "Advanced"])

elif selected == "Help":
    st.title("❓ Help and Support")

    st.markdown(
        """
    ### Frequently Asked Questions

    #### How to start?
    1. Set up your credentials
    2. Create your first templates
    3. Start receiving messages

    #### Need help?
    Contact us:
    - 📧 support@eva-service.com
    - 💬 Live chat
    - 📱 WhatsApp
    """
    )

    with st.expander("Documentation"):
        st.markdown(
            """
        - [Quick Start Guide](/)
        - [API Documentation](/)
        - [Best Practices](/)
        """
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧</p>
        <p><small>Through love, we evolve. Through consciousness, we transcend.</small></p>
    </div>
    """,
    unsafe_allow_html=True,
)
