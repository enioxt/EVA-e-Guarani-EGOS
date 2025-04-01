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
# - tools\utilities\rename_directory.bat (kept)
# - tools\utilities\rename_directory.bat.backup (moved to quarantine)
# ==================================================================

batch
@echo off
echo.
echo Renaming project directory...
echo This process needs to be run as administrator!
echo.
timeout /t 2 /nobreak
echo Renaming from "C:\Eva & Guarani - EGOS" to "C:\Eva and Guarani - EGOS"...
ren "C:\Eva & Guarani - EGOS" "Eva and Guarani - EGOS"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Renaming completed successfully!
    echo Please reopen the project in the new directory: C:\Eva and Guarani - EGOS
) else (
    echo.
    echo ERROR in renaming! Please check if:
    echo 1. You are running as administrator
    echo 2. No program is using files in the directory
    echo 3. The destination directory does not exist
)
echo.
pause