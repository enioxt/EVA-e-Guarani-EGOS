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

REM EVA & GUARANI - Cursor Context Enrichment Tool
REM This script adds Perplexity search results to Cursor's context

echo ✧༺❀༻∞ EVA & GUARANI - CURSOR CONTEXT ENRICHER ∞༺❀༻✧
echo.

REM Check if python is available
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found in PATH
    echo Please ensure Python is installed and added to your PATH
    pause
    exit /b 1
)

REM Check if command is provided
if "%~1"=="" (
    echo Usage: 
    echo   enrich_cursor_context.bat enrich "Your search query" [--persona PERSONA_NAME]
    echo   enrich_cursor_context.bat list
    echo   enrich_cursor_context.bat get CONTEXT_NAME
    echo.
    echo Examples:
    echo   enrich_cursor_context.bat enrich "Latest developments in quantum computing" --persona scientist
    echo   enrich_cursor_context.bat list
    echo.
    
    set /p COMMAND="Enter command (enrich/list/get): "
    
    if "!COMMAND!"=="enrich" (
        set /p QUERY="Enter your search query: "
        set /p PERSONA="Enter persona (optional, press Enter to skip): "
        
        if "!PERSONA!"=="" (
            set ARGS=enrich "!QUERY!"
        ) else (
            set ARGS=enrich "!QUERY!" --persona !PERSONA!
        )
    ) else if "!COMMAND!"=="list" (
        set ARGS=list
    ) else if "!COMMAND!"=="get" (
        set /p NAME="Enter context name to retrieve: "
        set ARGS=get !NAME!
    ) else (
        echo Invalid command: !COMMAND!
        pause
        exit /b 1
    )
) else (
    set ARGS=%*
)

REM Activate virtual environment if it exists
if exist "../../venv/Scripts/activate.bat" (
    call "../../venv/Scripts/activate.bat"
)

REM Execute the script
cd ..\..\
python -m tools.integration.cursor_context %ARGS%

REM Deactivate virtual environment
if exist "../../venv/Scripts/deactivate.bat" (
    call venv\Scripts\deactivate.bat
)

echo.
echo ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
echo.

pause 