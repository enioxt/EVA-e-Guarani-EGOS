import os
import sys
import pytest
from pathlib import Path

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from modules.translator_dev.config.config import ConfigManager, TranslatorConfig
from modules.translator_dev.core.cache import TranslationCache, CacheConfig
from modules.translator_dev.engines.huggingface.marian_engine import MarianTranslator, MarianConfig

def test_config_loading():
    """Test configuration loading and defaults"""
    config = ConfigManager()
    assert isinstance(config.config, TranslatorConfig)
    assert config.config.engine.name == "huggingface"
    assert config.config.cache.enabled is True

def test_cache_operations():
    """Test cache operations"""
    cache_config = CacheConfig(enabled=True, directory="./test_cache")
    cache = TranslationCache(cache_config)
    
    # Test setting and getting
    text = "Teste de cache"
    translation = "Cache test"
    cache.set(text, translation, "test_engine")
    
    cached = cache.get(text, "test_engine")
    assert cached == translation
    
    # Test cache stats
    stats = cache.stats()
    assert stats["enabled"] is True
    assert stats["count"] == 1
    
    # Cleanup
    cache.clear()
    assert cache.stats()["count"] == 0

def test_translator():
    """Test translation functionality"""
    translator = MarianTranslator()
    
    # Test single translation
    text = "Olá, mundo!"
    translation = translator.translate(text)
    assert isinstance(translation, str)
    assert len(translation) > 0
    assert translation != text
    
    # Test batch translation
    texts = ["Primeiro", "Segundo", "Terceiro"]
    translations = translator.translate_batch(texts)
    assert len(translations) == len(texts)
    assert all(isinstance(t, str) for t in translations)
    assert all(len(t) > 0 for t in translations if t)
    
    # Test empty string handling
    empty_texts = ["", "Texto", ""]
    empty_translations = translator.translate_batch(empty_texts)
    assert len(empty_translations) == len(empty_texts)
    assert empty_translations[0] == ""
    assert empty_translations[2] == ""
    assert len(empty_translations[1]) > 0

def test_integration():
    """Test integration between components"""
    # Initialize components
    config = ConfigManager()
    cache_config = CacheConfig(
        enabled=config.config.cache.enabled,
        directory=config.config.cache.directory,
        max_size=config.config.cache.max_size
    )
    cache = TranslationCache(cache_config)
    translator = MarianTranslator()
    
    # Test translation with cache
    text = "Teste de integração"
    
    # First translation (should not be cached)
    translation1 = translator.translate(text)
    assert translation1 != text
    
    # Cache the result
    cache.set(text, translation1, "huggingface")
    
    # Second translation (should be cached)
    cached = cache.get(text, "huggingface")
    assert cached == translation1 