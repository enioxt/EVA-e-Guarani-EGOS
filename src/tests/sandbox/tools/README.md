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

# EVA & GUARANI Sandbox Tools

This directory contains utility tools for the EVA & GUARANI sandbox environment. These tools are designed to assist with various development, testing, and maintenance tasks.

## Available Tools

### Translation Tools

Tools to help convert Portuguese content to English, maintaining the project's English-first standard:

- **translate_to_english.py** - Scans the codebase for files containing Portuguese content and generates a report of files that need translation.

  ```bash
  python translate_to_english.py --root-dir "../../" --output "translation_report.md"
  ```

- **ai_translate_file.py** - Uses OpenAI API to translate individual files from Portuguese to English, preserving code structure.

  ```bash
  python ai_translate_file.py "path/to/file.py" --output "path/to/output.py" --api-key "your-api-key"
  ```

- **translate_sandbox.bat** - Windows batch script that provides a menu-driven interface for running the translation tools.

  ```bash
  # Simply run:
  translate_sandbox.bat
  ```

- **translate_tools.ps1** - Enhanced PowerShell script with advanced features for Windows 11 users.

  ```powershell
  # Run in PowerShell:
  .\translate_tools.ps1
  ```

For detailed instructions on using these tools, see the [Translation Guide](../docs/TRANSLATION_GUIDE.md).

### Setup Tools

Tools for setting up and configuring the sandbox environment:

- **setup_sandbox.py** - Creates the directory structure and placeholder files for the sandbox environment.

  ```bash
  python setup_sandbox.py
  ```

- **run_sandbox.py** - Starts the sandbox environment, including the Flask API server and any other necessary components.

  ```bash
  python run_sandbox.py
  ```

### Integration Tools

Tools for testing integrations with external services:

- **perplexity_test.py** - Tests the integration with the Perplexity API.

  ```bash
  python perplexity_test.py --api-key "your-perplexity-api-key"
  ```

## Using the Tools

Most tools provide help information when run with the `--help` flag:

```bash
python translate_to_english.py --help
```

## Adding New Tools

When adding new tools to this directory, please follow these guidelines:

1. Use clear, descriptive names for tool scripts
2. Include comprehensive docstrings at the top of each file
3. Implement proper argument parsing with help information
4. Add appropriate logging
5. Update this README to include information about new tools

## License

All tools in this directory are covered by the same license as the EVA & GUARANI project.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
