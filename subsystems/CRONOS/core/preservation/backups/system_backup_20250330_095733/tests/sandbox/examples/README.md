---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: sandbox
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

# EVA & GUARANI Sandbox Examples

This directory contains example code demonstrating how to integrate with and use the EVA & GUARANI modules in various contexts.

## Available Examples

### Basic Integration

The `basic_integration.py` script demonstrates the fundamental integration patterns with all core modules (ATLAS, NEXUS, CRONOS, ETHIK) in a simple Python application:

```bash
python basic_integration.py
```

### Data Processing Examples

The `data_processing` directory contains examples for processing different types of data through EVA & GUARANI modules:

- Text analysis
- Code evaluation
- Structure mapping

### API Integration

The `api_integration` directory shows how to consume the sandbox API from different programming languages:

- Python
- JavaScript
- PowerShell

## Creating Your Own Examples

Follow these guidelines when creating new examples:

1. Create a descriptive directory or file name
2. Include clear documentation at the beginning of your code
3. Handle both scenarios:
   - When core modules are available
   - When using simulated data
4. Include sample output in comments or in a separate file

## Testing Your Examples

Before submitting new examples, verify that they work correctly both with and without core modules:

```bash
# Test with simulated data
python your_example.py

# Test with core modules (if available)
PYTHONPATH=$PYTHONPATH:/path/to/core python your_example.py
```

## Example Templates

Use the provided templates as starting points for your own examples:

- `template_basic.py` - Simple script example
- `template_class.py` - Class-based integration
- `template_async.py` - Asynchronous processing example
