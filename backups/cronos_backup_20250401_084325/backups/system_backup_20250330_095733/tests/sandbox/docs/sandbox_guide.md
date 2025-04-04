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

# EVA & GUARANI - Sandbox Environment Guide

## Overview

This guide provides step-by-step instructions for setting up and using the EVA & GUARANI sandbox environment on Windows 11 with PowerShell. The sandbox is a self-contained environment for experimenting with EVA & GUARANI's core modules and features without affecting the main project files.

## Prerequisites

- Windows 11
- PowerShell 7.0 or newer (PowerShell Core preferred)
- Python 3.8 or newer
- Git (optional, for version control)

## Setup Instructions

### 1. Open PowerShell

- Press `Win + X` and select "Windows Terminal" or "PowerShell"
- Ensure you're running PowerShell and not Command Prompt by checking the prompt or typing:

  ```powershell
  $PSVersionTable
  ```

### 2. Navigate to Project Directory

```powershell
cd "C:\Path\to\Eva & Guarani - EGOS"
```

### 3. Configure the Sandbox Environment

Run the setup script to create the necessary directories and files:

```powershell
cd sandbox
python setup_sandbox.py
```

The script will create the following structure:

- `/api` - API implementations
- `/frontend` - Web interfaces
- `/examples` - Integration examples
- `/data` - Test data files
- `/docs` - Documentation

### 4. Install Dependencies

```powershell
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### 5. Start the Sandbox

Using the provided batch script:

```powershell
.\run_sandbox.bat
```

Or directly with Python:

```powershell
python run_sandbox.py
```

## Using the Sandbox

### Web Interface

After starting the sandbox, open a web browser and navigate to:

```
http://localhost:5000
```

The web interface provides:

- Status overview of all modules
- Interactive visualization of ATLAS module data
- Component inspection from NEXUS module
- Backup management from CRONOS module
- Ethical principles from ETHIK module
- Data integration testing

### API Endpoints

The sandbox provides the following REST API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | System status and module availability |
| `/api/atlas` | GET | ATLAS module data (systemic cartography) |
| `/api/nexus` | GET | NEXUS module data (modular analysis) |
| `/api/cronos` | GET | CRONOS module data (evolutionary preservation) |
| `/api/ethik` | GET | ETHIK module data (integrated ethics) |
| `/api/integrate` | POST | Process data through available modules |

Example API call using PowerShell:

```powershell
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/status" -Method Get
$response | ConvertTo-Json
```

### Integration Examples

Explore integration examples in the `/examples` directory:

```powershell
cd examples
python basic_integration.py
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in the environment variables:

   ```powershell
   $env:FLASK_PORT=5001
   python run_sandbox.py
   ```

2. **Module import errors**
   - The sandbox uses simulated data by default
   - Check core module path configuration in `run_sandbox.py`

3. **Dependency errors**
   - Ensure all dependencies are installed:

   ```powershell
   pip install -r requirements.txt
   ```

4. **CORS issues when testing API**
   - The API has CORS enabled by default for development
   - For production, modify CORS settings in `app.py`

## Advanced Usage

### Environment Variables

The sandbox supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_DEBUG` | Enable debug mode | `False` |
| `FLASK_HOST` | Host to bind the server | `127.0.0.1` |
| `FLASK_PORT` | Port to bind the server | `5000` |

Set these in PowerShell before running:

```powershell
$env:FLASK_DEBUG="True"
$env:FLASK_HOST="0.0.0.0"  # Allow external connections
$env:FLASK_PORT="5001"
python run_sandbox.py
```

### Integrating with Core Modules

When core modules are available, the sandbox will detect and use them automatically. Place or link the modules in the following structure:

```
/core
  /atlas
    __init__.py
    atlas_core.py
  /nexus
    __init__.py
    nexus_core.py
  /cronos
    __init__.py
    cronos_core.py
  /ethik
    __init__.py
    ethik_core.py
```

## Additional Resources

- [EVA & GUARANI Documentation](../docs/README.md)
- [API Reference](../api/README.md)
- [Frontend Documentation](../frontend/README.md)
