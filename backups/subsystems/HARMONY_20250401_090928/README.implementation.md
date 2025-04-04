# HARMONY Implementation Guide

## Directory Structure

O subsistema HARMONY está estruturado em dois diretórios:

1. **QUANTUM_PROMPTS/HARMONY** - Framework conceitual, roadmap e configuração
2. **src/core/harmony** - Implementação com interfaces e código

## Status da Implementação

- Interfaces principais estão implementadas em `src/core/harmony/adapter.py`
- Estas interfaces definem o contrato para o framework de compatibilidade HARMONY
- Implementações concretas serão adicionadas em `src/modules/harmony/`

## Workflow de Desenvolvimento

Ao trabalhar no subsistema HARMONY:

1. **Consulte** o roadmap e PRD em `QUANTUM_PROMPTS/HARMONY` e `docs/prd/harmony_compatibility.md`
2. **Implemente** código em `src/core/harmony` e `src/modules/harmony`
3. **Atualize** o status de implementação em ambos os roadmaps quando concluir

## Manutenção de Alinhamento

Para evitar duplicação e garantir consistência:

- Mantenha materiais conceituais em QUANTUM_PROMPTS/HARMONY
- Mantenha código de implementação em src/core/harmony e src/modules/harmony
- Atualize a documentação em ambos os diretórios ao fazer alterações

Esta estrutura garante que a implementação siga o framework conceitual enquanto mantém o código em uma estrutura de projeto padrão.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
