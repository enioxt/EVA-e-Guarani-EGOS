powershell
# EVA & GUARANI - Bot Health Checker
# This script checks the health status of the EVA & GUARANI bot

# Encoding configuration to support Unicode characters
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

# Function to format log messages
function Write-LogMessage {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message,
        
        [Parameter(Mandatory = $false)]
        [ValidateSet("INFO", "SUCCESS", "ERROR", "WARNING", "CHECK")]
        [string]$Type = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $colorMap = @{
        "INFO" = "Cyan"
        "SUCCESS" = "Green"
        "ERROR" = "Red"
        "WARNING" = "Yellow"
        "CHECK" = "Magenta"
    }
    
    $color = $colorMap[$Type]
    Write-Host "[$timestamp] " -NoNewline
    Write-Host "[$Type] " -NoNewline -ForegroundColor $color
    Write-Host "$Message"
}

# Function to check if a file exists
function Test-FileExists {
    param (
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        
        [Parameter(Mandatory = $true)]
        [string]$Description
    )
    
    if (Test-Path $FilePath) {
        Write-LogMessage "✓ $Description found: $FilePath" -Type "SUCCESS"
        return $true
    } else {
        Write-LogMessage "✗ $Description not found: $FilePath" -Type "ERROR"
        return $false
    }
}

# Function to check if a process is running
function Test-ProcessRunning {
    param (
        [Parameter(Mandatory = $true)]
        [string]$ProcessName
    )
    
    $process = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue
    if ($process) {
        Write-LogMessage "✓ Process '$ProcessName' is running (PID: $($process.Id))" -Type "SUCCESS"
        return $true
    } else {
        Write-LogMessage "✗ Process '$ProcessName' is not running" -Type "WARNING"
        return $false
    }
}

# Function to check recent logs
function Test-RecentLogs {
    param (
        [Parameter(Mandatory = $true)]
        [string]$LogPath,
        
        [Parameter(Mandatory = $false)]
        [int]$MinutesThreshold = 10
    )
    
    if (Test-Path $LogPath) {
        $lastWriteTime = (Get-Item $LogPath).LastWriteTime
        $timeDiff = (Get-Date) - $lastWriteTime
        
        if ($timeDiff.TotalMinutes -le $MinutesThreshold) {
            Write-LogMessage "✓ Log updated recently ($([math]::Round($timeDiff.TotalMinutes, 2)) minutes ago)" -Type "SUCCESS"
            
            # Show the last 5 lines of the log
            Write-LogMessage "Latest log entries:" -Type "INFO"
            $lastLines = Get-Content $LogPath -Tail 5
            foreach ($line in $lastLines) {
                Write-Host "   $line" -ForegroundColor DarkGray
            }
            
            return $true
        } else {
            Write-LogMessage "✗ Log not updated recently ($([math]::Round($timeDiff.TotalMinutes, 2)) minutes ago)" -Type "WARNING"
            return $false
        }
    } else {
        Write-LogMessage "✗ Log file not found: $LogPath" -Type "ERROR"
        return $false
    }
}

# Function to check configurations
function Test-Configuration {
    param (
        [Parameter(Mandatory = $true)]
        [string]$ConfigPath,
        
        [Parameter(Mandatory = $true)]
        [string]$ConfigType,
        
        [Parameter(Mandatory = $false)]
        [string[]]$RequiredFields = @()
    )
    
    if (Test-Path $ConfigPath) {
        try {
            $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
            Write-LogMessage "✓ Valid $ConfigType configuration file" -Type "SUCCESS"
            
            $missingFields = @()
            foreach ($field in $RequiredFields) {
                if (-not ($config.PSObject.Properties.Name -contains $field) -or [string]::IsNullOrEmpty($config.$field)) {
                    $missingFields += $field
                }
            }
            
            if ($missingFields.Count -gt 0) {
                Write-LogMessage "✗ Missing or empty required fields: $($missingFields -join ', ')" -Type "WARNING"
                return $false
            }
            
            return $true
        } catch {
            Write-LogMessage "✗ Error parsing $ConfigType configuration file: $_" -Type "ERROR"
            return $false
        }
    } else {
        Write-LogMessage "✗ $ConfigType configuration file not found: $ConfigPath" -Type "ERROR"
        return $false
    }
}

