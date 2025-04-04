# EVA & GUARANI - Filesystem Module Test Starter
# Version: 1.0.0
# Date: 2025-03-29

$ErrorActionPreference = "Stop"
$Host.UI.RawUI.WindowTitle = "EVA & GUARANI Filesystem Test"

Write-Host "Starting EVA & GUARANI Filesystem Module Test..." -ForegroundColor Cyan

# Navigate to the filesystem module directory
Set-Location -Path "slop\modules\filesystem"

# Check if the cli-test.js file exists
if (-not (Test-Path "cli-test.js")) {
    Write-Host "ERROR: cli-test.js not found in the current directory" -ForegroundColor Red
    exit 1
}

# Start the test server
Write-Host "Starting test server on port 3001..." -ForegroundColor Green
Write-Host "Server will be available at http://localhost:3001" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

try {
    # Run Node.js command
    node cli-test.js server
} catch {
    Write-Host "Error starting test server: $_" -ForegroundColor Red
    exit 1
}
