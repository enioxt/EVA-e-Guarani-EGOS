powershell
﻿# EVA & GUARANI - Initializer for ElizaOS integration with Telegram
$ErrorActionPreference = "Stop"

$scriptPath = $PSScriptRoot
$elizaDir = Join-Path $scriptPath "eliza"

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "✧༚❀༛∞ EVA & GUARANI ∞༚❀༛✧" -ForegroundColor Magenta
Write-Host "Initializing ElizaOS integration with Telegram" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# Check if the ElizaOS directory exists
if (-not (Test-Path $elizaDir)) {
    Write-Host "ElizaOS directory not found: $elizaDir" -ForegroundColor Red
    Write-Host "Run the installation script first: install_eliza_integration.ps1" -ForegroundColor Red
    exit 1
}

# Start ElizaOS
Set-Location $elizaDir
Write-Host "Starting ElizaOS..." -ForegroundColor Green
& pnpm start

# Return to the original directory
Set-Location $scriptPath
