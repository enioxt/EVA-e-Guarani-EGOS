#!/usr/bin/env python3
python
"""
External Services Package - EVA & GUARANI
-----------------------------------------
This package contains modules for interaction with external services and APIs,
including configuration management and integration with AI providers.
"""

from .config import config_manager
from .perplexity_service import PerplexityService

__all__ = ["config_manager", "PerplexityService"]
