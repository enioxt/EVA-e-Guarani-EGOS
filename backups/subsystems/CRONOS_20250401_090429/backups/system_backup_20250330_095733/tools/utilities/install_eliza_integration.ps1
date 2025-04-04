powershell
# EVA & GUARANI - ElizaOS Integration Installer
# This script installs the ElizaOS framework and configures the integration
# with the EVA & GUARANI Telegram bot.

$ErrorActionPreference = "Stop"

# Settings
$scriptPath = $PSScriptRoot
$logFile = Join-Path $scriptPath "logs\eliza_install.log"
$logsDir = Join-Path $scriptPath "logs"
$telegramConfigFile = Join-Path $scriptPath "config\telegram_config.json"
$elizaConfigFile = Join-Path $scriptPath "config\eliza_config.json"
$installDir = Join-Path $scriptPath "eliza"
$elizaLogsDir = Join-Path $installDir "logs"

# Create logs directory if it doesn't exist
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir | Out-Null
}

# Function to log messages
function Write-Log {
    param (
        [string]$Message,
        [string]$Level = "INFO"
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"

    Write-Host $logMessage

    # Ensure the logs directory exists
    if (-not (Test-Path (Split-Path -Path $logFile -Parent))) {
        New-Item -ItemType Directory -Path (Split-Path -Path $logFile -Parent) -Force | Out-Null
    }

    Add-Content -Path $logFile -Value $logMessage -Encoding UTF8
}

# Check Node.js and npm
function Test-NodeJs {
    try {
        $nodeVersion = & node --version 2>&1
        $npmVersion = & npm --version 2>&1

        Write-Log "Node.js detected: $nodeVersion"
        Write-Log "npm detected: $npmVersion"

        return $true
    } catch {
        Write-Log "Node.js or npm not found. Please install Node.js version 23+ from https://nodejs.org/" "ERROR"
        return $false
    }
}

# Check pnpm
function Test-Pnpm {
    try {
        $pnpmVersion = & pnpm --version 2>&1
        Write-Log "pnpm detected: $pnpmVersion"
        return $true
    } catch {
        Write-Log "pnpm not found. Attempting to install..." "WARNING"

        try {
            & npm install -g pnpm
            $pnpmVersion = & pnpm --version 2>&1
            Write-Log "pnpm installed: $pnpmVersion"
            return $true
        } catch {
            Write-Log "Failed to install pnpm. Please install manually: npm install -g pnpm" "ERROR"
            return $false
        }
    }
}

# Check Python
function Test-Python {
    try {
        $pythonVersion = & python --version 2>&1
        Write-Log "Python detected: $pythonVersion"
        return $true
    } catch {
        Write-Log "Python not found. Please install Python 3.6 or higher." "ERROR"
        return $false
    }
}

# Check Git
function Test-Git {
    try {
        $gitVersion = & git --version 2>&1
        Write-Log "Git detected: $gitVersion"
        return $true
    } catch {
        Write-Log "Git not found. Please install Git from https://git-scm.com/" "ERROR"
        return $false
    }
}

# Clone ElizaOS repository
function Clone-ElizaRepo {
    if (Test-Path $installDir) {
        Write-Log "ElizaOS directory already exists. Updating..." "WARNING"

        Set-Location $installDir
        & git pull

        if ($LASTEXITCODE -ne 0) {
            Write-Log "Error updating repository. Attempting again with a clean repository..." "WARNING"
            Set-Location $scriptPath
            Remove-Item -Recurse -Force $installDir
            return Clone-ElizaRepo
        }

        Set-Location $scriptPath
        return $true
    }

    Write-Log "Cloning ElizaOS repository..."
    & git clone https://github.com/elizaOS/eliza-starter.git $installDir

    if ($LASTEXITCODE -ne 0) {
        Write-Log "Failed to clone ElizaOS repository." "ERROR"
        return $false
    }

    # Create logs directory within ElizaOS
    if (-not (Test-Path $elizaLogsDir)) {
        New-Item -ItemType Directory -Path $elizaLogsDir -Force | Out-Null
        Write-Log "Created logs directory: $elizaLogsDir"
    }

    return $true
}

# Install ElizaOS dependencies
function Install-ElizaDependencies {
    Write-Log "Installing ElizaOS dependencies..."
    Set-Location $installDir

    # Copy .env.example to .env (if it doesn't exist)
    if (-not (Test-Path ".env")) {
        Copy-Item ".env.example" ".env"
        Write-Log ".env file created from .env.example"
    }

    # Install dependencies
    & pnpm i

    if ($LASTEXITCODE -ne 0) {
        Write-Log "Failed to install ElizaOS dependencies." "ERROR"
        Set-Location $scriptPath
        return $false
    }

    # Build ElizaOS
    & pnpm build

    if ($LASTEXITCODE -ne 0) {
        Write-Log "Failed to build ElizaOS." "ERROR"
        Set-Location $scriptPath
        return $false
    }

    Set-Location $scriptPath
    return $true
}

# Load Telegram configuration
function Get-TelegramConfig {
    if (-not (Test-Path $telegramConfigFile)) {
        Write-Log "Telegram configuration file not found: $telegramConfigFile" "ERROR"
        return $null
    }

    try {
        $config = Get-Content $telegramConfigFile -Raw | ConvertFrom-Json
        return $config
    } catch {
        Write-Log "Error reading Telegram configuration file: $_" "ERROR"
        return $null
    }
}

# Configure ElizaOS for Telegram integration
function Configure-ElizaForTelegram {
    param (
        [PSCustomObject]$TelegramConfig
    )

    if ($null -eq $TelegramConfig) {
        return $false
    }

    $botToken = $TelegramConfig.bot_token

    if ([string]::IsNullOrEmpty($botToken)) {
        Write-Log "Bot token not found in Telegram configuration." "ERROR"
        return $false
    }

    # Create or update .env file for ElizaOS
    $envFile = Join-Path $installDir ".env"
    $envContent = @"
# ElizaOS Environment Configuration
TELEGRAM_BOT_TOKEN=$botToken
OPENAI_API_KEY=$($TelegramConfig.openai_api_key)

# Integration Configuration
ELIZA_INTEGRATION_MODE=telegram
ELIZA_LOG_LEVEL=info
"@

    try {
        Set-Content -Path $envFile -Value $envContent -Encoding UTF8
        Write-Log ".env file successfully configured for Telegram integration."

        # Create ElizaOS configuration file
        $elizaConfig = @{
            version = "1.0"
            name = "EVA & GUARANI"
            description = "Telegram Bot with integrated quantum capabilities"
            telegram = @{
                token = $botToken
                polling = @{
                    timeout = 30
                    drop_pending_updates = $true
                }
            }
            clients = @("telegram")
        }

        # Create configuration directory if it doesn't exist
        $elizaConfigDir = Split-Path $elizaConfigFile -Parent
        if (-not (Test-Path $elizaConfigDir)) {
            New-Item -ItemType Directory -Path $elizaConfigDir -Force | Out-Null
        }

        $elizaConfigJson = $elizaConfig | ConvertTo-Json -Depth 10
        Set-Content -Path $elizaConfigFile -Value $elizaConfigJson -Encoding UTF8

        Write-Log "ElizaOS configuration file successfully created: $elizaConfigFile"
        return $true
    } catch {
        Write-Log "Error configuring ElizaOS for Telegram: $_" "ERROR"
        return $false
    }
}

# Create startup script for ElizaOS integrated with Telegram
function Create-StartScript {
    $startScriptPath = Join-Path $scriptPath "start_eliza_telegram.ps1"
    $startScriptBatPath = Join-Path $scriptPath "start_eliza_telegram.bat"

    $startScriptContent = @"
# EVA & GUARANI - ElizaOS Telegram Integration Starter
`$ErrorActionPreference = "Stop"

`$scriptPath = `$PSScriptRoot
`$elizaDir = Join-Path `$scriptPath "eliza"

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧" -ForegroundColor Magenta
Write-Host "Initializing ElizaOS Telegram integration" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# Check if ElizaOS directory exists
if (-not (Test-Path `$elizaDir)) {
    Write-Host "ElizaOS directory not found: `$elizaDir" -ForegroundColor Red
    Write-Host "Run the installation script first: install_eliza_integration.ps1" -ForegroundColor Red
    exit 1
}

