#!/bin/bash

# Cores para saída no terminal
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RESET='\033[0m'

echo "===================================================="
echo "       INICIANDO EVA & GUARANI - EGOS v7.0"
echo "===================================================="
echo ""

# Obter diretório base do script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Configurar ambiente
export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR:$SCRIPT_DIR/EGOS"
export EGOS_ROOT="$SCRIPT_DIR"

# Verificar dependências
python3 -c "import sys; sys.exit(0 if all(map(lambda m: m in sys.modules or __import__(m, fromlist=['']) , ['os', 'sys', 'json', 'datetime'])) else 1)" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Falha ao instalar dependências. Verifique o arquivo requirements.txt."
        exit 1
    fi
fi

# Verificar se diretórios existem
if [ ! -d "$SCRIPT_DIR/EGOS" ]; then
    echo "Estrutura de diretórios EGOS não encontrada."
    echo "Execute python3 reorganize_egos.py para criar a estrutura necessária."
    exit 1
fi

echo "Carregando núcleo do sistema..."
echo ""

# Execução principal
python3 EGOS/core/egos_core.py "$@"

echo ""
echo "===================================================="
echo "         EVA & GUARANI - EGOS FINALIZADO"
echo "===================================================="
echo -e "${GREEN}✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧${RESET}"

# Tornar o script executável
chmod +x "$0"
