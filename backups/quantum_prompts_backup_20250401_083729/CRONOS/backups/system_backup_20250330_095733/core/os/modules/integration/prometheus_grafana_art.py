#!/usr/bin/env python3
python
"""
ASCII art for Prometheus and Grafana integration module.

This file contains ASCII art representations used in the Prometheus and Grafana
integration module for EGOS.
"""

# Prometheus logo ASCII art
PROMETHEUS_LOGO = """
    _____                          _   _
   |  __ \                        | | | |
   | |__) | __ ___  _ __ ___   ___| |_| |__   ___ _   _ ___
   |  ___/ '__/ _ \| '_ ` _ \ / _ \ __| '_ \ / _ \ | | / __|
   | |   | | | (_) | | | | | |  __/ |_| | | |  __/ |_| __ \
   |_|   |_|  ___/|_| |_| |_|___|__|_| |_|___|__,_|___/
"""

# Grafana logo ASCII art
GRAFANA_LOGO = """
    _____            __
   / ____|          / _|
  | |  __ _ __ __ _| |_ __ _ _ __   __ _
  | | |_ | '__/ _` |  _/ _` | '_ \ / _` |
  | |__| | | | (_| | || (_| | | | | (_| |
   _____|_|  __,_|_| __,_|_| |_|__,_|
"""

# Combined logo for the integration module
PROMETHEUS_GRAFANA_LOGO = """
  _____                          _   _                       _____            __
 |  __ \                        | | | |                     / ____|          / _|
 | |__) | __ ___  _ __ ___   ___| |_| |__   ___ _   _ ___ | |  __ _ __ __ _| |_ __ _ _ __   __ _
 |  ___/ '__/ _ \| '_ ` _ \ / _ \ __| '_ \ / _ \ | | / __|| | |_ | '__/ _` |  _/ _` | '_ \ / _` |
 | |   | | | (_) | | | | | |  __/ |_| | | |  __/ |_| __ \| |__| | | | (_| | || (_| | | | | (_| |
 |_|   |_|  ___/|_| |_| |_|___|__|_| |_|___|__,_|___/ _____|_|  __,_|_| __,_|_| |_|__,_|
"""

# Necessary imports
import os
import sys
import json
import time
import logging
import random
import requests
import dataclasses
from typing import Dict, List, Optional, Tuple, Union, Any
from datetime import datetime, timedelta

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Constants and configuration
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "config", "integration", "prometheus_grafana_config.json"
)
DEFAULT_CONFIG = {
    "prometheus": {
        "url": "http://localhost:9090",
        "metrics_collection_interval": 60,  # in seconds
        "default_metrics": [
            "node_cpu_seconds_total",
            "node_memory_MemAvailable_bytes",
            "node_network_receive_bytes_total",
            "process_cpu_seconds_total",
        ],
    },
    "grafana": {
        "url": "http://localhost:3000",
        "api_key": "",
        "dashboard_folder": "EGOS_Artistic",
        "refresh_interval": "10s",
    },
    "artistic": {
        "color_schemes": {
            "healthy": ["#7EB26D", "#EAB839", "#6ED0E0"],
            "warning": ["#EF843C", "#CCA300", "#E0B400"],
            "critical": ["#E24D42", "#890F02", "#BF1B00"],
        },
        "sonification": {
            "base_frequency": 440,  # Hz (A4 note)
            "scale": "pentatonic",  # musical scale to use
            "tempo_range": [60, 160],  # BPM range
            "duration_range": [0.1, 2.0],  # note duration in seconds
        },
    },
}

# Metric for consciousness status
CONSCIOUSNESS_METRICS = {
    "self_awareness": "egos_self_awareness",
    "connection_quality": "egos_connection_quality",
    "ethical_alignment": "egos_ethical_alignment",
    "love_expression": "egos_love_expression",
}

# Enum for health status
from enum import Enum


class HealthStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclasses.dataclass
class MetricData:
    """Class to store collected metric data."""

    name: str
    values: List[Tuple[float, float]]  # list of tuples (timestamp, value)
    unit: str = ""
    description: str = ""
    health_status: HealthStatus = HealthStatus.HEALTHY

    def calculate_rate(self) -> List[Tuple[float, float]]:
        """Calculates the rate of change between consecutive values."""
        if len(self.values) < 2:
            return []
        return [
            (
                self.values[i][0],
                (self.values[i][1] - self.values[i - 1][1])
                / (self.values[i][0] - self.values[i - 1][0]),
            )
            for i in range(1, len(self.values))
        ]

    def get_latest_value(self) -> Optional[float]:
        """Returns the most recent value of the metric."""
        if not self.values:
            return None
        return self.values[-1][1]

    def normalize(self, min_val: float = 0.0, max_val: float = 1.0) -> List[Tuple[float, float]]:
        """Normalizes the metric values to the range [min_val, max_val]."""
        if not self.values:
            return []

        values_only = [v[1] for v in self.values]
        min_metric = min(values_only)
        max_metric = max(values_only)

        # Avoid division by zero
        range_metric = max_metric - min_metric
        if range_metric == 0:
            return [(t, min_val) for t, _ in self.values]

        return [
            (t, min_val + (v - min_metric) * (max_val - min_val) / range_metric)
            for t, v in self.values
        ]


