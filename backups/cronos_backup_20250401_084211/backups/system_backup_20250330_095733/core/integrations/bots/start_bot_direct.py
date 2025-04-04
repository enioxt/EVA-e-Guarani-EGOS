#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
UNIFIED TELEGRAM BOT - DIRECT INITIALIZATION
Version: 7.0.0
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""

import os
import sys
import json
import subprocess
import logging
import importlib.util
import locale
import time
import asyncio
import platform
import traceback

# Set encoding to UTF-8 (resolves display issues on Windows)
os.environ["PYTHONIOENCODING"] = "utf-8"

# Try to set console encoding (Windows)
try:
    # Set console encoding on Windows
    if os.name == 'nt':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleCP(65001)
        kernel32.SetConsoleOutputCP(65001)
except Exception as e:
    pass  # Ignore errors if this fails

# Configure logging
def setup_logging():
    """Configures the logging system."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

# Display banner
def print_banner():
    """Displays the startup banner."""
    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")
    print("UNIFIED TELEGRAM BOT - DIRECT INITIALIZATION")
    print("Version: 7.0.0")
    print("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

# Check and install necessary dependencies
def check_dependencies():
    """Checks and installs necessary dependencies."""
    try:
        # List of required packages
        required_packages = [
            "python-telegram-bot>=20.3",
            "pytz",
            "openai",
            "pillow",
            "numpy",
            "tiktoken",
            "tenacity",
            "APScheduler>=3.6.3"
        ]

        # Check and install each package
        for package in required_packages:
            try:
                pkg_name = package.split('>=')[0].split('==')[0]
                importlib.import_module(pkg_name.replace('-', '_'))
                logging.info(f"✅ Package {package} is already installed")
            except ImportError:
                logging.info(f"Installing package {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                logging.info(f"✅ Package {package} installed successfully")

        # Configure timezone
        try:
            # Try to import pytz explicitly to ensure it's available
            import pytz
            # Create and verify a UTC timezone object
            utc = pytz.UTC
            # Set environment variable for timezone
            os.environ['TZ'] = 'UTC'
            # On Unix-like systems, apply the timezone setting
            if platform.system() != 'Windows' and hasattr(time, 'tzset'):
                time.tzset()

            # Create timezone configuration file
            setup_timezone_content = """
import os
import sys
import time
import platform
import importlib.util

# Check if pytz is installed
if importlib.util.find_spec("pytz") is None:
    print("Installing pytz...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytz"])

# Now import pytz
import pytz

# Configure timezone
os.environ['TZ'] = 'UTC'
if platform.system() != 'Windows' and hasattr(time, 'tzset'):
    time.tzset()

# Patch for APScheduler
def patch_apscheduler():
    from telegram.ext import JobQueue
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    import inspect

    # Store original reference of AsyncIOScheduler constructor
    original_asyncio_init = AsyncIOScheduler.__init__

    # Replace the constructor to always use UTC
    def patched_asyncio_init(self, *args, **kwargs):
        if 'timezone' not in kwargs:
            kwargs['timezone'] = pytz.UTC
        return original_asyncio_init(self, *args, **kwargs)

    # Apply the patch
    AsyncIOScheduler.__init__ = patched_asyncio_init

    # Patch for ApplicationBuilder
    from telegram.ext import ApplicationBuilder
    original_build = ApplicationBuilder.build

    def patched_build(self):
        app = original_build(self)
        # Ensure the job_queue scheduler uses UTC
        if hasattr(app, 'job_queue') and app.job_queue is not None:
            if hasattr(app.job_queue, '_scheduler'):
                app.job_queue._scheduler.timezone = pytz.UTC
        return app

    ApplicationBuilder.build = patched_build

    # Patch for the _create_scheduler method if it exists
    if hasattr(JobQueue, '_create_scheduler'):
        original_create_scheduler = JobQueue._create_scheduler

        def patched_create_scheduler(self):
            scheduler = original_create_scheduler(self)
            scheduler.timezone = pytz.UTC
            return scheduler

        JobQueue._create_scheduler = patched_create_scheduler

    print("APScheduler patched successfully to use UTC timezone")

