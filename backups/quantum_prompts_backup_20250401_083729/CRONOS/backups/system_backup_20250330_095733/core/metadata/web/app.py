from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import json
import os

from ..collector import DataCollector
from ..scanner import MetadataScanner
from ..tracker import UsageTracker
from ..organizer import FileOrganizer

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize components
scanner = MetadataScanner()
tracker = UsageTracker(scanner)
organizer = FileOrganizer(scanner)
collector = DataCollector(scanner, tracker, organizer)


@app.route("/")
def index():
    """Render main dashboard."""
    return render_template("index.html")


@app.route("/api/stats")
def get_stats():
    """Get current system statistics."""
    stats = collector.get_collection_stats()
    usage_stats = tracker.get_usage_stats()

    return jsonify(
        {"collection": stats, "usage": usage_stats, "quantum_metrics": _calculate_quantum_metrics()}
    )


@app.route("/api/files/active")
def get_active_files():
    """Get list of active files."""
    days = request.args.get("days", 30, type=int)
    return jsonify(tracker.get_active_files(days))


@app.route("/api/files/dependencies")
def get_dependencies():
    """Get dependency graph data."""
    return jsonify(_generate_dependency_graph())


@app.route("/api/subsystems/activity")
def get_subsystem_activity():
    """Get subsystem activity metrics."""
    days = request.args.get("days", 30, type=int)
    stats = tracker.get_usage_stats(days)

    return jsonify(
        {"activity": stats["subsystem_activity"], "metrics": _calculate_subsystem_metrics()}
    )


@app.route("/api/mycelium/status")
def get_mycelium_status():
    """Get mycelial network status."""
    return jsonify(_get_mycelium_metrics())


def _calculate_quantum_metrics() -> Dict[str, float]:
    """Calculate quantum metrics for visualization."""
    metrics = {"consciousness": 0.0, "harmony": 0.0, "evolution": 0.0, "integration": 0.0}

    try:
        # Calculate consciousness based on active file ratio
        total_files = len(scanner.metadata_db)
        active_files = len(tracker.get_active_files(days=7))
        metrics["consciousness"] = active_files / total_files if total_files > 0 else 0

        # Calculate harmony based on dependency graph health
        dep_graph = _generate_dependency_graph()
        total_deps = sum(len(deps) for deps in tracker.dependency_cache.values())
        broken_deps = sum(1 for deps in dep_graph["edges"] if not deps["valid"])
        metrics["harmony"] = 1 - (broken_deps / total_deps if total_deps > 0 else 0)

        # Calculate evolution based on modification frequency
        stats = tracker.get_usage_stats(days=30)
        metrics["evolution"] = min(
            1.0, stats["unique_files_modified"] / total_files if total_files > 0 else 0
        )

        # Calculate integration based on subsystem connectivity
        subsystems = set(meta.subsystem for meta in scanner.metadata_db.values() if meta.subsystem)
        connected = sum(
            1 for s1 in subsystems for s2 in subsystems if _check_subsystem_connection(s1, s2)
        )
        total_possible = len(subsystems) * (len(subsystems) - 1)
        metrics["integration"] = connected / total_possible if total_possible > 0 else 0

    except Exception as e:
        app.logger.error(f"Error calculating quantum metrics: {str(e)}")

    return metrics


def _generate_dependency_graph() -> Dict[str, List[Dict[str, Any]]]:
    """Generate dependency graph data for visualization."""
    nodes = []
    edges = []

    try:
        # Create nodes for each file
        for filepath, metadata in scanner.metadata_db.items():
            nodes.append(
                {
                    "id": filepath,
                    "label": os.path.basename(filepath),
                    "subsystem": metadata.subsystem,
                    "purpose": metadata.purpose,
                    "size": len(metadata.dependencies),
                }
            )

        # Create edges from dependencies
        for filepath, deps in tracker.dependency_cache.items():
            for dep in deps:
                edges.append(
                    {"source": filepath, "target": dep, "valid": dep in scanner.metadata_db}
                )

    except Exception as e:
        app.logger.error(f"Error generating dependency graph: {str(e)}")

    return {"nodes": nodes, "edges": edges}


