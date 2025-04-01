#!/usr/bin/env python3
import asyncio
import websockets
import json
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mcp_client.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('mcp_client')

async def test_connection():
    uri = "ws://localhost:38001"
    logger.info(f"Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected successfully!")
            
            # Enviar mensagem de teste
            test_message = {
                "type": "test",
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Sending test message: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Receber resposta
            response = await websocket.recv()
            logger.info(f"Received response: {response}")
            
            # Manter conexão aberta por um tempo
            await asyncio.sleep(5)
            
    except websockets.exceptions.ConnectionClosed:
        logger.error("Connection closed unexpectedly")
    except Exception as e:
        logger.error(f"Error during connection test: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(test_connection()) 