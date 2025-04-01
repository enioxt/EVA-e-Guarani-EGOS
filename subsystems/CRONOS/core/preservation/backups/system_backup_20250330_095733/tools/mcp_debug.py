#!/usr/bin/env python3
import os
import sys
import logging
import json
import websockets
import asyncio
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/mcp_debug.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

class MCPDebugServer:
    def __init__(self, host="localhost", port=38002):
        self.host = host
        self.port = port
        self.clients = set()

    async def monitor_connection(self, websocket):
        try:
            self.clients.add(websocket)
            client_info = {
                "remote_address": str(websocket.remote_address),
                "headers": dict(websocket.request_headers),
                "time": datetime.now().isoformat()
            }
            logger.info(f"Nova conexão estabelecida: {json.dumps(client_info, indent=2)}")
            
            try:
                while True:
                    message = await websocket.recv()
                    logger.info(f"Mensagem do cliente: {message}")
                    
                    try:
                        data = json.loads(message)
                        logger.info(f"Dados decodificados: {json.dumps(data, indent=2)}")
                        
                        # Processar a mensagem aqui
                        response = {
                            "status": "success",
                            "message": "Mensagem recebida com sucesso"
                        }
                        
                        await websocket.send(json.dumps(response))
                        logger.info(f"Resposta enviada: {json.dumps(response, indent=2)}")
                        
                    except json.JSONDecodeError:
                        logger.error("Erro ao decodificar JSON da mensagem")
                        await websocket.send(json.dumps({
                            "status": "error",
                            "error": "Invalid JSON format"
                        }))
                        
            except websockets.exceptions.ConnectionClosed:
                logger.warning("Cliente desconectou")
            except Exception as e:
                logger.error(f"Erro durante comunicação: {e}")
                
        except Exception as e:
            logger.error(f"Erro na conexão: {e}")
        finally:
            self.clients.remove(websocket)
            logger.info("Conexão finalizada")

    async def start(self):
        logger.info(f"=== Iniciando Monitor MCP na porta {self.port} ===")
        try:
            async with websockets.serve(self.monitor_connection, self.host, self.port):
                logger.info(f"Monitor MCP iniciado em ws://{self.host}:{self.port}")
                await asyncio.Future()  # run forever
        except Exception as e:
            logger.error(f"Erro ao iniciar servidor: {e}")

if __name__ == "__main__":
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    server = MCPDebugServer()
    asyncio.run(server.start()) 