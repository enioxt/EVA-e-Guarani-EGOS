#!/bin/bash

# EVA & GUARANI - Cursor Context Enrichment Tool
# This script adds Perplexity search results to Cursor's context

echo "✧༺❀༻∞ EVA & GUARANI - CURSOR CONTEXT ENRICHER ∞༺❀༻✧"
echo

# Check if python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python not found in PATH"
    echo "Please ensure Python is installed and added to your PATH"
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if command is provided
if [ -z "$1" ]; then
    echo "Usage:"
    echo "  ./enrich_cursor_context.sh enrich \"Your search query\" [--persona PERSONA_NAME]"
    echo "  ./enrich_cursor_context.sh list"
    echo "  ./enrich_cursor_context.sh get CONTEXT_NAME"
    echo
    echo "Examples:"
    echo "  ./enrich_cursor_context.sh enrich \"Latest developments in quantum computing\" --persona scientist"
    echo "  ./enrich_cursor_context.sh list"
    echo

    read -p "Enter command (enrich/list/get): " COMMAND

    if [ "$COMMAND" = "enrich" ]; then
        read -p "Enter your search query: " QUERY
        read -p "Enter persona (optional, press Enter to skip): " PERSONA

        if [ -z "$PERSONA" ]; then
            ARGS="enrich \"$QUERY\""
        else
            ARGS="enrich \"$QUERY\" --persona $PERSONA"
        fi
    elif [ "$COMMAND" = "list" ]; then
        ARGS="list"
    elif [ "$COMMAND" = "get" ]; then
        read -p "Enter context name to retrieve: " NAME
        ARGS="get $NAME"
    else
        echo "Invalid command: $COMMAND"
        read -p "Press Enter to continue..."
        exit 1
    fi
else
    ARGS="$@"
fi

# Navigate to project root
cd $(dirname "$0")/../..

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Execute the script
python3 -m tools.integration.cursor_context $ARGS

# Deactivate virtual environment
if [ -f "venv/bin/activate" ]; then
    deactivate
fi

echo
echo "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
echo

read -p "Press Enter to continue..."
