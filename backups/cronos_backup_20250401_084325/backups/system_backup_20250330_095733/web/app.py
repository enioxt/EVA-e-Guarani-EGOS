from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import json
import os
import sys

# Add core to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.metadata.collector import DataCollector
from core.metadata.scanner import MetadataScanner
from core.metadata.tracker import UsageTracker
from core.metadata.organizer import FileOrganizer
from core.metadata.ml.analyzer import MetadataAnalyzer

app = Flask(__name__, 
    static_folder='static',
    template_folder='templates'
)
socketio = SocketIO(app)

# Initialize components
scanner = MetadataScanner()
tracker = UsageTracker(scanner)
organizer = FileOrganizer(scanner)
collector = DataCollector(scanner, tracker, organizer)
analyzer = MetadataAnalyzer(scanner, tracker, organizer)

@app.route('/')
def index():
    """Render main dashboard."""
    return render_template('index.html')

@app.route('/quantum')
def quantum_prompts():
    """Render quantum prompts interface."""
    return render_template('quantum.html')

@app.route('/core')
def core_interface():
    """Render core system interface."""
    return render_template('core.html')

# Existing API routes from metadata system
@app.route('/api/stats')
def get_stats():
    """Get current system statistics."""
    stats = collector.get_collection_stats()
    usage_stats = tracker.get_usage_stats()
    
    return jsonify({
        'collection': stats,
        'usage': usage_stats,
        'quantum_metrics': _calculate_quantum_metrics()
    })

@app.route('/api/files/active')
def get_active_files():
    """Get list of active files."""
    days = request.args.get('days', 30, type=int)
    return jsonify(tracker.get_active_files(days))

@app.route('/api/files/dependencies')
def get_dependencies():
    """Get dependency graph data."""
    return jsonify(_generate_dependency_graph())

@app.route('/api/subsystems/activity')
def get_subsystem_activity():
    """Get subsystem activity metrics."""
    days = request.args.get('days', 30, type=int)
    stats = tracker.get_usage_stats(days)
    
    return jsonify({
        'activity': stats['subsystem_activity'],
        'metrics': _calculate_subsystem_metrics()
    })

@app.route('/api/mycelium/status')
def get_mycelium_status():
    """Get mycelial network status."""
    return jsonify(_get_mycelium_metrics())

@app.route('/api/quantum/context')
def get_quantum_context():
    """Get quantum context data."""
    return jsonify({
        'consciousness': 0.999,
        'love': 0.999,
        'integration': 0.998,
        'windows_compatibility': 0.997,
        'adaptive_evolution': 0.995,
        'quantum_security': 0.996,
        'mcp_integration': 0.998,
        'visualization_quality': 0.995,
        'mycelial_connections': {
            'active_nodes': 16384,
            'connection_strength': 0.998,
            'network_health': 0.997
        },
        'subsystems': {
            'ETHIK': {'status': 'ACTIVE', 'health': 0.998},
            'ATLAS': {'status': 'ACTIVE', 'health': 0.997},
            'NEXUS': {'status': 'ACTIVE', 'health': 0.996},
            'CRONOS': {'status': 'ACTIVE', 'health': 0.995},
            'TRANSLATOR': {'status': 'ACTIVE', 'health': 0.994}
        }
    })

@app.route('/api/ml/anomalies')
def get_anomalies():
    """Get detected file anomalies."""
    return jsonify(analyzer.detect_anomalies())

@app.route('/api/ml/clusters')
def get_clusters():
    """Get file clusters."""
    return jsonify(analyzer.find_file_clusters())

@app.route('/api/ml/predictions')
def get_predictions():
    """Get usage predictions for a file."""
    file_path = request.args.get('file')
    days = request.args.get('days', 7, type=int)
    if file_path:
        return jsonify(analyzer.predict_file_usage(file_path, days))
    return jsonify({'error': 'No file specified'})

@app.route('/api/ml/optimizations')
def get_optimizations():
    """Get optimization suggestions."""
    return jsonify(analyzer.suggest_optimizations())

# Existing helper functions
def _calculate_quantum_metrics() -> Dict[str, float]:
    """Calculate quantum metrics for visualization."""
    # ... existing implementation ...

def _generate_dependency_graph() -> Dict[str, List[Dict[str, Any]]]:
    """Generate dependency graph data for visualization."""
    # ... existing implementation ...

def _calculate_subsystem_metrics() -> Dict[str, Dict[str, float]]:
    """Calculate metrics for each subsystem."""
    # ... existing implementation ...

def _check_subsystem_connection(subsystem1: str, subsystem2: str) -> bool:
    """Check if two subsystems are connected through dependencies."""
    # ... existing implementation ...

def _get_mycelium_metrics() -> Dict[str, Any]:
    """Get metrics about the mycelial network."""
    # ... existing implementation ...

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    emit('status', {'connected': True})

@socketio.on('subscribe_updates')
def handle_subscribe():
    """Start sending real-time updates."""
    def send_updates():
        while True:
            stats = collector.get_collection_stats()
            quantum_context = get_quantum_context().json
            emit('stats_update', {
                'stats': stats,
                'quantum_context': quantum_context
            })
            socketio.sleep(1)
    
    socketio.start_background_task(send_updates)

@socketio.on('subscribe_ml_updates')
def handle_ml_subscribe():
    """Start sending real-time ML analysis updates."""
    def send_updates():
        while True:
            anomalies = analyzer.detect_anomalies()
            optimizations = analyzer.suggest_optimizations()
            emit('ml_update', {
                'anomalies': anomalies,
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            })
            socketio.sleep(60)  # Update every minute
    
    socketio.start_background_task(send_updates)

if __name__ == '__main__':
    socketio.run(app, debug=True) 