#!/bin/bash

echo "============================================================"
echo "     ✧༺❀༻∞ EVA AND GUARANI UNIFIED BOT ∞༺❀༻✧"
echo "============================================================"
echo ""
echo "Iniciando Bot Unificado..."
echo ""

# Ativar ambiente virtual se existir
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Ambiente virtual ativado."
else
    echo "Ambiente virtual não encontrado. Usando Python do sistema."
fi

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python não encontrado. Por favor, instale o Python 3.7 ou superior."
    exit 1
fi

# Iniciar o bot unificado
echo "Iniciando o Bot Unificado EVA & GUARANI..."
python3 unified_eva_guarani_bot.py

# Desativar ambiente virtual se ativado
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi

echo ""
echo "Bot encerrado." 