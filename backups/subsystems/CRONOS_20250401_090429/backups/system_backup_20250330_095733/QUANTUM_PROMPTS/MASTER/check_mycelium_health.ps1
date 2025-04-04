# EVA & GUARANI - Mycelium Network Health Check Script
# Version: 1.0
# Last Updated: 2025-03-30

$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

# Configuration
$CONFIG = @{
    MasterStatePath     = "C:/Eva Guarani EGOS/QUANTUM_PROMPTS/MASTER/master_state.json"
    LogPath             = "C:/Eva Guarani EGOS/QUANTUM_PROMPTS/MASTER/logs/mycelium_health.log"
    HealthCheckInterval = 300  # 5 minutes in seconds
    MaxRetries          = 3
    ConnectionTimeout   = 30  # seconds
}

# Ensure log directory exists
$LogDir = Split-Path $CONFIG.LogPath -Parent
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

function Write-HealthLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )

    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$Timestamp][$Level] $Message"
    Add-Content -Path $CONFIG.LogPath -Value $LogMessage
    Write-Verbose $LogMessage
}

function Test-MyceliumConnection {
    param(
        [string]$Component
    )

    try {
        # Simulate connection test (replace with actual connection logic)
        $result = $true
        switch ($Component) {
            "ETHIK Core" {
                $result = Test-Path "C:/Eva Guarani EGOS/QUANTUM_PROMPTS/ETHIK/ethik_core.js"
            }
            "SLOP Server" {
                $result = Test-Path "C:/Eva Guarani EGOS/QUANTUM_PROMPTS/MASTER/slop"
            }
            "AVA Core" {
                $result = Test-Path "C:/Eva Guarani EGOS/QUANTUM_PROMPTS/MASTER/mcp"
            }
            "PDD Manager" {
                $result = Test-Path "C:/Eva Guarani EGOS/QUANTUM_PROMPTS/MASTER/pdd.js"
            }
            "Quantum Context" {
                $result = Test-Path "C:/Eva Guarani EGOS/QUANTUM_PROMPTS/MASTER/quantum_context.md"
            }
        }

        return $result
    }
    catch {
        Write-HealthLog "Error testing connection to $Component: $_" -Level "ERROR"
        return $false
    }
}

function Update-MasterState {
    param(
        [hashtable]$HealthStatus
    )

    try {
        $masterState = Get-Content $CONFIG.MasterStatePath | ConvertFrom-Json -AsHashtable
        $masterState.network.mycelium.status = $HealthStatus.overall_status
        $masterState.network.mycelium.last_check = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        $masterState.network.mycelium.connection_status = $HealthStatus.connections

        $masterState | ConvertTo-Json -Depth 10 | Set-Content $CONFIG.MasterStatePath
        Write-HealthLog "Master state updated successfully"
    }
    catch {
        Write-HealthLog "Error updating master state: $_" -Level "ERROR"
    }
}

function Start-HealthCheck {
    Write-HealthLog "Starting Mycelium network health check"

    $healthStatus = @{
        overall_status = "UNKNOWN"
        connections    = @{}
        timestamp      = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    }

    # Test each connection
    $masterState = Get-Content $CONFIG.MasterStatePath | ConvertFrom-Json
    $connections = $masterState.network.mycelium.connections

    $allConnected = $true
    foreach ($connection in $connections) {
        $connectionStatus = Test-MyceliumConnection -Component $connection
        $healthStatus.connections[$connection] = if ($connectionStatus) { "CONNECTED" } else { "DISCONNECTED" }
        if (-not $connectionStatus) {
            $allConnected = $false
        }
    }

    $healthStatus.overall_status = if ($allConnected) { "CONNECTED" } else { "DEGRADED" }

    # Update master state with health check results
    Update-MasterState -HealthStatus $healthStatus

    # Log results
    Write-HealthLog "Health check completed. Overall status: $($healthStatus.overall_status)"
    foreach ($conn in $healthStatus.connections.GetEnumerator()) {
        Write-HealthLog "Connection status - $($conn.Key): $($conn.Value)"
    }
}

# Main execution loop
Write-HealthLog "Mycelium health check service started"

while ($true) {
    try {
        Start-HealthCheck
    }
    catch {
        Write-HealthLog "Error in health check cycle: $_" -Level "ERROR"
    }

    Start-Sleep -Seconds $CONFIG.HealthCheckInterval
}
