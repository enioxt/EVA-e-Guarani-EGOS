# EVA & GUARANI - NEXUS Environment Setup
# Version: 1.0.1
# Date: 2025-03-30

# Stop on first error
$ErrorActionPreference = "Stop"

# Get the script's directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Functions
function Test-Command {
    param($Command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Get-Command $Command) { return $true }
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }
}

function Write-Log {
    param($Message, $Type = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Type] $Message"
    Write-Host $logMessage

    # Ensure log directory exists
    $logsDir = Join-Path $scriptDir "logs"
    if (-not (Test-Path $logsDir)) {
        New-Item -ItemType Directory -Path $logsDir | Out-Null
    }

    Add-Content -Path $logFile -Value $logMessage
}

# Setup logging
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logsDir = Join-Path $scriptDir "logs"
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir | Out-Null
}
$logFile = Join-Path $logsDir "nexus_setup_$timestamp.log"
Write-Log "Starting NEXUS environment setup..."

# Check Node.js
Write-Log "Checking Node.js installation..."
if (-not (Test-Command "node")) {
    Write-Log "Node.js not found. Installing..." "SETUP"
    # Download and install Node.js
    $nodeUrl = "https://nodejs.org/dist/v22.14.0/node-v22.14.0-x64.msi"
    $nodeInstaller = "node_installer.msi"
    Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeInstaller
    Start-Process msiexec.exe -Wait -ArgumentList "/i $nodeInstaller /quiet"
    Remove-Item $nodeInstaller
    # Update PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}
$nodeVersion = node --version
Write-Log "Node.js version: $nodeVersion" "INFO"

# Check npm
Write-Log "Checking npm installation..."
if (-not (Test-Command "npm")) {
    Write-Log "npm not found" "ERROR"
    exit 1
}

# Install global npm packages
Write-Log "Installing global npm packages..." "SETUP"
npm install -g typescript@latest
npm install -g @types/node@latest
npm install -g webpack@latest
npm install -g webpack-cli@latest

# Create Python virtual environment
Write-Log "Setting up Python environment..." "SETUP"
python -m venv .venv
. .\.venv\Scripts\Activate.ps1

# Install Python dependencies from requirements.txt
Write-Log "Installing Python dependencies..." "SETUP"
python -m pip install --upgrade pip
$requirementsPath = Join-Path $scriptDir "nexus_requirements.txt"
if (Test-Path $requirementsPath) {
    pip install -r $requirementsPath
} else {
    Write-Log "Requirements file not found at: $requirementsPath" "ERROR"
    exit 1
}

# Create directory structure
Write-Log "Creating directory structure..." "SETUP"
$dirs = @(
    "QUANTUM_PROMPTS/NEXUS/core/python",
    "QUANTUM_PROMPTS/NEXUS/core/analyzers",
    "QUANTUM_PROMPTS/NEXUS/core/optimizers",
    "QUANTUM_PROMPTS/NEXUS/web/frontend/components",
    "QUANTUM_PROMPTS/NEXUS/web/frontend/styles",
    "QUANTUM_PROMPTS/NEXUS/web/backend/api",
    "QUANTUM_PROMPTS/NEXUS/web/backend/services",
    "QUANTUM_PROMPTS/NEXUS/integrations",
    "QUANTUM_PROMPTS/NEXUS/config",
    "QUANTUM_PROMPTS/NEXUS/docs",
    "QUANTUM_PROMPTS/NEXUS/tests/unit",
    "QUANTUM_PROMPTS/NEXUS/tests/integration",
    "QUANTUM_PROMPTS/NEXUS/scripts"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Log "Created directory: $dir" "INFO"
    }
}

# Initialize npm project in web directory
Write-Log "Initializing npm project..." "SETUP"
Push-Location
Set-Location QUANTUM_PROMPTS/NEXUS/web/frontend

# Create package.json with specific versions
$packageJson = @"
{
  "name": "nexus-frontend",
  "version": "1.0.0",
  "description": "NEXUS Frontend Components",
  "main": "src/index.ts",
  "scripts": {
    "build": "webpack --mode production",
    "dev": "webpack --mode development --watch",
    "test": "jest"
  },
  "keywords": ["nexus", "visualization", "analysis"],
  "author": "EVA & GUARANI",
  "license": "MIT"
}
"@
Set-Content -Path "package.json" -Value $packageJson

# Install dependencies
npm install --save react@latest d3@latest typescript@latest
npm install --save-dev webpack@latest webpack-cli@latest ts-loader@latest @types/react@latest @types/d3@latest

# Create webpack config
$webpackConfig = @"
const path = require('path');

module.exports = {
  entry: './src/index.ts',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
};
"@
Set-Content -Path "webpack.config.js" -Value $webpackConfig

# Create tsconfig
$tsConfig = @"
{
  "compilerOptions": {
    "outDir": "./dist/",
    "sourceMap": true,
    "noImplicitAny": true,
    "module": "es6",
    "target": "es5",
    "jsx": "react",
    "allowJs": true,
    "moduleResolution": "node",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "**/*.spec.ts"]
}
"@
Set-Content -Path "tsconfig.json" -Value $tsConfig

# Create src directory and basic files
New-Item -ItemType Directory -Path "src" -Force | Out-Null
New-Item -ItemType Directory -Path "src/components" -Force | Out-Null
New-Item -ItemType Directory -Path "src/styles" -Force | Out-Null

# Create initial index.ts
$indexTs = @"
import React from 'react';
import * as d3 from 'd3';

// Export components
export * from './components';
"@
Set-Content -Path "src/index.ts" -Value $indexTs

# Create components index
$componentsIndex = @"
// Export all components
"@
Set-Content -Path "src/components/index.ts" -Value $componentsIndex

Pop-Location

Write-Log "Environment setup completed successfully" "SUCCESS"
Write-Log "NEXUS environment setup completed" "SUCCESS"
