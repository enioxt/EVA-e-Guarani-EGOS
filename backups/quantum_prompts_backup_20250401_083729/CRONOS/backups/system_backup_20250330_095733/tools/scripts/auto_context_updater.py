#!/usr/bin/env python3
import time
import schedule
from pathlib import Path
from dynamic_context_manager import DynamicContextManager
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("context_updater.log"), logging.StreamHandler()],
)


class AutoContextUpdater:
    def __init__(self):
        self.manager = DynamicContextManager()
        self.last_update = None
        self.update_interval = 300  # 5 minutes

    def update_context(self):
        try:
            current_time = datetime.now()
            logging.info(f"Starting context update at {current_time}")

            # Update the context
            self.manager.update_context()
            self.last_update = current_time

            logging.info("Context update completed successfully")

        except Exception as e:
            logging.error(f"Error updating context: {e}")

    def run(self):
        logging.info("Starting Auto Context Updater")

        # Schedule updates every 5 minutes
        schedule.every(5).minutes.do(self.update_context)

        # Initial update
        self.update_context()

        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                logging.info("Auto Context Updater stopped by user")
                break
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                time.sleep(60)  # Wait a minute before retrying


if __name__ == "__main__":
    updater = AutoContextUpdater()
    updater.run()
