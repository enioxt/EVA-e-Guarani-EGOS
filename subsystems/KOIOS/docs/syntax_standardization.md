# KOIOS: Syntax Standardization & Correction Framework

**Version:** 0.1
**Status:** Planned

## Goal

To minimize syntax errors, enforce consistent coding style, and improve code quality across the EGOS project, ensuring compatibility and readability.

## Scope

-   Python (`.py`)
-   Shell Scripts (`.ps1`, `.bat`, `.sh`)
-   Configuration Files (`.json`, `.yaml`, `.toml`)
-   Documentation (`.md`)

## Chosen Tools

-   **Python:**
    -   Linter: `flake8` (Config: `.flake8`)
    -   Formatter: `black` (Config: `pyproject.toml`)
-   **General Formatter:** `prettier` (Config: `.prettierrc`) - For JSON, YAML, MD, etc.
-   **Shell (Bash/SH):** `shellcheck` (Requires separate install/integration)
-   **PowerShell:** `PSScriptAnalyzer` (Integrated with PowerShell)

## Automation Strategy: Pre-Commit Hooks

-   **Primary Mechanism:** Utilize the `pre-commit` framework ([https://pre-commit.com/](https://pre-commit.com/)).
-   **Configuration:** Manage hooks and tool versions in `.pre-commit-config.yaml` in the project root.
-   **Workflow:**
    1.  Developers run `pre-commit install` once in their local repository clone.
    2.  Before each commit, `pre-commit` automatically runs the configured linters and formatters on staged files.
    3.  Formatters (like `black`, `prettier`) automatically fix style issues.
    4.  Linters (`flake8`, `shellcheck`) report errors that need manual correction.
    5.  Commits are prevented if any hooks fail.

## Configuration Files (To Be Verified/Updated)

-   `.flake8`: Ensure rules align with PEP 8 and project conventions.
-   `pyproject.toml`: Verify/Add `[tool.black]` section.
-   `.prettierrc`: Verify/Add configuration for supported file types.
-   `.pre-commit-config.yaml`: Verify/Add hooks for `flake8`, `black`, `prettier`, `shellcheck` (if feasible), etc.

## Immediate Actions

1.  Verify/Update `.pre-commit-config.yaml` to include hooks for `black`, `flake8`, and `prettier`.
2.  Verify/Update corresponding tool configuration files (`.flake8`, `pyproject.toml`, `.prettierrc`).
3.  Document the developer workflow (`pre-commit install`) in the main `README.md` or a `CONTRIBUTING.md` file.

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
