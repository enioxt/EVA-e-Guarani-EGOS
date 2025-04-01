# Script para configurar o atalho 'eva' no PowerShell

# Criar o perfil do PowerShell se não existir
if (!(Test-Path -Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}

# Adicionar a função ao perfil do PowerShell
$functionContent = @"
function eva {
    Set-Location "C:\Eva Guarani EGOS"
}
"@

# Verificar se a função já existe
$profileContent = Get-Content $PROFILE -Raw
if ($profileContent -notlike "*function eva*") {
    Add-Content -Path $PROFILE -Value $functionContent
    Write-Host "Atalho 'eva' configurado com sucesso! Use o comando 'eva' para ir para a pasta do projeto."
}
else {
    Write-Host "O atalho 'eva' já está configurado!"
}

# Recarregar o perfil
. $PROFILE 