#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Dict, List, Tuple, Any
import json
import hashlib
import re

class QuantumPromptEncoder:
    """
    Codificador para o sistema quântico de prompts.
    Transforma prompts extensos em versões compactas de alta densidade informacional.
    """
    
    def __init__(self):
        self.compression_level = 3  # Níveis de 1-5, onde 5 é máxima compressão
        self.token_mapping = {}  # Mapeia tokens frequentes para representações compactas
        
    def encode_prompt(self, prompt: str, domain: str = "general") -> Tuple[str, Dict]:
        """
        Codifica um prompt extenso em uma versão quântica compacta.
        Retorna o prompt codificado e metadados para decodificação.
        """
        # 1. Pré-processamento
        clean_prompt = self._preprocess_prompt(prompt)
        
        # 2. Análise semântica
        key_concepts = self._extract_key_concepts(clean_prompt)
        
        # 3. Compressão conceitual
        compressed_concepts = self._compress_concepts(key_concepts, domain)
        
        # 4. Gerar prompt quântico
        quantum_prompt = self._generate_quantum_prompt(compressed_concepts, domain)
        
        # 5. Gerar metadados para decodificação
        metadata = {
            "original_length": len(prompt),
            "compressed_length": len(quantum_prompt),
            "compression_ratio": len(prompt) / max(1, len(quantum_prompt)),
            "domain": domain,
            "key_concepts": key_concepts[:10],  # Primeiros 10 conceitos
            "checksum": hashlib.md5(prompt.encode()).hexdigest()
        }
        
        return quantum_prompt, metadata
    
    def _preprocess_prompt(self, prompt: str) -> str:
        """Limpa e normaliza o prompt para processamento"""
        # Remove espaços em branco excessivos
        clean = re.sub(r'\s+', ' ', prompt).strip()
        # Remove formatação especial simples
        clean = re.sub(r'[*_~`]', '', clean)
        return clean
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """
        Extrai conceitos-chave do texto.
        Versão simplificada - uma implementação real usaria NLP mais avançado.
        """
        # Divide em sentenças
        sentences = re.split(r'[.!?]+', text)
        
        # Encontra frases nominais e palavras-chave
        concepts = []
        
        # Versão simplificada - extrai palavras maiores como potenciais conceitos
        words = re.findall(r'\b[A-Za-z]{5,}\b', text)
        word_freq = {}
        
        for word in words:
            word_lower = word.lower()
            word_freq[word_lower] = word_freq.get(word_lower, 0) + 1
        
        # Pega os conceitos mais frequentes
        concepts = [word for word, freq in sorted(
            word_freq.items(), key=lambda x: x[1], reverse=True
        )][:20]  # Top 20 conceitos
        
        return concepts
    
    def _compress_concepts(self, concepts: List[str], domain: str) -> List[Dict]:
        """Comprime conceitos em representações mais densas"""
        compressed = []
        
        for concept in concepts:
            # Em uma implementação real, usaríamos embeddings ou outras técnicas
            # de representação semântica. Aqui, simplificamos.
            compressed.append({
                "concept": concept,
                "weight": len(concept) / 100,  # Peso simples baseado no comprimento
                "domain_relevance": 0.8 if concept in domain else 0.4
            })
            
        # Ordena por relevância
        compressed.sort(key=lambda x: x["weight"] * x["domain_relevance"], reverse=True)
        
        return compressed[:10]  # Mantém apenas os 10 mais relevantes
    
    def _generate_quantum_prompt(self, concepts: List[Dict], domain: str) -> str:
        """
        Gera o prompt quântico a partir dos conceitos comprimidos.
        Um prompt quântico é uma representação densa que captura a essência semântica.
        """
        # Formato: @quantum:{domain}:[conceito1:peso1,conceito2:peso2,...]
        concept_parts = []
        
        for c in concepts:
            concept_parts.append(f"{c['concept']}:{c['weight']:.2f}")
        
        quantum_prompt = f"@quantum:{domain}:[{','.join(concept_parts)}]"
        
        return quantum_prompt 