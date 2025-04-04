---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: docs
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

# EVA & GUARANI Translation Strategy

> "Building a universal ethical quantum system with a consistent English foundation."

## Overview

This document outlines the strategy for standardizing the EVA & GUARANI project to use English exclusively across all code, documentation, and user interfaces. This transition is a foundational step in making the project more accessible to a global audience and establishing consistent development practices.

## Translation Goals

- **Consistent Language**: Standardize all code, comments, documentation, and interfaces to English
- **Preserve Functionality**: Ensure all translations maintain the original code behavior and intent
- **Improve Accessibility**: Make the project accessible to non-Portuguese speaking contributors
- **Establish Best Practices**: Create guidelines for future development in English
- **Maintain Cultural Essence**: Preserve the unique cultural and philosophical identity of EVA & GUARANI

## Translation Tools

We have developed specialized tools to assist with the translation process, available in the `sandbox/tools` directory:

- **translate_to_english.py**: Identifies files containing Portuguese content
- **ai_translate_file.py**: Uses AI to assist with translating files while preserving code structure
- **translate_sandbox.bat**: Provides a user-friendly interface for running the translation tools (Windows batch script)
- **translate_tools.ps1**: Enhanced PowerShell script with additional features (recommended for Windows 11)

See the [Translation Guide](./sandbox/docs/TRANSLATION_GUIDE.md) for detailed instructions on using these tools.

## Translation Process

The translation process follows these key phases:

1. **Discovery**: Scan the codebase to identify all files containing Portuguese content
2. **Prioritization**: Prioritize files for translation based on importance and dependencies
3. **Translation**: Translate files while preserving code structure and functionality
4. **Validation**: Test translated code to ensure it works correctly
5. **Documentation**: Update references and documentation to reflect the changes

## Translation Status

Current translation status:

- 📊 **Tools Created**: Translation tools have been developed and tested
- 🔍 **Discovery Phase**: Initial scanning to identify Portuguese files (in progress)
- 📝 **Documentation**: Translation guidelines established
- 🛠️ **Core Modules**: Translation of core modules (pending)
- 📋 **Configuration Files**: Translation of configuration files (pending)
- 🧪 **Testing**: Validation of translated code (pending)

## Getting Started with Translation

To help with the translation effort:

1. Set up the sandbox environment

   ```bash
   cd sandbox
   python setup_sandbox_env.py  # Installs dependencies and prepares the environment
   ```

2. Run the translation tools to identify files for translation:

   ```bash
   # For Windows PowerShell (recommended):
   cd sandbox/tools
   .\translate_tools.ps1

   # OR using batch script:
   cd sandbox/tools
   translate_sandbox.bat

   # OR directly using Python:
   cd sandbox/tools
   python translate_to_english.py --root-dir "../../"
   ```

3. Review the generated report and prioritize files for translation

4. Use the AI-assisted translation tool for initial translations:

   ```bash
   python ai_translate_file.py "path/to/file.py"
   ```

5. Review and validate the translations

6. Test the functionality of translated code

7. Update any references to renamed elements

## Translation Best Practices

When translating code and documentation:

- Maintain consistent terminology throughout the codebase
- Preserve code structure and formatting
- Translate variable and function names only when they are in Portuguese
- Use idiomatic English for comments and documentation
- Maintain the philosophical concepts and unique identity of EVA & GUARANI
- Validate that translated code functions identically to the original

## Conclusion

The standardization to English is a vital step in making EVA & GUARANI accessible to a global audience while maintaining its unique vision. By following this translation strategy, we ensure that the project's core values and functionality are preserved while improving its reach and collaborative potential.

## Resources

- [Detailed Translation Guide](./sandbox/docs/TRANSLATION_GUIDE.md)
- [Implementation Roadmap](./sandbox/docs/IMPLEMENTATION_ROADMAP.md)
- [System Analysis](./sandbox/docs/SYSTEM_ANALYSIS.md)

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
