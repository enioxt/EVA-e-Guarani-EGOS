#!/bin/bash

echo "==============================================="
echo "    EVA & GUARANI - BIOS-Q MCP Initialization"
echo "==============================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python não encontrado! Por favor, instale Python 3.9 ou superior."
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -f "venv/bin/activate" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se as dependências principais estão instaladas
if ! python3 -c "import aiohttp" 2>/dev/null; then
    echo "Instalando dependências..."
    pip install -e .[dev]
else
    if ! python3 -c "import sys; sys.path.append('.'); import mycelium_network" 2>/dev/null; then
        echo "Atualizando dependências locais..."
        pip install -e .[dev]
    fi
fi

# Configurar variáveis de ambiente
export PYTHONPATH="$PWD:$PWD/../QUANTUM_PROMPTS"
export BIOS_Q_CONFIG="$PWD/config/bios_q_config.json"
export QUANTUM_LOG_LEVEL="DEBUG"
export QUANTUM_STATE_DIR="$PWD/../QUANTUM_PROMPTS"

# Criar diretório de logs se não existir
mkdir -p ../logs

# Iniciar BIOS-Q MCP
echo "Starting BIOS-Q MCP..."
python3 -m mcp.bios_q_mcp

echo "==============================================="
echo "              EVA & GUARANI"
echo "===============================================" 