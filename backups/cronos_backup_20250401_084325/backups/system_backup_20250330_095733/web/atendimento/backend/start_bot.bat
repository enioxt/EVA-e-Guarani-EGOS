---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: eva-atendimento
  changelog: []
  dependencies:
  - QUANTUM_PROMPTS
  - BIOS-Q
  description: Component of the EVA & GUARANI Quantum Unified System
  documentation_quality: 0.95
  encoding: utf-8
  ethical_validation: true
  last_updated: '2025-03-29'
  related_files: []
  required: true
  review_status: approved
  security_level: 0.95
  simulation_capable: false
  status: active
  subsystem: MASTER
  test_coverage: 0.9
  translation_status: completed
  type: script
  version: '8.0'
  windows_compatibility: true
---
REM
REM METADATA:
REM   type: module
REM   category: module
REM   subsystem: MASTER
REM   status: active
REM   required: false
REM   simulation_capable: true
REM   dependencies: []
REM   description: Component of the  subsystem
REM   author: EVA & GUARANI
REM   version: 1.0.0
REM   last_updated: '2025-03-29'
REM   principles: []
REM   security_level: standard
REM   test_coverage: 0.0
REM   documentation_quality: 0.0
REM   ethical_validation: true
REM   windows_compatibility: true
REM   encoding: utf-8
REM   backup_required: false
REM   translation_status: pending
REM   api_endpoints: []
REM   related_files: []
REM   changelog: ''
REM   review_status: pending
REM REM

REM
REM METADATA:
REM   type: module
REM   category: module
REM   subsystem: MASTER
REM   status: active
REM   required: false
REM   simulation_capable: true
REM   dependencies: []
REM   description: Component of the  subsystem
REM   author: EVA & GUARANI
REM   version: 1.0.0
REM   last_updated: '2025-03-29'
REM REM

@echo off
echo Iniciando EVA & GUARANI Telegram Bot...

:: Diretório do script
set SCRIPT_DIR=%~dp0

:: Mudar para o diretório do backend
cd /d "%SCRIPT_DIR%"

:: Verificar se Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Erro: Python não encontrado. Por favor, instale Python 3.8 ou superior.
    pause
    exit /b 1
)

:: Verificar dependências
echo Verificando dependências...
pip install -r requirements.txt

:: Iniciar o bot
echo Iniciando o bot...
start /min cmd /c "python start_telegram_bot.py > telegram_bot.log 2>&1"

echo Bot iniciado em segundo plano!
echo Os logs estão sendo salvos em: telegram_bot.log
echo.
echo Para encerrar o bot, feche a janela do prompt de comando ou use o Gerenciador de Tarefas.
echo.

exit /b 0
