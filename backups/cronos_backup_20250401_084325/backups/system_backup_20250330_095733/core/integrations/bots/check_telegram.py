#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Check Telegram
=============

Simple script to verify the python-telegram-bot installation
"""

import sys
import os

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")

try:
    import telegram

    print(f"telegram module version: {telegram.__version__}")
    print(f"telegram module path: {telegram.__file__}")
    print(f"telegram module package: {telegram.__package__}")
except ImportError as e:
    print(f"Error importing telegram: {e}")

try:
    from telegram.ext import Updater

    print("Successfully imported telegram.ext.Updater")
except ImportError as e:
    print(f"Error importing telegram.ext.Updater: {e}")

print("\nPython path:")
for path in sys.path:
    print(f"  {path}")

print("\nDone.")
