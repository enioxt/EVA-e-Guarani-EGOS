---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: integrations
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
echo ===================================================
echo EVA & GUARANI - Unified Telegram Bot
echo ===================================================
echo.

:: Check if Python is installed
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

:: Set project root directory
set "PROJECT_ROOT=%~dp0..\.."
cd "%PROJECT_ROOT%"

:: Activate virtual environment if available
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Virtual environment not found. Creating a new one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing required packages...
    pip install -r requirements.txt
    pip install python-telegram-bot==13.15
)

:: Create logs directory if it doesn't exist
if not exist "integrations\bots\logs" mkdir "integrations\bots\logs"

echo Starting EVA & GUARANI Telegram Bot...
echo.
echo Bot logs will be saved to: integrations\bots\logs\telegram_bot.log
echo.
echo Press Ctrl+C to stop the bot.
echo.

:: Run the bot in background (start /B) or in current window
python integrations\bots\eva_guarani_telegram_bot.py

:: In case the script ends unexpectedly
echo.
echo Bot execution ended. Check logs for more information.
echo.
pause 