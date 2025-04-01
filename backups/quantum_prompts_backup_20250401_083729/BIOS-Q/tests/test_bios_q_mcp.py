#!/usr/bin/env python3
"""Tests for the BIOS-Q MCP."""
import asyncio
from asyncio import StreamReader, StreamWriter
import json
import logging
import os
import pytest
from unittest.mock import Mock, AsyncMock, patch, mock_open
from pathlib import Path
from mcp.bios_q_mcp import BiosQMCP, BiosQProtocol, main
from typing import Optional, Tuple
from asyncio import BaseTransport

pytestmark = pytest.mark.asyncio(loop_scope="function")

@pytest.fixture(autouse=True)
def setup_env():
    """Configure environment variables for tests."""
    os.environ["QUANTUM_LOG_LEVEL"] = "DEBUG"
    os.environ["QUANTUM_STATE_DIR"] = "C:\\Eva Guarani EGOS\\QUANTUM_PROMPTS"
    os.environ["BIOS_Q_CONFIG"] = "C:\\Eva Guarani EGOS\\BIOS-Q\\config\\bios_q_config.json"
    os.environ["PYTHONPATH"] = "C:\\Eva Guarani EGOS\\BIOS-Q;C:\\Eva Guarani EGOS\\QUANTUM_PROMPTS"
    yield
    # Cleanup after tests
    for key in ["QUANTUM_LOG_LEVEL", "QUANTUM_STATE_DIR", "BIOS_Q_CONFIG", "PYTHONPATH"]:
        os.environ.pop(key, None)

@pytest.fixture
def mock_reader():
    reader = AsyncMock(spec=asyncio.StreamReader)
    return reader

@pytest.fixture
def mock_writer():
    writer = Mock(spec=asyncio.StreamWriter)
    writer.drain = AsyncMock()
    return writer

@pytest.fixture
def mock_config():
    return {
        "paths": {
            "root": "C:\\Eva Guarani EGOS",
            "quantum_prompts": "C:\\Eva Guarani EGOS\\QUANTUM_PROMPTS"
        },
        "subsystems": {
            "ATLAS": {"required": True},
            "CRONOS": {"required": True}
        },
        "initialization": {
            "display_banner": True
        }
    }

@pytest.fixture
def mcp(mock_reader, mock_writer, mock_config):
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_config))):
        return BiosQMCP(mock_reader, mock_writer)

@pytest.mark.asyncio
async def test_read_message(mcp, mock_reader):
    # Arrange
    test_message = {"type": "test", "data": "hello"}
    mock_reader.readline.return_value = json.dumps(test_message).encode() + b"\n"
    
    # Act
    result = await mcp.read_message()
    
    # Assert
    assert result == test_message
    mock_reader.readline.assert_called_once()

@pytest.mark.asyncio
async def test_write_message(mcp, mock_writer):
    # Arrange
    test_message = {"type": "response", "data": "hello"}
    
    # Act
    await mcp.write_message(test_message)
    
    # Assert
    expected_data = json.dumps(test_message).encode() + b"\n"
    mock_writer.write.assert_called_once_with(expected_data)
    mock_writer.drain.assert_called_once()

@pytest.mark.asyncio
async def test_process_message_shutdown(mcp):
    # Arrange
    test_message = {"type": "shutdown"}
    
    # Act
    await mcp.process_message(test_message)
    
    # Assert
    assert mcp.running is False

@pytest.mark.asyncio
async def test_process_message_normal(mcp, mock_writer):
    # Arrange
    test_message = {"type": "test", "id": "123"}
    
    # Act
    await mcp.process_message(test_message)
    
    # Assert
    expected_response = {
        "type": "response",
        "id": "123",
        "status": "success",
        "data": {"message": "Message processed successfully"}
    }
    expected_data = json.dumps(expected_response).encode() + b"\n"
    mock_writer.write.assert_called_once_with(expected_data)
    mock_writer.drain.assert_called_once()

