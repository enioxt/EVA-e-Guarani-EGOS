---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: CHATS
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

# Sistema de Contexto EVA & GUARANI

## Visão Geral
Este sistema gerencia o contexto e estado do ambiente EVA & GUARANI, integrando com o Cursor IDE.

## Funcionalidades
- Gerenciamento de contexto
- Backup automático
- Integração com Cursor IDE
- Histórico de contextos
- Restauração de estado

## Estrutura
- `/CHATS`: Arquivos de chat e contexto
- `/QUANTUM_PROMPTS`: Prompts e configurações
- `/core`: Módulos principais
- `/tools`: Scripts e utilitários

## Uso
1. O sistema é inicializado automaticamente
2. Backups são criados a cada hora
3. Contextos antigos são limpos automaticamente
4. Estado pode ser restaurado se necessário

## Configuração
Edite `context_config.json` para ajustar:
- Intervalo de backup
- Número máximo de backups
- Tipos de contexto

## Manutenção
- Use `init_context.py` para reinicializar
- Verifique logs em `context_manager.log`
- Limpe backups antigos manualmente se necessário
