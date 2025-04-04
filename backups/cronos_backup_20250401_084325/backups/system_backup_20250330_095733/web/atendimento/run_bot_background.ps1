# Script para executar o bot do Telegram em segundo plano
# Autor: EVA & GUARANI
# Data: 2025-03-24

# Configurar o diretório de trabalho
cd "$PSScriptRoot\backend"

# Verificar se o ambiente virtual está ativado
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Ativando ambiente virtual..."
    # Se usar venv no Windows
    # & .\venv\Scripts\Activate.ps1
}

# Iniciar o bot em segundo plano
Start-Process -FilePath "python" -ArgumentList "start_telegram_bot.py" -WindowStyle Minimized -WorkingDirectory "$PSScriptRoot\backend"

Write-Host "Bot do Telegram iniciado em segundo plano."
