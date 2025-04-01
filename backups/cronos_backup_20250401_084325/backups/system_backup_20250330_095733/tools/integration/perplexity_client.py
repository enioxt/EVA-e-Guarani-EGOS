#!/usr/bin/env python3
"""
Perplexity API Client for EVA & GUARANI
Provides real-time search capabilities with AI synthesis
"""

import os
import json
import asyncio
import logging
import requests
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerplexityClient:
    """Client for interacting with the Perplexity API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Perplexity client with API key"""
        load_dotenv()
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        if not self.api_key:
            logger.warning("Perplexity API key not found. Set PERPLEXITY_API_KEY in .env or provide during initialization.")
    
    async def search(self, 
                    query: str, 
                    model: str = "sonar-medium-online", 
                    max_tokens: int = 800,
                    temperature: float = 0.7,
                    stream: bool = False) -> Dict[str, Any]:
        """
        Perform a search query through Perplexity API
        
        Args:
            query (str): The search query
            model (str): The model to use (default: sonar-medium-online)
            max_tokens (int): Maximum response tokens (default: 800)
            temperature (float): Creativity temperature (default: 0.7)
            stream (bool): Whether to stream the response (default: False)
            
        Returns:
            Dict containing the search results
        """
        try:
            endpoint = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": query}],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": stream
            }
            
            logger.debug(f"Sending request to Perplexity API: {json.dumps(payload)}")
            
            if stream:
                return await self._handle_streaming(endpoint, payload)
            else:
                response = requests.post(endpoint, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Error during Perplexity API call: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
    
    async def _handle_streaming(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle streaming response from Perplexity API"""
        try:
            full_response = ""
            async with aiohttp.ClientSession() as session:
                async with session.post(endpoint, headers=self.headers, json=payload) as response:
                    response.raise_for_status()
                    async for line in response.content:
                        line_text = line.decode('utf-8')
                        if line_text.startswith('data: '):
                            data = line_text[6:]  # Remove 'data: ' prefix
                            if data == "[DONE]":
                                break
                            try:
                                json_data = json.loads(data)
                                if 'choices' in json_data and json_data['choices']:
                                    content = json_data['choices'][0].get('delta', {}).get('content', '')
                                    if content:
                                        full_response += content
                            except json.JSONDecodeError:
                                continue
            
            return {"result": full_response}
                
        except Exception as e:
            error_msg = f"Error during streaming Perplexity API call: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
            
    async def search_with_sources(self, query: str, model: str = "sonar-medium-online") -> Dict[str, Any]:
        """
        Perform a search query and extract sources from the response
        
        Args:
            query (str): The search query
            model (str): The model to use (default: sonar-medium-online)
            
        Returns:
            Dict containing the search results and sources
        """
        try:
            # Modify query to ask for sources
            enhanced_query = f"{query}\n\nPlease include sources for this information."
            
            result = await self.search(enhanced_query, model=model)
            
            if "error" in result:
                return result
                
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Extract sources from content - assuming sources are at the end
            sources = self._extract_sources(content)
            
            return {
                "content": content,
                "sources": sources
            }
            
        except Exception as e:
            error_msg = f"Error during search with sources: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
    
    def _extract_sources(self, content: str) -> List[Dict[str, str]]:
        """Extract sources from the content"""
        sources = []
        
        # Simple extraction - assuming sources are listed as URLs at the end
        # This is a basic implementation - may need refinement based on actual API responses
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('http') or line.startswith('www.'):
                sources.append({"url": line})
            elif '[' in line and ']' in line and 'http' in line:
                # Handle markdown-style links [text](url)
                source_text = line[line.find('[')+1:line.find(']')]
                url_start = line.find('(')+1
                url_end = line.find(')', url_start)
                if url_end > url_start:
                    url = line[url_start:url_end]
                    sources.append({"title": source_text, "url": url})
        
        return sources

# Example usage
async def test_perplexity():
    """Test the Perplexity client"""
    client = PerplexityClient()
    result = await client.search("What are the latest developments in quantum computing?")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_perplexity()) 