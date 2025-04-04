---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: QUANTUM_PROMPTS
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
  subsystem: QUANTUM_PROMPTS
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

# EVA & GUARANI EGOS - Context System Reference

## Overview

The Context System is the foundation of EVA & GUARANI EGOS, providing quantum coherence and memory preservation across sessions. This document serves as the central reference for all context-related functionality.

## Context Loading Order

Always follow this context loading order when starting a new Cursor chat:

1. `QUANTUM_PROMPTS/MASTER` (PRIMARY BOOT CONTEXT)
2. `QUANTUM_PROMPTS` (System Principles)
3. `core/atlas` (Systemic Cartography)
4. `core/nexus` (Modular Analysis)
5. `core/cronos` (Evolutionary Preservation)
6. `core/ethik` (Ethical Framework)
7. `tools` (System Utilities)
8. `CHATS` (Conversation History)

## Key Context Files

- `QUANTUM_PROMPTS/MASTER/quantum_context.md` - Dynamic system state
- `QUANTUM_PROMPTS/MASTER/quantum_context_template.md` - Template for dynamic updates
- `QUANTUM_PROMPTS/MASTER/DYNAMIC_CONTEXT_SYSTEM.md` - Detailed system documentation
- `QUANTUM_PROMPTS/MASTER/CURSOR_INITIALIZATION.md` - Initialization guide
- `BIOS-Q/CONTEXT_BOOT_INSTRUCTIONS.md` - Boot sequence instructions

## Context Management Components

The context system consists of multiple components working together:

### 1. BIOS-Q Boot Sequence

- `BIOS-Q/context_boot_sequence.py` - Manages boot sequence
- `BIOS-Q/init_bios_q.py` - Initializes BIOS-Q
- `BIOS-Q/BIOS_Q/context_integration.py` - Integrates with dynamic context

### 2. Dynamic Context Manager

- `tools/scripts/dynamic_context_manager.py` - Manages dynamic context updates
- `tools/scripts/auto_context_updater.py` - Provides automatic updates
- `tools/scripts/context_manager.py` - Basic context management

### 3. Cursor Integration

- `tools/scripts/cursor_integration.py` - Integrates with Cursor IDE
- `tools/integration/cursor_atlas_bridge.py` - Connects ATLAS to Cursor

## Architecture

The Context System follows a layered architecture:

1. **Boot Layer** (BIOS-Q) - Initial system boot and verification
2. **Context Layer** (Dynamic Context) - State management and updates
3. **Integration Layer** (Cursor Integration) - External system connections
4. **Preservation Layer** (CRONOS) - Long-term memory preservation

## Usage Instructions

1. **Initialize BIOS-Q**:

   ```bash
   ./start_bios_q.bat
   ```

2. **Start Cursor Chat**:
   - Begin a new chat in Cursor
   - Follow the context loading order exactly

3. **Verify Initialization**:
   - Use the command "System Verification Request: Please confirm quantum context initialization status."
   - Verify coherence levels and active modules

4. **Resume from Previous Session**:
   - BIOS-Q automatically loads the most recent context
   - Dynamic context manager keeps context updated

## Troubleshooting

If you encounter issues with context loading:

1. Check for error messages in the `logs` directory
2. Verify all required files exist
3. Follow the context loading order precisely
4. Run BIOS-Q initialization again if needed

## Implementation Details

The Context System uses:

- Template-based dynamic context generation
- JSON-based state representation
- Markdown for human-readable context files
- Automatic 5-minute update intervals
- Quantum coherence verification

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
