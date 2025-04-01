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
# - tools\utilities\schedule_checks.bat (kept)
# - tools\utilities\schedule_checks.bat.backup (moved to quarantine)
# ==================================================================

batch
@echo off
echo ============================================================
echo            EVA & GUARANI - VERIFICATION SCHEDULER
echo ============================================================
echo.
echo This script schedules periodic bot checks on Windows.
echo.

cd /d "%~dp0"

REM Check if running as administrator
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo This script needs to be run as administrator.
    echo Please right-click and select "Run as administrator".
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found! Please install Python 3.8 or higher.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if scripts exist
if not exist check_bot_status.py (
    echo Script check_bot_status.py not found!
    pause
    exit /b 1
)

if not exist notify_status.py (
    echo Script notify_status.py not found!
    pause
    exit /b 1
)

if not exist check_updates.py (
    echo Script check_updates.py not found!
    echo Update checks will not be scheduled.
    set NO_UPDATE_CHECK=1
) else (
    set NO_UPDATE_CHECK=0
)

echo Choose the check interval:
echo 1. Every hour
echo 2. Every 3 hours
echo 3. Every 6 hours
echo 4. Every 12 hours
echo 5. Once a day
echo 6. Remove existing schedules
echo.

set /p choice="Enter the number of the desired option: "

REM Remove existing tasks
schtasks /Delete /TN "EVAGuarani\CheckBotStatus" /F >nul 2>&1
schtasks /Delete /TN "EVAGuarani\NotifyStatus" /F >nul 2>&1
schtasks /Delete /TN "EVAGuarani\CheckUpdates" /F >nul 2>&1

if "%choice%"=="6" (
    echo Schedules successfully removed.
    pause
    exit /b 0
)

REM Create directory for the script
set SCRIPT_DIR=%~dp0
set CHECK_SCRIPT=%SCRIPT_DIR%check_bot_status.py
set NOTIFY_SCRIPT=%SCRIPT_DIR%notify_status.py
set UPDATE_SCRIPT=%SCRIPT_DIR%check_updates.py

REM Set interval based on choice
set INTERVAL=HOURLY
if "%choice%"=="1" set INTERVAL=HOURLY
if "%choice%"=="2" set MODIFIER=/MO 3
if "%choice%"=="3" set MODIFIER=/MO 6
if "%choice%"=="4" set MODIFIER=/MO 12
if "%choice%"=="5" set INTERVAL=DAILY

REM Create task folder
schtasks /Create /TN "EVAGuarani" /F >nul 2>&1

REM Schedule status check
echo Scheduling status check...
if "%INTERVAL%"=="HOURLY" (
    if defined MODIFIER (
        schtasks /Create /TN "EVAGuarani\CheckBotStatus" /TR "python \"%CHECK_SCRIPT%\"" /SC %INTERVAL% %MODIFIER% /F
    ) else (
        schtasks /Create /TN "EVAGuarani\CheckBotStatus" /TR "python \"%CHECK_SCRIPT%\"" /SC %INTERVAL% /F
    )
) else (
    schtasks /Create /TN "EVAGuarani\CheckBotStatus" /TR "python \"%CHECK_SCRIPT%\"" /SC %INTERVAL% /F
)

REM Schedule status notification
echo Scheduling status notification...
if "%INTERVAL%"=="HOURLY" (
    if defined MODIFIER (
        schtasks /Create /TN "EVAGuarani\NotifyStatus" /TR "python \"%NOTIFY_SCRIPT%\"" /SC %INTERVAL% %MODIFIER% /F
    ) else (
        schtasks /Create /TN "EVAGuarani\NotifyStatus" /TR "python \"%NOTIFY_SCRIPT%\"" /SC %INTERVAL% /F
    )
) else (
    schtasks /Create /TN "EVAGuarani\NotifyStatus" /TR "python \"%NOTIFY_SCRIPT%\"" /SC %INTERVAL% /F
)

REM Schedule update check
if "%NO_UPDATE_CHECK%"=="0" (
    echo Scheduling update check...
    
    REM For update checks, we use a longer interval
    if "%choice%"=="1" (
        REM Every 6 hours if the main check is every hour
        schtasks /Create /TN "EVAGuarani\CheckUpdates" /TR "python \"%UPDATE_SCRIPT%\"" /SC HOURLY /MO 6 /F
    ) else if "%choice%"=="2" (
        REM Every 12 hours if the main check is every 3 hours
        schtasks /Create /TN "EVAGuarani\CheckUpdates" /TR "python \"%UPDATE_SCRIPT%\"" /SC HOURLY /MO 12 /F
    ) else (
        REM Once a day for other cases
        schtasks /Create /TN "EVAGuarani\CheckUpdates" /TR "python \"%UPDATE_SCRIPT%\"" /SC DAILY /F
    )
)

echo.
echo Checks successfully scheduled!
echo To view the scheduled tasks, open the Windows Task Scheduler.
echo.
pause