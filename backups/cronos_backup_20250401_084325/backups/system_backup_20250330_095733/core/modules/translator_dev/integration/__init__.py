#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Integration package for EVA & GUARANI Translator.

This package provides integration with other systems such as BIOS-Q.
"""

from .bios_q_integration import BIOSQTranslatorIntegration

__all__ = ["BIOSQTranslatorIntegration"]
