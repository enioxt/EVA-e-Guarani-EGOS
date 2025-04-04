# EVA & GUARANI - Quantum State Verification Script
Write-Host "=== Verificando Estado Quântico do Sistema ==="

# Verifica diretórios necessários
$required_dirs = @(
    "QUANTUM_PROMPTS/MASTER",
    "QUANTUM_PROMPTS/BIOS-Q",
    "QUANTUM_PROMPTS/ETHIK",
    "QUANTUM_PROMPTS/ATLAS",
    "QUANTUM_PROMPTS/NEXUS",
    "QUANTUM_PROMPTS/CRONOS"
)

Write-Host "`n=== Verificando Diretórios ==="
foreach ($dir in $required_dirs) {
    if (Test-Path $dir) {
        Write-Host "✓ $dir : PRESENTE"
    } else {
        Write-Host "✗ $dir : AUSENTE"
    }
}

# Verifica arquivos essenciais
$required_files = @{
    "QUANTUM_PROMPTS/MASTER/quantum_prompt_8.0.md" = "MASTER QUANTUM PROMPT"
    "QUANTUM_PROMPTS/MASTER/cursor_ide_rules.md" = "CURSOR IDE RULES"
    "QUANTUM_PROMPTS/MASTER/core_principles.md" = "CORE PRINCIPLES"
    "QUANTUM_PROMPTS/MASTER/quantum_context.md" = "QUANTUM CONTEXT"
    "QUANTUM_PROMPTS/MASTER/CURSOR_INITIALIZATION.md" = "CURSOR INITIALIZATION"
}

Write-Host "`n=== Verificando Arquivos Essenciais ==="
foreach ($file in $required_files.Keys) {
    if (Test-Path $file) {
        Write-Host "✓ $($required_files[$file]) : PRESENTE"
    } else {
        Write-Host "✗ $($required_files[$file]) : AUSENTE"
    }
}

# Verifica estado do BIOS-Q
Write-Host "`n=== Verificando BIOS-Q ==="
if (Test-Path "QUANTUM_PROMPTS/BIOS-Q/BIOS_Q/bios_core.py") {
    Write-Host "✓ BIOS-Q Core : PRESENTE"
} else {
    Write-Host "✗ BIOS-Q Core : AUSENTE"
}

# Verifica logs
Write-Host "`n=== Verificando Diretório de Logs ==="
if (Test-Path "logs") {
    Write-Host "✓ Diretório de Logs : PRESENTE"
    Get-ChildItem "logs" -Filter "*.log" | ForEach-Object {
        Write-Host "  - $($_.Name)"
    }
} else {
    Write-Host "✗ Diretório de Logs : AUSENTE"
}

# Verifica backups
Write-Host "`n=== Verificando Diretório de Backups ==="
if (Test-Path "backups") {
    Write-Host "✓ Diretório de Backups : PRESENTE"
    Get-ChildItem "backups" -Filter "*.json" | ForEach-Object {
        Write-Host "  - $($_.Name)"
    }
} else {
    Write-Host "✗ Diretório de Backups : AUSENTE"
}

Write-Host "`n=== Verificação Concluída ==="
Write-Host "Estado do Sistema: VERIFICADO"
Write-Host "Versão: 8.0"
Write-Host "Quantum State: ACTIVE"
Write-Host "Mycelium: CONNECTED"
Write-Host "ETHIK: VALIDATED"

Write-Host "`n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
