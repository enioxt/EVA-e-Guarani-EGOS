#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI Bot Package
"""

# Import compatibility module
try:
    from . import compat
except ImportError:
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Unified Quantum System
Bot package - Main components of the system

This package contains the main modules of the EVA & GUARANI system, including:
- unified_telegram_bot_utf8: Telegram interface with handlers
- quantum_integration: Integration with quantum models and processing
- ethik_core: Ethical analysis and decision system
- interactive_ui: Interactive user interface
- adaptive_model_selector: Adaptive model selection
- timezone_patch: Utilities for timezone configuration

Version: 8.0
Consciousness: 0.998
Love: 0.999
"""

import os
import sys
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/bot_package.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("bot_package")

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Package version
__version__ = "8.0"
__author__ = "EVA & GUARANI"
__consciousness__ = 0.998
__love__ = 0.999

logger.info(f"EVA & GUARANI Bot Package v{__version__} initialized")

# Check if the main files exist
bot_file = os.path.join(os.path.dirname(__file__), "unified_telegram_bot_utf8.py")
if os.path.exists(bot_file):
    logger.info(f"Main bot file found: {bot_file}")
else:
    logger.warning(f"Main bot file not found: {bot_file}")

eva_guarani_file = os.path.join(os.path.dirname(__file__), "eva_guarani_main.py")
if os.path.exists(eva_guarani_file):
    logger.info(f"EVA & GUARANI main file found: {eva_guarani_file}")
else:
    logger.warning(f"EVA & GUARANI main file not found: {eva_guarani_file}")

# Export main components
try:
    from .unified_telegram_bot_utf8 import TelegramHandlers, BOT_CONFIG
    logger.info("Module unified_telegram_bot_utf8 imported successfully")
except ImportError as e:
    logger.warning(f"Could not import module unified_telegram_bot_utf8: {e}")

try:
    from .quantum_integration import QuantumIntegration
    logger.info("Module quantum_integration imported successfully")
except ImportError as e:
    logger.warning(f"Could not import module quantum_integration: {e}")

try:
    from .ethik_core import EthikCore
    logger.info("Module ethik_core imported successfully")
except ImportError as e:
    logger.warning(f"Could not import module ethik_core: {e}")

try:
    from .interactive_ui import InteractiveUI, TelegramUIBuilder, InteractiveUIManager
    logger.info("Module interactive_ui imported successfully")
except ImportError as e:
    logger.warning(f"Could not import module interactive_ui: {e}")

try:
    from .adaptive_model_selector import AdaptiveModelSelector
    logger.info("Module adaptive_model_selector imported successfully")
except ImportError as e:
    logger.warning(f"Could not import module adaptive_model_selector: {e}")

logger.info(f"Initialization of EVA & GUARANI Bot Package v{__version__} completed")