#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Translation processor for EVA & GUARANI Translator.

This module provides functionality to process and translate files,
handling different file types and using multiple translation engines.
"""

import os
import logging
import time
import threading
import re
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path

from .cache import TranslationCache

# Set up logging
logger = logging.getLogger(__name__)


class TranslationProcessor:
    """Processor for translating files"""

    def __init__(self, cache: TranslationCache):
        """
        Initialize the translation processor

        Args:
            cache: Translation cache instance
        """
        self.cache = cache
        self.stats = {
            "files_processed": 0,
            "total_chars": 0,
            "total_time": 0.0,
            "cache_hits": 0,
            "api_calls": 0,
        }

        # For demonstration only - we're not actually implementing the engines
        # In a real implementation, these would be loaded dynamically
        self.engines = {
            "huggingface": self._mock_huggingface_translate,
            "openai": self._mock_openai_translate,
        }

        # File type specific handlers
        self.handlers = {
            ".md": self._handle_markdown,
            ".html": self._handle_html,
            ".json": self._handle_json,
            ".py": self._handle_code,
            ".js": self._handle_code,
            ".java": self._handle_code,
            ".txt": self._handle_text,
            # Default handler
            "default": self._handle_text,
        }

    def translate_files(
        self,
        files: List[str],
        output_dir: Optional[str] = None,
        engine_name: str = "huggingface",
        workers: int = 2,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> Dict[str, Any]:
        """
        Translate a list of files

        Args:
            files: List of file paths to translate
            output_dir: Directory to save translated files
            engine_name: Translation engine to use
            workers: Number of worker threads
            progress_callback: Optional callback function to report progress

        Returns:
            Dictionary with translation statistics
        """
        if not files:
            logger.warning("No files to translate")
            return self.stats

        start_time = time.time()

        # Reset statistics
        self.stats = {
            "files_processed": 0,
            "total_chars": 0,
            "total_time": 0.0,
            "cache_hits": 0,
            "api_calls": 0,
            "engine": engine_name,
        }

        # Create output directory if specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Get translation engine
        if engine_name not in self.engines:
            logger.error(f"Unknown translation engine: {engine_name}")
            return self.stats

        engine = self.engines[engine_name]

        # Use thread pool for concurrent processing
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Define the worker function
            def translate_file_worker(file_index_and_path):
                file_index, file_path = file_index_and_path
                try:
                    success = self._translate_file(file_path, engine, output_dir)
                    # Call progress callback if provided
                    if progress_callback:
                        progress_callback(file_index)
                    return success
                except Exception as e:
                    logger.error(f"Error translating file {file_path}: {e}")
                    # Still call progress callback to update progress
                    if progress_callback:
                        progress_callback(file_index)
                    return False

            # Submit all files for translation with their index
            file_index_and_paths = [(i, file_path) for i, file_path in enumerate(files)]
            results = list(executor.map(translate_file_worker, file_index_and_paths))

        # Update statistics
        self.stats["files_processed"] = sum(1 for r in results if r)
        self.stats["total_time"] = time.time() - start_time

        return self.stats

    def _translate_file(
        self, file_path: str, translate_fn: Callable, output_dir: Optional[str] = None
    ) -> bool:
        """
        Translate a single file

        Args:
            file_path: Path to file to translate
            translate_fn: Translation function to use
            output_dir: Directory to save translated file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Update statistics
            self.stats["total_chars"] += len(content)

            # Get file extension
            file_ext = os.path.splitext(file_path)[1].lower()

            # Select appropriate handler for file type
            handler = self.handlers.get(file_ext, self.handlers["default"])

            # Process with the appropriate handler
            translated_content = handler(content, translate_fn)

            # Write translated file
            if output_dir:
                # Create output file path
                rel_path = os.path.relpath(file_path)
                output_path = os.path.join(output_dir, rel_path)

                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Write translated content
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(translated_content)

                logger.info(f"Translated file saved: {output_path}")

            return True

        except Exception as e:
            logger.error(f"Error translating file {file_path}: {e}")
            return False

    # File type specific handlers

    def _handle_markdown(self, content: str, translate_fn: Callable) -> str:
        """
        Handle Markdown file translation

        Args:
            content: File content
            translate_fn: Translation function

        Returns:
            Translated content
        """
        # Split content into blocks
        blocks = re.split(r"(```.*?```|`.*?`)", content, flags=re.DOTALL)

        for i in range(len(blocks)):
            # Skip code blocks (odd indices after split)
            if i % 2 == 0:
                # Check cache
                cached = self.cache.get(blocks[i], "markdown")
                if cached:
                    self.stats["cache_hits"] += 1
                    blocks[i] = cached
                else:
                    # Translate text blocks
                    self.stats["api_calls"] += 1
                    blocks[i] = translate_fn(blocks[i])
                    # Cache translation
                    self.cache.set(blocks[i], blocks[i], "markdown")

        # Join blocks back together
        return "".join(blocks)

    def _handle_html(self, content: str, translate_fn: Callable) -> str:
        """
        Handle HTML file translation

        Args:
            content: File content
            translate_fn: Translation function

        Returns:
            Translated content
        """
        # For simplicity, we'll just use a basic approach here
        # In a real implementation, we would use BeautifulSoup

        # Split by tags
        blocks = re.split(r"(<[^>]*>)", content)

        for i in range(len(blocks)):
            # Skip tags
            if not blocks[i].startswith("<") and blocks[i].strip():
                # Check cache
                cached = self.cache.get(blocks[i], "html")
                if cached:
                    self.stats["cache_hits"] += 1
                    blocks[i] = cached
                else:
                    # Translate text blocks
                    self.stats["api_calls"] += 1
                    blocks[i] = translate_fn(blocks[i])
                    # Cache translation
                    self.cache.set(blocks[i], blocks[i], "html")

        # Join blocks back together
        return "".join(blocks)

    def _handle_json(self, content: str, translate_fn: Callable) -> str:
        """
        Handle JSON file translation

        Args:
            content: File content
            translate_fn: Translation function

        Returns:
            Translated content
        """
        # For demonstration, we'll just translate the whole file
        # In a real implementation, we would parse the JSON and translate values

        # Check cache
        cached = self.cache.get(content, "json")
        if cached:
            self.stats["cache_hits"] += 1
            return cached

        # Translate content
        self.stats["api_calls"] += 1
        translated = translate_fn(content)

        # Cache translation
        self.cache.set(content, translated, "json")

        return translated

    def _handle_code(self, content: str, translate_fn: Callable) -> str:
        """
        Handle code file translation (comments only)

        Args:
            content: File content
            translate_fn: Translation function

        Returns:
            Translated content
        """
        # Split by line
        lines = content.split("\n")

        for i in range(len(lines)):
            # Try to identify comments
            comment_match = re.search(r"(#|\/\/|\/\*|\*)\s*(.*)", lines[i])
            if comment_match:
                comment_text = comment_match.group(2)
                comment_prefix = comment_match.group(1)

                if comment_text.strip():
                    # Check cache
                    cached = self.cache.get(comment_text, "code")
                    if cached:
                        self.stats["cache_hits"] += 1
                        translated_comment = cached
                    else:
                        # Translate comment
                        self.stats["api_calls"] += 1
                        translated_comment = translate_fn(comment_text)
                        # Cache translation
                        self.cache.set(comment_text, translated_comment, "code")

                    # Replace comment in line
                    lines[i] = lines[i].replace(comment_text, translated_comment)

        # Join lines back together
        return "\n".join(lines)

    def _handle_text(self, content: str, translate_fn: Callable) -> str:
        """
        Handle plain text file translation

        Args:
            content: File content
            translate_fn: Translation function

        Returns:
            Translated content
        """
        # Check cache
        cached = self.cache.get(content, "text")
        if cached:
            self.stats["cache_hits"] += 1
            return cached

        # Translate content
        self.stats["api_calls"] += 1
        translated = translate_fn(content)

        # Cache translation
        self.cache.set(content, translated, "text")

        return translated

    # Mock translation engines for demonstration
    def _mock_huggingface_translate(self, text: str) -> str:
        """
        Mock HuggingFace translation engine

        Args:
            text: Text to translate

        Returns:
            Translated text
        """
        # Simulate translation by adding a prefix
        translated_text = f"[HF TRANSLATION] {text}"

        # Add a small delay to simulate processing time
        time.sleep(0.1)

        return translated_text

    def _mock_openai_translate(self, text: str) -> str:
        """
        Mock OpenAI translation engine

        Args:
            text: Text to translate

        Returns:
            Translated text
        """
        # Simulate translation by adding a prefix
        translated_text = f"[OPENAI TRANSLATION] {text}"

        # Add a small delay to simulate processing time
        time.sleep(0.2)

        return translated_text
