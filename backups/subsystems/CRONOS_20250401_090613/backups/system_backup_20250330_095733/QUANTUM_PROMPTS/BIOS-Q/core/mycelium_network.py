#!/usr/bin/env python3
"""
Mycelium Network - EVA & GUARANI Core Module
-------------------------------------------
Este módulo implementa o sistema Mycelium Network que conecta
todos os subsistemas do EVA & GUARANI através de uma rede
neural de nós interconectados.

Version: 8.0
Created: 2025-03-26
"""

import os
import sys
import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Set
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mycelium-network")


class MyceliumNode:
    """Um nó na rede Mycelium."""

    def __init__(self, node_id: str, node_type: str):
        self.node_id = node_id
        self.node_type = node_type
        self.connections: Dict[str, "MyceliumNode"] = {}
        self.data: Dict[str, Any] = {}
        self.last_update = datetime.now()

    async def process_update(self, data: Dict[str, Any]) -> None:
        """Processa uma atualização recebida através da rede."""
        try:
            # Armazena a atualização nos dados do nó
            self.data[data["type"]] = {
                "value": data.get("value"),
                "timestamp": data.get("timestamp", datetime.now().isoformat()),
                "source": data.get("source", "unknown"),
            }

            self.last_update = datetime.now()
            logger.info(f"Node {self.node_id} processed update: {data['type']}")

        except Exception as e:
            logger.error(f"Error processing update in node {self.node_id}: {str(e)}")

    def get_data(self, key: str) -> Optional[Dict[str, Any]]:
        """Obtém dados armazenados no nó."""
        return self.data.get(key)

    def get_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas do nó."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "connections": len(self.connections),
            "data_keys": list(self.data.keys()),
            "last_update": self.last_update.isoformat(),
        }


