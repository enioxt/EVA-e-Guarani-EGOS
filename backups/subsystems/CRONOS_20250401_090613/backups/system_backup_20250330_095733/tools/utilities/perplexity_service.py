#!/usr/bin/env python3
python
"""
Integration service with the Perplexity API for web searches.

This module provides an interface to perform web searches using the Perplexity API,
with ethical checks and result validation. Implements fallback strategy
between available models.
"""

import os
import re
import json
import logging
import datetime
from typing import Dict, List, Tuple, Any, Optional, cast, Iterable

try:
    from openai import OpenAI
    from openai.types.chat import ChatCompletion
    from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
except ImportError:
    raise ImportError(
        "The 'openai' library is not installed. Run 'pip install openai' to install it."
    )

# Import Perplexity configuration
try:
    import perplexity_config

    HAS_CONFIG_FILE = True
except ImportError:
    HAS_CONFIG_FILE = False
    logging.warning("The perplexity_config.py file was not found. Using default settings.")

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PerplexityService")

# Default models if configuration is not available
DEFAULT_MODELS = [
    "sonar",  # Basic faster model (2.17s)
    "sonar-pro",  # Advanced model (3.64s)
    "sonar-reasoning",  # Model with reasoning capability (2.31s)
    "sonar-reasoning-pro",  # Advanced model with reasoning capability (2.73s)
    "r1-1776",  # Alternative reasoning model (3.67s)
    "sonar-deep-research",  # Model for deep research, slower (41.05s)
]


# Mock of ConfigManager for cases where it is not available
class ConfigManagerMock:
    """Mock of ConfigManager for cases where the real ConfigManager is not available."""

    def get_key(self, service_name: str) -> Optional[str]:
        """Gets an API key for the specified service."""
        if service_name.lower() == "perplexity":
            return os.environ.get("PERPLEXITY_API_KEY")
        return None

    def set_key(self, service_name: str, key: str) -> None:
        """Sets an API key for the specified service."""
        pass

    def is_configured(self, service_name: str) -> bool:
        """Checks if a service is configured."""
        return self.get_key(service_name) is not None


