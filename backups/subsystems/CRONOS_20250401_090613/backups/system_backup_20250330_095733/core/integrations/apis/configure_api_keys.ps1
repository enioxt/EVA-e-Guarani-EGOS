powershell
# EVA & GUARANI - Interactive API Key Configurator
# This script assists in the manual configuration of the necessary API keys

# Set UTF-8 encoding for the console
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

# Function to display formatted messages
function Write-LogMessage {
    param (
        [string]$Message,
        [string]$Type = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = "White"
    
    switch ($Type) {
        "SUCCESS" { $prefix = "[OK]"; $color = "Green" }
        "ERROR" { $prefix = "[ERROR]"; $color = "Red" }
        "WARNING" { $prefix = "[WARNING]"; $color = "Yellow" }
        "INFO" { $prefix = "[INFO]"; $color = "Cyan" }
        "INPUT" { $prefix = "[INPUT]"; $color = "Magenta" }
    }
    
    Write-Host "$timestamp $prefix $Message" -ForegroundColor $color
    
    # Also log to the log file
    $logDir = "logs"
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir | Out-Null
    }
    
    Add-Content -Path "$logDir\api_config.log" -Value "$timestamp $prefix $Message"
}

# Function to read API keys from the user with masking option
function Read-APIKey {
    param (
        [string]$KeyName,
        [string]$Default = "",
        [bool]$IsMasked = $true
    )
    
    Write-LogMessage "Configuring $KeyName..." -Type "INPUT"
    
    if ($Default -ne "") {
        Write-Host "  Current: " -NoNewline
        if ($IsMasked -and $Default.Length -gt 8) {
            Write-Host ($Default.Substring(0, 4) + "..." + $Default.Substring($Default.Length - 4)) -ForegroundColor DarkGray
        } else {
            Write-Host $Default -ForegroundColor DarkGray
        }
    }
    
    Write-Host "  Enter the API key for $KeyName (leave blank to keep the current value):" -ForegroundColor White
    $apiKey = Read-Host
    
    if ([string]::IsNullOrWhiteSpace($apiKey)) {
        return $Default
    }
    
    Write-LogMessage "$KeyName configured successfully" -Type "SUCCESS"
    return $apiKey
}

# Display header
Write-Host ""
Write-Host "===============================================" -ForegroundColor Magenta
Write-Host "  EVA & GUARANI - API KEY CONFIGURATOR  " -ForegroundColor Magenta
Write-Host "===============================================" -ForegroundColor Magenta
Write-Host ""
Write-LogMessage "This wizard will help you configure the necessary API keys for the bot's operation."
Write-LogMessage "The keys will be stored in secure configuration files in the 'config' directory." -Type "INFO"
Write-LogMessage "You can leave blank to keep the current values." -Type "INFO"
Write-Host ""

# Create configuration directory if necessary
$configDir = "config"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir | Out-Null
    Write-LogMessage "Configuration directory created" -Type "SUCCESS"
}

# === TELEGRAM CONFIG ===
$telegramConfigFile = "$configDir\telegram_config.json"
$telegramConfig = @{}

if (Test-Path $telegramConfigFile) {
    try {
        $telegramConfig = Get-Content $telegramConfigFile -Raw | ConvertFrom-Json -AsHashtable
        Write-LogMessage "Telegram configuration file found" -Type "SUCCESS"
    } catch {
        Write-LogMessage "Error reading Telegram configuration file: $_" -Type "ERROR"
        $telegramConfig = @{
            "bot_token" = "",
            "admin_users" = @(),
            "stable_diffusion_api" = @{
                "url" = "https://stablediffusionapi.com/api/v3/text2img",
                "key" = ""
            },
            "pexels_api" = @{
                "key" = ""
            },
            "unsplash_api" = @{
                "key" = ""
            },
            "pixabay_api" = @{
                "key" = ""
            }
        }
    }
} else {
    Write-LogMessage "Creating new configuration for Telegram" -Type "INFO"
    $telegramConfig = @{
        "bot_token" = "",
        "admin_users" = @(),
        "stable_diffusion_api" = @{
            "url" = "https://stablediffusionapi.com/api/v3/text2img",
            "key" = ""
        },
        "pexels_api" = @{
            "key" = ""
        },
        "unsplash_api" = @{
            "key" = ""
        },
        "pixabay_api" = @{
            "key" = ""
        }
    }
}

# Ask for the Telegram token
Write-Host ""
Write-Host "=== TELEGRAM CONFIGURATION ===" -ForegroundColor Blue
$telegramConfig.bot_token = Read-APIKey -KeyName "Telegram Token" -Default $telegramConfig.bot_token

# Configure admin_users if necessary
if (-not $telegramConfig.admin_users -or $telegramConfig.admin_users.Count -eq 0) {
    Write-LogMessage "Configuring admin users..." -Type "INPUT"
    Write-Host "  Enter admin user IDs separated by commas (e.g., 123456789,987654321):" -ForegroundColor White
    $adminUsers = Read-Host
    
    if (-not [string]::IsNullOrWhiteSpace($adminUsers)) {
        $telegramConfig.admin_users = $adminUsers.Split(',') | ForEach-Object { [int]$_.Trim() }
        Write-LogMessage "Admin users configured" -Type "SUCCESS"
    } else {
        Write-LogMessage "No admin user configured" -Type "WARNING"
    }
}

