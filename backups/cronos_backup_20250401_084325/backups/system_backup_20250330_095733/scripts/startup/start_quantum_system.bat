---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: start_quantum_system.bat
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
REM ===================================
REM EVA & GUARANI - Quantum System v8.0
REM ===================================
REM
REM METADATA:
REM type: system_entry_point
REM category: core
REM subsystem: BIOS-Q
REM status: active
REM required: true
REM dependencies:
REM   - Python 3.8+
REM   - pip
REM   - venv
REM   - quantum_init.py
REM description: Entry point script for EVA & GUARANI system initialization
REM author: EVA & GUARANI
REM version: 8.0
REM last_updated: 2025-03-26
REM
REM ===================================

echo ===================================
echo EVA ^& GUARANI - Quantum System v8.0
echo ===================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Python nao encontrado. Instalando Python...
    REM Aqui você pode adicionar código para baixar e instalar Python
    echo Por favor, instale Python 3.8 ou superior e tente novamente
    pause
    exit /b 1
)

REM Verifica se pip está instalado
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Instalando pip...
    python -m ensurepip --default-pip
)

REM Verifica ambiente virtual
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativa ambiente virtual
call venv\Scripts\activate.bat

REM Instala/atualiza dependências
echo Verificando dependencias...
python -m pip install -r requirements.txt

REM Configura variáveis de ambiente
set QUANTUM_HOME=%cd%
set PYTHONPATH=%PYTHONPATH%;%cd%

echo.
echo Iniciando sistema quantum...
echo.

REM Executa o inicializador quantum
python quantum_init.py

REM Verifica o resultado
if errorlevel 1 (
    echo.
    echo AVISO: Alguns componentes podem estar em modo simulacao
    echo Verifique quantum_init_status.txt para mais detalhes
) else (
    echo.
    echo Sistema iniciado com sucesso!
)

echo.
echo Para mais informacoes, consulte:
echo - quantum_init.log (log detalhado)
echo - quantum_init_status.txt (status dos componentes)
echo.

REM Mantém a janela aberta
pause
