#!/usr/bin/env python3
"""
Translator - EVA & GUARANI Core Module
------------------------------------
This module implements the Translation system that provides
multilingual capabilities across all subsystems.

Version: 7.5
Created: 2025-03-26
"""

import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional, Set, Union, Sequence, cast
from datetime import datetime
import asyncio
from pathlib import Path

# Import Mycelium Network and Quantum Search
from .mycelium_network import mycelium
from .quantum_search import quantum_search

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("translator")

class TranslationMemory:
    """Manages translation memory and caching."""
    
    def __init__(self):
        self.memory: Dict[str, Dict[str, str]] = {}
        self.last_update = datetime.now()
        
    def add_translation(self, source_text: str, target_lang: str, translation: str) -> None:
        """Add a translation to memory."""
        if source_text not in self.memory:
            self.memory[source_text] = {}
        self.memory[source_text][target_lang] = translation
        self.last_update = datetime.now()
        
    def get_translation(self, source_text: str, target_lang: str) -> Optional[str]:
        """Retrieve a translation from memory."""
        return self.memory.get(source_text, {}).get(target_lang)
        
    def clear_memory(self) -> None:
        """Clear the translation memory."""
        self.memory.clear()
        self.last_update = datetime.now()

class Translator:
    """
    The Translation system that provides multilingual capabilities
    across all EVA & GUARANI subsystems.
    """
    
    def __init__(self):
        self.memory = TranslationMemory()
        self.supported_languages = {
            'en': 'English',
            'pt': 'Portuguese',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'nl': 'Dutch',
            'ru': 'Russian',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'hi': 'Hindi'
        }
        
        # Initialize Mycelium node
        self.node = mycelium.get_node("TRANSLATOR")
        if not self.node:
            self.node = mycelium.register_node("TRANSLATOR", "translation")
            
        # Connect to Quantum Search
        self._connect_to_quantum_search()
        
    def _connect_to_quantum_search(self) -> None:
        """Establish connection with Quantum Search system."""
        search_node = mycelium.get_node("QUANTUM_SEARCH")
        if search_node:
            mycelium.connect_nodes("TRANSLATOR", "QUANTUM_SEARCH")
            logger.info("Connected to Quantum Search system")
        else:
            logger.warning("Quantum Search system not found")
            
    async def translate(self, 
                       text: Union[str, Sequence[str]], 
                       target_lang: str,
                       source_lang: Optional[str] = None,
                       use_memory: bool = True,
                       propagate: bool = True) -> Union[str, List[str]]:
        """
        Translate text to target language.
        
        Args:
            text: Text or sequence of texts to translate
            target_lang: Target language code
            source_lang: Source language code (auto-detect if None)
            use_memory: Whether to use translation memory
            propagate: Whether to propagate translation through Mycelium
        """
        if target_lang not in self.supported_languages:
            raise ValueError(f"Unsupported target language: {target_lang}")
            
        # Handle sequence of texts
        if isinstance(text, (list, tuple)):
            translations = await asyncio.gather(*[
                self.translate(t, target_lang, source_lang, use_memory, False)
                for t in text
            ])
            return cast(List[str], translations)
            
        # At this point, text must be a string
        text_str = cast(str, text)
            
        # Check translation memory
        if use_memory:
            cached = self.memory.get_translation(text_str, target_lang)
            if cached:
                return cached
                
        # Perform translation
        translation = await self._translate_text(text_str, target_lang, source_lang)
        
        # Store in memory
        if use_memory:
            self.memory.add_translation(text_str, target_lang, translation)
            
        if propagate:
            # Propagate translation through Mycelium network
            translation_data = {
                "type": "translation",
                "source_text": text_str,
                "target_lang": target_lang,
                "translation": translation,
                "timestamp": datetime.now().isoformat()
            }
            
            try:
                # Ensure we await the propagation
                await mycelium.propagate_update("TRANSLATOR", translation_data)
                
                # Index translation in Quantum Search
                await self._index_translation(translation_data)
            except Exception as e:
                logger.error(f"Error propagating translation: {str(e)}")
            
        return translation
        
    async def _translate_text(self, 
                            text: str, 
                            target_lang: str,
                            source_lang: Optional[str] = None) -> str:
        """
        Perform actual translation.
        This is a placeholder implementation.
        """
        # In production, this would connect to a translation service
        # For now, we'll just append language code to demonstrate
        return f"{text} [{target_lang}]"
        
    async def _index_translation(self, translation_data: Dict[str, Any]) -> None:
        """Index translation in Quantum Search system."""
        try:
            metadata = {
                "type": "translation",
                "source_lang": "auto",  # We would detect this in production
                "target_lang": translation_data["target_lang"],
                "timestamp": translation_data["timestamp"]
            }
            
            # Add both source and translated text to search index
            await quantum_search.index.add_document(
                f"translation_{translation_data['timestamp']}",
                f"{translation_data['source_text']}\n{translation_data['translation']}",
                metadata
            )
            
        except Exception as e:
            logger.error(f"Error indexing translation: {str(e)}")
            
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages."""
        return self.supported_languages.copy()
        
    def get_stats(self) -> Dict[str, Any]:
        """Get translation system statistics."""
        return {
            "total_translations": len(self.memory.memory),
            "supported_languages": len(self.supported_languages),
            "last_update": self.memory.last_update.isoformat(),
            "connected_nodes": len(self.node.connections) if self.node else 0
        }

# Initialize the global translator
translator = Translator()

if __name__ == "__main__":
    # Test the translation system
    async def test_translation():
        print("\n✧༺❀༻∞ EVA & GUARANI - Translator Test ∞༺❀༻✧\n")
        
        # Test single translation
        text = "Hello, EVA & GUARANI!"
        target_lang = "pt"
        
        print(f"Translating: {text}")
        print(f"Target language: {target_lang}")
        
        translation = await translator.translate(text, target_lang)
        print(f"\nTranslation: {translation}")
        
        # Test batch translation
        texts = [
            "Quantum computing is the future",
            "Mycelial networks are amazing",
            "Neural networks learn patterns"
        ]
        
        print("\nBatch Translation:")
        translations = await translator.translate(texts, target_lang)
        
        for source, trans in zip(texts, translations):
            print(f"\nSource: {source}")
            print(f"Translation: {trans}")
            
        # Print stats
        stats = translator.get_stats()
        print(f"\nSystem Stats:")
        print(f"Total Translations: {stats['total_translations']}")
        print(f"Supported Languages: {stats['supported_languages']}")
        print(f"Last Update: {stats['last_update']}")
        print(f"Connected Nodes: {stats['connected_nodes']}")
        
        # Print supported languages
        print("\nSupported Languages:")
        for code, name in translator.get_supported_languages().items():
            print(f"- {code}: {name}")
            
        print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")
    
    # Run the test
    asyncio.run(test_translation()) 