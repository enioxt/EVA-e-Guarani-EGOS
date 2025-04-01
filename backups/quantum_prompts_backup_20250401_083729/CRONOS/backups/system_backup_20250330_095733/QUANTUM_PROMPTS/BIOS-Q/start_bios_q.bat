---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: BIOS-Q
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
  subsystem: BIOS-Q
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
chcp 65001 > nul
echo ===============================================
echo    EVA ^& GUARANI - BIOS-Q MCP Initialization
echo ===============================================

:: Verificar se Python está instalado
python --version > nul 2>&1
if errorlevel 1 (
    echo Python não encontrado! Por favor, instale Python 3.9 ou superior.
    exit /b 1
)

:: Verificar se o ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo Criando ambiente virtual...
    python -m venv venv
)

:: Ativar ambiente virtual
call venv\Scripts\activate.bat

:: Verificar se as dependências principais estão instaladas
python -c "import aiohttp" 2>nul
if errorlevel 1 (
    echo Instalando dependências...
    pip install -e .[dev]
) else (
    python -c "import sys; sys.path.append('.'); import mycelium_network" 2>nul
    if errorlevel 1 (
        echo Atualizando dependências locais...
        pip install -e .[dev]
    )
)

:: Configurar variáveis de ambiente
set "PYTHONPATH=%CD%;%CD%\..\QUANTUM_PROMPTS"
set "BIOS_Q_CONFIG=%CD%\config\bios_q_config.json"
set "QUANTUM_LOG_LEVEL=DEBUG"
set "QUANTUM_STATE_DIR=%CD%\..\QUANTUM_PROMPTS"

:: Verificar se requirements.txt foi instalado
if not exist "venv\Lib\site-packages\aiohttp" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

:: Criar diretório de logs se não existir
if not exist "..\logs" mkdir "..\logs"

:: Iniciar BIOS-Q MCP
echo Starting BIOS-Q MCP...
python -m mcp.bios_q_mcp

echo ===============================================
echo              EVA ^& GUARANI
echo =============================================== 