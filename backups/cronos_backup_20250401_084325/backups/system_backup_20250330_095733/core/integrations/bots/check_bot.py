#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Bot Health Check
================================

Unified tool to check the status and health of the EVA & GUARANI Telegram bot.
This tool combines functionality from multiple diagnostic scripts.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0.0
"""

import os
import sys
import json
import subprocess
import importlib
import logging
import datetime
import platform
import requests
import argparse
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("bot_health")

# Set up paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "tools/utilities"))


# ASCII art banner
def print_banner():
    banner = """
✧༺❀༻∞ EVA & GUARANI - Bot Health Check ∞༺❀༻✧
    """
    print(banner)
    print("=" * 60)


def check_os():
    """Check the operating system"""
    system = platform.system()
    release = platform.release()
    version = platform.version()

    print(f"🖥️ System Information:")
    print(f"  • Operating System: {system}")
    print(f"  • Release: {release}")
    print(f"  • Version: {version}")
    print(f"  • Python Version: {platform.python_version()}")

    return system


def check_dependencies():
    """Check if required dependencies are installed"""
    dependencies = {"python-telegram-bot": "13.15", "requests": None, "openai": None}

    all_good = True
    print("\n📦 Checking Dependencies...")

    for package, version in dependencies.items():
        try:
            imported = importlib.import_module(package.replace("-", "_"))
            if hasattr(imported, "__version__"):
                current_version = imported.__version__
                print(f"  ✅ {package}: Installed (version {current_version})")

                if version and current_version != version:
                    print(f"     ⚠️ Warning: Expected version {version}, found {current_version}")
            else:
                print(f"  ✅ {package}: Installed (version unknown)")
        except ImportError:
            print(f"  ❌ {package}: Not installed")
            all_good = False

    return all_good


def check_config():
    """Check if configuration files exist and are valid"""
    config_files = {
        "Telegram Config": os.path.join(current_dir, "telegram_config.json"),
        "Payment Config": os.path.join(project_root, "data/payment_config.json"),
    }

    all_good = True
    print("\n📄 Checking Configuration Files...")

    for name, path in config_files.items():
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    config = json.load(f)

                if name == "Telegram Config":
                    if "token" in config and config["token"]:
                        print(
                            f"  ✅ {name}: Valid (Token: {config['token'][:6]}...{config['token'][-4:]})"
                        )
                    else:
                        print(f"  ⚠️ {name}: Missing or invalid token")
                        all_good = False
                else:
                    print(f"  ✅ {name}: Valid")
            except json.JSONDecodeError:
                print(f"  ❌ {name}: Invalid JSON format")
                all_good = False
            except Exception as e:
                print(f"  ❌ {name}: Error reading file - {e}")
                all_good = False
        else:
            print(f"  ❌ {name}: File not found")
            all_good = False

    return all_good


def check_telegram_connection():
    """Check connection to Telegram API"""
    print("\n🌐 Checking Telegram API Connection...")

    config_path = os.path.join(current_dir, "telegram_config.json")
    if not os.path.exists(config_path):
        print("  ❌ No telegram_config.json found")
        return False

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        token = config.get("token", "")
        if not token:
            print("  ❌ No bot token found in configuration")
            return False

        # Test Telegram API
        api_url = f"https://api.telegram.org/bot{token}/getMe"

        try:
            response = requests.get(api_url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    bot_username = data.get("result", {}).get("username", "")
                    print(f"  ✅ Connected to Telegram API")
                    print(f"     • Bot: @{bot_username}")
                    return True
                else:
                    print(f"  ❌ Telegram API error: {data.get('description', 'Unknown error')}")
            else:
                print(f"  ❌ Telegram API HTTP error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("  ❌ Connection error. Check your internet connection.")
        except requests.exceptions.Timeout:
            print("  ❌ Connection timed out. Telegram API may be slow or unavailable.")
        except Exception as e:
            print(f"  ❌ Error connecting to Telegram API: {e}")

    except Exception as e:
        print(f"  ❌ Error reading configuration: {e}")

    return False


def check_logs():
    """Check bot logs"""
    print("\n📋 Checking Bot Logs...")

    logs_dir = os.path.join(current_dir, "logs")
    if not os.path.exists(logs_dir):
        print("  ⚠️ Logs directory not found")
        return

    log_files = [f for f in os.listdir(logs_dir) if f.endswith(".log")]

    if not log_files:
        print("  ⚠️ No log files found")
        return

    for log_file in log_files:
        log_path = os.path.join(logs_dir, log_file)
        file_size = os.path.getsize(log_path) / 1024  # KB
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(log_path))

        print(f"  • {log_file}")
        print(f"    - Size: {file_size:.2f} KB")
        print(f"    - Last Modified: {last_modified.strftime('%Y-%m-%d %H:%M:%S')}")

        # Check for errors in the log
        try:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                last_lines = f.readlines()[-50:]  # Read last 50 lines

                error_count = sum(1 for line in last_lines if "ERROR" in line)
                if error_count > 0:
                    print(f"    - ⚠️ Found {error_count} errors in recent logs")

                    # Show the last 3 errors
                    error_lines = [line for line in last_lines if "ERROR" in line][-3:]
                    for i, line in enumerate(error_lines):
                        print(f"      Error {i+1}: {line.strip()}")
                else:
                    print(f"    - ✅ No recent errors found")
        except Exception as e:
            print(f"    - ❌ Error reading log file: {e}")


def check_payment_system():
    """Check payment system"""
    print("\n💰 Checking Payment System...")

    # Check if payment_gateway.py exists
    payment_gateway_path = os.path.join(project_root, "tools/utilities/payment_gateway.py")
    if not os.path.exists(payment_gateway_path):
        print("  ❌ payment_gateway.py not found")
        return False

    # Check payment configuration
    payment_config_path = os.path.join(project_root, "data/payment_config.json")
    if not os.path.exists(payment_config_path):
        print("  ❌ payment_config.json not found")
        return False

    try:
        with open(payment_config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Check PIX configuration
        pix_config = config.get("pix", {})
        if pix_config.get("enabled", False):
            print(f"  ✅ PIX payment enabled")
            print(f"     • Key: {pix_config.get('key', 'Not configured')}")
        else:
            print(f"  ⚠️ PIX payment not enabled")

        # Check crypto configuration
        crypto_config = config.get("crypto", {})
        if crypto_config:
            print(f"  ✅ Crypto payment configured:")
            for crypto, details in crypto_config.items():
                if details.get("enabled", False):
                    print(f"     • {crypto.upper()}: {details.get('network', 'Unknown network')}")
        else:
            print(f"  ⚠️ Crypto payment not configured")

        # Check usage limits
        usage_limits = config.get("usage_limits", {})
        if usage_limits:
            print(f"  ✅ Usage limits configured:")
            for tier, limits in usage_limits.items():
                print(
                    f"     • {tier}: {limits.get('messages_per_day', 0)} msgs/day, {limits.get('special_calls_per_day', 0)} special calls/day"
                )
        else:
            print(f"  ⚠️ Usage limits not configured")

        return True
    except json.JSONDecodeError:
        print(f"  ❌ Invalid JSON format in payment_config.json")
    except Exception as e:
        print(f"  ❌ Error checking payment system: {e}")

    return False


def quick_check():
    """Performs a quick health check for startup"""
    all_checks_passed = True

    # Check for minimal required files
    required_files = [
        os.path.join(current_dir, "simple_telegram_bot.py"),
        os.path.join(current_dir, "telegram_config.json"),
    ]

    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Required file not found: {os.path.basename(file_path)}")
            all_checks_passed = False

    # Quick config check
    try:
        with open(os.path.join(current_dir, "telegram_config.json"), "r", encoding="utf-8") as f:
            config = json.load(f)

        if not config.get("token"):
            print("❌ Bot token not configured")
            all_checks_passed = False
    except Exception:
        print("❌ Error reading telegram_config.json")
        all_checks_passed = False

    # Check if Python-telegram-bot is installed
    try:
        import telegram

        if not hasattr(telegram, "__version__"):
            print("⚠️ python-telegram-bot is installed but version can't be detected")
    except ImportError:
        print("❌ python-telegram-bot not installed")
        all_checks_passed = False

    if all_checks_passed:
        print("✅ Quick health check passed")
    else:
        print("❌ Quick health check failed")

    return all_checks_passed


def main():
    """Main function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="EVA & GUARANI Bot Health Check")
    parser.add_argument("--quick", action="store_true", help="Perform a quick health check")
    args = parser.parse_args()

    # For quick check mode, only do minimal validation
    if args.quick:
        result = quick_check()
        sys.exit(0 if result else 1)

    print_banner()

    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Timestamp: {timestamp}")

    # Check system
    system = check_os()

    # Check dependencies
    dependencies_ok = check_dependencies()

    # Check configuration
    config_ok = check_config()

    # Check Telegram connection
    telegram_ok = check_telegram_connection()

    # Check logs
    check_logs()

    # Check payment system
    payment_ok = check_payment_system()

    # Print summary
    print("\n🧪 Health Check Summary:")
    print("=" * 60)
    print(f"  • Dependencies: {'✅ OK' if dependencies_ok else '❌ Issues Found'}")
    print(f"  • Configuration: {'✅ OK' if config_ok else '❌ Issues Found'}")
    print(f"  • Telegram API: {'✅ Connected' if telegram_ok else '❌ Connection Failed'}")
    print(f"  • Payment System: {'✅ Configured' if payment_ok else '❌ Issues Found'}")

    overall_status = dependencies_ok and config_ok and telegram_ok

    print("\n🏥 Overall Status:")
    if overall_status:
        print("✅ Bot is healthy and ready to run")
        print("\nTo start the bot, run: python simple_telegram_bot.py")
    else:
        print("❌ Issues found that may prevent the bot from running correctly")
        print("\nPlease fix the issues above before starting the bot")

    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

    # Return appropriate exit code
    return 0 if overall_status else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nBot health check interrupted.")
        sys.exit(130)  # Standard exit code for Ctrl+C
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        print(f"\n❌ Error during health check: {e}")
        sys.exit(1)
    print("\nFor more information, check the logs in the 'logs' directory.")
