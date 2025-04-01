#!/usr/bin/env python3
import asyncio
import json
import sys
import logging
from typing import Any, Dict, Optional

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('bios_q_simple_mcp')

class BiosQSimpleMCP:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.running = True
        self.initialized = False
        logger.info("BiosQSimpleMCP initialized")

    async def read_message(self) -> Optional[Dict[str, Any]]:
        try:
            data = await self.reader.readline()
            if not data:
                return None
            return json.loads(data.decode())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading message: {e}")
            return None

    async def write_message(self, message: Dict[str, Any]) -> None:
        try:
            data = json.dumps(message).encode() + b"\n"
            self.writer.write(data)
            await self.writer.drain()
        except Exception as e:
            logger.error(f"Error writing message: {e}")

    async def initialize(self) -> bool:
        self.initialized = True
        return True

    async def process_message(self, message: Dict[str, Any]) -> None:
        try:
            msg_type = message.get("type")
            msg_id = message.get("id")

            if msg_type == "initialize":
                success = await self.initialize()
                response = {
                    "type": "response",
                    "id": msg_id,
                    "status": "success" if success else "error",
                    "data": {"initialized": self.initialized}
                }
            elif msg_type == "shutdown":
                self.running = False
                response = {
                    "type": "response",
                    "id": msg_id,
                    "status": "success",
                    "data": {"shutdown": True}
                }
            elif msg_type == "list_tools":
                response = {
                    "type": "response",
                    "id": msg_id,
                    "status": "success",
                    "data": {
                        "tools": [
                            {
                                "name": "bios_q_status",
                                "description": "Get BIOS-Q status",
                                "schema": {"type": "object", "properties": {}}
                            },
                            {
                                "name": "bios_q_heartbeat",
                                "description": "Check if BIOS-Q is alive",
                                "schema": {"type": "object", "properties": {}}
                            }
                        ]
                    }
                }
            elif msg_type == "execute":
                tool_name = message.get("tool")
                if tool_name == "bios_q_status":
                    response = {
                        "type": "response",
                        "id": msg_id,
                        "status": "success",
                        "data": {
                            "initialized": self.initialized,
                            "running": self.running
                        }
                    }
                elif tool_name == "bios_q_heartbeat":
                    response = {
                        "type": "response",
                        "id": msg_id,
                        "status": "success",
                        "data": {"alive": True}
                    }
                else:
                    response = {
                        "type": "error",
                        "id": msg_id,
                        "error": f"Unknown tool: {tool_name}"
                    }
            else:
                response = {
                    "type": "error",
                    "id": msg_id,
                    "error": f"Unknown message type: {msg_type}"
                }

            await self.write_message(response)

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_response = {
                "type": "error",
                "id": msg_id if msg_id else "",
                "error": str(e)
            }
            await self.write_message(error_response)

    async def run(self) -> None:
        logger.info("Starting BiosQSimpleMCP")
        while self.running:
            message = await self.read_message()
            if message:
                await self.process_message(message)
        logger.info("BiosQSimpleMCP shutdown")

class BiosQProtocol(asyncio.Protocol):
    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        pass

    def connection_lost(self, exc: Optional[Exception]) -> None:
        pass

async def main() -> bool:
    try:
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = BiosQProtocol()
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)
        w_transport, w_protocol = await loop.connect_write_pipe(lambda: protocol, sys.stdout)
        writer = asyncio.StreamWriter(w_transport, w_protocol, reader, loop)

        mcp = BiosQSimpleMCP(reader, writer)
        await mcp.run()

        if not writer.is_closing():
            writer.close()
            await writer.wait_closed()

        return True

    except Exception as e:
        logger.error(f"Error in main: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(main()) 