#!/bin/bash

# EVA & GUARANI - Perplexity MCP Server
# Este script inicia o servidor MCP para integração do Perplexity com o Cursor

echo "✧༺❀༻∞ EVA & GUARANI - PERPLEXITY MCP SERVER ∞༺❀༻✧"
echo

# Check if python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python not found in PATH"
    echo "Please ensure Python is installed and added to your PATH"
    read -p "Press Enter to continue..."
    exit 1
fi

# Navigate to project root
cd $(dirname "$0")/../..

# Check if virtual environment exists and activate it
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Install dependencies if needed
pip install -q websockets python-dotenv

# Inform user
echo "Starting Perplexity MCP Server on localhost:38001"
echo "This window must remain open while using the MCP in Cursor"
echo "Press Ctrl+C to stop the server"
echo

# Start the MCP server
python3 -m tools.integration.mcp_server "$@"

# Deactivate virtual environment before exiting
if [ -f "venv/bin/activate" ]; then
    deactivate
fi