# Execute the patch
patch_apscheduler()
"""

            with open("setup_timezone.py", "w") as f:
                f.write(setup_timezone_content)

            logging.info("✅ Timezone successfully configured to UTC")
        except Exception as e:
            logging.error(f"❌ Error configuring timezone: {str(e)}")
            raise

        return True
    except Exception as e:
        logging.error(f"❌ Failed to check dependencies. Aborting initialization.")
        return False

# Check configuration files
def check_config_files():
    """Checks if configuration files exist."""
    config_files = [
        "config/bot_config.json",
        "config/telegram_config.json",
        "config/openai_config.json"
    ]

    for config_file in config_files:
        if not os.path.exists(config_file):
            logging.error(f"❌ Configuration file not found: {config_file}")
            return False

    # Check tokens in the Telegram configuration file
    try:
        with open("config/telegram_config.json", "r", encoding="utf-8") as f:
            telegram_config = json.load(f)

        if not telegram_config.get("bot_token"):
            logging.error("❌ Bot token not found in the Telegram configuration file")
            return False

        logging.info("✅ Configuration files successfully verified")
        logging.info(f"🔑 Telegram Token: {telegram_config.get('bot_token')[:5]}...")

        return True
    except Exception as e:
        logging.error(f"❌ Error verifying tokens: {str(e)}")
        return False

# Check bot scripts
def find_bot_script():
    """Finds the main bot script."""
    bot_scripts = [
        "unified_telegram_bot_utf8.py",
        "unified_telegram_bot.py",
        "bot.py"
    ]

    for script in bot_scripts:
        if os.path.exists(script):
            logging.info(f"✅ Bot script found: {script}")
            return script

    logging.error("❌ No bot script found")
    return None

# Create the patch for APScheduler
def create_apscheduler_patch():
    """Creates a patch file to fix the APScheduler timezone issue"""
    try:
        # Create patch directory if it doesn't exist
        patch_dir = os.path.join(os.getcwd(), "bot", "patches")
        os.makedirs(patch_dir, exist_ok=True)

        # Path of the patch file
        patch_file = os.path.join(patch_dir, "timezone_patch.py")

        with open(patch_file, 'w', encoding='utf-8') as f:
            f.write("""#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Patch to fix timezone issues in APScheduler
\"\"\"

import os
import sys
import pytz
import time
from importlib import import_module

# Ensure pytz is in the Python path
pytz_spec = sys.modules.get('pytz')
if not pytz_spec:
    raise ImportError("The pytz module is not installed or not imported correctly")

# Set global timezone
os.environ['TZ'] = 'UTC'
if hasattr(time, 'tzset'):
    time.tzset()

# Create UTC timezone object explicitly for verification
utc = pytz.timezone('UTC')
print(f"✅ UTC timezone configured correctly: {utc}")

# Monkey patch for AsyncIOScheduler from APScheduler
try:
    # Try to import APScheduler dynamically
    apscheduler_module = import_module('apscheduler.schedulers.asyncio')
    AsyncIOScheduler = apscheduler_module.AsyncIOScheduler

    # Store original constructor
    original_init = AsyncIOScheduler.__init__

    # Define new constructor with pytz timezone
    def patched_init(self, *args, **kwargs):
        # Ensure the timezone is from pytz
        if 'timezone' not in kwargs:
            kwargs['timezone'] = pytz.UTC
        return original_init(self, *args, **kwargs)

    # Apply the patch
    AsyncIOScheduler.__init__ = patched_init
    print("✅ Patch applied to AsyncIOScheduler successfully")

except (ImportError, AttributeError) as e:
    print(f"❌ Error applying patch to APScheduler: {e}")
    # Continue even with error - the patch will just be a backup

# Patch for JobQueue from python-telegram-bot
try:
    # Try to import JobQueue dynamically
    ptr_module = import_module('telegram.ext._jobqueue')
    JobQueue = ptr_module.JobQueue

    # Store original constructor
    original_jobqueue_init = JobQueue.__init__

    # Define new constructor with pytz timezone
    def patched_jobqueue_init(self, *args, **kwargs):
        # Force the use of pytz timezone in JobQueue
        self._tzinfo = pytz.UTC
        return original_jobqueue_init(self, *args, **kwargs)

    # Apply the patch
    JobQueue.__init__ = patched_jobqueue_init
    print("✅ Patch applied to JobQueue successfully")

except (ImportError, AttributeError) as e:
    print(f"❌ Error applying patch to JobQueue: {e}")
    # Continue even with error
