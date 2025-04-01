"""
EVA & GUARANI - METADATA Subsystem
Filesystem Monitor Module
Version: 1.0
"""

import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Set, Optional, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent
from QUANTUM_PROMPTS.METADATA.core.metadata_manager import MetadataManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MetadataEventHandler(FileSystemEventHandler):
    """Event handler for file system changes that trigger metadata updates."""
    
    def __init__(self, metadata_manager: MetadataManager, callback: Optional[Callable] = None):
        """Initialize the event handler.
        
        Args:
            metadata_manager (MetadataManager): Instance of the metadata manager
            callback (Optional[Callable]): Optional callback for notifications
        """
        self.metadata_manager = metadata_manager
        self.callback = callback
        self.ignored_patterns = {
            '.git', 'node_modules', '__pycache__',
            'venv', 'temp', 'logs', 'Backups'
        }
        self.last_events: Dict[str, float] = {}
        self.debounce_seconds = 1.0
        
    def on_modified(self, event: FileModifiedEvent):
        """Handle file modification events.
        
        Args:
            event (FileModifiedEvent): The file modification event
        """
        if not event.is_directory and self._should_process_event(event):
            self._process_file_event(event.src_path, "modified")
            
    def on_created(self, event: FileCreatedEvent):
        """Handle file creation events.
        
        Args:
            event (FileCreatedEvent): The file creation event
        """
        if not event.is_directory and self._should_process_event(event):
            self._process_file_event(event.src_path, "created")
            
    def _should_process_event(self, event) -> bool:
        """Determine if an event should be processed.
        
        Args:
            event: The file system event
            
        Returns:
            bool: True if the event should be processed
        """
        # Check if path contains ignored patterns
        path = Path(event.src_path)
        for pattern in self.ignored_patterns:
            if pattern in path.parts:
                return False
                
        # Check file extension
        if path.suffix.lower() in {'.pyc', '.pyo', '.pyd', '.so'}:
            return False
            
        # Implement debouncing
        current_time = time.time()
        last_time = self.last_events.get(event.src_path, 0)
        
        if current_time - last_time < self.debounce_seconds:
            return False
            
        self.last_events[event.src_path] = current_time
        return True
        
    def _process_file_event(self, file_path: str, event_type: str):
        """Process a file event by updating its metadata.
        
        Args:
            file_path (str): Path to the file
            event_type (str): Type of event ("modified" or "created")
        """
        try:
            path = Path(file_path)
            logger.info(f"Processing {event_type} event for {path}")
            
            # Update metadata
            success = self.metadata_manager.process_file(path)
            
            if success:
                logger.info(f"Successfully updated metadata for {path}")
                if self.callback:
                    self.callback(path, event_type)
            else:
                logger.error(f"Failed to update metadata for {path}")
                
        except Exception as e:
            logger.error(f"Error processing {event_type} event for {file_path}: {str(e)}")

class FilesystemMonitor:
    """Monitor the filesystem for changes and manage metadata updates."""
    
    def __init__(self, root_dir: str, callback: Optional[Callable] = None):
        """Initialize the filesystem monitor.
        
        Args:
            root_dir (str): Root directory to monitor
            callback (Optional[Callable]): Optional callback for notifications
        """
        self.root_dir = Path(root_dir)
        self.metadata_manager = MetadataManager(root_dir)
        self.event_handler = MetadataEventHandler(self.metadata_manager, callback)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, str(self.root_dir), recursive=True)
        self._active_monitors: Set[str] = set()
        
    def start(self):
        """Start monitoring the filesystem."""
        try:
            logger.info(f"Starting filesystem monitor for {self.root_dir}")
            self.observer.start()
            self._active_monitors.add(str(self.root_dir))
        except Exception as e:
            logger.error(f"Error starting filesystem monitor: {str(e)}")
            
    def stop(self):
        """Stop monitoring the filesystem."""
        try:
            logger.info("Stopping filesystem monitor")
            self.observer.stop()
            self.observer.join()
            self._active_monitors.remove(str(self.root_dir))
        except Exception as e:
            logger.error(f"Error stopping filesystem monitor: {str(e)}")
            
    def add_directory(self, directory: str):
        """Add a new directory to monitor.
        
        Args:
            directory (str): Directory path to monitor
        """
        try:
            path = Path(directory)
            if not path.is_absolute():
                path = self.root_dir / path
                
            if str(path) not in self._active_monitors:
                self.observer.schedule(self.event_handler, str(path), recursive=True)
                self._active_monitors.add(str(path))
                logger.info(f"Added monitoring for directory: {path}")
        except Exception as e:
            logger.error(f"Error adding directory {directory}: {str(e)}")
            
    def remove_directory(self, directory: str):
        """Remove a directory from monitoring.
        
        Args:
            directory (str): Directory path to stop monitoring
        """
        try:
            path = Path(directory)
            if not path.is_absolute():
                path = self.root_dir / path
                
            if str(path) in self._active_monitors:
                # Find and remove the appropriate observer
                for watch in self.observer._watches.copy():
                    if str(path) in str(watch.path):
                        self.observer.unschedule(watch)
                        
                self._active_monitors.remove(str(path))
                logger.info(f"Removed monitoring for directory: {path}")
        except Exception as e:
            logger.error(f"Error removing directory {directory}: {str(e)}")
            
    def is_monitoring(self, directory: str) -> bool:
        """Check if a directory is being monitored.
        
        Args:
            directory (str): Directory path to check
            
        Returns:
            bool: True if the directory is being monitored
        """
        path = Path(directory)
        if not path.is_absolute():
            path = self.root_dir / path
        return str(path) in self._active_monitors
        
    def get_active_monitors(self) -> Set[str]:
        """Get the set of actively monitored directories.
        
        Returns:
            Set[str]: Set of monitored directory paths
        """
        return self._active_monitors.copy()
        
    def process_existing_files(self):
        """Process all existing files in monitored directories."""
        try:
            logger.info("Processing existing files...")
            for directory in self._active_monitors:
                path = Path(directory)
                for file_path in path.rglob('*'):
                    if file_path.is_file() and self.event_handler._should_process_event(
                        type('Event', (), {'src_path': str(file_path), 'is_directory': False})
                    ):
                        self.event_handler._process_file_event(str(file_path), "existing")
            logger.info("Finished processing existing files")
        except Exception as e:
            logger.error(f"Error processing existing files: {str(e)}")

def example_callback(file_path: Path, event_type: str):
    """Example callback function for file events.
    
    Args:
        file_path (Path): Path to the affected file
        event_type (str): Type of event
    """
    print(f"Callback: {event_type} event for {file_path}")

if __name__ == "__main__":
    # Example usage
    def main():
        monitor = FilesystemMonitor("/c/Eva Guarani EGOS", example_callback)
        try:
            monitor.start()
            monitor.process_existing_files()
            
            # Keep the monitor running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Stopping monitor due to keyboard interrupt")
                
        finally:
            monitor.stop()
            
    main() 