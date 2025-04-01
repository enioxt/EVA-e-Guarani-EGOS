#!/bin/bash

# EVA & GUARANI - Assistente de Atualização para Linux/Mac

# Mudar para o diretório do script
cd "$(dirname "$0")"

# Função para exibir o cabeçalho
show_header() {
    clear
    echo "========================================================"
    echo "EVA & GUARANI - Assistente de Atualização"
    echo "========================================================"
    echo ""
}

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    show_header
    echo "[ERRO] Python 3 não encontrado. Por favor, instale o Python 3.8 ou superior."
    echo ""
    echo "Para instalar no Ubuntu/Debian:"
    echo "  sudo apt update && sudo apt install python3 python3-pip"
    echo ""
    echo "Para instalar no Fedora:"
    echo "  sudo dnf install python3 python3-pip"
    echo ""
    echo "Para instalar no macOS (com Homebrew):"
    echo "  brew install python3"
    echo ""
    exit 1
fi

# Verificar se o script de atualização existe
if [ ! -f "update_bot.py" ]; then
    show_header
    echo "[ERRO] Script de atualização não encontrado: update_bot.py"
    echo ""
    exit 1
fi

# Função para o menu principal
show_menu() {
    show_header
    echo "Escolha uma opção:"
    echo ""
    echo "[1] Verificar atualizações disponíveis"
    echo "[2] Atualizar o bot (com backup)"
    echo "[3] Atualizar o bot (sem backup)"
    echo "[4] Atualizar e reiniciar o bot"
    echo "[5] Forçar atualização (mesmo sem mudanças)"
    echo "[6] Sair"
    echo ""
    read -p "Digite o número da opção desejada: " choice
    echo ""
    
    case $choice in
        1)
            echo "Verificando atualizações disponíveis..."
            python3 update_bot.py --check-only
            echo ""
            read -p "Pressione ENTER para continuar..."
            show_menu
            ;;
        2)
            echo "Atualizando o bot (com backup)..."
            python3 update_bot.py --no-restart
            echo ""
            read -p "Pressione ENTER para continuar..."
            show_menu
            ;;
        3)
            echo "Atualizando o bot (sem backup)..."
            python3 update_bot.py --no-backup --no-restart
            echo ""
            read -p "Pressione ENTER para continuar..."
            show_menu
            ;;
        4)
            echo "Atualizando e reiniciando o bot..."
            python3 update_bot.py
            echo ""
            read -p "Pressione ENTER para continuar..."
            show_menu
            ;;
        5)
            echo "Forçando atualização..."
            python3 update_bot.py --force
            echo ""
            read -p "Pressione ENTER para continuar..."
            show_menu
            ;;
        6)
            echo "Saindo do assistente de atualização..."
            exit 0
            ;;
        *)
            echo "Opção inválida. Por favor, tente novamente."
            echo ""
            read -p "Pressione ENTER para continuar..."
            show_menu
            ;;
    esac
}

# Iniciar o menu
show_menu 