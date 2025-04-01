#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BIOS-Q Integration for EVA & GUARANI Translator.

This module provides integration between the BIOS-Q system and the
Translator module, enabling automatic translation of Portuguese content
to English throughout the system.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# Add parent directory to path to allow importing modules
parent_dir = str(Path(__file__).parent.parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from modules.translator_dev.translator import Translator
from modules.translator_dev.core.scanner import Scanner, ScanResult

# Set up logging
logger = logging.getLogger(__name__)

class BIOSQTranslatorIntegration:
    """Integration between BIOS-Q and the Translator module"""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize the BIOS-Q Translator integration
        
        Args:
            config_path: Path to the BIOS-Q configuration file
        """
        self.root_dir = Path("/c/Eva Guarani EGOS")
        
        # Load BIOS-Q configuration
        if config_path is None:
            config_path = self.root_dir / "BIOS-Q_backup" / "config" / "bios_q_config.json"
        
        self.config = self._load_config(config_path)
        
        # Initialize translator
        self.translator = Translator(verbose=True)
        
        # Initialize scanner
        self.scanner = Scanner()
        
        logger.info("BIOS-Q Translator integration initialized")
    
    def _load_config(self, config_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load BIOS-Q configuration
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            logger.info(f"Loaded BIOS-Q configuration from {config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading BIOS-Q configuration: {e}")
            return {}
    
    def translate_string(self, text: str, source_lang: str = "pt", target_lang: str = "en") -> str:
        """
        Translate a string
        
        Args:
            text: Text to translate
            source_lang: Source language (default: pt)
            target_lang: Target language (default: en)
            
        Returns:
            Translated text
        """
        # Get preferred engine from config
        engine = self._get_preferred_engine()
        
        # This is a simplified implementation - in reality, we would
        # call the appropriate translation engine directly
        
        # Check if text actually needs translation
        if not self._is_portuguese(text):
            return text
        
        # For now, we'll use a mock implementation
        # In a real implementation, we would use the actual translation engines
        translated = self._translate_with_engine(text, engine)
        
        logger.info(f"Translated string using {engine} engine")
        return translated
    
    def translate_file(self, file_path: Union[str, Path], output_dir: Optional[Union[str, Path]] = None) -> Optional[Path]:
        """
        Translate a file
        
        Args:
            file_path: Path to file to translate
            output_dir: Directory to save translated file
            
        Returns:
            Path to translated file or None if translation failed
        """
        file_path = Path(file_path)
        
        # Determine output directory
        if output_dir is None:
            output_dir = file_path.parent / "translated"
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create scan result with just this file
        scan_result = ScanResult(files=[str(file_path)], stats={})
        
        # Get preferred engine from config
        engine = self._get_preferred_engine()
        
        # Translate file
        result = self.translator.translate(
            scan_result,
            output_dir=str(output_dir),
            engine_name=engine
        )
        
        if result and result.get("files_processed", 0) > 0:
            output_path = Path(output_dir) / file_path.name
            logger.info(f"Translated file saved to {output_path}")
            return output_path
        
        logger.error(f"Failed to translate file {file_path}")
        return None
    
    def translate_directory(self, directory: Union[str, Path], output_dir: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """
        Translate all Portuguese files in a directory
        
        Args:
            directory: Directory to scan and translate
            output_dir: Directory to save translated files
            
        Returns:
            Dictionary with translation statistics
        """
        directory = Path(directory)
        
        # Determine output directory
        if output_dir is None:
            output_dir = directory.parent / "translated"
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Scan directory for Portuguese files
        scan_result = self.scanner.scan_directory(str(directory))
        
        if not scan_result.files:
            logger.info(f"No Portuguese files found in {directory}")
            return {"files_processed": 0}
        
        # Get preferred engine from config
        engine = self._get_preferred_engine()
        
        # Translate files
        result = self.translator.translate(
            scan_result,
            output_dir=str(output_dir),
            engine_name=engine
        )
        
        logger.info(f"Translated {result.get('files_processed', 0)} files from {directory} to {output_dir}")
        return result
    
    def _get_preferred_engine(self) -> str:
        """
        Get preferred translation engine from configuration
        
        Returns:
            Engine name (default: huggingface)
        """
        # Check if language configuration is present
        if "language" in self.config and "translation" in self.config["language"]:
            # Get preferred engine from configuration
            if "preferred_engine" in self.config["language"]["translation"]:
                return self.config["language"]["translation"]["preferred_engine"]
        
        # Default to HuggingFace
        return "huggingface"
    
    def _is_portuguese(self, text: str) -> bool:
        """
        Simple detection for Portuguese text
        
        Args:
            text: Text to analyze
            
        Returns:
            True if text is likely Portuguese, False otherwise
        """
        # Simple detection for Portuguese based on special characters
        pt_chars = {'ç', 'á', 'à', 'â', 'ã', 'õ', 'ê', 'é', 'í', 'ó', 'ú', 'ü'}
        
        # Count Portuguese characters
        pt_count = sum(1 for c in text.lower() if c in pt_chars)
        
        # If more than 3 Portuguese characters, consider it Portuguese
        if pt_count > 3:
            return True
            
        # Check for common Portuguese words
        pt_words = {
            ' de ', ' da ', ' do ', ' em ', ' no ', ' na ', ' um ', ' uma ', 
            ' que ', ' para ', ' com ', ' por ', ' os ', ' as ', ' é ', ' são '
        }
        
        # Count Portuguese words
        pt_word_count = sum(1 for word in pt_words if word in f" {text.lower()} ")
        
        # If more than 2 Portuguese words, consider it Portuguese
        if pt_word_count > 2:
            return True
            
        return False
    
    def _translate_with_engine(self, text: str, engine: str) -> str:
        """
        Translate text using the specified engine
        
        Args:
            text: Text to translate
            engine: Engine to use
            
        Returns:
            Translated text
        """
        try:
            # In a real implementation, we would call the actual translation engine
            # For now, we'll use a simplified implementation
            if engine == "openai":
                # Mock OpenAI translation
                return f"[OpenAI Translation] {text}"
            else:
                # Mock HuggingFace translation
                return f"[HF Translation] {text}"
                
        except Exception as e:
            logger.error(f"Error translating with {engine}: {e}")
            return text

def main():
    """Main entry point for BIOS-Q Translator integration"""
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(description="EVA & GUARANI BIOS-Q Translator Integration")
    
    # Add arguments
    parser.add_argument("--string", help="Translate a string")
    parser.add_argument("--file", help="Translate a file")
    parser.add_argument("--dir", help="Translate a directory")
    parser.add_argument("--output", help="Output directory for translated files")
    parser.add_argument("--config", help="Path to BIOS-Q configuration file")
    
    args = parser.parse_args()
    
    # Create integration
    integration = BIOSQTranslatorIntegration(config_path=args.config)
    
    # Translate string
    if args.string:
        translated = integration.translate_string(args.string)
        print(f"Original: {args.string}")
        print(f"Translated: {translated}")
        return
    
    # Translate file
    if args.file:
        result = integration.translate_file(args.file, output_dir=args.output)
        if result:
            print(f"Translated file saved to: {result}")
        else:
            print(f"Failed to translate file: {args.file}")
        return
    
    # Translate directory
    if args.dir:
        result = integration.translate_directory(args.dir, output_dir=args.output)
        print(f"Translated {result.get('files_processed', 0)} files")
        return
    
    # No action specified, show help
    parser.print_help()

if __name__ == "__main__":
    main() 