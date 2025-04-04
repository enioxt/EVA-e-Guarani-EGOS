#!/usr/bin/env python3
"""
EVA & GUARANI - Constants
----------------------
This module defines system-wide constants for the
EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

from enum import Enum
from typing import Dict, Any
from pathlib import Path

# System Information
VERSION = "7.5.0"
CREATED = "2025-03-26"
AUTHOR = "EVA & GUARANI"
DESCRIPTION = "Quantum Unified System"

# File System
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"
CONFIG_DIR = ROOT_DIR / "config"
CACHE_DIR = ROOT_DIR / "cache"

# Web Interface
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080
DEFAULT_WORKERS = 4
API_PREFIX = "/api/v1"
STATIC_URL = "/static"
STATIC_DIR = ROOT_DIR / "bios_q/web/static"
TEMPLATES_DIR = ROOT_DIR / "bios_q/web/templates"

# Security
TOKEN_EXPIRY = 24 * 60 * 60  # 24 hours
REFRESH_TOKEN_EXPIRY = 604800  # 1 week
PASSWORD_MIN_LENGTH = 12
PASSWORD_MAX_LENGTH = 128
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_TIME = 15 * 60  # 15 minutes
BCRYPT_ROUNDS = 12

# Rate Limiting
DEFAULT_RATE_LIMIT = 100  # requests per window
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_BY_IP = True

# Caching
DEFAULT_CACHE_SIZE = 1000
CACHE_EXPIRY = 3600  # seconds
CACHE_ENABLED = True

# Monitoring
METRICS_INTERVAL = 60  # seconds
MAX_METRICS_AGE = 7 * 24 * 60 * 60  # 7 days
GRAFANA_DEFAULT_PORT = 3000


# Logging
class LogLevel(str, Enum):
    """Log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


DEFAULT_LOG_LEVEL = LogLevel.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_ROTATION_SIZE = 10 * 1024 * 1024  # 10MB
MAX_LOG_FILES = 10

# Mycelium Network
MAX_NODES = 100
MAX_NODE_CONNECTIONS = 100
NODE_CLEANUP_INTERVAL = 3600  # seconds
CONNECTION_TIMEOUT = 5  # seconds
UPDATE_PROPAGATION_TIMEOUT = 5  # seconds

# Quantum Search
MAX_SEARCH_RESULTS = 100
MIN_SEARCH_LENGTH = 3
SEARCH_TIMEOUT = 10  # seconds
INDEX_UPDATE_INTERVAL = 300  # 5 minutes

# Translation
MAX_TEXT_LENGTH = 5000
TRANSLATION_TIMEOUT = 30  # seconds
DEFAULT_SOURCE_LANG = "auto"
DEFAULT_TARGET_LANG = "en"
TRANSLATION_CACHE_TTL = 86400  # 24 hours


# HTTP Status Codes
class HTTPStatus(int, Enum):
    """Common HTTP status codes."""

    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    GONE = 410
    TOO_MANY_REQUESTS = 429
    INTERNAL_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503


# Content Types
class ContentType(str, Enum):
    """Common content types."""

    JSON = "application/json"
    TEXT = "text/plain"
    HTML = "text/html"
    XML = "application/xml"
    FORM = "application/x-www-form-urlencoded"
    MULTIPART = "multipart/form-data"
    OCTET_STREAM = "application/octet-stream"


# Error Codes
class ErrorCode(str, Enum):
    """System error codes."""

    INTERNAL_ERROR = "INTERNAL_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    DEPENDENCY_ERROR = "DEPENDENCY_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"


# Default Configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    "system": {
        "version": VERSION,
        "host": DEFAULT_HOST,
        "port": DEFAULT_PORT,
        "workers": DEFAULT_WORKERS,
        "debug": False,
    },
    "security": {
        "token_expiry": TOKEN_EXPIRY,
        "refresh_token_expiry": REFRESH_TOKEN_EXPIRY,
        "password_min_length": PASSWORD_MIN_LENGTH,
        "max_login_attempts": MAX_LOGIN_ATTEMPTS,
        "bcrypt_rounds": BCRYPT_ROUNDS,
    },
    "rate_limiting": {
        "enabled": True,
        "limit": DEFAULT_RATE_LIMIT,
        "window": RATE_LIMIT_WINDOW,
        "by_ip": RATE_LIMIT_BY_IP,
    },
    "caching": {"enabled": CACHE_ENABLED, "ttl": CACHE_EXPIRY, "max_size": DEFAULT_CACHE_SIZE},
    "monitoring": {
        "enabled": True,
        "interval": METRICS_INTERVAL,
        "max_metrics": MAX_METRICS_AGE,
        "grafana_port": GRAFANA_DEFAULT_PORT,
    },
    "logging": {
        "level": DEFAULT_LOG_LEVEL.value,
        "format": LOG_FORMAT,
        "date_format": DATE_FORMAT,
        "max_size": LOG_ROTATION_SIZE,
        "backup_count": MAX_LOG_FILES,
    },
    "mycelium": {
        "max_nodes": MAX_NODES,
        "max_connections_per_node": MAX_NODE_CONNECTIONS,
        "node_timeout": CONNECTION_TIMEOUT,
        "update_timeout": UPDATE_PROPAGATION_TIMEOUT,
    },
    "quantum_search": {
        "max_results": MAX_SEARCH_RESULTS,
        "min_score": MIN_SEARCH_LENGTH,
        "timeout": SEARCH_TIMEOUT,
        "index_update_interval": INDEX_UPDATE_INTERVAL,
    },
    "translation": {
        "default_source": DEFAULT_SOURCE_LANG,
        "default_target": DEFAULT_TARGET_LANG,
        "timeout": TRANSLATION_TIMEOUT,
        "max_text_length": MAX_TEXT_LENGTH,
        "cache_ttl": TRANSLATION_CACHE_TTL,
    },
}

# File size limits
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
MAX_LOG_SIZE = 100 * 1024 * 1024  # 100MB

# Network settings
DEFAULT_TIMEOUT = 30  # seconds

# System paths
TEMP_DIR = "temp"

# Version info
PYTHON_MIN_VERSION = (3, 9, 0)
BUILD_DATE = "2025-03-26"
