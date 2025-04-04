#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Bot Configuration Test
======================================

Utility script to test and configure the Telegram bot for EVA & GUARANI.
This script helps verify configuration, setup API keys, and test functionality.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0.0
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("bot_config_test")

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "modules/quantum"))
sys.path.append(os.path.join(project_root, "tools/utilities"))

# Create necessary directories
os.makedirs(os.path.join(current_dir, "logs"), exist_ok=True)
os.makedirs(os.path.join(project_root, "data/payments"), exist_ok=True)


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        # Make sure Python-telegram-bot is available
        try:
            import telegram

            logger.info(f"✅ python-telegram-bot found (version: {telegram.__version__})")
        except ImportError:
            # Check with specific import path
            try:
                # Try to check if it's installed but not in the path
                import subprocess

                result = subprocess.run(
                    ["pip", "show", "python-telegram-bot"], capture_output=True, text=True
                )
                if "Version:" in result.stdout:
                    logger.warning(
                        "⚠️ python-telegram-bot is installed but not importable. Check your Python path."
                    )
                    # Try to install it again to make sure it's in the correct path
                    logger.warning("Attempting to reinstall python-telegram-bot...")
                    subprocess.run(
                        ["pip", "install", "--force-reinstall", "python-telegram-bot==13.15"],
                        capture_output=True,
                    )
                    # Try importing again
                    try:
                        import telegram

                        logger.info(
                            f"✅ python-telegram-bot found after reinstall (version: {telegram.__version__})"
                        )
                    except ImportError:
                        logger.error("❌ python-telegram-bot still not importable after reinstall")
                        logger.error("Run: pip install python-telegram-bot==13.15")
                        return False
                else:
                    logger.error(
                        "❌ python-telegram-bot not found. Run: pip install python-telegram-bot==13.15"
                    )
                    return False
            except Exception as e:
                logger.error(f"❌ Error checking python-telegram-bot: {e}")
                logger.error("Run: pip install python-telegram-bot==13.15")
                return False

        # Check for requests module
        try:
            import requests

            logger.info(f"✅ requests found (version: {requests.__version__})")
        except ImportError:
            logger.error("❌ requests not found. Run: pip install requests")
            return False

        # Check for PaymentGateway
        try:
            # First add tools directory to path
            tools_path = os.path.join(project_root, "tools", "utilities")
            if tools_path not in sys.path:
                sys.path.append(tools_path)

            from payment_gateway import PaymentGateway

            logger.info("✅ PaymentGateway module found")
        except ImportError:
            logger.warning(
                "⚠️ PaymentGateway module not found. Payment features may not work correctly."
            )

        return True

    except Exception as e:
        logger.error(f"❌ Error checking dependencies: {e}")
        return False


def check_config_file(config_path):
    """Check if config file exists and is valid"""
    try:
        if not os.path.exists(config_path):
            logger.error(f"❌ Config file not found: {config_path}")
            return False

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        logger.info(f"✅ Config file found and loaded: {config_path}")

        # Check essential configuration
        essential_keys = ["token", "bot_name", "allowed_users", "admin_users"]
        missing_keys = [key for key in essential_keys if key not in config]

        if missing_keys:
            logger.error(f"❌ Missing essential configuration: {', '.join(missing_keys)}")
            return False

        # Check if token is valid
        if not config.get("token") or config.get("token") == "YOUR_TOKEN_HERE":
            logger.error("❌ Bot token is not configured")
            return False

        logger.info(f"✅ Bot token found")
        logger.info(f"✅ Bot name: {config.get('bot_name')}")
        logger.info(f"✅ Allowed users: {len(config.get('allowed_users', []))} users")
        logger.info(f"✅ Admin users: {len(config.get('admin_users', []))} users")

        return True
    except Exception as e:
        logger.error(f"❌ Error checking config file: {e}")
        return False


