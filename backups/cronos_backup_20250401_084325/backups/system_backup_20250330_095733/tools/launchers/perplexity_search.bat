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

@echo off
setlocal enabledelayedexpansion

REM EVA & GUARANI - Perplexity Search Tool
REM This script launches the Perplexity search integration for EVA & GUARANI

echo ✧༺❀༻∞ EVA & GUARANI - PERPLEXITY SEARCH ∞༺❀༻✧
echo.

REM Check if python is available
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found in PATH
    echo Please ensure Python is installed and added to your PATH
    pause
    exit /b 1
)

REM Check if query is provided
if "%~1"=="" (
    echo Usage: perplexity_search.bat "your search query" [--persona PERSONA_NAME]
    echo.
    echo Example: perplexity_search.bat "Latest developments in quantum computing" --persona scientist
    echo.
    set /p QUERY="Enter your search query: "
) else (
    set QUERY=%~1
)

REM Check for persona parameter
set PERSONA_ARG=
if "%~2"=="--persona" (
    if NOT "%~3"=="" (
        set PERSONA_ARG=--persona %~3
    )
)

REM Activate virtual environment if it exists
if exist "../../venv/Scripts/activate.bat" (
    call "../../venv/Scripts/activate.bat"
)

REM Execute the script
cd ..\..\
python -m tools.integration.test_perplexity "%QUERY%" %PERSONA_ARG%

REM Deactivate virtual environment
if exist "../../venv/Scripts/deactivate.bat" (
    call venv\Scripts\deactivate.bat
)

echo.
echo ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
echo.

pause
