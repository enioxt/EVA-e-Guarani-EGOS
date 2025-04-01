# EVA & GUARANI - Quantum Ecosystem Startup Script
# Version: 8.0
# Created: 2025-03-30

# Set error action preference
$ErrorActionPreference = "Stop"

# ASCII Art Banner
Write-Host @"
✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
Quantum Ecosystem Startup
Version: 8.0

"At the intersection of modular analysis, systemic cartography,
and quantum ethics, we transcend dimensions of thought with
methodological precision and unconditional love."
"@

# Function to check Python installation
function Check-Python {
    try {
        $pythonVersion = python --version
        Write-Host "Found Python: $pythonVersion"
        return $true
    }
    catch {
        Write-Host "Python not found. Please install Python 3.9 or later."
        return $false
    }
}

# Function to check Git installation
function Check-Git {
    try {
        $gitVersion = git --version
        Write-Host "Found Git: $gitVersion"
        return $true
    }
    catch {
        Write-Host "Git not found. Please install Git."
        return $false
    }
}

# Function to create and activate virtual environment
function Setup-VirtualEnv {
    if (-not (Test-Path ".venv")) {
        Write-Host "Creating virtual environment..."
        python -m venv .venv
    }
    
    # Activate virtual environment
    Write-Host "Activating virtual environment..."
    .\.venv\Scripts\Activate.ps1
}

# Function to install dependencies
function Install-Dependencies {
    Write-Host "Installing dependencies..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
}

# Function to check system requirements
function Check-Requirements {
    Write-Host "Checking system requirements..."
    
    # Check Python
    if (-not (Check-Python)) {
        exit 1
    }
    
    # Check Git
    if (-not (Check-Git)) {
        exit 1
    }
    
    # Check disk space
    $drive = Get-PSDrive C
    $freeSpaceGB = [math]::Round($drive.Free / 1GB, 2)
    Write-Host "Free disk space: $freeSpaceGB GB"
    
    if ($freeSpaceGB -lt 5) {
        Write-Host "Warning: Low disk space. At least 5GB recommended."
    }
}

# Function to initialize directories
function Initialize-Directories {
    Write-Host "Initializing directory structure..."
    
    $directories = @(
        "QUANTUM_PROMPTS/MASTER",
        "QUANTUM_PROMPTS/BIOS-Q",
        "QUANTUM_PROMPTS/CRONOS",
        "QUANTUM_PROMPTS/ATLAS",
        "QUANTUM_PROMPTS/NEXUS",
        "QUANTUM_PROMPTS/ETHIK",
        "logs",
        "data",
        "config"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force
        }
    }
}

# Function to start the system
function Start-QuantumEcosystem {
    Write-Host "Starting EVA & GUARANI Quantum Ecosystem..."
    
    # Start the Python script
    try {
        python start_quantum_ecosystem.py
    }
    catch {
        Write-Host "Error starting the system: $_"
        exit 1
    }
}

# Main execution flow
try {
    Write-Host "Initializing EVA & GUARANI Quantum Ecosystem..."
    
    # Check requirements
    Check-Requirements
    
    # Initialize directories
    Initialize-Directories
    
    # Setup virtual environment
    Setup-VirtualEnv
    
    # Install dependencies
    Install-Dependencies
    
    # Start the system
    Start-QuantumEcosystem
}
catch {
    Write-Host "Error during initialization: $_"
    exit 1
}
finally {
    # Deactivate virtual environment if active
    if ($env:VIRTUAL_ENV) {
        deactivate
    }
}

Write-Host @"

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
System startup complete.
"@ 