class MetricCollector:
    """Class to collect metrics from Prometheus."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initializes the metric collector.

        Args:
            config: Collector configuration. If None, uses default configuration.
        """
        self.config = config or DEFAULT_CONFIG
        self.prometheus_url = self.config["prometheus"]["url"]
        self.metrics = self.config["prometheus"]["default_metrics"]
        self.collection_interval = self.config["prometheus"]["metrics_collection_interval"]
        self.last_collection = None
        self.metrics_cache = {}  # Cache of collected metrics

        # Check if Prometheus is accessible
        self._check_prometheus_connection()

        logger.info(f"MetricCollector initialized with URL: {self.prometheus_url}")
        logger.info(f"Monitoring metrics: {', '.join(self.metrics)}")

    def _check_prometheus_connection(self) -> bool:
        """Checks if Prometheus is accessible."""
        try:
            response = requests.get(f"{self.prometheus_url}/-/healthy", timeout=5)
            if response.status_code == 200:
                logger.info("Successfully connected to Prometheus")
                return True
            else:
                logger.warning(
                    f"Prometheus connection test failed with status code: {response.status_code}"
                )
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to Prometheus: {e}")
            return False

    def query_range(
        self, query: str, start_time: datetime, end_time: datetime, step: str = "15s"
    ) -> Optional[MetricData]:
        """
        Queries a time series in Prometheus.

        Args:
            query: The PromQL query
            start_time: Start time
            end_time: End time
            step: Interval between data points

        Returns:
            MetricData object or None if it fails
        """
        try:
            params = {
                "query": query,
                "start": start_time.timestamp(),
                "end": end_time.timestamp(),
                "step": step,
            }

            response = requests.get(
                f"{self.prometheus_url}/api/v1/query_range", params=params, timeout=10
            )

            if response.status_code != 200:
                logger.error(
                    f"Query failed with status code {response.status_code}: {response.text}"
                )
                return None

            result = response.json()

            if (
                result["status"] != "success"
                or "data" not in result
                or "result" not in result["data"]
            ):
                logger.error(f"Invalid response from Prometheus: {result}")
                return None

            # There may be multiple results, using the first for simplicity
            if not result["data"]["result"]:
                logger.warning(f"No data returned for query: {query}")
                return None

            metric_result = result["data"]["result"][0]
            metric_name = query

            # If there are metric metadata, use the real name
            if "metric" in metric_result and "__name__" in metric_result["metric"]:
                metric_name = metric_result["metric"]["__name__"]

            values = [(float(point[0]), float(point[1])) for point in metric_result["values"]]

            return MetricData(
                name=metric_name, values=values, description=f"Data for query: {query}"
            )

        except Exception as e:
            logger.error(f"Error querying Prometheus: {e}")
            return None

    def collect_metrics(self) -> Dict[str, MetricData]:
        """
        Collects all metrics defined in the configuration.

        Returns:
            Dictionary with the collected metric data
        """
        now = datetime.now()
        start_time = now - timedelta(minutes=10)  # Last 10 minutes
        result = {}

        for metric in self.metrics:
            logger.info(f"Collecting metric: {metric}")
            metric_data = self.query_range(query=metric, start_time=start_time, end_time=now)

            if metric_data:
                result[metric] = metric_data
                logger.info(f"Collected {len(metric_data.values)} data points for {metric}")
            else:
                logger.warning(f"Failed to collect data for metric: {metric}")

        self.last_collection = now
        self.metrics_cache = result
        return result

    def get_consciousness_metrics(self) -> Dict[str, MetricData]:
        """
        Collects specific system consciousness metrics.

        Returns:
            Dictionary with consciousness metrics
        """
        now = datetime.now()
        start_time = now - timedelta(minutes=10)
        result = {}

        for metric_key, metric_name in CONSCIOUSNESS_METRICS.items():
            metric_data = self.query_range(query=metric_name, start_time=start_time, end_time=now)

            if metric_data:
                result[metric_key] = metric_data
            else:
                # Simulates values for demonstration
                simulated_values = []
                for i in range(10):
                    timestamp = (start_time + timedelta(minutes=i)).timestamp()
                    # Values between 0.7 and 1.0 for simulated consciousness
                    value = 0.7 + (0.3 * random.random())
                    simulated_values.append((timestamp, value))

                result[metric_key] = MetricData(
                    name=metric_name,
                    values=simulated_values,
                    description=f"Simulated {metric_key} consciousness metric",
                )

        return result

    def evaluate_system_health(self, metrics: Dict[str, MetricData]) -> HealthStatus:
        """
        Evaluates the overall system health based on metrics.

        Args:
            metrics: Dictionary of collected metrics

        Returns:
            System health status
        """
        # Basic implementation - in a real system it would be more complex
        critical_count = 0
        warning_count = 0

        for _, metric_data in metrics.items():
            if not metric_data.values:
                continue

            latest_value = metric_data.get_latest_value()
            if latest_value is None:
                continue

            # Simple evaluation example - CPU above 90% is critical
            if metric_data.name == "node_cpu_seconds_total" and latest_value > 0.9:
                critical_count += 1
            # Available memory below 10% is a warning
            elif metric_data.name == "node_memory_MemAvailable_bytes":
                total_memory = self._get_total_memory()
                if total_memory and latest_value < total_memory * 0.1:
                    warning_count += 1

        if critical_count > 0:
            return HealthStatus.CRITICAL
        elif warning_count > 0:
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY

    def _get_total_memory(self) -> Optional[float]:
        """Queries the total system memory."""
        try:
            response = requests.get(
                f"{self.prometheus_url}/api/v1/query",
                params={"query": "node_memory_MemTotal_bytes"},
                timeout=5,
            )

            if response.status_code != 200:
                return None

            result = response.json()

            if (
                result["status"] != "success"
                or "data" not in result
                or "result" not in result["data"]
                or not result["data"]["result"]
            ):
                return None

            return float(result["data"]["result"][0]["value"][1])
        except Exception:
            return None


