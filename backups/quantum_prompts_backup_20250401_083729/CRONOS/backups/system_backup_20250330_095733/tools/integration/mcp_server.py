#!/usr/bin/env python3
"""
MCP Server for EVA & GUARANI Perplexity integration
Provides a Model Context Protocol server that allows Cursor to use Perplexity search
Based on MCP Server Example v2
"""

import os
import json
import socket
import asyncio
import logging
import signal
import sys
import traceback
import time
import platform
from typing import Dict, Any, List, Optional, Union, Callable, Set, Awaitable, Coroutine
from datetime import datetime
from dotenv import load_dotenv
from tools.integration.perplexity_integration import PerplexityAPI
import aiohttp
from aiohttp import web
import websockets
from websockets.server import WebSocketServerProtocol
from websockets.server import serve
from websockets.exceptions import ConnectionClosed

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Criar diretório de logs se não existir
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/mcp_server.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('mcp_server')

# MCP Protocol Constants
MCP_PORT = 38002
MCP_VERSION = "1.0"
MCP_SERVER_NAME = "eva-guarani"
MCP_PROTOCOL = "mcp"

# Configuration
HOST = "localhost"

# Verificar se a chave API está configurada
if not os.getenv("PERPLEXITY_API_KEY"):
    logger.error("PERPLEXITY_API_KEY não encontrada no arquivo .env")
    sys.exit(1)

# Importar e inicializar a API do Perplexity
perplexity_api = PerplexityAPI()

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = {
        'websockets': 'websockets',
        'python-dotenv': 'dotenv',
        'aiohttp': 'aiohttp',
        'psutil': 'psutil'
    }

    missing_packages = []
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        logger.error("Dependências faltando. Por favor, instale:")
        for package in missing_packages:
            logger.error(f"pip install {package}")
        return False
    return True

# Import dependencies after checking
if not check_dependencies():
    sys.exit(1)

class MCPTool:
    """Definição de uma ferramenta para o protocolo MCP."""
    def __init__(self, name: str, description: str, parameters: Dict[str, Any],
                 handler: Callable[[Dict[str, Any]], Union[Dict[str, Any], Awaitable[Dict[str, Any]]]]):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.handler = handler

