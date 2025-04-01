# Script para iniciar o MCP Server com logging detalhado
$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

# Definir diretório raiz do projeto
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$logDir = Join-Path $projectRoot "logs"
$logFile = Join-Path $logDir "mcp_startup.log"
$errorLogFile = Join-Path $logDir "mcp_error.log"
$pidFile = Join-Path $logDir "mcp_server.pid"
$configFile = Join-Path $PSScriptRoot "mcp.json"
$serverLogFile = Join-Path $logDir "mcp_server.log"
$heartbeatFile = Join-Path $logDir "mcp_heartbeat.txt"

# Criar diretório de logs se não existir
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

# Função para logging com timestamp e colorização
function Write-Log {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    # Escrever no arquivo de log
    Add-Content -Path $logFile -Value $logMessage -Encoding UTF8
    
    # Escrever no console com cores
    switch ($Level) {
        "ERROR" { Write-Host $logMessage -ForegroundColor Red }
        "WARN" { Write-Host $logMessage -ForegroundColor Yellow }
        "INFO" { Write-Host $logMessage -ForegroundColor Green }
        "DEBUG" { Write-Host $logMessage -ForegroundColor Gray }
        default { Write-Host $logMessage }
    }
}

# Função para verificar se o servidor já está rodando
function Test-ServerRunning {
    if (Test-Path $pidFile) {
        $processId = Get-Content $pidFile
        try {
            $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
            if ($process) {
                # Verificar também o heartbeat para confirmar que o servidor está respondendo
                if (Test-Path $heartbeatFile) {
                    $lastHeartbeat = Get-Item $heartbeatFile
                    $timeSinceLastHeartbeat = (Get-Date) - $lastHeartbeat.LastWriteTime
                    
                    if ($timeSinceLastHeartbeat.TotalMinutes -lt 2) {
                        Write-Log "Processo MCP encontrado com PID: $processId e heartbeat recente" -Level "DEBUG"
                        return $true
                    }
                    else {
                        Write-Log "Processo MCP encontrado com PID: $processId, mas heartbeat desatualizado" -Level "WARN"
                        return $false
                    }
                }
                
                Write-Log "Processo MCP encontrado com PID: $processId" -Level "DEBUG"
                return $true
            }
        }
        catch {
            Write-Log "Erro ao verificar processo ${processId}: ${_}" -Level "DEBUG"
            Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
        }
    }
    return $false
}

# Função para matar processos anteriores do MCP
function Stop-MCPProcesses {
    Write-Log "Procurando por processos MCP anteriores..." -Level "INFO"
    
    # Procurar por processos Python rodando o mcp_server
    $mcpProcesses = Get-WmiObject Win32_Process | Where-Object {
        $_.CommandLine -like "*python*" -and $_.CommandLine -like "*mcp_server*"
    }
    
    if ($mcpProcesses) {
        Write-Log "Encontrados $($mcpProcesses.Count) processos MCP anteriores" -Level "WARN"
        foreach ($proc in $mcpProcesses) {
            try {
                Write-Log "Finalizando processo MCP $($proc.ProcessId) com comando: $($proc.CommandLine)" -Level "DEBUG"
                Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
                Write-Log "Processo MCP $($proc.ProcessId) finalizado" -Level "INFO"
            }
            catch {
                Write-Log "Erro ao finalizar processo MCP $($proc.ProcessId): $_" -Level "ERROR"
            }
        }
    }
    else {
        Write-Log "Nenhum processo MCP anterior encontrado" -Level "INFO"
    }
    
    # Limpar arquivo PID se existir
    if (Test-Path $pidFile) {
        Remove-Item $pidFile -Force
        Write-Log "Arquivo PID removido" -Level "INFO"
    }
    
    # Limpar arquivo de heartbeat se existir
    if (Test-Path $heartbeatFile) {
        Remove-Item $heartbeatFile -Force -ErrorAction SilentlyContinue
        Write-Log "Arquivo de heartbeat removido" -Level "INFO"
    }
}

