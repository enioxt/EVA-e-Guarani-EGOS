#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from modules.translator_dev.config.config import ConfigManager
from modules.translator_dev.core.cache import TranslationCache, CacheConfig
from modules.translator_dev.engines.huggingface.marian_engine import MarianTranslator


def main():
    # Initialize configuration
    config = ConfigManager()

    # Initialize cache with correct config
    cache_config = CacheConfig(
        enabled=config.config.cache.enabled,
        directory=config.config.cache.directory,
        max_size=config.config.cache.max_size,
    )
    cache = TranslationCache(cache_config)

    # Initialize translator
    translator = MarianTranslator()

    # Example text in Portuguese
    text = """
    Este é um exemplo de texto em português que será traduzido para inglês.
    O tradutor deve preservar a formatação e a estrutura do texto.
    """

    # Check cache first
    cached_translation = cache.get(text, "huggingface")
    if cached_translation:
        print("Using cached translation:")
        print(cached_translation)
    else:
        # Translate text
        translation = translator.translate(text)

        # Cache the result
        cache.set(text, translation, "huggingface")

        print("New translation:")
        print(translation)

    # Example with batch translation
    texts = [
        "Primeiro texto para tradução.",
        "",  # Empty string should be preserved
        "Segundo texto para tradução.",
        "Terceiro texto para tradução.",
    ]

    print("\nBatch translation:")
    translations = translator.translate_batch(texts)
    for original, translated in zip(texts, translations):
        print(f"\nOriginal: {original}")
        print(f"Translated: {translated}")

    # Print cache statistics
    print("\nCache statistics:")
    stats = cache.stats()
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
