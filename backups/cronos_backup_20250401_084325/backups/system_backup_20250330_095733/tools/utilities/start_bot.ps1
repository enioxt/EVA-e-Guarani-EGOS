powershell
# EVA & GUARANI - PowerShell Initialization Script
# =============================================

# Set encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "            EVA & GUARANI - TELEGRAM BOT                " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "  You can download Python at: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Create necessary directories
$directories = @("logs", "config", "data", "temp")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "[OK] Directory '$dir' created" -ForegroundColor Green
    } else {
        Write-Host "[OK] Directory '$dir' already exists" -ForegroundColor Green
    }
}

# Set PYTHONPATH
$env:PYTHONPATH = "$env:PYTHONPATH;$PWD"
Write-Host "[OK] PYTHONPATH set: $env:PYTHONPATH" -ForegroundColor Green

# Check dependencies
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Cyan

$packages = @("python-telegram-bot", "openai")
foreach ($package in $packages) {
    $moduleName = if ($package -eq "python-telegram-bot") { "telegram" } else { $package -replace "-", "_" }
    $result = python -c "import $moduleName" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Package '$package' is already installed" -ForegroundColor Green
    } else {
        Write-Host "[INFO] Installing package '$package'..." -ForegroundColor Yellow
        pip install $package
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Package '$package' installed successfully" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] Failed to install package '$package'" -ForegroundColor Red
        }
    }
}

# Start the bot
Write-Host ""
Write-Host "Starting the EVA & GUARANI bot..." -ForegroundColor Cyan
Write-Host ""

# Try to start the bot as a Python module
if (Test-Path "bot\__main__.py") {
    Write-Host "Starting as Python module..." -ForegroundColor Cyan
    python -m bot
} elseif (Test-Path "bot\unified_telegram_bot_utf8.py") {
    Write-Host "Starting main bot script..." -ForegroundColor Cyan
    python bot\unified_telegram_bot_utf8.py
} else {
    Write-Host "[ERROR] Could not find the bot files." -ForegroundColor Red
    Write-Host "  Please check if the files are present in the 'bot' directory." -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit"
