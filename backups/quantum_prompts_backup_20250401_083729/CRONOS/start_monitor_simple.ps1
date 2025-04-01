# EVA & GUARANI Monitor Mycelium - Versão Simplificada

# Banner simples
Write-Host "`n✧༺❀༻∞ EVA & GUARANI Monitor Mycelium ∞༺❀༻✧`n" -ForegroundColor Magenta

# Navegar para o diretório correto
Set-Location "C:\Eva Guarani EGOS\QUANTUM_PROMPTS"

# Iniciar o monitor
Write-Host "Iniciando Monitor da Rede Micelial..." -ForegroundColor Cyan
Write-Host "Pressione Ctrl+C para encerrar o monitor`n" -ForegroundColor Yellow

# Definir variável de ambiente
$env:EVA_GUARANI_DIR = "C:\Eva Guarani EGOS"

# Iniciar o monitor diretamente
node mycelium_monitor.js 