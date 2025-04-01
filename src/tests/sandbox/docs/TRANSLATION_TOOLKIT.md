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

# EVA & GUARANI Translation Toolkit

This document provides an overview of the translation tools developed for standardizing the EVA & GUARANI project to English. These tools are designed to identify, manage, and translate Portuguese content throughout the entire codebase.

## Overview

The EVA & GUARANI Translation Toolkit consists of several complementary tools:

1. **Portuguese File Scanner** (`translate_to_english.py`)
2. **AI-Assisted Translation Tool** (`ai_translate_file.py`)
3. **Translation Tool Runner - Batch** (`translate_tools.bat`)
4. **Translation Tool Runner - PowerShell** (`translate_tools.ps1`)
5. **Documentation and Guides**

These tools work together to provide a complete workflow for translating the EVA & GUARANI project from Portuguese to English, ensuring that all code, comments, documentation, and user interfaces maintain consistency.

## Portuguese File Scanner

The scanner identifies files containing Portuguese content by analyzing text patterns, common Portuguese words, and diacritical marks.

**Key Features:**

- Recursively scans directories for files containing Portuguese text
- Filters out system directories and non-project files
- Prioritizes files based on importance (core modules, documentation, etc.)
- Generates detailed Markdown reports of identified files
- Supports sample mode for quick testing

**Usage:**

```bash
python translate_to_english.py --root-dir "C:\Eva & Guarani - EGOS" [--sample-only]
```

## AI-Assisted Translation Tool

The translation tool utilizes OpenAI's language models to translate individual files from Portuguese to English, maintaining code structure and functionality.

**Key Features:**

- Preserves code structure, formatting, and functionality
- Creates automatic backups of original files
- Adapts translation approach based on file type
- Supports dry-run mode for testing without making changes
- Handles comments, docstrings, and variable names appropriately

**Usage:**

```bash
python ai_translate_file.py --file "path/to/file.py" [--api-key "your-api-key"] [--dry-run]
```

**Requirements:**

- OpenAI API key (set as environment variable or passed as parameter)
- `openai` Python package installed (`pip install openai>=1.0.0`)

## Translation Tool Runners

### Windows Batch Interface (`translate_tools.bat`)

A user-friendly batch script for running the translation tools without needing to remember command-line parameters.

**Features:**

- Menu-driven interface for tool selection
- Simplified workflow for scanning and translating
- UTF-8 support for handling special characters
- Informative console output and guidance

**Usage:**

```
translate_tools.bat
```

### PowerShell Interface (`translate_tools.ps1`)

An enhanced PowerShell script with additional features for Windows users.

**Features:**

- Colorful, user-friendly console interface
- Advanced options for translation settings
- Project-wide scanning capabilities
- Detailed feedback and progress reporting

**Usage:**

```powershell
.\translate_tools.ps1
```

## Documentation and Guides

The toolkit includes comprehensive documentation:

1. **Translation Guide** (`TRANSLATION_GUIDE.md`)
   - Detailed guidelines for translating different types of content
   - Best practices for maintaining code functionality
   - Workflow recommendations for efficient translation

2. **Implementation Roadmap** (`IMPLEMENTATION_ROADMAP.md`)
   - Step-by-step roadmap for standardizing the project to English
   - Prioritized file lists for translation
   - Milestones and success criteria

## Translation Workflow

1. **Scan the Project**
   - Run the scanner to identify files containing Portuguese content
   - Review the generated translation report

2. **Prioritize Translation**
   - Start with high-priority files (core modules, documentation)
   - Plan the translation sequence based on dependencies

3. **Translate Files**
   - Use the AI translation tool for initial translation
   - Manually review and adjust translations as needed
   - Ensure code functionality is preserved

4. **Update References**
   - Update any references to translated files
   - Check import statements and documentation links
   - Verify file path references in both code and docs

5. **Validate Translations**
   - Test functionality after translation
   - Run any available tests
   - Check for consistent terminology

## Integration with EVA & GUARANI System

The Translation Toolkit is designed to work with all components of the EVA & GUARANI system:

- **Core Modules**: ATLAS, NEXUS, CRONOS, ETHIK
- **Frontend Components**: User interfaces and web components
- **Documentation**: Markdown, HTML, and other doc formats
- **Configuration Files**: JSON, YAML, and other config formats
- **Examples and Tests**: Demo code and test suites

## Setup Instructions

1. **Install Required Packages**

   ```bash
   pip install openai>=1.0.0
   ```

2. **Configure API Key**

   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # PowerShell
   $env:OPENAI_API_KEY="your_api_key_here"
   ```

3. **Run Translation Tools**

   ```bash
   cd "C:\Eva & Guarani - EGOS\sandbox\tools"
   
   # PowerShell
   .\translate_tools.ps1
   
   # Windows Batch
   translate_tools.bat
   ```

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient quota
- **Encoding Problems**: Make sure files use UTF-8 encoding
- **Large Files**: Break down large files into smaller chunks for translation
- **Complex Code**: Manually review translations of complex or critical code sections
- **Import Errors**: Check import statements after translation, especially when file names change

## Future Enhancements

- Batch translation of multiple files
- Progress tracking and reporting
- Terminology consistency verification
- Integration with version control systems
- Advanced detection for Portuguese patterns in code

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
