# EVA & GUARANI - Memory Context Preservation (MCP) Commands
# PowerShell script para gerenciar o contexto do Cursor

$ErrorActionPreference = "Stop"
$MCP_ROOT = "C:\Eva & Guarani - EGOS\tools\mcp"

function Ensure-MCPEnvironment {
    if (-not (Test-Path $MCP_ROOT)) {
        Write-Host "[X] Diretório MCP não encontrado em: $MCP_ROOT"
        exit 1
    }
}

function Save-CurrentContext {
    Write-Host "[*] Salvando contexto atual..."
    Ensure-MCPEnvironment
    python "$MCP_ROOT\cursor_commands.py" save_current
}

function Save-MCPContext {
    Write-Host "[*] Salvando contexto MCP completo..."
    Ensure-MCPEnvironment
    python "$MCP_ROOT\cursor_commands.py" save_mcp
}

function Load-MCPContext {
    Write-Host "[*] Carregando contexto MCP..."
    Ensure-MCPEnvironment
    python "$MCP_ROOT\cursor_commands.py" load_mcp
}

function Update-ContextLimit {
    Write-Host "[*] Atualizando limite de contexto..."
    Ensure-MCPEnvironment
    python "$MCP_ROOT\cursor_commands.py" update_limit
}

# Verifica argumentos
if ($args.Count -eq 0) {
    Write-Host "[X] Comando necessário. Use um dos seguintes:"
    Write-Host "  - save_current : Salva o contexto atual"
    Write-Host "  - save_mcp    : Salva todo o contexto MCP"
    Write-Host "  - load_mcp    : Carrega o contexto MCP"
    Write-Host "  - update_limit: Atualiza o limite de contexto"
    exit 1
}

# Executa o comando apropriado
switch ($args[0]) {
    "save_current" { Save-CurrentContext }
    "save_mcp" { Save-MCPContext }
    "load_mcp" { Load-MCPContext }
    "update_limit" { Update-ContextLimit }
    default {
        Write-Host "[X] Comando inválido: $($args[0])"
        exit 1
    }
} 