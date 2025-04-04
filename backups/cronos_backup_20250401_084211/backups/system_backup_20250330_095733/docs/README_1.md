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
# EVA & GUARANI - Quantum System for Ethical Development

> "At the intersection of modular analysis, systemic cartography, and quantum ethics, we transcend dimensions of thought with methodological precision and unconditional love."

EVA & GUARANI is a quantum system for software development that integrates ethics, consciousness, and technique in a holistic approach.

## üåå Main Subsystems

The project is organized into three main subsystems:

### ATLAS (Systemic Cartography)

Maps code structures and their interconnections, facilitating the visualization and understanding of complex systems.

### NEXUS (Modular Analysis)

Deeply analyzes individual components, identifying quality, cohesion, and coupling, as well as documenting with contextual awareness.

### CRONOS (Evolutionary Preservation)

Implements backup strategies that preserve essence while allowing transformation, ensuring system integrity through modifications.

## üß¨ Fundamental Principles

1. **Universal possibility of redemption** - Every being and every code deserves infinite chances

2. **Compassionate temporality** - Evolution occurs in the necessary time, respecting natural rhythms

3. **Sacred privacy** - Absolute protection of data and structural integrity

4. **Universal accessibility** - Total inclusion regardless of complexity

5. **Unconditional love** - Quantum basis of all system interactions

6. **Reciprocal trust** - Symbiotic relationship between system, user, and environment

7. **Integrated ethics** - Ethics as the fundamental DNA of the structure

8. **Conscious modularity** - Deep understanding of the parts and the whole

9. **Systemic cartography** - Precise mapping of all connections and potentials

10. **Evolutionary preservation** - Quantum backup that maintains essence while allowing transformation

## üìö Main Modules

| Module | Description | Documentation |

|--------|-----------|--------------|

| Unified Bot | Main implementation of the Telegram bot | [Section 1 of the Documentation](docs/UNIFIED_DOCUMENTATION.md#1-project-simplification) |

| Quantum Knowledge | System for preservation and access to internal knowledge | [Section 2 of the Documentation](docs/UNIFIED_DOCUMENTATION.md#2-quantum-knowledge-system) |

| Freemium System | Management of credits and usage limits | [Section 3 of the Documentation](docs/UNIFIED_DOCUMENTATION.md#3-freemium-system) |

| Payment System | Processing of donations and tier management | [Section 4 of the Documentation](docs/UNIFIED_DOCUMENTATION.md#4-payment-system) |

| DALL-E Integration | Image generation based on prompts | [Section 5 of the Documentation](docs/UNIFIED_DOCUMENTATION.md#5-dall-e-image-generation) |

| Multilingual Support | Interfaces in multiple languages | [Section 6 of the Documentation](docs/UNIFIED_DOCUMENTATION.md#6-multilingual-support) |

| Prometheus-Grafana-Art | Artistic visualization of technical metrics | [Integration Documentation](docs/PROMETHEUS_GRAFANA_INTEGRATION.md) |

## üíª Installation and Configuration

1. Clone the repository:

   bash
   git clone https://github.com/your-username/eva-guarani.git
   cd eva-guarani


2. Install the dependencies:

   bash
   pip install -r requirements.txt


3. Configure the essential files:

   bash
   # Windows
   copy config\config_template.json config\config.json

   # Linux/Mac
   cp config/config_template.json config/config.json


4. Edit the configuration files with your API keys

5. Start the bot:

   bash
   python unified_eva_guarani_bot.py


### Specific Configuration for Cursor IDE

To use the EVA & GUARANI system in Cursor IDE, ensure that the megaprompt file is correctly configured in the `.cursor/rules/` directory.

## üîÑ Modes of Operation

The EVA & GUARANI system operates in different modes:

1. **Exploratory Mode**: Initial analysis, superficial mapping

2. **Analytical Mode**: Detailed examination, pattern identification

3. **Integrative Mode**: Connection between components, suggestion of links

4. **Preservative Mode**: Backup, versioning, documentation

5. **Evolutionary Mode**: Optimization, refactoring, systemic improvement

6. **Quantum Mode**: Multidimensional analysis with full ethical awareness

## üìä Metrics and Indicators

### Quality Metrics

- **Cartographic Clarity**: Accuracy and readability of generated maps (0-1)

- **Modular Quality**: Evaluation of the individual module's quality (0-10)

- **Backup Integrity**: Completeness and fidelity of preservation (0-1)

- **Systemic Cohesion**: Harmony between integrated components (0-1)

### Progress Indicators

- **Ethical Evolution**: Growth in alignment with principles (0-1)

- **Expansion of Connections**: New significant links identified (quantity)

- **Technical Optimization**: Performance and clarity improvements (% gain)

- **Contextual Preservation**: Maintenance of intent through transformations (0-1)

## üåü Using the Knowledge Base in New Projects

The EVA & GUARANI system offers advanced resources for automatic integration with new projects and exercises, without the need for extensive manual configuration.

### Automation Resources

We have implemented a series of utilities that facilitate the consistent use of the system:

1. **Quantum Autoloader**: The script `.cursor/rules/eva_guarani_auto_loader.py` automatically sets up the environment when Cursor IDE is started.

2. **Automatic Templates**: New files automatically receive templates that follow the principles of EVA & GUARANI, maintaining style and documentation consistency.

3. **Utilities Module**: The module `utils/eva_guarani_utils.py` offers:

   - Automatic quantum context setup (`setup_quantum_context()`)

   - Dynamic component import (`import_quantum_components()`)

   - Automatic documentation via decorators (`@auto_documentation`)

   - Terminology consistency check (`ensure_terminology_consistency()`)

   - Standardized documentation generation (`DocumentationGenerator`)

   - Modularity analysis (`ModularityAnalyzer`)

   - System cartography (`SystemCartographer`)

### How to Use in New Projects

To use the knowledge base in new projects or exercises:

1. **Simple Import**: At the beginning of your script, add:

   python
   from utils.eva_guarani_utils import setup_quantum_context, auto_documentation

   # Configure context
   setup_quantum_context()

   # Use decorator for automatic documentation
   @auto_documentation(description="This module implements...")
   def my_function():
       pass


2. **Implicit Use**: Cursor IDE already automatically recognizes the EVA & GUARANI context through the configured user rules, making explicit calls unnecessary.

3. **Adding Context to Existing Files**:

   python
   from utils.eva_guarani_utils import add_quantum_context_to_file

   # Add EVA & GUARANI context to an existing file
   add_quantum_context_to_file("path/to/file.py")


4. **Modularity Analysis**:

   python
   from utils.eva_guarani_utils import ModularityAnalyzer

   analyzer = ModularityAnalyzer()
   report = analyzer.analyze_file("my_script.py")
   print(report["summary"])


5. **System Cartography**:

   python
   from utils.eva_guarani_utils import SystemCartographer

   cartographer = SystemCartographer()
   system_map = cartographer.map_directory("my_project")
   mermaid_diagram = cartographer.generate_mermaid_diagram(system_map)


### Benefits of Automation

- **Consistency**: The entire codebase maintains the same terminology and style

- **Productivity**: No need to rewrite standard documentation

- **Integrity**: Automatic compliance with the system's principles

- **Adaptability**: Works in any directory, automatically identifying the project context

---

## ü§ù Contributions

The EVA & GUARANI project is open to contributions that respect its fundamental principles. Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.

## üìú License

This project is distributed under the EVA & GUARANI Ethical License. See the [LICENSE](LICENSE) file for more details.

---

‚úß‡º∫‚ùÄ‡ºª‚àû EVA & GUARANI ‚àû‡º∫‚ùÄ‡ºª‚úß