# Function to check Python dependencies
function Test-PythonDependencies {
    param (
        [Parameter(Mandatory = $true)]
        [string]$RequirementsPath
    )
    
    if (Test-Path $RequirementsPath) {
        Write-LogMessage "Checking Python dependencies..." -Type "CHECK"
        
        $requirements = Get-Content $RequirementsPath
        $missingPackages = @()
        
        foreach ($req in $requirements) {
            if (-not [string]::IsNullOrWhiteSpace($req) -and -not $req.StartsWith("#")) {
                $packageInfo = $req -split "=="
                $packageName = $packageInfo[0].Trim()
                
                $checkCommand = "python -c `"import $packageName; print('OK')`" 2>&1"
                $result = Invoke-Expression $checkCommand
                
                if ($result -ne "OK") {
                    $missingPackages += $packageName
                }
            }
        }
        
        if ($missingPackages.Count -gt 0) {
            Write-LogMessage "✗ Missing Python dependencies: $($missingPackages -join ', ')" -Type "WARNING"
            return $false
        } else {
            Write-LogMessage "✓ All Python dependencies are installed" -Type "SUCCESS"
            return $true
        }
    } else {
        Write-LogMessage "✗ Requirements file not found: $RequirementsPath" -Type "ERROR"
        return $false
    }
}

# Function to check connectivity with external APIs
function Test-APIConnectivity {
    param (
        [Parameter(Mandatory = $true)]
        [string]$APIName,
        
        [Parameter(Mandatory = $true)]
        [string]$APIURL
    )
    
    try {
        $response = Invoke-WebRequest -Uri $APIURL -Method Head -TimeoutSec 10 -ErrorAction Stop
        Write-LogMessage "✓ Connectivity with $APIName API OK (Status: $($response.StatusCode))" -Type "SUCCESS"
        return $true
    } catch {
        Write-LogMessage "✗ Connectivity failure with $APIName API: $_" -Type "WARNING"
        return $false
    }
}

# Function to check disk space
function Test-DiskSpace {
    param (
        [Parameter(Mandatory = $false)]
        [int]$MinimumFreeSpaceGB = 1
    )
    
    $drive = Get-PSDrive -Name (Get-Location).Drive.Name
    $freeSpaceGB = [math]::Round($drive.Free / 1GB, 2)
    
    if ($freeSpaceGB -ge $MinimumFreeSpaceGB) {
        Write-LogMessage "✓ Sufficient disk space: $freeSpaceGB GB free" -Type "SUCCESS"
        return $true
    } else {
        Write-LogMessage "✗ Insufficient disk space: $freeSpaceGB GB free (minimum recommended: $MinimumFreeSpaceGB GB)" -Type "WARNING"
        return $false
    }
}

# Function to check Python version
function Test-PythonVersion {
    param (
        [Parameter(Mandatory = $false)]
        [version]$MinimumVersion = "3.8.0"
    )
    
    try {
        $versionOutput = python --version 2>&1
        if ($versionOutput -match "Python (\d+\.\d+\.\d+)") {
            $currentVersion = [version]$Matches[1]
            
            if ($currentVersion -ge $MinimumVersion) {
                Write-LogMessage "✓ Suitable Python version: $currentVersion" -Type "SUCCESS"
                return $true
            } else {
                Write-LogMessage "✗ Unsuitable Python version: $currentVersion (minimum recommended: $MinimumVersion)" -Type "WARNING"
                return $false
            }
        } else {
            Write-LogMessage "✗ Unable to determine Python version" -Type "ERROR"
            return $false
        }
    } catch {
        Write-LogMessage "✗ Python not found or error checking version: $_" -Type "ERROR"
        return $false
    }
}

# Function to generate health report
function Get-HealthReport {
    param (
        [Parameter(Mandatory = $true)]
        [hashtable]$CheckResults
    )
    
    $totalChecks = $CheckResults.Count
    $passedChecks = ($CheckResults.Values | Where-Object { $_ -eq $true }).Count
    $healthPercentage = [math]::Round(($passedChecks / $totalChecks) * 100, 2)
    
    Write-LogMessage "EVA & GUARANI Bot Health Report" -Type "INFO"
    Write-LogMessage "Total checks: $totalChecks" -Type "INFO"
    Write-LogMessage "Successful checks: $passedChecks" -Type "INFO"
    Write-LogMessage "Overall health: $healthPercentage%" -Type "INFO"
    
    if ($healthPercentage -ge 90) {
        Write-LogMessage "✓ Health status: EXCELLENT" -Type "SUCCESS"
    } elseif ($healthPercentage -ge 75) {
        Write-LogMessage "✓ Health status: GOOD" -Type "SUCCESS"
    } elseif ($healthPercentage -ge 50) {
        Write-LogMessage "⚠ Health status: FAIR" -Type "WARNING"
    } else {
        Write-LogMessage "✗ Health status: CRITICAL" -Type "ERROR"
    }
    
    return @{
        TotalChecks = $totalChecks
        PassedChecks = $passedChecks
        HealthPercentage = $healthPercentage
    }
}

# Function to suggest corrective actions
function Get-CorrectiveActions {
    param (
        [Parameter(Mandatory = $true)]
        [hashtable]$CheckResults
    )
    
    $actions = @()
    
    if (-not $CheckResults["ConfigTelegram"]) {
        $actions += "Check the Telegram configuration file (config/telegram_config.json)"
    }
    
    if (-not $CheckResults["ConfigOpenAI"]) {
        $actions += "Check the OpenAI configuration file (config/openai_config.json)"
    }
    
    if (-not $CheckResults["BotProcess"]) {
        $actions += "Restart the bot using the command: .\setup_and_start.ps1"
    }
    
    if (-not $CheckResults["RecentLogs"]) {
        $actions += "Check the logs for possible errors: logs/bot.log"
    }
    
    if (-not $CheckResults["PythonDependencies"]) {
        $actions += "Reinstall dependencies: pip install -r requirements.txt"
    }
    
    if (-not $CheckResults["PythonVersion"]) {
        $actions += "Upgrade Python to version 3.8.0 or higher"
    }
    
    if (-not $CheckResults["DiskSpace"]) {
        $actions += "Free up disk space to ensure proper bot operation"
    }
    
    if ($actions.Count -gt 0) {
        Write-LogMessage "Recommended corrective actions:" -Type "INFO"
        foreach ($action in $actions) {
            Write-Host "  • $action" -ForegroundColor Yellow
        }
    } else {
        Write-LogMessage "✓ No corrective actions needed" -Type "SUCCESS"
    }
    
    return $actions
}

# Header
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║  EVA & GUARANI - Bot Health Checker                          ║" -ForegroundColor Cyan
Write-Host "║  Version 1.0                                                 ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Start checks
Write-LogMessage "Starting health check for EVA & GUARANI bot..." -Type "INFO"

# Store check results
$checkResults = @{}

# Check essential files
Write-LogMessage "Checking essential files..." -Type "CHECK"
$checkResults["MainPyFile"] = Test-FileExists -FilePath "bot\unified_telegram_bot_utf8.py" -Description "Main bot file"
$checkResults["QuantumMaster"] = Test-FileExists -FilePath "quantum\quantum_master.py" -Description "Main quantum module"
$checkResults["Requirements"] = Test-FileExists -FilePath "requirements.txt" -Description "Requirements file"

# Check configuration files
Write-LogMessage "Checking configuration files..." -Type "CHECK"
$checkResults["ConfigTelegram"] = Test-Configuration -ConfigPath "config\telegram_config.json" -ConfigType "Telegram" -RequiredFields @("bot_token")
$checkResults["ConfigOpenAI"] = Test-Configuration -ConfigPath "config\openai_config.json" -ConfigType "OpenAI" -RequiredFields @("api_key")
$checkResults["ConfigBot"] = Test-Configuration -ConfigPath "config\bot_config.json" -ConfigType "Bot" -RequiredFields @()

# Check processes
Write-LogMessage "Checking processes..." -Type "CHECK"
$checkResults["BotProcess"] = Test-ProcessRunning -ProcessName "python"

# Check logs
Write-LogMessage "Checking logs..." -Type "CHECK"
$checkResults["RecentLogs"] = Test-RecentLogs -LogPath "logs\bot.log" -MinutesThreshold 30

# Check Python dependencies
$checkResults["PythonDependencies"] = Test-PythonDependencies -RequirementsPath "requirements.txt"

# Check Python version
$checkResults["PythonVersion"] = Test-PythonVersion -MinimumVersion "3.8.0"

# Check disk space
$checkResults["DiskSpace"] = Test-DiskSpace -MinimumFreeSpaceGB 1

# Check connectivity with APIs (if configured)
Write-LogMessage "Checking connectivity with APIs..." -Type "CHECK"
$checkResults["TelegramAPI"] = Test-APIConnectivity -APIName "Telegram" -APIURL "https://api.telegram.org"
$checkResults["OpenAIAPI"] = Test-APIConnectivity -APIName "OpenAI" -APIURL "https://api.openai.com"

# Generate health report
$healthReport = Get-HealthReport -CheckResults $checkResults

# Suggest corrective actions
$correctiveActions = Get-CorrectiveActions -CheckResults $checkResults

# Save report to file
$reportPath = "logs\health_check_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
$reportContent = @"
EVA & GUARANI - Bot Health Report
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Overall Health: $($healthReport.HealthPercentage)%
Total Checks: $($healthReport.TotalChecks)
Successful Checks: $($healthReport.PassedChecks)

Check Details:
$(($checkResults.GetEnumerator() | ForEach-Object { "- $($_.Key): $(if($_.Value){'✓ Passed'}else{'✗ Failed'})" }) -join "`n")

$(if($correctiveActions.Count -gt 0){"Recommended Corrective Actions:`n$(($correctiveActions | ForEach-Object { "- $_" }) -join "`n")"}else{"No corrective actions needed"})

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"@

New-Item -Path "logs" -ItemType Directory -Force | Out-Null
$reportContent | Out-File -FilePath $reportPath -Encoding utf8

Write-LogMessage "Health report saved to: $reportPath" -Type "INFO"

# Footer
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║  Health check completed                                      ║" -ForegroundColor Cyan
Write-Host "║  Overall health: $($healthReport.HealthPercentage)%                                       ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧" -ForegroundColor Magenta