@pytest.mark.asyncio
async def test_load_config_missing_env_var():
    # Arrange
    os.environ.pop("BIOS_Q_CONFIG", None)
    
    # Act & Assert
    with pytest.raises(ValueError, match="BIOS_Q_CONFIG environment variable not set"):
        BiosQMCP(AsyncMock(), Mock())

@pytest.mark.asyncio
async def test_verify_structure(mcp):
    # Arrange
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = True
        
        # Act
        result = mcp.verify_structure()
        
        # Assert
        assert result is True

@pytest.mark.asyncio
async def test_verify_structure_missing_path(mcp):
    # Arrange
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = False
        
        # Act
        result = mcp.verify_structure()
        
        # Assert
        assert result is False

@pytest.mark.asyncio
async def test_initialize_subsystems(mcp):
    # Arrange
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = True
        
        # Act
        result = mcp.initialize_subsystems()
        
        # Assert
        assert result is True

@pytest.mark.asyncio
async def test_initialize_subsystems_missing(mcp):
    # Arrange
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = False
        
        # Act
        result = mcp.initialize_subsystems()
        
        # Assert
        assert result is False

@pytest.mark.asyncio
async def test_initialize(mcp):
    # Arrange
    with patch.multiple(mcp,
                       verify_structure=Mock(return_value=True),
                       verify_dependencies=Mock(return_value=True),
                       initialize_subsystems=Mock(return_value=True)):
        
        # Act
        result = await mcp.initialize()
        
        # Assert
        assert result is True
        assert mcp.initialized is True

@pytest.mark.asyncio
async def test_initialize_failure(mcp):
    # Arrange
    with patch.multiple(mcp,
                       verify_structure=Mock(return_value=False),
                       verify_dependencies=Mock(return_value=True),
                       initialize_subsystems=Mock(return_value=True)):
        
        # Act
        result = await mcp.initialize()
        
        # Assert
        assert result is False
        assert mcp.initialized is False

@pytest.mark.asyncio
async def test_run_initialization_failure(mcp):
    # Arrange
    with patch.object(mcp, 'initialize', return_value=False):
        
        # Act
        await mcp.run()
        
        # Assert
        assert mcp.initialized is False

@pytest.mark.asyncio
async def test_process_message_error(mcp, mock_writer):
    # Arrange
    test_message = {"type": "test", "id": "123"}
    mock_writer.write.side_effect = Exception("Test error")
    
    # Act
    await mcp.process_message(test_message)
    
    # Assert
    expected_error = {
        "type": "error",
        "id": "123",
        "error": "Test error"
    }
    expected_data = json.dumps(expected_error).encode() + b"\n"
    assert mock_writer.write.call_count == 2  # First attempt + error response 

@pytest.mark.asyncio
async def test_setup_logging(mcp):
    """Testa a configuração de logging."""
    # Arrange
    with patch("logging.basicConfig") as mock_basic_config:
        # Act
        mcp.setup_logging()
        
        # Assert
        mock_basic_config.assert_called_once()

@pytest.mark.asyncio
async def test_verify_dependencies(mcp):
    """Testa a verificação de dependências."""
    # Arrange
    with patch("builtins.__import__") as mock_import:
        # Act & Assert - Sucesso
        mock_import.return_value = None
        assert mcp.verify_dependencies() is True
        
        # Act & Assert - Falha
        mock_import.side_effect = ImportError("Test error")
        assert mcp.verify_dependencies() is False

@pytest.mark.asyncio
async def test_run_success(mcp):
    """Testa a execução bem-sucedida do MCP."""
    # Arrange
    async def mock_initialize():
        mcp.initialized = True
        return True
        
    with patch.object(mcp, 'initialize', side_effect=mock_initialize), \
         patch.object(mcp, 'read_message', side_effect=[{"type": "shutdown"}]):
        
        # Act
        await mcp.run()
        
        # Assert
        assert mcp.initialized is True
        assert mcp.running is False

