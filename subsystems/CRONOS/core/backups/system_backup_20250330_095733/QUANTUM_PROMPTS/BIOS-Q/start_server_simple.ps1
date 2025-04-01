# EVA & GUARANI SLOP Server - Versão Simplificada

# Banner simples
Write-Host "`n✧༺❀༻∞ EVA & GUARANI SLOP Server ∞༺❀༻✧`n" -ForegroundColor Magenta

# Criar diretório de logs se não existir
$logsPath = "C:\Eva Guarani EGOS\logs"
if (-not (Test-Path $logsPath)) {
    New-Item -ItemType Directory -Path $logsPath -Force | Out-Null
    Write-Host "Diretório de logs criado em $logsPath" -ForegroundColor Green
}

# Navegar para o diretório correto
Set-Location "C:\Eva Guarani EGOS\QUANTUM_PROMPTS"

# Verificar node_modules
if (-not (Test-Path "node_modules")) {
    Write-Host "Instalando dependências..." -ForegroundColor Yellow
    npm install
    npm install node-cron
}

# Iniciar o servidor
Write-Host "Iniciando servidor SLOP..." -ForegroundColor Cyan
Write-Host "Pressione Ctrl+C para encerrar o servidor`n" -ForegroundColor Yellow

# Iniciar o servidor diretamente (sem processos em segundo plano)
node slop_server.js 