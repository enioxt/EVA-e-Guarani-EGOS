#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Adaptive Model Selector
=======================================

Module responsible for the intelligent selection of models based on query complexity,
usage context, and available resources, aiming to optimize:
- Cost savings
- Response performance
- Context-appropriate quality

Version: 2.0
Awareness: 0.990
Adaptability: 0.995
"""

import os
import json
import re
import math
import logging
import datetime
from typing import Dict, List, Any, Optional, Tuple
import tiktoken

# Configure logging
logger = logging.getLogger("adaptive_model_selector")
handler = logging.StreamHandler()
formatter = logging.Formatter("🔄 %(asctime)s - [MODEL] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class ModelProfile:
    """Profile of an AI model with its characteristics."""

    def __init__(
        self,
        name: str,
        capabilities: Dict[str, float],
        cost_per_1k_tokens: float,
        context_length: int,
        latency: float,
        specialties: List[str] = None,
    ):
        self.name = name
        self.capabilities = capabilities  # Dict of capabilities (0-1)
        self.cost_per_1k_tokens = cost_per_1k_tokens
        self.context_length = context_length
        self.latency = latency  # Average latency in seconds
        self.specialties = specialties or []

    def capability_score(self, required_capabilities: Dict[str, float]) -> float:
        """Calculates the model's suitability score for required capabilities."""
        if not required_capabilities:
            return 0.5  # Neutral score

        scores = []
        for cap, weight in required_capabilities.items():
            if cap in self.capabilities:
                scores.append(self.capabilities[cap] * weight)
            else:
                scores.append(0.3 * weight)  # Default value for unspecified capability

        return sum(scores) / sum(required_capabilities.values())

    def specialty_score(self, query_topics: List[str]) -> float:
        """Calculates the model's specialty score for the query topics."""
        if not query_topics or not self.specialties:
            return 0.5  # Neutral score

        matches = sum(
            1
            for topic in query_topics
            if any(specialty in topic.lower() for specialty in self.specialties)
        )
        return min(1.0, matches / len(query_topics) if query_topics else 0)

    def cost_score(self, budget_sensitivity: float) -> float:
        """Calculates the cost score (inverse - lower is better)."""
        # Normalized for typical cost values (0.001 to 0.1)
        normalized_cost = min(1.0, self.cost_per_1k_tokens / 0.1)
        return 1.0 - (normalized_cost * budget_sensitivity)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the profile to a dictionary."""
        return {
            "name": self.name,
            "capabilities": self.capabilities,
            "cost_per_1k_tokens": self.cost_per_1k_tokens,
            "context_length": self.context_length,
            "latency": self.latency,
            "specialties": self.specialties,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelProfile":
        """Creates an instance of ModelProfile from a dictionary."""
        return cls(
            name=data["name"],
            capabilities=data["capabilities"],
            cost_per_1k_tokens=data["cost_per_1k_tokens"],
            context_length=data["context_length"],
            latency=data["latency"],
            specialties=data.get("specialties", []),
        )


class AdaptiveModelSelector:
    """Adaptive model selector based on context and complexity."""

    def __init__(
        self,
        config_path: str = "config/model_profiles.json",
        default_model: str = "gpt-4o",
        cache_dir: str = "data/model_selection",
    ):
        self.config_path = config_path
        self.default_model = default_model
        self.cache_dir = cache_dir

        # Ensure the cache directory exists
        os.makedirs(cache_dir, exist_ok=True)

        # Load model profiles
        self.model_profiles = self._load_model_profiles()

        # Internal state
        self.query_history = []
        self.last_selections = {}
        self.selection_stats = {
            "total_queries": 0,
            "total_tokens_saved": 0,
            "total_cost_saved": 0.0,
            "model_distribution": {},
        }

        # Initialize tokenizers
        self.tokenizers = {}

        logger.info(f"Adaptive selector initialized with {len(self.model_profiles)} model profiles")

    def _load_model_profiles(self) -> Dict[str, ModelProfile]:
        """Loads model profiles from the configuration file."""
        profiles = {}

        # Define default profiles in case of read failure
        default_profiles = {
            "gpt-4o": ModelProfile(
                name="gpt-4o",
                capabilities={
                    "reasoning": 0.95,
                    "creativity": 0.92,
                    "knowledge": 0.96,
                    "coding": 0.94,
                    "ethics": 0.97,
                    "multimodal": 0.90,
                },
                cost_per_1k_tokens=0.01,
                context_length=128000,
                latency=1.5,
                specialties=["reasoning", "ethics", "latest knowledge"],
            ),
            "gpt-3.5-turbo": ModelProfile(
                name="gpt-3.5-turbo",
                capabilities={
                    "reasoning": 0.75,
                    "creativity": 0.8,
                    "knowledge": 0.7,
                    "coding": 0.8,
                    "ethics": 0.75,
                    "multimodal": 0.0,
                },
                cost_per_1k_tokens=0.001,
                context_length=16000,
                latency=1.0,
                specialties=["speed", "basic coding"],
            ),
            "text-embedding-3-large": ModelProfile(
                name="text-embedding-3-large",
                capabilities={"embedding": 0.97, "semantic_search": 0.98, "clustering": 0.95},
                cost_per_1k_tokens=0.00013,
                context_length=8000,
                latency=0.5,
                specialties=["embeddings", "semantic search"],
            ),
        }

        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    profiles_data = json.load(f)

                for name, profile_data in profiles_data.items():
                    profiles[name] = ModelProfile.from_dict(profile_data)

                logger.info(f"Loaded {len(profiles)} model profiles from {self.config_path}")
            else:
                # Use default profiles
                logger.warning(
                    f"Configuration file {self.config_path} not found. Using default profiles."
                )
                profiles = default_profiles

                # Save default profiles
                self._save_default_profiles(default_profiles)
        except Exception as e:
            logger.error(f"Error loading model profiles: {e}")
            profiles = default_profiles

        return profiles

    def _save_default_profiles(self, profiles: Dict[str, ModelProfile]) -> None:
        """Saves default profiles to the configuration file."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            # Convert profiles to dictionary
            profiles_dict = {name: profile.to_dict() for name, profile in profiles.items()}

            # Save to file
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(profiles_dict, f, indent=2)

            logger.info(f"Default profiles saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving default profiles: {e}")

    def get_tokenizer(self, model_name: str):
        """Obtains a tokenizer for the specified model."""
        if model_name not in self.tokenizers:
            try:
                self.tokenizers[model_name] = tiktoken.encoding_for_model(model_name)
            except:
                # Fallback to generic tokenizer
                self.tokenizers[model_name] = tiktoken.get_encoding("cl100k_base")

        return self.tokenizers[model_name]

    def count_tokens(self, text: str, model_name: str = "gpt-4o") -> int:
        """Counts tokens in a text for a specific model."""
        if not text:
            return 0

        tokenizer = self.get_tokenizer(model_name)
        return len(tokenizer.encode(text))

    def analyze_query_complexity(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyzes the complexity of a query."""
        if not context:
            context = {}

        # Basic analysis
        token_count = self.count_tokens(query)
        sentence_count = len(re.split(r"[.!?]+", query))
        avg_sentence_length = token_count / max(1, sentence_count)

        # Complexity analysis
        complexity_indicators = {
            "reasoning": sum(
                query.lower().count(word)
                for word in ["why", "because", "how", "explain", "compare", "analyze", "evaluate"]
            ),
            "creativity": sum(
                query.lower().count(word)
                for word in ["create", "invent", "imagine", "develop", "design", "creative"]
            ),
            "knowledge": sum(
                query.lower().count(word)
                for word in ["what is", "who was", "when", "where", "define", "describe"]
            ),
            "coding": sum(
                query.lower().count(word)
                for word in [
                    "code",
                    "function",
                    "program",
                    "bug",
                    "error",
                    "debug",
                    "optimize",
                    "refactor",
                ]
            ),
            "ethics": sum(
                query.lower().count(word)
                for word in ["ethical", "moral", "right", "wrong", "principle", "value", "impact"]
            ),
        }

        # Complexity score calculation (0-1)
        complexity_score = min(
            1.0,
            (
                0.1 * min(1.0, token_count / 100)  # Normalized length
                + 0.3 * min(1.0, avg_sentence_length / 20)  # Sentence complexity
                + 0.6 * min(1.0, sum(complexity_indicators.values()) / 10)  # Complexity indicators
            ),
        )

        # Estimate tokens needed for response
        estimated_response_tokens = int(token_count * (1.0 + complexity_score * 3))

        # Detect main topics
        topics = self._extract_topics(query)

        return {
            "token_count": token_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": avg_sentence_length,
            "complexity_score": complexity_score,
            "complexity_indicators": complexity_indicators,
            "estimated_response_tokens": estimated_response_tokens,
            "topics": topics,
        }

    def _extract_topics(self, query: str) -> List[str]:
        """Extracts main topics from a query."""
        # Simplified implementation - in a real system, more advanced NLP would be used
        lowercase = query.lower()

        topics = []
        topic_keywords = {
            "programming": ["code", "program", "function", "variable", "class", "object", "api"],
            "ethics": ["ethics", "moral", "value", "principle", "impact", "society"],
            "creativity": ["creative", "art", "design", "aesthetic", "innovation", "idea"],
            "science": ["science", "physics", "chemistry", "biology", "experiment", "theory"],
            "philosophy": ["philosophy", "existence", "metaphysics", "epistemology", "logic"],
            "technology": ["technology", "artificial intelligence", "ai", "robot", "automation"],
            "business": ["business", "company", "strategy", "market", "product", "customer"],
        }

        for topic, keywords in topic_keywords.items():
            if any(keyword in lowercase for keyword in keywords):
                topics.append(topic)

        return topics

    def select_model(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Selects the most appropriate model based on the query and context.

        Parameters:
            query: The user's query
            context: Additional context (optional)

        Returns:
            The name of the selected model and selection metadata
        """
        if not context:
            context = {}

        # Analyze query complexity
        complexity_analysis = self.analyze_query_complexity(query, context)

        # Get budget sensitivity from context (0-1)
        budget_sensitivity = context.get("budget_sensitivity", 0.5)

        # Define required capabilities based on analysis
        required_capabilities = {}
        for indicator, value in complexity_analysis["complexity_indicators"].items():
            if value > 0:
                required_capabilities[indicator] = min(1.0, value / 5)  # Normalize

        # If no required capabilities, set neutral base
        if not required_capabilities:
            required_capabilities = {"reasoning": 0.5, "knowledge": 0.5}

        # Scores for each model
        model_scores = {}
        for name, profile in self.model_profiles.items():
            # Calculate individual scores
            capability_score = profile.capability_score(required_capabilities)
            specialty_score = profile.specialty_score(complexity_analysis["topics"])
            cost_score = profile.cost_score(budget_sensitivity)

            # Composite score (adjustable weights)
            if complexity_analysis["complexity_score"] > 0.7:
                # For complex queries, prioritize capability
                weights = {"capability": 0.6, "specialty": 0.3, "cost": 0.1}
            elif budget_sensitivity > 0.7:
                # For high budget sensitivity, prioritize cost
                weights = {"capability": 0.3, "specialty": 0.2, "cost": 0.5}
            else:
                # Balanced by default
                weights = {"capability": 0.4, "specialty": 0.3, "cost": 0.3}

            composite_score = (
                weights["capability"] * capability_score
                + weights["specialty"] * specialty_score
                + weights["cost"] * cost_score
            )

            model_scores[name] = {
                "composite_score": composite_score,
                "capability_score": capability_score,
                "specialty_score": specialty_score,
                "cost_score": cost_score,
                "weights": weights,
            }

        # Select the model with the highest composite score
        if model_scores:
            selected_model = max(model_scores.items(), key=lambda x: x[1]["composite_score"])
            model_name = selected_model[0]
            selection_scores = selected_model[1]
        else:
            # Fallback to default model
            model_name = self.default_model
            selection_scores = {"note": "Using default model, no scores available"}

        # Log selection
        selection_metadata = {
            "model": model_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "query_tokens": complexity_analysis["token_count"],
            "complexity_score": complexity_analysis["complexity_score"],
            "estimated_response_tokens": complexity_analysis["estimated_response_tokens"],
            "selection_scores": selection_scores,
            "topics": complexity_analysis["topics"],
        }

        self._update_selection_stats(model_name, selection_metadata)

        logger.info(
            f"Model selected: {model_name} (complexity: {complexity_analysis['complexity_score']:.2f})"
        )

        return model_name, selection_metadata

    def _update_selection_stats(self, model_name: str, metadata: Dict[str, Any]) -> None:
        """Updates model selection statistics."""
        self.selection_stats["total_queries"] += 1

        # Update model distribution
        if model_name not in self.selection_stats["model_distribution"]:
            self.selection_stats["model_distribution"][model_name] = 0
        self.selection_stats["model_distribution"][model_name] += 1

        # Update query history (limited to 100 entries)
        self.query_history.append(
            {
                "timestamp": metadata["timestamp"],
                "model": model_name,
                "complexity": metadata["complexity_score"],
                "tokens": metadata["query_tokens"],
            }
        )

        if len(self.query_history) > 100:
            self.query_history.pop(0)

        # Calculate savings (if a more economical model was chosen)
        if model_name != "gpt-4o" and "gpt-4o" in self.model_profiles:
            token_estimate = metadata["query_tokens"] + metadata["estimated_response_tokens"]
            cost_per_1k_default = self.model_profiles["gpt-4o"].cost_per_1k_tokens
            cost_per_1k_selected = self.model_profiles[model_name].cost_per_1k_tokens

            tokens_saved = 0  # Tokens are the same, we save on cost per token
            cost_saved = (cost_per_1k_default - cost_per_1k_selected) * (token_estimate / 1000)

            self.selection_stats["total_tokens_saved"] += tokens_saved
            self.selection_stats["total_cost_saved"] += cost_saved

    def get_selection_stats(self) -> Dict[str, Any]:
        """Obtains model selection statistics."""
        return self.selection_stats

    def save_stats(self) -> None:
        """Saves statistics to file."""
        stats_file = os.path.join(
            self.cache_dir, f"selection_stats_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        )

        try:
            with open(stats_file, "w", encoding="utf-8") as f:
                json.dump(self.selection_stats, f, indent=2)
            logger.info(f"Selection statistics saved to {stats_file}")
        except Exception as e:
            logger.error(f"Error saving statistics: {e}")

    def get_model_details(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Obtains details of a specific model."""
        if model_name in self.model_profiles:
            return self.model_profiles[model_name].to_dict()
        return
