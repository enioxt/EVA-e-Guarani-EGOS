#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Marian MT translation engine for EVA & GUARANI Translator.

This module provides a translation engine using Hugging Face's Marian MT models.
"""

import os
import logging
from typing import Dict, Any, Optional

class MarianTranslator:
    """Marian MT translation engine using Hugging Face Transformers."""
    
    def __init__(self, config):
        """Initialize the translator with configuration.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get model configuration
        self.model_name = config.settings.get('huggingface', {}).get('model', 'Helsinki-NLP/opus-mt-pt-en')
        self.max_tokens = config.settings.get('huggingface', {}).get('max_tokens', 4096)
        self.temperature = config.settings.get('huggingface', {}).get('temperature', 0.3)
        
        # Initialize translator
        self.model = None
        self.tokenizer = None
        self._initialize_model()
    
    def _initialize_model(self) -> None:
        """Initialize the translation model."""
        try:
            from transformers import MarianMTModel, MarianTokenizer
            
            # Load tokenizer and model
            self.logger.info(f"Loading Marian MT model: {self.model_name}")
            
            # Check for local model first
            local_model_path = os.path.join(
                os.path.dirname(__file__),
                'models',
                os.path.basename(self.model_name)
            )
            
            if os.path.exists(local_model_path):
                self.logger.info(f"Using local model at {local_model_path}")
                self.tokenizer = MarianTokenizer.from_pretrained(local_model_path)
                self.model = MarianMTModel.from_pretrained(local_model_path)
            else:
                self.logger.info(f"Downloading model from Hugging Face")
                self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
                self.model = MarianMTModel.from_pretrained(self.model_name)
                
            self.logger.info("Model loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing Marian MT model: {str(e)}")
            raise
    
    def translate(self, text: str) -> str:
        """Translate text from Portuguese to English.
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text
        
        if not self.model or not self.tokenizer:
            self.logger.error("Model not initialized")
            return text
        
        try:
            # Split text into chunks to avoid exceeding token limit
            chunks = self._split_into_chunks(text)
            translated_chunks = []
            
            for chunk in chunks:
                # Translate chunk
                inputs = self.tokenizer(chunk, return_tensors="pt", padding=True)
                
                # Generate translation
                translated = self.model.generate(
                    **inputs,
                    max_length=self.max_tokens,
                    num_beams=4,
                    temperature=self.temperature,
                    early_stopping=True
                )
                
                # Decode translation
                translated_text = self.tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
                translated_chunks.append(translated_text)
            
            # Join chunks
            return " ".join(translated_chunks)
            
        except Exception as e:
            self.logger.error(f"Error translating text: {str(e)}")
            return text
    
    def translate_file_content(self, content: str, file_path: Optional[str] = None, file_ext: Optional[str] = None) -> str:
        """Translate file content, with format-specific handling.
        
        Args:
            content: Content to translate
            file_path: Path to the file (optional)
            file_ext: File extension (optional)
            
        Returns:
            Translated content
        """
        if not content or not content.strip():
            return content
        
        # Determine file type from extension if provided
        if file_ext and file_ext.startswith('.'):
            file_ext = file_ext[1:]
            
        if not file_ext and file_path:
            file_ext = os.path.splitext(file_path)[1].lstrip('.')
        
        # Apply format-specific handling
        if file_ext in ['md', 'markdown']:
            return self._translate_markdown(content)
        elif file_ext in ['html', 'htm', 'xml']:
            return self._translate_html(content)
        elif file_ext in ['json', 'yaml', 'yml']:
            return self._translate_structured(content, file_ext)
        else:
            # Default translation
            return self.translate(content)
    
    def _split_into_chunks(self, text: str, max_chunk_size: int = 512) -> list:
        """Split text into chunks for translation.
        
        Args:
            text: Text to split
            max_chunk_size: Maximum chunk size in characters
            
        Returns:
            List of text chunks
        """
        # Simple splitting by sentences
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                chunks.append(current_chunk)
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _translate_markdown(self, content: str) -> str:
        """Translate Markdown content preserving formatting.
        
        Args:
            content: Markdown content
            
        Returns:
            Translated Markdown content
        """
        # Simple implementation - translate entire content
        # A more sophisticated implementation would parse and translate parts separately
        return self.translate(content)
    
    def _translate_html(self, content: str) -> str:
        """Translate HTML content preserving tags.
        
        Args:
            content: HTML content
            
        Returns:
            Translated HTML content
        """
        # Simple implementation - translate entire content
        # A more sophisticated implementation would parse and translate only text nodes
        return self.translate(content)
    
    def _translate_structured(self, content: str, format_type: str) -> str:
        """Translate structured content like JSON or YAML.
        
        Args:
            content: Structured content
            format_type: Format type ('json', 'yaml', etc.)
            
        Returns:
            Translated structured content
        """
        # Simple implementation - translate entire content
        # A more sophisticated implementation would parse and translate only string values
        return self.translate(content) 