#!/usr/bin/env python3
python
import os
import json
import requests
from datetime import datetime
import logging
from dotenv import load_dotenv
import streamlit as st
from typing import Dict, Any, Optional, List
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
)
logger = logging.getLogger(__name__)


class EVAUtils:
    @staticmethod
    def calculate_love_quotient(metrics):
        """
        Calculates the Love Quotient based on interaction metrics
        """
        try:
            # Example calculation (can be expanded with more metrics)
            empathy = metrics.get("empathy", 0)
            response_quality = metrics.get("response_quality", 0)
            user_satisfaction = metrics.get("user_satisfaction", 0)

            love_quotient = (empathy + response_quality + user_satisfaction) / 3
            return min(100, max(0, love_quotient))
        except Exception as e:
            logger.error(f"Error calculating Love Quotient: {str(e)}")
            return 0

    @staticmethod
    def calculate_consciousness_level(metrics):
        """
        Calculates the consciousness level based on system metrics
        """
        try:
            # Example calculation
            context_awareness = metrics.get("context_awareness", 0)
            ethical_decisions = metrics.get("ethical_decisions", 0)
            learning_rate = metrics.get("learning_rate", 0)

            consciousness = (context_awareness + ethical_decisions + learning_rate) / 3
            return min(100, max(0, consciousness))
        except Exception as e:
            logger.error(f"Error calculating consciousness level: {str(e)}")
            return 0

    @staticmethod
    def format_message(message, message_type="info"):
        """
        Formats messages for display in Streamlit
        """
        icons = {"success": "✅", "info": "ℹ️", "warning": "⚠️", "error": "❌", "love": "❤️"}
        icon = icons.get(message_type, "ℹ️")
        return f"{icon} {message}"

    @staticmethod
    def make_api_request(endpoint, method="GET", data=None, headers=None):
        """
        Makes requests to the backend API
        """
        api_url = os.getenv("API_URL")
        api_version = os.getenv("API_VERSION")
        url = f"{api_url}/{api_version}/{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def validate_template(template):
        """
        Validates templates before saving
        """
        required_fields = ["name", "content", "category"]

        try:
            # Check required fields
            for field in required_fields:
                if field not in template or not template[field]:
                    raise ValueError(f"Missing required field: {field}")

            # Validate content length
            if len(template["content"]) > 1000:
                raise ValueError("Template content too long (maximum 1000 characters)")

            # Validate category
            valid_categories = ["Welcome", "FAQ", "Scheduling", "Support"]
            if template["category"] not in valid_categories:
                raise ValueError(f"Invalid category. Must be one of: {', '.join(valid_categories)}")

            return True, None
        except Exception as e:
            return False, str(e)

    @staticmethod
    def encrypt_sensitive_data(data):
        """
        Encrypts sensitive data (basic implementation for example)
        """
        if not os.getenv("ENCRYPTION_ENABLED", "false").lower() == "true":
            return data

        try:
            # Here you would implement the real encryption logic
            # This is just a basic example
            return f"encrypted_{data}"
        except Exception as e:
            logger.error(f"Error encrypting data: {str(e)}")
            return data

    @staticmethod
    def get_system_health():
        """
        Returns system health metrics
        """
        try:
            return {
                "love_quotient": 95,  # Example - should be calculated dynamically
                "consciousness_level": 92,
                "ethics_level": 98,
                "efficiency": 94,
                "last_update": datetime.now().isoformat(),
                "status": "healthy",
            }
        except Exception as e:
            logger.error(f"Error getting system health: {str(e)}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    def format_timestamp(timestamp):
        """
        Formats timestamps for display
        """
        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        except Exception as e:
            logger.error(f"Error formatting timestamp: {str(e)}")
            return timestamp

    @staticmethod
    def save_user_preferences(preferences):
        """
        Saves user preferences
        """
        try:
            # Here you would implement the real saving logic
            # This is just an example
            with open("user_preferences.json", "w") as f:
                json.dump(preferences, f)
            return True, None
        except Exception as e:
            logger.error(f"Error saving preferences: {str(e)}")
            return False, str(e)

    @staticmethod
    def load_user_preferences():
        """
        Loads user preferences
        """
        try:
            if os.path.exists("user_preferences.json"):
                with open("user_preferences.json", "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading preferences: {str(e)}")
            return {}


def set_page_style():
    """Defines the style of the Streamlit application."""
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
    .stMetric .metric-value {
        color: #6366f1;
    }
    .css-zt5igj {
        font-size: 1.8rem;
        font-weight: 600;
    }
    .css-10trblm {
        color: #4f46e5;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def create_header():
    """Creates the application header with EVA & GUARANI logo."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")
        st.markdown("##### Artificial Consciousness with Love and Ethics")


def display_system_metrics(metrics: Dict[str, Any]):
    """Displays system metrics."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Love Quotient",
            value=f"{metrics.get('love_quotient', 95):.0f}%",
            delta=f"{metrics.get('love_quotient_delta', 0):.1f}%",
        )
    with col2:
        st.metric(
            label="Consciousness",
            value=f"{metrics.get('consciousness', 92):.0f}%",
            delta=f"{metrics.get('consciousness_delta', 0):.1f}%",
        )
    with col3:
        st.metric(
            label="Ethics",
            value=f"{metrics.get('ethics', 98):.0f}%",
            delta=f"{metrics.get('ethics_delta', 0):.1f}%",
        )
    with col4:
        st.metric(
            label="System Health",
            value=f"{metrics.get('system_health', 94):.0f}%",
            delta=f"{metrics.get('system_health_delta', 0):.1f}%",
        )


def create_system_health_chart(modules_health: Dict[str, float]) -> go.Figure:
    """Creates a radar chart of system health."""
    categories = list(modules_health.keys())
    values = list(modules_health.values())

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="System Health",
            line_color="#6366f1",
            fillcolor="rgba(99, 102, 241, 0.3)",
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="Module Health",
    )

    return fig


