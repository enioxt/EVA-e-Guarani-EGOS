#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Term Manager for handling technical terminology during translation
"""

import os
import json
import re
import logging
from typing import Dict, List, Optional, Union, Tuple, Set
from pathlib import Path

# Setup logging
logger = logging.getLogger("term_manager")

class TermManager:
    """Manager for technical terminology handling during translation"""
    
    def __init__(self, terms_file: Optional[Union[str, Path]] = None):
        """Initialize the term manager
        
        Args:
            terms_file: Path to the JSON file with technical terms
        """
        self.terms_file = terms_file or os.path.join(os.path.dirname(__file__), 
                                                 '..', 'config', 'technical_terms.json')
        self.pt_to_en: Dict[str, str] = {}
        self.en_to_pt: Dict[str, str] = {}
        self.terms_by_category: Dict[str, Dict[str, List[str]]] = {}
        self.version = "1.0"
        self.load_terms()
    
    def load_terms(self) -> bool:
        """Load technical terms from JSON file
        
        Returns:
            True if terms were loaded successfully
        """
        try:
            if not os.path.exists(self.terms_file):
                logger.warning(f"Technical terms file not found: {self.terms_file}")
                return False
            
            with open(self.terms_file, 'r', encoding='utf-8') as f:
                terms_data = json.load(f)
            
            # Store version
            self.version = terms_data.get("version", "1.0")
            
            # Reset mappings
            self.pt_to_en = {}
            self.en_to_pt = {}
            self.terms_by_category = terms_data.get("terms", {})
            
            # Process each category
            for category, term_lists in self.terms_by_category.items():
                pt_terms = term_lists.get("portuguese", [])
                en_terms = term_lists.get("english", [])
                
                # Create mappings only for matching pairs
                for i, pt_term in enumerate(pt_terms):
                    if i < len(en_terms):
                        en_term = en_terms[i]
                        self.pt_to_en[pt_term.lower()] = en_term
                        self.en_to_pt[en_term.lower()] = pt_term
            
            logger.info(f"Loaded {len(self.pt_to_en)} technical terms from {self.terms_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading technical terms: {str(e)}")
            return False
    
    def get_term_translations(self, language: str = "pt", category: Optional[str] = None) -> Dict[str, str]:
        """Get term translations from one language to another
        
        Args:
            language: Source language ('pt' for Portuguese, 'en' for English)
            category: Category of terms to get (or None for all)
            
        Returns:
            Dictionary mapping terms from source language to target language
        """
        if language.lower() == "pt":
            # Portuguese to English
            if category:
                # Filter by category
                result = {}
                if category in self.terms_by_category:
                    pt_terms = self.terms_by_category[category].get("portuguese", [])
                    en_terms = self.terms_by_category[category].get("english", [])
                    
                    for i, pt_term in enumerate(pt_terms):
                        if i < len(en_terms):
                            result[pt_term.lower()] = en_terms[i]
                
                return result
            else:
                # All mappings
                return self.pt_to_en
        else:
            # English to Portuguese
            if category:
                # Filter by category
                result = {}
                if category in self.terms_by_category:
                    pt_terms = self.terms_by_category[category].get("portuguese", [])
                    en_terms = self.terms_by_category[category].get("english", [])
                    
                    for i, en_term in enumerate(en_terms):
                        if i < len(pt_terms):
                            result[en_term.lower()] = pt_terms[i]
                
                return result
            else:
                # All mappings
                return self.en_to_pt
    
    def add_term(self, pt_term: str, en_term: str, category: str) -> bool:
        """Add a new term pair to the dictionary
        
        Args:
            pt_term: Portuguese term
            en_term: English term
            category: Category for the term
            
        Returns:
            True if term was added successfully
        """
        try:
            # Ensure the category exists
            if category not in self.terms_by_category:
                self.terms_by_category[category] = {
                    "portuguese": [],
                    "english": []
                }
            
            # Add to category lists
            self.terms_by_category[category]["portuguese"].append(pt_term)
            self.terms_by_category[category]["english"].append(en_term)
            
            # Add to mappings
            self.pt_to_en[pt_term.lower()] = en_term
            self.en_to_pt[en_term.lower()] = pt_term
            
            # Save to file
            return self.save_terms()
            
        except Exception as e:
            logger.error(f"Error adding term: {str(e)}")
            return False
    
    def save_terms(self) -> bool:
        """Save terms to JSON file
        
        Returns:
            True if terms were saved successfully
        """
        try:
            data = {
                "version": self.version,
                "description": "Dictionary of technical terms for EVA & GUARANI Translator project",
                "terms": self.terms_by_category
            }
            
            with open(self.terms_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(self.pt_to_en)} technical terms to {self.terms_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving technical terms: {str(e)}")
            return False
    
    def preprocess_text(self, text: str, language: str = "pt") -> Tuple[str, Dict[str, str]]:
        """Preprocess text to replace technical terms with placeholders
        
        Args:
            text: Text to preprocess
            language: Source language ('pt' for Portuguese, 'en' for English)
            
        Returns:
            Tuple of (processed_text, placeholder_map)
        """
        # Get appropriate term mapping
        if language.lower() == "pt":
            term_map = self.pt_to_en
        else:
            term_map = self.en_to_pt
        
        # Sort terms by length (longest first) to avoid partial matches
        sorted_terms = sorted(term_map.keys(), key=len, reverse=True)
        
        placeholder_map = {}
        processed_text = text
        
        # Replace each term with a placeholder
        for i, term in enumerate(sorted_terms):
            placeholder = f"__TECH_TERM_{i}__"
            
            # Use word boundary regex to avoid partial matches
            pattern = r'\b' + re.escape(term) + r'\b'
            if re.search(pattern, processed_text, re.IGNORECASE):
                processed_text = re.sub(pattern, placeholder, processed_text, flags=re.IGNORECASE)
                placeholder_map[placeholder] = term_map[term]
        
        return processed_text, placeholder_map
    
    def postprocess_text(self, text: str, placeholder_map: Dict[str, str]) -> str:
        """Restore technical terms from placeholders
        
        Args:
            text: Text with placeholders
            placeholder_map: Map of placeholders to terms
            
        Returns:
            Text with restored terms
        """
        processed_text = text
        
        # Replace each placeholder with its term
        for placeholder, term in placeholder_map.items():
            processed_text = processed_text.replace(placeholder, term)
        
        return processed_text
    
    def apply_terminology(self, text: str, source_lang: str = "pt", target_lang: str = "en") -> str:
        """Apply terminology rules to a translated text
        
        This is used after translation to correct any terms that weren't
        properly handled during translation
        
        Args:
            text: Translated text
            source_lang: Source language
            target_lang: Target language
            
        Returns:
            Text with consistent terminology
        """
        # Determine the correct term mapping
        if source_lang.lower() == "pt" and target_lang.lower() == "en":
            # Looking for English terms that should be used
            term_map = self.pt_to_en
        elif source_lang.lower() == "en" and target_lang.lower() == "pt":
            # Looking for Portuguese terms that should be used
            term_map = self.en_to_pt
        else:
            # Unsupported language combination
            return text
        
        # Apply each term correction
        for source_term, target_term in term_map.items():
            # Create a regex pattern for matching variations of the term
            pattern = r'\b' + re.escape(target_term) + r'\b'
            
            # Replace with the correct term
            text = re.sub(pattern, target_term, text, flags=re.IGNORECASE)
        
        return text 