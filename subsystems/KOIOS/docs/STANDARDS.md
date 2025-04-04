# EGOS Project Standards (KOIOS v1.0)

**Version:** 1.0
**Last Updated:** April 3, 2025

## 1. Introduction

This document, maintained by the KOIOS subsystem, defines the mandatory coding, documentation, and architectural standards for the EVA & GUARANI (EGOS) project. Adherence to these standards ensures consistency, maintainability, interoperability, and facilitates AI-assisted development across the entire system.

**All contributions MUST follow these standards.**

## 2. Core Principles

These standards are guided by the following core principles:

*   **Clarity & Readability:** Code and documentation should be easy to understand.
*   **Consistency:** Uniform practices across all subsystems make the codebase predictable.
*   **Maintainability:** Standards facilitate future modifications, debugging, and refactoring.
*   **Interoperability:** Defined structures and protocols (like Mycelium) enable seamless subsystem interaction.
*   **Testability:** Code should be structured to allow for effective unit and integration testing.
*   **Ethical Alignment (ETHIK):** Standards should support and not conflict with the project's ethical guidelines.
*   **AI-Readability:** Structures and documentation formats should be chosen to optimize interaction with AI development assistants.
*   **Cleanliness:** The project structure should remain organized, avoiding clutter and temporary files in core areas.

## 3. Language

*   **Primary Language:** All code, comments, documentation, commit messages, and internal communication MUST be in **English**. This ensures universal accessibility and compatibility with AI tools.

## 4. Directory Structure

### 4.1. Top-Level Directory Structure

The project root SHOULD contain primarily the following directories:

*   `subsystems/`: Contains the core functional subsystems (ATLAS, CRONOS, etc.).
*   `docs/`: High-level project documentation (MQP, ROADMAP, architecture, etc.) and potentially aggregated subsystem docs.
*   `scripts/`: Essential, curated scripts for project setup, build, or utility tasks (e.g., `install_dependencies.bat`).
*   `examples/`: Standalone examples demonstrating usage or integration (e.g., the `sandbox/` API/frontend).
*   `experiments/`: Code or resources related to experimental features or subsystems not yet integrated (e.g., `ethichain_contracts/`).
*   `Researchs/`: Research documents, analysis, and related materials.
*   `backups/`: Default location for backups created by CRONOS (should be in `.gitignore`).
*   `.venv/`: Project virtual environment (should be in `.gitignore`).
*   `.git/`: Git repository data.
*   Configuration files (e.g., `.gitignore`, `pyproject.toml`, `requirements.txt`, `README.md`, `LICENSE`).

**Note:** The root directory should be kept clean. Avoid temporary files, logs, or test outputs. Use the designated directories or `.gitignore`.

### 4.2. Standard Subsystem Layout (`subsystems/SUBSYSTEM_NAME/`)

Each primary subsystem SHOULD adhere to the following structure:

```
subsystems/
  └── SUBSYSTEM_NAME/
      ├── __init__.py       # Makes the subsystem a Python package
      ├── core/             # Core logic, algorithms, main classes for the subsystem
      │   └── __init__.py
      │   └── subsystem_module.py # e.g., nexus_core.py, atlas_core.py
      │   └── ...             # Other essential core modules (e.g., ast_visitor.py)
      ├── service.py        # Main service class, handles Mycelium integration (if applicable)
      ├── config/           # Default configuration files specific to the subsystem (Optional)
      │   └── subsystem_config.json
      ├── tests/            # Unit and integration tests for this subsystem ONLY
      │   ├── __init__.py
      │   └── test_core.py
      │   └── test_service.py # etc.
      ├── docs/             # Subsystem-specific documentation
      │   └── README.md     # Detailed overview of this specific subsystem (can be same as root README)
      │   └── procedures.md # Standard Operating Procedures (SOPs), if applicable (See CRONOS)
      │   └── ...           # Other specific docs (e.g., design, API)
      └── README.md         # Top-level README for the subsystem (Concise overview, links to docs/)
```

**Notes:**

