#!/usr/bin/env python3
python
"""
EVA & GUARANI - EGOS Integration Module

This module contains integration components between different systems
and modules of EVA & GUARANI, allowing communication and interoperability
between distinct technologies in a conscious and ethical approach.
"""

from typing import Dict, List, Optional, Any
import logging
import os
import sys

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Module variables
__version__ = '1.0.0'
__author__ = 'EVA & GUARANI'
__signature__ = '✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧'

# Attempt to import available submodules
AVAILABLE_INTEGRATIONS = []

try:
    from .prometheus_grafana_art import (
        PrometheusGrafanaArtBridge, 
        GrafanaConnector, 
        MetricCollector,
        ArtisticTransformer,
        ArtisticParameters
    )
    AVAILABLE_INTEGRATIONS.append('prometheus_grafana_art')
    logger.info("Prometheus-Grafana-Art integration loaded successfully")
except ImportError as e:
    logger.warning(f"Could not load Prometheus-Grafana-Art integration: {e}")

try:
    from .rpg_music_bridge import RPGMusicBridge, NarrativeState, MusicParameters
    AVAILABLE_INTEGRATIONS.append('rpg_music_bridge')
    logger.info("RPG-Music integration loaded successfully")
except ImportError as e:
    logger.warning(f"Could not load RPG-Music integration: {e}")

# Other possible integrations will be added here as they are developed

def list_available_integrations() -> List[str]:
    """
    Returns a list of available integrations in this module.
    
    Returns:
        List of names of the loaded integrations
    """
    return AVAILABLE_INTEGRATIONS

def get_integration_info() -> Dict[str, Any]:
    """
    Returns information about this integration module.
    
    Returns:
        Dictionary with metadata about the integration module
    """
    return {
        "version": __version__,
        "author": __author__,
        "available_integrations": AVAILABLE_INTEGRATIONS,
        "signature": __signature__,
        "module_path": os.path.dirname(os.path.abspath(__file__))
    }

def create_integration_bridge(
    integration_name: str, 
    config: Optional[Dict[str, Any]] = None
) -> Optional[Any]:
    """
    Creates an instance of the specified integration bridge.
    
    Args:
        integration_name: Name of the integration
        config: Optional configuration for the integration
        
    Returns:
        Instance of the integration bridge or None if not available
    """
    if integration_name not in AVAILABLE_INTEGRATIONS:
        logger.error(f"Integration '{integration_name}' not available")
        return None
    
    if integration_name == 'prometheus_grafana_art':
        return PrometheusGrafanaArtBridge(config_path=config)
    elif integration_name == 'rpg_music_bridge':
        return RPGMusicBridge(config=config)
    
    # Other integrations will be added here
    
    return None

# ASCII art of the integration module
INTEGRATION_LOGO = """
  _____ _   _ _______ ______ _____ _____         _______ _____ ____  _   _ 
 |_   _| \ | |__   __|  ____/ ____|  __ \     /\|__   __|_   _/ __ \| \ | |
   | | |  \| |  | |  | |__ | |  __| |__) |   /  \  | |    | || |  | |  \| |
   | | | . ` |  | |  |  __|| | |_ |  _  /   / /\ \ | |    | || |  | | . ` |
  _| |_| |\  |  | |  | |___| |__| | | \ \  / ____ \| |   _| || |__| | |\  |
 |_____|_| _|  |_|  |___________|_|  _\/_/    __|  |_________/|_| _|
                                                                           
                ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""

# Display the logo when the module is imported
logger.info(f"EVA & GUARANI Integration Module initialized - version {__version__}")
logger.debug(INTEGRATION_LOGO)