---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: MCP_SETUP_README.md
  changelog: []
  dependencies:
  - QUANTUM_PROMPTS
  - BIOS-Q
  description: Component of the EVA & GUARANI Quantum Unified System
  documentation_quality: 0.95
  encoding: utf-8
  ethical_validation: true
  last_updated: '2025-03-29'
  related_files: []
  required: true
  review_status: approved
  security_level: 0.95
  simulation_capable: false
  status: active
  subsystem: MASTER
  test_coverage: 0.9
  translation_status: completed
  type: documentation
  version: '8.0'
  windows_compatibility: true
---
```yaml
METADATA:
  type: documentation
  category: module
  subsystem: MASTER
  status: active
  required: false
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
  principles: []
  security_level: standard
  test_coverage: 0.0
  documentation_quality: 0.0
  ethical_validation: true
  windows_compatibility: true
  encoding: utf-8
  backup_required: false
  translation_status: pending
  api_endpoints: []
  related_files: []
  changelog: ''
  review_status: pending
```

```yaml
METADATA:
  type: documentation
  category: module
  subsystem: MASTER
  status: active
  required: false
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
```

# Configuração do Sequential Thinking MCP

Este guia descreve como configurar e utilizar o Sequential Thinking MCP no Cursor IDE.

## Pré-requisitos

- Node.js instalado (versão 14+ recomendada)
- Cursor IDE (versão mais recente)
- Permissões de administrador no Windows

## Estrutura de Arquivos

```
C:\Eva Guarani EGOS\
  ├── .cursor\
  │   └── mcp.json         # Configuração do MCP para o Cursor
  ├── tools\
  │   └── mcp-sequentialthinking-tools\  # Repositório clonado
  │       └── dist\
  │           └── index.js  # Arquivo principal do MCP
  ├── logs\                # Diretório para logs
  └── start_sequential_thinking.bat  # Script de inicialização
```

## Passos para Configuração

### 1. Instalação de Dependências

Abra um PowerShell como administrador e execute:

```powershell
# Instalar dependências globais
npm install -g typescript @types/node

# Navegar até o diretório do projeto
cd "C:\Eva Guarani EGOS\tools\mcp-sequentialthinking-tools"

# Instalar dependências do projeto
npm install

# Construir o projeto
npm run build
```

### 2. Iniciar o Servidor MCP

1. Feche o Cursor IDE completamente
2. Abra um PowerShell como administrador
3. Execute o script de inicialização:

   ```powershell
   cd "C:\Eva Guarani EGOS"
   .\start_sequential_thinking.bat
   ```

4. Mantenha esta janela aberta para manter o servidor rodando

### 3. Configurar o Cursor IDE

1. Abra o Cursor IDE (não como administrador)
2. Vá em Settings > MCP
3. Desabilite todos os servidores MCP existentes
4. Habilite apenas o servidor "sequential-thinking"
5. Clique em "Refresh"

## Uso do Sequential Thinking

Após configurar o MCP, você pode usar o Sequential Thinking no Cursor IDE através de comandos como:

- "Proceed using the sequential thinking method"
- "Use sequential thinking to solve this problem"
- "Think through this step by step"

## Solução de Problemas

- **Servidor não inicia**: Verifique se todas as dependências estão instaladas corretamente
- **Cursor não reconhece o MCP**: Verifique a configuração no arquivo `.cursor/mcp.json`
- **MCP não responde**: Reinicie o servidor e o Cursor IDE

## Referências

- [Documentação Oficial do Sequential Thinking MCP](https://github.com/modelcontextprotocol/servers/tree/HEAD/src/sequentialthinking)
- [Cursor Directory MCP](https://cursor.directory/mcp/sequential-thinking)
