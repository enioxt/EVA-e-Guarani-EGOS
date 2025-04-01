# EVA & GUARANI - Simple Filesystem Test Starter
# Version: 1.0.0
# Date: 2025-03-29

$ErrorActionPreference = "Stop"
$Host.UI.RawUI.WindowTitle = "EVA & GUARANI Simple Filesystem Test"

Write-Host "Starting EVA & GUARANI Simple Filesystem Test..." -ForegroundColor Cyan

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Node.js is not installed or not in PATH. Please install Node.js to run the test." -ForegroundColor Red
    exit 1
}

# Check if test-filesystem-simple.js exists
if (-not (Test-Path "test-filesystem-simple.js")) {
    Write-Host "ERROR: test-filesystem-simple.js not found in the current directory" -ForegroundColor Red
    exit 1
}

# Start the test server
Write-Host "Starting test server on port 3002..." -ForegroundColor Green
Write-Host "Server will be available at http://localhost:3002" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

try {
    # Run Node.js command
    node test-filesystem-simple.js
} catch {
    Write-Host "Error starting test server: $_" -ForegroundColor Red
    exit 1
} 