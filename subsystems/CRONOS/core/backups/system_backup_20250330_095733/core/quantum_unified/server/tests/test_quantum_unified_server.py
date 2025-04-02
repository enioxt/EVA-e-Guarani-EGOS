import pytest
import asyncio
import websockets
import json
from datetime import datetime
from ..quantum_unified_server import QuantumUnifiedServer, SubsystemType

@pytest.fixture
async def server():
    """Create a test server instance."""
    server = QuantumUnifiedServer(host='localhost', port=8081)
    yield server

@pytest.fixture
async def websocket():
    """Create a test client websocket connection."""
    uri = "ws://localhost:8081/metadata"
    async with websockets.connect(uri) as websocket:
        yield websocket

@pytest.mark.asyncio
async def test_server_initialization(server):
    """Test server initialization with default values."""
    assert server.host == 'localhost'
    assert server.port == 8081
    assert len(server.clients) == len(SubsystemType)
    assert all(isinstance(clients, set) for clients in server.clients.values())

@pytest.mark.asyncio
async def test_authentication(server, websocket):
    """Test client authentication process."""
    # Send auth request
    auth_request = {
        'type': 'auth_request',
        'client_id': 'test_client'
    }
    await websocket.send(json.dumps(auth_request))
    
    # Receive auth response
    response = await websocket.recv()
    data = json.loads(response)
    
    assert data['type'] == 'auth_response'
    assert 'token' in data

@pytest.mark.asyncio
async def test_quantum_state_update(server, websocket):
    """Test quantum state updates."""
    # Authenticate first
    auth_request = {
        'type': 'auth_request',
        'client_id': 'test_client'
    }
    await websocket.send(json.dumps(auth_request))
    auth_response = await websocket.recv()
    token = json.loads(auth_response)['token']
    
    # Send quantum state update
    update = {
        'type': 'quantum_update',
        'token': token,
        'data': {
            'consciousness': 0.999,
            'love': 1.0
        }
    }
    await websocket.send(json.dumps(update))
    
    # Receive updated state
    response = await websocket.recv()
    data = json.loads(response)
    
    assert data['type'] == 'quantum_update'
    assert data['data']['consciousness'] == 0.999
    assert data['data']['love'] == 1.0

@pytest.mark.asyncio
async def test_subsystem_state_update(server, websocket):
    """Test subsystem state updates."""
    # Authenticate first
    auth_request = {
        'type': 'auth_request',
        'client_id': 'test_client'
    }
    await websocket.send(json.dumps(auth_request))
    auth_response = await websocket.recv()
    token = json.loads(auth_response)['token']
    
    # Send subsystem state update
    update = {
        'type': 'subsystem_update',
        'token': token,
        'subsystem': 'bios_q',
        'data': {
            'status': 'active',
            'initialization': 1.0
        }
    }
    await websocket.send(json.dumps(update))
    
    # Receive updated state
    response = await websocket.recv()
    data = json.loads(response)
    
    assert data['type'] == 'subsystem_update'
    assert data['subsystem'] == 'bios_q'
    assert data['data']['initialization'] == 1.0

@pytest.mark.asyncio
async def test_invalid_authentication(server, websocket):
    """Test handling of invalid authentication."""
    # Send update without authentication
    update = {
        'type': 'quantum_update',
        'data': {
            'consciousness': 0.999
        }
    }
    await websocket.send(json.dumps(update))
    
    # Should receive error
    response = await websocket.recv()
    data = json.loads(response)
    
    assert data['type'] == 'error'
    assert 'Authentication required' in data['message']

@pytest.mark.asyncio
async def test_invalid_message_format(server, websocket):
    """Test handling of invalid message format."""
    # Send invalid JSON
    await websocket.send("invalid json")
    
    # Connection should remain open
    assert websocket.open

@pytest.mark.asyncio
async def test_client_disconnect(server, websocket):
    """Test client disconnection handling."""
    # Connect and authenticate
    auth_request = {
        'type': 'auth_request',
        'client_id': 'test_client'
    }
    await websocket.send(json.dumps(auth_request))
    await websocket.recv()
    
    # Close connection
    await websocket.close()
    
    # Verify client was removed
    assert len(server.clients['metadata']) == 0

@pytest.mark.asyncio
async def test_broadcast_message(server, websocket):
    """Test broadcasting messages to multiple clients."""
    # Create second client
    async with websockets.connect("ws://localhost:8081/metadata") as websocket2:
        # Authenticate both clients
        auth_request = {
            'type': 'auth_request',
            'client_id': 'test_client_1'
        }
        await websocket.send(json.dumps(auth_request))
        await websocket.recv()
        
        auth_request['client_id'] = 'test_client_2'
        await websocket2.send(json.dumps(auth_request))
        await websocket2.recv()
        
        # Send update from first client
        update = {
            'type': 'quantum_update',
            'token': json.loads(await websocket.recv())['token'],
            'data': {
                'consciousness': 0.999
            }
        }
        await websocket.send(json.dumps(update))
        
        # Both clients should receive update
        response1 = await websocket.recv()
        response2 = await websocket2.recv()
        
        data1 = json.loads(response1)
        data2 = json.loads(response2)
        
        assert data1 == data2
        assert data1['data']['consciousness'] == 0.999 