#!/usr/bin/env python3
import asyncio
import json
import sys
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("bios-q-test-mcp")


class BiosQTool:
    """Represents a tool that can be used by the MCP."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.schema = {"type": "object", "properties": {}, "required": []}


class BiosQTestMCP:
    """A test implementation of the BIOS-Q MCP following the MCP protocol."""

    def __init__(self):
        self.initialized = False
        self.running = False
        self.tools = self._register_tools()
        self.message_handlers = {
            "initialize": self.handle_initialize,
            "shutdown": self.handle_shutdown,
            "status": self.handle_status,
            "list_tools": self.handle_list_tools,
            "execute": self.handle_execute,
        }
        logger.info("BiosQTestMCP instance created")

    def _register_tools(self) -> List[BiosQTool]:
        """Register available tools."""
        return [
            BiosQTool(
                name="bios_q_status", description="Get the current status of the BIOS-Q system"
            ),
            BiosQTool(
                name="bios_q_heartbeat", description="Check if BIOS-Q is alive and responding"
            ),
        ]

    async def handle_initialize(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request."""
        self.initialized = True
        return {
            "type": "response",
            "id": message.get("id"),
            "status": "success",
            "data": {
                "initialized": True,
                "version": "1.0",
                "capabilities": ["list_tools", "execute", "status"],
            },
        }

    async def handle_list_tools(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool listing request."""
        tools_data = [
            {"name": tool.name, "description": tool.description, "schema": tool.schema}
            for tool in self.tools
        ]
        return {
            "type": "response",
            "id": message.get("id"),
            "status": "success",
            "data": {"tools": tools_data},
        }

    async def handle_execute(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution request."""
        tool_name = message.get("tool")
        if not tool_name:
            return {"type": "error", "id": message.get("id"), "error": "Tool name not specified"}

        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            return {
                "type": "error",
                "id": message.get("id"),
                "error": f"Tool '{tool_name}' not found",
            }

        # Handle specific tools
        if tool_name == "bios_q_status":
            return {
                "type": "response",
                "id": message.get("id"),
                "status": "success",
                "data": {
                    "initialized": self.initialized,
                    "running": self.running,
                    "timestamp": datetime.now().isoformat(),
                },
            }
        elif tool_name == "bios_q_heartbeat":
            return {
                "type": "response",
                "id": message.get("id"),
                "status": "success",
                "data": {"status": "active", "timestamp": datetime.now().isoformat()},
            }

        # Default response for unknown tool
        return {
            "type": "error",
            "id": message.get("id"),
            "error": f"Tool '{tool_name}' execution not implemented",
        }

    async def handle_shutdown(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle shutdown request."""
        self.running = False
        return {
            "type": "response",
            "id": message.get("id"),
            "status": "success",
            "data": {"message": "Shutting down"},
        }

    async def handle_status(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle status request."""
        return {
            "type": "response",
            "id": message.get("id"),
            "status": "success",
            "data": {
                "initialized": self.initialized,
                "running": self.running,
                "timestamp": datetime.now().isoformat(),
            },
        }

    async def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process an incoming message."""
        try:
            message_type = message.get("type")
            if not message_type:
                raise ValueError("Message type not specified")

            handler = self.message_handlers.get(message_type)
            if not handler:
                raise ValueError(f"Unknown message type: {message_type}")

            response = await handler(message)
            return response

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {"type": "error", "id": message.get("id"), "error": str(e)}

    async def read_message(self) -> Optional[Dict[str, Any]]:
        """Read a message from stdin."""
        try:
            line = sys.stdin.buffer.readline()
            if not line:
                return None
            return json.loads(line.decode())
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON received: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error reading message: {str(e)}")
            return None

    async def write_message(self, message: Dict[str, Any]) -> None:
        """Write a message to stdout."""
        try:
            line = json.dumps(message).encode() + b"\n"
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.flush()
            logger.debug(f"Message sent: {message}")
        except Exception as e:
            logger.error(f"Error writing message: {str(e)}")

    async def run(self) -> None:
        """Main run loop."""
        logger.info("Starting BiosQTestMCP")
        self.running = True

        # Display banner
        print("\n✧༺❀༻∞ EVA & GUARANI - BIOS-Q Test MCP ∞༺❀༻✧")
        print("Version: 1.0")
        print("Status: Starting")
        print("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

        while self.running:
            try:
                # Read message
                message = await self.read_message()
                if not message:
                    await asyncio.sleep(0.1)  # Prevent CPU spinning
                    continue

                # Process message
                response = await self.process_message(message)
                if response:
                    await self.write_message(response)

            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt")
                self.running = False
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                await asyncio.sleep(1)

        logger.info("BiosQTestMCP shutting down")


async def main() -> None:
    """Main entry point."""
    if sys.platform == "win32":
        # Set up Windows-specific event loop policy
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    mcp = BiosQTestMCP()
    await mcp.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process terminated by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