# Ask for the API keys for images
Write-Host ""
Write-Host "=== IMAGE API CONFIGURATION ===" -ForegroundColor Blue
$telegramConfig.stable_diffusion_api.key = Read-APIKey -KeyName "Stable Diffusion API" -Default $telegramConfig.stable_diffusion_api.key
$telegramConfig.pexels_api.key = Read-APIKey -KeyName "Pexels API" -Default $telegramConfig.pexels_api.key
$telegramConfig.unsplash_api.key = Read-APIKey -KeyName "Unsplash API" -Default $telegramConfig.unsplash_api.key
$telegramConfig.pixabay_api.key = Read-APIKey -KeyName "Pixabay API" -Default $telegramConfig.pixabay_api.key

# Save Telegram configuration
$telegramConfig | ConvertTo-Json -Depth 10 | Set-Content $telegramConfigFile -Encoding UTF8
Write-LogMessage "Telegram configuration saved in $telegramConfigFile" -Type "SUCCESS"

# === OPENAI CONFIG ===
$openaiConfigFile = "$configDir\openai_config.json"
$openaiConfig = @{}

if (Test-Path $openaiConfigFile) {
    try {
        $openaiConfig = Get-Content $openaiConfigFile -Raw | ConvertFrom-Json -AsHashtable
        Write-LogMessage "OpenAI configuration file found" -Type "SUCCESS"
    } catch {
        Write-LogMessage "Error reading OpenAI configuration file: $_" -Type "ERROR"
        $openaiConfig = @{
            "api_key" = "",
            "models" = @{
                "default" = "gpt-4o",
                "chat" = "gpt-4o",
                "creation" = "gpt-4o",
                "embedding" = "text-embedding-3-large",
                "legacy" = "gpt-3.5-turbo"
            },
            "parameters" = @{
                "temperature" = 0.7,
                "max_tokens" = 1000,
                "top_p" = 1.0,
                "frequency_penalty" = 0.0,
                "presence_penalty" = 0.0
            },
            "usage" = @{
                "track" = $true,
                "log_path" = "logs/openai_usage.log",
                "budget_limit_daily" = 10.0,
                "notify_at_percent" = 80
            },
            "proxy" = @{
                "enabled" = $false,
                "url" = "",
                "auth" = @{
                    "user" = "",
                    "password" = ""
                }
            }
        }
    }
} else {
    Write-LogMessage "Creating new configuration for OpenAI" -Type "INFO"
    $openaiConfig = @{
        "api_key" = "",
        "models" = @{
            "default" = "gpt-4o",
            "chat" = "gpt-4o",
            "creation" = "gpt-4o",
            "embedding" = "text-embedding-3-large",
            "legacy" = "gpt-3.5-turbo"
        },
        "parameters" = @{
            "temperature" = 0.7,
            "max_tokens" = 1000,
            "top_p" = 1.0,
            "frequency_penalty" = 0.0,
            "presence_penalty" = 0.0
        },
        "usage" = @{
            "track" = $true,
            "log_path" = "logs/openai_usage.log",
            "budget_limit_daily" = 10.0,
            "notify_at_percent" = 80
        },
        "proxy" = @{
            "enabled" = $false,
            "url" = "",
            "auth" = @{
                "user" = "",
                "password" = ""
            }
        }
    }
}

# Ask for the OpenAI key
Write-Host ""
Write-Host "=== OPENAI CONFIGURATION ===" -ForegroundColor Blue
$openaiConfig.api_key = Read-APIKey -KeyName "OpenAI API Key" -Default $openaiConfig.api_key

# Save OpenAI configuration
$openaiConfig | ConvertTo-Json -Depth 10 | Set-Content $openaiConfigFile -Encoding UTF8
Write-LogMessage "OpenAI configuration saved in $openaiConfigFile" -Type "SUCCESS"

# === UPDATE BOT_CONFIG.JSON ===
$botConfigFile = "$configDir\bot_config.json"
$botConfig = @{}

if (Test-Path $botConfigFile) {
    try {
        $botConfig = Get-Content $botConfigFile -Raw | ConvertFrom-Json -AsHashtable
        Write-LogMessage "Bot configuration file found" -Type "SUCCESS"
    } catch {
        Write-LogMessage "Error reading Bot configuration file: $_" -Type "ERROR"
        $botConfig = @{
            "telegram_token" = $telegramConfig.bot_token,
            "openai_api_key" = $openaiConfig.api_key,
            "allowed_users" = @(),
            "admin_users" = $telegramConfig.admin_users,
            "consciousness_level" = 0.998,
            "love_level" = 0.995,
            "max_tokens" = 1000,
            "default_model" = "gpt-4o"
        }
    }
} else {
    Write-LogMessage "Creating new general configuration for the Bot" -Type "INFO"
    $botConfig = @{
        "telegram_token" = $telegramConfig.bot_token,
        "openai_api_key" = $openaiConfig.api_key,
        "allowed_users" = @(),
        "admin_users" = $telegramConfig.admin_users,
        "consciousness_level" = 0.998,
        "love_level" = 0.995,
        "max_tokens" = 1000,
        "default_model" = "gpt-4o"
    }
}

# Update botConfig keys with the latest values
$botConfig.telegram_token = $telegramConfig.bot_token
$botConfig.openai_api_key = $openaiConfig.api_key
$botConfig.admin_users = $telegramConfig.admin_users

# Save Bot configuration
$botConfig | ConvertTo-Json -Depth 10 | Set-Content $botConfigFile -Encoding UTF8
Write-LogMessage "Bot configuration saved in $botConfigFile" -Type "SUCCESS"

# Display final message
Write-Host ""
Write-Host "===============================================" -ForegroundColor Magenta
Write-Host "  API KEY CONFIGURATION COMPLETED  " -ForegroundColor Magenta
Write-Host "===============================================" -ForegroundColor Magenta
Write-Host ""
Write-LogMessage "API keys have been configured successfully!" -Type "SUCCESS"
Write-LogMessage "You can now run the setup_and_start.ps1 script to start the bot." -Type "INFO"
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")