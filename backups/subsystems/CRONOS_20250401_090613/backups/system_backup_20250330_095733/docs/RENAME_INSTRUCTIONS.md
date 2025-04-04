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

markdown
# Project Renaming Instructions



## Problem

The use of the special character `&` in the directory name `Eva & Guarani - EGOS` is causing problems on Windows, including:

- Import errors

- Character issues in logs

- Path difficulties in scripts



## Solution

Rename the directory to `Eva and Guarani - EGOS`, replacing the `&` symbol with `and`.



## Steps Already Completed

1. ✅ The script `rename_project.ps1` was executed to update all references in the files

2. ✅ Import error in `api_adapter.py` was fixed

3. ✅ Batch file to rename the directory was created



## Next Steps

1. Close all programs that might be accessing any project files:

   - Code editor

   - PowerShell terminal

   - Any other application using project files



2. Run the `rename_directory.bat` file **as administrator**:

   - Right-click on it

   - Select "Run as administrator"



3. After renaming:

   - Open the project in the new folder `C:\Eva and Guarani - EGOS`

   - Run the `setup_and_start.ps1` file to check if all issues have been resolved



## Possible Issues

If you encounter problems after renaming:

- Check for absolute paths in configuration files

- Look for references to the old name that may not have been updated

- Check log files to identify possible errors



## Backup

All original files are preserved. If necessary, you can restore the original version from the `backup_20250301_171540` directory or any other backup.