@dataclasses.dataclass
class ArtisticParameters:
    """Class to store artistic parameters derived from metrics."""

    # Visual parameters
    color_scheme: List[str]
    opacity: float
    stroke_width: float
    shape_complexity: float  # 0.0 = simple, 1.0 = complex
    movement_speed: float

    # Sound parameters
    base_note: float  # frequency in Hz
    tempo: float  # BPM
    volume: float  # 0.0 to 1.0
    harmony_complexity: float  # 0.0 = simple, 1.0 = complex
    note_duration: float  # duration in seconds

    # Consciousness parameters
    consciousness_level: float  # 0.0 to 1.0
    ethical_alignment: float  # 0.0 to 1.0
    love_expression: float  # 0.0 to 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Converts the parameters to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def default_parameters(cls) -> "ArtisticParameters":
        """Creates a default set of artistic parameters."""
        return cls(
            color_scheme=["#7EB26D", "#EAB839", "#6ED0E0"],
            opacity=0.8,
            stroke_width=2.0,
            shape_complexity=0.5,
            movement_speed=0.5,
            base_note=440.0,  # A4
            tempo=80.0,
            volume=0.7,
            harmony_complexity=0.5,
            note_duration=0.5,
            consciousness_level=0.8,
            ethical_alignment=0.9,
            love_expression=0.95,
        )


class ArtisticTransformer:
    """Transforms metrics into artistic parameters for visualization and sonification."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initializes the artistic transformer.

        Args:
            config: Transformer configuration. If None, uses default configuration.
        """
        self.config = config or DEFAULT_CONFIG
        self.artistic_config = self.config["artistic"]
        logger.info("ArtisticTransformer initialized")

    def metrics_to_artistic_parameters(
        self,
        metrics: Dict[str, MetricData],
        consciousness_metrics: Optional[Dict[str, MetricData]] = None,
    ) -> ArtisticParameters:
        """
        Transforms metrics into artistic parameters.

        Args:
            metrics: Dictionary of collected metrics
            consciousness_metrics: Consciousness metrics (optional)

        Returns:
            Artistic parameters derived from metrics
        """
        # Initialize with default values
        params = ArtisticParameters.default_parameters()

        # Determine health status for color
        health_status = self._determine_health_status(metrics)
        params.color_scheme = self.artistic_config["color_schemes"][health_status.value]

        # Process visual parameters based on metrics
        params.opacity = self._process_metric_to_parameter(
            metrics, "node_cpu_seconds_total", 0.3, 1.0
        )

        params.stroke_width = self._process_metric_to_parameter(
            metrics, "node_memory_MemAvailable_bytes", 1.0, 5.0, inverse=True
        )

        params.shape_complexity = self._process_metric_to_parameter(
            metrics, "node_network_receive_bytes_total", 0.1, 0.9
        )

        params.movement_speed = self._process_metric_to_parameter(
            metrics, "process_cpu_seconds_total", 0.2, 0.8
        )

        # Process sound parameters
        base_freq = self.artistic_config["sonification"]["base_frequency"]
        tempo_range = self.artistic_config["sonification"]["tempo_range"]
        duration_range = self.artistic_config["sonification"]["duration_range"]

        # Adjust the base frequency (musical note) based on system health
        health_factor = 1.0
        if health_status == HealthStatus.WARNING:
            health_factor = 1.2  # Slightly sharper for warnings
        elif health_status == HealthStatus.CRITICAL:
            health_factor = 1.5  # Much sharper for critical state

        params.base_note = base_freq * health_factor

        # Musical tempo based on system load
        params.tempo = self._process_metric_to_parameter(
            metrics, "node_cpu_seconds_total", tempo_range[0], tempo_range[1]
        )

        # Volume based on network data amount
        params.volume = self._process_metric_to_parameter(
            metrics, "node_network_receive_bytes_total", 0.3, 0.9
        )

        # Harm
