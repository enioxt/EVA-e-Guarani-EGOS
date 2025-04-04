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

# Instruções de Uso: MCP Perplexity no Cursor IDE

## O que é MCP?

**Model Context Protocol (MCP)** é um protocolo que permite ao Cursor IDE (e outros editores compatíveis) se comunicar diretamente com serviços de IA, incluindo o Perplexity, para pesquisas em tempo real.

## Como Ativar o MCP Perplexity no EVA & GUARANI

### Método Automático (Recomendado)

A integração MCP está configurada para iniciar automaticamente sempre que você abrir o projeto EVA & GUARANI no Cursor.

1. Abra o projeto EVA & GUARANI no Cursor
2. O servidor MCP iniciará automaticamente
3. Use os atalhos de teclado para pesquisas

### Método Manual

Se o servidor MCP não iniciar automaticamente, você pode iniciá-lo manualmente:

1. Abra o terminal no Cursor (`` Ctrl+` ``)
2. Execute o script de inicialização:

   ```bash
   # Windows
   .\tools\launchers\start_perplexity_mcp.bat

   # Linux/Mac
   ./tools/launchers/start_perplexity_mcp.sh
   ```

3. Mantenha a janela do terminal aberta enquanto usa o MCP

## Como Usar o MCP Perplexity

### Atalhos de Teclado

Os seguintes atalhos estão configurados:

| Atalho | Função |
|--------|--------|
| `Ctrl+Alt+P` | Buscar no Perplexity |
| `Ctrl+Alt+Shift+P` | Buscar como filósofo |
| `Ctrl+Alt+Shift+S` | Buscar como cientista |

### Exemplo de Uso

1. Selecione um texto no editor (ex: "inteligência artificial quântica")
2. Pressione `Ctrl+Alt+P` para realizar uma busca
3. O resultado aparecerá no painel de chat do Cursor

## Verificando o Status do MCP

Para verificar se o servidor MCP está ativo:

1. Abra o terminal no Cursor
2. Execute o comando:

   ```bash
   # Windows
   netstat -an | findstr 38001

   # Linux/Mac
   netstat -an | grep 38001
   ```

3. Se o servidor estiver ativo, você verá uma conexão na porta 38001

## Troubleshooting

### O MCP não está respondendo

Se o MCP não responder às suas consultas:

1. Verifique se o servidor está rodando (veja acima)
2. Reinicie o servidor MCP manualmente
3. Verifique os logs em `tools/integration/mcp_server.log`

### Erros de API

Se ocorrerem erros relacionados à API:

1. Verifique se a chave da API Perplexity está correta no arquivo `.env`
2. Verifique sua cota de API no painel do Perplexity

### Reiniciando o Servidor

Para reiniciar o servidor MCP:

1. Encerre o processo atual (Ctrl+C no terminal onde ele está rodando)
2. Inicie-o novamente usando o script de inicialização

## Adicionando Outros Servidores MCP

Você pode adicionar servidores MCP de terceiros modificando o arquivo `.cursor/settings.json`:

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
    },
    {
      "name": "Perplexity Oficial",
      "command": "npx @mcp-server/perplexity --api-key=${ENV:PPLX_KEY}",
      "env": {
        "PPLX_KEY": "sua_chave_api_aqui"
      },
      "autoStart": false,
      "priority": 90
    }
  ],
  "enabledServers": ["EVA & GUARANI Perplexity"]
}
```

## Mais Informações

Para detalhes técnicos completos, consulte:

- [Documentação MCP](docs/MCP_INTEGRATION.md)
- [Cursor MCP Documentation](https://docs.cursor.sh/resources/mcp-server)
- [MCP Protocol Spec](https://docs.cursor.sh/model-context-protocol)

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
