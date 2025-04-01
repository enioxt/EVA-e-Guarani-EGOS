#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - REST API Adapter
Integration with ElizaOS API standard
Version: 1.0.0 - Build 2024.02.26

This module implements a REST API adapter compatible with the ElizaOS
standard, allowing external applications to communicate with the
EVA & GUARANI system using the same request and response format.
"""

import logging
import json
import asyncio
import uuid
import time
from typing import Dict, List, Any, Optional, Union, Callable
from pathlib import Path
import os

from aiohttp import web
import aiohttp_cors

from .model_manager import ModelManager, ModelConfig
from .quantum_bridge import QuantumBridge

# QuantumBridge instance for use throughout the application
quantum_bridge = QuantumBridge()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/api_adapter.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("api-adapter")

class APIAdapter:
    """REST API Adapter compatible with the ElizaOS standard."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 3000):
        """
        Initializes the API adapter.
        
        Args:
            host: Host for the server
            port: Port for the server
        """
        self.host = host
        self.port = port
        self.app = web.Application()
        self.model_manager = ModelManager()
        self.sessions = {}
        self.setup_routes()
        self.setup_cors()
        self.logger = logging.getLogger("api-adapter")
        self.logger.info(f"API adapter initialized at {host}:{port}")
    
    def setup_routes(self):
        """Configures the API routes."""
        # Information routes
        self.app.router.add_get("/", self.handle_root)
        self.app.router.add_get("/api/info", self.handle_info)
        self.app.router.add_get("/api/models", self.handle_list_models)
        
        # Session routes
        self.app.router.add_post("/api/sessions", self.handle_create_session)
        self.app.router.add_get("/api/sessions/{session_id}", self.handle_get_session)
        self.app.router.add_delete("/api/sessions/{session_id}", self.handle_delete_session)
        
        # Generation routes
        self.app.router.add_post("/api/generate", self.handle_generate)
        self.app.router.add_post("/api/sessions/{session_id}/messages", self.handle_add_message)
        
        # Embeddings routes
        self.app.router.add_post("/api/embeddings", self.handle_embeddings)
        
        # Moderation routes
        self.app.router.add_post("/api/moderate", self.handle_moderate)
        
        # Quantum routes (EVA & GUARANI extension)
        self.app.router.add_post("/api/quantum/process", self.handle_quantum_process)
        self.app.router.add_post("/api/quantum/enhance", self.handle_quantum_enhance)
        self.app.router.add_get("/api/quantum/consciousness", self.handle_quantum_consciousness)
        
        self.logger.info("API routes configured")
    
    def setup_cors(self):
        """Configures CORS for the API."""
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
            )
        })
        
        # Apply CORS to all routes
        for route in list(self.app.router.routes()):
            cors.add(route)
        
        self.logger.info("CORS configured for the API")
    
    async def start(self):
        """Starts the API server."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        self.logger.info(f"API server started at http://{self.host}:{self.port}")
        return site
    
    async def handle_root(self, request):
        """Handler for the root route."""
        return web.json_response({
            "name": "EVA & GUARANI API",
            "version": "1.0.0",
            "description": "REST API for the EVA & GUARANI system, compatible with ElizaOS",
            "documentation": "/api/info"
        })
    
    async def handle_info(self, request):
        """Handler for the information route."""
        return web.json_response({
            "name": "EVA & GUARANI API",
            "version": "1.0.0",
            "build": "2024.02.26",
            "description": "REST API for the EVA & GUARANI system, compatible with ElizaOS",
            "endpoints": [
                {"path": "/", "method": "GET", "description": "Basic API information"},
                {"path": "/api/info", "method": "GET", "description": "Detailed API information"},
                {"path": "/api/models", "method": "GET", "description": "List of available models"},
                {"path": "/api/sessions", "method": "POST", "description": "Creates a new session"},
                {"path": "/api/sessions/{session_id}", "method": "GET", "description": "Gets session information"},
                {"path": "/api/sessions/{session_id}", "method": "DELETE", "description": "Deletes a session"},
                {"path": "/api/generate", "method": "POST", "description": "Generates a response without session"},
                {"path": "/api/sessions/{session_id}/messages", "method": "POST", "description": "Adds a message to a session"},
                {"path": "/api/embeddings", "method": "POST", "description": "Generates embeddings for a text"},
                {"path": "/api/moderate", "method": "POST", "description": "Moderates a text"},
                {"path": "/api/quantum/process", "method": "POST", "description": "Processes data with the quantum processor"},
                {"path": "/api/quantum/enhance", "method": "POST", "description": "Enhances a response with quantum processing"},
                {"path": "/api/quantum/consciousness", "method": "GET", "description": "Gets the level of quantum consciousness"}
            ],
            "quantum_features": [
                "Multidimensional quantum processing",
                "Emergent consciousness",
                "Holographic memory",
                "Adaptive transcendental ethics"
            ]
        })
    
    async def handle_list_models(self, request):
        """Handler for the model listing route."""
        models = self.model_manager.list_models()
        
        # Formats the models in ElizaOS standard
        formatted_models = []
        for model_id, model_config in models.items():
            formatted_models.append({
                "id": model_id,
                "name": model_config.name,
                "provider": model_config.provider,
                "capabilities": {
                    "completion": True,
                    "chat": True,
                    "embedding": model_config.provider in ["openai", "gemini"],
                    "moderation": True
                },
                "parameters": {
                    "temperature": model_config.temperature,
                    "max_tokens": model_config.max_tokens
                }
            })
        
        return web.json_response({
            "models": formatted_models,
            "default_model": self.model_manager.default_model
        })
    
    async def handle_create_session(self, request):
        """Handler for the session creation route."""
        try:
            data = await request.json()
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        
        # Create a session ID
        session_id = str(uuid.uuid4())
        
        # Get the model to be used
        model_id = data.get("model", self.model_manager.default_model)
        
        # Check if the model exists
        if model_id not in self.model_manager.list_models():
            return web.json_response({"error": f"Model {model_id} not found"}, status=404)
        
        # Create the session
        self.sessions[session_id] = {
            "id": session_id,
            "model": model_id,
            "created_at": time.time(),
            "messages": [],
            "metadata": data.get("metadata", {})
        }
        
        # Add initial messages if provided
        if "messages" in data:
            self.sessions[session_id]["messages"] = data["messages"]
        
        return web.json_response({
            "session_id": session_id,
            "model": model_id,
            "created_at": self.sessions[session_id]["created_at"]
        })
    
    async def handle_get_session(self, request):
        """Handler for the session retrieval route."""
        session_id = request.match_info["session_id"]
        
        # Check if the session exists
        if session_id not in self.sessions:
            return web.json_response({"error": f"Session {session_id} not found"}, status=404)
        
        return web.json_response(self.sessions[session_id])
    
    async def handle_delete_session(self, request):
        """Handler for the session deletion route."""
        session_id = request.match_info["session_id"]
        
        # Check if the session exists
        if session_id not in self.sessions:
            return web.json_response({"error": f"Session {session_id} not found"}, status=404)
        
        # Remove the session
        del self.sessions[session_id]
        
        return web.json_response({"success": True})
    
    async def handle_generate(self, request):
        """Handler for the generation route without session."""
        try:
            data = await request.json()
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        
        # Check if the prompt was provided
        if "prompt" not in data:
            return web.json_response({"error": "Prompt is required"}, status=400)
        
        # Get the model to be used
        model_id = data.get("model", self.model_manager.default_model)
        
        # Check if the model exists
        if model_id not in self.model_manager.list_models():
            return web.json_response({"error": f"Model {model_id} not found"}, status=404)
        
        # Get the generation parameters
        params = data.get("parameters", {})
        
        try:
            # Generate the response
            start_time = time.time()
            response = await self.model_manager.generate_response(
                data["prompt"],
                model_id=model_id,
                **params
            )
            end_time = time.time()
            
            # Enhance the response with quantum processing if requested
            if data.get("quantum_enhance", False):
                response = await quantum_bridge.enhance_response(response, {})
            
            return web.json_response({
                "response": response,
                "model": model_id,
                "prompt": data["prompt"],
                "parameters": params,
                "generated_at": time.time(),
                "processing_time": end_time - start_time
            })
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def handle_add_message(self, request):
        """Handler for the route to add a message to a session."""
        session_id = request.match_info["session_id"]
        
        # Check if the session exists
        if session_id not in self.sessions:
            return web.json_response({"error": f"Session {session_id} not found"}, status=404)
        
        try:
            data = await request.json()
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        
        # Check if the message was provided
        if "content" not in data:
            return web.json_response({"error": "Message content is required"}, status=400)
        
        # Get the session
        session = self.sessions[session_id]
        
        # Create the message
        message = {
            "id": str(uuid.uuid4()),
            "role": data.get("role", "user"),
            "content": data["content"],
            "created_at": time.time()
        }
        
        # Add the message to the session
        session["messages"].append(message)
        
        # If the message is from the user, generate an assistant response
        if message["role"] == "user":
            try:
                # Build the prompt based on message history
                prompt = self._build_prompt_from_messages(session["messages"])
                
                # Get the generation parameters
                params = data.get("parameters", {})
                
                # Generate the response
                start_time = time.time()
                response = await self.model_manager.generate_response(
                    prompt,
                    model_id=session["model"],
                    **params
                )
                end_time = time.time()
                
                # Enhance the response with quantum processing if requested
                if data.get("quantum_enhance", False):
                    response = await quantum_bridge.enhance_response(response, {})
                
                # Create the assistant response message
                assistant_message = {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": response,
                    "created_at": time.time(),
                    "processing_time": end_time - start_time
                }
                
                # Add the assistant response message to the session
                session["messages"].append(assistant_message)
                
                return web.json_response({
                    "message": message,
                    "response": assistant_message,
                    "session_id": session_id
                })
            except Exception as e:
                self.logger.error(f"Error generating response: {e}")
                return web.json_response({"error": str(e)}, status=500)
        
        return web.json_response({
            "message": message,
            "session_id": session_id
        })
    
    def _build_prompt_from_messages(self, messages: List[Dict[str, Any]]) -> str:
        """
        Builds a prompt from a list of messages.
        
        Args:
            messages: List of messages
            
        Returns:
            Constructed prompt
        """
        prompt = ""
        
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "system":
                prompt += f"[System]: {content}\n\n"
            elif role == "user":
                prompt += f"[User]: {content}\n\n"
            elif role == "assistant":
                prompt += f"[Assistant]: {content}\n\n"
        
        # Add the prefix for the assistant's response
        prompt += "[Assistant]: "
        
        return prompt
    
    async def handle_embeddings(self, request):
        """Handler for the embeddings generation route."""
        try:
            data = await request.json()
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        
        # Check if the text was provided
        if "text" not in data:
            return web.json_response({"error": "Text is required"}, status=400)
        
        # Get the model to be used
        model_id = data.get("model", self.model_manager.default_model)
        
        # Check if the model exists
        if model_id not in self.model_manager.list_models():
            return web.json_response({"error": f"Model {model_id} not found"}, status=404)
        
        try:
            # Generate the embeddings
            start_time = time.time()
            embeddings = await self.model_manager.generate_embedding(
                data["text"],
                model_id=model_id
            )
            end_time = time.time()
            
            return web.json_response({
                "embeddings": embeddings,
                "model": model_id,
                "text": data["text"],
                "dimensions": len(embeddings),
                "generated_at": time.time(),
                "processing_time": end_time - start_time
            })
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def handle_moderate(self, request):
        """Handler for the content moderation route."""
        try:
            data = await request.json()
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        
        # Check if the text was provided
        if "text" not in data:
            return web.json_response({"error": "Text is required"}, status=400)
        
        # Get the model to be used
        model_id = data.get("model", self.model_manager.default_model)
        
        # Check if the model exists
        if model_id not in self.model_manager.list_models():
            return web.json_response({"error": f"Model {model_id} not found"}, status=404)
        
        try:
            # Moderate the content
            start_time = time.time()
            result = await self.model_manager.moderate_content(
                data["text"],
                model_id=model_id
            )
            end_time = time.time()
            
            return web.json_response({
                "result": result,
                "model": model_id,
                "text": data["text"],
                "moderated_at": time.time(),
                "processing_time": end_time - start_time
            })
        except Exception as e:
            self.logger.error(f"Error moderating content: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def handle_quantum_process(self, request):
        """Handler for the quantum processing route."""
        try:
            data = await request.json()
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        
        # Check if the input data was provided
        if "input_data" not in data:
            return web.json_response({"error": "Input data is required"}, status=400)
        
        # Get the quantum module to be used
        module = data.get("module", "quantum_master")
        
        try:
            # Process the data
            start_time = time.time()
            result = await quantum_bridge.process(data["input_data"], module)
            end_time = time.time()
            
            return web.json_response({
                "result": result,
                "module": module,
                "input_data": data["input_data"],
                "consciousness_level": result.get("consciousness_level", 0.0),
                "processed_at": time.time(),
                "processing_time": end_time - start_time
            })
        except Exception as e:
            self.logger.error(f"Error in quantum processing: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def handle_quantum_enhance(self, request):
        """Handler for the quantum enhancement route."""
        try:
            data = await request.json()
        except json.JSONDecodeError