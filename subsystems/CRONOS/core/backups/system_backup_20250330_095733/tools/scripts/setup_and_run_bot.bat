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
# - tools\scripts\setup_and_run_bot.bat (kept)
# - tools\scripts\setup_and_run_bot.bat.backup (moved to quarantine)
# ==================================================================

batch
@echo off
echo ============================================================
echo            EVA ^& GUARANI - UNIFIED TELEGRAM BOT
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    echo.
    pause
    exit /b 1
)

REM Create necessary directories
if not exist logs mkdir logs
if not exist config mkdir config
if not exist data mkdir data
if not exist generated_images mkdir generated_images
if not exist generated_videos mkdir generated_videos

REM Install necessary dependencies for the bot
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install python-telegram-bot openai pillow numpy tiktoken tenacity python-dateutil colorama

REM Start the bot
echo Bot starting... Press Ctrl+C to terminate.
echo.
python EGOS\scripts\unified_telegram_bot_utf8.py

echo.
echo The bot has been terminated.
choice /c YN /m "Do you want to restart the bot? (Y/N)"
if %errorlevel% equ 1 (
    echo Restarting...
    echo.
    goto :start_bot
) else (
    echo.
    echo Bot terminated. Press any key to exit.
    pause >nul
)

:start_bot
cls
echo Restarting the bot...
echo.
python EGOS\scripts\unified_telegram_bot_utf8.py
goto :eof