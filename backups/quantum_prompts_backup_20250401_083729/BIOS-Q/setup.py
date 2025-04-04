#!/usr/bin/env python3
﻿"""
EVA & GUARANI - Setup Configuration
---------------------------------
This module provides the setup configuration for the
EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

import os
from setuptools import setup, find_packages

def create_env_file():
    """Create .env file from example if it doesn't exist."""
    if not os.path.exists('.env') and os.path.exists('.env.example'):
        with open('.env.example', 'r') as example, open('.env', 'w') as env:
            env.write(example.read())
            print("Created .env file from .env.example")

def setup_grafana_dashboard():
    """Set up Grafana dashboard if configuration exists."""
    try:
        from bios_q.core.monitoring import monitoring
        import asyncio
        asyncio.run(monitoring.create_grafana_dashboard())
        print("Grafana dashboard created successfully")
    except Exception as e:
        print(f"Warning: Could not set up Grafana dashboard: {str(e)}")

def main():
    """Main setup function."""
    # Create .env file if needed
    create_env_file()

    # Set up Grafana dashboard
    setup_grafana_dashboard()

    print("\nNext steps:")
    print("1. Update configuration in .env file")
    print("2. Start the system with: eva-guarani start")
    print("3. Visit documentation at: http://localhost:8080")

setup(
    name="bios-q",
    version="1.0.0",
    description="BIOS-Q MCP - Quantum System Initialization Protocol",
    author="EVA & GUARANI",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "aiohttp>=3.8.0",
        "asyncio>=3.4.3",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "prometheus-client>=0.19.0",
        "typing-extensions>=4.9.0",
        "grafana-api>=1.0.3",
        "prometheus-api-client>=0.5.5"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0"
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0"
        ]
    }
)

if __name__ == "__main__":
    main()
