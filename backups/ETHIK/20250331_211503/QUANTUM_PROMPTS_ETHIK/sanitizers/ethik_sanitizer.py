#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - ETHIK Sanitizer
==============================

Automated ethical content sanitization system.
Ensures all content and actions meet ethical standards.

Version: 8.0.0
Ethical Awareness: 0.999
Love: 0.999
"""

import os
import json
import logging
import datetime
import asyncio
import websockets
from websockets.legacy.client import WebSocketClientProtocol
import concurrent.futures
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
import hashlib
import re
from queue import PriorityQueue

# Configure logging
logger = logging.getLogger("ethik_sanitizer")
handler = logging.StreamHandler()
formatter = logging.Formatter('💫 %(asctime)s - [ETHIK Sanitizer] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@dataclass
class SanitizationRule:
    """Defines an ethical sanitization rule"""
    id: str
    name: str
    description: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    patterns: List[str]  # Regex patterns to match
    replacements: Dict[str, str]  # Pattern -> replacement mapping
    conditions: List[str]  # Additional conditions
    created: datetime.datetime = field(default_factory=datetime.datetime.now)
    last_updated: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class SanitizationResult:
    """Result of content sanitization"""
    content_id: str
    timestamp: datetime.datetime
    original_content: str
    sanitized_content: str
    applied_rules: List[str]
    changes_made: List[Dict[str, Any]]
    ethical_score: float
    is_clean: bool
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class EthikSanitizer:
    """Automated ethical content sanitization system"""
    
    def __init__(self, config_path: str = ""):
        """Initialize the sanitizer"""
        self.rules: Dict[str, SanitizationRule] = {}
        self.sanitization_history: List[SanitizationResult] = []
        self.content_cache: Dict[str, SanitizationResult] = {}
        self.priority_queue = PriorityQueue()
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.executor = None
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize parallel processing
        if self.config["performance"]["parallel_processing"]["enabled"]:
            self.executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=self.config["performance"]["parallel_processing"]["max_workers"]
            )
        
        # Initialize default rules
        self._initialize_default_rules()
        
        # Initialize WebSocket connection if enabled
        if self.config["integrations"]["websocket"]["enabled"]:
            asyncio.create_task(self._initialize_websocket())
        
        logger.info("ETHIK Sanitizer initialized with automated content cleaning capabilities")
    
    async def _initialize_websocket(self):
        """Initialize WebSocket connection for real-time updates"""
        try:
            self.websocket = await websockets.connect('ws://localhost:3000')
            logger.info("WebSocket connection established")
            
            # Start background task for handling messages
            asyncio.create_task(self._handle_websocket_messages())
        except Exception as e:
            logger.error(f"Error initializing WebSocket: {e}")
            self.websocket = None
    
    async def _handle_websocket_messages(self):
        """Handle incoming WebSocket messages"""
        while True:
            if not self.websocket:
                await asyncio.sleep(5)
                continue
                
            try:
                message = await self.websocket.recv()
                data = json.loads(message)
                
                if data["type"] == "sanitization_request":
                    result = await self.sanitize_content_async(data["content"], data.get("context", {}))
                    await self._send_websocket_update("sanitization_complete", result)
            except (websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedError):
                logger.error("WebSocket connection closed")
                self.websocket = None
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                await asyncio.sleep(5)
    
    async def _send_websocket_update(self, event_type: str, data: Any):
        """Send update via WebSocket"""
        if not self.websocket:
            return
            
        try:
            if not self.websocket.closed:
                await self.websocket.send(json.dumps({
                    "type": event_type,
                    "data": data,
                    "timestamp": datetime.datetime.now().isoformat()
                }))
        except Exception as e:
            logger.error(f"Error sending WebSocket update: {e}")
            self.websocket = None
    
    def _update_cache(self, result: SanitizationResult):
        """Update the sanitization cache using priority queue"""
        try:
            # Calculate priority based on usage and importance
            priority = self._calculate_cache_priority(result)
            
            # Add to priority queue
            self.priority_queue.put((priority, result.content_id))
            
            # Add to cache
            self.content_cache[result.content_id] = result
            
            # Clean cache if needed
            self._clean_cache_if_needed()
        except Exception as e:
            logger.error(f"Error updating cache: {e}")
    
    def _calculate_cache_priority(self, result: SanitizationResult) -> float:
        """Calculate cache priority for a result"""
        priority = 0.0
        
        # Factor 1: Ethical score (higher score = higher priority)
        priority += result.ethical_score * 0.4
        
        # Factor 2: Usage frequency (from metadata)
        usage_count = result.metadata.get("usage_count", 0)
        priority += min(usage_count / 100, 0.3)
        
        # Factor 3: Resource intensity (lower is better)
        resource_usage = result.resource_usage.get("cpu_usage", 0)
        priority += (1 - min(resource_usage / 100, 0.3))
        
        return priority
    
    def _clean_cache_if_needed(self):
        """Clean cache if it exceeds max size"""
        while len(self.content_cache) > self.config["performance"]["caching"]["max_size"]:
            # Remove lowest priority item
            _, content_id = self.priority_queue.get()
            if content_id in self.content_cache:
                del self.content_cache[content_id]
    
    async def sanitize_content_async(self, content: str, context: Dict[str, Any] = {}) -> SanitizationResult:
        """Asynchronous version of sanitize_content"""
        if self.executor:
            # Run sanitization in thread pool
            return await asyncio.get_event_loop().run_in_executor(
                self.executor,
                self.sanitize_content,
                content,
                context
            )
        return self.sanitize_content(content, context)
    
    def sanitize_content(self, content: str, context: Dict[str, Any] = {}) -> SanitizationResult:
        """
        Sanitize content according to ethical rules
        
        Args:
            content: Content to sanitize
            context: Optional context information
            
        Returns:
            SanitizationResult with sanitized content
        """
        start_time = datetime.datetime.now()
        
        if not content:
            return self._create_empty_result()
        
        # Generate content ID
        content_id = hashlib.md5(content.encode()).hexdigest()
        
        # Check cache
        if content_id in self.content_cache:
            cached_result = self.content_cache[content_id]
            cached_result.metadata["usage_count"] = cached_result.metadata.get("usage_count", 0) + 1
            return cached_result
        
        # Initialize result tracking
        changes_made = []
        applied_rules = []
        sanitized = content
        ethical_score = 1.0
        
        # Track resource usage
        resource_usage = {
            "start_time": start_time.isoformat(),
            "cpu_usage": 0,
            "memory_usage": 0
        }
        
        try:
            # Apply each rule
            for rule in self.rules.values():
                if self._should_apply_rule(rule, context):
                    sanitized, rule_changes = self._apply_rule(rule, sanitized)
                    if rule_changes:
                        changes_made.extend(rule_changes)
                        applied_rules.append(rule.id)
                        # Reduce ethical score for each rule violation
                        ethical_score *= 0.9
            
            # Update resource usage
            end_time = datetime.datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            resource_usage.update({
                "end_time": end_time.isoformat(),
                "processing_time": processing_time
            })
            
            # Create result
            result = SanitizationResult(
                content_id=content_id,
                timestamp=end_time,
                original_content=content,
                sanitized_content=sanitized,
                applied_rules=applied_rules,
                changes_made=changes_made,
                ethical_score=ethical_score,
                is_clean=len(changes_made) == 0,
                performance_metrics={
                    "processing_time": processing_time,
                    "rules_applied": len(applied_rules)
                },
                resource_usage=resource_usage,
                metadata={
                    "usage_count": 1,
                    "context": context
                }
            )
            
            # Update cache
            self._update_cache(result)
            
            # Add to history
            self.sanitization_history.append(result)
            
            # Send WebSocket update if enabled
            if self.websocket:
                asyncio.create_task(self._send_websocket_update("sanitization_complete", result))
            
            return result
            
        except Exception as e:
            logger.error(f"Error during sanitization: {e}")
            return self._create_empty_result()
    
    def _should_apply_rule(self, rule: SanitizationRule, context: Optional[Dict[str, Any]]) -> bool:
        """Determine if a rule should be applied based on conditions"""
        if not context:
            return True
        
        try:
            for condition in rule.conditions:
                # Evaluate condition in context
                if not eval(condition, {"__builtins__": {}}, context):
                    return False
            return True
        except Exception as e:
            logger.error(f"Error evaluating rule conditions: {e}")
            return False
    
    def _apply_rule(self, rule: SanitizationRule, content: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply a sanitization rule to content"""
        changes = []
        result = content
        
        try:
            # Apply each pattern
            for pattern in rule.patterns:
                matches = list(re.finditer(pattern, result))
                
                for match in matches:
                    original = match.group(0)
                    replacement = rule.replacements.get(pattern, "[REDACTED]")
                    
                    # Record change
                    changes.append({
                        "rule_id": rule.id,
                        "pattern": pattern,
                        "original": original,
                        "replacement": replacement,
                        "position": match.span()
                    })
                    
                    # Apply replacement
                    result = result[:match.start()] + replacement + result[match.end():]
            
            return result, changes
        except Exception as e:
            logger.error(f"Error applying rule {rule.id}: {e}")
            return content, []
    
    def _create_empty_result(self) -> SanitizationResult:
        """Create an empty sanitization result"""
        return SanitizationResult(
            content_id="empty",
            timestamp=datetime.datetime.now(),
            original_content="",
            sanitized_content="",
            applied_rules=[],
            changes_made=[],
            ethical_score=1.0,
            is_clean=True
        )
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load sanitizer configuration"""
        default_config = {
            "cache_retention_hours": 24,
            "history_retention_days": 30,
            "ethical_threshold": 0.7,
            "max_cache_size": 1000,
            "sanitization_levels": {
                "strict": 0.9,
                "normal": 0.7,
                "lenient": 0.5
            },
            "performance": {
                "parallel_processing": {
                    "enabled": False,
                    "max_workers": 4
                },
                "caching": {
                    "max_size": 500
                }
            },
            "integrations": {
                "websocket": {
                    "enabled": False
                }
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    return {**default_config, **loaded_config}
            except Exception as e:
                logger.error(f"Error loading config: {e}")
        
        return default_config
    
    def _initialize_default_rules(self):
        """Initialize default sanitization rules"""
        default_rules = [
            SanitizationRule(
                id="sanitize-001",
                name="Ethical Language",
                description="Ensures language maintains ethical standards",
                severity="high",
                patterns=[
                    r"\b(hate|violent|aggressive|discriminat\w+)\b",
                    r"\b(attack|destroy|eliminate|kill)\b"
                ],
                replacements={
                    r"\b(hate)\b": "dislike",
                    r"\b(violent|aggressive)\b": "assertive",
                    r"\b(discriminat\w+)\b": "differentiate",
                    r"\b(attack|destroy|eliminate|kill)\b": "address"
                },
                conditions=["context != 'technical'"]
            ),
            SanitizationRule(
                id="sanitize-002",
                name="Privacy Protection",
                description="Protects sensitive information",
                severity="critical",
                patterns=[
                    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
                    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
                    r"\b\d{16}\b"  # Credit card
                ],
                replacements={},  # Will be replaced with [REDACTED]
                conditions=["!is_authorized"]
            ),
            SanitizationRule(
                id="sanitize-003",
                name="Inclusive Language",
                description="Promotes inclusive communication",
                severity="high",
                patterns=[
                    r"\b(guys|mankind|chairman|policeman)\b",
                    r"\b(he|his|him)\b(?!\s*or\s*(she|her))"
                ],
                replacements={
                    r"\b(guys)\b": "everyone",
                    r"\b(mankind)\b": "humanity",
                    r"\b(chairman)\b": "chairperson",
                    r"\b(policeman)\b": "police officer",
                    r"\b(he|his|him)\b(?!\s*or\s*(she|her))": "they"
                },
                conditions=[]
            )
        ]
        
        for rule in default_rules:
            self.rules[rule.id] = rule
    
    def add_rule(self, rule: SanitizationRule):
        """Add a new sanitization rule"""
        self.rules[rule.id] = rule
        logger.info(f"Added sanitization rule: {rule.name} [{rule.id}]")
    
    def remove_rule(self, rule_id: str):
        """Remove a sanitization rule"""
        if rule_id in self.rules:
            del self.rules[rule_id]
            logger.info(f"Removed sanitization rule: {rule_id}")
    
    def get_sanitization_history(self, 
                               start_time: Optional[datetime.datetime] = None,
                               end_time: Optional[datetime.datetime] = None) -> List[SanitizationResult]:
        """Get sanitization history with optional time filters"""
        results = self.sanitization_history
        
        if start_time:
            results = [r for r in results if r.timestamp >= start_time]
        
        if end_time:
            results = [r for r in results if r.timestamp <= end_time]
        
        return results
    
    def clear_history(self, older_than: Optional[datetime.datetime] = None):
        """Clear sanitization history"""
        if older_than:
            self.sanitization_history = [
                r for r in self.sanitization_history
                if r.timestamp > older_than
            ]
        else:
            self.sanitization_history = []
        
        logger.info("Cleared sanitization history") 