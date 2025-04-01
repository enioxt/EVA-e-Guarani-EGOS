#!/usr/bin/env python3
python
"""
EVA & GUARANI System Modules
----------------------------
This package contains the main functional modules of the quantum system
EVA & GUARANI, including interfaces for external services and
specialized functionalities.
"""

# Import main modules
from .perplexity_integration import PerplexityIntegration
from .quantum_tools import QuantumTools

# Define the public interface
__all__ = ["PerplexityIntegration", "QuantumTools"]