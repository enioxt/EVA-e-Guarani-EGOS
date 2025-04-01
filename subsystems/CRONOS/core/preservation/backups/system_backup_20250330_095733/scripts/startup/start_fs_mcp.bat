---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: start_fs_mcp.bat
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
echo Starting Filesystem MCP Server...

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

:: Install the MCP filesystem server globally if not already installed
call npm install -g @modelcontextprotocol/server-filesystem

:: Set debug environment variable
set DEBUG=*

:: Kill any existing MCP processes on port 38005
for /f "tokens=5" %%a in ('netstat -aon ^| find ":38005"') do (
    taskkill /F /PID %%a 2>nul
)

:: Start the filesystem MCP server as a detached process
start /B cmd /c "npx -y @modelcontextprotocol/server-filesystem --port 38005 \"C:\Eva Guarani EGOS\" \"C:\Users\Enidi\Documents\" > logs\fs_mcp.log 2>&1"

:: Wait a moment for the server to start
timeout /t 2 /nobreak > nul

:: Check if the server is running
netstat -ano | find ":38005" > nul
if errorlevel 1 (
    echo Failed to start filesystem MCP server
    type logs\fs_mcp.log
    pause
    exit /b 1
) else (
    echo Filesystem MCP server started successfully on port 38005
    echo Server output is being logged to logs\fs_mcp.log
    echo The server is running in background
    
    :: Display the process information
    echo.
    echo Current MCP server process:
    netstat -ano | find ":38005"
    echo.
    
    :: Keep the window open to maintain the process
    echo Press Ctrl+C to stop the server...
    cmd /k "echo Server is running... && echo To stop the server, close this window."
) 