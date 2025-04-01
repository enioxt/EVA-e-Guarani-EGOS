---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: tools
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
REM   type: utility
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
REM   type: utility
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
ECHO ===================================
ECHO EVA ^& GUARANI - MONITOR DE CONTEXTO
ECHO ===================================
ECHO.
cd %~dp0
ECHO Verificando e interrompendo quaisquer monitores existentes...
python stop_monitor.py
timeout /t 2 /nobreak >nul

ECHO.
ECHO Iniciando monitor de contexto adaptativo...
ECHO.

REM Inicia o monitor em segundo plano
start /b pythonw context_monitor.py

ECHO.
ECHO Verificando status...
timeout /t 2 /nobreak >nul
python cursor_commands.py mcp_status

ECHO.
ECHO O monitor adaptativo esta rodando em segundo plano
ECHO e salvara automaticamente quando atingir 80%% da capacidade
ECHO ou a cada 30 minutos para evitar perda de dados.
ECHO.
ECHO Para adicionar ao startup do Windows, crie um atalho para este
ECHO arquivo na pasta "Inicializar" do menu Iniciar.
ECHO.
ECHO Para verificar o status, use o comando: @status
ECHO.
ECHO Pressione qualquer tecla para sair.
pause > nul 