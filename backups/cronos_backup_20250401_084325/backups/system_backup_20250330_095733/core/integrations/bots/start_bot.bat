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
echo EVA & GUARANI - Telegram Bot (avatechartbot)
echo ===================================================
echo.

:: Set project root directory
set "PROJECT_ROOT=%~dp0..\.."
cd "%PROJECT_ROOT%"

:: Set paths
set "BOT_DIR=%~dp0"
set "LOG_DIR=%BOT_DIR%logs"

:: Create necessary directories
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "data\payments" mkdir "data\payments"

:: Activate virtual environment if available
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Virtual environment not found.
    echo Attempting to install dependencies directly...
)

:: Ensure dependencies are installed
pip install --quiet python-telegram-bot==13.15
pip install --quiet requests
pip install --quiet openai

:: Set PYTHONPATH environment variable to include project directories
set "PYTHONPATH=%PROJECT_ROOT%;%PROJECT_ROOT%\modules;%PROJECT_ROOT%\modules\quantum;%PROJECT_ROOT%\tools\utilities"

:: Parse command line arguments
set MODE=standard
set RUN_HEALTH_CHECK=0

if "%1"=="--check" (
    set RUN_HEALTH_CHECK=1
) else if "%1"=="--simple" (
    set MODE=simple
) else if "%1"=="--web" (
    set MODE=web
) else if "%1"=="--help" (
    goto :show_help
)

:: Run health check if requested
if %RUN_HEALTH_CHECK% EQU 1 (
    echo Running bot health check...
    echo.
    python "%BOT_DIR%check_bot.py"
    goto :end
)

:: Run the appropriate version based on mode
if "%MODE%"=="simple" (
    echo Starting EVA & GUARANI Telegram Bot (Simple Mode)...
    echo This version is compatible with Python 3.13+ but has limited features.
    echo.
    echo Bot logs will be saved to: %LOG_DIR%\telegram_bot.log
    echo.
    echo Press Ctrl+C to stop the bot.
    echo.

    python "%BOT_DIR%simple_bot.py"
) else if "%MODE%"=="web" (
    echo Opening Telegram Web interface...
    python "%BOT_DIR%open_telegram_web.py"
) else (
    echo Running pre-start health check...
    python "%BOT_DIR%check_bot.py" --quick
    if %ERRORLEVEL% NEQ 0 (
        echo Warning: Health check reported issues. Start anyway? [Y/N]
        set /p CONFIRM=
        if /i "%CONFIRM%" NEQ "Y" goto :end
    )

    echo.
    echo Starting EVA & GUARANI Telegram Bot (Standard Mode)...
    echo.
    echo Bot logs will be saved to: %LOG_DIR%\telegram_bot.log
    echo.
    echo Press Ctrl+C to stop the bot.
    echo.

    python "%BOT_DIR%simple_telegram_bot.py"
)

goto :end

:show_help
echo.
echo EVA & GUARANI Telegram Bot - Usage
echo ===================================================
echo.
echo start_bot.bat [option]
echo.
echo Options:
echo   --check     Run health check only
echo   --simple    Run simplified version (for Python 3.13+)
echo   --web       Open Telegram Web interface
echo   --help      Show this help message
echo.
echo Examples:
echo   start_bot.bat           Run standard bot
echo   start_bot.bat --simple  Run simplified bot
echo   start_bot.bat --check   Run health check only
echo.

:end
echo.
echo Bot execution ended. Check logs for more information.
echo.
pause
