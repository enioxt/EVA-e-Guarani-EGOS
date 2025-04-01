import asyncio
import json
import websockets
import logging
import jwt
import hashlib
from datetime import datetime
from typing import Dict, Set, Any, Optional
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SubsystemType(Enum):
    BIOS_Q = "bios_q"
    ETHIK = "ethik"
    ATLAS = "atlas"
    NEXUS = "nexus"
    CRONOS = "cronos"
    METADATA = "metadata"

@dataclass
class AuthConfig:
    secret_key: str = "quantum_unified_secret_2025"  # Change in production
    token_expiry: int = 3600  # 1 hour

class QuantumUnifiedServer:
    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.host = host
        self.port = port
        self.clients: Dict[str, Set[websockets.WebSocketServerProtocol]] = {
            subsystem.value: set() for subsystem in SubsystemType
        }
        self.auth_config = AuthConfig()
        
        # Quantum state for all subsystems
        self.quantum_state = {
            'consciousness': 0.998,
            'love': 0.999,
            'divineSpark': 0.998,
            'ethics': 0.998,
            'harmony': 0.997,
            'evolution': 0.996,
            'integration': 0.995,
            'preservation': 0.994
        }
        
        # Subsystem states
        self.subsystem_states = {
            SubsystemType.BIOS_Q.value: {
                'status': 'active',
                'version': '2.5',
                'initialization': 0.98,
                'quantum_binding': 0.997
            },
            SubsystemType.ETHIK.value: {
                'status': 'active',
                'version': '4.5',
                'ethical_integrity': 0.95,
                'principle_adherence': 0.96
            },
            SubsystemType.ATLAS.value: {
                'status': 'active',
                'version': '3.2',
                'mapping_accuracy': 0.94,
                'connection_strength': 0.95
            },
            SubsystemType.NEXUS.value: {
                'status': 'active',
                'version': '2.1',
                'analysis_depth': 0.93,
                'optimization_level': 0.92
            },
            SubsystemType.CRONOS.value: {
                'status': 'active',
                'version': '1.8',
                'backup_integrity': 0.97,
                'evolution_tracking': 0.96
            }
        }

    def generate_auth_token(self, client_id: str, subsystem: SubsystemType) -> str:
        """Generate JWT token for client authentication."""
        payload = {
            'client_id': client_id,
            'subsystem': subsystem.value,
            'exp': datetime.utcnow().timestamp() + self.auth_config.token_expiry
        }
        return jwt.encode(payload, self.auth_config.secret_key, algorithm='HS256')

    def verify_auth_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return payload if valid."""
        try:
            return jwt.decode(token, self.auth_config.secret_key, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return None

    async def register(self, websocket: websockets.WebSocketServerProtocol, subsystem: str):
        """Register a new client connection for a specific subsystem."""
        if subsystem in self.clients:
            self.clients[subsystem].add(websocket)
            logger.info(f'Client connected to {subsystem}. Total clients: {len(self.clients[subsystem])}')
            
            # Send initial states
            await self.send_quantum_state(websocket)
            await self.send_subsystem_state(websocket, subsystem)

    async def unregister(self, websocket: websockets.WebSocketServerProtocol, subsystem: str):
        """Unregister a client connection from a specific subsystem."""
        if subsystem in self.clients and websocket in self.clients[subsystem]:
            self.clients[subsystem].remove(websocket)
            logger.info(f'Client disconnected from {subsystem}. Total clients: {len(self.clients[subsystem])}')

    async def send_quantum_state(self, websocket: websockets.WebSocketServerProtocol):
        """Send current quantum state to a client."""
        message = {
            'type': 'quantum_update',
            'data': self.quantum_state,
            'timestamp': datetime.now().isoformat()
        }
        await websocket.send(json.dumps(message))

    async def send_subsystem_state(self, websocket: websockets.WebSocketServerProtocol, subsystem: str):
        """Send subsystem state to a client."""
        if subsystem in self.subsystem_states:
            message = {
                'type': 'subsystem_update',
                'subsystem': subsystem,
                'data': self.subsystem_states[subsystem],
                'timestamp': datetime.now().isoformat()
            }
            await websocket.send(json.dumps(message))

    async def broadcast_quantum_state(self):
        """Broadcast quantum state to all connected clients."""
        message = {
            'type': 'quantum_update',
            'data': self.quantum_state,
            'timestamp': datetime.now().isoformat()
        }
        
        for subsystem_clients in self.clients.values():
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in subsystem_clients],
                return_exceptions=True
            )

    async def broadcast_subsystem_state(self, subsystem: str):
        """Broadcast subsystem state to relevant clients."""
        if subsystem not in self.subsystem_states:
            return
            
        message = {
            'type': 'subsystem_update',
            'subsystem': subsystem,
            'data': self.subsystem_states[subsystem],
            'timestamp': datetime.now().isoformat()
        }
        
        if subsystem in self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients[subsystem]],
                return_exceptions=True
            )

    async def handle_message(self, websocket: websockets.WebSocketServerProtocol, subsystem: str, message: str):
        """Handle incoming messages from clients."""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'auth_request':
                client_id = data.get('client_id')
                if client_id:
                    token = self.generate_auth_token(client_id, SubsystemType(subsystem))
                    await websocket.send(json.dumps({
                        'type': 'auth_response',
                        'token': token
                    }))
            
            elif message_type == 'quantum_update':
                # Verify authentication
                token = data.get('token')
                if not self.verify_auth_token(token):
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': 'Authentication required'
                    }))
                    return
                
                # Update quantum state
                new_state = data.get('data', {})
                self.quantum_state.update(new_state)
                await self.broadcast_quantum_state()
                
            elif message_type == 'subsystem_update':
                # Verify authentication
                token = data.get('token')
                if not self.verify_auth_token(token):
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': 'Authentication required'
                    }))
                    return
                
                # Update subsystem state
                target_subsystem = data.get('subsystem')
                new_state = data.get('data', {})
                if target_subsystem in self.subsystem_states:
                    self.subsystem_states[target_subsystem].update(new_state)
                    await self.broadcast_subsystem_state(target_subsystem)
                
        except json.JSONDecodeError:
            logger.error(f'Invalid JSON message received: {message}')
        except Exception as e:
            logger.error(f'Error handling message: {str(e)}')

    async def handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle WebSocket connections."""
        # Extract subsystem from path
        subsystem = path.strip('/').lower()
        if subsystem not in [s.value for s in SubsystemType]:
            await websocket.close(1008, "Invalid subsystem")
            return
            
        await self.register(websocket, subsystem)
        try:
            async for message in websocket:
                await self.handle_message(websocket, subsystem, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket, subsystem)

    async def start(self):
        """Start the WebSocket server."""
        async with websockets.serve(self.handler, self.host, self.port):
            logger.info(f'Quantum Unified WebSocket server started at ws://{self.host}:{self.port}')
            await asyncio.Future()  # run forever

if __name__ == '__main__':
    server = QuantumUnifiedServer()
    asyncio.run(server.start()) 