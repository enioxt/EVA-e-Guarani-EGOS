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
echo EVA & GUARANI - Simple Telegram Bot
echo ===================================================
echo.

:: Set project root directory
set "PROJECT_ROOT=%~dp0..\.."
cd "%PROJECT_ROOT%"

:: Activate virtual environment if available
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Virtual environment not found.
)

echo Starting EVA & GUARANI Simple Telegram Bot...
echo.
echo Bot logs will be saved to: integrations\bots\logs\telegram_bot.log
echo.
echo Press Ctrl+C to stop the bot.
echo.

:: Run the bot
python integrations\bots\simple_telegram_bot.py

echo.
echo Bot execution ended. Check logs for more information.
echo.
pause
