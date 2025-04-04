#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of using the Prometheus-Grafana-Art integration module.

This script demonstrates how to use the module to transform technical
metrics into artistic expressions through visualizations in Grafana.

Author: EVA & GUARANI
Version: 1.0.0
Signature: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""

import os
import sys
import time
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional

# Adds the root directory to the path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            os.path.join(os.path.dirname(__file__), "prometheus_grafana_art_example.log")
        ),
    ],
)
logger = logging.getLogger("prometheus_grafana_example")

# Import the integration module
try:
    # Direct import of modules
    from EGOS.modules.integration.prometheus_grafana_art import (
        PrometheusGrafanaArtBridge,
        ArtisticParameters,
        MetricCollector,
        ArtisticTransformer,
        GrafanaConnector,
    )
except ImportError as e:
    logger.error(f"Error importing modules: {e}")
    logger.error("Ensure that the EGOS module is available in your PYTHONPATH")
    sys.exit(1)


# Function to load configuration
def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Loads configuration from file or uses default values."""
    default_config_path = os.path.join(
        os.path.dirname(__file__), "..", "config", "integration", "prometheus_grafana_config.json"
    )

    config_file = config_path or default_config_path

    # Default configuration
    default_config = {
        "prometheus": {"url": "http://localhost:9090", "metrics_collection_interval": 60},
        "grafana": {
            "url": "http://localhost:3000",
            "api_key": "",
            "dashboard_folder": "EVA_GUARANI_Demo",
        },
    }

    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
                logger.info(f"Configuration loaded from {config_file}")
                return config
    except Exception as e:
        logger.warning(f"Error loading configuration: {e}")

    logger.info("Using default configuration")
    return default_config


# List available integrations
def list_available_integrations() -> list:
    """Returns a list of available integrations."""
    return ["prometheus_grafana_art", "rpg_music_bridge"]


# Create an instance of the bridge
def create_integration_bridge(
    integration_name: str, config: Optional[Dict[str, Any]] = None
) -> Any:
    """Creates an instance of the integration bridge."""
    if integration_name == "prometheus_grafana_art":
        return PrometheusGrafanaArtBridge(config_path=config)
    else:
        logger.error(f"Integration '{integration_name}' not available")
        return None


# Simple demonstration
def run_basic_demo(bridge: PrometheusGrafanaArtBridge, output_dir: str) -> None:
    """Runs a basic demonstration of the module."""
    logger.info("Starting basic demonstration")

    # Test connections
    connections_ok = bridge.test_connections()
    if not connections_ok:
        logger.warning("One or more connections failed, but continuing with the demonstration")

    # Generate a unique dashboard
    dashboard_url = bridge.generate_artistic_dashboard(
        dashboard_title=f"EVA & GUARANI - Demo {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    if dashboard_url:
        logger.info(f"Dashboard created at: {dashboard_url}")
    else:
        logger.warning("Could not create the dashboard in Grafana")

    # Generate an image (simulated)
    image_path = os.path.join(output_dir, "artistic_representation.txt")
    bridge.generate_image_from_metrics(image_path)

    # Generate music (simulated)
    music_path = os.path.join(output_dir, "musical_composition.txt")
    bridge.generate_music_from_metrics(music_path)

    logger.info("Basic demonstration completed")


# Advanced demonstration with customized parameters
def run_advanced_demo(bridge: PrometheusGrafanaArtBridge, output_dir: str) -> None:
    """Runs a more advanced demonstration with customization."""
    logger.info("Starting advanced demonstration")

    # Collect metrics
    metrics, default_params = bridge.collect_and_transform()

    # Create custom artistic parameters
    custom_params = ArtisticParameters(
        color_scheme=["#8A2BE2", "#4B0082", "#9400D3"],  # Purple color scheme
        opacity=0.85,
        stroke_width=2.5,
        shape_complexity=0.75,
        movement_speed=0.6,
        base_note=392.0,  # Note G4
        tempo=90.0,
        volume=0.8,
        harmony_complexity=0.7,
        note_duration=0.3,
        consciousness_level=0.97,
        ethical_alignment=0.98,
        love_expression=0.99,
    )

    # Generate dashboard with custom parameters
    dashboard_title = f"EVA & GUARANI - Customized Demo {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    dashboard_url = bridge.generate_artistic_dashboard(
        dashboard_title=dashboard_title, metrics=metrics, artistic_params=custom_params
    )

    if dashboard_url:
        logger.info(f"Customized dashboard created at: {dashboard_url}")

    # Generate image with custom parameters
    image_path = os.path.join(output_dir, "custom_artistic_representation.txt")
    bridge.generate_image_from_metrics(
        output_path=image_path, metrics=metrics, artistic_params=custom_params
    )

    # Generate music with custom parameters
    music_path = os.path.join(output_dir, "custom_musical_composition.txt")
    bridge.generate_music_from_metrics(
        output_path=music_path, metrics=metrics, artistic_params=custom_params, duration_seconds=90
    )

    logger.info("Advanced demonstration completed")


# Short period monitoring demonstration
def run_monitoring_demo(bridge: PrometheusGrafanaArtBridge) -> None:
    """Runs a limited time monitoring loop."""
    logger.info("Starting monitoring demonstration")

    # Run a loop with only 3 iterations, updating every 30 seconds
    try:
        # Inform the user about the demo duration
        logger.info("Monitoring will run for 3 iterations (90 seconds)")
        logger.info("Press Ctrl+C at any time to stop")

        # Start the monitoring loop
        bridge.start_monitoring_loop(
            interval_seconds=30,  # Update every 30 seconds
            dashboard_title_prefix="EVA & GUARANI - Monitor",
            max_iterations=3,  # Limit to 3 iterations
        )
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")

    logger.info("Monitoring demonstration completed")


# Main function
def main() -> None:
    """Main function of the example."""
    # ASCII art
    print(
        """
    ██████╗ ██████╗  ██████╗ ███╗   ███╗███████╗████████╗██╗  ██╗███████╗██╗   ██╗███████╗
    ██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔════╝██║   ██║██╔════╝
    ██████╔╝██████╔╝██║   ██║██╔████╔██║█████╗     ██║   ███████║█████╗  ██║   ██║███████╗
    ██╔═══╝ ██╔══██╗██║   ██║██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██╔══╝  ██║   ██║╚════██║
    ██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗   ██║   ██║  ██║███████╗╚██████╔╝███████║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝

     ██████╗ ██████╗  █████╗ ███████╗ █████╗ ███╗   ██╗ █████╗      █████╗ ██████╗ ████████╗
    ██╔════╝ ██╔══██╗██╔══██╗██╔════╝██╔══██╗████╗  ██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝
    ██║  ███╗██████╔╝███████║█████╗  ███████║██╔██╗ ██║███████║    ███████║██████╔╝   ██║
    ██║   ██║██╔══██╗██╔══██║██╔══╝  ██╔══██║██║╚██╗██║██╔══██║    ██╔══██║██╔══██╗   ██║
    ╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║██║ ╚████║██║  ██║    ██║  ██║██║  ██║   ██║
     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝

                        ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
    """
    )

    # Check available integrations
    logger.info(f"Available integrations: {list_available_integrations()}")

    # Load configuration
    config = load_config()

    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Create the integration bridge
    bridge = create_integration_bridge("prometheus_grafana_art", config)

    if not bridge:
        logger.error("Could not create the integration bridge")
        sys.exit(1)

    # Run demonstrations
    run_basic_demo(bridge, output_dir)
    print("\n" + "-" * 80 + "\n")

    run_advanced_demo(bridge, output_dir)
    print("\n" + "-" * 80 + "\n")

    run_monitoring_demo(bridge)

    # Conclusion
    logger.info("Example completed successfully")
    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")


if __name__ == "__main__":
    main()
