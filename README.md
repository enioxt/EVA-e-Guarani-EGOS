# EVA & GUARANI
Version: 8.1
Last Updated: 2025-04-04

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

### ATLAS
Advanced Topological Learning and Analysis System
- System cartography
- Connection mapping
- Visual analytics
- Pattern recognition

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

### HARMONY
Cross-Platform Integration and Compatibility System
- Ensures seamless operation across different environments
- Manages platform-specific adaptations
- Facilitates consistent user experience

### KOIOS
Knowledge Organization and Integration Operating System
- ✓ Centralized metadata management
- ✓ Schema validation
- ✓ File monitoring
- ✓ Data preservation
- Advanced search capabilities (in development)

### CORUJA
AI Communication & Integration Enhancement System
- Standardizes AI integration patterns
- Improves human-AI & AI-AI communication
- Defines interaction protocols and guidelines

### NEXUS
Neural Evolution and Cross-system Unification System
- Module analysis
- Code optimization
- Integration management
- Performance monitoring

### TRANSLATOR
Language and Protocol Translation System
- Facilitates communication between different components
- Handles data format conversions
- Bridges language barriers within the system

### MYCELIUM
Neural Network Communication System
- Facilitates subsystem communication
- Handles message routing
- Manages connection states
- Enables event-driven architecture

## Project Structure

The project follows a structured layout to separate concerns and facilitate collaboration:

-   **`/` (Root):** Contains core configuration (`requirements.txt`, `pyproject.toml`), main documentation (`README.md`), the primary project roadmap (`ROADMAP.md`), and entry points.
-   **`BIOS-Q/`:** Houses the core Python **implementation** of the Basic Input/Output System - Quantum, including its configuration (`config/`), runtime resources (`resources/`), state (`quantum_state.json`), and logs (`logs/`).
-   **`subsystems/`:** Contains the primary Python **implementation code** for each distinct functional subsystem (e.g., `ATLAS/`, `CRONOS/`, `ETHIK/`, `HARMONY/`, `KOIOS/`, `CORUJA/`, `NEXUS/`, `TRANSLATOR/`, `MYCELIUM/`). Each subsystem typically has a `core/` directory structure within it and may contain its own local `roadmap.md`.
    -   **Standard Subsystem Structure:**
        ```
        subsystems/<SUBSYSTEM>/
          ├── __init__.py         # Module definition
          ├── README.md           # Subsystem documentation
          ├── core/               # Core logic implementation
          ├── service.py          # Service layer orchestration (optional)
          ├── interfaces/         # Interface definitions (optional)
          ├── tests/              # Unit and integration tests
          ├── config/             # Specific configurations (optional)
          └── resources/          # Additional resources (optional)
        ```
-   **`src/`:** Contains shared source code, utilities, web components, assets, templates, and potentially core modules not large enough to be full subsystems.
-   **`scripts/`:** Provides utility scripts for development, maintenance, testing, deployment, and metadata management.
-   **`docs/`:** Houses documentation, including planning documents (`docs/planning/`), temporary files (`docs/temp/`), and archived materials (`docs/archive/`).
-   **`logs/`:** Contains system and subsystem logs, including translation logs and process monitoring.
-   **`research/`:** Stores research documents, analysis notes, and related materials.
-   **`external/`:** Contains external resources and temporary files not part of the core codebase.
-   **`.cursor/`:** Contains configuration for Cursor IDE integration and MCP connections.
-   **`.metadata/`:** (If using centralized DB) Stores the centralized metadata database (`metadata_db.json`).

This structure aims for clarity by separating core system implementation (BIOS-Q), subsystem implementations (subsystems), shared code (src), utilities (scripts), documentation (docs), and research notes (research).

## Current Status

### Completed Features
- ✓ Core system implementation (initial structures)
- ✓ English language standardization (ongoing)
- ✓ Documentation structure (foundational)
- ✓ Directory organization (major refactoring done)
- ✓ Metadata system centralization (via KOIOS)
- ✓ Schema implementation (initial KOIOS)
- ✓ Core utility scripts (various)
- ✓ Integration features (basic SLOP, MCP)
- ✓ Monitoring system (basic metrics in SLOP)
- ✓ Mycelium Network (Core Python classes & routing logic implemented & tested)
- ✓ KoiosLogger Integration (CRONOS, NEXUS, ETHIK)

### In Progress
- [ ] System Standardization (KOIOS - CRITICAL)
- [ ] KOIOS Evolution (CRITICAL)
- [ ] Mycelium Network (Integration Phase - CRITICAL)
- [ ] CORUJA Subsystem (Initialization Phase - HIGH)
- [ ] HARMONY Subsystem (Initialization Phase - MEDIUM)
- [ ] TRANSLATOR Subsystem (Initialization Phase - MEDIUM)
- [ ] ETHIK Enhancements (HIGH)
- [ ] ETHICHAIN Development (HIGH)
- [ ] Legacy system migration (low priority)
- [ ] Cross-system integration (via Mycelium)
- [ ] Unified testing framework (ongoing)
- [ ] Process optimization (via KOIOS)

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
- `/subsystems/*/docs/` or `/subsystems/*/README.md` - Subsystem-specific documentation

## Development

### Core Principles
1. English-only implementation
2. Comprehensive documentation
3. Test-driven development
4. Security-first approach
5. Quantum consciousness integration

### Implementation Standards & Conventions

1.  **Documentation**: Each file must include a header with metadata (use KOIOS standards) and a descriptive docstring.
2.  **Typing**: Utilize Python's static typing for all function signatures and variable annotations.
3.  **Tests**: Implement comprehensive unit and integration tests for all functionalities. Aim for high test coverage.
4.  **Logging**: Utilize the centralized `KoiosLogger` for all logging activities. Avoid standard `print` statements for operational logging.
5.  **Configuration**: Separate configuration from code. Load configurations from files (e.g., JSON, YAML) within the `config/` directory (either root or subsystem-specific).
6.  **Naming Conventions**:
    *   Packages and modules: `snake_case`
    *   Classes: `PascalCase`
    *   Functions and variables: `snake_case`
    *   Constants: `UPPER_SNAKE_CASE`
7.  **Code Structuring**:
    *   Organize code into small, focused functions and classes.
    *   Adhere to SOLID principles.
    *   Follow PEP 8 guidelines.

### Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) (if available) or adhere to the standards defined here and in KOIOS documentation for details on our code of conduct and the process for submitting pull requests.

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
