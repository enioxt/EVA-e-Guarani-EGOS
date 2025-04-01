powershell
# EVA & GUARANI - Update Script
# This script updates the EVA & GUARANI bot to the latest version

# Encoding configuration to support special characters
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Function to display log messages with formatting and colors
function Write-LogMessage {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message,
        
        [Parameter(Mandatory = $false)]
        [ValidateSet("INFO", "SUCCESS", "ERROR", "WARNING", "UPDATE")]
        [string]$Type = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    # Define colors for different message types
    switch ($Type) {
        "INFO"    { $color = "Cyan"; $prefix = "i" }
        "SUCCESS" { $color = "Green"; $prefix = "+" }
        "ERROR"   { $color = "Red"; $prefix = "x" }
        "WARNING" { $color = "Yellow"; $prefix = "!" }
        "UPDATE"  { $color = "Magenta"; $prefix = "*" }
    }
    
    # Display formatted message
    Write-Host "[$timestamp] " -NoNewline
    Write-Host "[$Type] " -ForegroundColor $color -NoNewline
    Write-Host "$prefix $Message"
}

# Function to create backup of configuration files
function Backup-ConfigFiles {
    $backupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    
    Write-LogMessage "Creating backup directory: $backupDir" -Type "INFO"
    
    if (-not (Test-Path $backupDir)) {
        New-Item -ItemType Directory -Path $backupDir | Out-Null
        Write-LogMessage "Backup directory created successfully" -Type "SUCCESS"
    }
    
    # Backup configuration files
    if (Test-Path "config") {
        Write-LogMessage "Backing up configuration files" -Type "INFO"
        Copy-Item -Path "config" -Destination "$backupDir\config" -Recurse -Force
        Write-LogMessage "Configuration files backup completed" -Type "SUCCESS"
    } else {
        Write-LogMessage "Configuration directory not found. No backup necessary." -Type "WARNING"
    }
    
    # Backup logs
    if (Test-Path "logs") {
        Write-LogMessage "Backing up logs" -Type "INFO"
        Copy-Item -Path "logs" -Destination "$backupDir\logs" -Recurse -Force
        Write-LogMessage "Logs backup completed" -Type "SUCCESS"
    }
    
    # Backup data
    if (Test-Path "data") {
        Write-LogMessage "Backing up data" -Type "INFO"
        Copy-Item -Path "data" -Destination "$backupDir\data" -Recurse -Force
        Write-LogMessage "Data backup completed" -Type "SUCCESS"
    }
    
    return $backupDir
}

# Function to check if Git is installed
function Test-GitInstalled {
    try {
        $gitVersion = git --version
        Write-LogMessage "Git found: $gitVersion" -Type "SUCCESS"
        return $true
    } catch {
        Write-LogMessage "Git not found. Please install Git to continue." -Type "ERROR"
        Write-LogMessage "You can download Git at: https://git-scm.com/downloads" -Type "INFO"
        return $false
    }
}

# Function to check if Python is installed
function Test-PythonInstalled {
    try {
        $pythonVersion = python --version
        Write-LogMessage "Python found: $pythonVersion" -Type "SUCCESS"
        return $true
    } catch {
        Write-LogMessage "Python not found. Please install Python to continue." -Type "ERROR"
        Write-LogMessage "You can download Python at: https://www.python.org/downloads/" -Type "INFO"
        return $false
    }
}

# Function to update the repository
function Update-Repository {
    Write-LogMessage "Checking repository updates" -Type "UPDATE"
    
    # Check if .git directory exists
    if (-not (Test-Path ".git")) {
        Write-LogMessage "This does not appear to be a valid Git repository." -Type "ERROR"
        Write-LogMessage "Automatic update is not possible. Please download the latest version manually." -Type "INFO"
        return $false
    }
    
    # Save the current version before updating
    $currentVersion = git rev-parse HEAD
    Write-LogMessage "Current version: $currentVersion" -Type "INFO"
    
    # Check for uncommitted local changes
    $status = git status --porcelain
    if ($status) {
        Write-LogMessage "There are uncommitted local changes:" -Type "WARNING"
        git status
        
        $confirmation = Read-Host "Do you want to continue anyway? Local changes will be preserved. (Y/N)"
        if ($confirmation -ne "Y") {
            Write-LogMessage "Update canceled by user." -Type "INFO"
            return $false
        }
    }
    
    # Update the repository
    try {
        Write-LogMessage "Fetching remote updates..." -Type "UPDATE"
        git fetch
        
        # Check if updates are available
        $localRef = git rev-parse HEAD
        $remoteRef = git rev-parse origin/main
        
        if ($localRef -eq $remoteRef) {
            Write-LogMessage "The bot is already at the latest version." -Type "SUCCESS"
            return $true
        }
        
        Write-LogMessage "Updating to the latest version..." -Type "UPDATE"
        git pull
        
        # Check if the update was successful
        if ($LASTEXITCODE -eq 0) {
            $newVersion = git rev-parse HEAD
            Write-LogMessage "Update completed successfully!" -Type "SUCCESS"
            Write-LogMessage "New version: $newVersion" -Type "INFO"
            
            # Display change log
            Write-LogMessage "Changes since the previous version:" -Type "INFO"
            git log --pretty=format:"%h - %s (%cr)" $currentVersion..$newVersion
            
            return $true
        } else {
            Write-LogMessage "Failed to update the repository." -Type "ERROR"
            return $false
        }
    } catch {
        Write-LogMessage "Error updating the repository: $_" -Type "ERROR"
        return $false
    }
}

