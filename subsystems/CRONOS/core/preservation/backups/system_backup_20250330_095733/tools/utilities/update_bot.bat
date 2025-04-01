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
# - tools\utilities\update_bot.bat (kept)
# - tools\utilities\update_bot.bat.backup (moved to quarantine)
# ==================================================================

batch
@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: EVA & GUARANI - Update Script (Batch Version)
:: This script updates the EVA & GUARANI bot to the latest version

:: Color configuration
set "INFO=[36m"
set "SUCCESS=[32m"
set "ERROR=[31m"
set "WARNING=[33m"
set "UPDATE=[35m"
set "RESET=[0m"
set "HEADER=[36m"
set "FOOTER=[36m"

:: Header
echo.
echo %HEADER%+--------------------------------------------------------------+%RESET%
echo %HEADER%|                                                              |%RESET%
echo %HEADER%|  EVA & GUARANI - Bot Update                                  |%RESET%
echo %HEADER%|  Version 1.0 (Batch)                                         |%RESET%
echo %HEADER%|                                                              |%RESET%
echo %HEADER%+--------------------------------------------------------------+%RESET%
echo.

:: Function to display log messages
call :log_message "Starting the update process for the EVA & GUARANI bot..." "INFO"

:: Create backup directory
set "backupDir=backup_%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "backupDir=%backupDir: =0%"

call :log_message "Creating backup directory: %backupDir%" "INFO"

if not exist "%backupDir%" mkdir "%backupDir%"
call :log_message "Backup directory created successfully" "SUCCESS"

:: Check prerequisites
call :log_message "Checking prerequisites..." "INFO"

:: Check Git
call :check_git_installed
if %errorlevel% neq 0 (
    call :log_message "Prerequisites not met. Update canceled." "ERROR"
    goto :end
)

:: Check Python
call :check_python_installed
if %errorlevel% neq 0 (
    call :log_message "Prerequisites not met. Update canceled." "ERROR"
    goto :end
)

:: Backup files
call :backup_files
call :log_message "Backup created in: %backupDir%" "SUCCESS"

:: Update repository
call :update_repository
if %errorlevel% neq 0 (
    call :log_message "Update canceled or failed." "WARNING"
    goto :end
)

:: Update dependencies
call :update_dependencies
if %errorlevel% neq 0 (
    call :log_message "Failed to update dependencies." "ERROR"
    set /p restore="Do you want to restore the backup? (Y/N): "
    if /i "%restore%"=="Y" (
        call :restore_backup
    )
    goto :end
)

:: Check bot health
call :check_bot_health
if %errorlevel% neq 0 (
    call :log_message "Problems detected after the update." "WARNING"
    set /p restore="Do you want to restore the backup? (Y/N): "
    if /i "%restore%"=="Y" (
        call :restore_backup
    )
    goto :end
)

call :log_message "Update completed successfully!" "SUCCESS"
call :log_message "The EVA & GUARANI bot has been updated to the latest version." "SUCCESS"
call :log_message "To start the bot, run: setup_and_start.ps1" "INFO"

:end
:: Footer
echo.
echo %FOOTER%+--------------------------------------------------------------+%RESET%
echo %FOOTER%|                                                              |%RESET%
echo %FOOTER%|  Update process completed                                    |%RESET%
echo %FOOTER%|                                                              |%RESET%
echo %FOOTER%+--------------------------------------------------------------+%RESET%
echo.

echo %UPDATE%*** EVA & GUARANI ***%RESET%
echo.

pause
exit /b 0

:: ===== FUNCTIONS =====

:log_message
:: %~1 = message, %~2 = type
set "timestamp=%date% %time%"
set "type=%~2"
if "%type%"=="" set "type=INFO"
set "color=!%type%!"
set "prefix=i"

if "%type%"=="SUCCESS" set "prefix=+"
if "%type%"=="ERROR" set "prefix=x"
if "%type%"=="WARNING" set "prefix=!"
if "%type%"=="UPDATE" set "prefix=*"

echo [%timestamp%] %color%[%type%]%RESET% %prefix% %~1
goto :eof

:check_git_installed
git --version > nul 2>&1
if %errorlevel% neq 0 (
    call :log_message "Git not found. Please install Git to continue." "ERROR"
    call :log_message "You can download Git at: https://git-scm.com/downloads" "INFO"
    exit /b 1
)

for /f "tokens=*" %%i in ('git --version') do set git_version=%%i
call :log_message "Git found: %git_version%" "SUCCESS"
exit /b 0

:check_python_installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    call :log_message "Python not found. Please install Python to continue." "ERROR"
    call :log_message "You can download Python at: https://www.python.org/downloads/" "INFO"
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set python_version=%%i
call :log_message "Python found: %python_version%" "SUCCESS"
exit /b 0

