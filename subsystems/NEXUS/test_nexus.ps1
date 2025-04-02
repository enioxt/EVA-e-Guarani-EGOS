# EVA & GUARANI - NEXUS Test Runner
# ================================
# PowerShell script to run NEXUS tests with coverage reporting

# Parameters
param(
    [switch]$Verbose = $false,
    [switch]$Coverage = $false
)

Write-Host "[NEXUS Test Runner] Starting..."

# Get the script's directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..\..") # Assumes script is in subsystems/NEXUS

Write-Host "[NEXUS Test Runner] Project Root: $projectRoot"
Write-Host "[NEXUS Test Runner] Script Directory: $scriptDir"

# Change to project root for pytest discovery
Write-Host "[NEXUS Test Runner] Changing location to Project Root..."
Set-Location $projectRoot

# Check for virtual environment at project root
$venvPath = Join-Path $projectRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "[NEXUS Test Runner] Creating virtual environment at project root..."
    python -m venv .venv
}

# Activate virtual environment
Write-Host "[NEXUS Test Runner] Activating virtual environment..."
if ($IsWindows) {
    .\.venv\Scripts\Activate.ps1
} else {
    # Adjust for non-Windows if needed, though primary target is Windows
    . ./.venv/bin/activate
}

# Install dependencies if needed (pytest, pytest-cov)
Write-Host "[NEXUS Test Runner] Installing/Updating test dependencies (pytest, pytest-cov)..."
pip install pytest pytest-cov

# Install the project in editable mode with increased verbosity
Write-Host "[NEXUS Test Runner] Installing project in editable mode (pip install -e . -v)..."
pip install -e . -v # Added -v for verbose output

# Construct pytest command targeting the NEXUS tests
Write-Host "[NEXUS Test Runner] Constructing pytest command..."
$pytestArgs = @(
    "subsystems/NEXUS/tests"
)

if ($Verbose) {
    Write-Host "[NEXUS Test Runner] Verbose mode enabled for pytest."
    $pytestArgs += "-v"
}

if ($Coverage) {
    Write-Host "[NEXUS Test Runner] Coverage reporting enabled for pytest."
    $pytestArgs += @(
        "--cov=subsystems/NEXUS/core", # Coverage for the core module
        "--cov-report=term-missing"
    )
}

# Run tests from project root
Write-Host "[NEXUS Test Runner] Executing pytest...
---"
python -m pytest $pytestArgs
Write-Host "---
[NEXUS Test Runner] Pytest execution finished."

# Deactivate virtual environment
Write-Host "[NEXUS Test Runner] Deactivating virtual environment..."
deactivate
Write-Host "[NEXUS Test Runner] Finished." 