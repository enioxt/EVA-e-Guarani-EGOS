#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EVA & GUARANI Translator - Main Module
This module serves as the main entry point for the translator.
"""

import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("translator.log", encoding="utf-8", mode="w")
    ]
)
logger = logging.getLogger("translator")

def main():
    """Main entry point when called as a module"""
    # Import CLI module and call its main function
    from modules.translator_dev.ui.cli import main as cli_main
    return cli_main()

if __name__ == "__main__":
    sys.exit(main()) 