class MyceliumNetwork:
    """
    A Rede Mycelium que gerencia todas as interconexões
    entre os subsistemas do EVA & GUARANI.
    """

    def __init__(self):
        self.nodes: Dict[str, MyceliumNode] = {}
        self.subsystems = {
            "CRONOS": {"type": "time-management"},
            "ATLAS": {"type": "cartography"},
            "NEXUS": {"type": "analysis"},
            "ETHIK": {"type": "ethics"},
            "QUANTUM_SEARCH": {"type": "search"},
            "TRANSLATOR": {"type": "language"},
            "PROMETHEUS": {"type": "monitoring"},
            "GRAFANA": {"type": "visualization"},
            "PDD": {"type": "prompt-management"},
            "EVA_ATENDIMENTO": {"type": "customer-service"},
        }
        self.last_update = datetime.now()

        # Inicializar subsistemas principais
        self.initialize_subsystems()

    def register_node(self, node_id: str, node_type: str) -> MyceliumNode:
        """Registra um novo nó na rede."""
        if node_id in self.nodes:
            return self.nodes[node_id]

        node = MyceliumNode(node_id, node_type)
        self.nodes[node_id] = node
        self.last_update = datetime.now()
        logger.info(f"Registered node: {node_id} ({node_type})")
        return node

    def remove_node(self, node_id: str) -> bool:
        """Remove um nó da rede e o desconecta."""
        if node_id not in self.nodes:
            return False

        # Obter o nó a ser removido
        node = self.nodes[node_id]

        # Desconectar de todos os nós conectados
        for connected_id in list(node.connections.keys()):
            self.disconnect_nodes(node_id, connected_id)

        # Remover o nó
        del self.nodes[node_id]
        self.last_update = datetime.now()
        logger.info(f"Removed node: {node_id}")
        return True

    def connect_nodes(
        self, source_id: str, target_id: str, connection_type: str = "default"
    ) -> bool:
        """Conecta dois nós na rede."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return False

        source = self.nodes[source_id]
        target = self.nodes[target_id]

        # Adicionar conexão bidirecional
        source.connections[target_id] = target
        target.connections[source_id] = source

        self.last_update = datetime.now()
        logger.info(f"Connected nodes: {source_id} <-> {target_id} ({connection_type})")
        return True

    def disconnect_nodes(self, source_id: str, target_id: str) -> bool:
        """Desconecta dois nós na rede."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return False

        source = self.nodes[source_id]
        target = self.nodes[target_id]

        # Remover conexão bidirecional
        source.connections.pop(target_id, None)
        target.connections.pop(source_id, None)

        self.last_update = datetime.now()
        logger.info(f"Disconnected nodes: {source_id} <-> {target_id}")
        return True

    async def propagate_update(
        self, source_id: str, data: Dict[str, Any], visited: Optional[Set[str]] = None
    ) -> None:
        """
        Propaga uma atualização através da rede começando pelo nó fonte.
        Usa uma abordagem breadth-first para evitar ciclos.
        """
        if source_id not in self.nodes:
            return

        if visited is None:
            visited = set()

        # Marcar fonte como visitada
        visited.add(source_id)
        source = self.nodes[source_id]

        # Atualizar timestamp
        data["propagated_at"] = datetime.now().isoformat()

        # Processar atualização no nó atual
        await source.process_update(data)

        # Propagar para nós conectados
        for node_id, node in source.connections.items():
            if node_id not in visited:
                visited.add(node_id)
                await self.propagate_update(node_id, data, visited)

    def get_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas da rede."""
        total_connections = sum(len(node.connections) for node in self.nodes.values())

        return {
            "total_nodes": len(self.nodes),
            "total_connections": total_connections,
            "last_update": self.last_update.isoformat(),
        }

    def initialize_subsystems(self) -> None:
        """Inicializa todos os nós dos subsistemas e suas conexões."""
        # Registrar todos os nós dos subsistemas
        for subsystem, info in self.subsystems.items():
            self.register_node(subsystem, info["type"])

        # Criar conexões baseadas em dependências
        self.connect_nodes("CRONOS", "ATLAS", "preservation-cartography")
        self.connect_nodes("ATLAS", "NEXUS", "cartography-analysis")
        self.connect_nodes("NEXUS", "ETHIK", "analysis-ethics")
        self.connect_nodes("QUANTUM_SEARCH", "ATLAS", "indexing")
        self.connect_nodes("QUANTUM_SEARCH", "TRANSLATOR", "search-translation")
        self.connect_nodes("PROMETHEUS", "GRAFANA", "monitoring-visualization")
        self.connect_nodes("PDD", "QUANTUM_SEARCH", "prompt-search")
        self.connect_nodes("EVA_ATENDIMENTO", "ETHIK", "service-ethics")

        logger.info("Initialized all subsystem nodes and connections")

    def get_network_status(self) -> Dict[str, Any]:
        """Obtém o status atual da rede Mycelium."""
        return {
            "total_nodes": len(self.nodes),
            "active_connections": sum(len(node.connections) for node in self.nodes.values()) // 2,
            "last_update": max(node.last_update for node in self.nodes.values()),
            "nodes": {
                node_id: {
                    "type": node.node_type,
                    "connections": len(node.connections),
                    "last_update": node.last_update.isoformat(),
                }
                for node_id, node in self.nodes.items()
            },
        }


# Inicializar a rede Mycelium global
mycelium = MyceliumNetwork()

if __name__ == "__main__":
    # Testar a rede Mycelium
    async def test_mycelium():
        print("\n✧༺❀༻∞ EVA & GUARANI - Mycelium Network Test ∞༺❀༻✧\n")

        # Criar nós de teste
        node1 = mycelium.register_node("TEST1", "test")
        node2 = mycelium.register_node("TEST2", "test")

        # Conectar nós
        mycelium.connect_nodes("TEST1", "TEST2")

        # Enviar atualização de teste
        test_data = {
            "type": "test",
            "value": "Hello, Mycelium!",
            "timestamp": datetime.now().isoformat(),
        }

        await mycelium.propagate_update("TEST1", test_data)

        # Imprimir estatísticas da rede
        stats = mycelium.get_stats()
        print(f"\nNetwork Stats:")
        print(f"Total Nodes: {stats['total_nodes']}")
        print(f"Total Connections: {stats['total_connections']}")
        print(f"Last Update: {stats['last_update']}")

        # Limpar nós de teste
        mycelium.remove_node("TEST1")
        mycelium.remove_node("TEST2")

        print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

    # Executar o teste
    asyncio.run(test_mycelium())
