#!/usr/bin/env python3
"""
Test script for MCP Server
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mcp_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('mcp_test')

async def test_connection():
    """Testa a conexão com o servidor MCP."""
    uri = "ws://localhost:38001"
    
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to MCP Server")
            
            # Enviar mensagem de teste
            test_message = {
                "type": "test",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "message": "Hello MCP Server!"
                }
            }
            
            await websocket.send(json.dumps(test_message))
            logger.info(f"Sent test message: {test_message}")
            
            # Receber resposta
            response = await websocket.recv()
            logger.info(f"Received response: {response}")
            
            # Verificar resposta
            response_data = json.loads(response)
            if response_data["status"] == "success":
                logger.info("Test completed successfully!")
            else:
                logger.error(f"Test failed: {response_data}")
                
    except websockets.exceptions.ConnectionRefused:
        logger.error("Could not connect to MCP Server. Is it running?")
    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(test_connection()) 