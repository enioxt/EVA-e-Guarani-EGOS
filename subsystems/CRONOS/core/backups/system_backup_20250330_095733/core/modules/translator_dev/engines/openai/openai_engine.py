#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenAI translation engine for EVA & GUARANI Translator.

This module provides a translation engine using OpenAI's API for translation.
"""

import os
import re
import json
import logging
from typing import Dict, Any, Optional, List
import time

class OpenAITranslator:
    """OpenAI translation engine."""
    
    def __init__(self, config):
        """Initialize the translator with configuration.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get API configuration
        self.model = config.settings.get('openai', {}).get('model', 'gpt-3.5-turbo')
        self.max_tokens = config.settings.get('openai', {}).get('max_tokens', 1000)
        self.temperature = config.settings.get('openai', {}).get('temperature', 0.3)
        self.budget = config.settings.get('openai', {}).get('max_budget', 5.0)
        
        # Cost monitoring
        self.cost_spent = 0.0
        self.total_tokens = 0
        
        # Initialize OpenAI
        self._initialize_api()
        
        # Check if term manager is available
        self.term_manager = None
        if (hasattr(config, 'settings') and 
            config.settings.get('terminology', {}).get('enabled', True)):
            try:
                from ...core.term_manager import TermManager
                self.term_manager = TermManager(config)
                self.logger.info("Term manager initialized for OpenAI translator")
            except Exception as e:
                self.logger.warning(f"Failed to initialize term manager: {str(e)}")
    
    def _initialize_api(self) -> None:
        """Initialize the OpenAI API."""
        try:
            import openai
            
            # Check for API key
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                api_key = self.config.settings.get('openai', {}).get('api_key')
            
            if not api_key:
                self.logger.warning("No OpenAI API key found. Please set OPENAI_API_KEY environment variable or configure it in settings.")
            
            # Initialize the client
            self.client = openai.OpenAI(api_key=api_key)
            self.logger.info(f"OpenAI API initialized with model {self.model}")
            
        except ImportError:
            self.logger.error("OpenAI package not installed. Please install it with 'pip install openai'")
            raise
        except Exception as e:
            self.logger.error(f"Error initializing OpenAI API: {str(e)}")
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
        
        # Apply terminology replacement before translation if available
        preprocessed_text = text
        if self.term_manager:
            try:
                # Apply technical term replacements
                preprocessed_text = self.term_manager.apply_technical_terms(text)
            except Exception as e:
                self.logger.warning(f"Error applying technical terms: {str(e)}")
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional translator. Translate the following Portuguese text to English. Maintain the same formatting and style. Keep technical terms intact."},
                    {"role": "user", "content": preprocessed_text}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            # Extract result
            translated_text = response.choices[0].message.content.strip()
            
            # Update cost tracking
            if hasattr(response, 'usage') and hasattr(response.usage, 'total_tokens'):
                self.total_tokens += response.usage.total_tokens
                # Approximate cost calculation (will depend on the model)
                if self.model.startswith('gpt-4'):
                    cost_per_1k_input = 0.03
                    cost_per_1k_output = 0.06
                else:  # gpt-3.5-turbo
                    cost_per_1k_input = 0.0015
                    cost_per_1k_output = 0.002
                
                # Calculate cost
                prompt_tokens = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens
                prompt_cost = (prompt_tokens / 1000) * cost_per_1k_input
                completion_cost = (completion_tokens / 1000) * cost_per_1k_output
                usage_cost = prompt_cost + completion_cost
                
                self.cost_spent += usage_cost
                
                # Check budget
                if self.budget > 0 and self.cost_spent > self.budget:
                    self.logger.warning(f"Budget exceeded: ${self.cost_spent:.2f} spent (limit: ${self.budget:.2f})")
            
            return translated_text
            
        except Exception as e:
            self.logger.error(f"Error translating text with OpenAI: {str(e)}")
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
        elif file_ext in ['py', 'js', 'java', 'c', 'cpp', 'cs']:
            return self._translate_code(content, file_ext)
        else:
            # Default translation
            return self.translate(content)
    
    def _translate_markdown(self, content: str) -> str:
        """Translate Markdown content preserving formatting.
        
        Args:
            content: Markdown content
            
        Returns:
            Translated Markdown content
        """
        try:
            # Use a specialized prompt for Markdown
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional translator specialized in Markdown documents. Translate the following Portuguese text to English. Carefully preserve all Markdown formatting, links, code blocks, headers, and other syntax elements. Do not translate text inside code blocks or code spans."},
                    {"role": "user", "content": content}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            # Extract result
            translated_text = response.choices[0].message.content.strip()
            return translated_text
        except Exception as e:
            self.logger.error(f"Error translating Markdown: {str(e)}")
            return self.translate(content)
    
    def _translate_html(self, content: str) -> str:
        """Translate HTML content preserving tags.
        
        Args:
            content: HTML content
            
        Returns:
            Translated HTML content
        """
        try:
            # Try to use BeautifulSoup for better HTML handling
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Function to process text nodes
            def process_text_nodes(node):
                if node.name in ['script', 'style']:
                    return  # Skip script and style tags
                
                if node.string and node.string.strip():
                    # Translate text node
                    original_text = node.string
                    translated_text = self.translate(original_text)
                    node.string.replace_with(translated_text)
                
                # Process child nodes
                for child in node.children:
                    if child.name:  # If it's a tag
                        process_text_nodes(child)
            
            # Process all text nodes
            process_text_nodes(soup)
            
            # Return translated HTML
            return str(soup)
            
        except ImportError:
            self.logger.warning("BeautifulSoup not installed, falling back to basic HTML translation")
            
            # Use a specialized prompt for HTML
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional translator specialized in HTML documents. Translate the following Portuguese text to English. Carefully preserve all HTML tags, attributes, and structure. Do not translate tag names, attribute names, or values of attributes like 'class', 'id', 'href', etc. Only translate human-readable text content."},
                    {"role": "user", "content": content}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            # Extract result
            translated_text = response.choices[0].message.content.strip()
            return translated_text
        except Exception as e:
            self.logger.error(f"Error translating HTML: {str(e)}")
            return self.translate(content)
    
    def _translate_structured(self, content: str, format_type: str) -> str:
        """Translate structured content like JSON or YAML.
        
        Args:
            content: Structured content
            format_type: Format type ('json', 'yaml', etc.)
            
        Returns:
            Translated structured content
        """
        try:
            if format_type == 'json':
                # Parse JSON
                data = json.loads(content)
                
                # Function to recursively translate string values
                def translate_json_values(obj):
                    if isinstance(obj, str) and obj.strip():
                        return self.translate(obj)
                    elif isinstance(obj, list):
                        return [translate_json_values(item) for item in obj]
                    elif isinstance(obj, dict):
                        return {k: translate_json_values(v) for k, v in obj.items()}
                    else:
                        return obj
                
                # Translate values
                translated_data = translate_json_values(data)
                
                # Serialize back to JSON
                return json.dumps(translated_data, ensure_ascii=False, indent=4)
                
            else:
                # Use a specialized prompt for YAML
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are a professional translator specialized in {format_type.upper()} documents. Translate the following Portuguese text to English. Carefully preserve all {format_type.upper()} structure, indentation, and syntax. Only translate string values, not keys or structural elements."},
                        {"role": "user", "content": content}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                
                # Extract result
                translated_text = response.choices[0].message.content.strip()
                return translated_text
                
        except Exception as e:
            self.logger.error(f"Error translating {format_type}: {str(e)}")
            return self.translate(content)
    
    def _translate_code(self, content: str, language: str) -> str:
        """Translate code comments while preserving code.
        
        Args:
            content: Code content
            language: Programming language
            
        Returns:
            Translated code content
        """
        try:
            # Use a specialized prompt for code
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a professional translator specialized in {language} code. Translate ONLY the comments from Portuguese to English. Do not modify any code, variable names, function names, or other code elements. Preserve the exact structure, indentation, and formatting of the original code."},
                    {"role": "user", "content": content}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            # Extract result
            translated_text = response.choices[0].message.content.strip()
            return translated_text
            
        except Exception as e:
            self.logger.error(f"Error translating code: {str(e)}")
            return content  # Return original for code to be safe
    
    def get_cost_stats(self) -> Dict[str, Any]:
        """Get cost statistics.
        
        Returns:
            Dictionary with cost statistics
        """
        return {
            'total_tokens': self.total_tokens,
            'cost_spent': self.cost_spent,
            'budget': self.budget,
            'budget_remaining': max(0, self.budget - self.cost_spent) if self.budget > 0 else None,
            'budget_exceeded': self.budget > 0 and self.cost_spent > self.budget,
            'model': self.model
        } 