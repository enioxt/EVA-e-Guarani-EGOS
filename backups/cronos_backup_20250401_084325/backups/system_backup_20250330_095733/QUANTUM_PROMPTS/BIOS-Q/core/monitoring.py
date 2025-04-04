#!/usr/bin/env python3
"""
Monitoring System - EVA & GUARANI Core Module
------------------------------------------
This module implements the monitoring system that integrates
Prometheus and Grafana with all subsystems.

Version: 7.5
Created: 2025-03-26
"""

import os
import sys
import json
import logging
import time
from typing import Dict, List, Any, Optional, Set, Union
from datetime import datetime
import asyncio
from pathlib import Path
from prometheus_client import start_http_server, Counter, Gauge, Histogram, Info
from aiohttp import web
import aiohttp

# Import core systems
from .mycelium_network import mycelium
from .quantum_search import quantum_search
from .translator import translator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("monitoring")


class MetricsCollector:
    """Collects and manages Prometheus metrics."""

    def __init__(self):
        # System metrics
        self.total_nodes = Gauge(
            "eva_guarani_total_nodes", "Total number of nodes in the Mycelium network"
        )

        self.active_connections = Gauge(
            "eva_guarani_active_connections", "Number of active connections in the Mycelium network"
        )

        self.search_requests = Counter(
            "eva_guarani_search_requests_total",
            "Total number of quantum search requests",
            ["status"],
        )

        self.translation_requests = Counter(
            "eva_guarani_translation_requests_total",
            "Total number of translation requests",
            ["source_lang", "target_lang", "status"],
        )

        self.search_latency = Histogram(
            "eva_guarani_search_latency_seconds",
            "Quantum search request latency in seconds",
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
        )

        self.translation_latency = Histogram(
            "eva_guarani_translation_latency_seconds",
            "Translation request latency in seconds",
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
        )

        # System information
        self.system_info = Info("eva_guarani_system", "EVA & GUARANI system information")

        # Memory usage
        self.memory_usage = Gauge(
            "eva_guarani_memory_bytes", "Memory usage in bytes", ["component"]
        )

        # Update system info
        self._update_system_info()

    def _update_system_info(self):
        """Update system information metrics."""
        self.system_info.info(
            {
                "version": "7.5",
                "build_date": "2025-03-26",
                "python_version": sys.version,
                "platform": sys.platform,
            }
        )

    async def collect_metrics(self):
        """Collect metrics from all subsystems."""
        try:
            # Update Mycelium network metrics
            if mycelium and mycelium.node:
                self.total_nodes.set(len(mycelium.nodes))
                total_connections = sum(len(node.connections) for node in mycelium.nodes.values())
                self.active_connections.set(total_connections)

            # Update Quantum Search metrics
            if quantum_search:
                stats = quantum_search.get_stats()
                self.memory_usage.labels(component="quantum_search").set(
                    sys.getsizeof(quantum_search.index.index)
                )

            # Update Translator metrics
            if translator:
                stats = translator.get_stats()
                self.memory_usage.labels(component="translator").set(
                    sys.getsizeof(translator.memory.memory)
                )

        except Exception as e:
            logger.error(f"Error collecting metrics: {str(e)}")


