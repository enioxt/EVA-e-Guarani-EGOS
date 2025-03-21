from dataclasses import dataclass
from transformers import MarianMTModel, MarianTokenizer
import os
import torch
from typing import Optional, List, Dict, Any

@dataclass
class MarianConfig:
    model_name: str = "Helsinki-NLP/opus-mt-pt-en"
    cache_dir: str = "./models"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

class MarianTranslator:
    def __init__(self, config: Optional[MarianConfig] = None):
        self.config = config or MarianConfig()
        
        # Load model and tokenizer only on first call
        self._model: Optional[MarianMTModel] = None
        self._tokenizer: Optional[MarianTokenizer] = None
    
    @property
    def model(self) -> MarianMTModel:
        if self._model is None:
            self._model = MarianMTModel.from_pretrained(
                self.config.model_name,
                cache_dir=self.config.cache_dir
            ).to(self.config.device)
        return self._model
    
    @property
    def tokenizer(self) -> MarianTokenizer:
        if self._tokenizer is None:
            self._tokenizer = MarianTokenizer.from_pretrained(
                self.config.model_name,
                cache_dir=self.config.cache_dir
            )
        return self._tokenizer
    
    def translate(self, text: str) -> str:
        """Translate a single text from Portuguese to English"""
        # Skip empty strings
        if not text or not text.strip():
            return text
            
        # Tokenize
        inputs = self.tokenizer([text], return_tensors="pt", padding=True)
        inputs = {k: v.to(self.config.device) for k, v in inputs.items()}
        
        # Translate
        with torch.no_grad():
            translated = self.model.generate(**inputs)
        
        # Decode
        result = self.tokenizer.decode(translated[0], skip_special_tokens=True)
        return result
    
    def translate_batch(self, texts: List[str]) -> List[str]:
        """Translate a batch of texts from Portuguese to English"""
        if not texts:
            return []
            
        # Filter empty strings
        non_empty_indices = [i for i, t in enumerate(texts) if t and t.strip()]
        if not non_empty_indices:
            return texts
            
        non_empty_texts = [texts[i] for i in non_empty_indices]
        
        # Tokenize
        inputs = self.tokenizer(non_empty_texts, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.config.device) for k, v in inputs.items()}
        
        # Translate
        with torch.no_grad():
            translated = self.model.generate(**inputs)
        
        # Decode
        results = [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        
        # Reintegrate with empty strings
        final_results = texts.copy()
        for idx, result in zip(non_empty_indices, results):
            final_results[idx] = result
            
        return final_results 