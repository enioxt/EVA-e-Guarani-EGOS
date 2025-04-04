#!/usr/bin/env python3
"""
EVA & GUARANI - Web Interface
---------------------------
This module implements a web interface for the EVA & GUARANI BIOS-Q
system using FastAPI.

Version: 7.5
Created: 2025-03-26
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..logging import get_logger
from ..config import Config
from ..utils import generate_id, format_timestamp
from ..middleware import setup_middleware, requires_roles

logger = get_logger(__name__)


# Request/response models
class SearchRequest(BaseModel):
    query: str
    limit: int = 10


class TranslationRequest(BaseModel):
    text: str
    target_lang: str
    source_lang: Optional[str] = None


class ApiResponse(BaseModel):
    success: bool
    data: Any = None
    error: Optional[str] = None


class WebInterface:
    """Web interface for the EVA & GUARANI BIOS-Q system."""

    def __init__(
        self,
        config: Config,
        mycelium_network=None,
        quantum_search=None,
        translator=None,
        monitoring=None,
    ):
        """Initialize the web interface.

        Args:
            config: The system configuration
            mycelium_network: The Mycelium Network instance
            quantum_search: The Quantum Search instance
            translator: The Translator instance
            monitoring: The Monitoring instance
        """
        self.config = config
        self.mycelium_network = mycelium_network
        self.quantum_search = quantum_search
        self.translator = translator
        self.monitoring = monitoring

        # Get configuration
        self.host = self.config.get("web.host", "0.0.0.0")
        self.port = int(self.config.get("web.port", 8080))
        self.debug = self.config.get("web.debug", False)

        # Create FastAPI app
        self.app = FastAPI(
            title="EVA & GUARANI API",
            description="API for the EVA & GUARANI quantum system",
            version="7.5",
        )

        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.get("web.cors.origins", ["*"]),
            allow_credentials=self.config.get("web.cors.credentials", True),
            allow_methods=self.config.get("web.cors.methods", ["*"]),
            allow_headers=self.config.get("web.cors.headers", ["*"]),
        )

        # Setup middleware
        setup_middleware(self.app)

        # Setup routes
        self._setup_routes()

        # WebSocket connections
        self.active_connections: List[WebSocket] = []

        # Static files
        static_dir = os.path.join(os.path.dirname(__file__), "..", "web", "static")
        if os.path.exists(static_dir):
            self.app.mount("/static", StaticFiles(directory=static_dir), name="static")

            # Templates
            templates_dir = os.path.join(os.path.dirname(__file__), "..", "web", "templates")
            if os.path.exists(templates_dir):
                self.templates = Jinja2Templates(directory=templates_dir)
            else:
                self.templates = None
        else:
            logger.warning(f"Static directory not found: {static_dir}")

    async def start_server(self):
        """Start the web server."""
        import uvicorn

        config = uvicorn.Config(
            app=self.app, host=self.host, port=self.port, log_level="info", reload=self.debug
        )

        server = uvicorn.Server(config)
        await server.serve()

    def _setup_routes(self):
        """Set up API routes."""

        # Root route
        @self.app.get("/", response_class=HTMLResponse)
        async def root(request: Request):
            if self.templates:
                return self.templates.TemplateResponse("index.html", {"request": request})
            else:
                return HTMLResponse(self._get_default_html())

        # API documentation redirects
        @self.app.get("/docs", tags=["Documentation"])
        async def docs_redirect():
            return {"message": "API documentation available at /api/docs"}

        @self.app.get("/redoc", tags=["Documentation"])
        async def redoc_redirect():
            return {"message": "API documentation available at /api/redoc"}

        # API routes
        api_router = FastAPI(
            title="EVA & GUARANI API",
            description="API for the EVA & GUARANI quantum system",
            version="7.5",
        )

        # Status endpoint
        @api_router.get("/status", tags=["System"], response_model=ApiResponse)
        async def get_status():
            try:
                status_info = await self._get_system_status()
                return ApiResponse(success=True, data=status_info)
            except Exception as e:
                logger.error(f"Error in status endpoint: {e}")
                return ApiResponse(success=False, error=str(e))

        # Search endpoint
        @api_router.post("/search", tags=["Search"], response_model=ApiResponse)
        async def search(request: SearchRequest):
            if not self.quantum_search:
                raise HTTPException(status_code=503, detail="Search service not available")

            try:
                results = await self.quantum_search.search(request.query, limit=request.limit)
                return ApiResponse(success=True, data=results)
            except Exception as e:
                logger.error(f"Error in search endpoint: {e}")
                return ApiResponse(success=False, error=str(e))

        # Translation endpoint
        @api_router.post("/translate", tags=["Translation"], response_model=ApiResponse)
        async def translate(request: TranslationRequest):
            if not self.translator:
                raise HTTPException(status_code=503, detail="Translation service not available")

            try:
                translation = await self.translator.translate(
                    request.text, target_lang=request.target_lang, source_lang=request.source_lang
                )

                return ApiResponse(success=True, data={"translation": translation})
            except Exception as e:
                logger.error(f"Error in translate endpoint: {e}")
                return ApiResponse(success=False, error=str(e))

        # Languages endpoint
        @api_router.get("/languages", tags=["Translation"], response_model=ApiResponse)
        async def get_languages():
            if not self.translator:
                raise HTTPException(status_code=503, detail="Translation service not available")

            try:
                languages = await self.translator.get_supported_languages()
                return ApiResponse(success=True, data=languages)
            except Exception as e:
                logger.error(f"Error in languages endpoint: {e}")
                return ApiResponse(success=False, error=str(e))

        # Metrics endpoint
        @api_router.get("/metrics", tags=["Monitoring"], response_model=ApiResponse)
        @requires_roles(["admin"])
        async def get_metrics():
            if not self.monitoring:
                raise HTTPException(status_code=503, detail="Monitoring service not available")

            try:
                metrics = await self.monitoring.get_metrics()
                return ApiResponse(success=True, data=metrics)
            except Exception as e:
                logger.error(f"Error in metrics endpoint: {e}")
                return ApiResponse(success=False, error=str(e))

        # Mount API router
        self.app.mount("/api", api_router)

        # WebSocket endpoint
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)

            try:
                while True:
                    data = await websocket.receive_text()
                    await self._handle_websocket_message(websocket, data)
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)

    async def _handle_websocket_message(self, websocket: WebSocket, data: str):
        """Handle WebSocket messages."""
        try:
            message = json.loads(data)
            message_type = message.get("type")

            if message_type == "search":
                query = message.get("query", "")
                results = await self.quantum_search.search(query) if self.quantum_search else []
                await websocket.send_json(
                    {"type": "search_results", "query": query, "results": results}
                )

            elif message_type == "translate":
                text = message.get("text", "")
                target_lang = message.get("target_lang", "en")
                translation = (
                    await self.translator.translate(text, target_lang) if self.translator else None
                )
                await websocket.send_json(
                    {
                        "type": "translation_result",
                        "original": text,
                        "translation": translation,
                        "target_lang": target_lang,
                    }
                )

            elif message_type == "status_update":
                status = await self._get_system_status()
                await websocket.send_json({"type": "status_update", "status": status})

            else:
                await websocket.send_json(
                    {"type": "error", "message": f"Unknown message type: {message_type}"}
                )

        except json.JSONDecodeError:
            await websocket.send_json({"type": "error", "message": "Invalid JSON message"})
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")
            await websocket.send_json({"type": "error", "message": str(e)})

    async def broadcast_update(self, update_type: str, data: Any):
        """Broadcast an update to all connected WebSocket clients."""
        message = {"type": update_type, "timestamp": format_timestamp(), "data": data}

        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        # Remove disconnected clients
        for connection in disconnected:
            if connection in self.active_connections:
                self.active_connections.remove(connection)

    async def _get_system_status(self) -> Dict[str, Any]:
        """Get system status information."""
        status_info = {
            "overall_status": "Operational",
            "subsystems": {
                "Mycelium Network": {"online": True, "status": "Operational"},
                "Quantum Search": {"online": True, "status": "Operational"},
                "Translation": {"online": True, "status": "Operational"},
                "Monitoring": {"online": True, "status": "Operational"},
            },
            "stats": {"Active Connections": len(self.active_connections), "Uptime": "Unknown"},
            "last_updated": format_timestamp(),
        }

        # Check mycelium network status
        if self.mycelium_network:
            try:
                network_stats = self.mycelium_network.get_stats()
                status_info["stats"]["Connected Nodes"] = network_stats.get("connected_nodes", 0)
                status_info["stats"]["Last Network Update"] = network_stats.get(
                    "last_update", "Unknown"
                )
            except Exception as e:
                logger.error(f"Error getting mycelium stats: {e}")
                status_info["subsystems"]["Mycelium Network"]["online"] = False
                status_info["subsystems"]["Mycelium Network"]["status"] = "Error"
        else:
            status_info["subsystems"]["Mycelium Network"]["online"] = False
            status_info["subsystems"]["Mycelium Network"]["status"] = "Not Available"

        # Check quantum search status
        if not self.quantum_search:
            status_info["subsystems"]["Quantum Search"]["online"] = False
            status_info["subsystems"]["Quantum Search"]["status"] = "Not Available"

        # Check translation status
        if not self.translator:
            status_info["subsystems"]["Translation"]["online"] = False
            status_info["subsystems"]["Translation"]["status"] = "Not Available"

        # Check monitoring status
        if self.monitoring:
            try:
                monitor_stats = self.monitoring.get_metrics()
                status_info["stats"]["System Load"] = f"{monitor_stats.get('system_load', 0):.2f}"
                status_info["stats"][
                    "Memory Usage"
                ] = f"{monitor_stats.get('memory_usage', 0):.1f}%"
                status_info["stats"]["Uptime"] = monitor_stats.get("uptime", "Unknown")
            except Exception as e:
                logger.error(f"Error getting monitoring stats: {e}")
                status_info["subsystems"]["Monitoring"]["online"] = False
                status_info["subsystems"]["Monitoring"]["status"] = "Error"
        else:
            status_info["subsystems"]["Monitoring"]["online"] = False
            status_info["subsystems"]["Monitoring"]["status"] = "Not Available"

        # Update overall status based on subsystem statuses
        operational_count = sum(
            1 for subsystem in status_info["subsystems"].values() if subsystem["online"]
        )
        total_subsystems = len(status_info["subsystems"])

        if operational_count == 0:
            status_info["overall_status"] = "Offline"
        elif operational_count < total_subsystems:
            status_info["overall_status"] = "Partially Operational"

        return status_info

    def _get_default_html(self) -> str:
        """Get default HTML for the root endpoint."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>EVA & GUARANI - BIOS-Q</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                    color: #333;
                }
                h1, h2, h3 {
                    color: #2c3e50;
                }
                .logo {
                    text-align: center;
                    margin-bottom: 2em;
                    color: #8e44ad;
                    font-size: 1.2em;
                }
                .signature {
                    text-align: center;
                    margin-top: 2em;
                    color: #8e44ad;
                }
                a {
                    color: #3498db;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                code {
                    background-color: #f9f9f9;
                    padding: 2px 5px;
                    border-radius: 3px;
                    font-family: monospace;
                }
                .card {
                    border: 1px solid #e0e0e0;
                    border-radius: 5px;
                    padding: 15px;
                    margin-bottom: 20px;
                    background-color: #f9f9f9;
                }
            </style>
        </head>
        <body>
            <div class="logo">
                <h1>EVA & GUARANI - BIOS-Q</h1>
                <p>Quantum-inspired system with mycelial network architecture</p>
            </div>

            <div class="card">
                <h2>API Documentation</h2>
                <p>Explore our API:</p>
                <ul>
                    <li><a href="/api/docs">Swagger UI</a> - Interactive API documentation</li>
                    <li><a href="/api/redoc">ReDoc</a> - Alternative API documentation</li>
                </ul>
            </div>

            <div class="card">
                <h2>Core Systems</h2>
                <ul>
                    <li><strong>Mycelium Network</strong> - Neural-like connection architecture</li>
                    <li><strong>Quantum Search</strong> - Intelligent information retrieval</li>
                    <li><strong>Translation System</strong> - Multilingual capabilities</li>
                    <li><strong>Monitoring System</strong> - Real-time system observability</li>
                </ul>
            </div>

            <div class="signature">
                ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
            </div>
        </body>
        </html>
        """


# For direct execution
async def main():
    """Run the web interface as a standalone module."""
    from ..config import Config

    # Load configuration
    config = Config()
    config.load_config()

    # Create web interface
    web = WebInterface(config)

    try:
        # Start the web server
        await web.start_server()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Error in web interface: {e}")


if __name__ == "__main__":
    asyncio.run(main())
