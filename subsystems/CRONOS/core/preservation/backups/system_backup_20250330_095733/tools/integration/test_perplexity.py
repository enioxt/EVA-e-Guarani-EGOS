#!/usr/bin/env python3
"""
Test script for Perplexity API integration with EVA & GUARANI
"""

import os
import sys
import json
import asyncio
import argparse
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the integration
from tools.integration.perplexity_integration import PerplexityIntegration

async def test_perplexity(query: str, persona: str = None):
    """Test the Perplexity integration with a query"""
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("PERPLEXITY_API_KEY")
    
    if not api_key:
        print("Error: PERPLEXITY_API_KEY not found in environment variables.")
        return
    
    print(f"Initializing Perplexity integration...")
    integration = PerplexityIntegration(api_key)
    
    print(f"Querying Perplexity API: '{query}'")
    if persona:
        print(f"Using persona: {persona}")
    
    try:
        result = await integration.enhance_knowledge(query, persona=persona)
        
        # Print the result in a formatted way
        status = result.get('status', 'unknown')
        if status == 'success':
            print("\n=== SEARCH RESULT ===")
            print(f"Query: {result.get('query')}")
            if persona:
                print(f"Persona: {result.get('knowledge', {}).get('persona')}")
            
            print("\nContent:")
            print(result.get('knowledge', {}).get('content', 'No content'))
            
            print("\nSources:")
            sources = result.get('knowledge', {}).get('sources', [])
            if not sources:
                print("No sources provided")
            else:
                for i, source in enumerate(sources, 1):
                    if 'title' in source and 'url' in source:
                        print(f"{i}. {source['title']}: {source['url']}")
                    elif 'url' in source:
                        print(f"{i}. {source['url']}")
            
            print(f"\nReliability: {result.get('knowledge', {}).get('reliability', 0.0)}")
            
            # Check for ethical warnings
            if 'ethical_warning' in result.get('knowledge', {}):
                print(f"\nEthical Warning: {result['knowledge']['ethical_warning']}")
        else:
            print(f"\nError: {result.get('message', 'Unknown error')}")
        
        # Save the full JSON result to a file for detailed inspection
        with open('perplexity_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        print("\nFull result saved to 'perplexity_result.json'")
        
    except Exception as e:
        print(f"Error during API call: {str(e)}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Test Perplexity API integration with EVA & GUARANI")
    parser.add_argument("query", help="The search query to test")
    parser.add_argument("--persona", "-p", help="The persona to use (e.g., philosopher, scientist, gamer)")
    
    args = parser.parse_args()
    
    asyncio.run(test_perplexity(args.query, args.persona))

if __name__ == "__main__":
    main() 