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
# - tools\utilities\start_egos.bat (kept)
# - tools\utilities\start_egos.bat.backup (moved to quarantine)
# ==================================================================

batch
@echo off
echo ====================================================
echo       STARTING EVA & GUARANI - EGOS v7.0
echo ====================================================
echo.

REM Set up environment
SET PYTHONPATH=%PYTHONPATH%;%~dp0;%~dp0\EGOS
SET EGOS_ROOT=%~dp0

REM Check dependencies
python -c "import sys; sys.exit(0 if all(map(lambda m: m in sys.modules or __import__(m, fromlist=['']) , ['os', 'sys', 'json', 'datetime'])) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install dependencies. Check the requirements.txt file.
        exit /b 1
    )
)

REM Check if directories exist
if not exist "%~dp0\EGOS" (
    echo EGOS directory structure not found.
    echo Run reorganize_egos.py to create the necessary structure.
    exit /b 1
)

echo Loading system core...
echo.

REM Main execution
python EGOS\core\egos_core.py %*

echo.
echo ====================================================
echo         EVA & GUARANI - EGOS FINISHED
echo ====================================================
echo ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