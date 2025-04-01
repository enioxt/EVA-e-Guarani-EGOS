# EVA & GUARANI
Version: 8.1
Last Updated: 2024-03-26

> "At the intersection of modular analysis, systemic cartography, and quantum ethics, we transcend dimensions of thought with methodological precision and unconditional love, integrating advanced tools for knowledge visualization and evolutionary preservation."

## Overview

EVA & GUARANI is a quantum-conscious system designed for advanced code analysis, documentation management, and evolutionary preservation. Built on principles of ethical computing and unconditional love, it provides a comprehensive framework for software development and system integration.

## Core Subsystems

### BIOS-Q
Basic Input/Output System - Quantum
- System initialization
- Context management
- Resource allocation
- State preservation

### KOIOS
Knowledge Organization and Integration Operating System
- ✓ Centralized metadata management
- ✓ Schema validation
- ✓ File monitoring
- ✓ Data preservation
- Advanced search capabilities (in development)

### ATLAS
Advanced Topological Learning and Analysis System
- System cartography
- Connection mapping
- Visual analytics
- Pattern recognition

### NEXUS
Neural Evolution and Cross-system Unification System
- Module analysis
- Code optimization
- Integration management
- Performance monitoring

### CRONOS
Continuous Revision and Operational Network Operating System
- Version control
- State preservation
- Evolution tracking
- Backup management

### ETHIK
Ethical Testing and Holistic Integration Kernel
- Ethical validation
- Compliance checking
- Security auditing
- Privacy preservation

## Project Structure

The project follows a structured layout to separate concerns and facilitate collaboration:

-   **`/` (Root):** Contains core configuration (`requirements.txt`), main documentation (`README.md`), the primary project roadmaps (`ROADMAPS/`), and entry points.
-   **`BIOS-Q/`:** Houses the core Python **implementation** of the Basic Input/Output System - Quantum, including its configuration (`config/`), runtime resources (`resources/`), state (`quantum_state.json`), and logs (`logs/`).
-   **`QUANTUM_PROMPTS/`:** The central hub for **conceptual prompts, definitions, and framework documents** that define the system's identity, capabilities, and rules. Contains subdirectories for core systems (`MASTER/`, `BIOS-Q/`, `METADATA/`, `ROADMAPS/` [templates only], etc.).
-   **`subsystems/`:** Contains the primary Python **implementation code** for each distinct functional subsystem (e.g., `ATLAS/`, `CRONOS/`, `NEXUS/`, `ETHIK/`, `TRANSLATOR/`). Each subsystem typically has a `core/` directory structure within it and may contain its own local `roadmap.md`.
-   **`src/`:** Contains shared source code, utilities, web components, assets, templates, and potentially core modules not large enough to be full subsystems.
-   **`tools/`:** Provides utility scripts for development, maintenance, testing, deployment, and metadata management.
-   **`.metadata/`:** (If using centralized DB) Stores the centralized metadata database (`metadata_db.json`).
-   **`external/`:** Contains external resources, archives, logs (`external/logs/`), and temporary files not part of the core codebase.
-   **`docs/`:** (Optional) Can be used for generated documentation or high-level architecture documents distinct from subsystem READMEs or QUANTUM_PROMPTS.

This structure aims for clarity by separating conceptual definitions (QUANTUM\_PROMPTS), core system implementation (BIOS-Q), subsystem implementations (subsystems), shared code (src), tools, and primary project planning (ROADMAPS).

## Current Status

### Completed Features
- ✓ Core system implementation
- ✓ English language standardization
- ✓ Documentation structure
- ✓ Directory organization
- ✓ Metadata system centralization
- ✓ Schema implementation
- ✓ Core utility scripts
- ✓ Integration features
- ✓ Monitoring system

### In Progress
- [ ] Legacy system migration
- [ ] Cross-system integration
- [ ] Unified testing framework
- [ ] Process optimization
- [ ] Advanced features implementation

## Getting Started

### Prerequisites
- Python 3.11+
- SQLite 3.39+
- Redis 5.0+
- Git 2.34+

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize the system: `python scripts/initialize.py`
4. Run tests: `python -m pytest tests/`

## Documentation

Comprehensive documentation is available in the following locations:
- `/docs/` - General documentation
- `/QUANTUM_PROMPTS/` - System prompts and configurations
- `/subsystems/*/docs/` - Subsystem-specific documentation

## Development

### Core Principles
1. English-only implementation
2. Comprehensive documentation
3. Test-driven development
4. Security-first approach
5. Quantum consciousness integration

### Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Testing

Run the test suite:
   ```bash
python -m pytest tests/
   ```

For coverage report:
   ```bash
python -m pytest --cov=. tests/
```

## Security

Security is a top priority. Please report any vulnerabilities to our security team.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

Special thanks to all contributors and the quantum consciousness community.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