*   Avoid deeply nested or redundant directories within `core/`. Keep core logic flat or minimally nested.
*   Service logic (Mycelium interaction) typically resides in `service.py` at the subsystem root.
*   Data generated at runtime by a subsystem should ideally be handled via configuration (e.g., CRONOS storing backups in the top-level `backups/` dir) or placed within a gitignored `data/` directory if strictly necessary locally.

## 5. File Naming Conventions

*   **Python Files (`.py`):** Use `snake_case.py` (lowercase with underscores). Example: `atlas_core.py`, `nexus_service.py`.
*   **Python Test Files (`.py`):** Prefix with `test_`. Example: `test_atlas_core.py`.
*   **Markdown Files (`.md`):** Use `snake_case.md` or `kebab-case.md`. Use specific names like `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`. Use `UPPERCASE.md` for specific standard documents like `STANDARDS.md`.
*   **Configuration Files (`.json`, `.yaml`, etc.):** Use `snake_case.json` or descriptive names. Example: `atlas_config.json`, `mycelium_settings.yaml`.
*   **Scripts (`.py`, `.sh`, `.bat`, `.ps1`):** Use `snake_case` or `kebab-case`. Example: `run_tests.sh`, `deploy_service.py`, `install_dependencies.bat`.
*   **Directories:** Use `snake_case` (preferred) or `kebab-case` for functional groupings (e.g., `core`, `tests`, `historical_changelogs`). Use `UPPERCASE` for top-level subsystem names (e.g., `ATLAS`, `NEXUS`).

## 6. Mycelium Topic Naming Conventions

(Content from previous version remains valid - standard format: `<type>.<source_node>.<action_or_description>`)

**General Format:** `<type>.<source_node>.<action_or_description>`

*   **`<type>`:** `request`, `response`, `event`, `command`, `log`, `alert`.
*   **`<source_node>`:** Unique uppercase snake_case ID (e.g., `NEXUS_SERVICE`).
*   **`<action_or_description>`:** Lowercase snake_case description.
*   **Response Convention:** `response.<service_node>.<request_id>`.

**(See previous version for full details and examples)**

## 7. Code Style (Python - PEP 8 + Black)