""")

        logging.info(f"✅ Patch file created at {patch_file}")
        return patch_file
    except Exception as e:
        logging.error(f"❌ Error creating patch file: {e}")
        return None

# Check and apply timezone patch
def patch_telegram_bot():
    try:
        # Create patch for APScheduler
        patch_file = create_apscheduler_patch()
        if not patch_file:
            return False

        # Try to import pytz explicitly before applying the patch
        try:
            import pytz
            # Verify if we can create a timezone object
            utc = pytz.timezone('UTC')
            logging.info(f"✅ Pytz imported correctly: {utc}")
        except ImportError:
            logging.error("❌ Pytz module not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pytz"])
            import pytz

        # Add patch directory to Python path
        patch_dir = os.path.dirname(patch_file)
        if patch_dir not in sys.path:
            sys.path.insert(0, patch_dir)

        # Execute the patch as a separate process to ensure it loads correctly
        logging.info("Applying timezone patch...")
        result = subprocess.run(
            [sys.executable, patch_file],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        if result.returncode == 0:
            logging.info(f"✅ Timezone patch executed successfully: {result.stdout.strip()}")

            # Additionally, try direct patch in APScheduler util.            try:
                # Find the APScheduler library
                import apscheduler
                apscheduler_path = os.path.dirname(apscheduler.__file__)
                util_path = os.path.join(apscheduler_path, 'util.py')

                if os.path.exists(util_path):
                    logging.info(f"Applying direct patch to file {util_path}")

                    # Backup
                    import shutil
                    backup_path = util_path + '.bak'
                    shutil.copy2(util_path, backup_path)

                    # Read current content
                    with open(util_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Replace the problematic function
                    if 'def astimezone(obj):' in content:
                        modified_content = content.replace(
                            'def astimezone(obj):',
                            '''def astimezone(obj):
    """
    Patched by EVA & GUARANI to ensure compatibility with timezone objects.
    """
    import pytz
    # If it's None, return None
    if obj is None:
        return None

    # If it's already a pytz timezone, return it
    if hasattr(obj, 'localize') and callable(obj.localize):
        return obj

    # If it's a string, convert to pytz timezone
    if isinstance(obj, str):
        return pytz.timezone(obj)

    # For other timezone objects, try to convert to pytz
    if hasattr(obj, 'tzname') and callable(obj.tzname):
        try:
            return pytz.timezone(obj.tzname(None))
        except:
            return pytz.UTC

    # Default fallback'''
                        )

                        # Write modified file
                        with open(util_path, 'w', encoding='utf-8') as f:
                            f.write(modified_content)

                        logging.info(f"✅ Patch applied directly to APScheduler's util.py file")
                    else:
                        logging.warning("⚠️ Could not find target function for patch in util.py file")
            except Exception as e:
                logging.warning(f"⚠️ Could not apply direct patch: {e}")

            return True
        else:
            logging.error(f"❌ Error executing timezone patch: {result.stderr.strip()}")
            return False

    except Exception as e:
        logging.error(f"❌ Error applying timezone patch: {e}")
        return False

# Function to send a notification message when the bot starts
async def send_startup_notification(bot_token):
    try:
        # Try to load settings to get admin chat_id
        admin_chat_id = None
        try:
            import json
            config_files = [
                "config/bot_config.json",
                "config/telegram_config.json",
                "config/admin_config.json"
            ]

            for config_file in config_files:
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)

                        # Try to find admin chat_id in different fields
                        for field in ['admin_chat_id', 'owner_id', 'admin_id', 'developer_chat_id']:
                            if field in config and config[field]:
                                admin_chat_id = config[field]
                                print(f"✅ Admin chat ID found: {admin_chat_id}")
                                break

                        if admin_chat_id:
                            break
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Error loading configuration for notification: {e}")

        # If chat_id was not found in any configuration, use a default value
        if not admin_chat_id:
            print("⚠️ Admin ID not found in configurations. To receive notifications, add 'admin_chat_id' to the config/bot_config.json file")

            # Create log message to be displayed on the console
            print("✅ BOT STARTED SUCCESSFULLY! However, notification could not be sent due to missing admin ID.")
            print("ℹ️ To add your ID as an admin:")
            print("   1. Start a conversation with the bot on Telegram")
            print("   2. Use the /start or /id command to get your ID")
            print("   3. Add your ID as 'admin_chat_id' in the config/bot_config.json file")
            return

        # Import the telegram library
        from telegram import Bot

        # Create bot instance
        bot = Bot(token=bot_token)

        # Message format with timestamp
        import datetime
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Simplified message without special characters
        startup_message = f"EVA & GUARANI - Bot successfully started! Date/Time: {current_time}"

        # Send message
        await bot.send_message(chat_id=admin_chat_id, text=startup_message)
        print(f"✅ Notification message sent to admin (ID: {admin_chat_id})")

    except Exception as e:
        print(f"⚠️ Error sending startup notification: {e}")
        print("✅ Bot started, but notification could not be sent.")
        return

# Run the bot with correct settings
def run_bot(bot_script):
    """Runs the bot as a child process."""
    if not bot_script:
        logging.error("❌ No bot script specified")
        return

    try:
        logging.info(f"🚀 Starting bot: {bot_script}")

        # Run the bot as a Python process
        subprocess.Popen([sys.executable, bot_script])

        logging.info("✅ Bot started successfully")
    except Exception as e:
        logging.error(f"❌ Error starting the bot: {str(e)}")

def setup_bot():
    """Configures and initializes the bot."""
    try:
        # Import the timezone configuration module
        try:
            # Ensure the setup_timezone module is imported correctly
            spec = importlib.util.spec_from_file_location("setup_timezone", "setup_timezone.py")
            if spec is not None:
                setup_timezone = importlib.util.module_from_spec(spec)
                if spec.loader is not None:
                    spec.loader.exec_module(setup_timezone)
                    logging.info("✅ Timezone module loaded successfully")
                else:
                    logging.error("❌ Error loading timezone module: spec.loader is None")
            else:
                logging.error("❌ Error loading timezone module: spec is None")
        except Exception as e:
            logging.error(f"❌ Error loading timezone module: {str(e)}")
            # Try to import pytz directly as a fallback
            try:
                import pytz
                os.environ['TZ'] = 'UTC'
                if platform.system() != 'Windows' and hasattr(time, 'tzset'):
                    time.tzset()
                logging.info("✅ Timezone configured directly as fallback")
            except Exception as fallback_error:
                logging.error(f"❌ Error in timezone fallback: {str(fallback_error)}")

        # Check and install dependencies
        if not check_dependencies