# Function to update dependencies
function Update-Dependencies {
    Write-LogMessage "Updating dependencies..." -Type "UPDATE"
    
    if (Test-Path "requirements.txt") {
        try {
            python -m pip install --upgrade pip
            python -m pip install -r requirements.txt --upgrade
            Write-LogMessage "Dependencies updated successfully!" -Type "SUCCESS"
            return $true
        } catch {
            Write-LogMessage "Error updating dependencies: $_" -Type "ERROR"
            return $false
        }
    } else {
        Write-LogMessage "requirements.txt file not found." -Type "ERROR"
        return $false
    }
}

# Function to restore backup in case of failure
function Restore-Backup {
    param (
        [Parameter(Mandatory = $true)]
        [string]$BackupDir
    )
    
    Write-LogMessage "Restoring backup from $BackupDir..." -Type "WARNING"
    
    # Restore configurations
    if (Test-Path "$BackupDir\config") {
        Copy-Item -Path "$BackupDir\config" -Destination "." -Recurse -Force
        Write-LogMessage "Configurations restored successfully" -Type "SUCCESS"
    }
    
    # Restore logs
    if (Test-Path "$BackupDir\logs") {
        Copy-Item -Path "$BackupDir\logs" -Destination "." -Recurse -Force
        Write-LogMessage "Logs restored successfully" -Type "SUCCESS"
    }
    
    # Restore data
    if (Test-Path "$BackupDir\data") {
        Copy-Item -Path "$BackupDir\data" -Destination "." -Recurse -Force
        Write-LogMessage "Data restored successfully" -Type "SUCCESS"
    }
    
    Write-LogMessage "Restoration completed" -Type "SUCCESS"
}

# Function to check bot health after update
function Test-BotHealth {
    Write-LogMessage "Checking bot health after update..." -Type "INFO"
    
    if (Test-Path "check_bot_health.ps1") {
        try {
            & .\check_bot_health.ps1
            return $true
        } catch {
            Write-LogMessage "Error checking bot health: $_" -Type "ERROR"
            return $false
        }
    } else {
        Write-LogMessage "Health check script not found." -Type "WARNING"
        return $true  # Consider success if the script does not exist
    }
}

# Main function
function Update-Bot {
    # Display header
    Write-Host ""
    Write-Host "+--------------------------------------------------------------+" -ForegroundColor Cyan
    Write-Host "|                                                              |" -ForegroundColor Cyan
    Write-Host "|  EVA & GUARANI - Bot Update                                  |" -ForegroundColor Cyan
    Write-Host "|  Version 1.0                                                 |" -ForegroundColor Cyan
    Write-Host "|                                                              |" -ForegroundColor Cyan
    Write-Host "+--------------------------------------------------------------+" -ForegroundColor Cyan
    Write-Host ""
    
    Write-LogMessage "Starting EVA & GUARANI bot update process..." -Type "INFO"
    
    # Check prerequisites
    $gitInstalled = Test-GitInstalled
    $pythonInstalled = Test-PythonInstalled
    
    if (-not $gitInstalled -or -not $pythonInstalled) {
        Write-LogMessage "Prerequisites not met. Update canceled." -Type "ERROR"
        return
    }
    
    # Create backup
    $backupDir = Backup-ConfigFiles
    Write-LogMessage "Backup created at: $backupDir" -Type "SUCCESS"
    
    # Update repository
    $repoUpdated = Update-Repository
    
    if ($repoUpdated) {
        # Update dependencies
        $depsUpdated = Update-Dependencies
        
        if ($depsUpdated) {
            # Check bot health
            $healthOk = Test-BotHealth
            
            if ($healthOk) {
                Write-LogMessage "Update completed successfully!" -Type "SUCCESS"
                Write-LogMessage "The EVA & GUARANI bot has been updated to the latest version." -Type "SUCCESS"
                Write-LogMessage "To start the bot, run: .\setup_and_start.ps1" -Type "INFO"
            } else {
                Write-LogMessage "Problems detected after the update." -Type "WARNING"
                $restore = Read-Host "Do you want to restore the backup? (Y/N)"
                
                if ($restore -eq "Y") {
                    Restore-Backup -BackupDir $backupDir
                }
            }
        } else {
            Write-LogMessage "Failed to update dependencies." -Type "ERROR"
            $restore = Read-Host "Do you want to restore the backup? (Y/N)"
            
            if ($restore -eq "Y") {
                Restore-Backup -BackupDir $backupDir
            }
        }
    } else {
        Write-LogMessage "Update canceled or failed." -Type "WARNING"
    }
    
    # Footer
    Write-Host ""
    Write-Host "+--------------------------------------------------------------+" -ForegroundColor Cyan
    Write-Host "|                                                              |" -ForegroundColor Cyan
    Write-Host "|  Update process completed                                    |" -ForegroundColor Cyan
    Write-Host "|                                                              |" -ForegroundColor Cyan
    Write-Host "+--------------------------------------------------------------+" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "*** EVA & GUARANI ***" -ForegroundColor Magenta
    Write-Host ""
}

# Execute the main function
Update-Bot

# Wait for user input before closing
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")