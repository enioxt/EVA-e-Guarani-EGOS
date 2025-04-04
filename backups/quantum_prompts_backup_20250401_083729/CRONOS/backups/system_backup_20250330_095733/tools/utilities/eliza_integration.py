#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Telegram Bot integration module with ElizaOS.
This module provides classes and functions to connect the Telegram bot with the ElizaOS platform.

Author: EVA & GUARANI
Version: 1.0
"""

import os
import sys
import json
import logging
import subprocess
import threading
import time
import queue
from typing import Dict, List, Any, Callable, Optional, Union

# Configure logger
logger = logging.getLogger("eliza_integration")


class ElizaIntegration:
    """
    Class responsible for integration with the ElizaOS system.
    Manages communication between the Telegram bot and ElizaOS.
    """

    def __init__(
        self,
        telegram_config_path: str = "config/telegram_config.json",
        eliza_config_path: str = "config/eliza_config.json",
    ):
        """
        Initializes the integration with ElizaOS.

        Args:
            telegram_config_path: Path to the Telegram configuration file
            eliza_config_path: Path to the ElizaOS configuration file
        """
        self.telegram_config_path = telegram_config_path
        self.eliza_config_path = eliza_config_path
        self.telegram_config = self._load_config(telegram_config_path)
        self.eliza_config = self._load_config(eliza_config_path)
        self.eliza_process = None
        self.is_running = False
        self.message_queue = queue.Queue()
        self.callbacks = []
        self.env_file_path = ".env"
        self._create_env_file()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Loads configurations from a JSON file.

        Args:
            config_path: Path to the configuration file

        Returns:
            Dictionary with the loaded configurations
        """
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                logger.warning(f"Configuration file not found: {config_path}")
                return {}
        except Exception as e:
            logger.error(f"Error loading configuration from {config_path}: {e}")
            return {}

    def _create_env_file(self) -> None:
        """
        Creates the .env file for ElizaOS with necessary variables.
        """
        try:
            eliza_dir = self.eliza_config.get("eliza_dir", "eliza")
            env_path = os.path.join(eliza_dir, self.env_file_path)

            # Variables to be set in the .env
            env_vars = {
                "ELIZA_API_KEY": self.eliza_config.get("api_key", ""),
                "OPENAI_API_KEY": self.eliza_config.get("openai_api_key", ""),
                "TELEGRAM_BOT_TOKEN": self.telegram_config.get("token", ""),
                "ELIZA_PORT": str(self.eliza_config.get("port", 3000)),
                "ELIZA_MODE": self.eliza_config.get("mode", "development"),
                "ELIZA_BRIDGE_ENABLED": "true",
            }

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(env_path), exist_ok=True)

            # Write .env file
            with open(env_path, "w", encoding="utf-8") as f:
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")

            logger.info(f".env file created at {env_path}")
        except Exception as e:
            logger.error(f"Error creating .env file: {e}")

    def is_eliza_installed(self) -> bool:
        """
        Checks if ElizaOS is installed correctly.

        Returns:
            True if ElizaOS is installed, False otherwise
        """
        eliza_dir = self.eliza_config.get("eliza_dir", "eliza")
        package_path = os.path.join(eliza_dir, "package.json")
        node_modules = os.path.join(eliza_dir, "node_modules")

        # Check existence of essential files/directories
        if not os.path.exists(eliza_dir):
            logger.error(f"ElizaOS directory not found: {eliza_dir}")
            return False

        if not os.path.exists(package_path):
            logger.error(f"package.json file not found: {package_path}")
            return False

        if not os.path.exists(node_modules):
            logger.warning(f"node_modules directory not found: {node_modules}")
            logger.info("ElizaOS dependencies may not be installed.")
            return False

        return True

    def start(self) -> bool:
        """
        Starts the ElizaOS process.

        Returns:
            True if the process was started successfully, False otherwise
        """
        if self.is_running:
            logger.warning("ElizaOS is already running")
            return True

        if not self.is_eliza_installed():
            logger.error("ElizaOS is not installed correctly")
            return False

        eliza_dir = self.eliza_config.get("eliza_dir", "eliza")

        try:
            # Command to start ElizaOS
            cmd = ["npm", "run", "dev"]

            # Start ElizaOS process
            logger.info("Starting ElizaOS...")
            self.eliza_process = subprocess.Popen(
                cmd,
                cwd=eliza_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                shell=True,
            )

            # Check if the process started correctly
            time.sleep(2)
            if self.eliza_process.poll() is not None:
                if self.eliza_process.stderr is not None:
                    stderr = self.eliza_process.stderr.read()
                    logger.error(f"Failed to start ElizaOS: {stderr}")
                else:
                    logger.error("Failed to start ElizaOS: unknown error")
                return False

            # Start thread to process output
            threading.Thread(target=self._process_output, daemon=True).start()

            # Start thread to process the message queue
            threading.Thread(target=self._process_message_queue, daemon=True).start()

            self.is_running = True
            logger.info("ElizaOS started successfully")
            return True
        except Exception as e:
            logger.error(f"Error starting ElizaOS: {e}")
            return False

    def stop(self) -> None:
        """
        Stops the ElizaOS process.
        """
        if not self.is_running or self.eliza_process is None:
            logger.warning("ElizaOS is not running")
            return

        try:
            # Terminate process
            logger.info("Stopping ElizaOS...")
            self.eliza_process.terminate()

            # Wait for the process to terminate
            self.eliza_process.wait(timeout=5)

            # Force termination if necessary
            if self.eliza_process.poll() is None:
                self.eliza_process.kill()

            self.is_running = False
            logger.info("ElizaOS stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping ElizaOS: {e}")

    def _process_output(self) -> None:
        """
        Processes the output of the ElizaOS process.
        """
        if self.eliza_process is None:
            return

        while self.is_running:
            try:
                # Read output
                if self.eliza_process.stdout is None:
                    logger.error("ElizaOS process stdout not available")
                    break

                line = self.eliza_process.stdout.readline()
                if not line:
                    if self.eliza_process.poll() is not None:
                        logger.warning("ElizaOS terminated unexpectedly")
                        self.is_running = False
                        break
                    continue

                # Process line
                line = line.strip()
                if line:
                    logger.debug(f"ElizaOS: {line}")

                    # Check if it is a JSON response
                    if line.startswith("{") and line.endswith("}"):
                        try:
                            data = json.loads(line)
                            self._notify_callbacks(data)
                        except json.JSONDecodeError:
                            pass
            except Exception as e:
                logger.error(f"Error processing ElizaOS output: {e}")

    def _process_message_queue(self) -> None:
        """
        Processes the message queue to be sent to ElizaOS.
        """
        while self.is_running:
            try:
                # Get message from queue
                message = self.message_queue.get(timeout=1)

                # Check if the process is running
                if self.eliza_process is None or not self.is_running:
                    logger.warning("ElizaOS is not running to process message")
                    continue

                # Check if stdin is available
                if self.eliza_process.stdin is None:
                    logger.error("ElizaOS process stdin not available")
                    continue

                # Convert message to JSON
                message_json = json.dumps(message)

                # Send message to ElizaOS
                self.eliza_process.stdin.write(message_json + "\n")
                self.eliza_process.stdin.flush()

                logger.debug(f"Message sent to ElizaOS: {message_json[:100]}...")
            except queue.Empty:
                # Queue timeout, continue the loop
                pass
            except Exception as e:
                logger.error(f"Error processing message queue: {e}")

    def send_message(self, message: Dict[str, Any]) -> None:
        """
        Sends a message to ElizaOS.

        Args:
            message: Dictionary with the message to be sent
        """
        try:
            self.message_queue.put(message)
        except Exception as e:
            logger.error(f"Error enqueuing message: {e}")

    def register_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Registers a callback function to receive responses from ElizaOS.

        Args:
            callback: Function that will be called when there is a response
        """
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def unregister_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Removes a callback function.

        Args:
            callback: Function to be removed
        """
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def _notify_callbacks(self, data: Dict[str, Any]) -> None:
        """
        Notifies all registered callbacks about a new response.

        Args:
            data: Data of the received response
        """
        for callback in self.callbacks:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Error in callback: {e}")


