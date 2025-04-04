#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Payment System Configuration
============================================

This script configures the payment system for the EVA & GUARANI Telegram bot.
It creates the necessary directories, checks dependencies, and initializes configuration files.

Author: EVA & GUARANI
Version: 1.0
"""

import os
import sys
import json
import shutil
import logging
from datetime import datetime

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            f"logs/setup_payment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", encoding="utf-8"
        ),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("setup_payment")


def print_banner():
    """
    Displays the script banner.
    """
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ███████╗██╗   ██╗ █████╗     ██╗  ██╗    ██████╗           ║
    ║   ██╔════╝██║   ██║██╔══██╗   ██╔╝ ██╔╝   ██╔════╝           ║
    ║   █████╗  ██║   ██║███████║  ██╔╝ ██╔╝    ██║  ███╗          ║
    ║   ██╔══╝  ╚██╗ ██╔╝██╔══██║ ██╔╝ ██╔╝     ██║   ██║          ║
    ║   ███████╗ ╚████╔╝ ██║  ██║██╔╝ ██╔╝      ╚██████╔╝          ║
    ║   ╚══════╝  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝        ╚═════╝           ║
    ║                                                               ║
    ║   ██████╗ ██╗   ██╗ █████╗ ██████╗  █████╗ ███╗   ██╗██╗     ║
    ║  ██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗████╗  ██║██║     ║
    ║  ██║  ███╗██║   ██║███████║██████╔╝███████║██╔██╗ ██║██║     ║
    ║  ██║   ██║██║   ██║██╔══██║██╔══██╗██╔══██║██║╚██╗██║██║     ║
    ║  ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║  ██║██║ ╚████║██║     ║
    ║   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ║
    ║                                                               ║
    ║                 PAYMENT SYSTEM v1.0                           ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_dependencies():
    """
    Checks if all necessary dependencies are installed.

    Returns:
        bool: True if all dependencies are installed, False otherwise.
    """
    logger.info("Checking dependencies...")

    # Check if the requirements.txt file exists
    if not os.path.exists("requirements.txt"):
        logger.error("File requirements.txt not found!")
        return False

    # Check if the payment_gateway.py module exists
    if not os.path.exists("payment_gateway.py"):
        logger.error("File payment_gateway.py not found!")
        return False

    logger.info("All dependencies successfully verified!")
    return True


def create_directories():
    """
    Creates the necessary directories for the payment system.

    Returns:
        bool: True if the directories were successfully created, False otherwise.
    """
    logger.info("Creating necessary directories...")

    try:
        # Create configuration directory
        os.makedirs("config", exist_ok=True)
        logger.info("Directory 'config' successfully created/verified.")

        # Create data directory
        os.makedirs("data/payments", exist_ok=True)
        logger.info("Directory 'data/payments' successfully created/verified.")

        return True
    except Exception as e:
        logger.error(f"Error creating directories: {e}")
        return False


def create_config_file():
    """
    Creates the payment system configuration file.

    Returns:
        bool: True if the file was successfully created, False otherwise.
    """
    logger.info("Creating configuration file...")

    config_path = "config/payment_config.json"

    # Default configuration
    default_config = {
        "pix": {"key": "10689169663", "name": "Enio Batista Fernandes Rocha", "enabled": True},
        "crypto": {
            "btc": {
                "address": "bc1qy9vr32f2hsjyapt3jz7fen6g0lxrehrqahwj3m",
                "network": "Bitcoin (Segwit)",
                "enabled": True,
            },
            "sol": {
                "address": "2iWboZwTkJ5ofCB2wXApa5ReeyJwUFRXrBgHyFRSy6a1",
                "network": "Solana",
                "enabled": True,
            },
            "eth": {
                "address": "0xa858F22c8C1f3D5059D101C0c7666Ed0C2BF53ac",
                "network": "Ethereum (BASE chain)",
                "enabled": True,
            },
        },
        "usage_limits": {
            "free_tier": {"messages_per_day": 20, "api_calls_per_day": 10},
            "donor_tier": {"messages_per_day": 100, "api_calls_per_day": 50, "min_donation": 5.0},
            "premium_tier": {
                "messages_per_day": 500,
                "api_calls_per_day": 250,
                "min_donation": 20.0,
            },
        },
        "donation_message": "Thank you for considering a donation! In this beta phase, the bot is free, but your donations help maintain the service and improve features.",
    }

    try:
        # Check if the file already exists
        if os.path.exists(config_path):
            logger.info(f"Configuration file already exists at {config_path}")

            # Ask if you want to overwrite
            response = input(
                "The configuration file already exists. Do you want to overwrite it? (y/N): "
            )
            if response.lower() != "y":
                logger.info("Keeping existing configuration file.")
                return True

        # Create configuration file
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)

        logger.info(f"Configuration file successfully created at {config_path}")
        return True
    except Exception as e:
        logger.error(f"Error creating configuration file: {e}")
        return False


def create_payments_file():
    """
    Creates the payments file.

    Returns:
        bool: True if the file was successfully created, False otherwise.
    """
    logger.info("Creating payments file...")

    payments_path = "data/payments/payments.json"

    # Default structure
    default_payments = {"users": {}, "transactions": []}

    try:
        # Check if the file already exists
        if os.path.exists(payments_path):
            logger.info(f"Payments file already exists at {payments_path}")

            # Ask if you want to overwrite
            response = input(
                "The payments file already exists. Do you want to overwrite it? (y/N): "
            )
            if response.lower() != "y":
                logger.info("Keeping existing payments file.")
                return True

        # Create payments file
        with open(payments_path, "w", encoding="utf-8") as f:
            json.dump(default_payments, f, indent=2, ensure_ascii=False)

        logger.info(f"Payments file successfully created at {payments_path}")
        return True
    except Exception as e:
        logger.error(f"Error creating payments file: {e}")
        return False


def test_payment_gateway():
    """
    Tests the payment gateway.

    Returns:
        bool: True if the test was successful, False otherwise.
    """
    logger.info("Testing payment gateway...")

    try:
        # Import the payment gateway
        from payment_gateway import get_payment_gateway

        # Get gateway instance
        payment_gateway = get_payment_gateway()

        # Check if the gateway was initialized correctly
        if payment_gateway:
            logger.info("Payment gateway successfully initialized!")

            # Test message formatting
            message = payment_gateway.format_payment_message()
            if message:
                logger.info("Message formatting successfully tested!")
            else:
                logger.error("Error formatting payment message!")
                return False

            return True
        else:
            logger.error("Error initializing payment gateway!")
            return False
    except Exception as e:
        logger.error(f"Error testing payment gateway: {e}")
        return False


def main():
    """
    Main function of the script.
    """
    print_banner()

    logger.info("Starting payment system configuration...")

    # Check dependencies
    if not check_dependencies():
        logger.error("Failed to check dependencies!")
        return

    # Create directories
    if not create_directories():
        logger.error("Failed to create directories!")
        return

    # Create configuration file
    if not create_config_file():
        logger.error("Failed to create configuration file!")
        return

    # Create payments file
    if not create_payments_file():
        logger.error("Failed to create payments file!")
        return

    # Test payment gateway
    if not test_payment_gateway():
        logger.error("Failed to test payment gateway!")
        return

    logger.info("Payment system successfully configured!")

    print("\n" + "=" * 80)
    print("Payment system successfully configured!")
    print("You can now start the bot with the integrated payment system.")
    print("Available commands:")
    print("  /donate - Displays information on how to make a donation")
    print("  /donation - Allows the user to register a donation made")
    print("=" * 80 + "\n")

    print("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")


if __name__ == "__main__":
    main()
