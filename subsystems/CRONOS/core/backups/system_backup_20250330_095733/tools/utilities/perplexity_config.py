#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configurations for the Perplexity API service.

This module contains all the configurations and constants necessary to
interact with the Perplexity API, including keys, available models,
and helper functions for model selection.
"""

import os
import logging
from typing import List, Dict, Any, Optional, Callable, TypeVar, cast

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PerplexityConfig")

# API key for the Perplexity service (replace with your actual key)
PERPLEXITY_API_KEY = "NWWFSoofq7r0u3bADTnS0HjpmhRCpO15ayix68imdbnJLSDK"  # Replace with the actual value for local testing

# Base URL of the API
API_BASE_URL = "https://api.perplexity.ai"

# Available models (all confirmed as available for this account)
AVAILABLE_MODELS = [
    "sonar",                # Basic faster model (2.17s)
    "sonar-pro",            # Advanced model (3.64s)
    "sonar-reasoning",      # Model with reasoning capability (2.31s)
    "sonar-reasoning-pro",  # Advanced model with reasoning capability (2.73s)
    "r1-1776",              # Alternative reasoning model (3.67s)
    "sonar-deep-research"   # Model for deep research, slower (41.05s)
]

# Default model for general use
DEFAULT_MODEL = "sonar"  # Fastest and suitable for simple queries

# Recommended models for specific tasks
SEARCH_MODEL = "sonar"  # For quick searches
REASONING_MODEL = "sonar-reasoning"  # For answers requiring reasoning
RESEARCH_MODEL = "sonar-deep-research"  # For detailed and in-depth research
PREMIUM_MODEL = "sonar-pro"  # For higher quality results in general queries

# Request configurations
MAX_TOKENS = 1000
TIMEOUT = 120  # Timeout in seconds (increased to accommodate the deep-research model)
MAX_RETRIES = 3

# Function to obtain the API key from different sources
def get_api_key() -> Optional[str]:
    """
    Retrieves the Perplexity API key from various possible sources,
    in the following order: variable in this file, environment variable, external configuration file.
    
    Returns:
        Optional[str]: The API key if found, or None otherwise.
    """
    # 1. Check if there is a key defined in this file
    if PERPLEXITY_API_KEY and PERPLEXITY_API_KEY != "INSIRA_SUA_CHAVE_API_AQUI":
        logger.info("Using API key defined in the file perplexity_config.py")
        return PERPLEXITY_API_KEY
    
    # 2. Check environment variable
    env_key = os.environ.get("PERPLEXITY_API_KEY")
    if env_key:
        logger.info("Using API key defined in the environment variable PERPLEXITY_API_KEY")
        return env_key
    
    # 3. Try to import from a possible configuration manager
    try:
        from config_manager import ConfigManager
        manager = ConfigManager()
        config_key = manager.get_key("perplexity")
        if config_key:
            logger.info("Using API key obtained from ConfigManager")
            return config_key
    except ImportError:
        pass
    
    logger.warning("No Perplexity API key found")
    return None

def is_configured() -> bool:
    """
    Checks if the API key is configured and available.
    
    Returns:
        bool: True if the key is configured, False otherwise.
    """
    key = get_api_key()
    return key is not None and len(key) > 0

def get_model_for_task(task_type: str = "general") -> str:
    """
    Returns the most suitable model for a specific type of task.
    
    Args:
        task_type (str): The type of task: "general", "search", "reasoning", "research", or "premium"
    
    Returns:
        str: The name of the recommended model for the specified task.
    """
    if task_type == "search":
        return SEARCH_MODEL
    elif task_type == "reasoning":
        return REASONING_MODEL
    elif task_type == "research":
        return RESEARCH_MODEL
    elif task_type == "premium":
        return PREMIUM_MODEL
    else:
        return DEFAULT_MODEL

T = TypeVar('T')
def try_models_in_order(api_function: Callable[..., T], models: Optional[List[str]] = None, *args: Any, **kwargs: Any) -> T:
    """
    Attempts to execute a function with different models in order until one succeeds.
    
    Args:
        api_function: The API function to be called
        models: List of models to try (if None, uses AVAILABLE_MODELS)
        *args, **kwargs: Arguments to pass to the function
    
    Returns:
        The result of the first successful function call
        
    Raises:
        Exception: If all models fail, raises the last captured exception
    """
    models_to_try = models or AVAILABLE_MODELS
    last_exception = None
    
    for model in models_to_try:
        try:
            logger.info(f"Attempting to execute with model: {model}")
            # Ensured that key is not None as is_configured() returned True
            kwargs["model"] = model
            result = api_function(*args, **kwargs)
            logger.info(f"Successful execution with model: {model}")
            return result
        except Exception as e:
            logger.warning(f"Failed to use model {model}: {str(e)}")
            last_exception = e
    
    if last_exception:
        logger.error(f"All models failed. Last exception: {str(last_exception)}")
        raise last_exception
    
    # This point should not be reached, but to satisfy the type checker
    raise ValueError("No available model to try")

# Test code - run this file directly to check configuration
if __name__ == "__main__":
    if is_configured():
        key = get_api_key()
        # Here we ensure that key is not None, since is_configured() returned True
        masked_key = key[:4] + "..." + key[-4:] if key and len(key) > 8 else "****"
        logger.info(f"Perplexity API key configured: {masked_key}")
        logger.info(f"Default model: {DEFAULT_MODEL}")
        logger.info(f"Available models: {', '.join(AVAILABLE_MODELS)}")
    else:
        logger.error("Perplexity API key not configured.")
        logger.info("Please configure the API key in one of the following ways:")
        logger.info("1. Set the environment variable PERPLEXITY_API_KEY")
        logger.info("2. Edit this file and update the PERPLEXITY_API_KEY variable")