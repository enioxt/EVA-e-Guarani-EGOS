---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: cronos
  changelog: []
  dependencies:
  - QUANTUM_PROMPTS
  - CRONOS
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
  subsystem: CRONOS
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

# CRONOS - Context Retention and Operational Neural Optimization System

Sistema de preservação de contexto para EVA & GUARANI no ambiente Cursor IDE.
Anteriormente conhecido como Memory Context Protocol (MCP).

## Funcionalidades

- Monitoramento automático de contexto
- Rastreamento de tamanho de contexto
- Funcionalidade de auto-save
- Comandos simples de save/load
- Limites adaptativos de contexto

## Início Rápido

### Via Scripts Batch

Navegue até `cronos/scripts` e execute:

- `save.bat` - Salvar contexto atual
- `load.bat` - Carregar contexto mais recente
- `start_monitor.bat` - Iniciar monitor de contexto
- `update_limit.bat` - Atualizar limite de contexto

### Via Linha de Comando

Do diretório `cronos`:

```bash
# Salvar contexto
python -m core.cursor_commands save_cronos

# Carregar contexto
python -m core.cursor_commands load_cronos

# Listar saves
python -m core.cursor_commands list_saves

# Mostrar status do monitor
python -m core.cursor_commands show_status

# Atualizar limite de contexto
python -m core.cursor_commands update_limit
```

### Via Chat do Cursor

Digite estes comandos no chat do Cursor:

- `@save` - Obter comando de save
- `@load` - Obter comando de load
- `@list` - Listar contextos salvos
- `@status` - Verificar status do monitor
- `@update` - Atualizar limite de contexto

## Estrutura de Diretórios

```
cronos/
├── core/
│   ├── context_monitor.py - Monitoramento de contexto
│   ├── cronos_capture.py  - Funcionalidade de save
│   ├── cronos_restore.py  - Funcionalidade de load
│   └── cursor_commands.py - Interface de comandos
├── scripts/
│   ├── save.bat          - Script de save
│   ├── load.bat          - Script de load
│   ├── start_monitor.bat - Script do monitor
│   └── update_limit.bat  - Script de atualização de limite
├── config/
│   └── context_limits.json - Limites de contexto
└── saves/
    └── context_*.json    - Contextos salvos
```

## Como Funciona

1. O monitor começa com um limite conservador (100.000 caracteres)
2. Quando o Cursor solicita novo chat, o sistema registra o tamanho atual
3. O limite é ajustado para 90% do tamanho medido por segurança
4. Auto-save dispara em 80% da capacidade ou a cada 30 minutos
5. Todos os dados de contexto são salvos com timestamps para rastreamento

## Requisitos

- Python 3.6+
- Windows 10/11
- Cursor IDE