class MonitoringSystem:
    """
    The Monitoring system that provides observability across
    all EVA & GUARANI subsystems using Prometheus and Grafana.
    """

    def __init__(self, prometheus_port: int = 9090, grafana_url: str = "http://localhost:3000"):
        self.prometheus_port = prometheus_port
        self.grafana_url = grafana_url
        self.metrics = MetricsCollector()
        self.node = mycelium.get_node("MONITORING")

        if not self.node:
            self.node = mycelium.register_node("MONITORING", "monitoring")

        # Connect to other systems
        self._connect_to_systems()

    def _connect_to_systems(self):
        """Connect to other core systems."""
        systems = ["QUANTUM_SEARCH", "TRANSLATOR"]
        for system in systems:
            node = mycelium.get_node(system)
            if node:
                mycelium.connect_nodes("MONITORING", system)
                logger.info(f"Connected to {system} system")
            else:
                logger.warning(f"{system} system not found")

    async def start(self):
        """Start the monitoring system."""
        try:
            # Start Prometheus HTTP server
            start_http_server(self.prometheus_port)
            logger.info(f"Prometheus metrics server started on port {self.prometheus_port}")

            # Start metrics collection loop
            while True:
                await self.metrics.collect_metrics()
                await asyncio.sleep(15)  # Collect metrics every 15 seconds

        except Exception as e:
            logger.error(f"Error starting monitoring system: {str(e)}")

    async def create_grafana_dashboard(self):
        """Create or update Grafana dashboard."""
        dashboard = {
            "dashboard": {
                "id": None,
                "uid": "eva-guarani-dashboard",
                "title": "EVA & GUARANI Dashboard",
                "tags": ["eva-guarani", "v7.5"],
                "timezone": "browser",
                "schemaVersion": 21,
                "version": 1,
                "refresh": "10s",
                "panels": [
                    {
                        "title": "Mycelium Network Status",
                        "type": "stat",
                        "datasource": "Prometheus",
                        "targets": [
                            {"expr": "eva_guarani_total_nodes"},
                            {"expr": "eva_guarani_active_connections"},
                        ],
                    },
                    {
                        "title": "Search Requests",
                        "type": "graph",
                        "datasource": "Prometheus",
                        "targets": [{"expr": "rate(eva_guarani_search_requests_total[5m])"}],
                    },
                    {
                        "title": "Translation Requests",
                        "type": "graph",
                        "datasource": "Prometheus",
                        "targets": [{"expr": "rate(eva_guarani_translation_requests_total[5m])"}],
                    },
                    {
                        "title": "System Memory Usage",
                        "type": "gauge",
                        "datasource": "Prometheus",
                        "targets": [{"expr": "eva_guarani_memory_bytes"}],
                    },
                ],
            },
            "overwrite": True,
        }

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {os.getenv('GRAFANA_API_KEY')}",
                }

                async with session.post(
                    f"{self.grafana_url}/api/dashboards/db", json=dashboard, headers=headers
                ) as response:
                    if response.status == 200:
                        logger.info("Grafana dashboard created/updated successfully")
                    else:
                        logger.error(f"Error creating Grafana dashboard: {response.status}")

        except Exception as e:
            logger.error(f"Error creating Grafana dashboard: {str(e)}")

    def get_stats(self) -> Dict[str, Any]:
        """Get monitoring system statistics."""
        return {
            "prometheus_port": self.prometheus_port,
            "grafana_url": self.grafana_url,
            "connected_nodes": len(self.node.connections) if self.node else 0,
            "last_update": datetime.now().isoformat(),
        }


# Initialize the global monitoring system
monitoring = MonitoringSystem()

if __name__ == "__main__":
    # Test the monitoring system
    async def test_monitoring():
        print("\n✧༺❀༻∞ EVA & GUARANI - Monitoring Test ∞༺❀༻✧\n")

        print("Starting monitoring system...")

        # Create Grafana dashboard
        print("\nCreating Grafana dashboard...")
        await monitoring.create_grafana_dashboard()

        # Start collecting metrics
        print("\nCollecting metrics...")
        try:
            await monitoring.start()
        except KeyboardInterrupt:
            print("\nMonitoring system stopped")

        # Print stats
        stats = monitoring.get_stats()
        print(f"\nSystem Stats:")
        print(f"Prometheus Port: {stats['prometheus_port']}")
        print(f"Grafana URL: {stats['grafana_url']}")
        print(f"Connected Nodes: {stats['connected_nodes']}")
        print(f"Last Update: {stats['last_update']}")

        print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

    # Run the test
    asyncio.run(test_monitoring())
