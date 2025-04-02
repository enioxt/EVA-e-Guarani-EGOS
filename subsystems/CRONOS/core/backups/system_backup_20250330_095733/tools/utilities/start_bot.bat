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


# ==================================================================
# COMBINED FILE FROM MULTIPLE SIMILAR FILES
# Date: 2025-03-22 08:37:43
# Combined files:
# - tools\utilities\start_bot.bat (kept)
# - tools\utilities\start_bot.bat.backup (moved to quarantine)
# ==================================================================

batch
@echo off
echo Starting EVA & GUARANI Bot...
echo Setting up environment...

:: Configure PYTHONPATH to include the current directory
set PYTHONPATH=%PYTHONPATH%;%CD%

:: Check if Python is installed
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found. Please ensure Python is installed and in the PATH.
    pause
    exit /b 1
)

:: Check if the python-telegram-bot module is installed
python -c "import telegram" > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing python-telegram-bot...
    pip install python-telegram-bot
)

:: Check if the openai module is installed
python -c "import openai" > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing openai...
    pip install openai
)

:: Start the bot
echo Starting the bot...
python bot/unified_telegram_bot_utf8.py

pause