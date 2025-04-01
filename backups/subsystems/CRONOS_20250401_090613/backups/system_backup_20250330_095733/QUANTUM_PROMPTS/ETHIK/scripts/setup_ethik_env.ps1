# EVA & GUARANI - ETHIK Environment Setup
# Version: 1.0
# Date: 2025-03-29

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
$logFile = "logs/ethik_setup_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
Start-Transcript -Path $logFile

try {
    Write-Log "Starting ETHIK environment setup..."

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
    npm install -g truffle
    npm install -g hardhat
    npm install -g ethers
    npm install -g web3
    npm install -g solc

    # Create Python virtual environment
    Write-Log "Setting up Python environment..." "SETUP"
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

    # Install Python dependencies
    Write-Log "Installing Python dependencies..." "SETUP"
    python -m pip install --upgrade pip
    pip install -r requirements.txt

    # Initialize Hardhat project
    Write-Log "Initializing Hardhat project..." "SETUP"
    mkdir -p QUANTUM_PROMPTS/ETHIK/core/contracts
    Set-Location QUANTUM_PROMPTS/ETHIK/core/contracts
    npm init -y
    npm install --save-dev hardhat @nomiclabs/hardhat-ethers ethers @nomiclabs/hardhat-waffle ethereum-waffle chai @openzeppelin/contracts
    npx hardhat init

    # Initialize Truffle project
    Write-Log "Initializing Truffle project..." "SETUP"
    truffle init

    # Create test network configuration
    $truffleConfig = @"
module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id: "*"
    }
  },
  compilers: {
    solc: {
      version: "^0.8.0"
    }
  }
};
"@
    Set-Content -Path "truffle-config.js" -Value $truffleConfig

    # Install development dependencies
    Write-Log "Installing development dependencies..." "SETUP"
    npm install --save-dev @openzeppelin/test-helpers
    npm install --save-dev solidity-coverage
    npm install --save-dev prettier prettier-plugin-solidity
    npm install --save-dev eslint eslint-config-standard
    npm install --save-dev typescript @types/node @types/mocha

    # Create basic test structure
    mkdir -p test/contracts
    mkdir -p test/web3

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