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
# - integrations\bots\check_bot_health.bat (kept)
# - integrations\bots\check_bot_health.bat.backup (moved to quarantine)
# ==================================================================

batch
@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: EVA & GUARANI - Bot Health Checker (Batch Version)
:: This script checks the health status of the EVA & GUARANI bot

:: Color configuration
set "INFO=[36m"
set "SUCCESS=[32m"
set "ERROR=[31m"
set "WARNING=[33m"
set "CHECK=[35m"
set "RESET=[0m"
set "HEADER=[36m"
set "FOOTER=[36m"

:: Header
echo.
echo %HEADER%╔══════════════════════════════════════════════════════════════╗%RESET%
echo %HEADER%║                                                              ║%RESET%
echo %HEADER%║  EVA & GUARANI - Bot Health Checker                          ║%RESET%
echo %HEADER%║  Version 1.0 (Batch)                                         ║%RESET%
echo %HEADER%║                                                              ║%RESET%
echo %HEADER%╚══════════════════════════════════════════════════════════════╝%RESET%
echo.

:: Function to display log messages
call :log_message "Starting health check for EVA & GUARANI bot..." "INFO"

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

:: Initialize check counters
set total_checks=0
set passed_checks=0

:: Check essential files
call :log_message "Checking essential files..." "CHECK"

call :check_file_exists "bot\unified_telegram_bot_utf8.py" "Main bot file"
call :check_file_exists "quantum\quantum_master.py" "Main quantum module"
call :check_file_exists "requirements.txt" "Requirements file"

:: Check configuration files
call :log_message "Checking configuration files..." "CHECK"

call :check_file_exists "config\telegram_config.json" "Telegram Configuration"
call :check_file_exists "config\openai_config.json" "OpenAI Configuration"
call :check_file_exists "config\bot_config.json" "Bot Configuration"

:: Check if Telegram token is configured
call :check_token_configured "config\telegram_config.json" "bot_token" "Telegram Token"

:: Check if OpenAI key is configured
call :check_token_configured "config\openai_config.json" "api_key" "OpenAI Key"

:: Check processes
call :log_message "Checking processes..." "CHECK"

call :check_process_running "python.exe" "Python"

:: Check logs
call :log_message "Checking logs..." "CHECK"

call :check_recent_logs "logs\bot.log" 30

:: Check Python version
call :log_message "Checking Python version..." "CHECK"

call :check_python_version "3.8.0"

:: Check disk space
call :log_message "Checking disk space..." "CHECK"

call :check_disk_space 1

:: Check API connectivity
call :log_message "Checking API connectivity..." "CHECK"

call :check_api_connectivity "Telegram" "https://api.telegram.org"
call :check_api_connectivity "OpenAI" "https://api.openai.com"

:: Calculate overall health
call :calculate_health

:: Generate report
call :generate_report

:: Footer
echo.
echo %FOOTER%╔══════════════════════════════════════════════════════════════╗%RESET%
echo %FOOTER%║                                                              ║%RESET%
echo %FOOTER%║  Health check completed                                      ║%RESET%
echo %FOOTER%║  Overall health: %health_percentage%%%                                       ║%RESET%
echo %FOOTER%║                                                              ║%RESET%
echo %FOOTER%╚══════════════════════════════════════════════════════════════╝%RESET%
echo.

