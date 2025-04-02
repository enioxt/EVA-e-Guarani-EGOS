import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
import asyncio

# Replace the koios logger with standard logging for testing
# from koios.logger import KoiosLogger

# Create dummy classes if mycelium can't be imported
try:
    from mycelium import MyceliumClient, Message, Topic
except ImportError:
    # Mock the mycelium imports for tests
    class Message:
        def __init__(self, id, data):
            self.id = id
            self.data = data

    class Topic:
        def __init__(self, name):
            self.name = name

    class MyceliumClient:
        def __init__(self):
            self.published_messages = []
            self.subscriptions = {}
            
        def subscribe(self, topic: str):
            def decorator(func):
                self.subscriptions[topic] = func
                return func
            return decorator
            
        async def publish(self, topic: str, data: dict):
            self.published_messages.append({
                "topic": topic,
                "data": data,
                "timestamp": datetime.now().isoformat()
            })

class AtlasCartographer:
    """System cartography and relationship mapping."""
    
    def __init__(self, config_path: Optional[Path] = None, mycelium_client: Optional[MyceliumClient] = None):
        """Initialize the cartographer with configuration and Mycelium client.
        
        Args:
            config_path (Optional[Path]): Path to configuration file
            mycelium_client (Optional[MyceliumClient]): Mycelium client for messaging
        """
        # Use standard logging for testing
        self.logger = logging.getLogger("ATLAS.Cartographer")
        self.mycelium = mycelium_client
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize system map
        self.system_map = {}
        self.relationships = {}
        self.metadata = {}
        self.analysis_cache = {}
        
        # Setup Mycelium handlers if client provided
        if self.mycelium:
            self.topics = self.config["mycelium"]["topics"]
            self._setup_mycelium_handlers()
            
        self.logger.info("AtlasCartographer initialized")
        
    def _setup_mycelium_handlers(self):
        """Setup handlers for Mycelium messages."""
        
        @self.mycelium.subscribe(self.topics["map_request"])
        async def handle_map_request(message: Message):
            """Handle incoming mapping requests."""
            try:
                self.logger.info(f"Received mapping request: {message.id}")
                
                # Extract mapping parameters
                target = message.data["target"]
                depth = message.data.get("depth", 1)
                include_metadata = message.data.get("include_metadata", True)
                
                # Generate map
                map_result = await self.generate_map(target, depth, include_metadata)
                
                # Publish result
                await self.mycelium.publish(
                    self.topics["map_result"],
                    {
                        "request_id": message.id,
                        "target": target,
                        "map": map_result,
                        "timestamp": datetime.now().isoformat()
                    }
                )
                
            except Exception as e:
                self.logger.error(f"Error handling map request: {e}", exc_info=True)
                await self.mycelium.publish(
                    self.topics["map_result"],
                    {
                        "request_id": message.id,
                        "status": "error",
                        "error": str(e)
                    }
                )
                
        @self.mycelium.subscribe(self.topics["metadata_update"])
        async def handle_metadata_update(message: Message):
            """Handle metadata update requests."""
            try:
                self.logger.info(f"Received metadata update: {message.id}")
                
                # Check for required fields
                if "component" not in message.data:
                    raise ValueError("Missing 'component' field in metadata update request")
                if "metadata" not in message.data:
                    raise ValueError("Missing 'metadata' field in metadata update request")
                
                # Update metadata
                component = message.data["component"]
                metadata = message.data["metadata"]
                await self.update_metadata(component, metadata)
                
                # Publish confirmation
                await self.mycelium.publish(
                    self.topics["metadata_status"],
                    {
                        "request_id": message.id,
                        "status": "success",
                        "component": component
                    }
                )
                
            except Exception as e:
                self.logger.error(f"Error handling metadata update: {e}", exc_info=True)
                await self.mycelium.publish(
                    self.topics["metadata_status"],
                    {
                        "request_id": message.id,
                        "status": "error",
                        "error": str(e)
                    }
                )
                
        @self.mycelium.subscribe(self.topics["relationship_update"])
        async def handle_relationship_update(message: Message):
            """Handle relationship update requests."""
            try:
                self.logger.info(f"Received relationship update: {message.id}")
                
                # Check for required fields
                if "source" not in message.data:
                    raise ValueError("Missing 'source' field in relationship update request")
                if "target" not in message.data:
                    raise ValueError("Missing 'target' field in relationship update request")
                if "type" not in message.data:
                    raise ValueError("Missing 'type' field in relationship update request")
                
                # Update relationship
                source = message.data["source"]
                target = message.data["target"]
                relationship_type = message.data["type"]
                metadata = message.data.get("metadata", {})
                
                await self.update_relationship(source, target, relationship_type, metadata)
                
                # Publish confirmation
                await self.mycelium.publish(
                    self.topics["relationship_status"],
                    {
                        "request_id": message.id,
                        "status": "success",
                        "source": source,
                        "target": target
                    }
                )
                
            except Exception as e:
                self.logger.error(f"Error handling relationship update: {e}", exc_info=True)
                await self.mycelium.publish(
                    self.topics["relationship_status"],
                    {
                        "request_id": message.id,
                        "status": "error",
                        "error": str(e)
                    }
                )
    
    async def _publish_alert(self, alert_type: str, message: str, details: Dict[str, Any]):
        """Publish an alert through Mycelium."""
        if not self.mycelium:
            return
            
        try:
            await self.mycelium.publish(
                self.topics["alert"],
                {
                    "type": alert_type,
                    "message": message,
                    "details": details,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            self.logger.error(f"Failed to publish alert: {e}")
    
    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "max_depth": 5,
            "cache_duration": 300,
            "mycelium": {
                "topics": {
                    "map_request": "atlas.map.request",
                    "map_result": "atlas.map.result",
                    "metadata_update": "atlas.metadata.update",
                    "metadata_status": "atlas.metadata.status",
                    "relationship_update": "atlas.relationship.update",
                    "relationship_status": "atlas.relationship.status",
                    "alert": "atlas.alert"
                }
            }
        }
        
        if config_path and config_path.exists():
            try:
                with open(config_path) as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    self._deep_merge(default_config, loaded_config)
            except Exception as e:
                self.logger.error(f"Error loading config from {config_path}: {e}. Using defaults.")
                
        return default_config
        
    def _deep_merge(self, base: Dict, update: Dict) -> None:
        """Recursively merge update dict into base dict."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
                
    async def generate_map(self, target: str, depth: int = 1, include_metadata: bool = True) -> Dict[str, Any]:
        """Generate a map of the system starting from the target component."""
        try:
            # Check cache first
            cache_key = f"{target}:{depth}:{include_metadata}"
            if cache_key in self.analysis_cache:
                cache_entry = self.analysis_cache[cache_key]
                cache_age = (datetime.now() - cache_entry["timestamp"]).total_seconds()
                
                if cache_age < self.config["cache_duration"]:
                    self.logger.info(f"Returning cached map for {target} (age: {cache_age:.1f}s)")
                    return cache_entry["result"]
                else:
                    self.logger.info(f"Cache expired for {target} (age: {cache_age:.1f}s)")
            
            if depth > self.config["max_depth"]:
                depth = self.config["max_depth"]
                await self._publish_alert(
                    "map_depth_limited",
                    f"Map depth limited to {self.config['max_depth']} for target {target}",
                    {"target": target, "requested_depth": depth}
                )
                
            visited = set()
            result = await self._build_map_recursive(target, depth, visited, include_metadata)
            
            # Update cache
            self.analysis_cache[cache_key] = {
                "result": result,
                "timestamp": datetime.now()
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating map for {target}: {e}", exc_info=True)
            raise
            
    async def _build_map_recursive(self, target: str, depth: int, visited: Set[str], include_metadata: bool) -> Dict[str, Any]:
        """Build a map recursively (internal implementation for testing)."""
        # This is a stub method that just wraps _map_component for testing mocking purposes
        result = {
            "nodes": {},
            "relationships": [],
            "metadata": {} if include_metadata else None
        }
        await self._map_component(target, depth, visited, result, include_metadata)
        return result
        
    async def _map_component(self, component: str, depth: int, visited: Set[str], result: Dict[str, Any], include_metadata: bool):
        """Recursively map a component and its relationships."""
        if depth < 0 or component in visited:
            return
            
        visited.add(component)
        
        # Only add to nodes if it exists in the system_map
        if component in self.system_map:
            result["nodes"][component] = self.system_map[component]
        
            # Only add metadata for components that exist
            if include_metadata and component in self.metadata:
                result["metadata"][component] = self.metadata[component]
            
        if component in self.relationships:
            for rel in self.relationships[component]:
                result["relationships"].append(rel)
                target = rel["target"]
                if target not in visited:
                    await self._map_component(target, depth - 1, visited, result, include_metadata)
                    
    async def update_metadata(self, component: str, metadata: Dict[str, Any]):
        """Update metadata for a component."""
        try:
            # Invalidate cache entries for this component
            self._invalidate_cache_for_component(component)
            
            self.metadata[component] = metadata
            self.logger.info(f"Updated metadata for {component}")
            
        except Exception as e:
            self.logger.error(f"Error updating metadata for {component}: {e}", exc_info=True)
            raise
            
    async def update_relationship(self, source: str, target: str, relationship_type: str, metadata: Dict[str, Any] = None):
        """Update or create a relationship between components."""
        try:
            # Invalidate cache entries for source and target
            self._invalidate_cache_for_component(source)
            self._invalidate_cache_for_component(target)
            
            if source not in self.relationships:
                self.relationships[source] = []
                
            # Update existing relationship or add new one
            relationship = {
                "source": source,
                "target": target,
                "type": relationship_type,
                "metadata": metadata or {}
            }
            
            # Remove existing relationship if present
            self.relationships[source] = [r for r in self.relationships[source] if r["target"] != target or r["type"] != relationship_type]
            self.relationships[source].append(relationship)
            
            self.logger.info(f"Updated relationship: {source} -> {target} ({relationship_type})")
            
        except Exception as e:
            self.logger.error(f"Error updating relationship {source} -> {target}: {e}", exc_info=True)
            raise
            
    def _invalidate_cache_for_component(self, component: str):
        """Invalidate cache entries related to a specific component."""
        keys_to_remove = []
        for key in self.analysis_cache:
            if key.startswith(f"{component}:"):
                keys_to_remove.append(key)
                
        for key in keys_to_remove:
            del self.analysis_cache[key]
            self.logger.debug(f"Invalidated cache entry: {key}") 