@pytest.mark.asyncio
async def test_main_initialization():
    """Testa a inicialização básica da função main."""
    # Arrange
    mock_mcp = AsyncMock(spec=BiosQMCP)
    mock_writer = AsyncMock(spec=StreamWriter)
    mock_reader = AsyncMock(spec=StreamReader)
    mock_loop = AsyncMock()
    mock_protocol = AsyncMock(spec=BiosQProtocol)

    mock_loop.connect_read_pipe = AsyncMock(return_value=(mock_protocol, mock_protocol))
    mock_loop.connect_write_pipe = AsyncMock(return_value=(mock_protocol, mock_protocol))

    with patch('mcp.bios_q_mcp.BiosQMCP', return_value=mock_mcp), \
         patch('asyncio.StreamWriter', return_value=mock_writer), \
         patch('asyncio.StreamReader', return_value=mock_reader), \
         patch('asyncio.get_event_loop', return_value=mock_loop), \
         patch('mcp.bios_q_mcp.BiosQProtocol', return_value=mock_protocol), \
         patch('sys.stdin'), \
         patch('sys.stdout'):

        # Configure mock_writer
        mock_writer.wait_closed = AsyncMock()
        mock_writer.close = Mock()
        mock_writer.is_closing = Mock(return_value=False)

        # Configure mock_mcp
        mock_mcp.run = AsyncMock()

        # Act
        result = await main()

        # Assert
        assert result is True
        mock_mcp.run.assert_awaited_once()
        mock_writer.close.assert_called_once()

@pytest.mark.asyncio
async def test_main_cleanup():
    """Testa o cleanup adequado na função main."""
    # Arrange
    mock_mcp = AsyncMock(spec=BiosQMCP)
    mock_writer = AsyncMock(spec=StreamWriter)
    mock_reader = AsyncMock(spec=StreamReader)
    mock_loop = AsyncMock()
    mock_protocol = AsyncMock(spec=BiosQProtocol)

    mock_loop.connect_read_pipe = AsyncMock(return_value=(mock_protocol, mock_protocol))
    mock_loop.connect_write_pipe = AsyncMock(return_value=(mock_protocol, mock_protocol))

    with patch('mcp.bios_q_mcp.BiosQMCP', return_value=mock_mcp), \
         patch('asyncio.StreamWriter', return_value=mock_writer), \
         patch('asyncio.StreamReader', return_value=mock_reader), \
         patch('asyncio.get_event_loop', return_value=mock_loop), \
         patch('mcp.bios_q_mcp.BiosQProtocol', return_value=mock_protocol), \
         patch('sys.stdin'), \
         patch('sys.stdout'):

        # Configure mock_writer
        mock_writer.wait_closed = AsyncMock()
        mock_writer.close = Mock()
        mock_writer.is_closing = Mock(return_value=False)

        # Configure mock_mcp
        mock_mcp.run = AsyncMock()

        # Act
        await main()

        # Assert
        mock_writer.close.assert_called_once()

@pytest.mark.asyncio
async def test_main_with_real_transport():
    """Testa a função main com transporte real."""
    # Arrange
    mock_mcp = AsyncMock(spec=BiosQMCP)
    mock_writer = AsyncMock(spec=StreamWriter)
    mock_reader = AsyncMock(spec=StreamReader)
    mock_loop = AsyncMock()
    mock_protocol = AsyncMock(spec=BiosQProtocol)

    mock_loop.connect_read_pipe = AsyncMock(return_value=(mock_protocol, mock_protocol))
    mock_loop.connect_write_pipe = AsyncMock(return_value=(mock_protocol, mock_protocol))

    with patch('mcp.bios_q_mcp.BiosQMCP', return_value=mock_mcp), \
         patch('asyncio.StreamWriter', return_value=mock_writer), \
         patch('asyncio.StreamReader', return_value=mock_reader), \
         patch('asyncio.get_event_loop', return_value=mock_loop), \
         patch('mcp.bios_q_mcp.BiosQProtocol', return_value=mock_protocol), \
         patch('sys.stdin'), \
         patch('sys.stdout'):

        # Configure mock_writer
        mock_writer.wait_closed = AsyncMock()
        mock_writer.close = Mock()
        mock_writer.is_closing = Mock(return_value=False)

        # Configure mock_mcp
        mock_mcp.run = AsyncMock()

        # Act
        await main()

        # Assert
        mock_mcp.run.assert_awaited_once()
        mock_writer.close.assert_called_once()

