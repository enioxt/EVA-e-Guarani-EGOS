---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: sandbox
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
REM Script to start the EVA & GUARANI sandbox environment on Windows

echo ===============================================
echo   EVA & GUARANI - Starting Sandbox Environment
echo ===============================================
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found in PATH.
    echo Please install Python 3.7 or higher.
    echo.
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Flask not found. Do you want to install the dependencies? (Y/N)
    set /p INSTALL=
    if /i "%INSTALL%"=="Y" (
        echo Installing dependencies...
        pip install -r requirements.txt
        if %ERRORLEVEL% neq 0 (
            echo ERROR installing dependencies.
            pause
            exit /b 1
        )
    ) else (
        echo Installation cancelled.
        pause
        exit /b 1
    )
)

REM Run the Python script
echo Starting the Sandbox environment...
python run_sandbox.py %*

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR starting the Sandbox environment.
    pause
)

exit /b %ERRORLEVEL%
