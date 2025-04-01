#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Language detection scanner for EVA & GUARANI Translator.

This module provides functionality to scan files and directories for
Portuguese language content, determining which files need translation.
"""

import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field
import time

# Set up logging
logger = logging.getLogger(__name__)

# Try to import language detection libraries
try:
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    LANGID_AVAILABLE = True
    identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE)
    logger.info("Using py3langid for language detection")
except ImportError:
    LANGID_AVAILABLE = False
    identifier = None
    logging.warning("py3langid not available. Basic detection will be used.")

# Define Portuguese character patterns for basic detection
PORTUGUESE_CHARS = "áàâãéèêíìóòôõúùûçÁÀÂÃÉÈÊÍÌÓÒÔÕÚÙÛÇ"
PORTUGUESE_WORDS = [
    "não", "sim", "você", "eu", "ele", "ela", "nós", "eles", "elas",
    "obrigado", "obrigada", "porque", "também", "muito", "pouco",
    "para", "como", "quando", "onde", "quem", "qual", "quais", "até",
    "mais", "menos", "apenas", "agora", "hoje", "amanhã", "ontem",
    "sobre", "sob", "entre", "dentro", "fora", "antes", "depois",
    "primeiro", "último", "tudo", "nada", "algo", "alguém", "ninguém"
]

@dataclass
class ScanResult:
    """Results from scanning directories for files to translate"""
    files: List[str]
    stats: dict
    
class Scanner:
    """Scans directories for files to translate"""
    
    def __init__(self):
        """Initialize the scanner"""
        self.stats = {
            "total_files": 0,
            "skipped_files": 0,
            "scanned_files": 0,
            "detected_files": 0,
            "scan_time": 0.0
        }
        
        # Check if we have advanced language detection available
        self.has_advanced_detection = LANGID_AVAILABLE
    
    def scan_directory(self, directory: str, target_lang: str = "pt") -> ScanResult:
        """
        Scan a directory for files in the target language
        
        Args:
            directory: Directory to scan
            target_lang: Target language to detect (default: pt for Portuguese)
            
        Returns:
            ScanResult object with list of files in target language
        """
        start_time = time.time()
        
        # Reset statistics
        self.stats = {
            "total_files": 0,
            "skipped_files": 0,
            "scanned_files": 0,
            "detected_files": 0,
            "scan_time": 0.0
        }
        
        logger.info(f"Scanning directory: {directory}")
        
        target_files = []
        
        # Walk through directory
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                self.stats["total_files"] += 1
                
                # Skip binary files and other non-text files
                if not self._is_text_file(file_path):
                    self.stats["skipped_files"] += 1
                    continue
                    
                # Skip files that are too large
                if os.path.getsize(file_path) > 1024 * 1024:  # 1MB limit
                    logger.debug(f"Skipping large file: {file_path}")
                    self.stats["skipped_files"] += 1
                    continue
                
                # Detect language
                self.stats["scanned_files"] += 1
                detected_lang = self._detect_language(file_path)
                
                # If language matches target, add to list
                if detected_lang == target_lang:
                    logger.debug(f"Detected {target_lang} in file: {file_path}")
                    target_files.append(file_path)
                    self.stats["detected_files"] += 1
        
        # Update scan time
        self.stats["scan_time"] = time.time() - start_time
        
        logger.info(f"Scan completed in {self.stats['scan_time']:.2f}s")
        logger.info(f"Total files: {self.stats['total_files']}")
        logger.info(f"Skipped files: {self.stats['skipped_files']}")
        logger.info(f"Scanned files: {self.stats['scanned_files']}")
        logger.info(f"Detected files in {target_lang}: {self.stats['detected_files']}")
        
        return ScanResult(files=target_files, stats=self.stats)
    
    def _is_text_file(self, file_path: str) -> bool:
        """
        Check if a file is a text file
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if the file is a text file, False otherwise
        """
        # Skip files with binary extensions
        binary_extensions = {
            '.exe', '.dll', '.so', '.dylib', '.bin', '.dat', '.db', '.sqlite', '.pyc',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.ico',
            '.mp3', '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wav', '.ogg',
            '.zip', '.tar', '.gz', '.bz2', '.7z', '.rar',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
        }
        
        _, ext = os.path.splitext(file_path.lower())
        if ext in binary_extensions:
            return False
            
        return True
    
    def _detect_language(self, file_path: str) -> Optional[str]:
        """
        Detect the language of a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            ISO language code or None if detection failed
        """
        try:
            # Read the first 4KB of the file for language detection
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(4096)
                
            # Skip if file is too short
            if len(content.strip()) < 20:
                logger.debug(f"Skipping short file: {file_path}")
                return None
                
            # Use best available language detection method
            if LANGID_AVAILABLE and identifier:
                try:
                    lang, _ = identifier.classify(content)
                    return lang
                except Exception as e:
                    logger.warning(f"Error using py3langid: {e}")
                    # Fall back to basic detection
            
            # Basic language detection
            return self._basic_detect_language(content)
            
        except Exception as e:
            logger.warning(f"Error detecting language in {file_path}: {e}")
            return None
    
    def _basic_detect_language(self, text: str) -> Optional[str]:
        """
        Basic language detection based on character frequency
        
        Args:
            text: Text to detect language
            
        Returns:
            Language code or None if detection failed
        """
        # Simple detection for Portuguese based on special characters
        pt_chars = {'ç', 'á', 'à', 'â', 'ã', 'õ', 'ê', 'é', 'í', 'ó', 'ú', 'ü'}
        
        # Count Portuguese characters
        pt_count = sum(1 for c in text.lower() if c in pt_chars)
        
        # If more than 5 Portuguese characters, consider it Portuguese
        if pt_count > 5:
            return "pt"
            
        # Check for common Portuguese words
        pt_words = {
            ' de ', ' da ', ' do ', ' em ', ' no ', ' na ', ' um ', ' uma ', 
            ' que ', ' para ', ' com ', ' por ', ' os ', ' as ', ' é ', ' são '
        }
        
        # Count Portuguese words
        pt_word_count = sum(1 for word in pt_words if word in text.lower())
        
        # If more than 3 Portuguese words, consider it Portuguese
        if pt_word_count > 3:
            return "pt"
            
        return None 