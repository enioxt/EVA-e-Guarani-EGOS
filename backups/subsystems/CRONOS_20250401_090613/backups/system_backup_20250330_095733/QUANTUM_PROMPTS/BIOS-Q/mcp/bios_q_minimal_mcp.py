#!/usr/bin/env python3
import asyncio
import json
import sys

class BiosQMinimalMCP:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.running = True

    async def read_message(self):
        try:
            data = await self.reader.readline()
            if not data:
                return None
            return json.loads(data.decode())
        except:
            return None

    async def write_message(self, message):
        try:
            data = json.dumps(message).encode() + b"\n"
            self.writer.write(data)
            await self.writer.drain()
        except:
            pass

    async def process_message(self, message):
        msg_type = message.get("type")
        msg_id = message.get("id")

        if msg_type == "shutdown":
            self.running = False
            response = {"type": "response", "id": msg_id, "status": "success"}
        elif msg_type == "list_tools":
            response = {
                "type": "response",
                "id": msg_id,
                "status": "success",
                "data": {
                    "tools": [{
                        "name": "bios_q_status",
                        "description": "Get BIOS-Q status",
                        "schema": {"type": "object", "properties": {}}
                    }]
                }
            }
        else:
            response = {"type": "response", "id": msg_id, "status": "success"}

        await self.write_message(response)

    async def run(self):
        while self.running:
            message = await self.read_message()
            if message:
                await self.process_message(message)

async def main():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.Protocol()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    w_transport, w_protocol = await loop.connect_write_pipe(lambda: protocol, sys.stdout)
    writer = asyncio.StreamWriter(w_transport, w_protocol, reader, loop)

    mcp = BiosQMinimalMCP(reader, writer)
    await mcp.run()

    if not writer.is_closing():
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main()) 