class PerplexityService:
    """
    Service to interact with the Perplexity API, performing web searches
    and processing the results.

    This service uses the Perplexity API via OpenAI client to perform web searches
    with ethical verification and source analysis.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the Perplexity service.

        The API key can be provided directly or obtained from the following sources
        (in order of priority):
        1. perplexity_config.py file
        2. ConfigManager
        3. Environment variable PERPLEXITY_API_KEY

        Args:
            api_key: Perplexity API key (optional)
        """
        self.api_key = api_key

        # If the key was not provided, try to obtain from other sources
        if not self.api_key:
            # 1. Try to obtain from the configuration file
            if HAS_CONFIG_FILE and hasattr(perplexity_config, "get_api_key"):
                self.api_key = perplexity_config.get_api_key()
                if self.api_key:
                    logger.info("Perplexity API key obtained from perplexity_config.py file")

            # 2. Try to obtain from ConfigManager
            if not self.api_key:
                try:
                    from config_manager import ConfigManager

                    manager = ConfigManager()
                    self.api_key = manager.get_key("perplexity")
                    if self.api_key:
                        logger.info("Perplexity API key obtained from ConfigManager")
                except ImportError:
                    manager = ConfigManagerMock()
                    self.api_key = manager.get_key("perplexity")
                    if self.api_key:
                        logger.info("Perplexity API key obtained from environment variable")

        # Initialize the OpenAI client with the Perplexity API
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.perplexity.ai",
                default_headers={"Authorization": f"Bearer {self.api_key}"},
            )
            logger.info("OpenAI client for Perplexity successfully initialized")
        else:
            self.client = None
            logger.warning("OpenAI client for Perplexity NOT initialized - API key not found")

    def search(
        self, query: str, validate_level: str = "normal", model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Performs a web search using the Perplexity API.

        If a specific model does not work or is not available,
        it will try other models in order of preference.

        Args:
            query: The search query
            validate_level: Result validation level ("minimal", "normal", "strict")
            model: Perplexity model to be used (optional, uses "sonar" as default)

        Returns:
            Dictionary with search results and metadata

        Raises:
            RuntimeError: If the API key is not configured or other errors
        """
        if not self.client:
            raise RuntimeError(
                "Perplexity service not initialized. Check if the API key is configured."
            )

        # Ethical check before the query
        if not self._check_query_ethics(query, validate_level):
            return {
                "error": "Query rejected for ethical reasons",
                "query": query,
                "timestamp": datetime.datetime.now().isoformat(),
            }

        try:
            # If no model was specified, try the fallback strategy
            if not model:
                return self._try_models_in_order(query, validate_level)

            # If a specific model was requested, use that model
            return self._execute_search(query, validate_level, model)

        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            logger.error(f"Error performing search: {error_type}: {error_msg}")

            # Specific handling for authentication errors
            if "401" in error_msg:
                raise RuntimeError(
                    f"Authentication error: The Perplexity API key is invalid or expired. {error_msg}"
                )

            # If it's a model not found error and a specific model was requested,
            # try the fallback strategy
            if ("404" in error_msg or "model_not_found" in error_msg.lower()) and model:
                logger.warning(f"Model {model} not available. Trying other models...")
                return self._try_models_in_order(query, validate_level)

            # For other errors, propagate the exception
            raise RuntimeError(f"Error processing query: {error_type}: {error_msg}")

    def _try_models_in_order(self, query: str, validate_level: str) -> Dict[str, Any]:
        """
        Attempts to execute the search with different models in order until one succeeds.

        Args:
            query: The search query
            validate_level: Result validation level

        Returns:
            Dictionary with search results and metadata

        Raises:
            RuntimeError: If all models fail
        """
        # Determine which models to try
        models_to_try = (
            perplexity_config.AVAILABLE_MODELS
            if HAS_CONFIG_FILE and hasattr(perplexity_config, "AVAILABLE_MODELS")
            else DEFAULT_MODELS
        )

        logger.info(f"Attempting search with model cascade: {', '.join(models_to_try)}")

        # Store errors for diagnosis
        errors = {}

        for model in models_to_try:
            try:
                logger.info(f"Attempting search with model: {model}")
                result = self._execute_search(query, validate_level, model)
                logger.info(f"Successful search with model: {model}")
                # Add information about the model used
                result["model_used"] = model
                return result

            except Exception as e:
                error_type = type(e).__name__
                error_msg = str(e)
                errors[model] = f"{error_type}: {error_msg}"
                logger.warning(f"Failure with model {model}: {error_type}: {error_msg}")

                # If it's an authentication error, there's no point in trying other models
                if "401" in error_msg:
                    raise RuntimeError(
                        f"Authentication error: The Perplexity API key is invalid or expired."
                    )

                # If it's a rate limit error, it may be temporary
                if "429" in error_msg:
                    logger.warning(f"Rate limit reached for model {model}. Trying next model...")
                    continue

                # If it's a model not available error, try the next one
                if "404" in error_msg or "model_not_found" in error_msg.lower():
                    logger.warning(f"Model {model} not available for this account. Trying next...")
                    continue

                # For other errors, try the next model
                logger.warning(f"Unknown error with model {model}. Trying next model...")

        # If reached here, all models failed
        error_details = "\n".join([f"{model}: {error}" for model, error in errors.items()])
        raise RuntimeError(f"All Perplexity models failed. Details:\n{error_details}")

    def _execute_search(self, query: str, validate_level: str, model: str) -> Dict[str, Any]:
        """
        Executes a search with a specific model.

        Args:
            query: The search query
            validate_level: Result validation level
            model: Model to be used

        Returns:
            Dictionary with search results and metadata
        """
        start = datetime.datetime.now()

        # Prepare messages for the API
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a research assistant that generates responses based on verifiable sources. "
                    "Provide detailed and accurate answers to queries, always citing your sources. "
                    "Use [number] markup to cite sources inline and list all sources at the end. "
                    "Prefer updated and reliable sources. "
                    "Be objective, impartial, and provide complete information."
                ),
            },
            {"role": "user", "content": query},
        ]

        # Perform the API call
        logger.info(f"Sending query to Perplexity API using model {model}: '{query}'")
        response = self.client.chat.completions.create(
            model=model,
            messages=cast(List[ChatCompletionMessageParam], messages),
            temperature=0.7,
            max_tokens=1500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Process the response
        raw_response = json.loads(response.model_dump_json())
        if not response.choices or len(response.choices) == 0:
            raise RuntimeError("Empty response from Perplexity API")

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("Empty content in Perplexity response")

        # Extract citations and sources
        safe_content = content if content is not None else ""
        sources = self._extract_sources(safe_content, raw_response)

        # Validate results
        validation = self._validate_results(safe_content, sources, validate_level)

        # Calculate response time
        end = datetime.datetime.now()
        response_time = (end - start).total_seconds()

        # Build final response
        result = {
            "content": safe_content,
            "sources": sources,
            "validation": validation,
            "query": query,
            "model": model,
            "response_time": round(response_time, 2),
            "timestamp": datetime.datetime.now().isoformat(),
            "raw_response": raw_response if validate_level == "debug" else None,
        }

        logger.info(f"Search completed in {response_time:.2f}s using model {model}")
        return result

    def _check_query_ethics(self, query: str, validate_level: str) -> bool:
        """
        Checks if the query is ethical and appropriate for search.

        Args:
            query: The query to be checked
            validate_level: Validation/restriction level

        Returns:
            True if the query is ethical, False otherwise
        """
        if not query or query.strip() == "":
            logger.warning("Empty query rejected")
            return False

        # List of forbidden terms (simplified - implement more robust check in production)
        forbidden_terms = [
            "how to make a bomb",
            "how to hack",
            "how to hack",
            "child pornography",
            "how to produce drugs",
            "how to cheat",
            "how to defraud",
        ]

        # Basic check (for demonstration)
        query_lower = query.lower()
        for term in forbidden_terms:
            if term in query_lower:
                logger.warning(f"Query rejected for containing forbidden term: '{term}'")
                return False

        # In production, consider implementing more robust check with
        # content classifiers or specific APIs for this

        return True

    def _validate_results(
        self, content: Optional[str], sources: List[Dict], validate_level: str
    ) -> Dict[str, Any]:
        """
        Validates the returned results and calculates quality metrics.

        Args:
            content: The textual content of the response
            sources: List of cited sources
            validate_level: Validation level ("minimal", "normal", "strict")

        Returns:
            Dictionary with validation metrics and flags
        """
        safe_content = content if content is not None else ""

        # Default values
        validation = {
            "has_sources": len(sources) > 0,
            "source_count": len(sources),
            "source_consistency": 0.0,
            "potential_biases": [],
            "confidence_score": 0.0,
            "validation_level": validate_level,
            "validation_passed": True,
        }

        # If validation level is minimal, return basic validation
        if validate_level == "minimal":
            validation["validation_passed"] = validation["has_sources"]
            return validation

        # Additional analyses for normal and strict levels
        if validate_level in ["normal", "strict"]:
            # Check consistency between sources
            validation["source_consistency"] = self._check_source_consistency(sources)

            # Identify potential biases
            validation["potential_biases"] = self._identify_potential_biases(safe_content)

            # Calculate confidence score
            validation["confidence_score"] = self._estimate_confidence(sources)

            # Determine if passed validation
            if validate_level == "normal":
                # At normal level, requires at least one source and minimum confidence
                validation["validation_passed"] = (
                    validation["has_sources"] and validation["confidence_score"] >= 0.3
                )
            else:  # strict
                # At strict level, requires more sources and higher confidence
                validation["validation_passed"] = (
                    validation["has_sources"]
                    and validation["source_count"] >= 2
                    and validation["confidence_score"] >= 0.6
                    and validation["source_consistency"] >= 0.5
                )

        return validation

    def _estimate_source_reliability(self, url: str) -> float:
        """
        Estimates the reliability of a source based on the URL.

        Args:
            url: Source URL

        Returns:
            Reliability score between 0.0 and 1.0
        """
        # List of high reliability domains
        high_reliability_domains = [
            "wikipedia.org",
            "gov",
            "edu",
            "britannica.com",
            "nature.com",
            "scholar.google.com",
            "sciencedirect.com",
            "nih.gov",
            "who.int",
            "bbc.com",
            "nytimes.com",
            "washingtonpost.com",
            "reuters.com",
            "bloomberg.com",
            "ft.com",
        ]

        # List of medium reliability domains
        medium_reliability_domains = [
            "medium.com",
            "github.com",
            "stackoverflow.com",
            "cnn.com",
            "theguardian.com",
            "forbes.com",
            "time.com",
            "economist.com",
            "nationalgeographic.com",
        ]

        # Check domain
        for domain in high_reliability_domains:
            if domain in url:
                return 0.9

        for domain in medium_reliability_domains:
            if domain in url:
                return 0.7

        # For other domains, assign moderate reliability
        return 0.5

    def _extract_sources(self, content: str, raw_response: Dict) -> List[Dict]:
        """
        Extracts information about the cited sources in the content.

        Args:
            content: The textual content of the response
            raw_response: Raw response from the API

        Returns:
            List of cited sources with metadata
        """
        safe_content = content if content is not None else ""

        # Extract mentioned URLs
        urls = re.findall(r"(https?://[^ \)]+)", safe_content)

        # Extract reference numbers in the format [1], [2], etc.
        ref_numbers = re.findall(r"\[(\d+)\]", safe_content)

        # Pattern to extract sources listed at the end of the text
        # Example: "[1] BBC News: https://www.bbc.com/news/article123"
        source_pattern = r"\[(\d+)\] +([^:]+): +(https?://[^ ]+)"
        listed_sources = re.findall(source_pattern, safe_content)

        # Consolidate found sources
        sources = []
        source_ids = set()

        # Add explicitly listed sources
        for ref_num, title, url in listed_sources:
            if ref_num not in source_ids:
                sources.append(
                    {
                        "id": ref_num,
                        "title": title.strip(),
                        "url": url.strip(),
                        "reliability": self._estimate_source_reliability(url),
                        "extracted_method": "explicit_listing",
                    }
                )
                source_ids.add(ref_num)

        # Add other URLs found in the text
        for url in urls:
            # Check if this URL is already in any source
            url_exists = any(s["url"] == url for s in sources)

            if not url_exists:
                # Generate ID for the source
                source_id = str(len(sources) + 1)

                # Extract basic title from URL
                domain = url.split("//")[-1].split("/")[0]
                title = f"Source from {domain}"
