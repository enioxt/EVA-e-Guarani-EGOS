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

# EVA & GUARANI - Master Quantum Prompt

Version: 7.5
Last Updated: 2024-03-26 15:45

## Core Configuration

```yaml
System:
  Name: "EVA & GUARANI"
  Version: "7.5"
  Type: "Master"
  Priority: 1
  
Integration:
  Subsystems:
    - Name: "CRONOS"
      Path: "../CRONOS/config/quantum_prompt.md"
      Priority: 2
      Dependencies: []
      
    - Name: "ATLAS"
      Path: "../ATLAS/config/quantum_prompt.md" 
      Priority: 3
      Dependencies: ["CRONOS"]
      
    - Name: "NEXUS"
      Path: "../NEXUS/config/quantum_prompt.md"
      Priority: 4
      Dependencies: ["ATLAS"]
      
    - Name: "ETHIK"
      Path: "../ETHIK/config/quantum_prompt.md"
      Priority: 5
      Dependencies: ["NEXUS"]
  
  Platforms:
    - Name: "Web"
      Type: "Primary"
      Priority: 1
      Technology: 
        Backend: "FastAPI"
        Frontend: "React"
        Visualization: "D3.js"
      
    - Name: "TelegramBot"
      Type: "Primary"
      Priority: 2
      Technology:
        Framework: "python-telegram-bot"
        
    - Name: "Desktop"
      Type: "Future"
      Priority: 3
      Technology:
        Framework: "Electron"
        
    - Name: "Mobile"
      Type: "Future"
      Priority: 4
      Technology:
        Framework: "React Native"

Capabilities:
  - Quantum Context Management
  - Subsystem Integration
  - Priority Resolution
  - Dependency Management
  - Version Control
  - Update Propagation
  - Platform Integration
  - Conceptual Visualization
  - Multi-Layered Communication
```

## System Description

The Master Quantum Prompt serves as the central coordination point for all subsystems in the EVA & GUARANI ecosystem. It manages context synchronization, dependency resolution, and ensures consistent behavior across all components.

## Integration Protocol

1. Each subsystem registers with the master prompt
2. Dependencies are validated and resolved
3. Updates are propagated based on priority
4. Conflicts are resolved using priority hierarchy
5. Context is synchronized across all active subsystems

## Platform Integration Architecture

```
                      ┌─────────────────┐
                      │   BIOS-Q Core   │
                      │  (Python/API)   │
                      └────────┬────────┘
                               │
                ┌──────────────┴───────────────┐
                │                              │
        ┌───────┴────────┐            ┌───────┴────────┐
        │  Web Frontend  │            │  Telegram Bot  │
        │   (JS/React)   │            │    (Python)    │
        └───────┬────────┘            └───────┬────────┘
                │                              │
      ┌─────────┴──────────┐          ┌───────┴────────┐
      │ Browser (All OS)   │          │ Telegram App   │
      │ (Web Application)  │          │ (All Platforms)│
      └────────────────────┘          └────────────────┘
```

## Implementation Priorities

1. **Web Application (Primary)**
   - REST API endpoints via FastAPI
   - React frontend for responsive dashboard
   - WebSocket integration for real-time updates
   - D3.js for visualization components
   - Progressive Web App capabilities

2. **Telegram Bot Integration**
   - Python-telegram-bot library integration
   - Commands mapped to core functions
   - Conversation flows mirroring mycelial network
   - File/media sharing via Telegram

3. **Cross-Platform Strategy (Future)**
   - Web-first approach with responsive design
   - Electron wrapper for desktop applications
   - React Native for mobile applications

## Communicating EVA & GUARANI's Essence

### Conceptual Map Visualization

- Interactive visualization of the mycelial network
- Connections between CRONOS, ATLAS, NEXUS and ETHIK
- Data flow visualization through the system

### ATLAS-First Implementation

- ATLAS subsystem as primary user-facing component
- Map-based navigation of system capabilities
- Visual exploration of interconnected components

### Multi-Layered Documentation

- Layer 1: Visual metaphors (mycelium, quantum connections)
- Layer 2: Interactive demonstrations of capabilities
- Layer 3: Technical documentation with progressive disclosure

## Security Measures

- Strict access control to prompt modifications
- Validation of all subsystem updates
- Integrity checks on context synchronization
- Audit logging of all prompt operations
- Secure storage of sensitive configurations

## Update Protocol

1. Version number increment
2. Changelog update
3. Dependency validation
4. Subsystem notification
5. Context synchronization
6. Integrity verification

## Maintenance Guidelines

1. Regular version updates
2. Dependency checks
3. Security audits
4. Performance optimization
5. Documentation updates

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
