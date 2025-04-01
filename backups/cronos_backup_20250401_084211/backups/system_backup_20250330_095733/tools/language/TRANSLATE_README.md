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

# EVA & GUARANI Translation Tools

This directory contains tools for identifying and translating Portuguese content to English across the entire EVA & GUARANI project.

## Quick Start

### Windows Users

1. Run the interactive tool:

   ```
   .\translate_tools.bat
   ```

2. Use the menu to:
   - Scan your project for Portuguese files
   - Automatically translate detected files
   - Translate individual files

### Mac/Linux Users

1. Run the Python scripts directly:

   ```
   python translate_to_english.py --root-dir "/path/to/project"
   ```

2. For translation:

   ```
   python ai_translate_file.py --file "/path/to/file.py"
   ```

## Features

- **Integrated workflow**: After scanning, the tool now offers to translate detected files immediately
- **Intelligent detection**: Automatically identifies Portuguese content in code, documentation, and configuration files
- **AI-powered translation**: Uses OpenAI's models to accurately translate while preserving code structure
- **Priority-based processing**: Focuses on the most important files first
- **Preservation**: Creates backups before modifying files

## Usage Options

### Scan Mode

```
python translate_to_english.py --root-dir "/path/to/project"
```

Options:

- `--root-dir`: Directory to scan (default: current directory)
- `--output`: Path for the report file (default: translation_report.md)
- `--ignore-dirs`: Directories to exclude from scanning

### Translation Mode

```
python ai_translate_file.py --file "/path/to/file.py"
```

Options:

- `--file`: Path to the file to translate
- `--output`: Output file path (default: replaces original)
- `--api-key`: OpenAI API key (optional)
- `--dry-run`: Preview changes without modifying files
- `--batch`: Process files from a translation report
- `--priority`: Which priority files to translate (high/medium/low/all)

## Interactive Tools

The project provides two interactive interfaces:

1. **Batch script** (`translate_tools.bat`):
   - Windows-friendly interface
   - Menu-driven operation
   - Automatic detection and translation workflow

2. **PowerShell script** (`translate_tools.ps1`):
   - More features and better error handling
   - Color-coded output
   - Detailed progress reporting

## Ethical Considerations

These tools are designed with EVA & GUARANI's ethical principles in mind:

- Files are backed up before modification
- Code structure and functionality are preserved
- Options for review before changes are applied
- Respect for original content and authorship

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
