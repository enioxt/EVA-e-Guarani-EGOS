# EVA & GUARANI - File Migration Script
# Version: 1.0.1
# Date: 2025-03-30

# Stop on first error
$ErrorActionPreference = "Stop"

Write-Host "Starting file migration..."

# Create directories if they don't exist
$directories = @(
    "QUANTUM_PROMPTS/ATLAS/scripts",
    "QUANTUM_PROMPTS/ATLAS/docs",
    "QUANTUM_PROMPTS/ETHIK/scripts",
    "QUANTUM_PROMPTS/ETHIK/docs"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        Write-Host "Creating directory: $dir"
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Move ATLAS files
Write-Host "Moving ATLAS files..."
Move-Item -Path "QUANTUM_PROMPTS/CRONOS/scripts/atlas_unification.py" -Destination "QUANTUM_PROMPTS/ATLAS/scripts/" -Force
Move-Item -Path "QUANTUM_PROMPTS/CRONOS/scripts/atlas_requirements.txt" -Destination "QUANTUM_PROMPTS/ATLAS/scripts/" -Force
Move-Item -Path "QUANTUM_PROMPTS/CRONOS/scripts/setup_atlas_env.ps1" -Destination "QUANTUM_PROMPTS/ATLAS/scripts/" -Force
Move-Item -Path "QUANTUM_PROMPTS/CRONOS/unification_reports/atlas_analysis.md" -Destination "QUANTUM_PROMPTS/ATLAS/docs/" -Force

# Move ETHIK files
Write-Host "Moving ETHIK files..."
Move-Item -Path "QUANTUM_PROMPTS/CRONOS/scripts/ethik_unification.py" -Destination "QUANTUM_PROMPTS/ETHIK/scripts/" -Force
Move-Item -Path "QUANTUM_PROMPTS/CRONOS/scripts/setup_ethik_env.ps1" -Destination "QUANTUM_PROMPTS/ETHIK/scripts/" -Force
Move-Item -Path "QUANTUM_PROMPTS/CRONOS/unification_reports/ethik_analysis.md" -Destination "QUANTUM_PROMPTS/ETHIK/docs/" -Force

Write-Host "File migration completed successfully!" 