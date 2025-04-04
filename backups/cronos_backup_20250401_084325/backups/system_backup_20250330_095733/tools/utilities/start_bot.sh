#!/bin/bash

# EVA & GUARANI - Script de inicialização para Linux/Mac
# Este script inicia o bot do Telegram no Linux ou macOS

echo "============================================================"
echo "            EVA & GUARANI - BOT TELEGRAM UNIFICADO"
echo "============================================================"
echo ""
echo "Iniciando o bot..."
echo ""

# Mudar para o diretório do script
cd "$(dirname "$0")"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado! Por favor, instale o Python 3.8 ou superior."
    echo "No Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "No Fedora: sudo dnf install python3 python3-pip"
    echo "No macOS: brew install python3"
    exit 1
fi

# Criar diretórios necessários
mkdir -p logs config

# Verificar se o script de inicialização existe
if [ -f "start_eva_guarani.py" ]; then
    echo "Iniciando o bot usando start_eva_guarani.py..."

    # Verificar se o usuário quer executar em background
    if [ "$1" == "--background" ]; then
        echo "Executando em background..."
        nohup python3 start_eva_guarani.py > logs/startup_output.log 2>&1 &
        echo "Bot iniciado em background com PID: $!"
        echo "Para verificar o status: python3 check_bot_status.py"
        echo "Para parar o bot: python3 start_eva_guarani.py --stop"
    else
        python3 start_eva_guarani.py "$@"
    fi
elif [ -f "bot/unified_telegram_bot_utf8.py" ]; then
    echo "Script de inicialização não encontrado. Iniciando diretamente o bot..."

    # Verificar se o usuário quer executar em background
    if [ "$1" == "--background" ]; then
        echo "Executando em background..."
        nohup python3 bot/unified_telegram_bot_utf8.py > logs/bot_output.log 2>&1 &
        echo "Bot iniciado em background com PID: $!"
    else
        python3 bot/unified_telegram_bot_utf8.py
    fi
else
    echo "Não foi possível encontrar os scripts do bot!"
    echo "Verifique se você está no diretório correto."
    exit 1
fi

echo ""
echo "Bot encerrado."
