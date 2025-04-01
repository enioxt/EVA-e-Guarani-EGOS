#!/usr/bin/env python3
"""
EVA & GUARANI MCP Framework
==========================

Framework para integração e gerenciamento de Model Context Protocols.

Este framework fornece uma base robusta para lidar com diversos MCPs,
permitindo que modelos de linguagem acessem ferramentas e fontes de dados
externas de forma padronizada e segura.
"""

__version__ = "1.0.0"
__author__ = "EVA & GUARANI"

# Importações principais para facilitar o uso
from mcp.core.mcp_manager import MCPManager
from mcp.integrations.mcp_integration import MCPIntegration

# Adaptadores MCP específicos
from mcp.integrations.sequential_thinking import SequentialThinkingAdapter
from mcp.integrations.perplexity import PerplexityAdapter 