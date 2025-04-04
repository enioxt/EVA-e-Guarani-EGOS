# PowerShell script para verificar o status do MCP no Windows 11

# Configurar o diretório do projeto
$projectRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
Set-Location $projectRoot

# Configurar arquivo de log
$logFile = Join-Path $projectRoot "logs\mcp_service.log"

# Função para registrar logs
function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "$timestamp - $Message"
    Add-Content -Path $logFile -Value $logMessage
    Write-Host $logMessage
}

try {
    Write-Log "Checking MCP Service Status..."

    # Encontrar o processo do MCP
    $process = Get-Process python | Where-Object { $_.CommandLine -like '*mcp_server*' } | Select-Object -First 1

    if ($process) {
        Write-Log "MCP Service is running:"
        Write-Log "Process ID: $($process.Id)"
        Write-Log "Start Time: $($process.StartTime)"
        Write-Log "CPU Usage: $($process.CPU) %"
        Write-Log "Memory Usage: $([math]::Round($process.WorkingSet64 / 1MB, 2)) MB"
    }
    else {
        Write-Log "MCP Service is not running."
    }

    # Verificar última linha do log
    if (Test-Path $logFile) {
        $lastLogLine = Get-Content $logFile -Tail 1
        Write-Log "Last log entry: $lastLogLine"
    }

}
catch {
    Write-Log "Error checking MCP service status: $_"
    exit 1
}
