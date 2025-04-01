#!/usr/bin/env python3
python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for integration with OpenAI's DALL-E API for image generation
This module manages communication with the DALL-E API, including authentication,
image generation, and credit management.
"""

import os
import json
import logging
import time
import requests
import base64
from io import BytesIO
from typing import Dict, List, Union, Optional, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/dalle_integration.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Check and create log directory
os.makedirs("logs", exist_ok=True)
os.makedirs("output/images", exist_ok=True)  # Directory to save generated images

class DalleIntegration:
    """
    Class for integration with OpenAI's DALL-E API
    """
    
    def __init__(self, config_path: str = "config/api_config.json"):
        """
        Initializes the DALL-E integrator.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.api_key = self.config.get("openai_api_key", "")
        self.base_url = "https://api.openai.com/v1"
        self.dalle_endpoint = "/images/generations"
        self.cost_per_image = self.config.get("cost_per_image", 1)  # Cost in credits
        
        # Check if the API Key is configured
        if not self.api_key:
            logger.warning("OpenAI API Key not configured. Image generation will not work.")
    
    def _load_config(self) -> Dict:
        """
        Loads the API configuration.
        
        Returns:
            Dict: API configuration
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default configuration if it doesn't exist
                default_config = {
                    "openai_api_key": "",
                    "cost_per_image": 1,
                    "default_model": "dall-e-3",
                    "default_size": "1024x1024",
                    "default_quality": "standard",
                    "default_style": "vivid",
                    "rate_limit": {
                        "requests_per_minute": 50,
                        "requests_per_day": 1000
                    },
                    "image_save_path": "output/images/"
                }
                
                # Ensure the configuration directory exists
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=4)
                
                return default_config
        except Exception as e:
            logger.error(f"Error loading API configuration: {e}")
            return {}
    
    def update_api_key(self, api_key: str) -> bool:
        """
        Updates the OpenAI API key.
        
        Args:
            api_key: New API key
            
        Returns:
            bool: True if the update was successful
        """
        try:
            self.api_key = api_key
            self.config["openai_api_key"] = api_key
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            
            return True
        except Exception as e:
            logger.error(f"Error updating API Key: {e}")
            return False
    
    def generate_image(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        style: Optional[str] = None,
        n: int = 1
    ) -> Tuple[bool, Union[Dict[str, List[str]], str]]:
        """
        Generates images using the DALL-E API.
        
        Args:
            prompt: Textual description of the desired image
            model: DALL-E model to use (dall-e-2, dall-e-3)
            size: Image size (256x256, 512x512, 1024x1024, 1792x1024, 1024x1792)
            quality: Image quality (standard, hd) - only for dall-e-3
            style: Image style (vivid, natural) - only for dall-e-3
            n: Number of images to generate (1-10) - only for dall-e-2
            
        Returns:
            Tuple: (success, result)
                - success (bool): True if generation was successful
                - result (Dict[str, List[str]] or str): Dictionary with URLs and local paths 
                  of the images or error message
        """
        if not self.api_key:
            return False, "OpenAI API Key not configured"
        
        # Use default configuration values if not specified
        model = model or self.config.get("default_model", "dall-e-3")
        size = size or self.config.get("default_size", "1024x1024")
        quality = quality or self.config.get("default_quality", "standard")
        style = style or self.config.get("default_style", "vivid")
        
        # Ensure n=1 for dall-e-3 (API limitation)
        if model == "dall-e-3":
            n = 1
        
        # Validate parameters
        if model not in ["dall-e-2", "dall-e-3"]:
            return False, f"Invalid model: {model}. Use 'dall-e-2' or 'dall-e-3'"
        
        valid_sizes = {
            "dall-e-2": ["256x256", "512x512", "1024x1024"],
            "dall-e-3": ["1024x1024", "1792x1024", "1024x1792"]
        }
        
        if size not in valid_sizes[model]:
            return False, f"Invalid size for {model}: {size}. Valid sizes: {', '.join(valid_sizes[model])}"
        
        # Prepare the payload
        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size
        }
        
        # Add specific parameters for dall-e-3
        if model == "dall-e-3":
            payload["quality"] = quality
            payload["style"] = style
        
        # Request headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            # Make request to the API
            response = requests.post(
                f"{self.base_url}{self.dalle_endpoint}",
                headers=headers,
                json=payload,
                timeout=60  # 60 seconds timeout
            )
            
            # Check response
            if response.status_code == 200:
                data = response.json()
                
                # Extract image URLs
                image_urls = [item["url"] for item in data["data"]]
                
                # Save images locally
                saved_paths = []
                for i, url in enumerate(image_urls):
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    filename = f"{self.config.get('image_save_path', 'output/images/')}{timestamp}-{i+1}.png"
                    
                    # Download and save the image
                    image_response = requests.get(url, timeout=30)
                    if image_response.status_code == 200:
                        with open(filename, 'wb') as f:
                            f.write(image_response.content)
                        saved_paths.append(filename)
                
                # Log successful generation
                logger.info(f"Images generated successfully. Prompt: '{prompt[:50]}...' Model: {model}")
                
                if saved_paths:
                    return True, {"urls": image_urls, "local_paths": saved_paths}
                else:
                    return True, {"urls": image_urls}
            else:
                error_data = response.json()
                error_message = error_data.get("error", {}).get("message", "Unknown API error")
                logger.error(f"Error in OpenAI API: {error_message}")
                return False, f"Error in OpenAI API: {error_message}"
        
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return False, f"Error generating image: {e}"
    
    def get_image_cost(self, model: str, size: str, quality: str = "standard") -> int:
        """
        Calculates the cost in credits to generate an image.
        
        Args:
            model: DALL-E model (dall-e-2, dall-e-3)
            size: Image size
            quality: Image quality (standard, hd)
            
        Returns:
            int: Cost in credits
        """
        # Cost table (credits)
        costs = {
            "dall-e-2": {
                "256x256": 1,
                "512x512": 1,
                "1024x1024": 2
            },
            "dall-e-3": {
                "1024x1024": {
                    "standard": 2,
                    "hd": 3
                },
                "1792x1024": {
                    "standard": 3,
                    "hd": 4
                },
                "1024x1792": {
                    "standard": 3,
                    "hd": 4
                }
            }
        }
        
        try:
            if model == "dall-e-2":
                return costs["dall-e-2"].get(size, 1)
            elif model == "dall-e-3":
                return costs["dall-e-3"].get(size, {}).get(quality, 2)
            else:
                return self.cost_per_image
        except Exception:
            return self.cost_per_image
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Tests the connection with the OpenAI API.
        
        Returns:
            Tuple[bool, str]: Connection status and message
        """
        if not self.api_key:
            return False, "API Key not configured"
        
        try:
            # Check authentication using a simple endpoint
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Successful connection to OpenAI API"
            else:
                error_data = response.json()
                error_message = error_data.get("error", {}).get("message", "Unknown error")
                return False, f"Authentication error: {error_message}"
                
        except Exception as e:
            return False, f"Error testing connection: {e}"


# Singleton function to get a single instance of the DALL-E integrator
_dalle_instance = None

def get_dalle_integration() -> DalleIntegration:
    """
    Returns a single instance of the DALL-E integrator.
    
    Returns:
        DalleIntegration: Instance of the DALL-E integrator
    """
    global _dalle_instance
    if _dalle_instance is None:
        _dalle_instance = DalleIntegration()
    return _dalle_instance


if __name__ == "__main__":
    # Basic integration test
    dalle = get_dalle_integration()
    
    # Check if the API Key is configured
    if not dalle.api_key:
        print("Please configure the API Key in the config/api_config.json file")
        exit(1)
    
    # Test connection
    connection_status, message = dalle.test_connection()
    print(f"Connection status: {message}")
    
    if connection_status:
        # Test image generation
        prompt = "A cat astronaut floating in space, digital art style"
        print(f"Generating image with prompt: '{prompt}'")
        
        success, result = dalle.generate_image(prompt)
        
        if success:
            print("Image generated successfully!")
            if isinstance(result, dict):
                print(f"Image URLs: {result.get('urls', [])}")
                print(f"Local paths: {result.get('local_paths', [])}")
            else:
                print(f"Result: {result}")
        else:
            print(f"Failed to generate image: {result}")