echo [35m✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧%RESET%
echo.

:: Ask if the user wants to open the report
set /p open_report=Do you want to open the detailed report? (Y/N):
if /i "%open_report%"=="Y" (
    start notepad.exe "%report_path%"
)

goto :eof

:: ===== FUNCTIONS =====

:log_message
:: %~1 = message, %~2 = type
set "timestamp=%date% %time%"
set "type=%~2"
if "%type%"=="" set "type=INFO"
set "color=!%type%!"

echo [%timestamp%] %color%[%type%]%RESET% %~1
goto :eof

:check_file_exists
:: %~1 = path, %~2 = description
set /a total_checks+=1
if exist "%~1" (
    call :log_message "✓ %~2 found: %~1" "SUCCESS"
    set /a passed_checks+=1
    set "file_exists_%~1=1"
) else (
    call :log_message "✗ %~2 not found: %~1" "ERROR"
    set "file_exists_%~1=0"
    set "corrective_actions=!corrective_actions!- Check if the file %~1 exists and is in the correct location.!LF!"
)
goto :eof

:check_token_configured
:: %~1 = config file, %~2 = token name, %~3 = description
set /a total_checks+=1
if exist "%~1" (
    findstr /C:"%~2" "%~1" > nul
    if !errorlevel! equ 0 (
        findstr /C:"%~2.*\"\"" "%~1" > nul
        if !errorlevel! equ 0 (
            call :log_message "✗ %~3 is empty in %~1" "WARNING"
            set "token_configured_%~2=0"
            set "corrective_actions=!corrective_actions!- Configure the %~3 in %~1.!LF!"
        ) else (
            call :log_message "✓ %~3 is configured in %~1" "SUCCESS"
            set /a passed_checks+=1
            set "token_configured_%~2=1"
        )
    ) else (
        call :log_message "✗ %~3 not found in %~1" "ERROR"
        set "token_configured_%~2=0"
        set "corrective_actions=!corrective_actions!- Add the %~3 in %~1.!LF!"
    )
) else (
    call :log_message "✗ Config file %~1 not found" "ERROR"
    set "token_configured_%~2=0"
    set "corrective_actions=!corrective_actions!- Create the config file %~1.!LF!"
)
goto :eof

:check_process_running
:: %~1 = process name, %~2 = description
set /a total_checks+=1
tasklist /FI "IMAGENAME eq %~1" 2>NUL | find /I "%~1" >NUL
if !errorlevel! equ 0 (
    call :log_message "✓ Process %~2 is running" "SUCCESS"
    set /a passed_checks+=1
    set "process_running_%~1=1"
) else (
    call :log_message "✗ Process %~2 is not running" "WARNING"
    set "process_running_%~1=0"
    set "corrective_actions=!corrective_actions!- Start the bot using the command: .\setup_and_start.ps1!LF!"
)
goto :eof

:check_recent_logs
:: %~1 = log path, %~2 = time limit in minutes
set /a total_checks+=1
if exist "%~1" (
    for %%A in ("%~1") do set log_date=%%~tA

    :: Show the last 5 lines of the log
    call :log_message "Latest log entries:" "INFO"
    type "%~1" | findstr /N "^" | findstr /R "^[0-9]*[0-9][0-9][0-9][0-9]:" | findstr /R "^[0-9]*[0-9][0-9][0-9][0-9]:" > nul
    if !errorlevel! equ 0 (
        for /f "skip=1 tokens=1* delims=:" %%a in ('type "%~1" ^| findstr /N "^" ^| findstr /R "^[0-9]*[0-9][0-9][0-9][0-9]:"') do (
            echo    %%b
        )
    ) else (
        type "%~1" | findstr /N "^" | findstr /R "^[0-9]*[0-9][0-9][0-9]:" > nul
        if !errorlevel! equ 0 (
            for /f "skip=1 tokens=1* delims=:" %%a in ('type "%~1" ^| findstr /N "^" ^| findstr /R "^[0-9]*[0-9][0-9][0-9]:"') do (
                echo    %%b
            )
        ) else (
            for /f "skip=1 tokens=1* delims=:" %%a in ('type "%~1" ^| findstr /N "^"') do (
                echo    %%b
            )
        )
    )

    call :log_message "✓ Log file found: %~1" "SUCCESS"
    set /a passed_checks+=1
    set "recent_logs_%~1=1"
) else (
    call :log_message "✗ Log file not found: %~1" "ERROR"
    set "recent_logs_%~1=0"
    set "corrective_actions=!corrective_actions!- Ensure the bot has been started at least once to generate logs.!LF!"
)
goto :eof

:check_python_version
:: %~1 = minimum version
set /a total_checks+=1
python --version 2>&1 | findstr /R /C:"Python [0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*" > nul
if !errorlevel! equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
    call :log_message "Python version: %python_version%" "INFO"

    :: Simple version comparison (not perfect, but works for most cases)
    set min_version=%~1
    set current_version=%python_version%

    if "%current_version%" geq "%min_version%" (
        call :log_message "✓ Suitable Python version: %python_version%" "SUCCESS"
        set /a passed_checks+=1
        set "python_version_ok=1"
    ) else (
        call :log_message "✗ Unsuitable Python version: %python_version% (minimum recommended: %min_version%)" "WARNING"
        set "python_version_ok=0"
        set "corrective_actions=!corrective_actions!- Upgrade Python to version %min_version% or higher.!LF!"
    )
) else (
    call :log_message "✗ Python not found or error checking version" "ERROR"
    set "python_version_ok=0"
    set "corrective_actions=!corrective_actions!- Install Python 3.8.0 or higher.!LF!"
)
goto :eof

:check_disk_space
:: %~1 = minimum space in GB
set /a total_checks+=1
for /f "tokens=3" %%a in ('dir /-c 2^>nul ^| findstr /C:"bytes free"') do set free_bytes=%%a
set /a free_gb=%free_bytes:,=%/1073741824

