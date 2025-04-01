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

# EVA & GUARANI EGOS - Language Tools

This directory contains tools for language processing, translation, and internationalization of the EVA & GUARANI EGOS system.

## Portuguese to English Translator

The `portuguese_english_translator.py` script provides a comprehensive solution for translating Portuguese content to English throughout the project. This helps maintain a consistent English-language codebase.

### Features

- File content translation
- File name translation
- Directory name translation
- Translation memory to ensure consistency
- Batch processing for large directories
- Dry-run mode for testing without making changes
- Dictionary-based translation with pattern matching

### Usage

#### Basic Translation

To translate a single file:

```bash
python tools/language/portuguese_english_translator.py --file path/to/file.txt
```

To translate all files in a directory (and subdirectories):

```bash
python tools/language/portuguese_english_translator.py --dir path/to/directory
```

#### Renaming Files and Directories

To translate file names from Portuguese to English:

```bash
python tools/language/portuguese_english_translator.py --dir path/to/directory --rename-files
```

To translate directory names from Portuguese to English:

```bash
python tools/language/portuguese_english_translator.py --dir path/to/directory --rename-dirs
```

#### Filtering by File Extension

To translate only files with specific extensions:

```bash
python tools/language/portuguese_english_translator.py --dir path/to/directory --extensions .md,.txt,.py
```

#### Dry Run

To simulate translation without making changes:

```bash
python tools/language/portuguese_english_translator.py --dir path/to/directory --dry-run
```

### Complete Example

To perform a full translation of a directory, including file content, file names, and directory names:

```bash
python tools/language/portuguese_english_translator.py --dir "Eva e Guarani changelogs" --rename-files --rename-dirs
```

### Customizing the Translation Dictionary

The translation dictionary is defined at the top of the `portuguese_english_translator.py` file. You can add, remove, or modify entries to improve translation quality.

```python
TRANSLATION_DICTIONARY = {
    "atualizacao": "update",
    "inicializacao": "initialization",
    # Add more translations here
}
```

### Translation Memory

The translator maintains a translation memory file at `tools/language/translation_memory.json` to ensure consistent translations across different runs. This memory is updated automatically when new translations are performed.

## Other Language Tools

### Future Development

- Advanced semantic translation using AI APIs
- Support for additional languages
- Language detection
- Automated translation of code comments
- Internationalization framework for user-facing content

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧

## Overview

The language tools provide functionality for:

- Automated translation of files between languages
- Detection of content in specific languages
- File encoding normalization
- Support for internationalization (i18n)
- Language integrity checking

## Available Tools

The following tools are available in this directory:

- `translate_to_english.py` - Scanner to identify files containing non-English content
- `ai_translate_file.py` - AI-powered translation of individual files
- `translate_tools.bat` / `translate_tools.ps1` - Interactive interfaces for translation tools

## Usage

For detailed usage instructions, please refer to the `TRANSLATE_README.md` file in this directory, or run any of the Python scripts with the `--help` flag for command-line options.

## Integration with EVA & GUARANI

These language tools are designed to work with the entire EVA & GUARANI ecosystem, maintaining ethical principles and preserving the artistic and cultural integrity of all content during the translation process.

## Migration to New Translator

The translator functionality has been migrated to a new, more advanced implementation with the following benefits:

1. **Enhanced Architecture**:
   - Modular design with clear separation of concerns
   - Better maintainability and extensibility

2. **Multiple Translation Engines**:
   - HuggingFace (offline, free): No internet required
   - OpenAI (online): Higher quality with cost controls

3. **Advanced Features**:
   - Format-specific handlers for different file types
   - Technical terminology management
   - Smart caching system
   - Cost monitoring and budget controls
   - Concurrent batch processing
   - Enhanced user interface

### How to Switch

To use the new translator, run:

```bash
python modules/translator_dev/translator.py [OPTIONS]
```

Or use the redirect script for a guided experience:

```bash
python tools/language/use_new_translator.py
```

## Legacy Tools (Deprecated)

The following tools are kept for reference but are no longer maintained:
