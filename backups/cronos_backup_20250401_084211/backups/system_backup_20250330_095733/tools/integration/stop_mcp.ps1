# PowerShell script para parar o MCP no Windows 11

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
    Write-Log "Stopping MCP Service..."

    # Encontrar o processo do MCP
    $process = Get-Process python | Where-Object { $_.CommandLine -like '*mcp_server*' } | Select-Object -First 1

    if ($process) {
        Write-Log "Found MCP process with ID: $($process.Id)"

        # Parar o processo
        Stop-Process -Id $process.Id -Force
        Write-Log "MCP service stopped successfully."
    }
    else {
        Write-Log "No MCP process found running."
    }

}
catch {
    Write-Log "Error stopping MCP service: $_"
    exit 1
}