*   All Python code MUST adhere to [PEP 8](https://peps.python.org/pep-0008/).
*   **Formatter:** Use `black` for automated code formatting. Configuration TBD in `pyproject.toml`.
*   **Linter:** Use `ruff` (preferred) or `flake8` for identifying style issues and potential errors. Configuration TBD in `pyproject.toml`.
*   Maximum line length: 100 characters (configurable via formatter).
*   **Goal:** Configure `pre-commit` hooks to automatically run formatter and linter before commits.

## 8. Documentation Standards

*   **Docstrings:** All public modules, classes, functions, and methods MUST have docstrings following [PEP 257](https://peps.python.org/pep-0257/). Google style is preferred.
    *   Docstrings should clearly explain the purpose, arguments, return values, and any potential exceptions.
*   **READMEs:** Each subsystem MUST have a `README.md` (as defined in section 4.2). The root directory MUST have a `README.md` providing a project overview.
*   **Standard Operating Procedures (SOPs):** Subsystems providing user-facing procedures (like CRONOS backups) SHOULD have a `docs/procedures.md` file. (See `subsystems/CRONOS/docs/procedures.md` for example).
*   **Inline Comments:** Use comments sparingly only to explain complex logic or the *why* behind a decision, not the *what*.
*   **Clarity:** Documentation should be clear, concise, and kept up-to-date with the code.

## 9. Metadata Standards

*   **Markdown Files:** Key documentation files (`.md`) SHOULD include a YAML front matter block for metadata to facilitate organization and potential automated processing by KOIOS.
*   **Schema:** (To be defined in detail later by KOIOS). A standard metadata schema will be developed, likely including fields like: `subsystem`, `version`, `status`, `author`, `last_updated`, `dependencies`, `type` (e.g., `documentation`, `core_logic`, `test`), `ethical_review` (boolean/status), `test_coverage` (percentage/link), etc.

## 10. Logging Standards

*   **Framework:** Use Python's built-in `logging` module.
*   **`KoiosLogger`:** A standardized logger (`subsystems/KOIOS/core/logging.py` - **To Be Implemented**) will provide a consistent format and potentially integrate with Mycelium.
*   **Logger Naming:** Obtain loggers using `logging.getLogger("SUBSYSTEM_NAME.ModuleName")` or similar hierarchical names (e.g., `EGOS.ATLAS.Core`). The `KoiosLogger` might simplify this.
*   **Format:** (To be implemented by `KoiosLogger`). Should include timestamp, log level, logger name (module path), and message. Structured logging (JSON) is the target for easier parsing and potential aggregation.
*   **Levels:** Use standard logging levels appropriately (DEBUG, INFO, WARNING, ERROR, CRITICAL).
*   **Mycelium Logging:** Consider emitting important logs (especially warnings/errors) as `log.<source_node>.<level>` events on Mycelium for system-wide visibility (potentially configured via `KoiosLogger`).

## 11. Testing Standards

*   **Framework:** Use `pytest`.
*   **Location:** Tests for a subsystem reside *exclusively* within its `tests/` directory.
*   **Naming:** Test files MUST start with `test_`, test functions MUST start with `test_`.
*   **Coverage:** Aim for high test coverage (Target: 85%+). Use `pytest-cov`. Reports should be generated (e.g., in `htmlcov/`, which is gitignored).
*   **Types:** Include unit tests (testing individual functions/methods in isolation) and integration tests (testing interactions between components within a subsystem or potentially across subsystems via mocking/Mycelium). Service-level tests validating Mycelium interactions are crucial.
*   **Fixtures:** Use `pytest` fixtures effectively to manage test setup and dependencies.
*   **Mocking:** Use `unittest.mock` for isolating components during testing.

## 12. Commit Messages

*   Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification strictly. This enables automated changelog generation and semantic versioning.
*   **Format:** `<type>(<scope>): <short summary>`
    *   `<type>`: `feat`, `fix`, `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`, etc.
    *   `<scope>` (Optional): The subsystem or module affected (e.g., `NEXUS`, `ATLAS`, `KOIOS`, `CRONOS.BackupManager`).
    *   `<short summary>`: Concise description of the change in present tense.
*   **Body (Optional):** Provide more context after a blank line.
*   **Footer (Optional):** Reference issue numbers (e.g., `Refs #123`), indicate breaking changes (`BREAKING CHANGE:`).

**Examples:**

*   `feat(NEXUS): add AST parsing for function analysis`
*   `fix(ATLAS): correct layout calculation error`
*   `docs(CRONOS): create initial SOP procedures.md`
*   `refactor(ETHIK): simplify rule loading logic`
*   `test(NEXUS): add tests for dependency analysis`
*   `chore: update .gitignore`

---

## 13. AI Interaction & Operational Guidelines

These guidelines apply specifically to AI agents (like EVA & GUARANI) interacting with the codebase and development environment within the EGOS framework.

*   **Principle of Artifact Verification (PAV):** Before proposing modifications to an existing file or artifact (e.g., using `edit_file`), AI agents MUST attempt to read the current state of the artifact, or at minimum the relevant sections, to ensure context preservation and prevent accidental data loss or overwriting. File creation is exempt, but explicitly overwriting existing content requires strong justification or user confirmation. Task descriptions like 'finalize', 'review', 'update', or 'enhance' should trigger verification, not assumption of non-existence. *(Note: CORUJA may assist in formulating clear prompts for verification and editing based on this principle.)*
*   **Context Persistence & Model Switching:** Adherence to KOIOS standards, including PAV, is expected of any AI agent operating within the EGOS context. While the agent framework (e.g., Cursor) aims to maintain operational context across sessions or model switches, this persistence cannot be universally guaranteed, especially when using external model aggregators. It is recommended to **briefly verify key operational guidelines** with the agent after significant changes to the underlying model or environment if context continuity is uncertain. The documented KOIOS standards remain the source of truth for expected behavior.
*   **(Future: Add other operational refinements here, e.g., Terminal CWD strategy, Python execution path, File Access Strategy)**

✧༺❀༻∞ KOIOS - EGOS Standards Authority ∞༺❀༻✧
