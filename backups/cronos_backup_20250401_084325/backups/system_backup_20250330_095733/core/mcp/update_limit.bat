---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: core
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
REM   type: core
REM   category: core
REM   subsystem: MASTER
REM   status: active
REM   required: true
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
REM   type: core
REM   category: core
REM   subsystem: MASTER
REM   status: active
REM   required: true
REM   simulation_capable: true
REM   dependencies: []
REM   description: Component of the  subsystem
REM   author: EVA & GUARANI
REM   version: 1.0.0
REM   last_updated: '2025-03-29'
REM REM

@echo off
ECHO ===================================
ECHO EVA ^& GUARANI - ATUALIZAR LIMITE
ECHO ===================================
ECHO.
ECHO Este script deve ser executado quando o Cursor
ECHO solicitar iniciar um novo chat.
ECHO.
ECHO O limite atual será registrado como o limite real
ECHO do Cursor para futuras sessões.
ECHO.

cd %~dp0
python cursor_commands.py update_limit %*

ECHO.
ECHO Para usar o novo limite, é necessário reiniciar o monitor:
ECHO 1. Feche o Cursor se necessário
ECHO 2. Execute start_monitor.bat para iniciar novamente
ECHO.
ECHO Pressione qualquer tecla para continuar...
pause > nul
