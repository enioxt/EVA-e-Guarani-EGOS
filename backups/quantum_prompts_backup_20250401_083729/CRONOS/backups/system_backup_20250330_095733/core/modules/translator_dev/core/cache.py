#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Translation cache system for EVA & GUARANI Translator.

This module provides functionality to cache translations to avoid
redundant API requests and speed up repeated translations.
"""

import os
import json
import hashlib
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import time

# Set up logging
logger = logging.getLogger(__name__)


class TranslationCache:
    """Cache system for storing and retrieving translations"""

    def __init__(self, cache_dir: Optional[str] = None, ttl: int = 2592000):
        """
        Initialize the translation cache

        Args:
            cache_dir: Directory to store cache files
            ttl: Time to live for cache entries in seconds (default: 30 days)
        """
        if cache_dir is None:
            # Default cache directory
            home_dir = os.path.expanduser("~")
            self.cache_dir = os.path.join(home_dir, ".eva_guarani", "cache")
        else:
            self.cache_dir = cache_dir

        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)

        self.ttl = ttl
        self.cache_stats = {"hits": 0, "misses": 0, "last_cleared": time.time()}

        # Log cache initialization
        logger.info(f"Translation cache initialized at {self.cache_dir}")

    def get(self, key: str, engine: str = "default") -> Optional[str]:
        """
        Get a cached translation

        Args:
            key: Source text to look up
            engine: Translation engine used

        Returns:
            Cached translation or None if not found
        """
        cache_key = self._make_cache_key(key, engine)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        if not os.path.exists(cache_file):
            self.cache_stats["misses"] += 1
            return None

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # Check if cache entry has expired
            if "timestamp" in cache_data:
                if time.time() - cache_data["timestamp"] > self.ttl:
                    logger.debug(f"Cache entry expired: {cache_key}")
                    os.remove(cache_file)
                    self.cache_stats["misses"] += 1
                    return None

            # Return cached translation
            self.cache_stats["hits"] += 1
            return cache_data.get("translation")

        except Exception as e:
            logger.warning(f"Error reading cache file {cache_file}: {e}")
            self.cache_stats["misses"] += 1
            return None

    def set(self, key: str, translation: str, engine: str = "default") -> bool:
        """
        Cache a translation

        Args:
            key: Source text to cache
            translation: Translation to cache
            engine: Translation engine used

        Returns:
            True if successful, False otherwise
        """
        cache_key = self._make_cache_key(key, engine)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        try:
            cache_data = {
                "source": key,
                "translation": translation,
                "engine": engine,
                "timestamp": time.time(),
            }

            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            logger.warning(f"Error writing cache file {cache_file}: {e}")
            return False

    def clear(self) -> bool:
        """
        Clear all cached translations

        Returns:
            True if successful, False otherwise
        """
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(self.cache_dir, filename)
                    os.remove(file_path)

            # Reset cache statistics
            self.cache_stats = {"hits": 0, "misses": 0, "last_cleared": time.time()}

            logger.info("Translation cache cleared")
            return True

        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Dictionary with cache statistics
        """
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = 0.0
        if total_requests > 0:
            hit_rate = self.cache_stats["hits"] / total_requests

        return {
            "hits": self.cache_stats["hits"],
            "misses": self.cache_stats["misses"],
            "total_requests": total_requests,
            "hit_rate": hit_rate,
            "last_cleared": time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(self.cache_stats["last_cleared"])
            ),
        }

    def _make_cache_key(self, text: str, engine: str) -> str:
        """
        Make a cache key from text and engine

        Args:
            text: Source text
            engine: Translation engine

        Returns:
            Cache key string
        """
        # Create a hash of the text to use as a filename
        # Include the engine in the hash to avoid collisions between engines
        key_text = f"{engine}:{text}"
        return hashlib.md5(key_text.encode("utf-8")).hexdigest()
