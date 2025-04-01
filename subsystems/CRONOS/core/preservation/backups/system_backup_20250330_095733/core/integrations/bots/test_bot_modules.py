#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Test Bot Modules
================================

This script tests if all required modules for the EVA & GUARANI Telegram bot
are properly installed and can be imported.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0.0
"""

import os
import sys
import importlib
from pathlib import Path

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "modules/quantum"))
sys.path.append(os.path.join(project_root, "tools/utilities"))

def test_module_import(module_name, package_name=None):
    """Test if a module can be imported."""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name}: Successfully imported")
        return True
    except ImportError as e:
        install_cmd = f"pip install {package_name or module_name}"
        print(f"❌ {module_name}: Import failed ({e})")
        print(f"   To install: {install_cmd}")
        return False

def main():
    """Main function to test all required modules."""
    print("✧༺❀༻∞ EVA & GUARANI - Testing Bot Modules ∞༺❀༻✧\n")
    
    # Core Python libraries
    print("Testing core Python libraries:")
    test_module_import("json")
    test_module_import("asyncio")
    test_module_import("datetime")
    test_module_import("pathlib")
    print()
    
    # Telegram Bot API
    print("Testing Telegram Bot API:")
    telegram_ok = test_module_import("telegram", "python-telegram-bot==13.15")
    if telegram_ok:
        try:
            from telegram import Update, ParseMode
            from telegram.ext import Updater, CommandHandler
            print("   All required Telegram classes are available")
        except ImportError as e:
            print(f"   ⚠️ Some Telegram classes couldn't be imported: {e}")
    print()
    
    # Quantum Knowledge system
    print("Testing Quantum Knowledge system:")
    hub_ok = test_module_import("quantum_knowledge_hub")
    integrator_ok = test_module_import("quantum_knowledge_integrator")
    
    if not (hub_ok and integrator_ok):
        print("   ⚠️ Quantum Knowledge system is not fully available")
        print("   The bot will fall back to OpenAI if needed")
    print()
    
    # Payment system
    print("Testing Payment system:")
    payment_ok = test_module_import("payment_gateway")
    if not payment_ok:
        print("   ⚠️ Payment Gateway is not available")
        print("   The bot will run without payment features")
    print()
    
    # OpenAI (fallback)
    print("Testing OpenAI (fallback):")
    openai_ok = test_module_import("openai")
    if not openai_ok:
        print("   ⚠️ OpenAI is not available for fallback")
    print()
    
    # Additional libraries
    print("Testing additional libraries:")
    test_module_import("numpy")
    test_module_import("requests")
    print()
    
    # Configuration files
    print("Testing configuration files:")
    telegram_config = os.path.join(current_dir, "telegram_config.json")
    if os.path.exists(telegram_config):
        print(f"✅ Telegram config: Found at {telegram_config}")
    else:
        print(f"❌ Telegram config: Not found at {telegram_config}")
        
    payment_config = os.path.join(project_root, "data", "payment_config.json")
    if os.path.exists(payment_config):
        print(f"✅ Payment config: Found at {payment_config}")
    else:
        print(f"❌ Payment config: Not found at {payment_config}")
    print()
    
    # Summary
    all_critical = telegram_ok and (hub_ok or openai_ok)
    
    print("Summary:")
    if all_critical:
        print("✅ Critical modules are available. The bot should work correctly.")
        print("   You can now run: start_eva_guarani_bot.bat")
    else:
        print("❌ Some critical modules are missing. The bot may not work correctly.")
        print("   Please install the missing modules before running the bot.")
    
    if not (hub_ok and integrator_ok) and not openai_ok:
        print("⚠️ Both Quantum Knowledge and OpenAI are unavailable.")
        print("   The bot won't be able to process messages properly.")
    print()
    
    print("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

if __name__ == "__main__":
    main() 