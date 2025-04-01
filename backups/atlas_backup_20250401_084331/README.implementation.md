# ATLAS Implementation Guide

## Directory Structure

O subsistema ATLAS está estruturado em dois diretórios:

1. **QUANTUM_PROMPTS/ATLAS** - Framework conceitual, roadmap e configuração
2. **src/core/atlas** - Implementação com interfaces e código

## Status da Implementação

- Interfaces principais estão implementadas em `src/core/atlas/mapper.py`
- Estas interfaces definem o contrato para o framework de visualização ATLAS
- Implementações concretas serão adicionadas em `src/modules/atlas/`

## Workflow de Desenvolvimento

Ao trabalhar no subsistema ATLAS:

1. **Consulte** o roadmap e PRD em `QUANTUM_PROMPTS/ATLAS` e `docs/prd/atlas_visualization.md`
2. **Implemente** código em `src/core/atlas` e `src/modules/atlas`
3. **Atualize** o status de implementação em ambos os roadmaps quando concluir

## Manutenção de Alinhamento

Para evitar duplicação e garantir consistência:

- Mantenha materiais conceituais em QUANTUM_PROMPTS/ATLAS
- Mantenha código de implementação em src/core/atlas e src/modules/atlas
- Atualize a documentação em ambos os diretórios ao fazer alterações

Esta estrutura garante que a implementação siga o framework conceitual enquanto mantém o código em uma estrutura de projeto padrão.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
