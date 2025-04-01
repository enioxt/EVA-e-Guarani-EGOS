---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: configure_firewall.bat
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
REM   type: configuration
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
REM   type: configuration
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
echo    CONFIGURANDO FIREWALL PARA CURSOR E NODE.JS
echo ====================================================

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

:: Adicionar regra para o Cursor
echo [INFO] Adicionando regra para o Cursor...
netsh advfirewall firewall add rule name="Cursor IDE" dir=in action=allow program="C:\Users\Enidi\AppData\Local\Programs\cursor\Cursor.exe" enable=yes profile=any

:: Adicionar regra para Node.js
echo [INFO] Adicionando regra para Node.js...
for /f "tokens=*" %%i in ('where node') do (
    netsh advfirewall firewall add rule name="Node.js" dir=in action=allow program="%%i" enable=yes profile=any
)

:: Adicionar regra para a porta do MCP
echo [INFO] Adicionando regra para porta 38002...
netsh advfirewall firewall add rule name="MCP Sequential Thinking" dir=in action=allow protocol=TCP localport=38002 enable=yes profile=any

echo [INFO] Configuração do firewall concluída
echo [INFO] Por favor, reinicie o Cursor e o servidor MCP
pause 