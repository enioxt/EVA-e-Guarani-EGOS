powershell
# EVA & GUARANI - Telegram Bot Service Script
# This script runs the Telegram bot as a background service,
# with automatic restart in case of failure.

$ErrorActionPreference = "Stop"

# Settings
$logFile = "logs\service.log"
$scriptPath = $PSScriptRoot
$botScript = "start_telegram_bot.py"
$maxRestarts = 10
$restartDelay = 30 # seconds
$restartCount = 0

# Create log directory if it doesn't exist
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
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
    Add-Content -Path $logFile -Value $logMessage
}

# Check if Python is installed
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

# Check dependencies
function Test-Dependencies {
    Write-Log "Checking dependencies..."

    try {
        & python -c "import telegram" 2>$null
        Write-Log "python-telegram-bot library found."
    } catch {
        Write-Log "Installing python-telegram-bot library..." "WARNING"
        & pip install python-telegram-bot

        if ($LASTEXITCODE -ne 0) {
            Write-Log "Failed to install python-telegram-bot. Trying with --user..." "WARNING"
            & pip install --user python-telegram-bot

            if ($LASTEXITCODE -ne 0) {
                Write-Log "Unable to install python-telegram-bot. Check your Python installation." "ERROR"
                return $false
            }
        }
    }

    return $true
}

# Check configuration file
function Test-Config {
    $configFile = Join-Path $scriptPath "config\telegram_config.json"

    if (-not (Test-Path $configFile)) {
        Write-Log "Configuration file not found: $configFile" "ERROR"
        return $false
    }

    try {
        $config = Get-Content $configFile -Raw | ConvertFrom-Json

        if ([string]::IsNullOrEmpty($config.bot_token) -or $config.bot_token -eq "YOUR_TOKEN_HERE") {
            Write-Log "Bot token not configured in $configFile" "ERROR"
            return $false
        }

        Write-Log "Configuration file successfully validated."
        return $true
    } catch {
        Write-Log "Error reading configuration file: $_" "ERROR"
        return $false
    }
}

# Check bot script
function Test-BotScript {
    $botScriptPath = Join-Path $scriptPath $botScript

    if (-not (Test-Path $botScriptPath)) {
        Write-Log "Bot script not found: $botScriptPath" "ERROR"
        return $false
    }

    Write-Log "Bot script found: $botScriptPath"
    return $true
}

# Start the bot as a background job
function Start-BotJob {
    Write-Log "Starting Telegram bot in the background..."

    $pythonPath = (Get-Command python).Path
    $botScriptPath = Join-Path $scriptPath $botScript

    # Job for background execution
    $job = Start-Job -ScriptBlock {
        param($python, $script, $workDir)

        Set-Location $workDir
        & $python $script
    } -ArgumentList $pythonPath, $botScriptPath, $scriptPath

    return $job
}

# Monitor the job and restart if necessary
function Watch-BotJob {
    param (
        [System.Management.Automation.Job]$Job
    )

    $jobId = $Job.Id
    Write-Log "Monitoring bot job (ID: $jobId)..."

    try {
        while ($true) {
            $currentJob = Get-Job -Id $jobId -ErrorAction SilentlyContinue

            # Check if the job still exists
            if ($null -eq $currentJob) {
                Write-Log "Job not found. Starting a new job..." "WARNING"
                $restartCount++

                if ($restartCount -gt $maxRestarts) {
                    Write-Log "Maximum number of restarts exceeded ($maxRestarts). Exiting." "ERROR"
                    exit 1
                }

                Write-Log "Restart $restartCount of $maxRestarts"
                Start-Sleep -Seconds $restartDelay
                $Job = Start-BotJob
                $jobId = $Job.Id
                continue
            }

            # Check job state
            $state = $currentJob.State

            switch ($state) {
                "Completed" {
                    $output = Receive-Job -Id $jobId
                    Write-Log "Job completed." "WARNING"
                    Write-Log "Job output: $output" "INFO"

                    # Restart the job
                    Write-Log "Restarting job..." "WARNING"
                    $restartCount++

                    if ($restartCount -gt $maxRestarts) {
                        Write-Log "Maximum number of restarts exceeded ($maxRestarts). Exiting." "ERROR"
                        exit 1
                    }

                    Write-Log "Restart $restartCount of $maxRestarts"
                    Start-Sleep -Seconds $restartDelay
                    $Job = Start-BotJob
                    $jobId = $Job.Id
                }
                "Failed" {
                    $errors = Receive-Job -Id $jobId -Keep
                    Write-Log "Job failed. Error: $errors" "ERROR"

                    # Restart the job
                    Write-Log "Restarting job after failure..." "WARNING"
                    $restartCount++

                    if ($restartCount -gt $maxRestarts) {
                        Write-Log "Maximum number of restarts exceeded ($maxRestarts). Exiting." "ERROR"
                        exit 1
                    }

                    Write-Log "Restart $restartCount of $maxRestarts"
                    Start-Sleep -Seconds $restartDelay
                    $Job = Start-BotJob
                    $jobId = $Job.Id
                }
                "Running" {
                    # Job is running correctly
                    Write-Log "Bot running (ID: $jobId)" "INFO"
                }
                default {
                    Write-Log "Job state: $state" "INFO"
                }
            }

            # Wait before checking again
            Start-Sleep -Seconds 60
        }
    } catch {
        Write-Log "Error monitoring job: $_" "ERROR"

        # Try to stop the job before exiting
        if ($null -ne $Job) {
            Stop-Job -Id $jobId -ErrorAction SilentlyContinue
            Remove-Job -Id $jobId -Force -ErrorAction SilentlyContinue
        }

        exit 1
    }
}

# Main function
function Start-BotService {
    Write-Log "EVA & GUARANI - Telegram Bot Service"
    Write-Log "========================================"

    # Initial checks
    if (-not (Test-Python)) {
        exit 1
    }

    if (-not (Test-Dependencies)) {
        exit 1
    }

    if (-not (Test-Config)) {
        exit 1
    }

    if (-not (Test-BotScript)) {
        exit 1
    }

    # Start the bot in the background
    $job = Start-BotJob

    # Success banner
    Write-Log "======================================================"
    Write-Log "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
    Write-Log "Telegram bot started in the background!"
    Write-Log "Job ID: $($job.Id)"
    Write-Log "Logs: $logFile"
    Write-Log "Use Ctrl+C to stop monitoring (the bot will continue running)"
    Write-Log "To stop the bot: Stop-Job -Id $($job.Id)"
    Write-Log "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
    Write-Log "======================================================"

    # Monitor the job
    Watch-BotJob -Job $job
}

# Start the service
Start-BotService
