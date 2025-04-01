#!/bin/bash

# EVA & GUARANI - Agendador de Verificações
# Este script agenda verificações periódicas do bot no Linux usando cron

echo "============================================================"
echo "            EVA & GUARANI - AGENDADOR DE VERIFICAÇÕES"
echo "============================================================"
echo ""
echo "Este script agenda verificações periódicas do bot no Linux usando cron."
echo ""

# Mudar para o diretório do script
cd "$(dirname "$0")"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado! Por favor, instale o Python 3.8 ou superior."
    echo "No Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "No Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

# Verificar se os scripts existem
if [ ! -f "check_bot_status.py" ]; then
    echo "Script check_bot_status.py não encontrado!"
    exit 1
fi

if [ ! -f "notify_status.py" ]; then
    echo "Script notify_status.py não encontrado!"
    exit 1
fi

# Verificar se o script de atualizações existe
if [ ! -f "check_updates.py" ]; then
    echo "Script check_updates.py não encontrado!"
    echo "As verificações de atualizações não serão agendadas."
    NO_UPDATE_CHECK=1
else
    NO_UPDATE_CHECK=0
fi

# Obter caminho absoluto dos scripts
SCRIPT_DIR="$(pwd)"
CHECK_SCRIPT="${SCRIPT_DIR}/check_bot_status.py"
NOTIFY_SCRIPT="${SCRIPT_DIR}/notify_status.py"
UPDATE_SCRIPT="${SCRIPT_DIR}/check_updates.py"

# Verificar se o usuário tem permissão para editar o crontab
if ! crontab -l &> /dev/null && [ "$?" -ne 0 ] && [ "$?" -ne 1 ]; then
    echo "Você não tem permissão para editar o crontab."
    echo "Execute este script com privilégios adequados."
    exit 1
fi

# Menu de opções
echo "Escolha o intervalo de verificação:"
echo "1. A cada hora"
echo "2. A cada 3 horas"
echo "3. A cada 6 horas"
echo "4. A cada 12 horas"
echo "5. Uma vez por dia"
echo "6. Remover agendamentos existentes"
echo ""

read -p "Digite o número da opção desejada: " choice

# Remover tarefas existentes
CURRENT_CRONTAB=$(crontab -l 2>/dev/null | grep -v "check_bot_status.py\|notify_status.py\|check_updates.py")

if [ "$choice" == "6" ]; then
    echo "$CURRENT_CRONTAB" | crontab -
    echo "Agendamentos removidos com sucesso."
    exit 0
fi

# Definir expressão cron com base na escolha
case $choice in
    1)
        # A cada hora
        CHECK_SCHEDULE="0 * * * *"
        NOTIFY_SCHEDULE="30 * * * *"
        UPDATE_SCHEDULE="0 */6 * * *"  # A cada 6 horas
        ;;
    2)
        # A cada 3 horas
        CHECK_SCHEDULE="0 */3 * * *"
        NOTIFY_SCHEDULE="30 */3 * * *"
        UPDATE_SCHEDULE="0 */12 * * *"  # A cada 12 horas
        ;;
    3)
        # A cada 6 horas
        CHECK_SCHEDULE="0 */6 * * *"
        NOTIFY_SCHEDULE="30 */6 * * *"
        UPDATE_SCHEDULE="0 8 * * *"  # Uma vez por dia às 8h
        ;;
    4)
        # A cada 12 horas
        CHECK_SCHEDULE="0 */12 * * *"
        NOTIFY_SCHEDULE="30 */12 * * *"
        UPDATE_SCHEDULE="0 8 * * *"  # Uma vez por dia às 8h
        ;;
    5)
        # Uma vez por dia
        CHECK_SCHEDULE="0 8 * * *"
        NOTIFY_SCHEDULE="0 20 * * *"
        UPDATE_SCHEDULE="0 12 * * *"  # Uma vez por dia às 12h
        ;;
    *)
        echo "Opção inválida!"
        exit 1
        ;;
esac

# Adicionar novas tarefas ao crontab
NEW_CRONTAB="${CURRENT_CRONTAB}"
NEW_CRONTAB="${NEW_CRONTAB}
# EVA & GUARANI - Verificações automáticas
${CHECK_SCHEDULE} cd ${SCRIPT_DIR} && python3 ${CHECK_SCRIPT} > ${SCRIPT_DIR}/logs/cron_check.log 2>&1
${NOTIFY_SCHEDULE} cd ${SCRIPT_DIR} && python3 ${NOTIFY_SCRIPT} > ${SCRIPT_DIR}/logs/cron_notify.log 2>&1
"

# Adicionar verificação de atualizações se o script existir
if [ $NO_UPDATE_CHECK -eq 0 ]; then
    NEW_CRONTAB="${NEW_CRONTAB}
# EVA & GUARANI - Verificação de atualizações
${UPDATE_SCHEDULE} cd ${SCRIPT_DIR} && python3 ${UPDATE_SCRIPT} > ${SCRIPT_DIR}/logs/cron_updates.log 2>&1
"
fi

# Atualizar crontab
echo "$NEW_CRONTAB" | crontab -

echo ""
echo "Verificações agendadas com sucesso!"
if [ $NO_UPDATE_CHECK -eq 0 ]; then
    echo "Verificações de status, notificações e atualizações foram agendadas."
else
    echo "Verificações de status e notificações foram agendadas."
    echo "Verificações de atualizações não foram agendadas (script não encontrado)."
fi
echo "Para visualizar as tarefas agendadas, execute: crontab -l"
echo "" 