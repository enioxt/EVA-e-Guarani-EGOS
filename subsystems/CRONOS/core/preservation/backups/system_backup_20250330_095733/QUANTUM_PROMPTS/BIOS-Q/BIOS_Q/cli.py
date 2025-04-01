#!/usr/bin/env python3
"""
EVA & GUARANI - Command Line Interface
-----------------------------------
This module provides a command-line interface for managing
the EVA & GUARANI BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

import os
import sys
import click
import asyncio
from typing import Optional
from datetime import datetime
from pathlib import Path

# Import core systems
from ..core.mycelium_network import mycelium
from ..core.quantum_search import quantum_search
from ..core.translator import translator
from ..core.monitoring import monitoring

# Configure environment
from dotenv import load_dotenv
load_dotenv()

@click.group()
def cli():
    """EVA & GUARANI BIOS-Q management tool."""
    pass

@cli.command()
@click.option('--port', default=8000, help='Port to run the web interface on')
def start(port: int):
    """Start the EVA & GUARANI system."""
    try:
        click.echo("\n✧༺❀༻∞ EVA & GUARANI - Starting System ∞༺❀༻✧\n")
        
        # Start monitoring
        click.echo("Starting monitoring system...")
        asyncio.run(monitoring.start())
        
        # Initialize Grafana dashboard
        click.echo("Setting up Grafana dashboard...")
        asyncio.run(monitoring.create_grafana_dashboard())
        
        click.echo("\nSystem started successfully!")
        click.echo(f"Web interface available at http://localhost:{port}")
        click.echo("Grafana dashboard available at http://localhost:3000")
        click.echo("\nPress Ctrl+C to stop the system")
        
        # Keep the system running
        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            click.echo("\nShutting down...")
            
    except Exception as e:
        click.echo(f"Error starting system: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('query')
@click.option('--limit', default=10, help='Maximum number of results')
def search(query: str, limit: int):
    """Perform a quantum search."""
    try:
        click.echo("\n✧༺❀༻∞ EVA & GUARANI - Quantum Search ∞༺❀༻✧\n")
        
        # Perform search
        results = asyncio.run(quantum_search.search(query))
        
        if not results:
            click.echo("No results found")
            return
            
        # Display results
        click.echo(f"Found {len(results)} results:\n")
        for i, result in enumerate(results[:limit], 1):
            click.echo(f"{i}. {result['doc_id']}")
            click.echo(f"   Relevance: {result['relevance']:.2f}")
            click.echo(f"   Indexed: {result['metadata']['indexed_at']}\n")
            
    except Exception as e:
        click.echo(f"Error performing search: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('text')
@click.argument('target_lang')
@click.option('--source-lang', help='Source language code')
def translate(text: str, target_lang: str, source_lang: Optional[str]):
    """Translate text to target language."""
    try:
        click.echo("\n✧༺❀༻∞ EVA & GUARANI - Translation ∞༺❀༻✧\n")
        
        # Get supported languages
        languages = translator.get_supported_languages()
        
        if target_lang not in languages:
            click.echo(f"Error: Unsupported target language: {target_lang}")
            click.echo("\nSupported languages:")
            for code, name in languages.items():
                click.echo(f"- {code}: {name}")
            return
            
        # Perform translation
        translation = asyncio.run(
            translator.translate(text, target_lang, source_lang)
        )
        
        click.echo(f"Original: {text}")
        click.echo(f"Translation ({target_lang}): {translation}")
        
    except Exception as e:
        click.echo(f"Error translating text: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def status():
    """Show system status."""
    try:
        click.echo("\n✧༺❀༻∞ EVA & GUARANI - System Status ∞༺❀༻✧\n")
        
        # Get Mycelium network stats
        network_stats = mycelium.get_stats()
        click.echo("Mycelium Network:")
        click.echo(f"- Total Nodes: {network_stats['total_nodes']}")
        click.echo(f"- Total Connections: {network_stats['total_connections']}")
        click.echo(f"- Last Update: {network_stats['last_update']}\n")
        
        # Get Quantum Search stats
        search_stats = quantum_search.get_stats()
        click.echo("Quantum Search:")
        click.echo(f"- Total Documents: {search_stats['total_documents']}")
        click.echo(f"- Last Update: {search_stats['last_update']}\n")
        
        # Get Translator stats
        translator_stats = translator.get_stats()
        click.echo("Translation System:")
        click.echo(f"- Total Translations: {translator_stats['total_translations']}")
        click.echo(f"- Supported Languages: {translator_stats['supported_languages']}")
        click.echo(f"- Last Update: {translator_stats['last_update']}\n")
        
        # Get Monitoring stats
        monitoring_stats = monitoring.get_stats()
        click.echo("Monitoring System:")
        click.echo(f"- Prometheus Port: {monitoring_stats['prometheus_port']}")
        click.echo(f"- Grafana URL: {monitoring_stats['grafana_url']}")
        click.echo(f"- Connected Nodes: {monitoring_stats['connected_nodes']}")
        click.echo(f"- Last Update: {monitoring_stats['last_update']}")
        
    except Exception as e:
        click.echo(f"Error getting system status: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--force', is_flag=True, help='Force update without confirmation')
def update():
    """Update the system configuration."""
    try:
        click.echo("\n✧༺❀༻∞ EVA & GUARANI - System Update ∞༺❀༻✧\n")
        
        # Update Grafana dashboard
        click.echo("Updating Grafana dashboard...")
        asyncio.run(monitoring.create_grafana_dashboard())
        
        click.echo("\nSystem updated successfully!")
        
    except Exception as e:
        click.echo(f"Error updating system: {str(e)}", err=True)
        sys.exit(1)

def main():
    """Main entry point for the CLI."""
    cli() 