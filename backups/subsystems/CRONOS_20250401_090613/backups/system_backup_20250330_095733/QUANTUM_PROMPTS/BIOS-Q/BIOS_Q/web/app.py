#!/usr/bin/env python3
"""
EVA & GUARANI - Web Interface
---------------------------
This module provides a web interface for the EVA & GUARANI
BIOS-Q system.

Version: 7.5
Created: 2025-03-26
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Union
from datetime import datetime

from aiohttp import web
from aiohttp.web import Request, Response, FileResponse
from aiohttp_cors import setup as cors_setup, ResourceOptions

# Import core systems
from ..core.mycelium_network import mycelium
from ..core.quantum_search import quantum_search
from ..core.translator import translator
from ..core.monitoring import monitoring

# Configure environment
from dotenv import load_dotenv

load_dotenv()

# Configure routes
routes = web.RouteTableDef()


@routes.get("/")
async def index(request: Request) -> Union[Response, FileResponse]:
    """Render the main dashboard."""
    return web.FileResponse("web/static/index.html")


@routes.get("/api/status")
async def get_status(request: Request) -> Response:
    """Get system status."""
    try:
        # Get stats from all systems
        network_stats = mycelium.get_stats()
        search_stats = quantum_search.get_stats()
        translator_stats = translator.get_stats()
        monitoring_stats = monitoring.get_stats()

        status = {
            "timestamp": datetime.now().isoformat(),
            "mycelium": network_stats,
            "quantum_search": search_stats,
            "translator": translator_stats,
            "monitoring": monitoring_stats,
        }

        return web.json_response(status)

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


@routes.post("/api/search")
async def search(request: Request) -> Response:
    """Perform a quantum search."""
    try:
        data = await request.json()
        query = data.get("query")
        limit = data.get("limit", 10)

        if not query:
            return web.json_response({"error": "Query parameter is required"}, status=400)

        results = await quantum_search.search(query)

        return web.json_response(
            {"query": query, "total_results": len(results), "results": results[:limit]}
        )

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


@routes.post("/api/translate")
async def translate(request: Request) -> Response:
    """Translate text."""
    try:
        data = await request.json()
        text = data.get("text")
        target_lang = data.get("target_lang")
        source_lang = data.get("source_lang")

        if not text or not target_lang:
            return web.json_response(
                {"error": "Text and target_lang parameters are required"}, status=400
            )

        translation = await translator.translate(text, target_lang, source_lang)

        return web.json_response(
            {
                "text": text,
                "translation": translation,
                "target_lang": target_lang,
                "source_lang": source_lang,
            }
        )

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


@routes.get("/api/languages")
async def get_languages(request: Request) -> Response:
    """Get supported languages."""
    try:
        languages = translator.get_supported_languages()

        return web.json_response({"languages": languages})

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


@routes.get("/api/metrics")
async def get_metrics(request: Request) -> Response:
    """Get system metrics."""
    try:
        metrics = await monitoring.get_metrics()

        return web.json_response({"metrics": metrics})

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


def create_app() -> web.Application:
    """Create and configure the web application."""
    app = web.Application()

    # Add routes
    app.add_routes(routes)

    # Configure CORS
    cors = cors_setup(
        app,
        defaults={
            "*": ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*", allow_methods="*"
            )
        },
    )

    # Configure static files
    app.router.add_static("/static/", path="web/static")

    return app


def main():
    """Start the web application."""
    app = create_app()
    web.run_app(app, port=int(os.getenv("WEB_PORT", 8000)))