def check_payment_config(config_path):
    """Check if payment config file exists and is valid"""
    try:
        payment_config_path = config_path.get("payment", {}).get("config_path", "")
        if not payment_config_path:
            logger.warning("⚠️ Payment config path not specified")
            return False

        # Convert to absolute path if needed
        if not os.path.isabs(payment_config_path):
            payment_config_path = os.path.join(project_root, payment_config_path)

        if not os.path.exists(payment_config_path):
            logger.error(f"❌ Payment config file not found: {payment_config_path}")
            return False

        with open(payment_config_path, "r", encoding="utf-8") as f:
            payment_config = json.load(f)

        logger.info(f"✅ Payment config file found and loaded: {payment_config_path}")

        # Check essential configuration
        payment_keys = ["pix", "crypto", "usage_limits", "pricing"]
        missing_keys = [key for key in payment_keys if key not in payment_config]

        if missing_keys:
            logger.warning(f"⚠️ Missing payment configuration: {', '.join(missing_keys)}")

        return True
    except Exception as e:
        logger.error(f"❌ Error checking payment config file: {e}")
        return False


def check_image_apis(config):
    """Check if image APIs are configured"""
    try:
        if not config.get("media_generation", {}).get("enabled", False):
            logger.warning("⚠️ Media generation is disabled")
            return False

        image_apis = config.get("media_generation", {}).get("image_apis", {})
        if not image_apis:
            logger.warning("⚠️ No image APIs configured")
            return False

        working_apis = 0

        # Check Stable Diffusion API
        if "stable_diffusion" in image_apis:
            sd_api = image_apis["stable_diffusion"]
            if sd_api.get("key") and sd_api.get("key") != "YOUR_KEY_HERE":
                logger.info(f"✅ Stable Diffusion API key found")
                working_apis += 1
            else:
                logger.warning("⚠️ Stable Diffusion API key not configured")

        # Check Unsplash API
        if "unsplash" in image_apis:
            unsplash_api = image_apis["unsplash"]
            if unsplash_api.get("key") and unsplash_api.get("key") != "YOUR_KEY_HERE":
                logger.info(f"✅ Unsplash API key found")
                working_apis += 1
            else:
                logger.warning("⚠️ Unsplash API key not configured")

        # Check Pexels API
        if "pexels" in image_apis:
            pexels_api = image_apis["pexels"]
            if pexels_api.get("key") and pexels_api.get("key") != "YOUR_KEY_HERE":
                logger.info(f"✅ Pexels API key found")
                working_apis += 1
            else:
                logger.warning("⚠️ Pexels API key not configured")

        logger.info(f"ℹ️ {working_apis}/3 image APIs configured")
        return working_apis > 0
    except Exception as e:
        logger.error(f"❌ Error checking image APIs: {e}")
        return False


def test_bot_connection(token):
    """Test connection to Telegram bot API"""
    try:
        import telegram

        bot = telegram.Bot(token=token)
        bot_info = bot.get_me()
        logger.info(f"✅ Connected to Telegram bot: @{bot_info.username} (ID: {bot_info.id})")
        return True
    except Exception as e:
        logger.error(f"❌ Error connecting to Telegram bot: {e}")
        return False