# Função para verificar logs do servidor
function Check-ServerLogs {
    param (
        [int]$Lines = 10
    )
    
    if (Test-Path $serverLogFile) {
        $lastLines = Get-Content $serverLogFile -Tail $Lines -ErrorAction SilentlyContinue
        if ($lastLines) {
            Write-Log "Últimas $Lines linhas do log do servidor:" -Level "DEBUG"
            foreach ($line in $lastLines) {
                Write-Log "  $line" -Level "DEBUG"
            }
        }
        else {
            Write-Log "Arquivo de log do servidor está vazio ou não foi possível ler" -Level "WARN"
        }
    }
    else {
        Write-Log "Arquivo de log do servidor não encontrado" -Level "WARN"
    }
}

# Função para verificar dependências
function Test-Dependencies {
    try {
        $pythonVersion = python --version
        Write-Log "Python encontrado: $pythonVersion" -Level "INFO"
        
        # Verificar se o websockets está instalado
        $hasWebsockets = python -c "import websockets; print('OK')" 2>$null
        if ($hasWebsockets -ne "OK") {
            Write-Log "Módulo websockets não encontrado. Será instalado." -Level "WARN"
            return $false
        }
        
        Write-Log "Todas as dependências Python encontradas" -Level "INFO"
        return $true
    }
    catch {
        Write-Log "Erro ao verificar dependências: $_" -Level "ERROR"
        return $false
    }
}

# Função para instalar dependências Python
function Install-PythonDependencies {
    Write-Log "Instalando dependências Python..." -Level "INFO"
    
    $required_packages = @(
        "websockets",
        "python-dotenv",
        "aiohttp",
        "psutil"
    )
    
    foreach ($package in $required_packages) {
        Write-Log "Instalando $package..." -Level "DEBUG"
        # Usar o pip do ambiente virtual
        $result = & $pythonPath -m pip install --no-cache-dir $package 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Log "Erro ao instalar ${package}: ${result}" -Level "ERROR"
            return $false
        }
        Write-Log "Pacote $package instalado com sucesso" -Level "DEBUG"
    }
    
    Write-Log "Todas as dependências instaladas com sucesso" -Level "INFO"
    return $true
}

