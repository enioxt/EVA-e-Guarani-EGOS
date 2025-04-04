---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: start_project.bat
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
echo.
echo ================================================================================
echo EVA ^& GUARANI - Project Launcher
echo ================================================================================
echo.

REM Check if workspace file exists
if not exist "eva_guarani.code-workspace" (
    echo ERROR: Workspace file not found.
    echo Please run setup first or make sure you're in the correct directory.
    goto :error
)

REM Check if folders are properly linked/excluded
echo Checking project structure...

REM Verify docs and eva-atendimento are excluded or linked
set docs_handled=0
set eva_handled=0

if exist "docs" (
    if exist "docs\NUL" (
        REM Directory exists, check if it's a symbolic link
        dir /al docs | find "<SYMLINK>" > nul
        if !errorlevel! equ 0 (
            echo - docs: OK ^(symbolic link^)
            set docs_handled=1
        ) else (
            echo - docs: Found ^(regular directory^)
        )
    )
) else (
    echo - docs: Not found ^(excluded^)
    set docs_handled=1
)

if exist "eva-atendimento" (
    if exist "eva-atendimento\NUL" (
        REM Directory exists, check if it's a symbolic link
        dir /al eva-atendimento | find "<SYMLINK>" > nul
        if !errorlevel! equ 0 (
            echo - eva-atendimento: OK ^(symbolic link^)
            set eva_handled=1
        ) else (
            echo - eva-atendimento: Found ^(regular directory^)
        )
    )
) else (
    echo - eva-atendimento: Not found ^(excluded^)
    set eva_handled=1
)

if %docs_handled% equ 0 (
    echo.
    echo WARNING: The docs directory is not optimized.
    echo It's recommended to move it outside the project for better performance.
    echo Run 'tools\setup_references.ps1' as Administrator.
)

if %eva_handled% equ 0 (
    echo.
    echo WARNING: The eva-atendimento directory is not optimized.
    echo It's recommended to move it outside the project for better performance.
    echo Run 'tools\setup_references.ps1' as Administrator.
)

REM Clean up __pycache__ directories to improve performance
echo.
echo Cleaning up temporary files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo - Removed __pycache__ directories

REM Launch Cursor/VSCode with the workspace
echo.
echo Launching project...
echo.

REM Try to detect Cursor or use VSCode as fallback
set found=0

REM Try to find Cursor
for %%p in (
    "%LOCALAPPDATA%\Programs\cursor\Cursor.exe"
    "%APPDATA%\Local\Programs\cursor\Cursor.exe"
    "C:\Program Files\cursor\Cursor.exe"
    "C:\Program Files (x86)\cursor\Cursor.exe"
) do (
    if exist %%p (
        echo Opening with Cursor...
        start "" %%p "eva_guarani.code-workspace"
        set found=1
        goto :found
    )
)

REM Try to find VSCode
for %%p in (
    "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
    "%APPDATA%\Local\Programs\Microsoft VS Code\Code.exe"
    "C:\Program Files\Microsoft VS Code\Code.exe"
    "C:\Program Files (x86)\Microsoft VS Code\Code.exe"
) do (
    if exist %%p (
        echo Opening with Visual Studio Code...
        start "" %%p "eva_guarani.code-workspace"
        set found=1
        goto :found
    )
)

:found
if %found% equ 0 (
    echo.
    echo Could not find Cursor or VSCode automatically.
    echo Please open "eva_guarani.code-workspace" manually.
)

echo.
echo ================================================================================
echo EVA ^& GUARANI project is ready.
echo.
echo If you need to work with large directories:
echo - Open them directly as separate workspaces
echo - Or temporarily modify the exclude settings in the workspace file
echo ================================================================================

goto :end

:error
echo.
echo Setup failed. Please check the error messages above.

:end
pause
