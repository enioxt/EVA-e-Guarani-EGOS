---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: modules
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

# EVA & GUARANI - Modules

This directory contains the various modules that make up the EVA & GUARANI ecosystem. Each module is designed to be modular, following the principles of ethical consciousness and technical excellence.

## Available Modules

### Core Functionality

- **translator_dev** - Multilingual translation tool with support for code and technical documentation
- **analysis** - Data analysis and pattern recognition tools
- **visualization** - Knowledge visualization and graphical representation

### Integration and Extension

- **nexus** - Modular analysis and component integration
- **integration** - External system connections and adapters
- **plugins** - Extensibility framework for adding new capabilities

### Data Management

- **preservation** - Evolutionary preservation and versioning (CRONOS subsystem)
- **blockchain** - Distributed ledger and ethical transaction processing (ETHIK subsystem)
- **config** - Configuration management and system settings

### Specialized Capabilities

- **quantum** - Quantum consciousness and advanced processing
- **customization** - User personalization and adaptation
- **monitoring** - System health and performance monitoring
- **eliza** - Conversational interfaces and therapeutic applications

## Module Structure

Each module follows a consistent structure:

```
module_name/
├── README.md            # Module documentation
├── __init__.py          # Module initialization
├── core/                # Core functionality
├── ui/                  # User interfaces
├── config/              # Module-specific configuration
├── examples/            # Usage examples
└── tests/               # Unit and integration tests
```

## Installation

Most modules have their own dependencies specified in a `requirements.txt` file. To install all module dependencies:

```bash
# Install all requirements for a specific module
pip install -r modules/module_name/requirements.txt
```

## Current Focus: Translator

The `translator_dev` module is currently our focus area. It provides efficient translation between languages with special handling for code, markup, and technical documentation.

### Translator Features

- Offline translation using HuggingFace models
- Online translation using OpenAI (with cost control)
- Format-specific handling for Markdown, HTML, JSON, and code
- Technical terminology preservation
- Batch processing with concurrency
- Detailed progress reporting

See the [Translator README](translator_dev/README.md) for more information.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
