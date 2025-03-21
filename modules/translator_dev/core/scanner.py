#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File scanner for detecting Portuguese content in files
"""

import os
import logging
import re
import json
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional, Union
from dataclasses import dataclass
import shutil

# Import language detection library
try:
    from langdetect import detect, DetectorFactory, LangDetectException
    # Set seed for consistent results
    DetectorFactory.seed = 0
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

# Setup logging
logger = logging.getLogger("scanner")

# Portuguese words commonly found in code and documentation
PORTUGUESE_KEYWORDS = {
    'função', 'variável', 'classe', 'método', 'objeto', 'arquivo', 'retorno',
    'para', 'enquanto', 'faça', 'senão', 'como', 'portanto', 'então', 'lista',
    'dicionário', 'conjunto', 'tupla', 'inteiro', 'flutuante', 'texto', 'verdadeiro',
    'falso', 'nulo', 'este', 'aquele', 'estes', 'aqueles', 'cada', 'todos', 'nenhum',
    'primeiro', 'último', 'próximo', 'anterior', 'antes', 'depois', 'agora', 'hoje',
    'amanhã', 'ontem', 'sempre', 'nunca', 'talvez', 'possível', 'impossível',
    'execução', 'implementação', 'configuração', 'inicialização', 'finalização',
    'tratamento', 'exceção', 'erro', 'aviso', 'informação', 'depuração', 'mensagem',
    'documentação', 'comentário', 'cabeçalho', 'rodapé', 'índice', 'tabela', 'gráfico',
    'imagem', 'áudio', 'vídeo', 'animação', 'formulário', 'campo', 'botão', 'menu',
    'janela', 'diálogo', 'painel', 'controle', 'ferramenta', 'dispositivo', 'sensor',
    'resposta', 'pergunta', 'solicitação', 'envio', 'recebimento', 'exportação',
    'importação', 'tradução', 'conversão', 'transformação', 'serialização',
    'deserialização', 'alocação', 'liberação', 'bloqueio', 'desbloqueio', 'conexão',
    'desconexão', 'autenticação', 'autorização', 'verificação', 'validação'
}

# Portuguese special characters
PORTUGUESE_CHARS = {'ç', 'á', 'à', 'â', 'ã', 'é', 'ê', 'í', 'ó', 'ô', 'õ', 'ú', 'ü'}

@dataclass
class ScanConfig:
    """Configuration for file scanner"""
    min_words: int = 3  # Minimum Portuguese words to consider a match
    min_confidence: float = 0.3  # Minimum confidence to consider a file Portuguese
    ignore_dirs: List[str] = None  # Directories to ignore
    file_extensions: List[str] = None  # File extensions to scan
    max_file_size: int = 10 * 1024 * 1024  # Max file size in bytes (10MB default)
    sample_size: int = 1000  # Number of characters to sample for language detection
    use_langdetect: bool = True  # Whether to use langdetect library

    def __post_init__(self):
        """Set defaults for optional fields"""
        if self.ignore_dirs is None:
            self.ignore_dirs = ['.git', '.svn', '__pycache__', 'node_modules', 'venv', 'env', 'build', 'dist']
        
        if self.file_extensions is None:
            self.file_extensions = ['.py', '.js', '.java', '.c', '.cpp', '.h', '.html', '.htm', '.xml', 
                                   '.md', '.txt', '.json', '.yaml', '.yml', '.ini', '.cfg', '.conf']

@dataclass
class ScanResult:
    """Result of scanning a file for Portuguese content"""
    file_path: Path
    is_portuguese: bool
    confidence: float
    portuguese_words: int
    total_words: int
    file_type: str
    size_kb: float
    scan_time: float


class FileScanner:
    """Scanner for detecting Portuguese content in files"""
    
    def __init__(self, config: Optional[ScanConfig] = None):
        """Initialize file scanner
        
        Args:
            config: Configuration for file scanner
        """
        self.config = config or ScanConfig()
        self.results = []
        
        if not LANGDETECT_AVAILABLE and self.config.use_langdetect:
            logger.warning("langdetect library not available. Install with 'pip install langdetect'")
    
    def is_portuguese_text(self, text: str) -> Tuple[bool, float, int, int]:
        """Check if text contains Portuguese content
        
        Args:
            text: Text to check
            
        Returns:
            Tuple (is_portuguese, confidence, portuguese_words, total_words)
        """
        if not text or not text.strip():
            return False, 0.0, 0, 0
        
        # Count total words
        words = re.findall(r'\b\w+\b', text.lower())
        total_words = len(words)
        
        if total_words == 0:
            return False, 0.0, 0, 0
        
        # Count Portuguese keywords
        pt_words = sum(1 for word in words if word in PORTUGUESE_KEYWORDS)
        
        # Count words with Portuguese special characters
        pt_char_words = sum(1 for word in words if any(char in word for char in PORTUGUESE_CHARS))
        
        # Combine counts
        portuguese_words = pt_words + pt_char_words
        
        # Use langdetect for better accuracy if available
        lang_detect_confidence = 0.0
        if LANGDETECT_AVAILABLE and self.config.use_langdetect and len(text) >= 20:
            try:
                # Take a sample of the text for efficiency
                sample = text[:min(len(text), self.config.sample_size)]
                
                # Detect language
                detected_lang = detect(sample)
                
                # If detected as Portuguese, increase confidence
                if detected_lang == 'pt':
                    lang_detect_confidence = 0.8
            except LangDetectException:
                # If detection fails, rely on keyword matching
                pass
        
        # Calculate confidence based on keyword matches and langdetect
        keyword_confidence = min(1.0, portuguese_words / max(10, total_words))
        confidence = max(keyword_confidence, lang_detect_confidence)
        
        # Determine if it's Portuguese based on confidence threshold
        is_portuguese = confidence >= self.config.min_confidence
        
        return is_portuguese, confidence, portuguese_words, total_words
    
    def should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned based on extension and size
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file should be scanned
        """
        # Check if file exists
        if not file_path.exists() or not file_path.is_file():
            return False
        
        # Check file extension
        if self.config.file_extensions and file_path.suffix.lower() not in self.config.file_extensions:
            return False
        
        # Check file size
        try:
            if file_path.stat().st_size > self.config.max_file_size:
                logger.info(f"Skipping large file: {file_path} ({file_path.stat().st_size / 1024:.1f} KB)")
                return False
        except OSError:
            return False
        
        return True
    
    def is_in_ignored_dir(self, file_path: Path) -> bool:
        """Check if file is in an ignored directory
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is in an ignored directory
        """
        if not self.config.ignore_dirs:
            return False
        
        parts = file_path.parts
        return any(ignore_dir in parts for ignore_dir in self.config.ignore_dirs)
    
    def scan_file(self, file_path: Path) -> Optional[ScanResult]:
        """Scan a file for Portuguese content
        
        Args:
            file_path: Path to file
            
        Returns:
            ScanResult if file should be scanned, None otherwise
        """
        if not self.should_scan_file(file_path) or self.is_in_ignored_dir(file_path):
            return None
        
        start_time = time.time()
        
        try:
            # Try reading with UTF-8 encoding
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Fall back to latin-1 if UTF-8 fails
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            
            # Check if content is Portuguese
            is_portuguese, confidence, portuguese_words, total_words = self.is_portuguese_text(content)
            
            # Only consider as Portuguese if minimum words threshold is met
            if portuguese_words < self.config.min_words:
                is_portuguese = False
                confidence = 0.0
            
            # Calculate file size in KB
            size_kb = file_path.stat().st_size / 1024
            
            # Get file type from extension
            file_type = file_path.suffix.lstrip('.').lower()
            
            scan_time = time.time() - start_time
            
            # Create scan result
            result = ScanResult(
                file_path=file_path,
                is_portuguese=is_portuguese,
                confidence=confidence,
                portuguese_words=portuguese_words,
                total_words=total_words,
                file_type=file_type,
                size_kb=size_kb,
                scan_time=scan_time
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {str(e)}")
            return None
    
    def scan_directory(self, directory: Union[str, Path]) -> List[ScanResult]:
        """Scan a directory for files with Portuguese content
        
        Args:
            directory: Directory to scan
            
        Returns:
            List of scan results for files with Portuguese content
        """
        directory = Path(directory)
        
        if not directory.exists() or not directory.is_dir():
            logger.error(f"Directory not found: {directory}")
            return []
        
        logger.info(f"Scanning directory: {directory}")
        
        # Reset results
        self.results = []
        
        # Walk directory tree
        for root, dirs, files in os.walk(directory):
            # Remove ignored directories from the list to avoid walking them
            for ignore_dir in self.config.ignore_dirs:
                if ignore_dir in dirs:
                    dirs.remove(ignore_dir)
            
            # Scan each file
            for file in files:
                file_path = Path(root) / file
                result = self.scan_file(file_path)
                
                if result and result.is_portuguese:
                    self.results.append(result)
        
        # Sort results by confidence (highest first)
        self.results.sort(key=lambda r: r.confidence, reverse=True)
        
        logger.info(f"Found {len(self.results)} files with Portuguese content")
        
        return self.results
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate a report of files with Portuguese content
        
        Args:
            output_file: Path to output file (optional)
            
        Returns:
            Path to report file
        """
        if not self.results:
            logger.warning("No results to generate report")
            return ""
        
        # Default output file
        if not output_file:
            output_file = "portuguese_files_report.md"
        
        # Generate report content
        report = "# Portuguese Files Report\n\n"
        report += f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"Total files: {len(self.results)}\n\n"
        
        report += "## Files by Confidence\n\n"
        report += "| File | Type | Size (KB) | Confidence | Portuguese Words | Total Words |\n"
        report += "| ---- | ---- | --------- | ---------- | ---------------- | ----------- |\n"
        
        for result in self.results:
            report += f"| {result.file_path} | {result.file_type} | {result.size_kb:.1f} | "
            report += f"{result.confidence:.2f} | {result.portuguese_words} | {result.total_words} |\n"
        
        # Write report to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report generated: {output_file}")
        
        return output_file
    
    def export_results_json(self, output_file: Optional[str] = None) -> str:
        """Export results to JSON
        
        Args:
            output_file: Path to output file (optional)
            
        Returns:
            Path to JSON file
        """
        if not self.results:
            logger.warning("No results to export")
            return ""
        
        # Default output file
        if not output_file:
            output_file = "portuguese_files.json"
        
        # Convert results to dict for JSON serialization
        results_dict = []
        for result in self.results:
            results_dict.append({
                "file_path": str(result.file_path),
                "is_portuguese": result.is_portuguese,
                "confidence": result.confidence,
                "portuguese_words": result.portuguese_words,
                "total_words": result.total_words,
                "file_type": result.file_type,
                "size_kb": result.size_kb
            })
        
        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2)
        
        logger.info(f"Results exported to: {output_file}")
        
        return output_file 