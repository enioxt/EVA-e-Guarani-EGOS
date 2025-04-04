---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: tools
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

# MCP - Memory Context Preservation

Sistema de preservação de contexto para EVA & GUARANI no ambiente Cursor.

## 🆕 Novidade: Monitor de Contexto Adaptativo

O MCP agora inclui um **monitor adaptativo** que:

1. **Aprende o limite real do Cursor** através de dados empíricos
2. **Salva automaticamente** quando atinge 80% da capacidade
3. **Backup preventivo** a cada 30 minutos para evitar perda de dados
4. **Integração com BIOS-Q** para persistência dos limites entre sessões

### Como usar o sistema adaptativo

1. Quando o Cursor solicitar iniciar um novo chat, execute:

   ```
   cd /c/Eva\ \&\ Guarani\ -\ EGOS/tools/mcp && python cursor_commands.py update_limit
   ```

2. O sistema registrará o limite real e ajustará automaticamente todos os cálculos de capacidade

### Para iniciar o monitor

```
cd /c/Eva\ \&\ Guarani\ -\ EGOS/tools/mcp
./start_monitor.bat
```

O monitor funcionará em segundo plano e salvará automaticamente o contexto quando necessário.

**Para verificar o status:**

```
@status
```

## Comandos Rápidos

### No chat do Cursor

Quando estiver no chat com Claude no Cursor, digite:

- `@save` - Obter comando para salvar contexto
- `@load` - Obter comando para carregar contexto
- `@list` - Obter comando para listar contextos salvos
- `@status` - Verificar status do monitor de contexto
- `@update` - Obter comando para atualizar limite de contexto (quando solicitado novo chat)

Claude irá responder com as instruções específicas para executar no terminal.

### Via Terminal (Windows)

Para salvar o contexto atual:

```
cd /c/Eva\ \&\ Guarani\ -\ EGOS/tools/mcp && python cursor_commands.py save_mcp
```

Para carregar o contexto mais recente:

```
cd /c/Eva\ \&\ Guarani\ -\ EGOS/tools/mcp && python cursor_commands.py load_mcp
```

Para listar todos os contextos salvos:

```
cd /c/Eva\ \&\ Guarani\ -\ EGOS/tools/mcp && python cursor_commands.py mcp_list
```

Para verificar o status do monitor:

```
cd /c/Eva\ \&\ Guarani\ -\ EGOS/tools/mcp && python cursor_commands.py mcp_status
```

Para atualizar o limite de contexto (quando Cursor solicitar novo chat):

```
cd /c/Eva\ \&\ Guarani\ -\ EGOS/tools/mcp && python cursor_commands.py update_limit
```

### Via Scripts Batch (mais simples)

Abra Explorador de Arquivos e navegue até:

```
C:\Eva & Guarani - EGOS\tools\mcp
```

E execute um dos scripts:

- `save.bat` - Para salvar contexto
- `load.bat` - Para carregar contexto
- `start_monitor.bat` - Para iniciar o monitor automático
- `update_limit.bat` - Para atualizar o limite após novo chat

## Integração com BIOS-Q

O sistema MCP foi projetado para integrar com o BIOS-Q para preservação de contexto entre sessões. Os arquivos são salvos em:

```
C:\Eva & Guarani - EGOS\CHATS\cursor_context\
```

Os limites de contexto são armazenados em:

```
C:\Eva & Guarani - EGOS\tools\BIOS-Q\context_limits.json
```

## Estrutura do Contexto

Cada arquivo de contexto salvo contém:

- Lista de módulos discutidos (ETHIK, ATLAS, etc.)
- Resumo da conversa
- Conceitos-chave mencionados
- Relacionamentos entre componentes
- Timestamp da sessão
- Instruções de transição para novo chat

## Uso Recomendado

1. Inicie o monitor automático no começo da sessão
2. O monitor salvará automaticamente quando o contexto atingir 80% da capacidade
3. Também salvará a cada 30 minutos como backup preventivo
4. Verifique o status do monitor periodicamente com `@status`
5. Quando o Cursor solicitar novo chat, atualize o limite com `@update`
6. Carregue o contexto ao iniciar uma nova sessão com `@load`

## Como o Sistema Adaptativo Funciona

1. O sistema começa com um limite conservador de 100.000 caracteres
2. Quando o Cursor solicitar novo chat, o sistema registra o tamanho atual como limite real
3. O limite de 80% é ajustado para 90% desse limite real para segurança
4. A informação é armazenada no BIOS-Q e usada em todas as sessões futuras
5. O sistema continuará aprendendo e se ajustando com o uso

## Arquivos do Sistema

- `mcp_capture.py` - Captura e salva o contexto
- `mcp_restore.py` - Restaura o contexto salvo
- `cursor_commands.py` - Interface para comandos
- `context_monitor.py` - Monitor adaptativo de contexto
- `save.bat`, `load.bat`, `start_monitor.bat` - Scripts de conveniência

## Requisitos

- Python 3.6+
- Windows 10/11
- Ambiente Cursor com Claude 3 Opus ou versões mais recentes
