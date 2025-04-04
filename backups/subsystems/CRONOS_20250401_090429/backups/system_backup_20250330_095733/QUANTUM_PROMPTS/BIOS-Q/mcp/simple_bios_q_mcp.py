#!/usr/bin/env python3
import asyncio
import json
import sys
import logging
from datetime import datetime

# Configurar logging básico
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("simple-bios-q-mcp")


class SimpleBiosQMCP:
    def __init__(self):
        self.running = True
        logger.info("SimpleBiosQMCP initialized")

    async def read_message(self):
        """Lê mensagens da entrada padrão."""
        try:
            line = sys.stdin.buffer.readline()
            if not line:
                return None
            return json.loads(line.decode())
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return None
        except Exception as e:
            logger.error(f"Error reading message: {str(e)}")
            return None

    async def write_message(self, message):
        """Escreve mensagens na saída padrão."""
        try:
            line = json.dumps(message).encode() + b"\n"
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.flush()
            logger.debug(f"Message sent: {message}")
        except Exception as e:
            logger.error(f"Error writing message: {str(e)}")

    async def run(self):
        """Loop principal simplificado."""
        logger.info("Starting SimpleBiosQMCP")

        # Display banner
        print("\n✧༺❀༻∞ EVA & GUARANI - Simple BIOS-Q MCP ∞༺❀༻✧")
        print("Version: 1.0")
        print("Status: Active")
        print("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

        heartbeat_count = 0

        while self.running:
            try:
                # Enviar heartbeat a cada 5 segundos
                heartbeat = {
                    "type": "heartbeat",
                    "id": f"heartbeat-{datetime.now().timestamp()}",
                    "timestamp": datetime.now().isoformat(),
                    "status": "active",
                }
                await self.write_message(heartbeat)
                heartbeat_count += 1
                logger.debug(f"Heartbeat sent ({heartbeat_count})")

                # Aguardar mensagens
                await asyncio.sleep(5)

            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt")
                self.running = False
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                await asyncio.sleep(1)

        logger.info("SimpleBiosQMCP shutting down")


async def main():
    """Função principal."""
    mcp = SimpleBiosQMCP()
    await mcp.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process terminated by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
