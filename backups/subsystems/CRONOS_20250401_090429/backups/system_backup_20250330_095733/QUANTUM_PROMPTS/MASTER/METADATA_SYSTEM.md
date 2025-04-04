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

# EVA & GUARANI - File Metadata System v1.0

## Overview

The EVA & GUARANI system uses a standardized metadata system at the beginning of each file to facilitate context identification and file categorization. This helps AI agents and developers quickly understand the purpose and context of each file without having to read its entire contents.

## Metadata Format

```yaml
METADATA:
type: <file_type>
category: <main_category>
subsystem: <subsystem_name>
status: <active|inactive|deprecated|planned>
required: <true|false>
simulation_capable: <true|false>
dependencies:
  - <dependency_1>
  - <dependency_2>
description: <brief_description>
author: <author_name>
version: <version_number>
last_updated: <YYYY-MM-DD>
```

## File Types

- system_initialization
- system_entry_point
- configuration
- module
- utility
- test
- documentation
- prompt
- integration
- api
- ui
- database
- backup

## Categories

- core
- subsystem
- utility
- test
- documentation
- integration
- api
- ui
- data

## Subsystems

- BIOS-Q
- QUANTUM_PROMPTS
- ETHIK
- ATLAS
- NEXUS
- CRONOS
- TRANSLATOR

## Status Values

- active: File is currently in use
- inactive: File exists but is not currently used
- deprecated: File is obsolete and should be moved to quarantine
- planned: File is planned for future implementation

## Example

```python
"""
METADATA:
type: system_initialization
category: core
subsystem: BIOS-Q
status: active
required: true
simulation_capable: true
dependencies:
  - BIOS-Q
  - QUANTUM_PROMPTS
description: System initialization script
author: EVA & GUARANI
version: 8.0
last_updated: 2025-03-26
"""
```

## Usage Guidelines

1. Every new file should include metadata at the beginning
2. Use appropriate comment syntax for the file type:
   - Python: Use docstring (""")
   - JavaScript/TypeScript: Use /**/
   - Batch: Use REM
   - Markdown: Use yaml code block
   - Shell: Use #

3. Keep metadata up to date when modifying files
4. Use consistent formatting and indentation
5. Include all required fields
6. Be specific in descriptions
7. List all direct dependencies

## Benefits

1. Quick context identification for AI agents
2. Easy file categorization and organization
3. Clear dependency tracking
4. Simple obsolescence identification
5. Facilitates system maintenance
6. Improves documentation
7. Helps prevent duplicate functionality

## Implementation

1. Add metadata to all new files
2. Gradually add metadata to existing files during updates
3. Move deprecated files to quarantine
4. Update metadata when making significant changes
5. Use metadata for system analysis and documentation

## Tooling

Future tools will be developed to:

1. Validate metadata format
2. Generate system documentation from metadata
3. Track dependencies
4. Identify potential duplicates
5. Manage file categorization
6. Monitor system health

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
