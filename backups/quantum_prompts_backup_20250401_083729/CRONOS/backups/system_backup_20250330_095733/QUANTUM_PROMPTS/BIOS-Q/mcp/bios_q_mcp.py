#!/usr/bin/env python3
"""
BIOS-Q MCP - Main Script
------------------------
Este é o script principal do BIOS-Q MCP que gerencia
a inicialização e configuração do sistema quantum.

Version: 8.0
Created: 2025-03-26
"""

import os
import sys
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    import debugpy
except ImportError:
    debugpy = None

# Configurar logging - Garantir que o diretório de logs exista
log_dir = Path("C:\\Eva Guarani EGOS\\logs")
log_dir.mkdir(exist_ok=True, parents=True)
log_file = log_dir / "bios_q.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(str(log_file)), logging.StreamHandler()],
)
logger = logging.getLogger("bios-q-mcp")

# Marcar início da sessão com um timestamp
logger.info(f"Nova sessão iniciada: {datetime.now().isoformat()}")


class BiosQMCP:
    """Gerenciador principal do BIOS-Q MCP."""

    def __init__(self):
        self.running = True
        self.initialized = False
        self.setup_logging()
        self.load_config()
        logger.info("BiosQMCP instance initialized")

    def setup_logging(self):
        """Configura o sistema de logging."""
        log_dir = Path("C:/Eva Guarani EGOS/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "bios_q_mcp.log"
        log_level = os.getenv("QUANTUM_LOG_LEVEL", "DEBUG")

        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stderr)],
        )
        self.logger = logging.getLogger("BIOS-Q")
        self.logger.info("Logging initialized")

    def load_config(self):
        """Carrega a configuração do BIOS-Q."""
        config_path = os.getenv("BIOS_Q_CONFIG")
        if not config_path:
            raise ValueError("BIOS_Q_CONFIG environment variable not set")

        self.logger.info(f"Loading config from {config_path}")
        try:
            with open(config_path) as f:
                self.config = json.load(f)
            self.logger.info("Config loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            raise

    def verify_structure(self) -> bool:
        """Verifica a estrutura de diretórios necessária."""
        paths = self.config["paths"]
        for path_name, path in paths.items():
            path_obj = Path(path)
            if not path_obj.exists():
                logger.error(f"Required path {path_name} does not exist: {path}")
                return False
            logger.info(f"Found required path {path_name}: {path}")
        return True

    def verify_dependencies(self, modules: Optional[List[str]] = None) -> bool:
        """Verifica as dependências do sistema."""
        try:
            default_modules = ["asyncio", "json", "logging"]
            modules_to_check = modules if modules is not None else default_modules

            for module in modules_to_check:
                try:
                    __import__(module)
                    logger.info(f"Dependency check passed: {module}")
                except ImportError as e:
                    logger.error(f"Missing dependency: {str(e)}")
                    return False
            return True
        except Exception as e:
            logger.error(f"Error verifying dependencies: {str(e)}")
            return False

    def initialize_subsystems(self) -> bool:
        """Inicializa os subsistemas do BIOS-Q."""
        subsystems = self.config["subsystems"]
        quantum_prompts_path = Path(self.config["paths"]["quantum_prompts"])

        for name, info in subsystems.items():
            if info["required"]:
                path = quantum_prompts_path / name
                if not path.exists():
                    logger.error(f"Required subsystem {name} not found at {path}")
                    return False
                logger.info(f"Subsystem {name} found at {path}")
        return True

    async def initialize(self) -> bool:
        """Inicializa o BIOS-Q MCP."""
        logger.info("Initializing BIOS-Q MCP")

        if not self.verify_structure():
            return False

        if not self.verify_dependencies():
            return False

        if not self.initialize_subsystems():
            return False

        self.initialized = True
        logger.info("BIOS-Q MCP initialized successfully")
        return True

    def display_banner(self):
        """Exibe o banner do BIOS-Q."""
        banner = """
✧༺❀༻∞ EVA & GUARANI - BIOS-Q MCP ∞༺❀༻✧
Version: 8.0
Status: Initialized
Quantum State: Active
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""
        print(banner, flush=True)
        logger.info("Banner displayed")

    async def read_message(self) -> Optional[Dict[str, Any]]:
        """Lê uma mensagem do stdin."""
        try:
            if sys.platform == "win32":
                # No Windows, usar sys.stdin.buffer diretamente
                line = sys.stdin.buffer.readline()
            else:
                # Em outros sistemas, usar asyncio
                loop = asyncio.get_running_loop()
                line = await loop.run_in_executor(None, sys.stdin.buffer.readline)

            if not line:
                self.logger.warning("No data received (EOF)")
                return None

            message = json.loads(line.decode())
            self.logger.debug(f"Received message: {message}")
            return message
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading message: {e}")
            return None

    async def write_message(self, message: Dict[str, Any]) -> None:
        """Escreve uma mensagem para stdout."""
        try:
            self.logger.debug(f"Sending message: {message}")
            data = json.dumps(message).encode() + b"\n"

            if sys.platform == "win32":
                # No Windows, usar sys.stdout.buffer diretamente
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            else:
                # Em outros sistemas, usar asyncio
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(None, sys.stdout.buffer.write, data)
                await loop.run_in_executor(None, sys.stdout.buffer.flush)

            self.logger.debug("Message sent successfully")
        except Exception as e:
            self.logger.error(f"Error writing message: {e}")
            raise

    async def send_heartbeat(self) -> None:
        """Envia uma mensagem de heartbeat para indicar que o MCP está ativo."""
        heartbeat = {
            "type": "heartbeat",
            "id": f"heartbeat-{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "status": "active",
        }
        try:
            await self.write_message(heartbeat)
            self.last_heartbeat = datetime.now()
            logger.debug("Heartbeat sent")
        except Exception as e:
            logger.error(f"Failed to send heartbeat: {e}")

    async def process_message(self, message: Dict[str, Any]) -> None:
        """Processa uma mensagem recebida do Cursor."""
        try:
            self.logger.info(f"Processing message type: {message.get('type')}")

            if message.get("type") == "shutdown":
                self.logger.info("Received shutdown command")
                self.running = False
                return

            if message.get("type") == "ping":
                self.logger.debug("Received ping, sending pong")
                await self.write_message(
                    {
                        "type": "pong",
                        "id": message.get("id"),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
                return

            # Resposta padrão
            response = {
                "type": "response",
                "id": message.get("id"),
                "status": "success",
                "data": {"message": "Message processed successfully"},
            }
            await self.write_message(response)
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            error_response = {"type": "error", "id": message.get("id"), "error": str(e)}
            await self.write_message(error_response)

    async def run(self) -> None:
        """Executa o loop principal do MCP."""
        if not await self.initialize():
            logger.error("Failed to initialize BIOS-Q MCP")
            return

        if self.config["initialization"].get("display_banner", True):
            self.display_banner()

        logger.info("BIOS-Q MCP running...")

        # Enviar heartbeat inicial
        await self.send_heartbeat()

        heartbeat_interval = 10  # segundos
        last_heartbeat_time = datetime.now()

        while self.running:
            try:
                # Verificar se é hora de enviar um heartbeat
                current_time = datetime.now()
                if (current_time - last_heartbeat_time).total_seconds() >= heartbeat_interval:
                    await self.send_heartbeat()
                    last_heartbeat_time = current_time

                # Tentar ler uma mensagem com timeout
                try:
                    message = await asyncio.wait_for(self.read_message(), 1.0)
                    if message is not None:
                        await self.process_message(message)
                except asyncio.TimeoutError:
                    # Timeout normal, continuar o loop
                    continue

            except asyncio.CancelledError:
                logger.info("BIOS-Q MCP received cancellation signal")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                await asyncio.sleep(1)
                continue

        logger.info("BIOS-Q MCP shutting down gracefully...")


async def main() -> bool:
    """Função principal que inicializa e executa o BIOS-Q MCP."""
    try:
        # Configurar debugpy se disponível
        if debugpy:
            try:
                debugpy.listen(("127.0.0.1", 5678))
                print("Debugger listening on port 5678")
            except Exception as e:
                print(f"Failed to start debugger: {e}")

        # Configurar logging inicial
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger("BIOS-Q")

        # Criar e executar MCP
        mcp = BiosQMCP()
        await mcp.run()

        logger.info("BIOS-Q MCP terminated successfully")
        return True

    except Exception as e:
        logger.error(f"Fatal error in main(): {e}")
        return False


if __name__ == "__main__":
    try:
        # Registrar início do processo
        logger.info(f"BIOS-Q MCP process starting with PID: {os.getpid()}")

        # Configurar o loop de eventos para Windows
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        # Executar o loop de eventos
        logger.info("Starting main coroutine with asyncio.run()")
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("BIOS-Q MCP terminated by user")
    except Exception as e:
        logger.error(f"BIOS-Q MCP terminated with error: {str(e)}")
    finally:
        logger.info("BIOS-Q MCP shutdown complete")