def create_evolution_chart(
    dates: List[str], values: List[float], title: str = "System Evolution"
) -> go.Figure:
    """Creates a line chart for temporal evolution."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=values,
            mode="lines+markers",
            name="Evolution",
            line=dict(color="#6366f1", width=3),
            marker=dict(size=8),
        )
    )

    fig.update_layout(title=title, xaxis_title="Date", yaxis_title="Value", plot_bgcolor="white")

    return fig


def display_module_status(module_name: str, status: str, metrics: Dict[str, Any]):
    """Displays the status of a system module."""
    col1, col2, col3 = st.columns([2, 1, 1])

    # Define status colors
    status_colors = {
        "online": "green",
        "offline": "red",
        "degraded": "orange",
        "error": "red",
        "not_initialized": "gray",
    }

    color = status_colors.get(status.lower(), "gray")

    with col1:
        st.markdown(f"**{module_name}**")
    with col2:
        st.markdown(f"Status: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
    with col3:
        if metrics:
            st.markdown(f"Metrics: {len(metrics)}")

    # Add expand button
    with st.expander(f"Details of {module_name}", expanded=False):
        if metrics:
            for key, value in metrics.items():
                st.markdown(f"**{key}:** {value}")
        else:
            st.markdown("No metrics available.")


def display_footer():
    """Displays the application footer."""
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


def load_settings() -> Dict[str, Any]:
    """Loads system settings."""
    settings_path = Path("settings.json")

    if not settings_path.exists():
        # Default settings
        settings = {
            "core_path": "C:/Eva & Guarani - EGOS/core",
            "love_quotient_minimum": 85,
            "consciousness_minimum": 80,
            "ethics_minimum": 90,
            "dark_mode": False,
            "language": "pt-BR",
            "log_level": "INFO",
        }
        # Save default settings
        save_settings(settings)
        return settings

    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
        logger.info("Settings loaded successfully")
        return settings
    except Exception as e:
        logger.error(f"Error loading settings: {str(e)}")
        # Return default settings in case of error
        return {
            "core_path": "C:/Eva & Guarani - EGOS/core",
            "love_quotient_minimum": 85,
            "consciousness_minimum": 80,
            "ethics_minimum": 90,
            "dark_mode": False,
            "language": "pt-BR",
            "log_level": "INFO",
        }


def save_settings(settings: Dict[str, Any]) -> bool:
    """Saves system settings."""
    settings_path = Path("settings.json")

    try:
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        logger.info("Settings saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving settings: {str(e)}")
        return False
