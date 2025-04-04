# EVA & GUARANI - Register Mycelium Health Check Task
# Version: 1.0
# Last Updated: 2025-03-30

$ErrorActionPreference = "Stop"

# Task configuration
$taskName = "EVA_GUARANI_MyceliumHealthCheck"
$taskDescription = "Performs regular health checks on the Mycelium network connections"
$scriptPath = "C:\Eva Guarani EGOS\QUANTUM_PROMPTS\MASTER\check_mycelium_health.ps1"
$logPath = "C:\Eva Guarani EGOS\QUANTUM_PROMPTS\MASTER\logs\task_registration.log"

# Ensure the script exists
if (-not (Test-Path $scriptPath)) {
    Write-Error "Health check script not found at: $scriptPath"
    exit 1
}

# Create the task action
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

# Create the task trigger (run every 5 minutes)
$trigger = New-ScheduledTaskTrigger -Daily -At (Get-Date) -DaysInterval 1
$trigger.Repetition = @{
    Duration = 'P1D';
    Interval = 'PT5M'
}

# Set task settings
$settings = New-ScheduledTaskSettingsSet `
    -MultipleInstances IgnoreNew `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Register the task
try {
    # Remove existing task if it exists
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

    # Register new task
    Register-ScheduledTask `
        -TaskName $taskName `
        -Description $taskDescription `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -User "System"

    Write-Output "Successfully registered Mycelium health check task"

    # Log the registration
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] Successfully registered task: $taskName"
    Add-Content -Path $logPath -Value $logMessage
}
catch {
    Write-Error "Failed to register task: $_"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] ERROR: Failed to register task: $_"
    Add-Content -Path $logPath -Value $logMessage
    exit 1
}
