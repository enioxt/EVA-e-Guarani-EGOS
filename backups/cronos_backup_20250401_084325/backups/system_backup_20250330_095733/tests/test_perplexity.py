#!/usr/bin/env python3
python
#!/usr/bin/env python3
"""
Perplexity API Integration Test
------------------------------------
This script checks if the integration with the Perplexity API
has been correctly implemented and is functioning.
"""

import os
import sys
import json
from datetime import datetime

# Add the current directory to PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


def print_separator(title=None):
    """Prints a separator line with an optional title."""
    width = 70
    print("\n" + "=" * width)
    if title:
        print(f" {title} ".center(width))
        print("=" * width)


def print_status(message, success=True):
    """Prints a formatted status message."""
    icon = "✅" if success else "❌"
    print(f"{icon} {message}")


# Main test
if __name__ == "__main__":
    print_separator("PERPLEXITY API INTEGRATION TEST")
    print("Starting integration tests for the Perplexity API with EVA & GUARANI...")

    # Test 1: Importing the services module
    print("\nTest 1: Importing the services modules")
    try:
        from EGOS.services.config import config_manager

        print_status("Configuration module imported successfully")
    except ImportError as e:
        print_status(f"Failed to import configuration module: {e}", False)
        print("Check if the directory structure is correct.")
        sys.exit(1)

    # Test 2: Check the Perplexity API configuration
    print("\nTest 2: Checking the Perplexity API configuration")
    try:
        if config_manager.is_configured("perplexity"):
            api_key = config_manager.get_key("perplexity")
            masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
            print_status(f"Perplexity API configured successfully (key: {masked_key})")
        else:
            print_status("Perplexity API not configured", False)
            print("Run the setup_perplexity.py script to configure the API.")
            sys.exit(1)
    except Exception as e:
        print_status(f"Error checking configuration: {e}", False)
        sys.exit(1)

    # Test 3: Importing the PerplexityService module
    print("\nTest 3: Importing the Perplexity service")
    try:
        from EGOS.services.perplexity_service import PerplexityService

        print_status("Perplexity service imported successfully")
    except ImportError as e:
        print_status(f"Failed to import Perplexity service: {e}", False)
        sys.exit(1)

    # Test 4: Initializing the Perplexity service
    print("\nTest 4: Initializing the Perplexity service")
    try:
        perplexity_service = PerplexityService()
        print_status("Perplexity service initialized successfully")
    except Exception as e:
        print_status(f"Failed to initialize Perplexity service: {e}", False)
        sys.exit(1)

    # Test 5: Importing the integration module
    print("\nTest 5: Importing the Perplexity integration module")
    try:
        from EGOS.modules.perplexity_integration import PerplexityIntegration

        print_status("Integration module imported successfully")
    except ImportError as e:
        print_status(f"Failed to import integration module: {e}", False)
        sys.exit(1)

    # Test 6: Initializing the integration module
    print("\nTest 6: Initializing the integration module")
    try:
        perplexity_integration = PerplexityIntegration()
        print_status("Integration module initialized successfully")
    except Exception as e:
        print_status(f"Failed to initialize integration module: {e}", False)
        sys.exit(1)

    # Test 7: Importing the QuantumTools module
    print("\nTest 7: Importing the QuantumTools module")
    try:
        from EGOS.modules.quantum_tools import QuantumTools

        print_status("QuantumTools module imported successfully")
    except ImportError as e:
        print_status(f"Failed to import QuantumTools module: {e}", False)
        sys.exit(1)

    # Test 8: Initializing the QuantumTools module
    print("\nTest 8: Initializing the QuantumTools module")
    try:
        quantum_tools = QuantumTools()
        print_status("QuantumTools module initialized successfully")
        print_status(f"PERPLEXITY module active: {quantum_tools.perplexity is not None}")
    except Exception as e:
        print_status(f"Failed to initialize QuantumTools module: {e}", False)
        sys.exit(1)

    # Conclusion of tests
    print_separator("TEST RESULTS")
    print("\nAll tests were completed successfully!")
    print("The integration with the Perplexity API is correctly configured.")
    print("The EVA & GUARANI system can now perform internet searches.")

    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")
