#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Engines module for EVA & GUARANI Translator.

This package contains translation engines for different providers.
Currently supported engines are HuggingFace and OpenAI.
"""

# Import engines when available
try:
    from .huggingface import HuggingFaceTranslator
except ImportError:
    pass

try:
    from .openai import OpenAITranslator
except ImportError:
    pass

"""
EVA & GUARANI Translator - Engines Package
Contains translation engines including HuggingFace and OpenAI implementations.
""" 