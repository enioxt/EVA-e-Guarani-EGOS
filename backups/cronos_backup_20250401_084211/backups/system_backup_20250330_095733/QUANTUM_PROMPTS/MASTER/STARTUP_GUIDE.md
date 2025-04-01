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

# EVA & GUARANI EGOS - Startup Guide

## Initialization Options

EVA & GUARANI EGOS can be initialized in several ways depending on your needs:

### 1. BIOS-Q Initialization (Recommended)

```bash
# Run from project root
./start_bios_q.bat
```

This initializes the BIOS-Q system which:

- Sets up proper context loading
- Verifies system integrity
- Prepares quantum coherence
- Creates context reminders
- Updates dynamic contexts

**Use this option when starting a new session from scratch.**

### 2. Project Initialization

```bash
# Run from project root
./start_project.bat
```

This initializes the complete project environment:

- Activates the virtual environment
- Sets up necessary folders
- Configures paths and variables
- Does NOT set up context loading

**Use this option for development environment setup.**

### 3. Quantum Review

```bash
# Run from project root
./start_quantum_review.bat
```

This starts the quantum approval system:

- Activates necessary interfaces
- Creates staging and history directories
- Runs the quantum approval UI

**Use this option for reviewing and approving quantum states.**

## Context Loading in Cursor

Always follow this context loading order when starting a new Cursor chat:

1. `QUANTUM_PROMPTS/MASTER`
2. `QUANTUM_PROMPTS`
3. `core/atlas`
4. `core/nexus`
5. `core/cronos`
6. `core/ethik`
7. `tools`
8. `CHATS`

For more details, see `CURSOR_INITIALIZATION.md`.

## File Consolidation Plan

The startup scripts and initialization files are being consolidated:

- `start_bios_q.bat` - Primary initialization (Current Active Version)
- `BIOS-Q/start_cursor_bios.bat` - Legacy file (Being consolidated)

## Troubleshooting

If initialization fails:

1. Check that you're in the project root
2. Verify that the virtual environment is active
3. Ensure all required directories exist
4. Check logs in the `logs` directory

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