# Start ElizaOS
Set-Location `$elizaDir
Write-Host "Starting ElizaOS..." -ForegroundColor Green
& pnpm start

# Return to the original directory
Set-Location `$scriptPath
"@

    $startScriptBatContent = @"
@echo off
echo ====================================================
echo EVA ^& GUARANI - ElizaOS Integration Starter
echo ====================================================
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0start_eliza_telegram.ps1"

echo.
echo Press any key to exit...
pause > nul
"@

    try {
        Set-Content -Path $startScriptPath -Value $startScriptContent -Encoding UTF8
        Set-Content -Path $startScriptBatPath -Value $startScriptBatContent -Encoding UTF8

        Write-Log "Startup scripts successfully created:"
        Write-Log "- $startScriptPath"
        Write-Log "- $startScriptBatPath"

        return $true
    } catch {
        Write-Log "Error creating startup scripts: $_" "ERROR"
        return $false
    }
}

# Main function
function Install-ElizaIntegration {
    Write-Log "EVA & GUARANI - ElizaOS Integration Installer"
    Write-Log "================================================"

    # Initial checks
    if (-not (Test-NodeJs)) {
        exit 1
    }

    if (-not (Test-Pnpm)) {
        exit 1
    }

    if (-not (Test-Python)) {
        exit 1
    }

    if (-not (Test-Git)) {
        exit 1
    }

    # Clone and install ElizaOS
    if (-not (Clone-ElizaRepo)) {
        exit 1
    }

    if (-not (Install-ElizaDependencies)) {
        exit 1
    }

    # Configure integration
    $telegramConfig = Get-TelegramConfig
    if (-not (Configure-ElizaForTelegram -TelegramConfig $telegramConfig)) {
        exit 1
    }

    # Create startup scripts
    if (-not (Create-StartScript)) {
        exit 1
    }

    # Success banner
    Write-Log "======================================================="
    Write-Log "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
    Write-Log "ElizaOS integration successfully installed!"
    Write-Log "To start the bot integrated with ElizaOS, run:"
    Write-Log "- start_eliza_telegram.bat"
    Write-Log "or"
    Write-Log "- ./start_eliza_telegram.ps1"
    Write-Log "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
    Write-Log "======================================================="
}

# Start installation
Install-ElizaIntegration
