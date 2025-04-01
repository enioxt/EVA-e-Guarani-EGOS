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

:: EVA & GUARANI - Translation Tools Runner
:: This batch script helps run translation tools for the entire EVA & GUARANI system, not just sandbox

:: Set UTF-8 code page
chcp 65001 > nul

:: Function to display header
:display_header
echo.
echo ========================================================================
echo                EVA ^& GUARANI - Translation Tools Runner
echo            (For the entire EVA ^& GUARANI system, not just sandbox)
echo ========================================================================
echo.
goto :eof

:: Main menu
:main_menu
call :display_header
echo Select an option:
echo.
echo 1. Scan project for Portuguese files
echo 2. Translate a specific file using AI
echo 3. Exit
echo.
set /p option="Enter your choice (1-3): "

if "%option%"=="1" goto scan_project
if "%option%"=="2" goto translate_file
if "%option%"=="3" goto exit_script

echo Invalid option. Please try again.
pause
cls
goto main_menu

:: Scan project
:scan_project
echo.
echo Scanning project for Portuguese files...
echo.

set "defaultRootDir=C:\Eva & Guarani - EGOS"

if not exist "%defaultRootDir%" (
    set "defaultRootDir=..\..\"
)

echo This will scan the entire EVA ^& GUARANI system for Portuguese content.
echo The scan will focus on project files and exclude system directories.
echo This may take a few minutes depending on the size of your project.
echo.

set /p rootDir="Enter root directory to scan (default: %defaultRootDir%): "

if "!rootDir!"=="" (
    set "rootDir=%defaultRootDir%"
)

echo.
echo Running scanner...
echo.

python translate_to_english.py --root-dir "!rootDir!"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Scan complete. Check translation_report.md for results.
    echo.
) else (
    echo.
    echo Scan failed with error code %ERRORLEVEL%
    echo.
)

pause
cls
goto main_menu

:: Translate a file
:translate_file
echo.
echo Translate a specific file using AI
echo.
set /p file_path="Enter the path to the file you want to translate: "

if not exist "!file_path!" (
    echo File does not exist: !file_path!
    pause
    cls
    goto main_menu
)

:: Default API key from the project
set "default_api_key=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"

echo.
echo A default API key is available in the project.
set /p use_custom_key="Do you want to use a different API key? (y/N): "

if /i "!use_custom_key!"=="y" (
    set /p custom_api_key="Enter your OpenAI API key (or press Enter to use OPENAI_API_KEY environment variable): "
    set "api_key_param="
    if not "!custom_api_key!"=="" (
        set "api_key_param=--api-key !custom_api_key!"
    )
) else (
    set "OPENAI_API_KEY=!default_api_key!"
    set "api_key_param="
)

set /p output_path="Enter output file path (leave empty to replace original): "
set "output_param="
if not "!output_path!"=="" (
    set "output_param=--output !output_path!"
)

set /p dry_run="Do you want to perform a dry run (no changes will be made)? (y/N): "
set "dry_run_param="
if /i "!dry_run!"=="y" (
    set "dry_run_param=--dry-run"
)

echo.
echo Translating file...
echo.

python ai_translate_file.py --file "!file_path!" !api_key_param! !output_param! !dry_run_param!

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Translation complete. Check the output file.
    echo.
) else (
    echo.
    echo Translation failed with error code %ERRORLEVEL%
    echo.
)

pause
cls
goto main_menu

:exit_script
echo.
echo Thank you for using the EVA ^& GUARANI translation tools.
echo.
pause
exit /b 0 