class ElizaBot:
    """
    Adapter to connect the Telegram bot with ElizaOS.
    """

    def __init__(self, integration: Optional[ElizaIntegration] = None):
        """
        Initializes the ElizaBot adapter.

        Args:
            integration: Instance of ElizaIntegration for communication with ElizaOS
        """
        self.integration = integration
        self.message_handlers = []
        self.update_handlers = []

    def register_message_handler(
        self, handler: Callable, content_types: Optional[List[str]] = None
    ) -> None:
        """
        Registers a handler for messages.

        Args:
            handler: Function that will process the messages
            content_types: List of content types to be processed
        """
        if content_types is None:
            content_types = ["text"]

        self.message_handlers.append({"handler": handler, "content_types": content_types})

    def register_update_handler(self, handler: Callable) -> None:
        """
        Registers a handler for updates from ElizaOS.

        Args:
            handler: Function that will process the updates
        """
        if self.integration:
            self.integration.register_callback(handler)
        self.update_handlers.append(handler)

    def process_update(self, update: Dict[str, Any]) -> None:
        """
        Processes an update from Telegram.

        Args:
            update: Data of the update
        """
        if not self.integration:
            logger.warning("Attempt to process update without integration with ElizaOS")
            return

        # Send update to ElizaOS
        self.integration.send_message(update)


