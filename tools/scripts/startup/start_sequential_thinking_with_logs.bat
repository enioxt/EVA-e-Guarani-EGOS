---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: start_sequential_thinking_with_logs.bat
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
echo    INICIANDO SEQUENTIAL THINKING MCP SERVER COM LOGS
echo ====================================================

:: Criar diretório de logs se não existir
if not exist "logs" mkdir logs

:: Definir variáveis de ambiente
set DEBUG=*
set NODE_ENV=development

:: Iniciar o servidor e redirecionar saída para arquivo de log
echo [INFO] Iniciando Sequential Thinking MCP em modo stdio...
echo [INFO] Data e hora: %date% %time%
echo [INFO] NÃO FECHE ESTA JANELA - O servidor precisa continuar rodando!
echo [INFO] Logs serão salvos em: logs\sequential_thinking.log

:: Usar cmd /c para executar o comando e capturar logs
cmd /c node "C:\Eva Guarani EGOS\tools\mcp-sequentialthinking-tools\dist\index.js" > logs\sequential_thinking.log 2>&1

:: Se houver erro, mostrar mensagem
if errorlevel 1 (
    echo [ERRO] Falha ao iniciar o servidor. Verifique os logs em logs\sequential_thinking.log
    pause
) 