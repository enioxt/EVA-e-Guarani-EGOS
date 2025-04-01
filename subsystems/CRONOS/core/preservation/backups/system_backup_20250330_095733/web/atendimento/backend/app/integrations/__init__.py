#!/usr/bin/env python3
"""
EVA & GUARANI EGOS - Módulo de Integrações

Este módulo contém as integrações do EVA Atendimento com serviços externos
como APIs de geração de imagens, vídeos e outros serviços.
"""

from .egos_connector import EGOSConnector
from .stable_diffusion import StableDiffusionAPI

__all__ = ['EGOSConnector', 'StableDiffusionAPI'] 