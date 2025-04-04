#!/bin/bash

# Exit on error
set -e

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Set environment variables
export PYTHONPATH="$ROOT_DIR"

echo "Starting metadata server..."
echo "Root directory: $ROOT_DIR"

# Start the server
python "$SCRIPT_DIR/metadata_server.py"
