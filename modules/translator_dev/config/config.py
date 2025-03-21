from dataclasses import dataclass, field, asdict
import os
import yaml
from typing import Dict, Any, Optional, List

@dataclass
class EngineConfig:
    name: str = "huggingface"
    api_key: Optional[str] = None
    model: str = "Helsinki-NLP/opus-mt-pt-en"
    max_tokens: int = 4096
    temperature: float = 0.3
    
@dataclass
class ScannerConfig:
    ignore_dirs: List[str] = field(default_factory=lambda: [
        ".git", "__pycache__", "venv", "env", 
        "node_modules", "cursor", "build", "dist"
    ])
    ignore_files: List[str] = field(default_factory=lambda: [
        ".gitignore", "LICENSE", ".DS_Store", "Thumbs.db"
    ])
    file_extensions: List[str] = field(default_factory=lambda: [
        ".py", ".md", ".txt", ".json", ".js", ".html", ".css", ".bat", ".ps1"
    ])

@dataclass
class CacheConfig:
    enabled: bool = True
    directory: str = "./cache"
    max_size: int = 1_000_000_000  # 1GB

@dataclass
class TranslatorConfig:
    engine: EngineConfig = field(default_factory=EngineConfig)
    scanner: ScannerConfig = field(default_factory=ScannerConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    report_output: str = "translation_report.md"
    backup_originals: bool = True
    
class ConfigManager:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "config", 
            "settings.yaml"
        )
        self.config = self.load()
    
    def load(self) -> TranslatorConfig:
        """Load configuration from YAML file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            # Fill in missing configurations
            config = TranslatorConfig()
            
            if data and isinstance(data, dict):
                # Engine config
                if 'engine' in data:
                    engine_data = data['engine']
                    config.engine.name = engine_data.get('name', config.engine.name)
                    config.engine.api_key = engine_data.get('api_key', config.engine.api_key)
                    config.engine.model = engine_data.get('model', config.engine.model)
                    config.engine.max_tokens = engine_data.get('max_tokens', config.engine.max_tokens)
                    config.engine.temperature = engine_data.get('temperature', config.engine.temperature)
                
                # Scanner config
                if 'scanner' in data:
                    scanner_data = data['scanner']
                    if 'ignore_dirs' in scanner_data:
                        config.scanner.ignore_dirs = scanner_data['ignore_dirs']
                    if 'ignore_files' in scanner_data:
                        config.scanner.ignore_files = scanner_data['ignore_files']
                    if 'file_extensions' in scanner_data:
                        config.scanner.file_extensions = scanner_data['file_extensions']
                
                # Cache config
                if 'cache' in data:
                    cache_data = data['cache']
                    config.cache.enabled = cache_data.get('enabled', config.cache.enabled)
                    config.cache.directory = cache_data.get('directory', config.cache.directory)
                    config.cache.max_size = cache_data.get('max_size', config.cache.max_size)
                
                # General config
                config.report_output = data.get('report_output', config.report_output)
                config.backup_originals = data.get('backup_originals', config.backup_originals)
                
            return config
        else:
            # Return default configuration
            return TranslatorConfig()
    
    def save(self) -> None:
        """Save configuration to YAML file"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Convert dataclass to dict
        config_dict = asdict(self.config)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False)
    
    def update(self, **kwargs) -> None:
        """Update configuration with provided values"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value) 