if %free_gb% geq %~1 (
    call :log_message "✓ Sufficient disk space: %free_gb% GB free" "SUCCESS"
    set /a passed_checks+=1
    set "disk_space_ok=1"
) else (
    call :log_message "✗ Insufficient disk space: %free_gb% GB free (minimum recommended: %~1 GB)" "WARNING"
    set "disk_space_ok=0"
    set "corrective_actions=!corrective_actions!- Free up disk space to ensure proper bot operation.!LF!"
)
goto :eof

:check_api_connectivity
:: %~1 = API name, %~2 = URL
set /a total_checks+=1
ping -n 1 %~2 2>NUL | find "TTL=" >NUL
if !errorlevel! equ 0 (
    call :log_message "✓ Connectivity with API %~1 OK" "SUCCESS"
    set /a passed_checks+=1
    set "api_connectivity_%~1=1"
) else (
    call :log_message "✗ Failed connectivity with API %~1" "WARNING"
    set "api_connectivity_%~1=0"
    set "corrective_actions=!corrective_actions!- Check your internet connection and if the API %~1 is available.!LF!"
)
goto :eof

:calculate_health
:: Calculate health percentage
set /a health_percentage=(%passed_checks% * 100) / %total_checks%

call :log_message "EVA & GUARANI Bot Health Report" "INFO"
call :log_message "Total checks: %total_checks%" "INFO"
call :log_message "Successful checks: %passed_checks%" "INFO"
call :log_message "Overall health: %health_percentage%%%" "INFO"

if %health_percentage% geq 90 (
    call :log_message "✓ Health status: EXCELLENT" "SUCCESS"
    set "health_status=EXCELLENT"
) else if %health_percentage% geq 75 (
    call :log_message "✓ Health status: GOOD" "SUCCESS"
    set "health_status=GOOD"
) else if %health_percentage% geq 50 (
    call :log_message "⚠ Health status: FAIR" "WARNING"
    set "health_status=FAIR"
) else (
    call :log_message "✗ Health status: CRITICAL" "ERROR"
    set "health_status=CRITICAL"
)
goto :eof

:generate_report
:: Generate health report
set "timestamp=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "timestamp=%timestamp: =0%"
set "report_path=logs\health_check_%timestamp%.log"

echo EVA & GUARANI - Bot Health Report > "%report_path%"
echo Date: %date% %time% >> "%report_path%"
echo. >> "%report_path%"
echo Overall Health: %health_percentage%%% >> "%report_path%"
echo Health Status: %health_status% >> "%report_path%"
echo Total Checks: %total_checks% >> "%report_path%"
echo Successful Checks: %passed_checks% >> "%report_path%"
echo. >> "%report_path%"
echo Check Details: >> "%report_path%"

:: Essential files
echo - Main bot file: %file_exists_bot\unified_telegram_bot_utf8.py% >> "%report_path%"
echo - Main quantum module: %file_exists_quantum\quantum_master.py% >> "%report_path%"
echo - Requirements file: %file_exists_requirements.txt% >> "%report_path%"

:: Configurations
echo - Telegram Configuration: %file_exists_config\telegram_config.json% >> "%report_path%"
echo - OpenAI Configuration: %file_exists_config\openai_config.json% >> "%report_path%"
echo - Bot Configuration: %file_exists_config\bot_config.json% >> "%report_path%"

:: Tokens
echo - Telegram Token configured: %token_configured_bot_token% >> "%report_path%"
echo - OpenAI Key configured: %token_configured_api_key% >> "%report_path%"

:: Processes
echo - Python process running: %process_running_python.exe% >> "%report_path%"

:: Logs
echo - Recent logs: %recent_logs_logs\bot.log% >> "%report_path%"

:: Python
echo - Suitable Python version: %python_version_ok% >> "%report_path%"

:: Disk
echo - Sufficient disk space: %disk_space_ok% >> "%report_path%"

:: APIs
echo - Connectivity with Telegram API: %api_connectivity_Telegram% >> "%report_path%"
echo - Connectivity with OpenAI API: %api_connectivity_OpenAI% >> "%report_path%"

:: Corrective actions
echo. >> "%report_path%"
if defined corrective_actions (
    echo Recommended Corrective Actions: >> "%report_path%"
    echo !corrective_actions! >> "%report_path%"

    call :log_message "Recommended corrective actions:" "INFO"
    for /f "tokens=*" %%a in ("!corrective_actions!") do (
        echo %WARNING%  • %%a%RESET%
    )
) else (
    echo No corrective actions necessary >> "%report_path%"
    call :log_message "✓ No corrective actions necessary" "SUCCESS"
)

echo. >> "%report_path%"
echo ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧ >> "%report_path%"

call :log_message "Health report saved at: %report_path%" "INFO"
goto :eof
