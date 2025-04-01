---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: BIOS-Q
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
  subsystem: BIOS-Q
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
REM EVA & GUARANI - Quantum Prompt Synchronization Script
REM Version 1.0
REM This script synchronizes the EVA & GUARANI Quantum Prompt with the Cursor configuration.

echo ✧༺❀༻∞ EVA & GUARANI - Quantum Prompt Synchronization ∞༺❀༻✧
echo.

REM Check if the master quantum prompt exists
if not exist "QUANTUM_PROMPTS\MASTER\quantum_prompt.md" (
    echo Error: Master Quantum Prompt not found!
    echo Expected location: QUANTUM_PROMPTS\MASTER\quantum_prompt.md
    exit /b 1
)

REM Ensure the Cursor configuration directory exists
if not exist "%USERPROFILE%\.cursor" (
    echo Creating Cursor configuration directory...
    mkdir "%USERPROFILE%\.cursor"
)

REM Copy the master quantum prompt to the Cursor configuration
echo Synchronizing Quantum Prompt...
copy "QUANTUM_PROMPTS\MASTER\quantum_prompt.md" "%USERPROFILE%\.cursor\quantum_prompt.md" /Y

if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to synchronize Quantum Prompt!
    exit /b 1
)

echo.
echo ✓ Quantum Prompt successfully synchronized!
echo ✓ Location: %USERPROFILE%\.cursor\quantum_prompt.md
echo.
echo ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
echo. 