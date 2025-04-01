import os
import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import asdict
from .scanner import MetadataScanner
from .tracker import UsageTracker
from .organizer import FileOrganizer

class DataCollector:
    def __init__(self, scanner: MetadataScanner, tracker: UsageTracker, organizer: FileOrganizer):
        self.scanner = scanner
        self.tracker = tracker
        self.organizer = organizer
        self.db_path = 'metadata.db'
        self.setup_logging()
        self.setup_database()
        self.performance_metrics: Dict[str, Any] = {
            'collection_start_time': None,
            'last_collection': None,
            'total_files_processed': 0,
            'total_events_recorded': 0,
            'average_processing_time': 0.0
        }
        
    def setup_logging(self) -> None:
        """Setup logging configuration."""
        logging.basicConfig(
            filename='metadata_collector.log',
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
    def setup_database(self) -> None:
        """Initialize SQLite database for efficient data storage."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create tables for different types of data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE,
                    metadata_json TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT,
                    event_type TEXT,
                    event_data TEXT,
                    timestamp TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT,
                    metric_value REAL,
                    timestamp TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def start_collection(self) -> None:
        """Start continuous data collection process."""
        self.performance_metrics['collection_start_time'] = datetime.now()
        logging.info("Starting data collection process")
        
        try:
            # Collect initial metadata
            self._collect_metadata()
            
            # Start tracking file events
            self._start_event_tracking()
            
            # Schedule periodic data validation
            self._schedule_validation()
            
        except Exception as e:
            logging.error(f"Error in data collection: {str(e)}")
            raise
    
    def _collect_metadata(self) -> None:
        """Collect and store file metadata."""
        start_time = datetime.now()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for filepath, metadata in self.scanner.metadata_db.items():
                    # Convert metadata to JSON
                    metadata_json = json.dumps(asdict(metadata))
                    
                    # Update or insert metadata
                    cursor.execute('''
                        INSERT OR REPLACE INTO file_metadata 
                        (path, metadata_json, created_at, updated_at)
                        VALUES (?, ?, COALESCE(
                            (SELECT created_at FROM file_metadata WHERE path = ?),
                            CURRENT_TIMESTAMP
                        ), CURRENT_TIMESTAMP)
                    ''', (filepath, metadata_json, filepath))
                    
                    self.performance_metrics['total_files_processed'] += 1
                
                conn.commit()
            
            # Update performance metrics
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            self._update_performance_metrics('metadata_collection', processing_time)
            
            logging.info(f"Collected metadata for {self.performance_metrics['total_files_processed']} files")
            
        except Exception as e:
            logging.error(f"Error collecting metadata: {str(e)}")
            raise
    
    def _start_event_tracking(self) -> None:
        """Start tracking file events."""
        def event_callback(event_type: str, file_path: str, event_data: Dict[str, Any]) -> None:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Store event data
                    cursor.execute('''
                        INSERT INTO file_events 
                        (file_path, event_type, event_data, timestamp)
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                    ''', (file_path, event_type, json.dumps(event_data)))
                    
                    conn.commit()
                    
                self.performance_metrics['total_events_recorded'] += 1
                logging.info(f"Recorded {event_type} event for {file_path}")
                
            except Exception as e:
                logging.error(f"Error recording event: {str(e)}")
        
        # Register callback with tracker
        self.tracker.register_event_callback(event_callback)
    
    def _schedule_validation(self) -> None:
        """Schedule periodic data validation."""
        def validate_data() -> None:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Check for metadata consistency
                    cursor.execute('SELECT path, metadata_json FROM file_metadata')
                    for path, metadata_json in cursor.fetchall():
                        if not os.path.exists(path):
                            logging.warning(f"File not found: {path}")
                            continue
                            
                        metadata = json.loads(metadata_json)
                        current_metadata = asdict(self.scanner._extract_file_metadata(path))
                        
                        if metadata != current_metadata:
                            logging.info(f"Updating metadata for {path}")
                            self._collect_metadata()
                            break
                    
                    # Validate event data
                    cursor.execute('''
                        SELECT COUNT(*) FROM file_events 
                        WHERE timestamp < datetime('now', '-30 days')
                    ''')
                    old_events = cursor.fetchone()[0]
                    
                    if old_events > 0:
                        # Archive old events
                        self._archive_old_events()
                
                logging.info("Completed data validation")
                
            except Exception as e:
                logging.error(f"Error in data validation: {str(e)}")
        
        # Run validation every hour
        import schedule
        schedule.every(1).hour.do(validate_data)
    
    def _archive_old_events(self) -> None:
        """Archive old event data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Export old events to JSON
                cursor.execute('''
                    SELECT * FROM file_events 
                    WHERE timestamp < datetime('now', '-30 days')
                ''')
                old_events = cursor.fetchall()
                
                if old_events:
                    # Create archive directory if needed
                    archive_dir = 'archive/events'
                    os.makedirs(archive_dir, exist_ok=True)
                    
                    # Save to archive file
                    archive_file = os.path.join(
                        archive_dir,
                        f'events_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                    )
                    
                    with open(archive_file, 'w') as f:
                        json.dump(old_events, f, indent=2, default=str)
                    
                    # Delete archived events
                    cursor.execute('''
                        DELETE FROM file_events 
                        WHERE timestamp < datetime('now', '-30 days')
                    ''')
                    
                    conn.commit()
                    logging.info(f"Archived {len(old_events)} events to {archive_file}")
        
        except Exception as e:
            logging.error(f"Error archiving events: {str(e)}")
    
    def _update_performance_metrics(self, metric_name: str, value: float) -> None:
        """Update performance metrics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO performance_metrics 
                    (metric_name, metric_value, timestamp)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (metric_name, value))
                
                conn.commit()
            
            # Update running averages
            if metric_name == 'metadata_collection':
                total_time = sum(self.performance_metrics.get('processing_times', [value]))
                total_count = len(self.performance_metrics.get('processing_times', [1]))
                self.performance_metrics['average_processing_time'] = total_time / total_count
                
            self.performance_metrics['last_collection'] = datetime.now()
            
        except Exception as e:
            logging.error(f"Error updating performance metrics: {str(e)}")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the data collection process."""
        return {
            'start_time': self.performance_metrics['collection_start_time'],
            'last_collection': self.performance_metrics['last_collection'],
            'total_files': self.performance_metrics['total_files_processed'],
            'total_events': self.performance_metrics['total_events_recorded'],
            'avg_processing_time': self.performance_metrics['average_processing_time']
        }
    
    def export_data(self, start_date: Optional[datetime] = None, 
                   end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Export collected data for analysis."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build date filter
                date_filter = ''
                params = []
                if start_date and end_date:
                    date_filter = 'WHERE timestamp BETWEEN ? AND ?'
                    params = [start_date.isoformat(), end_date.isoformat()]
                
                # Get file metadata
                cursor.execute(f'SELECT * FROM file_metadata {date_filter}', params)
                metadata = cursor.fetchall()
                
                # Get events
                cursor.execute(f'SELECT * FROM file_events {date_filter}', params)
                events = cursor.fetchall()
                
                # Get performance metrics
                cursor.execute(f'SELECT * FROM performance_metrics {date_filter}', params)
                metrics = cursor.fetchall()
                
                return {
                    'metadata': metadata,
                    'events': events,
                    'performance_metrics': metrics,
                    'export_time': datetime.now().isoformat()
                }
                
        except Exception as e:
            logging.error(f"Error exporting data: {str(e)}")
            raise 