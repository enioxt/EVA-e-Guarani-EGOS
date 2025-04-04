#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to test all available models from the Perplexity API.
This script tests each model available in the documentation and checks which are accessible for your account.
"""

import os
import sys
import json
import logging
import datetime
from importlib.util import spec_from_file_location, module_from_spec
import traceback
import pytest
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PerplexityModelTest")

# List of all documented Perplexity models
ALL_MODELS = [
    "sonar",
    "sonar-pro",
    "sonar-reasoning",
    "sonar-reasoning-pro",
    "sonar-deep-research",
    "r1-1776",  # Offline model - may not use search subsystem
]


def import_config(config_path: Path) -> Optional[Any]:
    """
    Dynamically imports a configuration module.

    Args:
        config_path: Path to the configuration file

    Returns:
        Imported module or None if it fails
    """
    try:
        spec = spec_from_file_location("perplexity_config", config_path)
        if spec is None or spec.loader is None:
            return None
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception:
        return None


def get_api_key() -> Optional[str]:
    """
    Obtains the Perplexity API key from various possible sources.

    Returns:
        str: API key or None if not found.
    """
    # Check configuration file
    config_paths = [
        Path(__file__).parent.parent / "config" / "perplexity_config.py",
        Path(__file__).parent.parent / "core" / "config" / "perplexity_config.py",
        Path(__file__).parent.parent / "modules" / "config" / "perplexity_config.py",
    ]

    for config_path in config_paths:
        if config_path.exists():
            config_module = import_config(config_path)
            if config_module and hasattr(config_module, "get_api_key"):
                api_key = config_module.get_api_key()
                if api_key:
                    logger.info(f"API key obtained from file {config_path}")
                    return api_key

    # Check environment variable
    env_key = os.environ.get("PERPLEXITY_API_KEY")
    if env_key:
        logger.info("API key obtained from environment variable")
        return env_key

    return None


@pytest.fixture(scope="session")
def api_key() -> str:
    """Fixture that provides the API key for the entire test session."""
    key = get_api_key()
    if not key:
        pytest.skip(
            "API key not found. Set PERPLEXITY_API_KEY in the environment or in the configuration file."
        )
    return key


@pytest.fixture(scope="session")
def client(api_key: str) -> Any:
    """Fixture that provides a configured OpenAI client for the entire test session."""
    try:
        from openai import OpenAI
    except ImportError:
        pytest.skip("OpenAI library not installed. Run: pip install openai")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.perplexity.ai",
        default_headers={"Authorization": f"Bearer {api_key}"},
    )


@pytest.mark.parametrize("model", ALL_MODELS)
def test_model_availability(model: str, api_key: str, client: Any) -> None:
    """
    Tests a specific model from the Perplexity API.

    Args:
        model: Name of the model to be tested
        api_key: Perplexity API key
        client: Configured OpenAI client
    """
    logger.info(f"Testing model: {model}")

    start_time = datetime.datetime.now()

    try:
        # Make a test call
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that responds concisely.",
                },
                {
                    "role": "user",
                    "content": "What is the capital of Brazil? Please answer in one sentence.",
                },
            ],
            max_tokens=50,
        )

        # Calculate response time
        end_time = datetime.datetime.now()
        response_time = (end_time - start_time).total_seconds()

        # Check response
        content = response.choices[0].message.content
        logger.info(f"Response from model {model}: {content}")

        # Assertions
        assert content.strip(), f"Model {model} returned an empty response"
        assert (
            "Brazil" in content or "Brasília" in content
        ), f"Response from model {model} does not seem to answer the question about the capital of Brazil"
        assert response_time < 30, f"Model {model} took too long to respond ({response_time:.2f}s)"

        # Save test result
        save_test_result(model, True, content, response_time)

    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        logger.error(f"Error testing model {model}: {error_msg}")

        # Save error result
        save_test_result(model, False, error=error_msg)

        if "401" in error_msg or "unauthorized" in error_msg.lower():
            pytest.skip(f"Authentication error for model {model}")
        elif "404" in error_msg or "not found" in error_msg.lower():
            pytest.skip(f"Model {model} not found")
        elif "429" in error_msg or "limit" in error_msg.lower():
            pytest.skip(f"Request limit reached for model {model}")
        else:
            pytest.fail(f"Unexpected error testing model {model}: {error_msg}")


def save_test_result(
    model: str,
    success: bool,
    response: Optional[str] = None,
    response_time: Optional[float] = None,
    error: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Saves the test result in a JSON file.

    Args:
        model: Name of the tested model
        success: Whether the test was successful
        response: Model response (if successful)
        response_time: Response time in seconds (if successful)
        error: Error message (if failed)

    Returns:
        Dict containing the test result data
    """
    result: Dict[str, Any] = {
        "timestamp": datetime.datetime.now().isoformat(),
        "model": model,
        "success": success,
        "response": response,
        "response_time": response_time,
        "error": error,
    }

    # Create report directory if it doesn't exist
    report_dir = Path(__file__).parent.parent / "docs" / "test_reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    # Save individual result
    result_file = (
        report_dir
        / f"perplexity_test_{model}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    return result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--capture=no"])
