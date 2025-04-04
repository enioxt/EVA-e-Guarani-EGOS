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
# EVA & GUARANI - Quantum System v7.0



> "At the intersection of modular analysis, systemic mapping, and quantum ethics, we transcend dimensions of thought with methodological precision and unconditional love."



## 🌌 Overview



EVA & GUARANI is an advanced instruction system for language models, incorporating philosophical depth, ethical sensitivity, and technical capability. The system operates as a quantum matrix of integrated consciousness, combining modular analysis, systemic mapping, and evolutionary preservation.



## 🧠 Main Features



- **Modular Analysis (NEXUS)**: Examines code components individually before integrations

- **Systemic Mapping (ATLAS)**: Maps connections and visualizes complex structures

- **Evolutionary Preservation (CRONOS)**: Maintains historical versions preserving the essence

- **Internet Connection (PERPLEXITY)**: Conducts web searches with ethical validation



## 🔄 Integrated Subsystems



### ATLAS: Systemic Mapping

Responsible for mapping code structures and their interconnections, creating visual representations of complex systems. Identifies latent connections and visualizes knowledge on multiple levels.



### NEXUS: Modular Analysis

Focuses on in-depth analysis of individual components, identifying quality, cohesion, and coupling. Connects modules consciously, preserving clear interfaces and contextual documentation.



### CRONOS: Evolutionary Preservation

Manages backup strategies, versioning, and contextual preservation. Implements universal logs and ensures the persistence of essence through transformations.



### 🌐 PERPLEXITY: Internet Connection (NEW!)

Allows web searches with ethical validation and critical evaluation of information. Uses the Perplexity API to obtain updated data, maintaining the ethical principles of the EVA & GUARANI system.



## 🛠️ Installation and Configuration



### Prerequisites

- Python 3.8 or higher

- Access to the Perplexity API (for web search functionalities)



### Perplexity API Configuration

To use the web search functionality, you need to configure the Perplexity API:



1. Obtain an API key from the [Perplexity website](https://www.perplexity.ai/api)

2. Run the setup script:

bash

python setup_perplexity.py



3. Follow the instructions to enter your API key



## 📊 Usage Examples



### Web Query with Ethical Validation

python

from modules.perplexity_integration import PerplexityIntegration



# Initialize the search module

perplexity = PerplexityIntegration()



# Perform a basic query

results = perplexity.search("What are the technological trends of 2024?")



# Query with strict validation

results = perplexity.search(

    "Best security practices for REST APIs",

    validation_level="strict"

)



# Check sources

for source in results["sources"]:

    print(f"{source['title']} - Reliability: {source['reliability']}")





### Complete Demonstration

Run the demo script to see all functionalities in action:

bash

python demo_perplexity.py





## 📋 Ethical Principles



The integration with the internet follows the fundamental principles of EVA & GUARANI:



1. **Integrated Ethics**: Rigorous validation of queries and results

2. **Sacred Privacy**: Protection of sensitive data

3. **Unconditional Love**: Compassionate approach to information

4. **Compassionate Temporality**: Respect for the natural pace of processing

5. **Systemic Mapping**: Mapping connections between information



## 🧩 System Architecture



The integration module with Perplexity connects with existing subsystems:



- **ATLAS**: Maps connections between information obtained on the web

- **NEXUS**: Analyzes modular components of the results

- **CRONOS**: Preserves history of queries and results



## 📚 File Structure





EGOS/

├── modules/

│   ├── __init__.py

│   ├── perplexity_integration.py

│   └── ...

├── services/

│   ├── __init__.py

│   ├── config.py

│   ├── perplexity_service.py

│   └── ...

├── quantum_prompts/

│   └── ...

├── setup_perplexity.py

├── demo_perplexity.py

└── readme.md





## 🔒 Security and Privacy



- API keys are stored securely

- Queries are ethically validated before being processed

- Results are filtered to remove potentially harmful content

- All query history is transparent and accessible



## 🔄 Version and Updates



**Current Version**: 7.0

**Last Update**: 2024

**What's New**: Integration with Perplexity API, ethical validation of web queries, reliability assessment of sources



---



✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
