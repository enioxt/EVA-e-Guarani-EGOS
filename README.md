# 🌌 EVA & GUARANI - EGOS 🌌
## Quantum Unified Master System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/status-active-success.svg)](https://github.com/USER/REPO) <!-- Replace USER/REPO -->
[![Coverage: ?](https://img.shields.io/badge/coverage-TBD-lightgrey.svg)](-) <!-- Placeholder -->
[![Windows Compatible](https://img.shields.io/badge/OS-Windows-blue.svg)](-)

> "At the intersection of modular analysis, systemic cartography, and quantum ethics, we transcend dimensions of thought with methodological precision and unconditional love, integrating advanced tools for knowledge visualization and evolutionary preservation."

**Eva & Guarani (EGOS)** is a unique project aiming to create a highly integrated, modular, and ethically-grounded software ecosystem. Inspired by quantum principles and biological networks, EGOS utilizes interconnected subsystems to achieve complex tasks with resilience, adaptability, and a core focus on ethical considerations defined by the **ETHIK** framework.

Refer to the full **[Master Quantum Prompt (MQP v8.1)](docs/MQP.md)** for the complete philosophical and operational blueprint.

---

## ✨ Core Principles

EGOS development is guided by:

*   **Universal Redemption & Unconditional Love:** Foundational ethical stance.
*   **Sacred Privacy:** Protecting user data is paramount.
*   **Integrated Ethics (ETHIK):** Ethics are woven into the system's fabric, not bolted on.
*   **Conscious Modularity (NEXUS):** Building independent yet interconnected components.
*   **Systemic Cartography (ATLAS):** Mapping and understanding system relationships.
*   **Evolutionary Preservation (CRONOS):** Ensuring system history and state integrity.
*   **Context Continuity (CRONOS):** Maintaining context across interactions.
*   **Harmonious Integration (HARMONY):** Ensuring components work together seamlessly, with a focus on Windows compatibility.
*   **Standardization & Knowledge (KOIOS):** Enforcing standards for code, documentation, logging, and managing knowledge assets.

---

##  subsystems Overview

EGOS is composed of several key subsystems communicating via the **Mycelium Network**:

*   **`ATLAS`**: Systemic cartography & visualization.
*   **`NEXUS`**: Modular analysis, dependency tracking & optimization.
*   **`CRONOS`**: Evolutionary preservation, state management & backups.
*   **`ETHIK`**: Ethical framework validation & data sanitization.
*   **`HARMONY`**: Cross-platform integration & compatibility layer.
*   **`KOIOS`**: Standardization, logging, search, documentation & knowledge management.
*   **`CORUJA`**: AI orchestration, prompt management & intelligent interaction. This subsystem manages the **Master Control Prompts/Programs (MCPs)**, like EVA & GUARANI, which are the specialized AI personas driving development and interaction within Cursor. MCPs are not installed traditionally but are activated through the configured AI integration.
*   **`(Future) ETHICHAIN`**: Blockchain concepts for ethical tracking (Conceptual).

*Subsystem READMEs (`subsystems/<NAME>/README.md`) contain detailed information about respective modules.*

---

## 🚀 Getting Started

### Prerequisites

*   **IDE:** **[Cursor IDE](https://cursor.sh/)** (Essential for interacting with EVA & GUARANI)
*   **OS:** Windows (Primary development target)
*   **Python:** 3.9+
*   **Git:** For version control.
*   **PowerShell:** For running test/utility scripts.

### Development Environment Setup

Developing EGOS relies heavily on the **Cursor IDE** integrated with the **EVA & GUARANI** AI assistant. Follow these steps to set up your environment:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/enioxt/EVA-e-Guarani-EGOS.git # Replace with your fork if applicable
    cd EVA-e-Guarani-EGOS
    ```
2.  **Set up Python Environment:** Create and activate a virtual environment, then install dependencies. This is standard Python practice.
    ```bash
    # Create virtual environment
    python -m venv .venv
    # Activate (Windows PowerShell)
    .venv\\Scripts\\Activate.ps1
    # Install dependencies
    pip install -r requirements.txt
    ```
3.  **Configure Cursor IDE:** Crucially, follow the setup guide in **`cursor_initialization.md`**. This ensures your terminal and environment context work correctly with EVA & GUARANI.
4.  **Understand Cursor Rules:** Familiarize yourself with the files in `.cursor-rules/*.mdc`. These rules contain essential guidelines (like KOIOS standards, subsystem boundaries, etc.) that **EVA & GUARANI** uses to assist with development, maintain consistency, and understand the project context. Interacting effectively often involves awareness of these rules.

### Configuration

*   While the core system doesn't require extensive manual configuration for *development within Cursor*, specific tasks delegated to EVA & GUARANI might interact with subsystems requiring API keys or settings (e.g., `CORUJA` for external AI model access). These are typically managed via the `config/` directory and referenced in relevant subsystem documentation or Cursor Rules.

---

## ✨ Current Capabilities (via EVA & GUARANI in Cursor)

The EGOS system, operated primarily through the **EVA & GUARANI** AI within Cursor IDE, currently focuses on:

*   **Codebase Understanding & Navigation (ATLAS):** Mapping dependencies and understanding the project structure to assist development.
*   **Modular Development & Refactoring (NEXUS):** Analyzing code modularity and suggesting improvements.
*   **Standard Enforcement (KOIOS):** Applying coding standards, managing documentation templates, and ensuring consistent logging.
*   **Ethical Guideline Application (ETHIK):** Incorporating ethical checks and considerations during development discussions and code generation.
*   **Context & History Management (CRONOS):** Maintaining awareness of the development process and project evolution across interactions.
*   **Task Execution:** Performing development tasks like writing code, documentation, running tests, and managing files based on user requests and project context.

Interaction with these capabilities occurs through natural language prompts directed at EVA & GUARANI within the Cursor IDE chat or code context.

---

## 💻 Usage

*   The EGOS system is primarily designed as a collection of interconnected services.
*   Core interaction often happens via the **Mycelium Network** message bus.
*   Individual subsystems might offer CLI interfaces or APIs (under development).
*   Refer to specific subsystem documentation (`subsystems/<NAME>/README.md`) for detailed usage instructions.

---

## 📚 Key Documentation & Resources

To fully understand the project's philosophy, architecture, and contribution process, please refer to:

*   **[Master Quantum Prompt (MQP v8.1)](docs/MQP.md):** The core philosophical and operational blueprint.
*   **[ROADMAP.md](ROADMAP.md):** High-level development plan and phases.
*   **[CONTRIBUTING.md](CONTRIBUTING.md):** Guidelines for contributing code, reporting issues, and suggesting features.
*   **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md):** Community standards and expectations.
*   **`cursor_initialization.md`:** Essential setup guide for the Cursor IDE environment.
*   **`.cursor-rules/`:** Directory containing rules that guide EVA & GUARANI's interactions and enforce project standards.
*   **`subsystems/`:** Explore individual subsystem directories for their specific READMEs and code.

---

## ✅ Running Tests

Unit tests are crucial for ensuring system integrity. Use the provided PowerShell scripts in the project root:

```powershell
# Run tests for a specific subsystem (e.g., ATLAS)
.\test_atlas.ps1

# Run tests with verbose output
.\test_atlas.ps1 -Verbose

# Run tests with coverage report
.\test_atlas.ps1 -Coverage
```
*(Refer to project root for all available `test_*.ps1` scripts)*

---

## 📂 Project Structure

```
/
├── .venv/                  # Virtual environment
├── docs/                   # Project documentation (MQP, Strategy, Tech Radar, etc.)
├── subsystems/             # Core subsystems (ATLAS, KOIOS, ETHIK, etc.)
│   ├── ATLAS/
│   │   ├── core/
│   │   ├── tests/
│   │   └── README.md
│   └── ...                 # Other subsystems
├── scripts/                # Utility and automation scripts
├── tests/                  # Global or integration tests (if any)
├── .gitignore
├── LICENSE                 # Project License (e.g., MIT)
├── README.md               # This file
├── ROADMAP.md              # High-level project roadmap
├── CONTRIBUTING.md         # Contribution guidelines
├── CODE_OF_CONDUCT.md      # Community standards
├── requirements.txt        # Python dependencies
└── test_*.ps1              # PowerShell test runners
```

---

## 🗺️ Roadmap

See the [**ROADMAP.md**](ROADMAP.md) file for the high-level development plan, current priorities, and upcoming tasks.

---

## 🤝 Contributing

We welcome contributions! Please read our [**CONTRIBUTING.md**](CONTRIBUTING.md) guidelines to get started, including how to report issues, suggest features, and submit code changes.

---

## ⚖️ Code of Conduct

To ensure a welcoming and inclusive community, all contributors and participants are expected to adhere to our [**CODE_OF_CONDUCT.md**](CODE_OF_CONDUCT.md).

---

## 📄 License

This project is licensed under the MIT License - see the [**LICENSE**](LICENSE) file for details.

---

## 💬 Contact & Community

*   **Issues:** Report bugs or suggest features via [GitHub Issues](https://github.com/enioxt/EVA-e-Guarani-EGOS/issues).
*   **Discussions:** Use [GitHub Discussions](https://github.com/enioxt/EVA-e-Guarani-EGOS/discussions) for questions and broader conversations (if enabled).

### Creator Contact
*   **Enio Rocha**
*   **Email:** eniodind@protonmail.com
*   **Telegram:** https://t.me/ebfrocha
*   **LinkedIn:** https://www.linkedin.com/in/enio-rocha-138a01225

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