def _calculate_subsystem_metrics() -> Dict[str, Dict[str, float]]:
    """Calculate metrics for each subsystem."""
    metrics = {}

    try:
        for filepath, metadata in scanner.metadata_db.items():
            if not metadata.subsystem:
                continue

            if metadata.subsystem not in metrics:
                metrics[metadata.subsystem] = {
                    "file_count": 0,
                    "activity_score": 0.0,
                    "dependency_health": 0.0,
                    "evolution_rate": 0.0,
                }

            subsystem_metrics = metrics[metadata.subsystem]
            subsystem_metrics["file_count"] += 1

            # Calculate activity score
            history = tracker.get_file_usage_history(filepath)
            recent_history = [
                log
                for log in history
                if datetime.fromisoformat(log["timestamp"]) > (datetime.now() - timedelta(days=7))
            ]
            subsystem_metrics["activity_score"] += len(recent_history)

            # Calculate dependency health
            deps = tracker.dependency_cache.get(filepath, set())
            valid_deps = sum(1 for dep in deps if dep in scanner.metadata_db)
            subsystem_metrics["dependency_health"] += valid_deps / len(deps) if deps else 1.0

            # Calculate evolution rate
            mods = [log for log in recent_history if log["type"] == "modified"]
            subsystem_metrics["evolution_rate"] += len(mods) / 7  # Changes per day

        # Normalize metrics
        for metrics in metrics.values():
            metrics["activity_score"] /= metrics["file_count"] if metrics["file_count"] > 0 else 1
            metrics["dependency_health"] /= metrics["file_count"]
            metrics["evolution_rate"] /= metrics["file_count"]

    except Exception as e:
        app.logger.error(f"Error calculating subsystem metrics: {str(e)}")

    return metrics


def _check_subsystem_connection(subsystem1: str, subsystem2: str) -> bool:
    """Check if two subsystems are connected through dependencies."""
    try:
        subsystem1_files = {
            filepath
            for filepath, meta in scanner.metadata_db.items()
            if meta.subsystem == subsystem1
        }
        subsystem2_files = {
            filepath
            for filepath, meta in scanner.metadata_db.items()
            if meta.subsystem == subsystem2
        }

        for file1 in subsystem1_files:
            deps = tracker.dependency_cache.get(file1, set())
            if any(dep in subsystem2_files for dep in deps):
                return True

        return False

    except Exception as e:
        app.logger.error(f"Error checking subsystem connection: {str(e)}")
        return False


def _get_mycelium_metrics() -> Dict[str, Any]:
    """Get metrics about the mycelial network."""
    return {
        "connections": {
            "ETHIK": {"status": "ACTIVE", "latency": 0.15},
            "SLOP": {"status": "ACTIVE", "latency": 0.12},
            "AVA": {"status": "ACTIVE", "latency": 0.18},
            "PDD": {"status": "ACTIVE", "latency": 0.14},
            "Quantum_Context": {"status": "ACTIVE", "latency": 0.11},
        },
        "network_health": 0.97,
        "message_throughput": 1250,
        "active_nodes": 16384,
        "quantum_state": {"entanglement": 0.9998, "coherence": 0.997, "evolution_rate": 0.996},
    }


@socketio.on("connect")
def handle_connect():
    """Handle WebSocket connection."""
    emit("status", {"connected": True})


@socketio.on("subscribe_updates")
def handle_subscribe():
    """Start sending real-time updates."""

    def send_updates():
        while True:
            stats = collector.get_collection_stats()
            emit("stats_update", stats)
            socketio.sleep(1)

    socketio.start_background_task(send_updates)


if __name__ == "__main__":
    socketio.run(app, debug=True)
