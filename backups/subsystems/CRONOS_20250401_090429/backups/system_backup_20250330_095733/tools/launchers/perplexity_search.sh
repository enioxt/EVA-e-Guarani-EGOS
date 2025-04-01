#!/bin/bash

# EVA & GUARANI - Perplexity Search Tool
# This script launches the Perplexity search integration for EVA & GUARANI

echo "✧༺❀༻∞ EVA & GUARANI - PERPLEXITY SEARCH ∞༺❀༻✧"
echo

# Check if python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python not found in PATH"
    echo "Please ensure Python is installed and added to your PATH"
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if query is provided
if [ -z "$1" ]; then
    echo "Usage: ./perplexity_search.sh \"your search query\" [--persona PERSONA_NAME]"
    echo
    echo "Example: ./perplexity_search.sh \"Latest developments in quantum computing\" --persona scientist"
    echo
    read -p "Enter your search query: " QUERY
else
    QUERY="$1"
fi

# Check for persona parameter
PERSONA_ARG=""
if [ "$2" = "--persona" ] && [ ! -z "$3" ]; then
    PERSONA_ARG="--persona $3"
fi

# Navigate to project root
cd $(dirname "$0")/../..

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Execute the script
python3 -m tools.integration.test_perplexity "$QUERY" $PERSONA_ARG

# Deactivate virtual environment
if [ -f "venv/bin/activate" ]; then
    deactivate
fi

echo
echo "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
echo

read -p "Press Enter to continue..." 