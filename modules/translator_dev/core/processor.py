import os
import logging
import time
import threading
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
import shutil
import json
from datetime import datetime

from modules.translator_dev.config.config import ConfigManager
from modules.translator_dev.core.cache import TranslationCache, CacheConfig
from modules.translator_dev.core.scanner import FileScanner, ScanResult

# Setup logging
logger = logging.getLogger("processor")

class TranslationProcessor:
    """Main processor for handling translation tasks"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the translation processor
        
        Args:
            config_path: Path to the configuration file (optional)
        """
        # Load configuration
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config
        
        # Initialize cache
        cache_config = CacheConfig(
            enabled=self.config.cache.enabled,
            directory=self.config.cache.directory,
            max_size=self.config.cache.max_size
        )
        self.cache = TranslationCache(cache_config)
        
        # Initialize scanner
        self.scanner = FileScanner(self.config.scanner)
        
        # Initialize engine
        self.engine = None
        self._setup_engine()
        
        # Threading lock for stats updates
        self._stats_lock = threading.Lock()
        
        # Stats
        self.stats = {
            "files_processed": 0,
            "files_skipped": 0,
            "translation_time": 0,
            "bytes_processed": 0,
            "cache_hits": 0,
            "start_time": time.time()
        }
    
    def _setup_engine(self):
        """Setup the translation engine based on configuration"""
        engine_name = self.config.engine.name.lower()
        
        # Check if cost control is enabled and if we're over budget with OpenAI
        if engine_name == "openai" and hasattr(self.config.engine, "cost_control") and self.config.engine.cost_control.enabled:
            if self._check_cost_limits():
                logger.warning("OpenAI usage is over budget limit! Falling back to HuggingFace engine.")
                engine_name = "huggingface"
            
        if engine_name == "huggingface":
            from modules.translator_dev.engines.huggingface.huggingface_engine import HuggingFaceTranslator
            self.engine = HuggingFaceTranslator(self.config.engine)
            logger.info("Using HuggingFace translation engine (offline mode)")
        elif engine_name == "openai":
            from modules.translator_dev.engines.openai.openai_engine import OpenAITranslator, OpenAIConfig
            
            # Use OpenAI specific config if available
            if hasattr(self.config, "openai"):
                openai_config = OpenAIConfig(
                    api_key=self.config.engine.api_key,
                    model=self.config.openai.model,
                    max_tokens=self.config.openai.max_tokens,
                    temperature=self.config.openai.temperature
                )
            else:
                openai_config = OpenAIConfig(
                    api_key=self.config.engine.api_key,
                    model=self.config.engine.model,
                    max_tokens=self.config.engine.max_tokens,
                    temperature=self.config.engine.temperature
                )
                
            self.engine = OpenAITranslator(openai_config)
            logger.info("Using OpenAI translation engine (online mode)")
            
        elif engine_name == "huggingface":
            from modules.translator_dev.engines.huggingface.marian_engine import MarianTranslator, MarianConfig
            
            # Create MarianMT config
            marian_config = MarianConfig(
                model_name=self.config.engine.model,
                cache_dir=os.path.join(self.config.cache.directory, "models")
            )
            
            self.engine = MarianTranslator(marian_config)
            logger.info(f"Using HuggingFace engine with model {marian_config.model_name}")
            
        else:
            raise ValueError(f"Unsupported engine: {engine_name}")
    
    def _check_cost_limits(self):
        """Check if we're exceeding the configured cost limits"""
        if not hasattr(self.config.engine, "cost_control"):
            return False
            
        cost_control = self.config.engine.cost_control
        if not cost_control.enabled:
            return False
            
        # Check usage file
        usage_file = Path(self.config.cache.directory) / "openai_usage.json"
        current_month = datetime.now().strftime("%Y-%m")
        
        try:
            if usage_file.exists():
                with open(usage_file, 'r') as f:
                    usage_data = json.load(f)
                    
                if current_month in usage_data:
                    current_usage = usage_data[current_month]
                    budget = cost_control.monthly_budget
                    
                    # Check if over budget
                    if current_usage >= budget:
                        logger.warning(f"OpenAI usage (${current_usage:.2f}) exceeds monthly budget (${budget:.2f})")
                        return True
                        
                    # Check if approaching budget
                    if current_usage >= (budget * cost_control.warn_at_percent / 100):
                        percent_used = (current_usage / budget) * 100
                        logger.warning(f"OpenAI usage at {percent_used:.1f}% of monthly budget (${current_usage:.2f}/${budget:.2f})")
        except Exception as e:
            logger.error(f"Error checking cost limits: {str(e)}")
            
        return False

    def _update_usage_costs(self, tokens_used, engine="openai"):
        """Update the usage tracking for cost management"""
        if engine != "openai" or not hasattr(self.config.engine, "cost_control"):
            return
            
        if not self.config.engine.cost_control.enabled:
            return
            
        # Price per 1K tokens (approximate)
        price_per_1k = 0.002  # $0.002 per 1K tokens for GPT-3.5-turbo
        
        # Calculate cost
        cost = (tokens_used / 1000) * price_per_1k
        
        # Update usage file
        usage_file = Path(self.config.cache.directory) / "openai_usage.json"
        current_month = datetime.now().strftime("%Y-%m")
        
        try:
            usage_data = {}
            if usage_file.exists():
                with open(usage_file, 'r') as f:
                    usage_data = json.load(f)
                    
            if current_month not in usage_data:
                usage_data[current_month] = 0
                
            usage_data[current_month] += cost
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(usage_file), exist_ok=True)
            
            with open(usage_file, 'w') as f:
                json.dump(usage_data, f)
                
        except Exception as e:
            logger.error(f"Error updating usage costs: {str(e)}")

    def _save_translated_file(self, original_path: Path, translated_content: str) -> Path:
        """Save translated content to a file
        
        Args:
            original_path: Path to the original file
            translated_content: Translated content
            
        Returns:
            Path to the translated file
        """
        # Create output directory if it doesn't exist
        output_dir = original_path.parent / "translated"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create output file
        output_path = output_dir / original_path.name
        
        # Write translated content
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated_content)
            
        return output_path

    def translate_file(self, file_path: Path) -> Tuple[bool, str]:
        """Translate a single file
        
        Args:
            file_path: Path to the file to translate
            
        Returns:
            Tuple with success status and path to translated file
        """
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return False, ""
            
        logger.info(f"Translating file: {file_path}")
        
        try:
            # Read the file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Try alternative encoding
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            
            # Get file type
            file_type = file_path.suffix.lstrip('.').lower()
            
            # Check cache first
            cache_key = f"{file_path}:{file_type}"
            cached_content = self.cache.get(content, self.config.engine.name, {"file_type": file_type})
            
            if cached_content:
                translated_content = cached_content
                with self._stats_lock:
                    self.stats["cache_hits"] += 1
                logger.info(f"Using cached translation for {file_path}")
            else:
                # Translate based on file type
                start_time = time.time()
                
                if hasattr(self.engine, "translate_file_content"):
                    translated_content = self.engine.translate_file_content(content, file_type)
                else:
                    translated_content = self.engine.translate(content)
                
                # Update stats with thread safety
                with self._stats_lock:
                    self.stats["translation_time"] += time.time() - start_time
                
                # Cache the result
                self.cache.set(content, translated_content, self.config.engine.name, {"file_type": file_type})
            
            # Create output path
            output_dir = file_path.parent / "translated"
            os.makedirs(output_dir, exist_ok=True)
            
            output_path = output_dir / file_path.name
            
            # Backup original if configured
            if self.config.backup_originals:
                backup_dir = file_path.parent / "originals"
                os.makedirs(backup_dir, exist_ok=True)
                
                backup_path = backup_dir / file_path.name
                if not backup_path.exists():
                    shutil.copy2(file_path, backup_path)
            
            # Write translated content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            # Update stats with thread safety
            with self._stats_lock:
                self.stats["files_processed"] += 1
                self.stats["bytes_processed"] += len(content)
            
            logger.info(f"Translation complete: {output_path}")
            return True, str(output_path)
            
        except Exception as e:
            logger.error(f"Error translating file {file_path}: {str(e)}")
            with self._stats_lock:
                self.stats["files_skipped"] += 1
            return False, ""
    
    def translate_files_from_scan(self, directory: Path, priority: Optional[str] = None) -> Dict[str, Any]:
        """Scan a directory and translate Portuguese files
        
        Args:
            directory: Directory to scan
            priority: Filter by priority (high, medium, low) or None for all
            
        Returns:
            Dictionary with results
        """
        # Scan directory for Portuguese files
        results = self.scanner.scan_directory(directory)
        
        if not results:
            logger.info(f"No Portuguese files found in {directory}")
            return {"success": True, "files_processed": 0, "files_found": 0}
        
        # Filter by priority if specified
        if priority:
            priority = priority.lower()
            filtered_results = []
            
            for result in results:
                file_priority = "medium"  # Default
                
                # Determine priority based on confidence
                if result.confidence > 0.8:
                    file_priority = "high"
                elif result.confidence < 0.5:
                    file_priority = "low"
                
                # Increase priority for important file types
                if result.file_type in ["md", "py", "js", "html", "json"]:
                    if file_priority == "medium":
                        file_priority = "high"
                
                if file_priority == priority:
                    filtered_results.append(result)
                    
            results = filtered_results
            
        logger.info(f"Found {len(results)} {'high priority ' if priority else ''}files to translate")
        
        # Convert scan results to paths and use concurrent translation
        file_paths = [result.file_path for result in results]
        result = self.translate_files_from_list(file_paths)
        result["files_found"] = len(results)
        
        return result
    
    def translate_files_from_list(self, file_paths: List[Path]) -> Dict[str, Any]:
        """Translate files from a list of paths
        
        Args:
            file_paths: List of file paths to translate
            
        Returns:
            Dictionary with results
        """
        if not file_paths:
            logger.info("No files provided for translation")
            return {"success": True, "files_processed": 0}
        
        translated_files = []
        skipped_files = []
        
        # Determine max workers based on available cores, but cap it
        max_workers = min(os.cpu_count() or 4, 8)
        
        # Use concurrent processing if enabled in config and more than one file
        use_concurrent = getattr(self.config, 'use_concurrent', True) and len(file_paths) > 1
        
        if use_concurrent and max_workers > 1:
            logger.info(f"Using concurrent processing with {max_workers} workers")
            
            # Define worker function
            def translate_file_worker(file_path):
                path = Path(file_path)
                success, output_path = self.translate_file(path)
                return success, str(path)
            
            # Process files concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(translate_file_worker, path): path for path in file_paths}
                
                for future in concurrent.futures.as_completed(futures):
                    success, path = future.result()
                    if success:
                        translated_files.append(path)
                    else:
                        skipped_files.append(path)
        else:
            # Process files sequentially
            for file_path in file_paths:
                path = Path(file_path)
                success, output_path = self.translate_file(path)
                
                if success:
                    translated_files.append(str(path))
                else:
                    skipped_files.append(str(path))
        
        return {
            "success": True,
            "files_processed": len(translated_files),
            "files_skipped": len(skipped_files),
            "translated_files": translated_files,
            "skipped_files": skipped_files,
            "stats": self.get_stats()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current translation statistics
        
        Returns:
            Dictionary with statistics
        """
        # Update elapsed time
        elapsed = time.time() - self.stats["start_time"]
        
        # Add cache stats
        cache_stats = self.cache.stats()
        
        # Calculate speeds
        files_per_second = self.stats["files_processed"] / elapsed if elapsed > 0 else 0
        bytes_per_second = self.stats["bytes_processed"] / elapsed if elapsed > 0 else 0
        
        return {
            "files_processed": self.stats["files_processed"],
            "files_skipped": self.stats["files_skipped"],
            "translation_time": self.stats["translation_time"],
            "bytes_processed": self.stats["bytes_processed"],
            "cache_hits": self.stats["cache_hits"],
            "elapsed_time": elapsed,
            "files_per_second": files_per_second,
            "bytes_per_second": bytes_per_second,
            "cache": cache_stats
        } 