# EGOS Project Standards (KOIOS v1.0)

**Version:** 1.0
**Last Updated:** 2025-04-02

## 1. Introduction

This document, maintained by the KOIOS subsystem, defines the mandatory coding, documentation, and architectural standards for the EVA & GUARANI (EGOS) project. Adherence to these standards ensures consistency, maintainability, interoperability, and facilitates AI-assisted development.

**All contributions MUST follow these standards.**

## 2. Language

- **Primary Language:** All code, comments, documentation, commit messages, and internal communication MUST be in **English**. This ensures universal accessibility and compatibility with AI tools.

## 3. File Naming Conventions

- **Python Files (`.py`):** Use `snake_case.py` (lowercase with underscores). Example: `atlas_core.py`, `nexus_service.py`.
- **Python Test Files (`.py`):** Prefix with `test_`. Example: `test_atlas_core.py`.
- **Markdown Files (`.md`):** Use `kebab-case.md` (lowercase with hyphens) or `snake_case.md` for general documentation. Use specific names like `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`. Use `UPPERCASE.md` for specific standard documents like `STANDARDS.md`.
- **Configuration Files (`.json`, `.yaml`, etc.):** Use `snake_case.json` or descriptive names. Example: `atlas_config.json`, `mycelium_settings.yaml`.
- **Scripts (`.py`, `.sh`, `.ps1`):** Use `snake_case` or `kebab-case`. Example: `run_tests.sh`, `deploy_service.py`.
- **Directories:** Use `snake_case` (preferred) or `kebab-case` for functional groupings. Use `UPPERCASE` for top-level subsystem names (e.g., `ATLAS`, `NEXUS`).

## 4. Directory Structure (Standard Subsystem Layout)

Each primary subsystem (e.g., ATLAS, NEXUS, ETHIK, CRONOS, KOIOS) located under the main `subsystems/` directory SHOULD adhere to the following structure:

```
subsystems/
  └── SUBSYSTEM_NAME/
      ├── __init__.py       # Makes the subsystem a Python package
      ├── core/             # Core logic, algorithms, main classes
      │   └── __init__.py
      │   └── subsystem_core.py
      │   └── ... (other core modules)
      ├── services/         # Service orchestration, Mycelium integration (Optional)
      │   └── __init__.py
      │   └── service.py
      ├── utils/            # Utility functions specific to the subsystem (Optional)
      │   └── __init__.py
      │   └── helpers.py
      ├── config/           # Default configuration files for the subsystem
      │   └── subsystem_config.json
      ├── data/             # Data generated or used by the subsystem (Add to .gitignore)
      │   └── .gitkeep
      ├── tests/            # Unit and integration tests for the subsystem
      │   ├── __init__.py
      │   └── test_core.py
      │   └── test_service.py
      ├── docs/             # Subsystem-specific documentation
      │   └── README.md     # Overview of this specific subsystem
      │   └── usage.md      # How to use the subsystem
      │   └── api.md        # API documentation (if applicable)
      └── README.md         # Top-level README for the subsystem (may duplicate docs/README.md)
```

**Notes:**

- Optional directories (`services/`, `utils/`) can be omitted if not needed.
- The `core/` directory might contain subdirectories for better organization if the logic is complex.
- The main `README.md` at the subsystem root should provide a concise overview and link to the more detailed documentation in `docs/`.
- Data generated at runtime should go into `data/` and be gitignored.

## 5. Mycelium Topic Naming Conventions

Standardized topics enhance discoverability and routing within the Mycelium network.

**General Format:** `<type>.<source_node>.<action_or_description>`

- **`<type>`:**
    - `request`: A message requesting an action or data.
    - `response`: A reply to a specific `request` message (often includes a request ID).
    - `event`: A notification about something that happened (state change, completion, error).
    - `command`: A directive for a node to perform an action (stronger than `request`).
    - `log`: A structured log message emitted onto the network (optional).
    - `alert`: A high-priority notification requiring attention.