# Função para monitorar o heartbeat do servidor
function Update-ServerHeartbeat {
    param (
        [Parameter(Mandatory = $true)]
        [int]$ProcessId
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $heartbeatContent = "$timestamp|$ProcessId"
    $heartbeatContent | Out-File -FilePath $heartbeatFile -Force -Encoding UTF8
}

try {
    # Parar processos anteriores
    Stop-MCPProcesses
    
    Write-Log "Iniciando processo de setup do MCP Server..." -Level "INFO"
    Write-Log "Diretório do projeto: $projectRoot" -Level "INFO"
    
    # Verificar se Python está instalado
    try {
        $pythonVersion = python --version
        Write-Log "Python encontrado: $pythonVersion" -Level "INFO"
    }
    catch {
        Write-Log "Python não encontrado no PATH" -Level "ERROR"
        throw "Python não está instalado ou não está no PATH"
    }
    
    # Verificar ambiente virtual
    $venvPath = Join-Path $projectRoot "venv"
    $venvScripts = Join-Path $venvPath "Scripts"
    $venvActivate = Join-Path $venvScripts "Activate.ps1"
    
    if (Test-Path $venvActivate) {
        Write-Log "Ativando ambiente virtual em $venvPath" -Level "INFO"
        & $venvActivate
    }
    else {
        Write-Log "Criando novo ambiente virtual em $venvPath" -Level "INFO"
        python -m venv $venvPath
        & $venvActivate
    }
    
    # Verificar e instalar dependências
    if (-not (Test-Dependencies)) {
        Write-Log "Instalando dependências faltantes..." -Level "INFO"
        if (-not (Install-PythonDependencies)) {
            Write-Log "Falha ao instalar dependências. Abortando." -Level "ERROR"
            throw "Falha ao instalar dependências Python"
        }
    }
    
    # Iniciar o servidor MCP
    Write-Log "Iniciando MCP Server..." -Level "INFO"
    
    # Limpar arquivos de log antigos se muito grandes
    if ((Test-Path $serverLogFile) -and ((Get-Item $serverLogFile).Length -gt 10MB)) {
        Write-Log "Arquivo de log do servidor muito grande. Criando backup e iniciando novo." -Level "WARN"
        $backupFile = "$serverLogFile.$(Get-Date -Format 'yyyyMMdd_HHmmss').bak"
        Move-Item -Path $serverLogFile -Destination $backupFile -Force
        Write-Log "Backup do log salvo em: $backupFile" -Level "INFO"
    }
    
    # Iniciar o servidor em uma nova janela do PowerShell para melhor isolamento
    # e evitar problemas com o redirecionamento de saída
    $pythonPath = (Get-Command python).Path
    $serverScript = "tools.integration.mcp_server"
    
    Write-Log "Configuração do processo:" -Level "DEBUG"
    Write-Log "  Python: $pythonPath" -Level "DEBUG"
    Write-Log "  Script: $serverScript" -Level "DEBUG"
    Write-Log "  WorkingDirectory: $projectRoot" -Level "DEBUG"
    
    # Iniciar o processo Python
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $pythonPath
    $psi.Arguments = "-m $serverScript"
    $psi.WorkingDirectory = $projectRoot
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true

    # Adicionar PYTHONPATH para garantir que o módulo seja encontrado
    $psi.EnvironmentVariables["PYTHONPATH"] = $projectRoot

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    $process.EnableRaisingEvents = $true

    # Iniciar o processo
    $result = $process.Start()

    if (-not $result) {
        Write-Log "Falha ao iniciar o processo MCP" -Level "ERROR"
        throw "Não foi possível iniciar o processo MCP"
    }

    # Salvar PID
    $process.Id | Set-Content $pidFile -Encoding UTF8

    Write-Log "MCP Server iniciado com PID: $($process.Id)" -Level "INFO"
    Write-Log "Logs disponíveis em:" -Level "INFO"
    Write-Log "  - Startup: $logFile" -Level "INFO"
    Write-Log "  - Server: $serverLogFile" -Level "INFO"
    Write-Log "  - Erros: $errorLogFile" -Level "INFO"
    Write-Log "  - PID: $pidFile" -Level "INFO"
    Write-Log "  - Heartbeat: $heartbeatFile" -Level "INFO"

    # Criar heartbeat inicial
    Update-ServerHeartbeat -ProcessId $process.Id

    # Iniciar jobs em background para capturar saída
    $stdoutJob = Start-Job -ScriptBlock {
        param($processId, $logFile)
        $process = Get-Process -Id $processId
        while (-not $process.HasExited) {
            $output = $process.StandardOutput.ReadLine()
            if ($output) {
                $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                $logMessage = "[$timestamp] [OUTPUT] $output"
                Add-Content -Path $logFile -Value $logMessage -Encoding UTF8
            }
            Start-Sleep -Milliseconds 100
        }
    } -ArgumentList $process.Id, $serverLogFile

    $stderrJob = Start-Job -ScriptBlock {
        param($processId, $logFile)
        $process = Get-Process -Id $processId
        while (-not $process.HasExited) {
            $errorOutput = $process.StandardError.ReadLine()
            if ($errorOutput) {
                $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                $logMessage = "[$timestamp] [ERROR] $errorOutput"
                Add-Content -Path $logFile -Value $logMessage -Encoding UTF8
            }
            Start-Sleep -Milliseconds 100
        }
    } -ArgumentList $process.Id, $errorLogFile

    # Aguardar um pouco para verificar se o servidor está ativo
    Start-Sleep -Seconds 2

    if ($process.HasExited) {
        Write-Log "Processo MCP finalizou prematuramente com código $($process.ExitCode)" -Level "ERROR"
        Check-ServerLogs -Lines 20
        throw "O servidor MCP finalizou logo após iniciar. Verifique os logs."
    }

    # Manter script ativo e monitorar o processo
    Write-Log "Iniciando monitoramento do servidor..." -Level "INFO"

    $failureCount = 0
    $maxFailures = 5
    $startTime = Get-Date

    while ($true) {
        Start-Sleep -Seconds 5
        
        # Atualizar heartbeat
        if (-not $process.HasExited) {
            Update-ServerHeartbeat -ProcessId $process.Id
        }
        
        # Verificar se o processo está vivo
        if ($process.HasExited) {
            $failureCount++
            $exitCode = $process.ExitCode
            $runTime = (Get-Date) - $startTime
            
            Write-Log "Processo MCP finalizou após $($runTime.TotalMinutes.ToString('0.0')) minutos com código $exitCode. Tentativa $failureCount de $maxFailures." -Level "WARN"
            
            if ($failureCount -ge $maxFailures) {
                Write-Log "Número máximo de falhas atingido. Desistindo." -Level "ERROR"
                Check-ServerLogs -Lines 30
                throw "O servidor MCP falhou $failureCount vezes consecutivas. Verifique os logs."
            }
            
            # Esperar um pouco antes de reiniciar
            Write-Log "Aguardando 3 segundos antes de reiniciar..." -Level "INFO"
            Start-Sleep -Seconds 3
            
            # Check logs for clues
            Check-ServerLogs -Lines 10
            
            # Reiniciar o processo
            Write-Log "Reiniciando o servidor MCP..." -Level "INFO"
            
            # Criar novo processo
            $process = New-Object System.Diagnostics.Process
            $process.StartInfo = $psi
            $process.EnableRaisingEvents = $true
            
            # Iniciar novo processo
            $result = $process.Start()
            
            if (-not $result) {
                Write-Log "Falha ao reiniciar o processo MCP" -Level "ERROR"
                throw "Não foi possível reiniciar o processo MCP"
            }
            
            # Atualizar PID
            $process.Id | Set-Content $pidFile -Encoding UTF8
            
            # Criar heartbeat
            Update-ServerHeartbeat -ProcessId $process.Id
            
            Write-Log "Servidor reiniciado com PID: $($process.Id)" -Level "INFO"
            $startTime = Get-Date
        }
        else {
            # Resetar contador de falhas se o servidor está rodando por pelo menos 30 segundos
            $runTime = (Get-Date) - $startTime
            if ($runTime.TotalSeconds -gt 30 -and $failureCount -gt 0) {
                Write-Log "Servidor estável por 30 segundos, resetando contador de falhas." -Level "INFO"
                $failureCount = 0
            }
            
            # Logar status a cada minuto
            if ($runTime.TotalSeconds % 60 -lt 5) {
                Write-Log "Servidor MCP rodando há $($runTime.TotalMinutes.ToString('0.0')) minutos com PID: $($process.Id)" -Level "INFO"
            }
        }
    }
}
catch {
    $errorMessage = $_.Exception.Message
    Write-Log "Erro fatal durante inicialização: $errorMessage" -Level "ERROR"
    Write-Log "Stack Trace: $($_.Exception.StackTrace)" -Level "ERROR"
    Add-Content -Path $errorLogFile -Value "[$([DateTime]::Now)] Erro fatal: $errorMessage`nStack Trace:`n$($_.Exception.StackTrace)" -Encoding UTF8
    Check-ServerLogs -Lines 30
    throw $_
}
finally {
    Write-Log "Script de inicialização finalizado" -Level "INFO"
} 