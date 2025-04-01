#!/usr/bin/env python3
"""
Perplexity Integration for EVA & GUARANI
Connects Perplexity search capabilities with the EVA & GUARANI ecosystem
"""

import os
import asyncio
import logging
import requests
import json
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv
import aiohttp

from .perplexity_client import PerplexityClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerplexityAPI:
    """Classe para integração com a API do Perplexity."""
    
    def __init__(self):
        """Inicializa a API do Perplexity."""
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        if not self.api_key:
            logger.warning("API Key do Perplexity não encontrada nas variáveis de ambiente")
    
    def is_configured(self) -> bool:
        """Verifica se a API está configurada corretamente."""
        return bool(self.api_key)
    
    async def search(self, query: str, persona: str = "default") -> Dict:
        """
        Realiza uma busca usando a API do Perplexity.
        
        Args:
            query: A consulta de busca
            persona: O persona a ser usado (default, philosopher, scientist)
            
        Returns:
            Dict com os resultados da busca
        """
        if not self.is_configured():
            raise ValueError("API Key do Perplexity não configurada")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/search",
                    headers=self.headers,
                    json={
                        "query": query,
                        "persona": persona
                    }
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise Exception(f"Erro na API do Perplexity: {error_text}")
        except Exception as e:
            logger.error(f"Erro ao realizar busca: {str(e)}")
            raise

