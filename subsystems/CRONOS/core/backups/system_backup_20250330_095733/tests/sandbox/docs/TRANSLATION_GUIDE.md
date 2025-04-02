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

# EVA & GUARANI - Translation Guide

This guide provides instructions for translating the EVA & GUARANI project files from Portuguese to English, ensuring consistency and preserving functionality throughout the codebase.

## Translation Tools

The EVA & GUARANI project includes several tools to facilitate translation:

1. **Portuguese File Scanner (`translate_to_english.py`)**
   - Scans the codebase to identify files containing Portuguese content
   - Generates a report listing files that need translation
   - Excludes system directories and non-project files

2. **AI-Assisted Translator (`ai_translate_file.py`)**
   - Uses OpenAI's models to translate individual files
   - Preserves code structure and functionality
   - Creates backups of original files

3. **Translation Tools Launcher**
   - Windows Batch script: `translate_tools.bat`
   - PowerShell script: `translate_tools.ps1`
   - Provides a user-friendly interface for running translation tools

## Setup and Requirements

### Required Packages

```
openai>=1.0.0
```

### API Key Setup

For AI-assisted translation, you need an OpenAI API key:

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Set it as an environment variable:

   ```
   # Windows
   set OPENAI_API_KEY=your-api-key
   
   # PowerShell
   $env:OPENAI_API_KEY="your-api-key"
   ```

3. Or pass it directly when running the tool with `--api-key`

## Translation Process

### 1. Scan the Project

First, identify files containing Portuguese content:

```
# Using PowerShell script
.\translate_tools.ps1
# Choose option 1 to scan

# Using Python directly
python translate_to_english.py --root-dir "C:\Eva & Guarani - EGOS"
```

This generates a `translation_report.md` file with a list of files requiring translation.

### 2. Prioritize Files

Translate files in this recommended order:

1. Documentation (`README.md`, guide files)
2. Configuration files
3. Core modules
4. Integration and utility scripts
5. Test files

### 3. Translate Files

Translate individual files using the AI translation tool:

```
# Using PowerShell script
.\translate_tools.ps1
# Choose option 2 to translate

# Using Python directly
python ai_translate_file.py --file "path/to/file.py"
```

### 4. Review and Verify

After translation:

- Check that code still functions correctly
- Verify that translated file names and imports are consistent
- Update any references to the file in other parts of the codebase

## Translation Guidelines

### General Principles

- Maintain code functionality and structure
- Keep consistent naming conventions
- Follow Python PEP 8 style guide for Python files
- Preserve documentation structure and formatting

### Code Elements to Translate

- Comments and docstrings
- Variable, function, and class names (if in Portuguese)
- String literals meant for user display
- Documentation and markdown files

### Elements NOT to Translate

- Reserved keywords
- Library and package names
- Standard programming terms
- Code that would break functionality if changed

### File Naming Conventions

- Use lowercase with underscores for Python files
- Use kebab-case for documentation and web files
- Maintain consistent naming patterns within modules

## Troubleshooting

### Common Issues

- **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient credits
- **Character Encoding**: Files should use UTF-8 encoding
- **Backup Failures**: Check write permissions in your directories
- **Import Errors**: After renaming files, update all import statements

### Getting Help

For additional assistance, check:

- Project documentation in the `docs` directory
- GitHub repository issues
- Contact the project maintainers

## Translation Progress Tracking

The translation scanner creates a report showing:

- Total files requiring translation
- Translation progress percentage
- Files grouped by type and priority

Check the `translation_report.md` file after each scan to monitor progress.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
