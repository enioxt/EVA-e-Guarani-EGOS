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


# ==================================================================
# COMBINED FILE FROM MULTIPLE SIMILAR FILES
# Date: 2025-03-22 08:37:43
# Combined files:
# - integrations\bots\start_telegram_eliza_bridge.bat (kept)
# - integrations\bots\start_telegram_eliza_bridge.bat.backup (moved to quarantine)
# ==================================================================

batch
@echo off
echo ===================================================
echo "EVA & GUARANI - Bridge Telegram-ElizaOS"
echo ===================================================
echo.

echo Checking requirements...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found. Please install Python 3.6 or higher.
    goto :end
)

echo Creating directories...
if not exist "config" mkdir config
if not exist "logs" mkdir logs
if not exist "bot" mkdir bot

echo Checking configuration...
if not exist "config\telegram_config.json" (
    echo [WARNING] Configuration file not found: config\telegram_config.json
    echo Creating default configuration file...
    echo {"token":"YOUR_TELEGRAM_BOT_TOKEN_HERE","allowed_users":[123456789],"admin_users":[123456789],"enable_eliza":true} > config\telegram_config.json
    echo [WARNING] Edit the file config\telegram_config.json and add your bot token.
)

if not exist "config\eliza_config.json" (
    echo [WARNING] ElizaOS configuration file not found: config\eliza_config.json
    echo Creating default configuration file...
    echo {"eliza_dir":"eliza","api_key":"","openai_api_key":"","port":3000,"mode":"development","enable_bridge":true} > config\eliza_config.json
)

echo Checking dependencies...
pip show python-telegram-bot >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Python Telegram Bot...
    pip install python-telegram-bot==13.15
)

echo Checking project files...
if not exist "bot\eliza_integration.py" (
    echo [ERROR] Integration module not found: bot\eliza_integration.py
    echo Ensure the module was created correctly.
    goto :end
)

if not exist "start_telegram_eliza_bridge.py" (
    echo [ERROR] Main script not found: start_telegram_eliza_bridge.py
    goto :end
)

echo.
echo Starting the Telegram-ElizaOS Bridge...
echo.
echo "EVA & GUARANI Bridge started"
echo.

:: Alternative method to start the Python process in the background
cmd /c start /min "" python "%~dp0start_telegram_eliza_bridge.py"

echo.
echo The Bridge is running in the background.
echo Check the logs in logs\telegram_eliza_bridge.log for details.
echo.

:end
pause