class PerplexityIntegration:
    """Integration between Perplexity and EVA & GUARANI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the integration"""
        load_dotenv()
        self.client = PerplexityClient(api_key)
        self.enabled = bool(self.client.api_key)
        
        # Cache for recent search results
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
        self.cache_max_size = 100
        
        # Connect to ETHIK module if available
        try:
            from core.ethik import EthicalEvaluator
            self.ethical_evaluator = EthicalEvaluator()
            self.ethics_enabled = True
        except ImportError:
            logger.warning("ETHIK module not found. Ethical evaluation disabled.")
            self.ethics_enabled = False
            
        # Connect to CRONOS module if available
        try:
            from core.cronos import EvolutionPreserver
            self.evolution_preserver = EvolutionPreserver()
            self.preservation_enabled = True
        except ImportError:
            logger.warning("CRONOS module not found. Evolution preservation disabled.")
            self.preservation_enabled = False
            
        logger.info(f"Perplexity integration initialized. Enabled: {self.enabled}")
    
    async def enhance_knowledge(self, 
                              query: str, 
                              context: Optional[Dict[str, Any]] = None,
                              persona: Optional[str] = None,
                              ethical_filter: bool = True) -> Dict[str, Any]:
        """
        Enhance EVA & GUARANI knowledge with Perplexity search
        
        Args:
            query (str): The search query
            context (Dict, optional): Additional context for the search
            persona (str, optional): The persona making the query
            ethical_filter (bool): Whether to apply ethical filtering
            
        Returns:
            Dict containing enhanced knowledge
        """
        if not self.enabled:
            return {"error": "Perplexity integration not enabled. API key required."}
        
        # Prepare enhanced query with EVA & GUARANI context
        enhanced_query = self._prepare_enhanced_query(query, context, persona)
        
        # Check cache first
        cache_key = self._generate_cache_key(enhanced_query)
        if cache_key in self.cache:
            logger.info(f"Returning cached result for query: {query}")
            return self.cache[cache_key]
        
        # Perform search
        search_result = await self.client.search_with_sources(enhanced_query)
        
        # Apply ethical evaluation if enabled
        if ethical_filter and self.ethics_enabled:
            search_result = self._apply_ethical_filter(search_result)
        
        # Format for EVA & GUARANI
        formatted_result = self._format_for_egos(search_result, query, persona)
        
        # Save to cache
        self._update_cache(cache_key, formatted_result)
        
        # Preserve evolution if enabled
        if self.preservation_enabled:
            await self._preserve_knowledge(formatted_result, query, persona)
        
        return formatted_result
    
    def _prepare_enhanced_query(self, 
                              query: str, 
                              context: Optional[Dict[str, Any]] = None,
                              persona: Optional[str] = None) -> str:
        """
        Prepare an enhanced query with EVA & GUARANI context
        
        Args:
            query (str): The basic query
            context (Dict, optional): Additional context
            persona (str, optional): The persona making the query
            
        Returns:
            An enhanced query string
        """
        enhanced_query = query
        
        # Add persona context if available
        if persona:
            # Different query enhancements based on persona
            if persona.lower() == "philosopher":
                enhanced_query = f"As a philosopher would analyze: {query}. Focus on ethical, epistemological, and metaphysical aspects."
            elif persona.lower() == "scientist":
                enhanced_query = f"Analyze from a scientific perspective: {query}. Focus on empirical evidence, theories, and research."
            elif persona.lower() == "gamer":
                enhanced_query = f"From a gaming perspective: {query}. Consider game mechanics, player experience, and gaming culture."
            elif persona.lower() == "economist":
                enhanced_query = f"Economic analysis of: {query}. Consider market dynamics, economic theories, and financial implications."
            else:
                enhanced_query = f"{query}"
        
        # Add additional context if provided
        if context:
            relevant_context = []
            if "topics" in context:
                relevant_context.append(f"Focus on topics: {', '.join(context['topics'])}")
            if "time_period" in context:
                relevant_context.append(f"Consider time period: {context['time_period']}")
            if "perspective" in context:
                relevant_context.append(f"From the perspective of: {context['perspective']}")
                
            if relevant_context:
                enhanced_query += "\n\nAdditional context: " + ". ".join(relevant_context)
        
        return enhanced_query
    
    def _apply_ethical_filter(self, search_result: Dict[str, Any]) -> Dict[str, Any]:
        """Apply ethical filtering to search results"""
        try:
            if "error" in search_result:
                return search_result
                
            content = search_result.get("content", "")
            
            # Apply ethical evaluation through ETHIK module
            evaluation = self.ethical_evaluator.evaluate_content(content)
            
            # If content violates ethical standards, modify it
            if evaluation.get("ethical_score", 1.0) < 0.7:
                warning = "Note: Some content was filtered based on ethical considerations."
                filtered_content = self.ethical_evaluator.sanitize_content(content)
                search_result["content"] = filtered_content
                search_result["ethical_warning"] = warning
                search_result["ethical_evaluation"] = evaluation
            
            return search_result
            
        except Exception as e:
            logger.error(f"Error during ethical filtering: {str(e)}")
            return search_result
    
    def _format_for_egos(self, 
                       search_result: Dict[str, Any], 
                       original_query: str,
                       persona: Optional[str] = None) -> Dict[str, Any]:
        """Format search results for EVA & GUARANI consumption"""
        
        if "error" in search_result:
            return {
                "status": "error",
                "message": search_result["error"],
                "query": original_query
            }
        
        content = search_result.get("content", "")
        sources = search_result.get("sources", [])
        
        # Format based on persona if specified
        if persona:
            formatted_result = {
                "status": "success",
                "query": original_query,
                "knowledge": {
                    "content": content,
                    "sources": sources,
                    "persona": persona,
                    "reliability": self._calculate_reliability(sources),
                    "timestamp": self._get_timestamp()
                }
            }
        else:
            formatted_result = {
                "status": "success",
                "query": original_query,
                "knowledge": {
                    "content": content,
                    "sources": sources,
                    "reliability": self._calculate_reliability(sources),
                    "timestamp": self._get_timestamp()
                }
            }
        
        # Add ethical evaluation if present
        if "ethical_warning" in search_result:
            formatted_result["knowledge"]["ethical_warning"] = search_result["ethical_warning"]
            
        if "ethical_evaluation" in search_result:
            formatted_result["knowledge"]["ethical_evaluation"] = search_result["ethical_evaluation"]
        
        return formatted_result
    
    def _calculate_reliability(self, sources: List[Dict[str, str]]) -> float:
        """Calculate reliability score based on sources"""
        if not sources:
            return 0.6  # Default moderate reliability with no sources
            
        # Simple heuristic: more sources = more reliable, up to a point
        source_count = len(sources)
        if source_count >= 5:
            return 0.9
        elif source_count >= 3:
            return 0.8
        elif source_count >= 1:
            return 0.7
        else:
            return 0.6
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _generate_cache_key(self, query: str) -> str:
        """Generate a cache key for a query"""
        import hashlib
        return hashlib.md5(query.encode()).hexdigest()
    
    def _update_cache(self, key: str, value: Dict[str, Any]) -> None:
        """Update the cache with a new value"""
        self.cache[key] = value
        
        # Trim cache if it gets too large
        if len(self.cache) > self.cache_max_size:
            # Remove oldest entries (simple implementation)
            remove_count = len(self.cache) - self.cache_max_size
            keys_to_remove = list(self.cache.keys())[:remove_count]
            for k in keys_to_remove:
                del self.cache[k]
    
    async def _preserve_knowledge(self, 
                                knowledge: Dict[str, Any], 
                                query: str,
                                persona: Optional[str] = None) -> None:
        """Preserve knowledge through CRONOS module"""
        try:
            if self.preservation_enabled and knowledge.get("status") == "success":
                metadata = {
                    "source": "perplexity",
                    "query": query,
                    "timestamp": self._get_timestamp()
                }
                
                if persona:
                    metadata["persona"] = persona
                
                await self.evolution_preserver.preserve(
                    content=knowledge.get("knowledge", {}).get("content", ""),
                    metadata=metadata,
                    category="external_knowledge"
                )
        except Exception as e:
            logger.error(f"Error preserving knowledge: {str(e)}")

# Example usage
async def test_integration():
    """Test the Perplexity integration"""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    integration = PerplexityIntegration(api_key)
    
    # Test with philosopher persona
    result = await integration.enhance_knowledge(
        "What is the nature of consciousness?",
        persona="philosopher"
    )
    
    import json
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_integration()) 