# Auxiliary functions


def create_text_response(
    chat_id: int,
    text: str,
    reply_to_message_id: Optional[int] = None,
    parse_mode: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Creates a text response to send back to Telegram.

    Args:
        chat_id: Chat ID
        text: Message text
        reply_to_message_id: ID of the message to reply to
        parse_mode: Text formatting mode

    Returns:
        Dictionary with the response data
    """
    response = {"method": "sendMessage", "chat_id": chat_id, "text": text}

    if reply_to_message_id:
        response["reply_to_message_id"] = reply_to_message_id

    if parse_mode:
        response["parse_mode"] = parse_mode

    return response


def create_photo_response(
    chat_id: int,
    photo: str,
    caption: Optional[str] = None,
    reply_to_message_id: Optional[int] = None,
    parse_mode: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Creates a photo response to send back to Telegram.

    Args:
        chat_id: Chat ID
        photo: URL or path of the photo
        caption: Photo caption
        reply_to_message_id: ID of the message to reply to
        parse_mode: Text formatting mode

    Returns:
        Dictionary with the response data
    """
    response = {"method": "sendPhoto", "chat_id": chat_id, "photo": photo}

    if caption:
        response["caption"] = caption

    if reply_to_message_id:
        response["reply_to_message_id"] = reply_to_message_id

    if parse_mode:
        response["parse_mode"] = parse_mode

    return response


# Example of usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create instance of ElizaIntegration
    integration = ElizaIntegration()

    # Start ElizaOS
    if integration.start():
        print("ElizaOS started successfully")

        # Create instance of ElizaBot
        bot = ElizaBot(integration=integration)

        # Register handler for messages
        def message_handler(message):
            print(f"Message received: {message}")

        bot.register_message_handler(message_handler, content_types=["text"])

        # Example of processing update
        update = {
            "update_id": 123456789,
            "message": {
                "message_id": 1,
                "from": {"id": 123456789, "first_name": "User", "is_bot": False},
                "chat": {"id": 123456789, "type": "private"},
                "text": "Hello, ElizaOS!",
            },
        }

        bot.process_update(update)

        # Wait for processing
        time.sleep(10)

        # Stop ElizaOS
        integration.stop()
    else:
        print("Failed to start ElizaOS")
