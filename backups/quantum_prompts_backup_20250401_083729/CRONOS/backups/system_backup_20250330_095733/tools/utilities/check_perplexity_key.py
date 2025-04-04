#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to verify and test the Perplexity API key.
This script checks if the API key is configured correctly and makes a simple test call.
"""

import os
import sys
import json
import logging
import traceback
import datetime

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PerplexityCheck")


def check_api_key():
    """
    Checks if the Perplexity API key is configured correctly.

    Returns:
        str or None: The API key if found, None otherwise.
    """
    logger.info("Checking Perplexity API key")

    # INSERT YOUR API KEY MANUALLY HERE
    manual_api_key = (
        "NWWFSoofq7r0u3bADTnS0HjpmhRCpO15ayix68imdbnJLSDK"  # Replace with your API key value
    )

    # Check manual key
    if manual_api_key and manual_api_key != "INSERT_YOUR_API_KEY_HERE":
        masked_key = (
            manual_api_key[:4] + "..." + manual_api_key[-4:] if len(manual_api_key) > 8 else "****"
        )
        logger.info(f"Using manually entered API key: {masked_key}")
        return manual_api_key

    # Check environment variable
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if api_key:
        masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "****"
        logger.info(f"API key found in environment variable: {masked_key}")
        return api_key
    else:
        # Check configuration file
        try:
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from perplexity_config import get_api_key

            config_api_key = get_api_key()
            if config_api_key:
                masked_key = (
                    config_api_key[:4] + "..." + config_api_key[-4:]
                    if len(config_api_key) > 8
                    else "****"
                )
                logger.info(f"API key found in configuration file: {masked_key}")
                return config_api_key
        except ImportError:
            logger.warning("Could not import the perplexity_config module")

    logger.error("No valid API key found!")
    return None


def test_api_connection(api_key):
    """
    Tests the connection to the Perplexity API using the provided key.

    Args:
        api_key (str): API key to test

    Returns:
        bool: True if the test is successful, False otherwise
    """
    if not api_key:
        logger.error("No API key provided for testing")
        return False

    try:
        # Import necessary modules
        try:
            from openai import OpenAI
        except ImportError:
            logger.error("The 'openai' library is not installed. Run 'pip install openai'")
            return False

        # Import Perplexity configuration if available
        try:
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            import perplexity_config

            has_config = True
            available_models = perplexity_config.AVAILABLE_MODELS
            logger.info(f"Available models: {', '.join(available_models)}")
        except ImportError:
            logger.warning("perplexity_config.py file not found")
            has_config = False
            available_models = [
                "sonar",
                "sonar-pro",
                "sonar-reasoning",
                "sonar-reasoning-pro",
                "sonar-deep-research",
                "r1-1776",
            ]

        # Test models sequentially until one succeeds
        for model in available_models:
            logger.info(f"Testing connection with model {model}...")
            try:
                # Initialize OpenAI client with the API key
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.perplexity.ai",
                    default_headers={"Authorization": f"Bearer {api_key}"},
                )

                # Perform a test call
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {
                            "role": "user",
                            "content": "What is the capital of Brazil? Please answer in one sentence.",
                        },
                    ],
                    max_tokens=50,
                )

                # Check response
                if (
                    response
                    and response.choices
                    and len(response.choices) > 0
                    and response.choices[0].message
                    and response.choices[0].message.content
                ):
                    content = response.choices[0].message.content
                    logger.info(f"Response from model {model}: {content[:50]}...")
                    print(f"✓ Connection with model {model} successful!")
                    print(f"Response: {content[:100]}...")
                    return True
                else:
                    logger.warning(f"Empty or no content response from model {model}")
                    continue

            except Exception as e:
                error_type = type(e).__name__
                error_msg = str(e)

                if "401" in error_msg:
                    logger.error(f"Authentication error (401): The API key is invalid or expired.")
                    print(
                        f"✗ Authentication error with model {model}: The API key is invalid or expired."
                    )
                    # For 401 we do not try other models, as it is an authentication issue
                    print(f"Error details: {error_msg}")
                    return False
                elif "404" in error_msg or "model_not_found" in error_msg.lower():
                    logger.warning(f"Model {model} not found or unavailable: {error_msg}")
                    print(f"✗ Model {model} not available for your account. Trying next model...")
                    continue
                elif "429" in error_msg:
                    logger.warning(f"Rate limit exceeded: {error_msg}")
                    print(f"✗ Rate limit exceeded with model {model}. Trying next model...")
                    continue
                else:
                    logger.error(f"Unknown error testing model {model}: {error_type}: {error_msg}")
                    print(f"✗ Error testing model {model}: {error_type}")
                    print(f"Error details: {error_msg}")
                    continue

        # If reached here, no model worked
        logger.error("All models failed. Check your connection and configuration.")
        print("✗ Could not connect to the Perplexity API using any of the available models.")
        return False

    except Exception as e:
        logger.error(f"Error testing connection: {str(e)}")
        traceback.print_exc()
        print(f"✗ Error testing connection: {str(e)}")
        return False


def main():
    """
    Main function that checks the API key and tests the connection.
    """
    print("\n============================================================")
    print("   PERPLEXITY API CHECK AND TEST")
    print(f"   {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("============================================================\n")

    # Check API key
    api_key = check_api_key()

    if not api_key:
        print("\n✗ FAILURE: No valid API key found.")
        print("\nTo configure your API key, you can:")
        print("  1. Edit this file and add your key to the 'manual_api_key' variable")
        print("  2. Set the environment variable PERPLEXITY_API_KEY")
        print("  3. Create a perplexity_config.py file with the PERPLEXITY_API_KEY variable set")
        return False

    # Mask key for display
    masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "****"
    print(f"\nUsing API key: {masked_key}")

    # Test connection
    print("\nTesting connection with the Perplexity API...")
    result = test_api_connection(api_key)

    if result:
        print("\n✓ SUCCESS: Connection with the Perplexity API established successfully!")
        print("\nYour configuration is correct and you can use the service.")
        return True
    else:
        print("\n✗ FAILURE: Could not connect to the Perplexity API.")
        print("\nCheck the following items:")
        print("  1. The API key is correct and not expired")
        print("  2. Your internet connection is working")
        print("  3. The Perplexity service is available and accessible from your location")
        print("  4. Your account has access to the requested models")
        return False


if __name__ == "__main__":
    main()
