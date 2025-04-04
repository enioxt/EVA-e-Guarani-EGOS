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

REM EVA & GUARANI - Perplexity MCP Server
REM Este script inicia o servidor MCP para integração do Perplexity com o Cursor

echo ✧༺❀༻∞ EVA & GUARANI - PERPLEXITY MCP SERVER ∞༺❀༻✧
echo.

REM Check if python is available
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found in PATH
    echo Please ensure Python is installed and added to your PATH
    pause
    exit /b 1
)

REM Navigate to project root
cd /d %~dp0..\..

REM Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Install dependencies if needed
pip install -q websockets python-dotenv

REM Inform user
echo Starting Perplexity MCP Server on localhost:38001
echo This window must remain open while using the MCP in Cursor
echo Press Ctrl+C to stop the server
echo.

REM Start the MCP server
python -m tools.integration.mcp_server %*

REM Deactivate virtual environment before exiting
if exist "venv\Scripts\deactivate.bat" (
    call venv\Scripts\deactivate.bat
)

pause
