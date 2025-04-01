#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Term Manager module for EVA & GUARANI Translator.

This module provides functionality to manage technical terms during translation.
"""

import os
import json
import re
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

class TermManager:
    """Manager for technical terminology during translation."""
    
    def __init__(self, config):
        """Initialize the term manager with configuration.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Load technical terms dictionary
        self.terms = {}
        self.load_terms()
    
    def load_terms(self) -> bool:
        """Load technical terms from dictionary file.
        
        Returns:
            True if terms were loaded successfully, False otherwise
        """
        # Get dictionary file path from config
        dictionary_file = self.config.settings.get('terminology', {}).get('dictionary_file', None)
        
        if not dictionary_file:
            self.logger.warning("No dictionary file specified in config")
            return False
        
        # Check if path is absolute or relative
        if not os.path.isabs(dictionary_file):
            # Relative to the module directory
            module_dir = os.path.dirname(os.path.dirname(__file__))
            dictionary_file = os.path.join(module_dir, dictionary_file)
        
        if not os.path.exists(dictionary_file):
            self.logger.warning(f"Dictionary file not found: {dictionary_file}")
            return False
        
        try:
            with open(dictionary_file, 'r', encoding='utf-8') as f:
                self.terms = json.load(f)
            
            self.logger.info(f"Loaded {len(self.terms)} term categories from {dictionary_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error loading dictionary file: {str(e)}")
            return False
    
    def get_term_replacement(self, term: str, category: Optional[str] = None) -> Optional[str]:
        """Get the replacement for a term in the given category.
        
        Args:
            term: Term to replace
            category: Category to look in (optional)
            
        Returns:
            Replacement term or None if not found
        """
        # If category is specified, only look in that category
        if category and category in self.terms:
            category_terms = self.terms[category]
            if term in category_terms:
                return category_terms[term]
            return None
        
        # Otherwise, look in all categories
        for category_name, category_terms in self.terms.items():
            if term in category_terms:
                return category_terms[term]
        
        return None
    
    def apply_technical_terms(self, text: str) -> str:
        """Apply technical term replacements to text.
        
        Args:
            text: Text to process
            
        Returns:
            Processed text with technical terms replaced
        """
        if not self.terms:
            return text
        
        processed_text = text
        preserve_case = self.config.settings.get('terminology', {}).get('preserve_case', True)
        
        # Process each category
        for category, terms in self.terms.items():
            for pt_term, en_term in terms.items():
                # Skip empty terms
                if not pt_term or not en_term:
                    continue
                
                # Create pattern with word boundaries for whole-word replacement
                pattern = r'\b' + re.escape(pt_term) + r'\b'
                
                # Replace term
                if preserve_case:
                    # Case-preserving replacement
                    def replace_with_case(match):
                        matched = match.group(0)
                        if matched.islower():
                            return en_term.lower()
                        elif matched.isupper():
                            return en_term.upper()
                        elif matched[0].isupper() and matched[1:].islower():
                            return en_term[0].upper() + en_term[1:].lower()
                        else:
                            return en_term
                    
                    processed_text = re.sub(pattern, replace_with_case, processed_text, flags=re.IGNORECASE)
                else:
                    # Simple replacement
                    processed_text = re.sub(pattern, en_term, processed_text, flags=re.IGNORECASE)
        
        return processed_text
    
    def add_term(self, category: str, pt_term: str, en_term: str) -> bool:
        """Add a new term to the dictionary.
        
        Args:
            category: Category for the term
            pt_term: Portuguese term
            en_term: English term
            
        Returns:
            True if term was added successfully, False otherwise
        """
        if not category or not pt_term or not en_term:
            return False
        
        # Create category if it doesn't exist
        if category not in self.terms:
            self.terms[category] = {}
        
        # Add term
        self.terms[category][pt_term] = en_term
        
        # Save dictionary
        dictionary_file = self.config.settings.get('terminology', {}).get('dictionary_file', None)
        if dictionary_file:
            try:
                if not os.path.isabs(dictionary_file):
                    # Relative to the module directory
                    module_dir = os.path.dirname(os.path.dirname(__file__))
                    dictionary_file = os.path.join(module_dir, dictionary_file)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(dictionary_file), exist_ok=True)
                
                with open(dictionary_file, 'w', encoding='utf-8') as f:
                    json.dump(self.terms, f, ensure_ascii=False, indent=2)
                
                self.logger.info(f"Added term '{pt_term}' -> '{en_term}' to category '{category}'")
                return True
                
            except Exception as e:
                self.logger.error(f"Error saving term: {str(e)}")
                return False
        
        return True 