- **`<source_node>`:** The unique ID of the node publishing the message (e.g., `NEXUS_SERVICE`, `ATLAS_CORE`, `ETHIK_VALIDATOR`). Use uppercase snake_case.
- **`<action_or_description>`:** Lowercase snake_case describing the purpose.
    - For `request`: Verb describing the request (e.g., `analyze_workspace`, `get_status`).
    - For `response`: Usually includes the original request ID (e.g., `request_id_123`).
    - For `event`: Past tense description (e.g., `analysis_complete`, `status_updated`, `error_occurred`).
    - For `command`: Verb describing the command (e.g., `start_scan`, `shutdown`).
    - For `log`: Log level (e.g., `info`, `warning`, `error`).
    - For `alert`: Severity level (e.g., `critical`, `high`, `medium`).

**Wildcard Subscriptions:** Components can use wildcards (`*` for single level, `>` for multiple levels) to subscribe to patterns.

**Examples:**

- `request.NEXUS_SERVICE.analyze_workspace`
- `response.NEXUS_SERVICE.req_abc123`
- `event.CRONOS_SERVICE.backup_complete`
- `event.ATLAS_CORE.map_updated`
- `command.BIOS_Q.shutdown_subsystem`
- `log.ETHIK_VALIDATOR.warning`
- `alert.ETHIK_VALIDATOR.critical`

**Response Topic Convention:**
Responses to requests should typically be published on a topic specific to the request ID:
`response.<service_node>.<request_id>`

## 6. Code Style (Python - PEP 8)

- All Python code MUST adhere to [PEP 8](https://peps.python.org/pep-0008/).
- Use automated tools like `black`, `ruff`, or `flake8` to enforce style consistency. Configuration for these tools should be included in the project root (`pyproject.toml`).
- Maximum line length: 100-120 characters (to be finalized).

## 7. Documentation Standards

- **Docstrings:** All public modules, classes, functions, and methods MUST have docstrings following [PEP 257](https://peps.python.org/pep-0257/) (e.g., Google style or NumPy style).
- **READMEs:** Each subsystem MUST have a `README.md` explaining its purpose, structure, configuration, and usage.
- **Inline Comments:** Use comments sparingly to explain *why* something is done, not *what* it does (the code should be clear).

## 8. Metadata Standards

- **Markdown Files:** Documentation files (`.md`) SHOULD include a YAML front matter block for metadata.
- **Schema:** (To be defined in detail later by KOIOS). Will include fields like `subsystem`, `version`, `status`, `author`, `last_updated`, `dependencies`, `type`, `ethical_validation`, `test_coverage`, etc.

## 9. Logging Standards

- **Framework:** Use Python's built-in `logging` module.
- **Logger Naming:** Obtain loggers using `logging.getLogger("SUBSYSTEM_NAME.ModuleName")` or similar hierarchical names (e.g., `EGOS.ATLAS.Core`).
- **Format:** (To be finalized, implemented by `KoiosLogger`). Should include timestamp, log level, logger name, and message. Structured logging (JSON) is preferred for potential aggregation.
- **Levels:** Use standard logging levels appropriately (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- **Mycelium Logging:** Consider emitting important logs (especially warnings/errors) as `log.<source_node>.<level>` events on Mycelium for system-wide visibility.

## 10. Testing Standards

- **Framework:** Use `pytest`.
- **Location:** Tests for a module/subsystem reside in its `tests/` directory.
- **Naming:** Test files MUST start with `test_`, test functions MUST start with `test_`.
- **Coverage:** Aim for high test coverage (target: 85%+). Use `pytest-cov`.
- **Types:** Include unit tests, integration tests (where applicable), and potentially service-level tests.

## 11. Commit Messages

- Follow [Conventional Commits](https://www.conventionalcommits.org/) specification. Example: `feat(NEXUS): add AST parsing for function analysis` or `fix(ATLAS): correct layout calculation error`.

---

✧༺❀༻∞ KOIOS - EGOS Standards Authority ∞༺❀༻✧ 