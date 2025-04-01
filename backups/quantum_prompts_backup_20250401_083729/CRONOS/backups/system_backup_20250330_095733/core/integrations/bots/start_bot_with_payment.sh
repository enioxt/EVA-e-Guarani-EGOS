#!/bin/bash
# EVA & GUARANI - Script de Inicialização com Sistema de Pagamento
# Versão: 1.0

echo "==============================================================================="
echo "                     EVA & GUARANI - TELEGRAM BOT"
echo "                    COM SISTEMA DE PAGAMENTO v1.0"
echo "==============================================================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 não encontrado. Por favor, instale o Python 3.8 ou superior."
    echo ""
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "[INFO] Criando ambiente virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERRO] Falha ao criar ambiente virtual."
        echo ""
        exit 1
    fi
fi

# Ativar ambiente virtual
echo "[INFO] Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "[INFO] Verificando dependências..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[AVISO] Algumas dependências podem não ter sido instaladas corretamente."
fi

# Configurar sistema de pagamento
echo "[INFO] Configurando sistema de pagamento..."
python setup_payment_system.py
if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao configurar sistema de pagamento."
    echo ""
    deactivate
    exit 1
fi

# Iniciar o bot
echo ""
echo "[INFO] Iniciando o bot do Telegram com sistema de pagamento..."
echo "[INFO] Pressione Ctrl+C para encerrar."
echo ""
python unified_eva_guarani_bot.py
if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao iniciar o bot."
    echo ""
    deactivate
    exit 1
fi

# Desativar ambiente virtual
deactivate

echo ""
echo "[INFO] Bot encerrado."
echo "" 