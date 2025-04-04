#!/usr/bin/env python3
"""
BIOS-Q: Sistema Quântico de Preservação e Gestão de Contexto

Este módulo implementa a interface principal do BIOS-Q, fornecendo
funções para gestão de contexto, compressão quântica de prompts e
integração com outros sistemas como MCP, ATLAS e ETHIK.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

# Importa componentes principais
from core.context_manager import BIOSQContextManager
from quantum.prompt_encoder import QuantumPromptEncoder
from integrations.mcp_connector import MCPConnector


class BIOSQ:
    """
    Interface principal do BIOS-Q
    """

    def __init__(self, use_mcp=True):
        """
        Inicializa o BIOS-Q com seus componentes principais
        """
        self.context_manager = BIOSQContextManager()
        self.prompt_encoder = QuantumPromptEncoder()

        self.mcp_connector = None
        if use_mcp:
            try:
                self.mcp_connector = MCPConnector()
            except Exception as e:
                print(f"Aviso: Não foi possível inicializar o conector MCP: {str(e)}")

    def add_message(self, role, content, metadata=None):
        """Adiciona uma mensagem ao contexto atual"""
        return self.context_manager.add_message(role, content, metadata)

    def save_context(self, path=None):
        """Salva o contexto atual em um arquivo"""
        return self.context_manager.save_context(path)

    def load_context(self, path):
        """Carrega o contexto de um arquivo"""
        return self.context_manager.load_context(path)

    def save_to_mcp(self):
        """Salva o contexto atual usando o MCP"""
        if not self.mcp_connector:
            return {"success": False, "message": "MCP não está disponível"}
        return self.mcp_connector.save_to_mcp()

    def load_from_mcp(self, file_path=None):
        """Carrega contexto do MCP"""
        if not self.mcp_connector:
            return {"success": False, "message": "MCP não está disponível"}
        return self.mcp_connector.load_from_mcp(file_path)

    def update_context_limit(self, current_size):
        """Atualiza o limite de contexto baseado em medição empírica"""
        if not self.mcp_connector:
            return self.context_manager.update_max_tokens(current_size)
        return self.mcp_connector.update_context_limit(current_size)

    def encode_quantum_prompt(self, prompt, domain="general"):
        """Codifica um prompt em formato quântico comprimido"""
        return self.prompt_encoder.encode_prompt(prompt, domain)

    def prune_context(self, strategy="recency"):
        """Remove partes menos relevantes do contexto para economizar tokens"""
        return self.context_manager.prune_context(strategy)

    def get_status(self):
        """Retorna o status atual do BIOS-Q"""
        status = self.context_manager.get_context_summary()
        status["mcp_available"] = self.mcp_connector is not None
        return status


# Exporta a API principal
__all__ = ["BIOSQ", "BIOSQContextManager", "QuantumPromptEncoder", "MCPConnector"]
