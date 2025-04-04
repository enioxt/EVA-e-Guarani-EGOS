# Script para configurar o atalho 'eva' no PowerShell (versão global)

# Definir o caminho do projeto
$projectPath = "C:\Eva Guarani EGOS"

# Verificar se o diretório existe
if (!(Test-Path $projectPath)) {
    Write-Host "Erro: O diretório '$projectPath' não existe!"
    exit 1
}

# Criar o perfil do PowerShell se não existir
if (!(Test-Path -Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
    Write-Host "Perfil do PowerShell criado em: $PROFILE"
}

# Adicionar a função ao perfil do PowerShell
$functionContent = @"
function eva {
    Set-Location "$projectPath"
    Write-Host "Diretório alterado para: $projectPath"
}
"@

# Verificar se a função já existe
$profileContent = Get-Content $PROFILE -Raw
if ($profileContent -notlike "*function eva*") {
    Add-Content -Path $PROFILE -Value $functionContent
    Write-Host "Atalho 'eva' configurado com sucesso!"
    Write-Host "Use o comando 'eva' para ir para a pasta do projeto."
}
else {
    Write-Host "O atalho 'eva' já está configurado!"
}

# Recarregar o perfil
. $PROFILE

Write-Host "`nPara testar, digite 'eva' no PowerShell."