def configure_bot():
    """Interactive configuration of the bot"""
    config_path = os.path.join(current_dir, "telegram_config.json")

    # Check if config exists
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        # Create default config
        config = {
            "token": "YOUR_TOKEN_HERE",
            "bot_name": "avatechartbot",
            "allowed_users": [],
            "admin_users": [],
            "webhook_enabled": False,
            "webhook_url": "",
            "enable_eliza": True,
            "debug_mode": False,
            "openai_api_key": "",
            "message_timeout": 300,
            "max_message_length": 4096,
            "startup_notification": True,
            "payment": {
                "enabled": True,
                "config_path": "../../data/payment_config.json",
                "freemium_enabled": True,
                "initial_credits": 10,
                "credits_per_payment": 10,
                "payment_amount": 2.0,
            },
            "knowledge": {
                "enabled": True,
                "hub_config_path": "../../modules/quantum/quantum_hub.json",
                "integrator_config_path": "../../modules/quantum/quantum_integrator.json",
            },
            "media_generation": {
                "enabled": True,
                "image_apis": {
                    "stable_diffusion": {
                        "url": "https://stablediffusionapi.com/api/v3/text2img",
                        "key": "YOUR_KEY_HERE",
                    },
                    "unsplash": {
                        "url": "https://api.unsplash.com/photos/random",
                        "key": "YOUR_KEY_HERE",
                    },
                    "pexels": {"url": "https://api.pexels.com/v1/search", "key": "YOUR_KEY_HERE"},
                },
                "video_apis": {
                    "synthesia": {
                        "enabled": False,
                        "url": "https://api.synthesia.io/v2/videos",
                        "key": "YOUR_KEY_HERE",
                    },
                    "d-id": {
                        "enabled": False,
                        "url": "https://api.d-id.com/talks",
                        "key": "YOUR_KEY_HERE",
                    },
                },
            },
        }

    print("\n===== EVA & GUARANI Bot Configuration =====\n")

    # Configure token
    token = input(f"Enter bot token [current: {config.get('token')}]: ").strip()
    if token:
        config["token"] = token

    # Configure allowed users
    allowed_users = input(
        f"Enter allowed user IDs (comma-separated) [current: {config.get('allowed_users')}]: "
    ).strip()
    if allowed_users:
        try:
            config["allowed_users"] = [
                int(uid.strip()) for uid in allowed_users.split(",") if uid.strip()
            ]
        except ValueError:
            logger.error("Invalid user IDs. Using existing values.")

    # Configure admin users
    admin_users = input(
        f"Enter admin user IDs (comma-separated) [current: {config.get('admin_users')}]: "
    ).strip()
    if admin_users:
        try:
            config["admin_users"] = [
                int(uid.strip()) for uid in admin_users.split(",") if uid.strip()
            ]
        except ValueError:
            logger.error("Invalid admin IDs. Using existing values.")

    # Configure OpenAI API key
    openai_key = input(f"Enter OpenAI API key [current: {config.get('openai_api_key')}]: ").strip()
    if openai_key:
        config["openai_api_key"] = openai_key

    # Configure image APIs
    configure_images = input("Configure image APIs? (y/n): ").strip().lower() == "y"
    if configure_images:
        # Stable Diffusion
        sd_key = input("Enter Stable Diffusion API key: ").strip()
        if sd_key:
            config["media_generation"]["image_apis"]["stable_diffusion"]["key"] = sd_key

        # Unsplash
        unsplash_key = input("Enter Unsplash API key: ").strip()
        if unsplash_key:
            config["media_generation"]["image_apis"]["unsplash"]["key"] = unsplash_key

        # Pexels
        pexels_key = input("Enter Pexels API key: ").strip()
        if pexels_key:
            config["media_generation"]["image_apis"]["pexels"]["key"] = pexels_key

    # Save configuration
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    logger.info(f"✅ Configuration saved to {config_path}")

    return config


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="EVA & GUARANI Bot Configuration Tool")
    parser.add_argument("--check", action="store_true", help="Check bot configuration")
    parser.add_argument("--configure", action="store_true", help="Configure bot interactively")
    parser.add_argument(
        "--test-connection", action="store_true", help="Test connection to Telegram"
    )
    args = parser.parse_args()

    print("\n✧༺❀༻∞ EVA & GUARANI - Bot Configuration Tool ∞༺❀༻✧\n")

    # Check dependencies
    if not check_dependencies():
        logger.error("Please install required dependencies and run again.")
        return

    config_path = os.path.join(current_dir, "telegram_config.json")

    # Configure bot if requested
    if args.configure:
        config = configure_bot()
    else:
        # Load existing config
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            logger.info("Run with --configure to create a new configuration.")
            return

    # Check configuration
    if args.check or not args.configure:
        if not check_config_file(config_path):
            logger.error("Bot configuration check failed.")
            return

        check_payment_config(config)
        check_image_apis(config)

    # Test connection
    if args.test_connection:
        if test_bot_connection(config["token"]):
            logger.info("Bot connection test successful.")
        else:
            logger.error("Bot connection test failed.")

    print("\n✧༺❀༻∞ Configuration complete ∞༺❀༻✧\n")


if __name__ == "__main__":
    main()
