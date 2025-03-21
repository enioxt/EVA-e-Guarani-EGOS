from dataclasses import dataclass
import os
import json
import hashlib
from typing import Dict, Any, Optional, Union
try:
    from diskcache import Cache
    DISKCACHE_AVAILABLE = True
except ImportError:
    DISKCACHE_AVAILABLE = False
    Cache = Any

@dataclass
class CacheConfig:
    enabled: bool = True
    directory: str = "./cache"
    max_size: int = 1_000_000_000  # 1GB
    
class TranslationCache:
    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        self._cache: Optional[Cache] = None
        
        if self.config.enabled and DISKCACHE_AVAILABLE:
            os.makedirs(self.config.directory, exist_ok=True)
            self._cache = Cache(
                directory=self.config.directory,
                size_limit=self.config.max_size
            )
    
    def _get_key(self, text: str, engine: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Generate a unique key based on text, engine and options"""
        key_parts = [text, engine]
        
        if options:
            # Sort options to ensure consistency
            sorted_options = json.dumps(options, sort_keys=True)
            key_parts.append(sorted_options)
            
        key_str = "::".join(key_parts)
        return hashlib.md5(key_str.encode('utf-8')).hexdigest()
    
    def get(self, text: str, engine: str, options: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Retrieve translation from cache if it exists"""
        if not self.config.enabled or not self._cache:
            return None
            
        key = self._get_key(text, engine, options)
        return self._cache.get(key)
    
    def set(self, text: str, translation: str, engine: str, options: Optional[Dict[str, Any]] = None) -> None:
        """Store translation in cache"""
        if not self.config.enabled or not self._cache:
            return
            
        key = self._get_key(text, engine, options)
        self._cache.set(key, translation)
    
    def clear(self) -> None:
        """Clear entire cache"""
        if self._cache:
            self._cache.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Return cache statistics"""
        if not self._cache:
            return {"enabled": False}
            
        return {
            "enabled": True,
            "size": self._cache.size,
            "size_limit": self._cache.size_limit,
            "count": len(self._cache),
            "directory": self.config.directory
        } 