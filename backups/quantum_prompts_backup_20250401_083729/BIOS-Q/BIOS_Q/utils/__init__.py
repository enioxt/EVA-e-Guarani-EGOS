#!/usr/bin/env python3
"""
EVA & GUARANI - Utilities
----------------------
This module provides utility functions and classes for the
EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

import os
import json
import logging
import hashlib
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path

from ..constants import DEFAULT_RATE_LIMIT, RATE_LIMIT_WINDOW


def generate_id(prefix: str = "") -> str:
    """Generate a unique identifier."""
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    random_suffix = os.urandom(4).hex()
    return f"{prefix}{timestamp}-{random_suffix}"


def hash_data(data: Any) -> str:
    """Generate a hash of the data."""
    if not isinstance(data, bytes):
        data = str(data).encode()
    return hashlib.sha256(data).hexdigest()


def ensure_directory(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> Dict[str, Any]:
    """Load JSON data from file."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {path}: {e}")
        return {}


def save_json(path: Path, data: Dict[str, Any]) -> None:
    """Save data to JSON file."""
    ensure_directory(path.parent)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format datetime as ISO 8601 string."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.isoformat()


def parse_timestamp(timestamp: str) -> datetime:
    """Parse ISO 8601 timestamp string."""
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def truncate_string(text: str, max_length: int = 100) -> str:
    """Truncate string to maximum length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size = int(size / 1024)
    return f"{size:.1f}PB"


class AsyncTimer:
    """Timer for periodic asynchronous tasks."""

    def __init__(self, interval: float, callback, *args, **kwargs):
        self.interval = interval
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self._task = None
        self._running = False

    async def start(self):
        """Start the timer."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        """Stop the timer."""
        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run(self):
        """Run the timer loop."""
        while self._running:
            try:
                await self.callback(*self.args, **self.kwargs)
            except Exception as e:
                logging.error(f"Error in timer callback: {e}")
            await asyncio.sleep(self.interval)


class Cache:
    """Simple in-memory cache with size limit."""

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._cache: Dict[str, Any] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        if len(self._cache) >= self.max_size:
            # Remove random item if cache is full
            self._cache.pop(next(iter(self._cache)))
        self._cache[key] = value

    def remove(self, key: str) -> None:
        """Remove value from cache."""
        self._cache.pop(key, None)

    def clear(self) -> None:
        """Clear all values from cache."""
        self._cache.clear()

    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)


class RateLimiter:
    """Rate limiter for API requests."""

    def __init__(self, limit: int = DEFAULT_RATE_LIMIT, window: int = RATE_LIMIT_WINDOW):
        self.limit = limit
        self.window = window
        self._requests: Dict[str, list] = {}

    def check_rate_limit(self, client_id: str) -> bool:
        """Check if client has exceeded rate limit."""
        now = datetime.now(timezone.utc).timestamp()

        # Get client's request timestamps
        timestamps = self._requests.get(client_id, [])

        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts <= self.window]

        # Check if limit is exceeded
        if len(timestamps) >= self.limit:
            return False

        # Add new timestamp
        timestamps.append(now)
        self._requests[client_id] = timestamps

        return True

    def get_remaining_requests(self, client_id: str) -> int:
        """Get number of remaining requests for client."""
        now = datetime.now(timezone.utc).timestamp()
        timestamps = self._requests.get(client_id, [])
        timestamps = [ts for ts in timestamps if now - ts <= self.window]
        return max(0, self.limit - len(timestamps))

    def get_reset_time(self, client_id: str) -> Optional[float]:
        """Get time until rate limit resets for client."""
        timestamps = self._requests.get(client_id, [])
        if not timestamps:
            return None

        now = datetime.now(timezone.utc).timestamp()
        oldest = min(timestamps)
        return max(0, self.window - (now - oldest))

    def clear(self, client_id: Optional[str] = None) -> None:
        """Clear rate limit data for client or all clients."""
        if client_id:
            self._requests.pop(client_id, None)
        else:
            self._requests.clear()