@pytest.mark.asyncio
async def test_process_message_invalid_json(mcp, mock_reader):
    """Testa o processamento de uma mensagem com JSON inválido."""
    # Arrange
    mock_reader.readline.return_value = b"invalid json\n"
    
    # Act
    result = await mcp.read_message()
    
    # Assert
    assert result is None

@pytest.mark.asyncio
async def test_verify_dependencies_specific_modules(mcp):
    """Testa a verificação de dependências específicas."""
    # Arrange
    test_modules = ["asyncio", "json", "logging"]
    
    # Act & Assert
    with patch("builtins.__import__") as mock_import:
        mock_import.return_value = None
        assert mcp.verify_dependencies(test_modules) is True
        assert mock_import.call_count == len(test_modules)

@pytest.mark.asyncio
async def test_run_with_multiple_messages(mcp):
    """Testa a execução do MCP com múltiplas mensagens."""
    # Arrange
    messages = [
        {"type": "test", "data": "message1"},
        {"type": "test", "data": "message2"},
        {"type": "shutdown"}
    ]
    
    async def mock_initialize():
        mcp.initialized = True
        return True
    
    async def mock_read():
        if messages:
            return messages.pop(0)
        return {"type": "shutdown"}
    
    # Act
    with patch.object(mcp, 'initialize', side_effect=mock_initialize), \
         patch.object(mcp, 'read_message', side_effect=mock_read):
        await mcp.run()
        
        # Assert
        assert mcp.initialized is True
        assert mcp.running is False

@pytest.mark.asyncio
async def test_display_banner(mcp, capsys):
    """Testa a exibição do banner."""
    # Act
    mcp.display_banner()
    
    # Assert
    captured = capsys.readouterr()
    assert "EVA & GUARANI - BIOS-Q MCP" in captured.out
    assert "Version: 8.0" in captured.out

@pytest.mark.asyncio
async def test_process_message_with_invalid_type(mcp):
    """Testa o processamento de mensagem com tipo inválido."""
    # Arrange
    test_message = {"type": "invalid_type", "id": "123"}
    
    # Act
    await mcp.process_message(test_message)
    
    # Assert
    # Verifica se a mensagem foi processada sem erros
    assert mcp.running is True

@pytest.mark.asyncio
async def test_run_with_display_banner(mcp):
    """Testa a execução com exibição do banner."""
    # Arrange
    messages = [{"type": "shutdown"}]
    mcp.config["initialization"]["display_banner"] = True
    
    async def mock_initialize():
        mcp.initialized = True
        return True
    
    async def mock_read():
        if messages:
            return messages.pop(0)
        return {"type": "shutdown"}
    
    # Act
    with patch.object(mcp, 'initialize', side_effect=mock_initialize), \
         patch.object(mcp, 'read_message', side_effect=mock_read), \
         patch.object(mcp, 'display_banner') as mock_display:
        await mcp.run()
        
        # Assert
        mock_display.assert_called_once()
        assert mcp.initialized is True
        assert mcp.running is False

@pytest.mark.asyncio
async def test_connection_protocol():
    """Testa os métodos do protocolo de conexão."""
    # Arrange
    protocol = BiosQProtocol()
    transport = Mock(spec=asyncio.BaseTransport)
    
    # Act & Assert
    protocol.connection_made(transport)  # Não deve levantar exceção
    protocol.connection_lost(None)  # Não deve levantar exceção

@pytest.fixture
def test_protocol():
    """Fixture que fornece um protocolo de teste."""
    loop = asyncio.new_event_loop()
    protocol = BiosQProtocol()
    protocol._closed = loop.create_future()
    protocol._closed.set_result(None)
    return protocol

if __name__ == "__main__":
    pytest.main(["-v", "--cov=mcp", "--cov-report=html"]) 