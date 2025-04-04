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

# EVA & GUARANI - Optimized Workspace Guide

## Introduction

This guide explains how to work efficiently with the EVA & GUARANI project, especially when dealing with large directories like `docs` and `eva-atendimento`. The project has been optimized to improve performance by excluding these directories from automatic indexing.

## Getting Started

1. **Use the project launcher:**

   ```
   # Windows
   start_project.bat

   # Unix/macOS
   python start_project.py
   ```

   This script will:
   - Check if your large directories are properly handled
   - Clean temporary files
   - Open Cursor/VSCode with the optimized workspace settings

2. **Or open the project using the workspace file directly:**

   ```
   File > Open Workspace from File... > eva_guarani.code-workspace
   ```

## Working with Large Directories

The project contains very large directories that can slow down indexing and autocomplete:

- `docs` - Contains project documentation
- `eva-atendimento` - Contains the attendance application
- `modules` - Contains various module directories

### Managing Large Directories

We've created tools to help you work with these directories without slowing down your development:

1. **Reference Management Tool**

   This tool lets you move large directories outside your workspace while maintaining access through symbolic links.

   ```bash
   # Setup reference directories
   python tools/manage_references.py setup

   # Move the docs folder (this will create a symlink)
   python tools/manage_references.py move docs ../EVA_REFS/docs

   # Move the eva-atendimento folder
   python tools/manage_references.py move eva-atendimento ../EVA_REFS/apps
   ```

   For Windows users, run the PowerShell script as Administrator:

   ```
   Right-click on tools/setup_references.ps1 > Run as Administrator
   ```

2. **Module Management Tool**

   This tool helps you enable/disable specific modules when you need them:

   ```bash
   # List all modules and their sizes
   python tools/manage_modules.py list --details

   # Disable modules you don't need right now
   python tools/manage_modules.py disable blockchain

   # Enable a module when you need to work with it
   python tools/manage_modules.py enable blockchain

   # Work with module groups
   python tools/manage_modules.py group list
   python tools/manage_modules.py group disable specialized
   python tools/manage_modules.py group enable core

   # Save your current module configuration as a profile
   python tools/manage_modules.py profile save minimal

   # Load a saved profile later
   python tools/manage_modules.py profile load minimal
   ```

3. **Accessing Documentation**

   After moving the docs, you can still access them through:
   - The symbolic link at the original location
   - Directly at the new location (`../EVA_REFS/docs/docs`)

4. **Working with eva-atendimento**

   When you need to work specifically on the `eva-atendimento` module:
   - Open it directly as a separate workspace
   - Or temporarily remove it from the exclude list in settings

## Workspace Organization

The workspace is organized into focused modules:

- **ATLAS** - Core module for system cartography
- **NEXUS** - Core module for modular analysis
- **CRONOS** - Core module for evolutionary preservation
- **ETHIK** - Core module for ethical guidance
- **TOOLS** - Utility scripts and tools
- **UI** - User interface components
- **MODULES** - Additional system modules
- **INTEGRATIONS** - External system integrations

## Maintenance

To clean up temporary files and improve performance:

```bash
# Analyze project structure
python tools/cleanup.py

# Archive unused directories
python tools/archive_unused.py --list
python tools/archive_unused.py
```

## Best Practices

1. **Always launch the project using start_project.py/bat** - This ensures proper setup
2. **Focus on one module at a time** - This improves performance and focus
3. **Keep large reference directories outside the workspace** - Use the reference management tool
4. **Disable modules you're not actively using** - Use the module management tool
5. **Create module profiles for different tasks** - Save/load module configurations
6. **Clean up regularly** - Remove **pycache** and other temporary files
7. **Use the workspace file** - It contains optimized settings for performance

## Troubleshooting

If you encounter slow performance:

1. Make sure you're using the workspace file
2. Check if large directories are excluded from indexing
3. Disable unused modules using the module management tool
4. Try closing and reopening the workspace
5. Run the cleanup tools to remove temporary files

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
