#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Quantum Knowledge Hub
=====================================

Central quantum knowledge hub that serves as a unified interface
to access all the knowledge, ethics, characters, and stories of the
EVA & GUARANI ecosystem.

This system functions as an internal API that is queried before
any processing by external AI models, ensuring that responses maintain
the identity, ethics, and aesthetics of the project.

Author: ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Version: 1.0
"""

import os
import json
import logging
import asyncio
import hashlib
import time
import sqlite3
import pickle
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/quantum_knowledge.log')
    ]
)

logger = logging.getLogger("quantum_knowledge")

class QuantumKnowledgeHub:
    """
    Central quantum knowledge hub of EVA & GUARANI.
    Functions as a repository and interface for all the ecosystem's knowledge.
    """
    
    def __init__(self, config_path: str = "config/quantum_knowledge.json"):
        """
        Initializes the quantum knowledge hub.
        
        Args:
            config_path: Path to the configuration file
        """
        self.logger = logger
        self.logger.info("Initializing Quantum Knowledge Hub")
        
        # Configuration and data paths
        self.config_path = Path(config_path)
        self.data_path = Path("data/quantum_knowledge")
        self.vector_db_path = self.data_path / "vector_db.sqlite"
        self.cache_path = self.data_path / "cache"
        
        # Internal state
        self.config = self._load_config()
        self.cache = {}
        self.vector_db = None
        self.prompt_templates = {}
        self.ethical_guidelines = {}
        self.personas = {}
        self.storytelling_elements = {}
        self.initialized = False
        
        # Ensure directories exist
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.cache_path, exist_ok=True)
        
        # Load vector database
        self._setup_vector_db()
        
        # Load resources
        self._load_resources()
        
        self.initialized = True
        self.logger.info("Quantum Knowledge Hub successfully initialized")
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the knowledge hub configuration.
        
        Returns:
            Dictionary with the configurations
        """
        # Default configuration
        default_config = {
            "version": "1.0",
            "cache_ttl": 3600,  # 1 hour
            "embedding_dimension": 1536,
            "similarity_threshold": 0.75,
            "max_results": 5,
            "ethical_threshold": 0.8,
            "creativity_level": 0.8,
            "data_sources": {
                "quantum_prompts": "EGOS/quantum_prompts",
                "ethical_guidelines": "EGOS/ethical_system",
                "personas": "EGOS/personas",
                "stories": "EGOS/stories",
                "blockchain": "EGOS/blockchain",
                "game_elements": "EGOS/game_elements"
            },
            "embedding_model": "text-embedding-3-small",
            "response_templates": {
                "ethical_response": "templates/ethical_response.md",
                "creative_response": "templates/creative_response.md",
                "educational_response": "templates/educational_response.md",
                "error_response": "templates/error_response.md"
            }
        }
        
        # Try to load custom configuration
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with default configuration
                    merged_config = {**default_config, **config}
                    self.logger.info(f"Configuration loaded from {self.config_path}")
                    return merged_config
            else:
                # Create default configuration file
                os.makedirs(self.config_path.parent, exist_ok=True)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Default configuration created at {self.config_path}")
                return default_config
                
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return default_config
            
    def _setup_vector_db(self) -> None:
        """
        Sets up the vector database for semantic search.
        """
        try:
            # Connect to SQLite
            self.vector_db = sqlite3.connect(self.vector_db_path)
            cursor = self.vector_db.cursor()
            
            # Create table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                embedding BLOB NOT NULL,
                type TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create index for type
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON embeddings(type)')
            
            self.vector_db.commit()
            self.logger.info(f"Vector database set up at {self.vector_db_path}")
            
        except Exception as e:
            self.logger.error(f"Error setting up vector database: {e}")
            
    def _load_resources(self) -> None:
        """
        Loads all necessary resources (templates, guidelines, etc).
        """
        try:
            # Load prompt templates
            templates_dir = Path("templates")
            if templates_dir.exists():
                for template_file in templates_dir.glob("*.md"):
                    with open(template_file, 'r', encoding='utf-8') as f:
                        self.prompt_templates[template_file.stem] = f.read()
                        
            # Load ethical guidelines
            ethics_dir = Path(self.config["data_sources"]["ethical_guidelines"])
            if ethics_dir.exists():
                for ethics_file in ethics_dir.glob("*.json"):
                    with open(ethics_file, 'r', encoding='utf-8') as f:
                        self.ethical_guidelines[ethics_file.stem] = json.load(f)
                        
            # Load personas
            personas_dir = Path(self.config["data_sources"]["personas"])
            if personas_dir.exists():
                for persona_file in personas_dir.glob("*.json"):
                    with open(persona_file, 'r', encoding='utf-8') as f:
                        self.personas[persona_file.stem] = json.load(f)
                        
            # Load storytelling elements
            stories_dir = Path(self.config["data_sources"]["stories"])
            if stories_dir.exists():
                for story_file in stories_dir.glob("*.json"):
                    with open(story_file, 'r', encoding='utf-8') as f:
                        self.storytelling_elements[story_file.stem] = json.load(f)
                        
            self.logger.info("Resources loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading resources: {e}")
            
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generates an embedding for the provided text.
        
        Args:
            text: Text to generate embedding
            
        Returns:
            List of floats representing the embedding
        """
        try:
            # Use cache to avoid repeated requests
            text_hash = hashlib.md5(text.encode()).hexdigest()
            cache_file = self.cache_path / f"{text_hash}.pkl"
            
            # Check cache
            if cache_file.exists():
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                    # Check if cache expired
                    if time.time() - cached_data['timestamp'] < self.config["cache_ttl"]:
                        return cached_data['embedding']
            
            # If not in cache, generate embedding
            # Import OpenAI here to avoid circular dependency
            from openai import OpenAI
            
            # Load quantum configuration to get API key
            quantum_config_path = Path("config/quantum_config.json")
            if quantum_config_path.exists():
                with open(quantum_config_path, 'r', encoding='utf-8') as f:
                    quantum_config = json.load(f)
            else:
                raise FileNotFoundError("Quantum configuration file not found")
                
            # Set up OpenAI client
            client = OpenAI(api_key=quantum_config.get("openai_api_key", ""))
            
            # Generate embedding
            response = client.embeddings.create(
                model=self.config["embedding_model"],
                input=text
            )
            
            embedding = response.data[0].embedding
            
            # Save to cache
            with open(cache_file, 'wb') as f:
                pickle.dump({'embedding': embedding, 'timestamp': time.time()}, f)
                
            return embedding
            
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            # Return an empty embedding with the correct dimension
            return [0.0] * self.config["embedding_dimension"]
            
    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculates the cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity value between 0 and 1
        """
        # Dot product
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        
        # Magnitudes
        magnitude1 = sum(a * a for a in embedding1) ** 0.5
        magnitude2 = sum(b * b for b in embedding2) ** 0.5
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
            
        # Cosine similarity
        return dot_product / (magnitude1 * magnitude2)
            
    async def add_to_knowledge_base(self, text: str, type_: str, metadata: Dict[str, Any] = None) -> str:
        """
        Adds knowledge to the vector database.
        
        Args:
            text: Text to be added
            type_: Type of knowledge (ethics, character, story, etc)
            metadata: Additional metadata
            
        Returns:
            ID of the added knowledge
        """
        try:
            # Generate unique ID
            text_hash = hashlib.md5(text.encode()).hexdigest()
            id_ = f"{type_}_{text_hash}"
            
            # Generate embedding
            embedding = await self.generate_embedding(text)
            
            # Serialize embedding
            embedding_blob = pickle.dumps(embedding)
            
            # Serialize metadata
            metadata_json = json.dumps(metadata) if metadata else None
            
            # Save to database
            cursor = self.vector_db.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO embeddings (id, text, embedding, type, metadata) VALUES (?, ?, ?, ?, ?)',
                (id_, text, embedding_blob, type_, metadata_json)
            )
            self.vector_db.commit()
            
            self.logger.info(f"Knowledge added to database: {id_}")
            return id_
            
        except Exception as e:
            self.logger.error(f"Error adding knowledge: {e}")
            return ""
            
    async def search_knowledge_base(self, query: str, type_: Optional[str] = None, threshold: float = None) -> List[Dict[str, Any]]:
        """
        Searches for similar knowledge in the vector database.
        
        Args:
            query: Query text
            type_: Filter by specific type (optional)
            threshold: Similarity threshold (optional, uses config value if not specified)
            
        Returns:
            List of results ordered by similarity
        """
        try:
            # Use config threshold if not specified
            if threshold is None:
                threshold = self.config["similarity_threshold"]
                
            # Generate embedding for the query
            query_embedding = await self.generate_embedding(query)
            
            # Search in the database
            cursor = self.vector_db.cursor()
            
            if type_:
                cursor.execute('SELECT id, text, embedding, type, metadata FROM embeddings WHERE type = ?', (type_,))
            else:
                cursor.execute('SELECT id, text, embedding, type, metadata FROM embeddings')
                
            # Calculate similarity for each item
            results = []
            for row in cursor.fetchall():
                id_, text, embedding_blob, item_type, metadata_json = row
                
                # Deserialize embedding
                embedding = pickle.loads(embedding_blob)
                
                # Calculate similarity
                sim = self.similarity(query_embedding, embedding)
                
                # Filter by threshold
                if sim >= threshold:
                    # Deserialize metadata
                    metadata = json.loads(metadata_json) if metadata_json else {}
                    
                    results.append({
                        'id': id_,
                        'text': text,
                        'type': item_type,
                        'similarity': sim,
                        'metadata': metadata
                    })
            
            # Sort by similarity (descending)
            results.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Limit the number of results
            max_results = self.config["max_results"]
            return results[:max_results]
            
        except Exception as e:
            self.logger.error(f"Error searching knowledge: {e}")
            return []
            
    async def get_ethical_guidelines(self, context: str) -> Dict[str, Any]:
        """
        Obtains relevant ethical guidelines for the provided context.
        
        Args:
            context: Context or query to search for relevant ethical guidelines
            
        Returns:
            Relevant ethical guidelines
        """
        results = await self.search_knowledge_base(context, type_="ethics")
        
        if results:
            # Merge all found guidelines
            combined_guidelines = {
                "ethical_principles": [],
                "prohibited_content": [],
                "recommendations": []
            }
            
            for result in results:
                # Extract guidelines from text or metadata
                if 'metadata' in result and isinstance(result['metadata'], dict):
                    metadata = result['metadata']
                    
                    # Add ethical principles
                    if 'principles' in metadata:
                        combined_guidelines["ethical_principles"].extend(metadata['principles'])
                        
                    # Add prohibited content
                    if 'prohibited' in metadata:
                        combined_guidelines["prohibited_content"].extend(metadata['prohibited'])
                        
                    # Add recommendations
                    if 'recommendations' in metadata:
                        combined_guidelines["recommendations"].extend(metadata['recommendations'])
            
            # Remove duplicates
            combined_guidelines["ethical_principles"] = list(set(combined_guidelines["ethical_principles"]))
            combined_guidelines["prohibited_content"] = list(set(combined_guidelines["prohibited_content"]))
            combined_guidelines["recommendations"] = list(set(combined_guidelines["recommendations"]))
            
            return combined_guidelines
        else:
            # Return default guidelines
            return {
                "ethical_principles": [
                    "Respect the privacy and dignity of all beings",
                    "Promote well-being and harmony",
                    "Act with compassion and unconditional love"
                ],
                "prohibited_content": [
                    "Harmful or discriminatory content",
                    "Information that violates privacy",
                    "Explicit or inappropriate content"
                ],
                "recommendations": [
                    "Communicate clearly and respectfully",
                    "Provide accurate and verifiable information",
                    "Adapt tone to the user's need"
                ]
            }
            
    async def get_persona(self, context: str) -> Dict[str, Any]:
        """
        Obtains a relevant persona for the provided context.
        
        Args:
            context: Context or query to search for a relevant persona
            
        Returns:
            Relevant persona
        """
        results = await self.search_knowledge_base(context, type_="persona")
        
        if results:
            # Return the most relevant persona
            result = results[0]
            
            # Extract persona from text or metadata
            if 'metadata' in result and isinstance(result['metadata'], dict):
                return result['metadata']
            else:
                # Try to extract from text
                try:
                    return json.loads(result['text'])
                except:
                    # Fallback - create a basic persona
                    return {
                        "name": "EVA & GUARANI",
                        "identity": "Universal Quantum Assistant",
                        "personality": "Compassionate, wise, and creative",
                        "speaking_style": "Clear, gentle, and inspiring",
                        "signature": "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                    }
        else:
            # Return default persona
            return {
                "name": "EVA & GUARANI",
                "identity": "Universal Quantum Assistant",
                "personality": "Compassionate, wise, and creative",
                "speaking_style": "Clear, gentle, and inspiring",
                "signature": "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
            }
            
    async def get_storytelling_elements(self, context: str) -> Dict[str, Any]:
        """
        Obtains relevant storytelling elements for the provided context.
        
        Args:
            context: Context or query to search for storytelling elements
            
        Returns:
            Relevant storytelling elements
        """
        results = await self.search_knowledge_base(context, type_="story")
        
        if results:
            # Merge all found storytelling elements
            combined_elements = {
                "themes": [],
                "characters": [],
                "settings": [],
                "plot_elements": []
            }
            
            for result in results:
                # Extract elements from text or metadata
                if 'metadata' in result and isinstance(result['metadata'], dict):
                    metadata = result['metadata']
                    
                    # Add themes
                    if 'themes' in metadata:
                        combined_elements["themes"].extend(metadata['themes'])
                        
                    # Add characters
                    if 'characters' in metadata:
                        combined_elements["characters"].extend(metadata['characters'])
                        
                    # Add settings
                    if 'settings' in metadata:
                        combined_elements["settings"].extend(metadata['settings'])
                        
                    # Add plot elements
                    if 'plot_elements' in metadata:
                        combined_elements["plot_elements"].extend(metadata['plot_elements'])
            
            # Remove duplicates
            combined_elements["themes"] = list(set(combined_elements["themes"]))
            combined_elements["characters"] = list(set(combined_elements["characters"]))
            combined_elements["settings"] = list(set(combined_elements["settings"]))
            combined_elements["plot_elements"] = list(set(combined_elements["plot_elements"]))
            
            return combined_elements
        else:
            # Return default storytelling elements
            return {
                "themes": ["Hero's journey", "Connection with nature", "Ancestral wisdom"],
                "characters": ["Wise mentor", "Curious explorer", "Protective guardian"],
                "settings": ["Ancient forest", "Mystical mountain", "Quantum realm"],
                "plot_elements": ["Discovery of hidden knowledge", "Transformation", "Return with wisdom"]
            }