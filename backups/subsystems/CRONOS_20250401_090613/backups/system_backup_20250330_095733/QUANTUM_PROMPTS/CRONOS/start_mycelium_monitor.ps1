# EVA & GUARANI - Iniciador do Monitor da Rede Micelial
# ✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧

function Write-Rainbow {
    param([string]$Text)
    $colors = @("Blue", "Magenta", "Red", "Yellow", "Green", "Cyan")
    $colorIndex = 0
    foreach ($char in $Text.ToCharArray()) {
        Write-Host $char -NoNewline -ForegroundColor $colors[$colorIndex]
        $colorIndex = ($colorIndex + 1) % $colors.Length
    }
    Write-Host ""
}

function Show-Banner {
    Write-Host "`n"
    Write-Rainbow "✧༺❀༻∞ EVA & GUARANI EGOS ∞༺❀༻✧"
    Write-Host "`n"
    Write-Host "Monitor da Rede Micelial" -ForegroundColor Cyan
    Write-Host "`n"
}

# Exibir banner
Show-Banner

# Verificar se o Node.js está instalado
try {
    $nodeVersion = node -v
    Write-Host "Node.js encontrado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Node.js não encontrado. Por favor, instale o Node.js." -ForegroundColor Red
    exit 1
}

# Verificar existência do script
$scriptPath = Join-Path -Path $PSScriptRoot -ChildPath "mycelium_monitor.js"
if (-not (Test-Path $scriptPath)) {
    Write-Host "Script mycelium_monitor.js não encontrado em: $scriptPath" -ForegroundColor Red
    exit 1
}

# Criar diretório de logs se não existir
$logsDir = Join-Path -Path (Split-Path -Parent $PSScriptRoot) -ChildPath "logs"
if (-not (Test-Path $logsDir)) {
    Write-Host "Criando diretório de logs: $logsDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
}

# Configurar variáveis de ambiente
$env:EVA_GUARANI_DIR = Split-Path -Parent $PSScriptRoot

Write-Host "Iniciando Monitor da Rede Micelial..." -ForegroundColor Cyan
Write-Host "Diretório base: $env:EVA_GUARANI_DIR" -ForegroundColor Cyan
Write-Host "Diretório de logs: $logsDir" -ForegroundColor Cyan
Write-Host "`nO monitor irá verificar a integridade da rede a cada 5 minutos." -ForegroundColor Yellow
Write-Host "Os logs serão salvos em: $logsDir" -ForegroundColor Yellow
Write-Host "`nPressione Ctrl+C para interromper o monitor.`n" -ForegroundColor Red

# Iniciar o monitor
try {
    # Definir variáveis de ambiente
    $env:NODE_ENV = "production"

    # Iniciar o script
    node $scriptPath
} catch {
    Write-Host "Erro ao iniciar o monitor: $_" -ForegroundColor Red
}
