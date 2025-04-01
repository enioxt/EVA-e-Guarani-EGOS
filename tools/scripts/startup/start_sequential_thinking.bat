---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: start_sequential_thinking.bat
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
echo ====================================================
echo    INICIANDO SEQUENTIAL THINKING MCP SERVER
echo ====================================================

:: Criar diretórios necessários
if not exist "logs" mkdir logs

:: Definir variáveis de ambiente
set DEBUG=*
set NODE_ENV=production

:: Verificar se o Node.js está instalado
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Node.js não encontrado! Por favor, instale o Node.js.
    echo Baixe em: https://nodejs.org/
    pause
    exit /b 1
)

:: Verificar se o diretório do projeto existe
if not exist "%~dp0tools\mcp-sequentialthinking-tools\dist\index.js" (
    echo [ERRO] Arquivo index.js não encontrado!
    echo Verifique se o repositório foi clonado corretamente.
    pause
    exit /b 1
)

:: Iniciar o servidor Sequential Thinking MCP
echo [INFO] Iniciando Sequential Thinking MCP em modo stdio...
echo [INFO] Data e hora: %date% %time%
echo [INFO] NÃO FECHE ESTA JANELA - O servidor precisa continuar rodando!
echo.

:: Mudar para o diretório correto antes de iniciar
cd "%~dp0tools\mcp-sequentialthinking-tools"

:: Executar o servidor
node dist/index.js

:: Verificar se o servidor foi iniciado corretamente
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao iniciar o Sequential Thinking MCP
    echo Verifique se todas as dependências estão instaladas com:
    echo npm install
    echo npm run build
    pause
    exit /b 1
)

:: Manter o console aberto (não deve chegar aqui normalmente, pois o processo node mantém o console aberto)
pause 