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

# EVA & GUARANI EGOS - Integration Tools

## Overview

This directory contains integration tools that connect EVA & GUARANI EGOS with external systems and platforms.

## File Structure

- `cursor_atlas_bridge.py` - Bridge between Cursor IDE and ATLAS module

## Integration Architecture

The integration architecture follows these principles:

1. **Bridge Pattern**: Each integration uses a bridge pattern to connect EVA & GUARANI components with external systems
2. **Minimal Coupling**: Components are designed to minimize dependencies
3. **Coherence Preservation**: All integrations maintain quantum coherence across transitions

## Integration with BIOS-Q

The integration components work with BIOS-Q to ensure proper initialization and context loading:

1. BIOS-Q initialization triggers context setup
2. Integration components connect to required modules
3. Coherence is maintained throughout the session

## Related Files

Some integration functionality also exists in:

- `/BIOS-Q/BIOS_Q/cursor_integration.py` - Cursor integration for BIOS-Q
- `/tools/scripts/cursor_integration.py` - Script-level integration with Cursor
- `/integrations/platforms/integrate_quantum_knowledge.py` - General platform integration

## Consolidation Plan

The integration files are being consolidated:

- Script-level integration will use `/tools/scripts/cursor_integration.py`
- Module-level integration will use `/tools/integration/cursor_atlas_bridge.py`
- BIOS-Q specific integration will use `/BIOS-Q/BIOS_Q/cursor_integration.py`

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
