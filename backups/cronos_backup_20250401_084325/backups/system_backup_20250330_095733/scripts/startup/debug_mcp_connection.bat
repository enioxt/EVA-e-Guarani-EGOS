---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: debug_mcp_connection.bat
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
echo    DIAGNÓSTICO DO MCP SEQUENTIAL THINKING
echo ====================================================

:: Criar diretório de logs se não existir
if not exist "logs" mkdir logs

:: Verificar se está rodando como administrador
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Script está rodando como administrador
) else (
    echo [ERRO] Este script precisa ser executado como administrador
    echo [INFO] Por favor, clique com botão direito e selecione "Executar como administrador"
    pause
    exit /b 1
)

:: Verificar se Node.js está instalado
where node >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Node.js está instalado
    node --version
) else (
    echo [ERRO] Node.js não está instalado ou não está no PATH
    pause
    exit /b 1
)

:: Verificar portas em uso
echo [INFO] Verificando portas em uso...
netstat -ano | findstr "38002" > logs\port_check.log
type logs\port_check.log

:: Verificar processos Node.js
echo [INFO] Verificando processos Node.js...
tasklist | findstr "node.exe" > logs\process_check.log
type logs\process_check.log

:: Verificar permissões do diretório
echo [INFO] Verificando permissões do diretório...
icacls "C:\Eva Guarani EGOS\tools\mcp-sequentialthinking-tools" > logs\permissions.log
type logs\permissions.log

:: Verificar firewall
echo [INFO] Verificando regras do firewall...
netsh advfirewall firewall show rule name=all | findstr "38002" > logs\firewall.log
type logs\firewall.log

:: Iniciar o servidor com logs detalhados
echo [INFO] Iniciando Sequential Thinking MCP com logs detalhados...
echo [INFO] Data e hora: %date% %time%

:: Definir variáveis de ambiente
set DEBUG=*
set NODE_ENV=development
set NODE_DEBUG=net,stream,module,http

:: Iniciar o servidor com redirecionamento de logs
cmd /c node "C:\Eva Guarani EGOS\tools\mcp-sequentialthinking-tools\dist\index.js" > logs\sequential_thinking_detailed.log 2>&1

:: Se houver erro, mostrar mensagem
if errorlevel 1 (
    echo [ERRO] Falha ao iniciar o servidor. Verifique os logs em logs\sequential_thinking_detailed.log
    pause
) 