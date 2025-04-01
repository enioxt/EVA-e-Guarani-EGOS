# Script de Reorganização BIOS-Q
# Data: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# Versão: 1.0

# Função para criar backup
function Create-Backup {
    param (
        [string]$SourcePath,
        [string]$BackupPath
    )
    
    if (Test-Path $SourcePath) {
        Write-Host "Criando backup de $SourcePath para $BackupPath"
        Copy-Item -Path $SourcePath -Destination $BackupPath -Recurse -Force
        return $true
    }
    return $false
}

# Função para mover com verificação
function Safe-Move {
    param (
        [string]$Source,
        [string]$Destination
    )
    
    if (Test-Path $Source) {
        Write-Host "Movendo $Source para $Destination"
        Move-Item -Path $Source -Destination $Destination -Force
        return $true
    }
    Write-Host "Aviso: $Source não encontrado"
    return $false
}

# Criar diretórios necessários
$directories = @(
    "C:\Eva & Guarani - EGOS\BIOS-Q\BIOS_Q\storage\cursor_context",
    "C:\Eva & Guarani - EGOS\quarantine\core",
    "C:\Eva & Guarani - EGOS\quarantine\modules"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        Write-Host "Criando diretório: $dir"
        New-Item -Path $dir -ItemType Directory -Force
    }
}

# Backup dos arquivos de contexto
$backupPath = "C:\Eva & Guarani - EGOS\CHATS\backup_context_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Create-Backup "C:\Eva & Guarani - EGOS\CHATS\cursor_context" $backupPath

# Mover arquivos de contexto
Safe-Move "C:\Eva & Guarani - EGOS\CHATS\cursor_context\*" "C:\Eva & Guarani - EGOS\BIOS-Q\BIOS_Q\storage\cursor_context\"

# Backup dos módulos
$modules = @("preservation", "monitoring")
foreach ($module in $modules) {
    $sourcePath = "C:\Eva & Guarani - EGOS\modules\$module"
    $backupPath = "C:\Eva & Guarani - EGOS\quarantine\modules\${module}_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Create-Backup $sourcePath $backupPath
}

# Atualizar referências no cursor_integration.py
$integrationFile = "C:\Eva & Guarani - EGOS\BIOS-Q\BIOS_Q\cursor_integration.py"
if (Test-Path $integrationFile) {
    Write-Host "Atualizando referências em $integrationFile"
    $content = Get-Content $integrationFile -Raw
    $content = $content.Replace(
        "CURSOR_CONTEXT_DIR = CHATS_DIR / 'cursor_context'",
        "CURSOR_CONTEXT_DIR = Path(__file__).parent / 'storage' / 'cursor_context'"
    )
    Set-Content -Path $integrationFile -Value $content
}

Write-Host "`nReorganização concluída!"
Write-Host "Backups foram criados em:"
Write-Host "- $backupPath"
Write-Host "- C:\Eva & Guarani - EGOS\quarantine\modules\"
