# CRONOS Implementation Guide

## Directory Structure

O subsistema CRONOS está estruturado em dois diretórios:

1. **QUANTUM_PROMPTS/CRONOS** - Framework conceitual, roadmap e configuração
2. **src/core/cronos** - Implementação com interfaces e código

## Status da Implementação

- Interfaces principais estão implementadas em `src/core/cronos/preserver.py`
- Estas interfaces definem o contrato para o framework de preservação CRONOS
- Implementações concretas serão adicionadas em `src/modules/cronos/`

## Workflow de Desenvolvimento

Ao trabalhar no subsistema CRONOS:

1. **Consulte** o roadmap e PRD em `QUANTUM_PROMPTS/CRONOS` e `docs/prd/cronos_preservation.md`
2. **Implemente** código em `src/core/cronos` e `src/modules/cronos`
3. **Atualize** o status de implementação em ambos os roadmaps quando concluir

## Manutenção de Alinhamento

Para evitar duplicação e garantir consistência:

- Mantenha materiais conceituais em QUANTUM_PROMPTS/CRONOS
- Mantenha código de implementação em src/core/cronos e src/modules/cronos
- Atualize a documentação em ambos os diretórios ao fazer alterações

Esta estrutura garante que a implementação siga o framework conceitual enquanto mantém o código em uma estrutura de projeto padrão.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