:backup_files
call :log_message "Backing up files..." "INFO"

:: Backup configuration files
if exist "config" (
    call :log_message "Backing up configuration files" "INFO"
    xcopy "config" "%backupDir%\config\" /E /I /H /Y > nul
    call :log_message "Configuration files backup completed" "SUCCESS"
) else (
    call :log_message "Configuration directory not found. No backup needed." "WARNING"
)

:: Backup logs
if exist "logs" (
    call :log_message "Backing up logs" "INFO"
    xcopy "logs" "%backupDir%\logs\" /E /I /H /Y > nul
    call :log_message "Logs backup completed" "SUCCESS"
)

:: Backup data
if exist "data" (
    call :log_message "Backing up data" "INFO"
    xcopy "data" "%backupDir%\data\" /E /I /H /Y > nul
    call :log_message "Data backup completed" "SUCCESS"
)

goto :eof

:update_repository
call :log_message "Checking repository updates" "UPDATE"

:: Check if the .git directory exists
if not exist ".git" (
    call :log_message "This does not appear to be a valid Git repository." "ERROR"
    call :log_message "Automatic update is not possible. Please download the latest version manually." "INFO"
    exit /b 1
)

:: Save the current version before updating
for /f "tokens=*" %%i in ('git rev-parse HEAD') do set current_version=%%i
call :log_message "Current version: %current_version%" "INFO"

:: Check for uncommitted local changes
git status --porcelain > temp_status.txt
set /p status=<temp_status.txt
del temp_status.txt

if not "%status%"=="" (
    call :log_message "There are uncommitted local changes:" "WARNING"
    git status
    
    set /p confirmation="Do you want to continue anyway? Local changes will be preserved. (Y/N): "
    if /i not "%confirmation%"=="Y" (
        call :log_message "Update canceled by user." "INFO"
        exit /b 1
    )
)

:: Update the repository
call :log_message "Fetching remote updates..." "UPDATE"
git fetch

:: Check if updates are available
for /f "tokens=*" %%i in ('git rev-parse HEAD') do set local_ref=%%i
for /f "tokens=*" %%i in ('git rev-parse origin/main') do set remote_ref=%%i

if "%local_ref%"=="%remote_ref%" (
    call :log_message "The bot is already at the latest version." "SUCCESS"
    exit /b 0
)

call :log_message "Updating to the latest version..." "UPDATE"
git pull

if %errorlevel% neq 0 (
    call :log_message "Failed to update the repository." "ERROR"
    exit /b 1
)

for /f "tokens=*" %%i in ('git rev-parse HEAD') do set new_version=%%i
call :log_message "Update completed successfully!" "SUCCESS"
call :log_message "New version: %new_version%" "INFO"

:: Display change log
call :log_message "Changes since the previous version:" "INFO"
git log --pretty=format:"%%h - %%s (%%cr)" %current_version%..%new_version%

exit /b 0

:update_dependencies
call :log_message "Updating dependencies..." "UPDATE"

if not exist "requirements.txt" (
    call :log_message "requirements.txt file not found." "ERROR"
    exit /b 1
)

python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    call :log_message "Error updating pip." "ERROR"
    exit /b 1
)

python -m pip install -r requirements.txt --upgrade
if %errorlevel% neq 0 (
    call :log_message "Error updating dependencies." "ERROR"
    exit /b 1
)

call :log_message "Dependencies updated successfully!" "SUCCESS"
exit /b 0

:restore_backup
call :log_message "Restoring backup from %backupDir%..." "WARNING"

:: Restore configurations
if exist "%backupDir%\config" (
    xcopy "%backupDir%\config" "config\" /E /I /H /Y > nul
    call :log_message "Configurations restored successfully" "SUCCESS"
)

:: Restore logs
if exist "%backupDir%\logs" (
    xcopy "%backupDir%\logs" "logs\" /E /I /H /Y > nul
    call :log_message "Logs restored successfully" "SUCCESS"
)

:: Restore data
if exist "%backupDir%\data" (
    xcopy "%backupDir%\data" "data\" /E /I /H /Y > nul
    call :log_message "Data restored successfully" "SUCCESS"
)

call :log_message "Restoration completed" "SUCCESS"
goto :eof

:check_bot_health
call :log_message "Checking bot health after update..." "INFO"

if exist "check_bot_health.bat" (
    call check_bot_health.bat
    exit /b %errorlevel%
) else if exist "check_bot_health.ps1" (
    call :log_message "Running health check via PowerShell..." "INFO"
    powershell -ExecutionPolicy Bypass -File "check_bot_health.ps1"
    exit /b %errorlevel%
) else (
    call :log_message "Health check script not found." "WARNING"
    exit /b 0
)