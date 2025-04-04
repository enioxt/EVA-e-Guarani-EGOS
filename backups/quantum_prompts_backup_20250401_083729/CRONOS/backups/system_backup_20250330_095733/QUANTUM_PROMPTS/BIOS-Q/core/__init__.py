#!/usr/bin/env python3
"""
EVA & GUARANI - Core Package
---------------------------
Este é o pacote principal do BIOS-Q que contém
os módulos essenciais do sistema.

Version: 8.0
Created: 2025-03-26
"""

from .mycelium_network import MyceliumNetwork, MyceliumNode

__version__ = "8.0.0"
__all__ = ["MyceliumNetwork", "MyceliumNode"]
