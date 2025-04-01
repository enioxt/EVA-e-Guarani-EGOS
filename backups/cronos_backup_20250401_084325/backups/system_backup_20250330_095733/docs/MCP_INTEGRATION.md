---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: docs
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

# Integração MCP (Model Context Protocol) para EVA & GUARANI

## Visão Geral

Esta documentação descreve a integração do protocolo MCP (Model Context Protocol) no sistema EVA & GUARANI, permitindo que o Cursor IDE execute comandos de pesquisa diretamente via Perplexity API.

O MCP é um protocolo que permite que editores e IDEs se comuniquem com servidores de modelos de linguagem para obter respostas em tempo real.

## Arquitetura

A integração MCP do EVA & GUARANI consiste em três componentes principais:

1. **Servidor MCP** - Um servidor WebSocket que implementa o protocolo MCP
2. **Integração Perplexity** - Conecta o servidor MCP à API Perplexity
3. **Configuração do Cursor** - Define como o Cursor IDE se conecta ao servidor MCP

### Fluxo de Dados

```
┌─────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Cursor  │────▶│ Servidor MCP │────▶│  Perplexity  │────▶│ Resultados   │
│  IDE    │◀────│  (38001)     │◀────│  Integration │◀────│ da Pesquisa  │
└─────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

## Configuração

### Pré-requisitos

- Python 3.9+
- Biblioteca websockets (`pip install websockets`)
- Chave de API do Perplexity

### Arquivos de Configuração

#### 1. Configuração do Servidor MCP

O servidor MCP é configurado em `.cursor/mcp-servers/perplexity.json`:

```json
{
  "name": "EVA & GUARANI Perplexity",
  "command": "python -m tools.integration.mcp_server",
  "env": {
    "PERPLEXITY_API_KEY": "sua_chave_api_aqui"
  },
  "autoStart": true,
  "priority": 100
}
```

#### 2. Configuração do Cursor

As configurações do Cursor estão em `.cursor/settings.json` e incluem a seção `mcp`:

```json
"mcp": {
  "servers": [
    {
      "name": "EVA & GUARANI Perplexity",
      "command": "python -m tools.integration.mcp_server",
      "env": {
        "PERPLEXITY_API_KEY": "sua_chave_api_aqui"
      },
      "autoStart": true,
      "priority": 100
    }
  ],
  "enabledServers": ["EVA & GUARANI Perplexity"]
}
```

## Uso

### Inicialização Manual

Se o servidor MCP não iniciar automaticamente, você pode iniciá-lo manualmente:

#### Windows

```
.\tools\launchers\start_perplexity_mcp.bat
```

#### Linux/Mac

```
./tools/launchers/start_perplexity_mcp.sh
```

### Atalhos de Teclado

Os seguintes atalhos estão configurados no Cursor:

- `Ctrl+Alt+P` - Buscar no Perplexity
- `Ctrl+Alt+Shift+P` - Buscar como filósofo
- `Ctrl+Alt+Shift+S` - Buscar como cientista

### Comandos Personalizados

Para adicionar novos comandos personalizados, edite a seção `ai.customCommands` em `.cursor/settings.json`.

## Integração com MCP de terceiros

Além do servidor MCP personalizado, você pode integrar o EVA & GUARANI com outros servidores MCP:

1. **Perplexity MCP Official**

   ```
   npx @mcp-server/perplexity --api-key=pplx-sua-chave
   ```

2. **LocalAI + Ollama**

   ```
   npx @mcp-server/ollama --model=llama2
   ```

3. **OpenRouter**

   ```
   npx mcp-server-openrouter --api-key=sk-or-v1-...
   ```

Para configurar múltiplos servidores MCP, adicione-os à seção `mcp.servers` e ajuste suas prioridades.

## Solução de Problemas

### Verificação do Servidor

Para verificar se o servidor MCP está rodando:

1. Abra um terminal e execute `netstat -an | findstr 38001` (Windows) ou `netstat -an | grep 38001` (Linux/Mac)
2. Verifique os logs em `tools/integration/mcp_server.log`

### Problemas Comuns

1. **Servidor não inicia**
   - Verifique se a chave API está configurada corretamente
   - Verifique se as dependências estão instaladas

2. **Cursor não consegue se conectar**
   - Verifique se a porta 38001 está disponível
   - Reinicie o Cursor e o servidor MCP

3. **Respostas incorretas ou vazias**
   - Verifique os logs para erros
   - Garanta que a API Perplexity esteja funcionando corretamente

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
