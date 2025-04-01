# EVA & GUARANI - ATLAS Environment Setup
# Version: 1.0
# Date: 2025-03-30

# Stop on first error
$ErrorActionPreference = "Stop"

# Function to check if a command exists
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Function to log messages
function Write-Log {
    param($Message, $Type = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Type] $Message"
}

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs"
}

# Start logging
$logFile = "logs/atlas_setup_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
Start-Transcript -Path $logFile

try {
    Write-Log "Starting ATLAS environment setup..."

    # Check Node.js
    if (-not (Test-Command "node")) {
        Write-Log "Installing Node.js..." "SETUP"
        winget install OpenJS.NodeJS.LTS
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    }
    Write-Log "Node.js version: $(node --version)"

    # Check npm
    if (-not (Test-Command "npm")) {
        Write-Log "ERROR: npm not found after Node.js installation" "ERROR"
        exit 1
    }
    Write-Log "npm version: $(npm --version)"

    # Install global npm packages
    Write-Log "Installing global npm packages..." "SETUP"
    npm install -g d3
    npm install -g react
    npm install -g typescript
    npm install -g @types/d3
    npm install -g @types/react

    # Create Python virtual environment
    Write-Log "Setting up Python environment..." "SETUP"
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

    # Install Python dependencies
    Write-Log "Installing Python dependencies..." "SETUP"
    python -m pip install --upgrade pip
    pip install streamlit
    pip install networkx
    pip install plotly
    pip install pandas
    pip install numpy
    pip install scipy
    pip install scikit-learn
    pip install matplotlib
    pip install seaborn
    pip install pytest
    pip install pytest-cov
    pip install black
    pip install flake8
    pip install mypy
    pip install python-dotenv

    # Create visualization directory structure
    Write-Log "Creating visualization directory structure..." "SETUP"
    mkdir -p QUANTUM_PROMPTS/ATLAS/core/visualization
    Set-Location QUANTUM_PROMPTS/ATLAS/core/visualization

    # Initialize npm project for visualizations
    npm init -y
    npm install --save d3
    npm install --save react
    npm install --save typescript
    npm install --save @types/d3
    npm install --save @types/react
    npm install --save-dev webpack
    npm install --save-dev webpack-cli
    npm install --save-dev typescript
    npm install --save-dev ts-loader

    # Create basic webpack configuration
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

    # Create TypeScript configuration
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
    "moduleResolution": "node"
  }
}
"@
    Set-Content -Path "tsconfig.json" -Value $tsConfig

    # Return to root directory
    Set-Location -Path (Get-Item $PSScriptRoot).Parent.Parent.Parent.FullName

    Write-Log "Environment setup completed successfully" "SUCCESS"
    Write-Log "You can now run the unification script"

} catch {
    Write-Log $_.Exception.Message "ERROR"
    Write-Log "Environment setup failed" "ERROR"
    exit 1
} finally {
    Stop-Transcript
} 