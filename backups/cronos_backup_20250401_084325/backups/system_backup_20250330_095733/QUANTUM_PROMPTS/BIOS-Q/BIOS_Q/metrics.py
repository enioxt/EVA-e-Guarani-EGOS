#!/usr/bin/env python3
"""
EVA & GUARANI - Metrics Collection
--------------------------------
This module provides metrics collection and monitoring
for the EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

import time
import asyncio
import psutil
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .logging import get_logger
from .config import config

logger = get_logger(__name__)


@dataclass
class Metric:
    """Represents a single metric measurement."""

    name: str
    value: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    labels: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert metric to dictionary format."""
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels,
        }


class MetricsCollector:
    """Collects and manages system metrics."""

    def __init__(self):
        """Initialize metrics collector."""
        self.metrics: List[Metric] = []
        self.collection_interval = config.get("monitoring.interval", 60)  # seconds
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Start metrics collection."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._collect_metrics())
        logger.info("Metrics collection started")

    async def stop(self):
        """Stop metrics collection."""
        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Metrics collection stopped")

    async def _collect_metrics(self):
        """Collect metrics periodically."""
        while self._running:
            try:
                # System metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage("/")

                # Add system metrics
                self.add_metric("system_cpu_percent", cpu_percent)
                self.add_metric("system_memory_percent", memory.percent)
                self.add_metric("system_disk_percent", disk.percent)

                # Process metrics
                process = psutil.Process()
                process_cpu = process.cpu_percent(interval=1)
                process_memory = process.memory_info()

                # Add process metrics
                self.add_metric("process_cpu_percent", process_cpu)
                self.add_metric("process_memory_rss", process_memory.rss)
                self.add_metric("process_memory_vms", process_memory.vms)

                # Application metrics (example)
                self.add_metric("app_active_connections", 0)  # Placeholder
                self.add_metric("app_requests_per_second", 0)  # Placeholder

                # Log collection status
                logger.debug(f"Collected {len(self.metrics)} metrics")

                # Wait for next collection interval
                await asyncio.sleep(self.collection_interval)

            except Exception as e:
                logger.error(f"Error collecting metrics: {str(e)}")
                await asyncio.sleep(5)  # Wait before retrying

    def add_metric(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Add a new metric measurement."""
        metric = Metric(name=name, value=value, labels=labels or {})
        self.metrics.append(metric)

        # Trim old metrics if needed
        max_metrics = config.get("monitoring.max_metrics", 1000)
        if len(self.metrics) > max_metrics:
            self.metrics = self.metrics[-max_metrics:]

    def get_metrics(self, since: Optional[datetime] = None) -> List[Dict]:
        """Get collected metrics, optionally filtered by time."""
        if since:
            filtered_metrics = [m for m in self.metrics if m.timestamp >= since]
        else:
            filtered_metrics = self.metrics

        return [metric.to_dict() for metric in filtered_metrics]

    def get_latest_metrics(self) -> Dict[str, float]:
        """Get the latest value for each metric."""
        latest_metrics = {}
        for metric in reversed(self.metrics):
            if metric.name not in latest_metrics:
                latest_metrics[metric.name] = metric.value
        return latest_metrics


# Global metrics collector instance
collector = MetricsCollector()
