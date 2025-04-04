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

# EVA & GUARANI - Sandbox

This directory serves as an experimentation and learning environment for integrating EVA & GUARANI functionalities with frontend interfaces and APIs.

## Purpose

This sandbox was created to:

1. Experiment with frontend technologies (HTML, CSS, JavaScript) with the EVA & GUARANI backend
2. Develop simple APIs and test their consumption
3. Learn integrations without the pressure of producing perfect code
4. Serve as a laboratory for testing new ideas and approaches
5. Provide tools for standardizing the project language to English

## Structure

```
sandbox/
├── README.md               # This file
├── api/                    # Simple APIs for testing
│   ├── django_api/         # Django API
│   └── flask_api/          # Flask API (simpler)
├── frontend/               # Simple user interfaces
│   ├── html_basic/         # Pure HTML + fetch API
│   ├── javascript/         # Examples with vanilla JavaScript
│   └── components/         # Reusable components
├── examples/               # Complete integration examples
│   ├── atlas_explorer/     # Systemic mapping viewer
│   ├── nexus_connector/    # Modular analysis demonstration
│   └── cronos_timeline/    # Interface to visualize evolutionary preservation
├── tools/                  # Utility tools for development
│   ├── translate_to_english.py  # Tool to identify Portuguese files
│   ├── ai_translate_file.py     # AI-assisted file translation
│   └── translate_sandbox.bat    # Windows script for translation tools
└── docs/                   # Documentation
    ├── TRANSLATION_GUIDE.md      # Guide for translation process
    └── IMPLEMENTATION_ROADMAP.md # Development roadmap
```

## Getting Started

1. **Initial Setup**

   The easiest way to set up the sandbox environment is to use the setup script:

   ```bash
   # Run the setup script
   python setup_sandbox_env.py
   ```

   This script will:
   - Check your Python installation
   - Install required dependencies (including flask-cors)
   - Verify the sandbox directory structure
   - Create run scripts if they don't exist

   Alternatively, you can set up manually:

   ```bash
   # Setup Python environment
   python -m venv sandbox_venv
   source sandbox_venv/bin/activate  # Linux/macOS
   # or
   sandbox_venv\Scripts\activate      # Windows

   # Install dependencies
   pip install -r sandbox/requirements.txt
   ```

2. **Running the Sandbox**

   After setup, you can run the sandbox using:

   ```bash
   # On Windows
   run_sandbox.bat

   # On Linux/macOS
   python run_sandbox.py
   ```

   This will start the Flask API server and open your browser to the sandbox interface.

3. **Available Examples**
   - **Basic HTML**: A simple example of how to consume the EVA & GUARANI API with pure HTML
   - **Flask API**: A simple API to serve data from the EVA & GUARANI core
   - **Atlas Explorer**: An interface to visualize the mappings created by ATLAS

4. **Adding Your Experiments**
   Feel free to add your own experiments or modify existing ones.
   This is a safe space to try, fail, and learn.

## Translation Tools

The sandbox includes tools to help standardize the EVA & GUARANI project to use English exclusively:

1. **Portuguese File Scanner** (`tools/translate_to_english.py`)
   - Scans the codebase to identify files containing Portuguese content
   - Generates a report of files that need translation

2. **AI-Assisted Translator** (`tools/ai_translate_file.py`)
   - Uses OpenAI API to translate files from Portuguese to English
   - Preserves code structure and functionality

3. **Translation Tools Interface**
   - **Batch Script** (`tools/translate_sandbox.bat`) - Simple menu-driven interface for Windows
   - **PowerShell Script** (`tools/translate_tools.ps1`) - Enhanced interface with batch translation capabilities for Windows 11

For detailed instructions on using these tools, see the [Translation Guide](./docs/TRANSLATION_GUIDE.md).

## Integration with Core

The examples in this sandbox are configured to work with the main modules (ATLAS, NEXUS, CRONOS, ETHIK). Each component includes documentation on how it integrates with the core.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
