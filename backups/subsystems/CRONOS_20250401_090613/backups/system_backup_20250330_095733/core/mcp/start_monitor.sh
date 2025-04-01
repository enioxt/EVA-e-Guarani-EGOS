#!/bin/bash
# Script para iniciar o monitor de contexto MCP no Linux/Mac

cd "$(dirname "$0")"
echo "Iniciando monitor de contexto MCP a 80%..."
python3 context_monitor.py &

echo "Monitor iniciado em segundo plano."
echo "Verificando status..."
python3 cursor_commands.py mcp_status

echo ""
echo "O monitor continuará rodando em segundo plano."
echo "Para verificar o status, use o comando: python3 cursor_commands.py mcp_status" 