class MCPServer:
    """Implementação do servidor MCP para EVA & GUARANI."""

    def __init__(self, host: str = "localhost", port: int = 38002, status_port: int = 38003):
        self.host = host
        self.port = port
        self.status_port = status_port
        self.start_time = None
        self.clients: List[WebSocketServerProtocol] = []
        self.perplexity_api = None
        self.server = None
        self.status_server = None
        self.running = False
        self.tools = self._register_tools()

    def _register_tools(self) -> Dict[str, MCPTool]:
        """Registra as ferramentas disponíveis no servidor."""
        tools = {}

        # Ferramenta de pesquisa com Perplexity
        if perplexity_api.is_configured():
            tools["perplexity_search"] = MCPTool(
                name="perplexity_search",
                description="Performs a web search using Perplexity API with real-time information",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to look up on the web"
                        },
                        "model": {
                            "type": "string",
                            "description": "The model to use for the search",
                            "enum": ["sonar-small-online", "sonar-medium-online", "mistral-7b-instruct", "llama-2-70b-chat"],
                            "default": "sonar-small-online"
                        }
                    },
                    "required": ["query"]
                },
                handler=self._handle_perplexity_search
            )
            logger.info("Ferramenta de pesquisa Perplexity registrada")

        # Adicione outras ferramentas aqui...

        return tools

    async def _handle_perplexity_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Manipulador para a ferramenta de pesquisa Perplexity."""
        query = params.get("query", "")
        model = params.get("model", "sonar-small-online")

        if not query:
            return {
                "error": "O parâmetro 'query' é obrigatório"
            }

        # Executa a busca
        result = perplexity_api.get_search_result(query, model)

        return {
            "result": result
        }

    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Manipula conexões de clientes WebSocket"""
        try:
            self.clients.append(websocket)
            logger.info(f"Novo cliente conectado. Total: {len(self.clients)}")

    async for message in websocket:
        try:
            data = json.loads(message)
                    response = await self.handle_message(data)
                    await websocket.send(json.dumps(response))
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "error": "Invalid JSON format",
                        "status": "error"
                    }))
                except Exception as e:
                    logger.error(f"Erro ao processar mensagem: {str(e)}")
                    await websocket.send(json.dumps({
                        "error": str(e),
                        "status": "error"
                    }))
        except ConnectionClosed:
            logger.info("Cliente desconectado")
        finally:
            if websocket in self.clients:
                self.clients.remove(websocket)
                logger.info(f"Cliente removido. Total: {len(self.clients)}")

    async def handle_message(self, data: Dict) -> Dict:
        """Processa mensagens recebidas dos clientes"""
        try:
            if data.get("type") == "perplexity_search":
                if not self.perplexity_api:
                    self.perplexity_api = PerplexityAPI()

                query = data.get("query", "")
                persona = data.get("persona", "default")

                if not query:
                    return {
                        "status": "error",
                        "message": "Query parameter is required"
                    }

                result = await self.perplexity_api.search(query, persona)
                return {
                    "status": "success",
                    "type": "perplexity_search",
                    "data": result
                    }
            else:
                return {
                    "status": "error",
                    "message": f"Unknown message type: {data.get('type')}"
                }
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def status_handler(self, request):
        """Manipula requisições de status HTTP"""
        if request.path == '/status':
            uptime = int(time.time() - self.start_time) if self.start_time else 0
            return aiohttp.web.Response(
                text=json.dumps({
                    "status": "running",
                    "uptime": uptime,
                    "clients": len(self.clients),
                    "version": "1.0",
                    "server_name": "eva-guarani"
                }),
                content_type='application/json'
            )
        return aiohttp.web.Response(status=404)

    async def start(self):
        """Inicia o servidor MCP"""
        try:
            # Carrega variáveis de ambiente
            load_dotenv()

            # Verifica se a API key está configurada
            if not os.getenv("PERPLEXITY_API_KEY"):
                logger.error("PERPLEXITY_API_KEY não encontrada nas variáveis de ambiente")
                return

            # Inicializa a API do Perplexity
            self.perplexity_api = PerplexityAPI()
            logger.info("API do Perplexity inicializada com sucesso")

            # Inicializa o servidor WebSocket
            self.server = await serve(
                self.handle_client,
                self.host,
                self.port,
                ping_interval=20,
                ping_timeout=10,
                close_timeout=10,
                max_size=10485760
            )

            # Inicializa o servidor de status HTTP
            app = aiohttp.web.Application()
            app.router.add_get('/status', self.status_handler)
            runner = aiohttp.web.AppRunner(app)
            await runner.setup()
            self.status_server = aiohttp.web.TCPSite(runner, self.host, self.status_port)
            await self.status_server.start()

            self.start_time = time.time()
            self.running = True

            logger.info("MCP Server inicializado")
            logger.info(f"Versão do MCP: 1.0")
            logger.info(f"Nome do servidor: eva-guarani")

            if sys.platform == 'win32':
                logger.info("Executando no Windows, manipulação de sinais limitada")

            logger.info(f"Servidor MCP iniciado em ws://{self.host}:{self.port}")
            logger.info(f"Endpoint de status disponível em http://{self.host}:{self.status_port}/status")

            # Loop principal
            while self.running:
                uptime = int(time.time() - self.start_time)
                logger.info(f"Servidor ativo há {uptime} segundos. Clientes conectados: {len(self.clients)}")
                await asyncio.sleep(60)

        except Exception as e:
            logger.error(f"Erro ao iniciar servidor: {str(e)}")
            await self.stop()

    async def stop(self):
        """Para o servidor MCP"""
        self.running = False
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        if self.status_server:
            await self.status_server.stop()
        logger.info("Servidor MCP encerrado")

async def shutdown_server(server, signal=None):
    """Graceful shutdown handler"""
    if signal:
        logger.info(f"Recebido sinal {signal.name}, desligando servidor...")
    else:
        logger.info("Desligando servidor...")

    await server.stop()

    # Give tasks time to complete
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    asyncio.get_event_loop().stop()

async def main():
    try:
        # Configuração do servidor
        server = MCPServer(
            host="localhost",
            port=38002,
            status_port=38003
        )

        # Check if we're running on Windows
        if platform.system() != 'Windows':
            # Unix-style signal handling (not supported on Windows)
            for sig in (signal.SIGINT, signal.SIGTERM):
                asyncio.get_event_loop().add_signal_handler(
                    sig,
                    lambda s=sig: asyncio.create_task(shutdown_server(server, s))
                )
        else:
            # Windows alternative
            logger.info("Executando no Windows, manipulação de sinais limitada")

        # Start the server
        await server.start()

        # Keep the server running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("Recebido sinal de interrupção (Ctrl+C)")
        await shutdown_server(server)
    except Exception as e:
        logger.error(f"Erro fatal no servidor: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Servidor encerrado pelo usuário")
    except Exception as e:
        logger.error(f"Erro ao iniciar servidor: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)
