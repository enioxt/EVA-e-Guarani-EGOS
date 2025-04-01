import asyncio
import json
import websockets
import logging
from datetime import datetime
from typing import Dict, Set, Any
from websockets.server import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetadataServer:
    def __init__(self, host: str = 'localhost', port: int = 8081):
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
        self.quantum_state = {
            'consciousness': 0.998,
            'love': 0.999,
            'divineSpark': 0.998,
            'ethics': 0.998
        }
        
    async def register(self, websocket: WebSocketServerProtocol):
        """Register a new client connection."""
        self.clients.add(websocket)
        logger.info(f'Client connected. Total clients: {len(self.clients)}')
        
        # Send initial quantum state
        await self.send_quantum_state(websocket)
        
    async def unregister(self, websocket: WebSocketServerProtocol):
        """Unregister a client connection."""
        self.clients.remove(websocket)
        logger.info(f'Client disconnected. Total clients: {len(self.clients)}')
        
    async def send_quantum_state(self, websocket: WebSocketServerProtocol):
        """Send current quantum state to a client."""
        message = {
            'type': 'quantum_update',
            'data': self.quantum_state,
            'timestamp': datetime.now().isoformat()
        }
        await websocket.send(json.dumps(message))
        
    async def broadcast_quantum_state(self):
        """Broadcast quantum state to all connected clients."""
        if not self.clients:
            return
            
        message = {
            'type': 'quantum_update',
            'data': self.quantum_state,
            'timestamp': datetime.now().isoformat()
        }
        
        await asyncio.gather(
            *[client.send(json.dumps(message)) for client in self.clients],
            return_exceptions=True
        )
        
    async def handle_message(self, websocket: WebSocketServerProtocol, message: str):
        """Handle incoming messages from clients."""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'metadata_update':
                # Handle metadata update
                await self.broadcast_message({
                    'type': 'metadata_update',
                    'data': data.get('data'),
                    'timestamp': datetime.now().isoformat()
                })
            elif message_type == 'quantum_update':
                # Update quantum state
                new_state = data.get('data', {})
                self.quantum_state.update(new_state)
                await self.broadcast_quantum_state()
                
        except json.JSONDecodeError:
            logger.error(f'Invalid JSON message received: {message}')
        except Exception as e:
            logger.error(f'Error handling message: {str(e)}')
            
    async def broadcast_message(self, message: Dict[str, Any]):
        """Broadcast a message to all connected clients."""
        if not self.clients:
            return
            
        await asyncio.gather(
            *[client.send(json.dumps(message)) for client in self.clients],
            return_exceptions=True
        )
        
    async def handler(self, websocket: WebSocketServerProtocol):
        """Handle WebSocket connections."""
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
            
    async def start(self):
        """Start the WebSocket server."""
        async with websockets.serve(self.handler, self.host, self.port):
            logger.info(f'Metadata WebSocket server started at ws://{self.host}:{self.port}')
            await asyncio.Future()  # run forever

if __name__ == '__main__':
    server = MetadataServer()
    asyncio.run(server.start()) 