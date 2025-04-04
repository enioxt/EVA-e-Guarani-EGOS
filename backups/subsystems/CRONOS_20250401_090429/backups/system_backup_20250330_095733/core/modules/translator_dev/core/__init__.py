#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core module for EVA & GUARANI Translator.

This package contains the core components of the translator system,
including the scanner, processor, cache, and term manager.
"""

from .scanner import Scanner, ScanResult
from .processor import TranslationProcessor
from .cache import TranslationCache

__all__ = ["Scanner", "ScanResult", "TranslationProcessor", "TranslationCache"]

"""
EVA & GUARANI Translator - Core Package
Contains core functionality for the translator, including scanning,
processing, caching, and cost monitoring.
"""
